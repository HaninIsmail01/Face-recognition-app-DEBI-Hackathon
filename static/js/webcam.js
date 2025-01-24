// Access the webcam and display the video feed
const camera = document.getElementById('camera');
const captureBtn = document.getElementById('captureBtn');
const canvas = document.getElementById('canvas');
const resultDiv = document.getElementById('result');

// Get the video stream from the webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        camera.srcObject = stream;
    })
    .catch(err => {
        console.log("Error accessing webcam: ", err);
    });

// Capture the image from the video feed
captureBtn.addEventListener('click', () => {
    const ctx = canvas.getContext('2d');
    canvas.width = camera.videoWidth;
    canvas.height = camera.videoHeight;
    ctx.drawImage(camera, 0, 0, canvas.width, canvas.height);

    // Convert the canvas image to a data URL (base64)
    const imageData = canvas.toDataURL('image/jpeg');

    // Send the image to the server for face recognition
    fetch('/recognize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            resultDiv.innerHTML = `<h2>Recognized: ${data.message}</h2><img src="${data.image}" alt="Result Image" />`;
        } else {
            resultDiv.innerHTML = `<h2>${data.message}</h2>`;
        }
    })
    .catch(err => {
        console.log("Error sending image to server: ", err);
    });
});
