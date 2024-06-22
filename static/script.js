document.getElementById('recordButton').addEventListener('click', function() {
    console.log("btn clicked")
    fetch('/record', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('transcriptionBox').value = data.transcription;
    })
    .catch(error => console.error('Error:', error));

    // Show recording started message
    document.getElementById('statusMessage').textContent = 'Recording started...';

    // Simulate recording end after 10 seconds (adjust this based on your actual recording duration)
    setTimeout(function() {
        document.getElementById('statusMessage').textContent = 'Recording ended.';
    }, 10000); // 10 seconds in milliseconds
});
