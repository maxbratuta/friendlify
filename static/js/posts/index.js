document.addEventListener("DOMContentLoaded", function () {
    const inputElement = document.getElementById("post_message");
    const initialFont = window.getComputedStyle(inputElement).getPropertyValue("font");
    const maxWidth = 300;
    const minWidth = 125;

    inputElement.addEventListener("input", function () {
        const textWidth = getTextWidth(this.value, initialFont) + 20;
        this.style.width = `${Math.min(Math.max(textWidth, minWidth), maxWidth)}px`;
    });

    function getTextWidth(text, font) {
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        context.font = font;
        return context.measureText(text).width;
    }
});