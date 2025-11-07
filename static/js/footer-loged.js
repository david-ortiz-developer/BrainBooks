document.addEventListener("DOMContentLoaded", function () {
    const textElement = document.getElementById("footer-text");

    // Texto que se escribirá en el footer
    const text = `⚡ App soportada por David Ortiz — Científico de la información, ingeniero y guitarrista. 
🔗 LinkedIn: https://www.linkedin.com/in/davit-ortiz-ios-developper/`;

    let index = 0;
    const speed = 40; // ms entre letras

    function typeWriter() {
        if (index < text.length) {
            textElement.textContent += text.charAt(index);
            index++;
            setTimeout(typeWriter, speed);
        }
    }

    typeWriter();
});