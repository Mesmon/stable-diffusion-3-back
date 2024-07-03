from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    num_inference_steps: int = 50
    height: int = 512
    width: int = 512
    guidance_scale: float = 7.5
    max_sequence_length: int = 512
