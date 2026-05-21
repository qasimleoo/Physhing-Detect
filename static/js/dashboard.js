// ==================== AOS INIT ====================
if (typeof AOS !== 'undefined') {
    AOS.init({
        duration: 800,
        once: true
    });
}

// ==================== COUNTUP ANIMATION ====================
window.addEventListener('load', () => {
    const counters = document.querySelectorAll('[data-count]');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-count')) || 0;
        if (typeof countUp !== 'undefined' && target > 0) {
            const count = new countUp.CountUp(counter, target, {
                duration: 2.5,
                separator: ','
            });
            count.start();
        } else {
            counter.innerText = target;
        }
    });
});

// ==================== AUTO REFRESH (30 sec) ====================
setInterval(function() {
    location.reload();
}, 30000);

// ==================== HIGHLIGHT TABLE RESULTS ====================
window.onload = function() {
    let rows = document.querySelectorAll('tbody tr');
    
    rows.forEach(function(row) {
        let cells = row.querySelectorAll('td');
        cells.forEach(function(cell) {
            let text = cell.innerText.toLowerCase().trim();
            
            if (text === 'phishing' || text.includes('phishing')) {
                cell.innerHTML = '<span style="color: #ff6b6b; font-weight: 700; padding: 4px 12px; background: rgba(255,107,107,0.15); border-radius: 20px; font-size: 12px;"><i class="fas fa-exclamation-triangle"></i> ' + cell.innerText + '</span>';
            }
            else if (text === 'safe' || text.includes('safe')) {
                cell.innerHTML = '<span style="color: #00b894; font-weight: 700; padding: 4px 12px; background: rgba(0,184,148,0.15); border-radius: 20px; font-size: 12px;"><i class="fas fa-check-circle"></i> ' + cell.innerText + '</span>';
            }
            else if (text === 'suspicious' || text.includes('suspicious')) {
                cell.innerHTML = '<span style="color: #fdcb6e; font-weight: 700; padding: 4px 12px; background: rgba(253,203,110,0.15); border-radius: 20px; font-size: 12px;"><i class="fas fa-question-circle"></i> ' + cell.innerText + '</span>';
            }
        });
    });
};

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
        'a, button, .card, .action-btn, tr, .nav-links li'
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