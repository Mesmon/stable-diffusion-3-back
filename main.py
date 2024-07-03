from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import torch
from diffusers import StableDiffusion3Pipeline
import uuid
import os

class PromptRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    num_inference_steps: int = 50
    height: int = 512
    width: int = 512
    guidance_scale: float = 7.5
    max_sequence_length: int = 512

app = FastAPI()

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3-medium-diffusers",
    text_encoder_3=None,
    tokenizer_3=None,
    torch_dtype=torch.float16
)
pipe.to("cuda")

@app.post("/generate-image/")
async def generate_image(request: PromptRequest):
    try:
        image = pipe(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            num_inference_steps=request.num_inference_steps,
            height=request.height,
            width=request.width,
            guidance_scale=request.guidance_scale,
            max_sequence_length=request.max_sequence_length,
        ).images[0]
        
        image_id = str(uuid.uuid4())
        image_path = f"images/{image_id}.png"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image.save(image_path)
        return FileResponse(image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
