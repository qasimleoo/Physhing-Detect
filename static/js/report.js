// ==================== AOS INIT ====================
if (typeof AOS !== 'undefined') {
    AOS.init({
        duration: 800,
        once: true
    });
}

// ==================== LOAD DATA ====================
fetch('/report-data')
.then(res => res.json())
.then(data => {
    let logs = data.logs;

    if (!logs || logs.length === 0) {
        animateCount("totalScans", 0);
        animateCount("totalPhishing", 0);
        animateCount("totalSafe", 0);
        animateCount("totalSuspicious", 0);
        return;
    }

    generateReport(logs);
})
.catch(err => {
    console.log("Error loading report data:", err);
});

// ==================== ANIMATE COUNTERS ====================
function animateCount(id, value) {
    if (typeof countUp !== 'undefined') {
        const counter = new countUp.CountUp(id, value, {
            duration: 2.5,
            separator: ','
        });
        counter.start();
    } else {
        document.getElementById(id).innerText = value;
    }
}

// ==================== GENERATE REPORT ====================
function generateReport(logs) {
    let totalScans = logs.length;
    let phishing = logs.filter(l => l.result && l.result.toLowerCase().includes("phishing")).length;
    let safe = logs.filter(l => l.result && l.result.toLowerCase().includes("safe")).length;
    let suspicious = logs.filter(l => l.result && l.result.toLowerCase().includes("suspicious")).length;

    // Animated counters
    animateCount("totalScans", totalScans);
    animateCount("totalPhishing", phishing);
    animateCount("totalSafe", safe);
    animateCount("totalSuspicious", suspicious);

    // Charts
    drawPieChart(safe, suspicious, phishing);
    drawBarChart(logs);
    showPatterns(logs);
}

// ==================== PIE CHART (Chart.js) ====================
function drawPieChart(safe, suspicious, phishing) {
    const ctx = document.getElementById("pieChart").getContext("2d");

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Safe', 'Suspicious', 'Phishing'],
            datasets: [{
                data: [safe, suspicious, phishing],
                backgroundColor: [
                    'rgba(2, 158, 111, 0.8)',
                    'rgba(247, 185, 72, 0.8)',
                    'rgba(240, 52, 52, 0.8)'
                ],
                borderColor: [
                    '#00b894',
                    '#fdcb6e',
                    '#ff6b6b'
                ],
                borderWidth: 2,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#e6f1ff',
                        font: {
                            family: 'Poppins',
                            size: 13
                        },
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 34, 64, 0.95)',
                    titleColor: '#00d4ff',
                    bodyColor: '#e6f1ff',
                    borderColor: '#00d4ff',
                    borderWidth: 1,
                    padding: 12,
                    titleFont: { family: 'Poppins', size: 13 },
                    bodyFont: { family: 'Poppins', size: 13 }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 2000
            }
        }
    });
}

// ==================== BAR CHART (Chart.js) ====================
function drawBarChart(logs) {
    const ctx = document.getElementById("barChart").getContext("2d");

    let days = {};
    logs.forEach(l => {
        if (l.date) {
            let day = l.date.substring(0, 10);
            days[day] = (days[day] || 0) + 1;
        }
    });

    let keys = Object.keys(days).slice(-7);
    let values = keys.map(k => days[k]);

    if (keys.length === 0) {
        keys = ['No Data'];
        values = [0];
    }

    // Format dates
    let labels = keys.map(k => {
        if (k === 'No Data') return k;
        let date = new Date(k);
        return date.toLocaleDateString('en-US', { weekday: 'short', day: 'numeric' });
    });

    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 280);
    gradient.addColorStop(0, 'rgba(0, 212, 255, 0.8)');
    gradient.addColorStop(1, 'rgba(0, 212, 255, 0.2)');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Scans',
                data: values,
                backgroundColor: gradient,
                borderColor: '#00d4ff',
                borderWidth: 2,
                borderRadius: 8,
                hoverBackgroundColor: '#00d4ff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 34, 64, 0.95)',
                    titleColor: '#00d4ff',
                    bodyColor: '#e6f1ff',
                    borderColor: '#00d4ff',
                    borderWidth: 1,
                    padding: 12,
                    titleFont: { family: 'Poppins', size: 13 },
                    bodyFont: { family: 'Poppins', size: 13 }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#8892b0',
                        font: { family: 'Poppins', size: 12 }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        color: '#8892b0',
                        font: { family: 'Poppins', size: 12 }
                    },
                    grid: {
                        display: false
                    }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            }
        }
    });
}

// ==================== PATTERNS ====================
function showPatterns(logs) {
    let patterns = {};

    logs.forEach(l => {
        if (l.result) {
            let key = l.result.toLowerCase().includes("phishing") ? "Phishing Detected" :
                      l.result.toLowerCase().includes("safe") ? "Safe Results" : "Suspicious Activity";

            patterns[key] = (patterns[key] || 0) + 1;
        }
    });

    let list = document.getElementById("patternsList");
    list.innerHTML = "";

    Object.keys(patterns).forEach(p => {
        let li = document.createElement("li");
        li.innerText = p + ": " + patterns[p] + " detections";
        list.appendChild(li);
    });

    if (Object.keys(patterns).length === 0) {
        let li = document.createElement("li");
        li.innerText = "No patterns detected yet";
        list.appendChild(li);
    }
}

// ==================== EXPORT REPORT ====================
function exportReport() {
    let total = document.getElementById("totalScans").innerText;
    let phishing = document.getElementById("totalPhishing").innerText;
    let safe = document.getElementById("totalSafe").innerText;
    let suspicious = document.getElementById("totalSuspicious").innerText;

    let text = `
╔════════════════════════════════════════╗
║     PHISHGUARD - REPORT SUMMARY        ║
╚════════════════════════════════════════╝

Generated: ${new Date().toLocaleString()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Total Scans    : ${total}
  Safe Results   : ${safe}
  Suspicious     : ${suspicious}
  Phishing Found : ${phishing}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  PhishGuard Anti-Phishing System
  AI-Powered Detection & Analytics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    `;

    let blob = new Blob([text], {type: "text/plain"});
    let link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "phishguard_report_" + new Date().toISOString().split('T')[0] + ".txt";
    link.click();
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
        'a, button, .card, .chart-card, #patternsList li, .nav-links li'
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