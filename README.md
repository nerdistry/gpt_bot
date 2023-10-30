#  *AgriSense WhatsApp Bot*
*Welcome to the AgriSense WhatsApp Bot Repo!!*  
This is a FastAPI application that integrates with various services to create a chatbot powered by OpenAI's GPT-3.5 Turbo model. The chatbot can respond to incoming messages and process images sent by users via a WhatsApp integration.

# *Requirements*  
Before you can use this application, you'll need to have the following requirements in place:

- FastAPI
- Uvicorn (for running the FastAPI server)  
- Twilio (for receiving WhatsApp messages)  
- OpenAI (for generating text responses)  
- python-decouple (for managing configuration)  
- SQLAlchemy (for database interactions)  
- psycopg2-binary (PostgreSQL database driver)  
- python-multipart (for handling file uploads)  
- pyngrok (optional, for exposing the FastAPI server over the internet)

# *Installation*  
Clone the repository:

bash
git clone https://github.com/your/repository.git
cd your-repo-directory  


Create a virtual environment and activate it (optional but recommended):

bash
python -m venv venv
source venv/bin/activate

On Windows, use
bash
venv\Scripts\activate
 
Install the required packages:

bash
pip install -r requirements.txt

Configure the application by creating a .env file and setting the necessary environment variables.  
Set up a PostgreSQL database for storing conversation data.  
Run the FastAPI application:

bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# *Configuration*
The application uses environment variables for configuration. Create a .env file in the root directory of the application and set the following variables:  

markdown 
OPENAI_API_KEY: Your OpenAI API key.
TWILIO_ACCOUNT_SID: Your Twilio account SID.
TWILIO_AUTH_TOKEN: Your Twilio authentication token.
DB_USER: Your PostgreSQL database username.
DB_PASSWORD: Your PostgreSQL database password.


# *Usage*
The FastAPI application listens for incoming requests at the root URL ("/").  
WhatsApp messages should be sent to the /message endpoint via a POST request.  
The message content can be provided as a form field named "Body," and image URLs can be provided as a form field named "MediaUrl0."  
The application uses OpenAI's GPT-3.5 Turbo model to generate responses to text messages.  
If an image is received, the application processes it by calculating image attributes (mean intensity, standard deviation, and edge density) and responds with the results.

Make sure to fill in the actual values for each of these variables

# *Database*
This application uses a PostgreSQL database to store conversations. It utilizes SQLAlchemy for database interaction.  
The conversation data is stored in a table named "gpt_conversation."   
The database connection details should be configured in the .env file as mentioned in the Configuration section.  

You can access the conversation data from the database as needed for analysis or reporting.

# *Dependencies*
This application relies on several external libraries and services, including:  

- FastAPI: A modern web framework for building APIs.
- Uvicorn: A lightweight ASGI server for running FastAPI applications.
- Twilio: A cloud communications platform for integrating WhatsApp messaging.
- OpenAI: A platform for natural language processing and text generation.
- python-decouple: A library for managing configuration in a .env file.
- SQLAlchemy: An ORM for Python used to interact with the PostgreSQL database.
- psycopg2-binary: A PostgreSQL database adapter.
- python-multipart: A library for handling file uploads in FastAPI.
- pyngrok (optional): A utility for exposing local servers over the internet (useful for development and testing).

Make sure to install and configure these dependencies as mentioned in the Requirements and Configuration sections.
