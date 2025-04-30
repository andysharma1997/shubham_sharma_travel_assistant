# 🧠 Smart Travel Agentic Assistant

This is a **Smart Travel Agentic Assistant**, built with Streamlit, Langchain and Python 3.10.

The assistant helps you **plan your trip effortlessly** by providing:

- 🌍 **Travel destination recommendations**
- ✈️ **Flight price checking**
- 🗓️ **Itinerary planning**
- 📸 **Suggestions for top tourist spots**

It’s designed to make travel planning smarter, faster, and more intuitive.


---

## 🚀 Running the App

### 🔹 Option 1: Run Locally with CLI

1. Make sure Python 3.10+ and pip are installed.
2. Create a virtualenv
   ```bash
   python -m venv .venv
3. Activate the virtualenv
   ```bash
   source venv/bin/activate

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
5. Create a .env file.
6. Add your OPENAI_API_KEY in the .env
7. Run the Streamlit app:
   ```bash
   streamlit run main.py
8. Open the Smart Travel Bot UI in browser
   ```bash
   http://localhost:8501/

### 🔹 Option 2: Run Locally with Docker
1. Make sure docker is installed and is updated.
2. Change the directory to shubham_sharma_travel_assistant
   ```bash
   cd shubham_sharma_travel_assistant
3. Build the docker image
   ```bash
   docker build -t smart_travel_assistant:latest .
4. Run the container
   ```bash
   docker run -p 8501:8501 -e OPENAI_API_KEY=<YOUR_OPENAI_API_KEY> -d --name assitant smart_travel_assistant:latest
5. To check the logs run the below command
   ```bash
   docker logs -f assitant
6. Open the Smart Travel Bot UI in browser
   ```bash
   http://localhost:8501/


## 👤 Author
**Shubham Sharma**
