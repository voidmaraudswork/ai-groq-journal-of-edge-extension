document.getElementById('generateBtn').addEventListener('click', async () => {
  const outputDiv = document.getElementById('output');
  outputDiv.innerText = "Analyzing your day... Please wait...";
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/generate-summary');
    const data = await response.json();
    outputDiv.innerText = data.summary;
  } catch (err) {
    outputDiv.innerText = "Error: Make sure your Python server is running!";
  }
});