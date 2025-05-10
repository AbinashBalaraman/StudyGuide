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

model =  genai.GenerativeModel('gemini-2.0-flash-lite')

def generate_study_questions(input_text):
    """Generate study questions based on the input text."""
    prompt = f"""You are an expert AI research assistant and educational content creator. Your primary function is to generate comprehensive, detailed, and well-structured study notes on any given topic, suitable for individuals preparing for competitive examinations or seeking a thorough understanding of the subject.The user has requested in-depth information on the topic: "{input_text}".Your task is to:
1.  **Deconstruct the Topic:** Identify the core concepts, sub-topics, and essential facets related to "{input_text}".
2.  **Retrieve Key Information:** From your knowledge base, gather all significant facts, definitions, principles, theories, processes, examples, applications, key figures/contributors, historical context (if applicable), current status/relevance (if applicable), and important classifications or typologies.
3.  **Structure for Clarity:** Organize the information logically using clear main headings and subheadings relevant to the topic. The structure should facilitate learning and retention.
4.  **Detail and Depth:** For each key piece of information, provide sufficient detail. Avoid superficial statements. Explain concepts, elaborate on significance, and provide context.
    *   If listing items (e.g., types, components, steps, examples, contributors), ensure the list is as comprehensive as possible and provide brief relevant details for each item.
    *   If discussing processes or theories, outline them clearly.
    *   If discussing historical events or figures (even outside of history-specific topics), include relevant dates, outcomes, and impacts.
5.  **Presentation:** Present the information using itemized lists (bullet points or numbered lists) extensively under each heading and subheading. Use clear, concise, and precise language.Essentially, imagine you are creating the core content for a detailed chapter in a high-quality textbook or an exhaustive study guide on "{input_text}". The output should be factual, well-organized, and cover the topic from multiple relevant angles to provide a holistic understanding.Consider these general categories as a starting point, adapting them as necessary based on the nature of "{input_text}":
*   **Introduction / Definition / Overview:** What is "{input_text}"? Its fundamental nature and scope.
*   **Key Concepts / Principles / Theories:** Core ideas and theoretical underpinnings.
*   **Components / Types / Classifications:** How is "{input_text}" broken down or categorized?
*   **Processes / Mechanisms / How it Works:** If applicable, the steps or workings involved.
*   **Historical Development / Evolution (if applicable):** How has "{input_text}" changed or developed over time? Key milestones.
*   **Important Figures / Contributors / Organizations:** Who are the key individuals or groups associated with "{input_text}"? Their contributions.
*   **Applications / Uses / Importance / Significance:** Why does "{input_text}" matter? Where is it used or seen? What is its impact?
*   **Advantages & Disadvantages / Strengths & Weaknesses / Pros & Cons (if applicable):** A balanced view.
*   **Current Trends / Future Outlook / Challenges (if applicable):**
*   **Related Concepts / Comparisons with Similar Topics (if useful for clarity):**"""
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
       #num_questions =int(data['numQuestions'])
       #question_type = data['questionType']
       questions = generate_study_questions(input_text)
       return jsonify({"questions": questions})    
    except Exception as e:
       print(f'error in generate_questions: {str(e)}')
       return jsonify({"error": "An error occurred while generating questions."}), 500
