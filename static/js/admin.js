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
            counter.innerText = '0';
            const count = new countUp.CountUp(counter, target, {
                duration: 2.5,
                separator: ','
            });
            count.start();
        }
    });
});

// ==================== SEARCH TABLE ====================
function searchTable() {
    let input = document.getElementById("search").value.toLowerCase();
    let rows = document.getElementById("logTable").getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        let text = rows[i].innerText.toLowerCase();
        rows[i].style.display = text.includes(input) ? "" : "none";
    }
}

// ==================== HIGHLIGHT TABLE RESULTS ====================
window.addEventListener('load', function() {
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
});

// ==================== SWEETALERT FORM CONFIRMATIONS ====================

// Keyword Form
const keywordForm = document.getElementById('keywordForm');
if (keywordForm) {
    keywordForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const keyword = this.querySelector('input[name="keyword"]').value.trim();
        const category = this.querySelector('select[name="category"]').value;

        if (keyword === "") {
            Swal.fire({
                icon: 'error',
                title: 'Empty Field',
                text: 'Please enter a keyword!',
                background: '#112240',
                color: '#e6f1ff',
                confirmButtonColor: '#00d4ff'
            });
            return;
        }

        Swal.fire({
            title: 'Add Keyword?',
            html: `Add "<b>${keyword}</b>" to <b>${category}</b> list?`,
            icon: 'question',
            background: '#112240',
            color: '#e6f1ff',
            showCancelButton: true,
            confirmButtonColor: '#00d4ff',
            cancelButtonColor: '#ff6b6b',
            confirmButtonText: 'Yes, Add it!',
            cancelButtonText: 'Cancel'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({
                    icon: 'success',
                    title: 'Adding...',
                    text: 'Please wait',
                    background: '#112240',
                    color: '#e6f1ff',
                    timer: 1000,
                    showConfirmButton: false
                });
                setTimeout(() => keywordForm.submit(), 1000);
            }
        });
    });
}

// URL Form
const urlForm = document.getElementById('urlForm');
if (urlForm) {
    urlForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const url = this.querySelector('input[name="url"]').value.trim();

        if (url === "") {
            Swal.fire({
                icon: 'error',
                title: 'Empty Field',
                text: 'Please enter a URL!',
                background: '#112240',
                color: '#e6f1ff',
                confirmButtonColor: '#00d4ff'
            });
            return;
        }

        Swal.fire({
            title: 'Blacklist URL?',
            html: `Add <b>${url}</b> to blacklist?`,
            icon: 'warning',
            background: '#112240',
            color: '#e6f1ff',
            showCancelButton: true,
            confirmButtonColor: '#ff6b6b',
            cancelButtonColor: '#8892b0',
            confirmButtonText: 'Yes, Block it!',
            cancelButtonText: 'Cancel'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({
                    icon: 'success',
                    title: 'Adding...',
                    text: 'Blacklisting URL',
                    background: '#112240',
                    color: '#e6f1ff',
                    timer: 1000,
                    showConfirmButton: false
                });
                setTimeout(() => urlForm.submit(), 1000);
            }
        });
    });
}

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
            events: { onhover: { enable: true, mode: 'grab' }},
            modes: { grab: { distance: 150, line_linked: { opacity: 0.6 }}}
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
        'a, button, input, select, .card, .box, tr, .nav-links li'
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