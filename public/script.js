    document.addEventListener('DOMContentLoaded',() => {
    const generateButton = document.getElementById('generate-button');
    const outputText = document.getElementById('output-text');
    
    //const pdf = document.getElementById('download-button');
    //const {jspdf} = window.jspdf;
    //const pdfSpinner= document.getElementById('pdf-spinner');
    const generateSpinner= document.getElementById('generate-spinner');
    
    generateButton.addEventListener('click', () => {
    const inputText = document.getElementById('input-text').value;
        
    if (!inputText.trim()) {
        document.getElementById('output-text').textContent = 'Please enter some text.';
        return;
    }
    generateButton.disabled = true;
            if (generateSpinner) {
                generateSpinner.classList.remove('d-none');

            }
    fetch('api/generate_questions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            inputText: inputText, // Corrected key
           // #numQuestions: numQuestions, // Corrected key
            //questionType: questionType
            })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('output-text').textContent = `Error: ${data.error}`;
        } else {

            outputText.innerHTML = marked.parse(data.questions);
            //const output =outputText; 
        }
    })
   
    .catch(error => {
        document.getElementById('output-text').textContent = "An error occurred while communicating with the server.";
        console.error("Fetch error:", error);
    })
    .finally(() => {
        generateButton.disabled = false;
        if (generateSpinner) {
            generateSpinner.classList.add('d-none');}

      
})})});

document.getElementById('clear-button').addEventListener('click', () => {
    document.getElementById('input-text').value = '';
    document.getElementById('output-text').innerHTML = '';
  
});
