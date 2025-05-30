    document.addEventListener('DOMContentLoaded',() => {
    const generateButton = document.getElementById('generate-button');
    const outputText = document.getElementById('output-text');
    
    const pdf = document.getElementById('download-button');
   
    const pdfSpinner= document.getElementById('pdf-spinner');
    const generateSpinner= document.getElementById('generate-spinner');

    if (pdf){
        pdf.disabled = true;}

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
    fetch('/api/generate_questions/generate_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            inputText: inputText, 
            })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('output-text').textContent = `Error: ${data.error}`;
        } else {

            outputText.innerHTML = marked.parse(data.answer);
            pdf.disabled = false;
        }
    })
   
    .catch(error => {
        document.getElementById('output-text').textContent = "An error occurred while communicating with the server.";
        console.error("Fetch error:", error);
    })
     .finally(() => {
        generateButton.disabled = false;
        if (generateSpinner) {
            generateSpinner.classList.add('d-none');
        }})
       if(pdf){
        pdf.addEventListener('click', () => {
            const pdfElement = document.getElementById('output-text'); 
            html2canvas(pdfElement, {scale : 2}).then(canvas =>{ 
            const {jsPDF} = window.jspdf;
            const doc = new jsPDF({
                orientation: 'portrait',
                unit: 'mm',
                format: 'a4'
                
            })
            const imgData = canvas.toDataURL('image.png');
                const imgwidth = 210;
                const pageHeight = 295;
                const imgHeight = (canvas.height *imgwidth)/canvas.width;
                let heightleft = imgHeight;
                let position = 0;
                doc.addImage(imgData, 'PNG', 0, position, imgwidth, imgHeight);        
                heightleft -= pageHeight;
                while(heightleft >0){
                    position = heightleft - imgHeight;
                    doc.addPage();
                    doc.addImage(imgData, 'PNG', 0, position, imgwidth, imgHeight);
                    heightleft -= pageHeight;
                }
                doc.save('Answer.pdf');
        });

            })}


    
    })});

document.getElementById('clear-button').addEventListener('click', () => {
    document.getElementById('input-text').value = '';
    document.getElementById('output-text').innerHTML = '';
  
});
