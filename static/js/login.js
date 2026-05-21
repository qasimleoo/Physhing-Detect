// ==================== AOS INIT ====================
if (typeof AOS !== 'undefined') {
    AOS.init({
        duration: 800,
        once: true
    });
}

// ==================== URL SAFETY CHECK ====================
let url = window.location.href;
let banner = document.getElementById("securityBanner");

if (banner) {
    if (url.startsWith("https")) {
        banner.innerHTML = '<i class="fas fa-shield-alt"></i> You are on a secure page';
        banner.classList.add("secure");
    } else {
        banner.innerHTML = '<i class="fas fa-exclamation-triangle"></i> This URL looks suspicious';
        banner.classList.add("warning");
    }
}

// ==================== IFRAME DETECTION ====================
if (window.self !== window.top) {
    alert("⚠ This page might be loaded inside a phishing iframe!");
}

// ==================== SSL INDICATOR ====================
let ssl = document.getElementById("sslStatus");

if (ssl) {
    if (url.startsWith("https")) {
        ssl.innerHTML = '<i class="fas fa-lock"></i> Secure HTTPS Connection';
        ssl.style.color = "#00b894";
        ssl.style.background = "rgba(0, 184, 148, 0.1)";
        ssl.style.border = "1px solid rgba(0, 184, 148, 0.3)";
    } else {
        ssl.innerHTML = '<i class="fas fa-unlock"></i> Not Secure Connection';
        ssl.style.color = "#ff6b6b";
        ssl.style.background = "rgba(255, 107, 107, 0.1)";
        ssl.style.border = "1px solid rgba(255, 107, 107, 0.3)";
    }
}

// ==================== TOGGLE PASSWORD ====================
function togglePassword() {
    const passwordField = document.getElementById("passwordField");
    const toggleIcon = document.querySelector(".toggle-password");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
    }
}

// ==================== PARTICLES.JS ====================
if (typeof particlesJS !== 'undefined' && document.getElementById('particles-js')) {
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 800 }},
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
        'a, button, input, .info-feature, .trust-badge, .nav-links li, .toggle-password'
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