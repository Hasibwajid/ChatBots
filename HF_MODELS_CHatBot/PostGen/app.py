from flask import Flask, request, jsonify, render_template
from langchain.prompts import PromptTemplate
from langchain.llms.base import LLM
from groq import Groq
from typing import Any, List, Optional
import random

# Example services offered by your company
company_services = [ # use your services
    "Machine Learning and Deep Learning services",
    "Custom chatbot development for businesses",
    "Innovative Computer Vision solutions",
    "SaaS product development",
    "Data Analysis and Insights services",
    "Web and App development services",
    "Cloud computing and scalability solutions",
    "AI-driven medical applications",
    "Business automation with AI"
]

# Flask app setup
app = Flask(__name__)

groq_client = Groq(api_key="Your_Groq_API_Key")

# Custom LLM class for Groq
class GroqLLM(LLM):
    client: Any
    model: str = "llama-3.1-70b-versatile"  # you can try other models too

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
        )
        return chat_completion.choices[0].message.content.strip() 

    @property
    def _llm_type(self) -> str:
        return "groq"

# LLaMA or Groq LLM initialization
llm = GroqLLM(client=groq_client)

# Define a prompt template for social media post generation
social_media_prompt_template = """
You are a social media content writer for [Your're copany name], a company specializing in {service}. Your task is to generate a creative, engaging, and professional post for {platform}. The post should inspire clients to learn more about [Company]'s services and emphasize the value of the solutions provided.

Make sure to highlight the unique benefits of {service}, and create a narrative that encourages engagement. Include a call-to-action encouraging businesses to seek real-time project help and provide our contact number [Your contact]. Mention our website for more information www.yourwebsite.com.

Do not use any special characters for formatting (like asterisks or quotes). Service: {service}
Platform: {platform}

Please generate a detailed and captivating post:
"""


PROMPT = PromptTemplate(
    template=social_media_prompt_template, 
    input_variables=["service", "platform"]
)

def generate_social_media_post(service, platform):
    """Generate a social media post for the given service and platform"""
    prompt = PROMPT.format(service=service, platform=platform)
    response = llm(prompt)
    
    return response  # Generated post content

@app.route('/')
def index():
    """Render the main page with the form"""
    return render_template('index.html', services=company_services)

@app.route('/generate_post', methods=['POST'])
def generate_post():
    """Endpoint to generate a social media post for a specific service"""
    data = request.get_json()
    platform = data.get('platform', 'Facebook').strip()  # Default to Facebook if no platform provided

    # Randomly pick a service or accept a specific one
    service = data.get('service', random.choice(company_services)).strip()

    # Generate post
    post_content = generate_social_media_post(service, platform)

    # Return the generated post as a response
    return jsonify({"post": post_content.strip()})  # Strip unnecessary whitespace from the final output

# Example of running Flask app
if __name__ == '__main__':
    app.run()
