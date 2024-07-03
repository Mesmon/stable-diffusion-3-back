import asyncio
from services.generate_image import generate_image_function
from models import PromptRequest

request_queue = asyncio.Queue()
processing = False

async def process_queue():
    global processing
    while True:
        request = await request_queue.get()
        if request is None:
            break
        try:
            generate_image_function(request)
        except Exception as e:
            print(f"Error processing request: {e}")
        finally:
            request_queue.task_done()
            processing = False

def add_to_queue(request: PromptRequest):
    global processing
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(request_queue.put_nowait, request)
    if not processing:
        processing = True
        asyncio.create_task(process_queue())
