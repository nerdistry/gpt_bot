# Third-party imports
import openai
from fastapi import FastAPI, Form, Depends, Request, UploadFile, File
from decouple import config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import requests
from io import BytesIO
from PIL import Image
from requests.auth import HTTPBasicAuth
from skimage import io, color, filters
import numpy as np


# Internal imports
from models import Conversation, SessionLocal
from utils import send_message, logger

app = FastAPI()
# Set up the OpenAI API client
openai.api_key = config("OPENAI_API_KEY")

TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return {"msg": "working"}


@app.post("/message")
async def reply(request: Request, Body: str = Form(""), MediaUrl0: str = Form(None), db: Session = Depends(get_db)):
    # Extract the phone number from the incoming webhook request
    form_data = await request.form()
    whatsapp_number = form_data['From'].split("whatsapp:")[-1]

    response_message = ""

    logger.info(f"Incoming message body: {Body}")
    logger.info(f"Media URL: {MediaUrl0}")

    # Check if an image is sent
    if MediaUrl0:
        try:
            # Download the image
            response = requests.get(MediaUrl0, timeout=10, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))  # Increase timeout to 10 seconds
            print(response.content[:100])

            if response.status_code == 200:
                # Read the image with scikit-image
                image = io.imread(BytesIO(response.content))

                # Convert the image to grayscale
                gray_image = color.rgb2gray(image)

                # Calculate the mean and standard deviation of the image's intensity
                mean_intensity = np.mean(gray_image)
                std_intensity = np.std(gray_image)

                # Detect edges using the Sobel filter
                edges = filters.sobel(gray_image)

                # Calculate the percentage of edge pixels (this is a very basic edge density measure)
                edge_density = np.sum(edges > 0.1) / edges.size

                response_message = (f"Image attributes:\n"
                                    f"- Mean Intensity: {mean_intensity:.2f}\n"
                                    f"- Intensity Standard Deviation: {std_intensity:.2f}\n"
                                    f"- Edge Density: {edge_density:.2%}")

            else:
                response_message = "Failed to download the image."
        except Exception as e:
            logger.error(f"Error processing image: {str(e)} - Response content: {response.content[:500]}")
            response_message = "Sorry, I couldn't process the image."
        print("Media URL:", MediaUrl0)
        logger.info("Media URL: %s", MediaUrl0)

    else:
        # Call the OpenAI API to generate text with ChatGPT
        messages = [{"role": "user", "content": Body}]
        messages.append({"role": "system",
                         "content": "You're a farming expert, you have founded many agricultural organization and know a lot about it. You understand nothing but agriculture."})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5
        )

        # The generated text
        chatgpt_response = response.choices[0].message.content
        logger.info(f"OpenAI Response: {chatgpt_response}")

        # Store the conversation in the database
        try:
            conversation = Conversation(
                sender=whatsapp_number,
                message=Body,
                response=chatgpt_response
            )
            db.add(conversation)
            db.commit()
            logger.info(f"Conversation #{conversation.id} stored in database")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error storing conversation in database: {e}")

        response_message = chatgpt_response

    # Send response message
    send_message(whatsapp_number, response_message)
    return ""
