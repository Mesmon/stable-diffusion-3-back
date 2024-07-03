from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import image_routes
from dotenv import load_dotenv
from queue_manager import queue_cleanup_shutdown

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

app.include_router(image_routes.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    queue_cleanup_shutdown()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
