import time

from multiprocessing import Lock, Process, current_process


class Task(object):
    @property
    def __pid(self):
        return current_process().pid

    @property
    def __process_name(self):
        return current_process().name

    def __call__(self, name: str, lock: Lock()):
        print(f'Task "{name}" started')

        try:
            while True:
                with lock:
                    print(f'{self.__process_name}. task: {name}, pid: {self.__pid}')

                time.sleep(2)
        except KeyboardInterrupt:
            pass

        print(f'Task "{name}" stopped')


if __name__ == '__main__':
    lock = Lock()
    tasks = [Task() for _ in range(4)]
    processes = [Process(target=task, args=(f'Task_{index}', lock)) for index, task in enumerate(tasks)]

    try:
        for process in processes:
            process.start()

        for process in processes:
            process.join()
    except KeyboardInterrupt:
        pass


