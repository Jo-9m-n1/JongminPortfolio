window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const body = document.body;
    const html = document.documentElement;
    const themeIcon = document.querySelector('#themeToggle i');
    
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
        html.classList.add('dark-mode');
        if (themeIcon) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
    }

    const themeBtn = document.getElementById('themeToggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', (e) => {
            e.stopPropagation(); 
            
            const isDark = body.classList.toggle('dark-mode');
            html.classList.toggle('dark-mode'); 
            
            const icon = themeBtn.querySelector('i');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            
            if (icon) {
                icon.style.transition = 'transform 0.4s ease';
                icon.style.transform = isDark ? 'rotate(360deg)' : 'rotate(-360deg)';
                
                setTimeout(() => {
                    if(isDark) {
                        icon.classList.replace('fa-moon', 'fa-sun');
                    } else {
                        icon.classList.replace('fa-sun', 'fa-moon');
                    }
                    icon.style.transform = 'rotate(0deg)';
                }, 200);
            }
        });
    }

    const menuTrigger = document.getElementById('menuTrigger');
    const menuDropdown = document.getElementById('expandablePill');

    if (menuTrigger && menuDropdown) {
        menuTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            menuDropdown.classList.toggle('active');
            menuTrigger.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!menuDropdown.contains(e.target)) {
                menuDropdown.classList.remove('active');
                menuTrigger.classList.remove('active');
            }
        });
    }
});

let activeFilters = ['all'];


function filterSelection(c) {
    if (c === 'all') {
        activeFilters = ['all'];
    } else {
        activeFilters = activeFilters.filter(f => f !== 'all');
        if (activeFilters.includes(c)) {
            activeFilters = activeFilters.filter(f => f !== c);
        } else {
            activeFilters.push(c);
        }
        if (activeFilters.length === 0) activeFilters = ['all'];
    }
    updateUI();
    applyFilterEffect();
}

function applyFilterEffect() {
    const items = document.getElementsByClassName("filter-item");
    const noResultsMsg = document.getElementById("no-results");
    const achievementsRow = document.getElementById("achievements-row");
    let visibleCount = 0;

    for (let item of items) {
        let isMatch = activeFilters.includes('all') || 
                    activeFilters.every(filter => item.classList.contains(filter));
        
        if (isMatch) {
            item.style.display = "block";
            item.style.opacity = "1";
            item.classList.add("filter-animate");
            visibleCount++;
        } else {
            item.style.display = "none";
            item.style.opacity = "0";
            item.classList.remove("filter-animate");
        }
    }

    if (noResultsMsg) noResultsMsg.style.display = (visibleCount === 0) ? "block" : "none";
    if (achievementsRow) achievementsRow.style.display = (visibleCount === 0) ? "none" : "flex";
}

function updateUI() {
    const buttons = document.getElementsByClassName("filter-btn");
    for (let btn of buttons) {
        const filterVal = btn.getAttribute('data-filter');
        if (activeFilters.includes(filterVal)) {
            btn.classList.add("active");
        } else {
            btn.classList.remove("active");
        }
    }
}

let mouseX = window.innerWidth / 2;
let mouseY = window.innerHeight / 2;
let currentX = mouseX;
let currentY = mouseY;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
});

function animateBlobs() {
    currentX += (mouseX - currentX) * 0.15;
    currentY += (mouseY - currentY) * 0.15;

    const cursorBlob = document.getElementById('cursorBlob');
    const blobs = document.querySelectorAll('.glow-blob');

    if (cursorBlob) {
        cursorBlob.style.left = `${currentX}px`;
        cursorBlob.style.top = `${currentY}px`;
    }

    blobs.forEach((blob, index) => {
        const moveX = (currentX - window.innerWidth / 2) / (25 + index * 5);
        const moveY = (currentY - window.innerHeight / 2) / (25 + index * 5);
        blob.style.transform = `translate(${moveX}px, ${moveY}px)`;
    });

    requestAnimationFrame(animateBlobs);
}
animateBlobs();

document.addEventListener('mousedown', () => {
    const cursorBlob = document.getElementById('cursorBlob');
    if (cursorBlob) cursorBlob.style.width = '700px';
});

document.addEventListener('mouseup', () => {
    const cursorBlob = document.getElementById('cursorBlob');
    if (cursorBlob) cursorBlob.style.width = '500px';
});

document.addEventListener('mousemove', (e) => {
    const heroContent = document.querySelector('.hero .container');
    if (!heroContent) return;

    const x = (window.innerWidth / 2 - e.clientX) / 50;
    const y = (window.innerHeight / 2 - e.clientY) / 50;

    heroContent.style.transform = `rotateY(${x}deg) rotateX(${-y}deg)`;
});

const animateCounters = () => {
    const counters = document.querySelectorAll('.counter');
    const duration = 1500;

    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const hasPlus = counter.getAttribute('data-plus') === 'true';
        let startTime = null;

        const step = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            
            const currentValue = Math.floor(progress * target);
            counter.innerText = currentValue.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                counter.innerText = target.toLocaleString() + (hasPlus ? "+" : "");
            }
        };

        requestAnimationFrame(step);
    });
};

document.addEventListener("DOMContentLoaded", () => {
    const funnyEmojis = ['🤓', '🤡', '🤪', '🥸', '🥴', '🍌'];
    let typedKeys = "";
    let isRaining = false;


    function triggerOliverRain() {
        if (isRaining) return;
        isRaining = true;

        for (let i = 0; i < 80; i++) {
            setTimeout(() => {
                const emojiNode = document.createElement('div');
                emojiNode.classList.add('oliver-emoji-drop');
                emojiNode.innerText = funnyEmojis[Math.floor(Math.random() * funnyEmojis.length)];
                
                emojiNode.style.left = Math.random() * 100 + 'vw';
                emojiNode.style.fontSize = (Math.random() * 2 + 1.5) + 'rem';
                emojiNode.style.animationDuration = (Math.random() * 2 + 2) + 's';
                
                document.body.appendChild(emojiNode);

                setTimeout(() => {
                    emojiNode.remove();
                }, 5000); 
            }, i * 60);
        }

        setTimeout(() => {
            isRaining = false;
        }, 3000);
    }

    window.addEventListener("keydown", (e) => {
        if(e.key.length === 1) {
            typedKeys += e.key.toLowerCase();
        }
        
        if (typedKeys.length > 12) {
            typedKeys = typedKeys.slice(-12);
        }
        
        if (typedKeys === "oliverisdumb") {
            triggerOliverRain();
            typedKeys = "";
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const words = [
        "a Computer Scientist", 
        "a Full-stack Developer",  
        "a Problem Solver"
    ];
    
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    
    const typingElement = document.querySelector(".typing-text");
    const cursorElement = document.querySelector(".typing-cursor");
    
    if(!typingElement) return;

    function type() {
        const currentWord = words[wordIndex];
        
        if (isDeleting) {
            typingElement.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typingElement.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
        }

        let typeSpeed = isDeleting ? 40 : 100;

        if (!isDeleting && charIndex === currentWord.length) {
            typeSpeed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex++;
            if (wordIndex >= words.length) {
                wordIndex = 0;
            }
            typeSpeed = 500;
        }

        setTimeout(type, typeSpeed);
    }

    setTimeout(type, 1000);
});

window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    const progressBar = document.getElementById("progress-bar");
    if (progressBar) progressBar.style.width = scrolled + "%";
});

document.addEventListener("DOMContentLoaded", function() {
    const logo = `
    ██╗ ██████╗ ███╗   ██╗ ██████╗ ███╗   ███╗██╗███╗   ██╗
    ██║██╔═══██╗████╗  ██║██╔════╝ ████╗ ████║██║████╗  ██║
    ██║██║   ██║██╔██╗ ██║██║  ███╗██╔████╔██║██║██╔██╗ ██║
██  ██║██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║
╚████╔╝╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║
 ╚═══╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝
    `;

    console.log(`%c${logo}`, "color: #0d6efd; font-weight: bold;");
    console.log("%cWelcome to My Portfolio!", "color: #0d6efd; font-size: 20px; font-weight: bold;");
});

document.addEventListener('DOMContentLoaded', function() {
    const chartCtx = document.getElementById('categoryBarChart');
    if (!chartCtx) return;

    const ctx = chartCtx.getContext('2d');
    
    const getThemeColor = () => {
        return document.body.classList.contains('dark-mode') ? '#ffffff' : '#1e293b';
    };

    const categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Software', 'Hardware', 'Math'],
            datasets: [{
                label: 'Count',
                data: [4, 1, 3],
                backgroundColor: [
                    'rgba(212, 175, 55, 0.9)',
                    'rgba(16, 185, 129, 0.8)', 
                    'rgba(139, 92, 246, 0.8)'
                ],
                borderRadius: 50,
                borderSkipped: false,
                barThickness: 18
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { display: false },
                y: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { 
                        color: getThemeColor(),
                        font: { family: "'Inter', sans-serif", weight: '700', size: 14 }
                    }
                }
            }
        }
    });

    const observer = new MutationObserver(() => {
        categoryChart.options.scales.y.ticks.color = getThemeColor();
        categoryChart.update();
    });

    observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });
});

document.addEventListener("DOMContentLoaded", () => {
    const wrapper = document.getElementById('countdown-wrapper');
    const widget = document.getElementById('countdown-widget');
    
    if (!widget) return;

    const rawData = widget.getAttribute('data-events');
    if (!rawData || rawData === "[]") {
        if (wrapper) wrapper.style.display = 'none';
        return;
    }
    
    const allEvents = JSON.parse(rawData);
    const rawEvents = allEvents.filter(ev => 
        ev.title && ev.title.includes("Will Participate") && ev['start-date'] && ev['end-date']
    );

    const now = new Date();
    let targetEvent = null;
    let isOngoing = false;
    let minDiff = Infinity;

    rawEvents.forEach(ev => {
        const startDate = new Date(ev['start-date']);
        const endDate = new Date(ev['end-date']);

        if (now >= startDate && now <= endDate) {
            targetEvent = {
                title: ev.title.replace("Will Participate: ", ""),
                dateStr: ev.date,
                startDate: startDate,
                endDate: endDate
            };
            isOngoing = true;
        } else if (!isOngoing && startDate > now) {
            const diff = startDate - now;
            if (diff < minDiff) {
                minDiff = diff;
                targetEvent = {
                    title: ev.title.replace("Will Participate: ", ""),
                    dateStr: ev.date,
                    startDate: startDate,
                    endDate: endDate
                };
            }
        }
    });

    if (!targetEvent) {
        if (wrapper) wrapper.style.display = 'none';
        return;
    }

    const titleEl = document.getElementById('next-event-title');
    const dateEl = document.getElementById('next-event-date');
    const timerEl = document.getElementById('countdown-timer');
    const badge = widget.querySelector('.badge');

    if (titleEl) titleEl.innerText = targetEvent.title;

    function switchToLiveTheme() {
        if (dateEl) dateEl.innerText = "HACKING IN PROGRESS...";
        if (timerEl) {
            timerEl.style.fontSize = "1.8rem";
            timerEl.innerHTML = "I am currently in this competition!";
            timerEl.style.color = "#ff4757";
        }
        if (badge) {
            badge.className = "badge bg-danger mb-2 rounded-pill px-3 py-2 fw-bold text-white";
            badge.innerHTML = `LIVE NOW`;
        }
    }

    function launchCelebration() {
        if (typeof confetti === 'undefined') return;
        const duration = 5 * 1000;
        const animationEnd = Date.now() + duration;
        const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };

        const interval = setInterval(function() {
            const timeLeft = animationEnd - Date.now();
            if (timeLeft <= 0) return clearInterval(interval);
            const particleCount = 50 * (timeLeft / duration);
            confetti({ ...defaults, particleCount, origin: { x: Math.random() * 0.3, y: Math.random() - 0.2 } });
            confetti({ ...defaults, particleCount, origin: { x: Math.random() * 0.3 + 0.7, y: Math.random() - 0.2 } });
        }, 250);
    }

    let hasCelebrated = false;
    function handleIntersectionCelebration() {
        if (hasCelebrated) return;
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !hasCelebrated) {
                    hasCelebrated = true;
                    launchCelebration();
                    switchToLiveTheme();
                    observer.unobserve(widget);
                }
            });
        }, { threshold: 0.5 });
        observer.observe(widget);
    }

    if (isOngoing) {
        switchToLiveTheme();
        return; 
    }

    if (dateEl) dateEl.innerText = `Scheduled for: ${targetEvent.dateStr}`;

    let isInitialLoad = true;

    function updateCountdown() {
        const currentTime = new Date();
        const timeRemaining = targetEvent.startDate - currentTime;

        if (timeRemaining <= 0) {
            handleIntersectionCelebration();
            return;
        }

        const targetDays = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
        const targetHours = Math.floor(timeRemaining / (1000 * 60 * 60));
        const targetMinutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
        const targetSeconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

        function getTimerHTML(d, h, m, s) {
            const hStr = String(h).padStart(2, '0');
            const mStr = String(m).padStart(2, '0');
            const sStr = String(s).padStart(2, '0');
            if (d > 0) {
                const dayLabel = (d === 1) ? "Day" : "Days";
                return `<span class="day-part">${d} ${dayLabel} Left</span>
                        <span class="time-digits">${hStr}:${mStr}:${sStr}</span>`;
            } else {
                return `<span class="time-digits">${hStr}:${mStr}:${sStr}</span>`;
            }
        }

        if (isInitialLoad) {
            isInitialLoad = false;
            let startTimestamp = null;
            const duration = 2000;

            function step(timestamp) {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                
                const d = Math.floor(progress * targetDays);
                const h = Math.floor(progress * targetHours);
                const m = Math.floor(progress * targetMinutes);
                const s = Math.floor(progress * targetSeconds);

                if (timerEl) timerEl.innerHTML = getTimerHTML(d, h, m, s);

                if (progress < 1) {
                    window.requestAnimationFrame(step);
                } else {
                    setInterval(updateCountdown, 1000);
                }
            }
            window.requestAnimationFrame(step);
        } else {
            if (timerEl) timerEl.innerHTML = getTimerHTML(targetDays, targetHours, targetMinutes, targetSeconds);
        }
    }

    updateCountdown();
});

window.addEventListener('load', animateCounters);