from services.generate_image import generate_image_function
from models import PromptRequest
from queue import Queue
from threading import Thread

task_queue = Queue()

def task_worker():
    while True:
        task = task_queue.get()
        if task is None:
            break
        task()
        task_queue.task_done()

worker_thread = Thread(target=task_worker)
worker_thread.start()

def add_to_queue(request: PromptRequest):
    task_queue.put(lambda: generate_image_function(request))


def queue_cleanup_shutdown():
    task_queue.put(None)
    worker_thread.join()