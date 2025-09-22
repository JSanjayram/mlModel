let playerName = '';

// Start the quest
function startQuest() {
    console.log('Start quest clicked');
    showScreen('nameEntry');
}

// Begin journey with name
function beginJourney() {
    const nameInput = document.getElementById('heroName');
    playerName = nameInput.value.trim();
    
    if (!playerName) {
        alert('A hero needs a name!');
        return;
    }
    
    document.getElementById('playerName').textContent = playerName;
    
    // Show welcome message
    alert(`Welcome, ${playerName}. Your mission, should you choose to accept it: Find the one true birthday cake and survive the party madness.`);
    showScreen('pathChoice');
}

// Choose path
function choosePath(path) {
    const resultTitle = document.getElementById('resultTitle');
    const resultText = document.getElementById('resultText');
    
    switch(path) {
        case 'balloon':
            resultTitle.textContent = '🦕 Balloon Army Encounter!';
            resultText.textContent = 'You tried to sneak past, but they popped in protest. You are now covered in confetti. Stylish.';
            break;
        case 'dance':
            resultTitle.textContent = '💃 Dance Battle Royale!';
            resultText.textContent = 'You broke out the worm. Aunt Karen countered with the Macarena. It\'s a draw. She lets you pass.';
            break;
        case 'bribe':
            resultTitle.textContent = '🍬 Piñata Negotiations!';
            resultText.textContent = 'He accepts your candy bribe... then explodes with joy (and more candy). Success!';
            break;
    }
    
    showScreen('pathResult');
}

// Show boss level
function showBoss() {
    showScreen('bossLevel');
}

// Defeat boss
function defeatBoss(method) {
    let message = '';
    
    switch(method) {
        case 'juice':
            message = 'The toddler accepts your juice box tribute and waddles away happily. Victory!';
            break;
        case 'bubbles':
            message = 'The bubbles mesmerize the sugar-rushed guardian. They float away chasing bubbles. Genius!';
            break;
        case 'reason':
            message = 'You tried to reason with a sugar-rushed toddler. Surprisingly, they understood and shared the cake. Miracle!';
            break;
    }
    
    alert(message);
    showVictory();
}

// Show victory screen
function showVictory() {
    document.getElementById('finalName').textContent = playerName;
    showScreen('victory');
    createConfetti();
}

// Take selfie
function takeSelfie() {
    document.getElementById('selfieHero').textContent = playerName;
    showScreen('selfie');
}

// Restart quest
function restartQuest() {
    playerName = '';
    document.getElementById('heroName').value = '';
    showScreen('landing');
}

// Show screen function
function showScreen(screenId) {
    console.log('Switching to screen:', screenId);
    
    // Hide all screens
    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show target screen
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.add('active');
        console.log('Screen switched successfully');
    } else {
        console.error('Screen not found:', screenId);
    }
}

// Create confetti effect
function createConfetti() {
    const colors = ['#ff6b6b', '#ffd700', '#ff69b4', '#00ffff', '#98fb98'];
    
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.top = '-10px';
            confetti.style.width = '10px';
            confetti.style.height = '10px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.borderRadius = '50%';
            confetti.style.pointerEvents = 'none';
            confetti.style.zIndex = '1000';
            confetti.style.animation = 'fall 3s linear forwards';
            
            document.body.appendChild(confetti);
            
            setTimeout(() => {
                confetti.remove();
            }, 3000);
        }, i * 100);
    }
}

// Add CSS for confetti animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fall {
        0% {
            transform: translateY(-10px) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);