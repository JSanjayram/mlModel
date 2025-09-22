function createFireworks() {
    const container = document.querySelector('.fireworks');
    
    function createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random position
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        
        // Random speed and duration
        const speed = Math.random() * 3 + 1;
        const duration = Math.random() * 2 + 1;
        
        // Random color
        const colors = ['#ff6b6b', '#ffd700', '#00ff88', '#ff69b4', '#00bfff', '#ff4757', '#7bed9f', '#70a1ff'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        // Random size
        const size = Math.random() * 6 + 2;
        
        particle.style.cssText = `
            position: absolute;
            left: ${x}%;
            top: ${y}%;
            width: ${size}px;
            height: ${size}px;
            background: ${color};
            border-radius: 50%;
            box-shadow: 0 0 ${size * 2}px ${color};
            animation: explode ${duration}s ease-out forwards;
            animation-delay: ${Math.random() * 2}s;
        `;
        
        container.appendChild(particle);
        
        // Remove particle after animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, (duration + 2) * 1000);
    }
    
    // Create particles continuously
    setInterval(createParticle, 200);
}

// CSS animation for particles
const style = document.createElement('style');
style.textContent = `
    @keyframes explode {
        0% {
            transform: scale(0) rotate(0deg);
            opacity: 1;
        }
        50% {
            transform: scale(1) rotate(180deg);
            opacity: 0.8;
        }
        100% {
            transform: scale(3) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);