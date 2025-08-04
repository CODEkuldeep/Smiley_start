const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const snap = document.getElementById("snap");
const context = canvas.getContext("2d");
const result = document.getElementById("result");
const motivation = document.getElementById("motivation");

const messages = [
  "You are stronger than your doubts 💪",
  "A smile is your superpower ✨",
  "Let’s win the day — with joy 😊",
  "Progress over perfection!",
  "Your energy is your edge 🚀",
];

// Set random motivational message on page load
motivation.innerText = messages[Math.floor(Math.random() * messages.length)];

// Get webcam stream
navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
  video.srcObject = stream;
});

// On button click, capture image and send to backend
snap.addEventListener("click", () => {
  context.drawImage(video, 0, 0, 640, 480);
  const dataURL = canvas.toDataURL("image/png");

  fetch("/capture", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: dataURL }),
  })
    .then((res) => res.json())
    .then((data) => {
      result.innerText = data.message;
      result.style.color = data.status === "success" ? "green" : "red";

      if (data.status === "success") {
        // Show captured image
        const imgDisplay = document.createElement("img");
        imgDisplay.src = data.image_url;
        imgDisplay.alt = "Your Smiley Pic!";
        imgDisplay.width = 320;
        document.body.appendChild(imgDisplay);

        // Ask to share
        const shareBtn = document.createElement("button");
        shareBtn.innerText = "Share This Smile 😊";
        shareBtn.onclick = () => {
          alert(
            "This feature will be available in the next version (SmileyStart2). For now, you can manually download and share."
          );
        };
        document.body.appendChild(shareBtn);
      }
    })
    .catch((error) => {
      result.innerText = "Something went wrong.";
      result.style.color = "red";
      console.error(error);
    });
});
