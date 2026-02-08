let step = 0;
let loanData = {};

const questions = [
    "👋 Hi! What is your monthly income (₹)?",
    "💰 What loan amount do you want (₹)?",
    "📅 What is the loan tenure (in months)?",
    "📊 What is your CIBIL score?"
];

window.onload = () => {
    addBotMessage(questions[step]);
};

/* Chat helpers */
function addBotMessage(msg) {
    const chat = document.getElementById("chat-box");
    chat.innerHTML += `<div class="bot">${msg}</div>`;
    chat.scrollTop = chat.scrollHeight;
}

function addUserMessage(msg) {
    const chat = document.getElementById("chat-box");
    chat.innerHTML += `<div class="user">${msg}</div>`;
    chat.scrollTop = chat.scrollHeight;
}

/* Typing animation */
function showTyping() {
    addBotMessage("⏳ Virtual Bank Assistant is thinking...");
}

async function handleInput() {

    const input = document.getElementById("userInput");
    const value = input.value.trim();
    if (!value) return;

    addUserMessage(value);
    input.value = "";

    if (step === 0) loanData.income = parseInt(value);
    if (step === 1) loanData.loan = parseInt(value);
    if (step === 2) loanData.tenure = parseInt(value);
    if (step === 3) loanData.cibil = parseInt(value);

    step++;

    if (step < questions.length) {
        addBotMessage(questions[step]);
    } else {
        showTyping();

        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(loanData)
        });

        const data = await response.json();

        addBotMessage(`
            <b>📄 Loan Result:</b><br>
            EMI: ₹${data.emi}<br>
            FOIR: ${data.foir}%<br>
            Risk: ${data.risk}/100<br>
            Status: <b>${data.status}</b>
        `);

        addBotMessage(data.reply);

        updateRobot(data.status);

        step = 0;
        loanData = {};
    }
}

/* Robot emotions */
function updateRobot(status) {

    const mouth = document.getElementById("mouth");
    const head = document.getElementById("head");
    const robot = document.getElementById("robot");

    if (status === "Approved") {

        mouth.setAttribute("d", "M70 115 Q100 145 130 115");
        head.setAttribute("fill", "#4CAF50");

        confetti({
            particleCount: 150,
            spread: 70,
            origin: { y: 0.6 }
        });

        

    } else {

        mouth.setAttribute("d", "M70 130 Q100 105 130 130");
        head.setAttribute("fill", "#f44336");

        robot.classList.add("shake");
        setTimeout(() => robot.classList.remove("shake"), 500);

        
    }
}

/* Eye tracking */
document.addEventListener("mousemove", function(e) {

    const left = document.getElementById("leftPupil");
    const right = document.getElementById("rightPupil");

    const x = (e.clientX / window.innerWidth - 0.5) * 10;
    const y = (e.clientY / window.innerHeight - 0.5) * 10;

    left.setAttribute("cx", 75 + x);
    left.setAttribute("cy", 80 + y);

    right.setAttribute("cx", 125 + x);
    right.setAttribute("cy", 80 + y);
});
