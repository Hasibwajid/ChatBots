import os
from quart import Quart, request, jsonify
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize Quart app
app = Quart(__name__)

# Initialize AsyncOpenAI client
client = AsyncOpenAI(api_key=openai_api_key)

# Maintain conversation history in-memory
conversation_history = {}

# Empathetic prompt template
empathetic_prompt_template = """
You are an empathetic and supportive chatbot. Your role is to provide emotional and mental support and understanding to users like empathetic therapist or counselor. Respond to the user's message with compassion, empathy, and encouragement, ensuring they feel heard and cared for. Avoid giving medical advice, but offer comforting and reassuring words or ask if they need some practical steps to solve there issue.

{history}
User: {message}
Chatbot:
"""

@app.route('/chat', methods=['POST'])
async def chat():
    global conversation_history
    
    data = await request.json
    message = data.get('message', '')
    chat_id = data.get('chat_id', None)  # Optional: Get chat_id if using multiple chats
    
    try:
        # Initialize conversation history for new chat if not exists
        if chat_id not in conversation_history:
            conversation_history[chat_id] = []
        
        # Append user's message to conversation history
        conversation_history[chat_id].append(f"User: {message}")
        
        # Construct prompt with conversation history
        history = "\n".join(conversation_history[chat_id])
        prompt = empathetic_prompt_template.format(history=history, message=message)
        
        # Send user message and conversation history to OpenAI for completion
        chat_completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an empathetic and mental health supportive chatbot."},
                {"role": "user", "content": prompt}
            ],
        )
        
        # Get bot's reply
        bot_reply = chat_completion.choices[0].message.content.strip()
        
        # Append bot's reply to conversation history
        conversation_history[chat_id].append(f"Bot: {bot_reply}")
        
        return jsonify({'reply': bot_reply})
    
    except Exception as e:
        return jsonify({'error': str(e)})

def run_quart():
    app.run(port=5000)

if __name__ == "__main__":
    run_quart()
