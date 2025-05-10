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
    #"""Generate study questions based on the input text."""
    prompt = f"""Your task is to extract and present {num_questions} key facts and important pieces of information from the following text, which should be treated as the main topic.
The focus should be on the {question_type} aspects of the topic.
The extracted information should highlight core concepts, significant details, and essential knowledge that demonstrates a solid understanding of the topic.

Present each piece of information as a separate numbered point.
For example, if the input text is about the "Lodi Dynasty", your output should include points covering:
- The time period of the dynasty.
- Important kings or rulers.
- Significant events or contributions.
- Key characteristics or policies.

Input Text (Topic):
{input_text}
Key Facts and Information:"""
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