document.addEventListener("DOMContentLoaded", function () {
    const textElement = document.getElementById("footer-text");
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