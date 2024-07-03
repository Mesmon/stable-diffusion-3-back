import torch
from diffusers import StableDiffusion3Pipeline
import uuid
import os
from models import PromptRequest
from supabase import create_client, Client
from dotenv import load_dotenv
from huggingface_hub import login

load_dotenv()  # Load environment variables from .env file

huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

# Login to Hugging Face
login(token=huggingface_token)

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3-medium-diffusers",
    text_encoder_3=None,
    tokenizer_3=None,
    torch_dtype=torch.float16
)
pipe.to("cuda")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_client: Client = create_client(supabase_url, supabase_key)

def generate_image_function(request: PromptRequest):
    image = pipe(
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        num_inference_steps=request.num_inference_steps,
        height=request.height,
        width=request.width,
        guidance_scale=request.guidance_scale,
    ).images[0]
    
    image_id = str(uuid.uuid4())
    image_path = f"images/{image_id}.png"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    image.save(image_path)
    
    with open(image_path, "rb") as file:
        content = file.read()
        res = supabase_client.storage.from_('stable-diffusion-results').upload(f"{image_id}.png", content)
    
    if res.status_code == 200:
        os.remove(image_path)
        print(f"Uploaded image to Supabase: {image_id}.png")
    else:
        raise Exception("Failed to upload image to Supabase")
