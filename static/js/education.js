// ==================== FORCE CURSOR NONE ====================
document.addEventListener('mouseover', function(e) {
    e.target.style.cursor = 'none';
});

// ==================== AOS INIT ====================
if (typeof AOS !== 'undefined') {
    AOS.init({
        duration: 800,
        once: true,
        offset: 80
    });
}

// ==================== QUIZ ====================
const questions = [
    {
        text: "Your bank asks you to click a link and login urgently.",
        correct: "phishing",
        explanation: "⚠️ Banks never ask for login details via email!"
    },
    {
        text: "Email from your university's official domain.",
        correct: "legit",
        explanation: "✅ Trusted domain from known institution is usually safe."
    },
    {
        text: "You won a lottery you never entered!",
        correct: "phishing",
        explanation: "⚠️ This is a classic scam trick — never fall for it!"
    },
    {
        text: "Secure HTTPS website of a well-known company.",
        correct: "legit",
        explanation: "✅ HTTPS with a known domain indicates safety."
    },
    {
        text: "Message asking you to share your OTP immediately.",
        correct: "phishing",
        explanation: "⚠️ Never share OTP with anyone — ever!"
    }
];

let index = 0;
let score = 0;

function updateProgress() {
    const percent = ((index) / questions.length) * 100;
    document.getElementById("progressFill").style.width = percent + "%";
    document.getElementById("progressText").innerText = 
        (index + 1) + "/" + questions.length;
    document.getElementById("scoreDisplay").innerText = score;
}

function loadQuestion() {
    if (index < questions.length) {
        document.getElementById("question").innerText = questions[index].text;
        document.getElementById("feedback").innerText = "";
        document.getElementById("feedback").className = "";
        document.getElementById("feedbackBox").style.display = "flex";
        updateProgress();
    }
}

function answer(user) {
    const feedbackEl = document.getElementById("feedback");
    const isCorrect = user === questions[index].correct;

    if (isCorrect) {
        score++;
        feedbackEl.innerText = "✅ Correct! " + questions[index].explanation;
        feedbackEl.className = "correct";
    } else {
        feedbackEl.innerText = "❌ Wrong! " + questions[index].explanation;
        feedbackEl.className = "wrong";
    }

    document.getElementById("scoreDisplay").innerText = score;
    index++;

    if (index < questions.length) {
        setTimeout(loadQuestion, 2000);
    } else {
        setTimeout(() => {
            // Final score
            let message = "";
            let emoji = "";

            if (score === 5) {
                message = "Perfect Score! You are a phishing expert!";
                emoji = "🏆";
            } else if (score >= 3) {
                message = "Good job! Keep learning to stay safe.";
                emoji = "👍";
            } else {
                message = "Keep practicing! Phishing awareness is important.";
                emoji = "📚";
            }

            document.getElementById("question").innerText = 
                emoji + " Quiz Complete! Score: " + score + "/" + questions.length + " — " + message;
            document.getElementById("feedback").innerText = "";
            document.getElementById("progressFill").style.width = "100%";
            document.getElementById("progressText").innerText = "Done!";

            // Hide buttons
            document.querySelector(".quiz-buttons").style.display = "none";

            // Show restart button
            const restartBtn = document.createElement("button");
            restartBtn.className = "quiz-btn legit-btn";
            restartBtn.innerHTML = '<i class="fas fa-redo"></i> Restart Quiz';
            restartBtn.style.width = "100%";
            restartBtn.style.marginTop = "15px";
            restartBtn.onclick = restartQuiz;
            document.querySelector(".feedback-box").appendChild(restartBtn);

        }, 2000);
    }
}

function restartQuiz() {
    index = 0;
    score = 0;
    document.querySelector(".quiz-buttons").style.display = "flex";

    // Remove restart button
    const restartBtn = document.querySelector(".feedback-box .legit-btn");
    if (restartBtn) restartBtn.remove();

    loadQuestion();
}

// Start quiz
loadQuestion();

// ==================== PARTICLES.JS ====================
if (typeof particlesJS !== 'undefined' && document.getElementById('particles-js')) {
    particlesJS('particles-js', {
        particles: {
            number: { value: 60, density: { enable: true, value_area: 800 }},
            color: { value: '#00d4ff' },
            shape: { type: 'circle' },
            opacity: { value: 0.5, random: true },
            size: { value: 3, random: true },
            line_linked: {
                enable: true,
                distance: 150,
                color: '#00d4ff',
                opacity: 0.3,
                width: 1
            },
            move: {
                enable: true,
                speed: 1.5,
                direction: 'none',
                random: true,
                out_mode: 'out'
            }
        },
        interactivity: {
            detect_on: 'window',
            events: {
                onhover: { enable: true, mode: 'grab' }
            },
            modes: {
                grab: { distance: 150, line_linked: { opacity: 0.6 }}
            }
        },
        retina_detect: true
    });
}

// ==================== CUSTOM CURSOR ====================
const cursorDot = document.querySelector('.cursor-dot');
const cursorRing = document.querySelector('.cursor-ring');

if (cursorDot && cursorRing) {
    let mouseX = 0, mouseY = 0;
    let dotX = 0, dotY = 0;
    let ringX = 0, ringY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animateCursor() {
        dotX += (mouseX - dotX) * 0.9;
        dotY += (mouseY - dotY) * 0.9;
        ringX += (mouseX - ringX) * 0.15;
        ringY += (mouseY - ringY) * 0.15;

        cursorDot.style.transform = `translate(${dotX}px, ${dotY}px) translate(-50%, -50%)`;
        cursorRing.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`;

        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    const hoverElements = document.querySelectorAll(
        'a, button, .card, .tip-card, .stat, .checklist li, .nav-links li'
    );

    hoverElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursorRing.classList.add('hover');
            cursorDot.classList.add('hover');
        });
        el.addEventListener('mouseleave', () => {
            cursorRing.classList.remove('hover');
            cursorDot.classList.remove('hover');
        });
    });

    document.addEventListener('mousedown', () => cursorRing.classList.add('click'));
    document.addEventListener('mouseup', () => cursorRing.classList.remove('click'));
}

// ==================== NAVBAR ACTIVE LINK ====================
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
    }
});