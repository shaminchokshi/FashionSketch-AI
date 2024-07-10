from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

class ImageRequest(BaseModel):
    description: str

# OpenAI API configuration
OPENAI_API_KEY = "sk-proj-eUCM3NI5rNjPgBMOtLcUT3BlbkFJxdGDErpnEv5182Oad7Cf"
openai.api_key = OPENAI_API_KEY

def generate_image(prompt: str):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-groom/")
def generate_groom(request: ImageRequest):
    prompt = request.description
    image_url = generate_image(prompt)
    return {"image_url": image_url}

@app.post("/generate-bride/")
def generate_bride(request: ImageRequest):
    prompt = request.description
    image_url = generate_image(prompt)
    return {"image_url": image_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
