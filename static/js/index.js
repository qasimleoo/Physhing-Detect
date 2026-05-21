// ==================== EXISTING CODE (KEEP) ====================

let url = window.location.href;

/* 1. Browser URL Warning */
let banner = document.getElementById("warningBanner");

if (banner) {
    if (url.startsWith("https")) {
        banner.innerHTML = "🟢 You are on a secure page";
        banner.style.background = "green";
    } else {
        banner.innerHTML = "🔴 This URL looks suspicious";
        banner.style.background = "red";
    }
}

/* 2. Iframe Detection */
if (window.self !== window.top) {
    alert("⚠ This might be a phishing frame (iframe detected)");
}

/* 3. SSL Indicator */
let sslBox = document.getElementById("sslBox");

if (sslBox) {
    if (url.startsWith("https")) {
        sslBox.innerHTML = "🔒 Secure Connection (HTTPS)";
        sslBox.style.color = "green";
    } else {
        sslBox.innerHTML = "⚠ Not Secure (HTTP)";
        sslBox.style.color = "red";
    }
}

// ==================== AOS INIT ====================
if (typeof AOS !== 'undefined') {
    AOS.init({
        duration: 900,
        once: true,
        offset: 80
    });
}

// ==================== TYPED.JS ====================
if (typeof Typed !== 'undefined' && document.getElementById('typedHero')) {
    new Typed('#typedHero', {
        strings: [
            'Phishing Attacks',
            'Fake Emails',
            'Malicious URLs',
            'Online Fraud'
        ],
        typeSpeed: 60,
        backSpeed: 40,
        backDelay: 1500,
        loop: true,
        cursorChar: '|'
    });
}

// ==================== COUNTUP.JS ====================
// Yeh function check karta hai ki element screen pe dikhai de raha hai ya nahi
function isElementInView(el) {
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom > 0;
}

let countStarted = false;

function startCounting() {
    if (countStarted) return;

    const statScans = document.getElementById('statScans');
    if (!statScans || !isElementInView(statScans)) return;

    countStarted = true;

    if (typeof countUp !== 'undefined') {
        const scans = new countUp.CountUp('statScans', 500, {
            duration: 2.5,
            suffix: '+'
        });
        const accuracy = new countUp.CountUp('statAccuracy', 98, {
            duration: 2,
            suffix: '%'
        });
        const users = new countUp.CountUp('statUsers', 1200, {
            duration: 3,
            suffix: '+'
        });

        scans.start();
        accuracy.start();
        users.start();
    }
}

// Jab scroll ho tab count start ho
window.addEventListener('scroll', startCounting);
window.addEventListener('load', startCounting);

// ==================== PARTICLES.JS ====================
if (typeof particlesJS !== 'undefined' && document.getElementById('particles-js')) {
    particlesJS('particles-js', {
        particles: {
            number: {
                value: 80,
                density: { enable: true, value_area: 800 }
            },
            color: { value: '#00d4ff' },
            shape: { type: 'circle' },
            opacity: {
                value: 0.7,
                random: true
            },
            size: {
                value: 3,
                random: true
            },
            line_linked: {
                enable: true,
                distance: 150,
                color: '#00d4ff',
                opacity: 0.5,
                width: 1
            },
            move: {
                enable: true,
                speed: 2,
                direction: 'none',
                random: true,
                out_mode: 'out'
            }
        },
        interactivity: {
            detect_on: 'window',
            events: {
                onhover: {
                    enable: true,
                    mode: 'grab'
                }
            },
            modes: {
                grab: {
                    distance: 200,
                    line_linked: { opacity: 0.8 }
                }
            }
        },
        retina_detect: true
    });
}

// ==================== NAVBAR ACTIVE LINK ====================
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
    }
});

// ==================== CUSTOM CURSOR (SMOOTH) ====================
const cursorDot = document.querySelector('.cursor-dot');
const cursorRing = document.querySelector('.cursor-ring');

if (cursorDot && cursorRing) {
    let mouseX = 0, mouseY = 0;
    let dotX = 0, dotY = 0;
    let ringX = 0, ringY = 0;

    // Track mouse position
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Smooth animation loop
    function animateCursor() {
        // Dot follows fast
        dotX += (mouseX - dotX) * 0.9;
        dotY += (mouseY - dotY) * 0.9;
        
        // Ring follows slower (smooth lag)
        ringX += (mouseX - ringX) * 0.15;
        ringY += (mouseY - ringY) * 0.15;

        cursorDot.style.transform = `translate(${dotX}px, ${dotY}px) translate(-50%, -50%)`;
        cursorRing.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`;

        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // Hover effect on interactive elements
    const hoverElements = document.querySelectorAll(
        'a, button, .card, .feature-item, .stat-box, .btn, input, textarea, .nav-links li'
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

    // Click effect
    document.addEventListener('mousedown', () => {
        cursorRing.classList.add('click');
    });

    document.addEventListener('mouseup', () => {
        cursorRing.classList.remove('click');
    });

    // Hide on leave
    document.addEventListener('mouseleave', () => {
        cursorDot.style.opacity = '0';
        cursorRing.style.opacity = '0';
    });

    document.addEventListener('mouseenter', () => {
        cursorDot.style.opacity = '1';
        cursorRing.style.opacity = '0.6';
    });
}