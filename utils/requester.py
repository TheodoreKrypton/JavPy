import threading
from threading import Lock
from utils.common import try_evaluate
try:
    from typing import Dict
except ImportError:
    pass


class Master:
    results = {}
    __result_lock = Lock()

    MAX_WORKER = 20

    __task_id = 0
    __q_lock = Lock()
    __waiting_for_run = []

    workers = {}  # type: Dict[int, Worker]
    __workers_lock = Lock()

    @classmethod
    def get_result(cls, task_id):
        with cls.__result_lock:
            if task_id in cls.results:
                return cls.results[task_id]
            else:
                return None

    @classmethod
    def del_result(cls, task_id):
        with cls.__result_lock:
            if task_id in cls.results:
                del cls.results[task_id]
            else:
                return

    @classmethod
    def __spawnable(cls):
        return not cls.__workers_lock.locked() and len(cls.workers) <= cls.MAX_WORKER

    @classmethod
    def wait_for_run(cls, task):
        with cls.__q_lock:
            cls.__task_id += 1
            task.id = cls.__task_id
            cls.__waiting_for_run.append(task)

    @classmethod
    def finish_task(cls, task_id):
        with cls.__workers_lock:
            del cls.workers[task_id]

    @classmethod
    def master_thread(cls):
        while True:
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


master = threading.Thread(target=Master.master_thread)
master.daemon = True
master.start()


class Task:
    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.completed = False
        self.id = None
        self.then_cb = None
        self.catch_cb = None
        self.on_timeout_cb = None

    def wait_for_result(self):
        while self.id not in Master.results:
            pass
        res = Master.get_result(self.id)
        Master.del_result(self.id)
        return res

    def then(self, callback):
        self.then_cb = callback
        return self

    def catch(self, callback):
        self.catch_cb = callback
        return self

    def on_timeout(self, callback):
        self.on_timeout_cb = callback
        return self


class TaskGroup:
    def __init__(self, tasks):
        self.tasks = tasks
        self.one_complete_cb = None
        self.all_complete_cb = None
        self.catch_cb = None
        self.on_timeout_cb = None

    def __kill_all_threads(self):
        for task in self.tasks:
            if task.id in Master.workers and Master.workers[task.id].is_alive():
                Master.workers[task.id].terminate()
            if task.id in Master.results:
                Master.del_result(task.id)

    def wait_for_one_complete(self):
        while True:
            completed = 0
            for task in self.tasks:
                if task.id in Master.results:
                    completed += 1
                    res = Master.get_result(task.id)
                    if res is not None:
                        self.__kill_all_threads()
                        return res
            if completed == self.tasks:
                self.__kill_all_threads()
                return None

    def wait_for_all_complete(self):
        while len(self.tasks) != sum(map(lambda x: x.id in Master.results, self.tasks)):
            pass
        return tuple(map(lambda x: Master.get_result(x.id), self.tasks))

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
    task_group = TaskGroup(tasks)
    for task in tasks:
        Master.wait_for_run(task)
    return task_group


class Worker(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task
        self._stop_event = threading.Event()

    def run(self):
        Master.results[self.task.id], ex = try_evaluate(lambda: self.task.target(*self.task.args, **self.task.kwargs))
        Master.finish_task(self.task.id)
        if ex and self.task.catch_cb:
            self.task.catch_cb(ex)
        elif self.task.then_cb:
            res = Master.get_result(self.task.id)
            self.task.then_cb(res)

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
        .wait_for_all_complete()
