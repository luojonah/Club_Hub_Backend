from flask import Blueprint, request, jsonify
from model.gemini import Gemini
from google.generativeai import configure, GenerativeModel
import os
from api.gemini import gemini_api



# Creating blueprint for the gemini API
gemini_api = Blueprint('gemini_api', __name__, url_prefix='/api/gemini')

# Configure the Generative AI API
api_key = os.getenv('GENAI_API_KEY', 'AIzaSyBAuvDOOru9Eckuc8ag-vYi-M_m1MmwUOQ')  # Replace YOUR_API_KEY with the actual key or use env var
configure(api_key=api_key)
model = GenerativeModel('gemini-pro')

@gemini_api.route('/help', methods=['POST'])
def ai_help():
    """
    Endpoint to get AI-generated suggestions and answers.
    """
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided."}), 400

    try:
        response = model.generate_content(
            f"Your name is Gemini Integration. Your job is to provide club leaders and members with suggestions "
            f"and answer their requests to maximize their club planning efficiency and enhance their experience "
            f"with ClubHub. Here is your prompt: {question}"
        )

        # Save the question and response to the database
        gemini_response = Gemini(question=question, response=response.text)
        gemini_response.create()

        return jsonify({"response": response.text}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
