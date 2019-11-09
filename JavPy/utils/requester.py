import threading
from threading import Event
from JavPy.utils.common import try_evaluate
import time


class Master:
    def __init__(self, num_threads):
        self.workers = [Worker(self) for i in range(num_threads)]
        self.semaphore = threading.BoundedSemaphore(num_threads)
        for worker in self.workers:
            worker.start()

    def wait_for_run(self, task):
        self.semaphore.acquire(True)
        for t in self.workers:
            if not t.event.is_set():
                t.do(task)
                break
        else:
            raise Exception("No free worker.")

    def spawn(self, target, *args, **kwargs):
        task = Task(target, *args, **kwargs)
        self.wait_for_run(task)
        return task

    def spawn_many(self, tasks):
        task_group = _TaskGroup(list(tasks))
        for task in task_group.tasks:
            self.wait_for_run(task)
        return task_group


class Worker(threading.Thread):
    def __init__(self, master):
        threading.Thread.__init__(self)
        self.event = Event()
        self.task = None
        self.master = master

    def run(self):
        while True:
            self.event.wait()
            self.task.status = Task.RUNNING
            self.task.result, ex = try_evaluate(
                lambda: self.task.target(*self.task.args, **self.task.kwargs)
            )
            if ex and self.task.catch_cb:
                self.task.catch_cb(ex)
                self.task.status = Task.FAILED
            elif self.task.then_cb:
                self.task.then_cb(self.task.result)
            if self.task.result is not None:
                self.task.status = Task.SUCCESS
            else:
                self.task.status = Task.FAILED

            if self.task.task_group:
                self.task.task_group.finished_cnt += 1
                if self.task.status == Task.FAILED:
                    self.task.task_group.failed_cnt += 1
                else:
                    self.task.task_group.success_cnt += 1
            self.event.clear()
            self.master.semaphore.release()

    def do(self, task):
        self.task = task
        self.event.set()


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
        self.task_group = None

    def wait_for_result(self):
        while self.status % 2:
            time.sleep(0.1)
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


class _TaskGroup:
    def __init__(self, tasks):
        self.tasks = tasks

        for task in self.tasks:
            task.task_group = self

        self.one_complete_cb = None
        self.all_complete_cb = None
        self.catch_cb = None
        self.on_timeout_cb = None
        self.finished_cnt = 0
        self.success_cnt = 0
        self.failed_cnt = 0
        self.n_tasks = len(self.tasks)

    def __gather_results(self):
        res = tuple((task.result for task in self.tasks))
        return res

    def wait_for_all_finished(self):
        while self.n_tasks != self.finished_cnt:
            time.sleep(0.2)
        return self.__gather_results()

    def wait_until(self, condition):
        while not time.sleep(0.1):
            for task in self.tasks:
                if task.status % 2:
                    continue
                res = task.result
                if res is not None and condition(res):
                    return self.__gather_results()
            if self.finished_cnt == self.n_tasks:
                return self.__gather_results()

    def wait_for_one_finished(self):
        return self.wait_until(lambda x: True)

    def wait_for(self, success_cnt):
        while not time.sleep(0.1):
            if success_cnt == self.success_cnt or self.n_tasks == self.finished_cnt:
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


__master_thread_started = False
__global_master = None


def __master_thread():
    global __global_master
    __global_master = Master(20)


def start_master_thread():
    global __master_thread_started
    if __master_thread_started:
        return
    __master_thread_started = True
    master = threading.Thread(target=__master_thread)
    master.setDaemon(True)
    master.start()


start_master_thread()

while not __global_master:
    pass
spawn = __global_master.spawn
spawn_many = __global_master.spawn_many
