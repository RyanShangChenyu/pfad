from diffusers import DiffusionPipeline
import torch
print(torch.__version__)

model = "runwayml/stable-diffusion-v1-5"

pipe = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16)


pipe.to("cpu")

while True:
    prompt = input("Type a prompt and press enter to generate an image:\n>>> ")
    images = pipe(prompt, num_inference_steps=5).images
    images[0].show()
