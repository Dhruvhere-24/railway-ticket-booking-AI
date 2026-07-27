document.addEventListener("DOMContentLoaded", () => {
    const line = document.querySelector('.line');
    
    // Add class for animation after short delay
    if (line) {
        setTimeout(() => {
            line.classList.add('animate');
        }, 200);
    }
});
