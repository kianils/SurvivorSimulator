document.querySelectorAll('.flame').forEach(flame => {
    flame.style.animationDelay = `${Math.random() * 0.2}s`; // Add random delay for flames
});