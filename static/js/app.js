function getAnalysis() {
    const ticker = document.getElementById('ticker').value;
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ticker: ticker}),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch(error => console.error('Error:', error));
}