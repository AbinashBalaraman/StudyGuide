from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=api_key)

model =  genai.GenerativeModel('gemini-2.0-flash')

def generate_study_questions(input_text, num_questions, question_type):
    """Generate study questions based on the input text."""
    prompt = f"""Generate {num_questions} focusing on {question_type} facts and important informations on the following text as topic:\n\n{input_text}\n\n,The information should be designed to test understanding of the key concepts . Format each points give as a separate numbered item for example if given text is lodi dynasty sthe answer should include 'the time period important kings and important details'"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating questions: {str(e)}"    
@app.route('/api/generate_questions', methods=['POST'])
def generate_questions():
    """API endpoint to generate study questions."""
    try:
       data = request.get_json()
       input_text = data ['inputText']
       num_questions =int(data['numQuestions'])
       question_type = data['questionType']
       questions = generate_study_questions(input_text, num_questions, question_type)
       return jsonify({"questions": questions})    
    except Exception as e:
       print(f'error in generate_questions: {str(e)}')
       return jsonify({"error": "An error occurred while generating questions."}), 500

#if __name__ == '__main__':
   # app.run(debug=True)