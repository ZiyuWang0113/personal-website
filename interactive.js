document.addEventListener("DOMContentLoaded", function () {
    console.log("Interactive elements loaded");

    document.body.style.backgroundColor = "#282e38";
    document.body.style.fontFamily = "Comic Sans MS, cursive, sans-serif";
    document.body.style.color = "#fff";
    document.body.style.overflowX = "hidden";
    document.body.style.lineHeight = "3.0";
    document.body.style.textAlign = "center";
    document.body.style.padding = "2rem";
    document.body.style.backgroundSize = "cover";
    document.body.style.backgroundPosition = "center";
    document.body.style.backgroundAttachment = "fixed";
    
    // Create Main Container for Interactive Section
    let container = document.createElement("div");
    container.className = "container";
    container.style.maxWidth = "1000px";
    container.style.margin = "auto";
    container.style.padding = "20px";
    container.style.background = "rgba(255, 255, 255, 0.1)";
    container.style.borderRadius = "10px";
    container.style.backdropFilter = "blur(5px)";
    container.style.fontSize = "1rem";
    container.style.boxShadow = "0 4px 10px rgba(255, 255, 255, 0.3)";
    container.innerHTML = `
        <h1>Something Interesting</h1>
        <p>🎉 Welcome to the fun zone!</p>
        <p>Stay tuned for exciting content!</p>
        <a href="index.html" class="back-btn" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #fff; color: #000; text-decoration: none; border-radius: 5px; transition: 0.3s;">Back to Home</a>
    `;
    document.body.appendChild(container);

    // Placeholder for Moving Desktop Pet
    function createDesktopPet() {
        let pet = document.createElement("div");
        pet.id = "desktop-pet";
        pet.style.width = "80px";
        pet.style.height = "80px";
        pet.style.position = "fixed";
        pet.style.bottom = "20px";
        pet.style.left = "20px";
        pet.style.backgroundImage = "url('pet.png')";
        pet.style.backgroundSize = "cover";
        document.body.appendChild(pet);
        console.log("Desktop pet initialized");
    }

    // Placeholder for Video Box
    function createVideoBox() {
        let videoContainer = document.createElement("div");
        videoContainer.id = "video-box";
        videoContainer.innerHTML = `
            <video width="500" controls>
                <source src="videos/bobo_cat.mp4" type="video/mp4">
            </video>
        `;
        document.body.appendChild(videoContainer);
        console.log("Video box added");
    }

    // Placeholder for Virtual Wooden Fish
    function createWoodenFish() {
        let fish = document.createElement("button");
        fish.id = "wooden-fish";
        fish.innerText = "🔔 Click to Strike!";
        fish.style.padding = "10px 20px";
        fish.style.fontSize = "1.5rem";
        fish.addEventListener("click", function () {
            console.log("Wooden fish struck!");
            // Future sound effect implementation
        });
        document.body.appendChild(fish);
        console.log("Wooden fish initialized");
    }

    // Initialize Features (Will be refined later)
    createDesktopPet();
    createVideoBox();
    createWoodenFish();
});
