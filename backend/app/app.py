from flask import Flask, request, jsonify
from pymongo import MongoClient
from app.services.factories.ai_factory import AIFactory
from app.services.factories.search_factory import SearchFactory
from app.utils.ai_instructions import assistant_instructions, has_no_answer_token, assistant_prompt
from app.utils.session_manager import get_session_id, get_session_thread, get_current_session_id, set_session_thread
from config import Config
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize services using factories
ai_service = AIFactory.create_ai_service("openai")
search_service = SearchFactory.create_search_service("google")

# Initialize MongoDB
client = MongoClient(Config.MONGO_URI)
db = client.get_database()
chat_logs = db.chat_logs


@app.before_request
def ensure_session_id():
    if request.is_json:
        session_id = get_session_id(request)
        request.session_id = session_id


@app.route("/api/chat", methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')

    # todo: check if prompt is not empty

    # Retrieve conversation history from session manager
    conversation_history = get_session_thread()

    if conversation_history:
        messages = eval(conversation_history)
    else:
        messages = [{"role": "system", "content": assistant_instructions}]

    messages.append({"role": "user", "content": prompt})
    response_txt = ai_service.get_response(context=messages)

    # Add AI response to conversation
    messages.append({"role": "assistant", "content": response_txt})

    if has_no_answer_token in response_txt.lower():
        search_results = search_service.search(query=prompt)
        # Combine search results with OpenAI for a natural response
        prompt = assistant_prompt(search_results)
        messages.append({"role": "user", "content": prompt})
        response_txt = ai_service.get_response(context=messages)
        messages.append({"role": "assistant", "content": response_txt})

    # Store conversation in Redis
    set_session_thread(messages)

    # Log conversation to MongoDB
    chat_logs.insert_one({
        "session_id": get_current_session_id(),
        "timestamp": datetime.now(),
        "user_message": prompt,
        "ai_response": response_txt
    })

    return jsonify({
        "response": response_txt,
        "session_id": get_current_session_id()
    })
