// ==================== AOS INIT ====================
if (typeof AOS !== 'undefined') {
    AOS.init({
        duration: 800,
        once: true
    });
}

// ==================== TYPED.JS PLACEHOLDER ====================
if (typeof Typed !== 'undefined' && document.getElementById('urlInput')) {
    new Typed('#urlInput', {
        strings: [
            'https://example.com',
            'Paste suspicious URL here...',
            'http://phishing-site.com',
            'Enter URL to scan...'
        ],
        typeSpeed: 60,
        backSpeed: 30,
        backDelay: 2000,
        loop: true,
        attr: 'placeholder',
        showCursor: false
    });
}

// ==================== FORM SUBMIT ====================
document.getElementById("urlForm").addEventListener("submit", function(e) {
    let urlInput = document.getElementById("urlInput").value.trim();

    // Empty check
    if (urlInput === "") {
        e.preventDefault();
        alert("Please enter a URL first!");
        return;
    }

    // Basic URL format check
    if (!urlInput.startsWith("http://") && !urlInput.startsWith("https://")) {
        e.preventDefault();
        alert("Please enter a valid URL starting with http:// or https://");
        return;
    }

    // Show loading
    let btn = document.getElementById("checkBtn");
    let spinner = document.getElementById("spinner");

    spinner.classList.add("active");
    btn.innerHTML = '<span class="btn-text"><i class="fas fa-spinner fa-spin"></i> Scanning...</span>';
    btn.disabled = true;
});

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
        'a, button, input, .info-card, .nav-links li, .reasons-list li'
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