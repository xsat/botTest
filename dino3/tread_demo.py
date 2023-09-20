from threading import Thread
from time import sleep, time
from queue import Queue


SIGNAL_1: int = 1
SIGNAL_2: int = 2


def tread_demo() -> None:
    def work1(queue: Queue) -> None:
        while True:
            start_time: float = time()
            value = queue.get()

            if value:
                print(f'GET {value}')

            print('work1 iteration is %s seconds' % (time() - start_time))

    def work2(name: str, seconds: int, signal_id: int, queue: Queue) -> None:
        while True:
            start_time: float = time()
            print(f'work2 is sleeping {seconds} second in {name}')
            queue.put(signal_id)
            queue.task_done()
            sleep(seconds)
            print(f'work2 iteration in {name} is %s seconds' % (time() - start_time))

    work_queue: Queue = Queue()

    work1_thread: Thread = Thread(target=work1, daemon=False, args=(work_queue, ))
    work2_thread: Thread = Thread(target=work2, daemon=True, args=('A', 3, SIGNAL_1, work_queue))
    work3_thread: Thread = Thread(target=work2, daemon=True, args=('B', 6, SIGNAL_2, work_queue))

    work1_thread.start()
    work2_thread.start()
    work3_thread.start()

    work_queue.join()
    work1_thread.join()
    work2_thread.join()
    work3_thread.join()


if __name__ == '__main__':
    tread_demo()
