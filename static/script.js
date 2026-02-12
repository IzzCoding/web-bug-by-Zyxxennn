// Socket.IO connection
const socket = io();

socket.on('connect', function() {
    console.log('Wheel berputar - Mahoraga terhubung');
});

socket.on('response', function(data) {
    console.log('Mahoraga:', data.data);
});

// Global state
let currentLevel = 1;
let currentWheel = 0;

// Export functions for global access
window.selectAttack = function(attack) {
    window.selectedAttack = attack;
    const btn = document.getElementById('launchBtn');
    if (btn) btn.innerHTML = `<i class="fas fa-bolt"></i> ${attack}`;
};

window.launchAttack = function() {
    const target = document.getElementById('targetInput')?.value;
    if (!target) {
        alert('Isi target, Master.');
        return;
    }
    
    // Implementasi di main HTML
};

window.sendAIPrompt = function() {
    // Implementasi di main HTML
};

window.quickAIAction = function(query) {
    const input = document.getElementById('aiPrompt');
    if (input) {
        input.value = query;
        window.sendAIPrompt();
    }
};

// Initialize attack grid on load
document.addEventListener('DOMContentLoaded', function() {
    // Set default attack
    window.selectedAttack = 'DDOS';
});
