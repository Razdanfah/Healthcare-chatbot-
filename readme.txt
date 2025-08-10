# Heart Health Chatbot (FastAPI Version)

A web-based chatbot that provides information about heart health using the Gemini AI model from Google, built with FastAPI.

## Features

- Interactive chat interface for heart health questions
- Powered by Google's Gemini AI model
- Built with FastAPI for high performance
- Responsive design that works on desktop and mobile
- Session-based conversations with persistence
- Animated heartbeat logo
- Medical disclaimer
- Automatic API documentation via Swagger UI

## Prerequisites

- Python 3.7+
- Google API key for Gemini AI

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd heart-health-chatbot
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your Google API key: `GOOGLE_API_KEY=your_gemini_api_key_here`

## Project Structure

```
heart-health-chatbot/
├── main.py                 # FastAPI application
├── static/
│   ├── css/
│   │   └── style.css       # Stylesheet
│   └── js/
│       └── script.js       # Frontend JavaScript
├── templates/
│   └── index.html          # HTML template
├── .env                    # Environment variables (create this)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Running the Application

1. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```
   
   Or simply run:
   ```
   python main.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

3. For API documentation, visit:
   ```
   http://127.0.0.1:8000/docs
   ```

## How to Use

1. Type your heart health question in the text area
2. Press Enter or click the send button
3. The chatbot will respond with relevant information
4. Continue the conversation as needed
5. Your session is preserved in local storage

## Customization

- Modify the `SYSTEM_PROMPT` in `main.py` to change the chatbot's behavior
- Edit the CSS in `static/css/style.css` to change the appearance
- Update the HTML in `templates/index.html` to modify the layout

## Important Notes

- This chatbot provides general information only and is not a substitute for professional medical advice
- Always direct users to consult healthcare providers for personal medical guidance

## Advantages of FastAPI

- Faster performance compared to Flask
- Built-in request validation via Pydantic models
- Automatic API documentation with Swagger UI
- WebSocket support (for potential real-time features)
- Asynchronous request handling
- Type hints throughout the codebase