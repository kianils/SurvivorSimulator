document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.flame').forEach(flame => {
        const randomDelay = Math.random() * 0.5; // Range: 0 to 0.5 seconds
        flame.style.animationDelay = `${randomDelay}s`;
        flame.style.animationDuration = `${1 + Math.random() * 0.5}s`; // Range: 1 to 1.5 seconds
    });
});