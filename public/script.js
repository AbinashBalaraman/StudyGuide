document.getElementById('generate-button').addEventListener('click', () => {
    const inputText = document.getElementById('input-text').value;
    const numQuestions = document.getElementById('num-questions').value;
    const questionType = document.getElementById('question-type').value;

    if (!inputText.trim()) {
        document.getElementById('output-text').textContent = 'Please enter some text.';
        return;
    }
    fetch('/api/generate_questions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            inputText: inputText, // Corrected key
            numQuestions: numQuestions, // Corrected key
            questionType: questionType
            })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('output-text').textContent = `Error: ${data.error}`;
        } else {
            document.getElementById('output-text').textContent = data.questions;
        }
    })
    .catch(error => {
        document.getElementById('output-text').textContent = "An error occurred while communicating with the server.";
        console.error("Fetch error:", error);
    });
});

document.getElementById('clear-button').addEventListener('click', () => {
    document.getElementById('input-text').value = '';
    document.getElementById('output-text').textContent = '';
});
