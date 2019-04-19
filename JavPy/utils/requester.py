from __future__ import absolute_import, print_function, unicode_literals
import threading
from threading import Lock
from JavPy.utils.common import try_evaluate
try:
    from typing import Dict
except ImportError:
    pass
import time

"""
                                       Lifecycle of a Task:
                                       
       -------------------------------------------------------
       | Construct a Task with target function and arguments |------(Task: (target, args, kwargs))
       -------------------------------------------------------                   ^
                                v                                                |
     __task_id_generator   -->  v   Wait for task id generator              [Task Queue]
                                v                                                |
                        ------------------                                       v
                        | Gain a task id |----------------------(Task: (target, args, kwargs), task_id)
                        ------------------
                                v
              MAX_WORKER   -->  v   Wait for len(workers) < MAX_WORKER
                                v
               -------------------------------------
               | Construct a Worker to do the task |--------------(Worker: Task); len(workers) += 1
               -------------------------------------                             ^
                                v                                                |
           remote server   -->  v   Wait for response                            |
                                v                                         [Worker Dict]
                       --------------------                                      |
                       | Get the response |                                      |
                -----------------------------------                              v
                | Set task.result, delete worker  |---------------------  len(workers) -= 1
     ------------------------------------------------------------                
     [Exception ][ Use rsp through cb ][ Get result through wait]                
     ------------------------------------------------------------                
          v                 v                      v                             
          v                 v                      v                     
          v                 v                      v
         catch             then               gather_result
         

    All the requester tasks are owned by the Master thread

"""


def _get_a_task_id():
    task_id = 0
    while True:
        task_id += 1
        yield task_id


class Master:
    __waiting_for_run = []
    __q_lock = Lock()

    MAX_WORKER = 20
    workers = {}  # type: Dict[int, Worker]
    __workers_lock = Lock()

    __task_id_generator = _get_a_task_id()

    @classmethod
    def get_a_task_id(cls):
        return next(cls.__task_id_generator)

    @classmethod
    def __spawnable(cls):
        return not cls.__workers_lock.locked() and len(cls.workers) <= cls.MAX_WORKER

    @classmethod
    def wait_for_run(cls, task):
        with cls.__q_lock:
            task.id = next(cls.__task_id_generator)
            cls.__waiting_for_run.append(task)

    @classmethod
    def finish_task(cls, task_id):
        with cls.__workers_lock:
            if task_id in Master.workers:
                if Master.workers[task_id].is_alive():
                    Master.workers[task_id].terminate()
                del cls.workers[task_id]

    @classmethod
    def master_thread(cls):
        while True:
            time.sleep(0.1)
            if not cls.__waiting_for_run:
                continue
            while not cls.__spawnable():
                pass
            with cls.__workers_lock:
                task = cls.__waiting_for_run[0]
                with cls.__q_lock:
                    del cls.__waiting_for_run[0]
                cls.workers[task.id] = Worker(task)
                cls.workers[task.id].start()


__master_thread_started = False


def start_master_thread():
    global __master_thread_started
    if __master_thread_started:
        return
    __master_thread_started = True
    master = threading.Thread(target=Master.master_thread)
    master.setDaemon(True)
    master.start()


start_master_thread()


class Task:
    SUCCESS = 0
    NOT_STARTED = 1
    FAILED = 2
    RUNNING = 3

    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.id = None
        self.then_cb = None
        self.catch_cb = None
        self.on_timeout_cb = None
        self.result = None
        self.status = Task.NOT_STARTED

    def finished(self):
        return not self.status % 2

    def wait_for_result(self):
        while not self.finished():
            pass
        return self.result

    def then(self, callback):
        self.then_cb = callback
        return self

    def catch(self, callback):
        self.catch_cb = callback
        return self

    def on_timeout(self, callback):
        self.on_timeout_cb = callback
        return self


class __TaskGroup:
    def __init__(self, tasks):
        self.tasks = tasks
        self.one_complete_cb = None
        self.all_complete_cb = None
        self.catch_cb = None
        self.on_timeout_cb = None

    def __gather_results(self):
        res = tuple((task.result for task in self.tasks))
        return res

    def __finished_cnt(self):
        res = sum(map(lambda x: x.finished(), self.tasks))
        return res

    def __failed_cnt(self):
        return sum(map(lambda x: x.status == Task.FAILED, self.tasks))

    def __success_cnt(self):
        return sum(map(lambda x: x.status == Task.SUCCESS, self.tasks))

    def wait_for_all_finished(self):
        while len(self.tasks) != self.__finished_cnt():
            pass
        return self.__gather_results()

    def wait_until(self, condition):
        while True:
            for task in self.tasks:
                if task.status % 2:
                    continue
                res = task.result
                if res is not None and condition(res):
                    return self.__gather_results()
            if self.__finished_cnt() == len(self.tasks):
                return self.__gather_results()

    def wait_for_one_finished(self):
        return self.wait_until(lambda x: True)

    def wait_for(self, success_cnt):
        while True:
            if success_cnt == self.__success_cnt() or len(self.tasks) == self.__finished_cnt():
                return self.__gather_results()

    def on_one_complete(self, callback):
        for task in self.tasks:
            task.then(callback)
        return self

    def on_all_complete(self, callback):
        self.all_complete_cb = callback
        return self

    def catch(self, callback):
        self.catch_cb = callback
        return self

    def on_timeout(self, callback):
        self.on_timeout_cb = callback
        return self


def spawn(target, *args, **kwargs):
    task = Task(target, *args, **kwargs)
    Master.wait_for_run(task)
    return task


def spawn_many(tasks):
    task_group = __TaskGroup(list(tasks))
    for task in task_group.tasks:
        Master.wait_for_run(task)
    return task_group


class Worker(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task
        self._stop_event = threading.Event()

    def run(self):
        self.task.status = Task.RUNNING
        self.task.result, ex = try_evaluate(lambda: self.task.target(*self.task.args, **self.task.kwargs))
        Master.finish_task(self.task.id)
        if ex and self.task.catch_cb:
            self.task.catch_cb(ex)
            self.task.status = Task.FAILED
        elif self.task.then_cb:
            res = self.task.result
            self.task.then_cb(res)
        if self.task.result is not None:
            self.task.status = Task.SUCCESS
        else:
            self.task.status = Task.FAILED

    def terminate(self):
        self._stop_event.set()


if __name__ == '__main__':
    import requests

    def cb(res):
        print(res)

    def err_handler(ex):
        print(ex)
        print(ex.with_traceback())

    spawn_many([Task(requests.get, "http://www.baidu.com") for x in range(0, 100)])\
        .on_one_complete(cb)\
        .wait_for_all_finished()
