document.addEventListener("DOMContentLoaded", function() {
    document.body.style.margin = "0";
    document.body.style.padding = "0";
    document.body.style.boxSizing = "border-box";
    document.body.style.fontFamily = "Comic Sans MS, cursive, sans-serif";
    document.body.style.color = "#333";
    document.body.style.backgroundColor = "#000";
    document.body.style.overflowX = "hidden";
    document.body.style.lineHeight = "1.6";

    // Create iframe for canvas background
    let iframe = document.createElement("iframe");
    iframe.src = "canvas_star.html";
    iframe.style.position = "absolute";
    iframe.style.top = "0";
    iframe.style.left = "0";
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.zIndex = "-1";
    iframe.style.border = "none";
    document.body.appendChild(iframe);

    // Create main container
    let main = document.createElement("main");
    main.style.maxWidth = "1200px";
    main.style.margin = "2rem auto";
    main.style.display = "grid";
    main.style.gridTemplateColumns = "repeat(2, 1fr)";
    main.style.gap = "2rem";
    main.style.justifyItems = "center";
    main.style.alignItems = "center";
    main.style.position = "relative";
    main.style.zIndex = "1";
    
    // Bubble content
    let bubbleTexts = ["About Me", "Computer Science", "Something Interesting", "My Links"];
    let bubbleLinks = ["about.html", "#", "interesting.html", "link.html"];

    bubbleTexts.forEach((text, index) => {
        let bubble = document.createElement("div");
        bubble.className = "bubble";
        bubble.textContent = text;
        bubble.style.width = "200px";
        bubble.style.height = "200px";
        bubble.style.borderRadius = "50%";
        bubble.style.background = "linear-gradient(145deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1))";
        bubble.style.boxShadow = "0 4px 10px rgba(0, 0, 0, 0.4)";
        bubble.style.backdropFilter = "blur(8px)";
        bubble.style.border = "2px solid rgba(255, 255, 255, 0.3)";
        bubble.style.display = "flex";
        bubble.style.justifyContent = "center";
        bubble.style.alignItems = "center";
        bubble.style.color = "white";
        bubble.style.fontSize = "1.5rem";
        bubble.style.textAlign = "center";
        bubble.style.position = "relative";
        bubble.style.transition = "all 0.3s ease-in-out";
        
        bubble.addEventListener("mouseover", function() {
            bubble.style.transform = "scale(1.2)";
            bubble.style.boxShadow = "0 10px 25px rgba(255, 255, 255, 0.7)";
            bubble.style.background = "linear-gradient(145deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.2))";
        });

        bubble.addEventListener("mouseleave", function() {
            bubble.style.transform = "scale(1)";
            bubble.style.boxShadow = "0 4px 10px rgba(0, 0, 0, 0.4)";
            bubble.style.background = "linear-gradient(145deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1))";
        });

        // Add click event to navigate to specific pages
        bubble.addEventListener("click", function() {
            if (bubbleLinks[index] !== "#") {
                window.location.href = bubbleLinks[index];
            }
        });
        
        main.appendChild(bubble);
    });
    
    document.body.appendChild(main);

    // Footer
    let footer = document.createElement("footer");
    footer.style.position = "absolute";
    footer.style.bottom = "0";
    footer.style.width = "100%";
    footer.style.textAlign = "center";
    footer.style.background = "rgba(0, 0, 0, 0.7)";
    footer.style.color = "white";
    footer.style.padding = "10px 0";
    footer.style.zIndex = "1";
    
    let footerText = document.createElement("p");
    footerText.innerHTML = "&copy; 2025. All Rights Reserved.";
    footer.appendChild(footerText);
    document.body.appendChild(footer);
});
