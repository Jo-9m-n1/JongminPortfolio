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

        const menuLinks = menuDropdown.querySelectorAll('.pill-menu-content a');
        menuLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                const currPath = window.location.pathname;
                
                const isSimpleAnchor = href.startsWith('#');
                
                const isSamePage = href === currPath || (href === '/' && currPath === '/');
                
                const isPathAnchor = href.includes('#') && (href.split('#')[0] === currPath || href.split('#')[0] === '');

                if (isSimpleAnchor || isSamePage || isPathAnchor) {
                    
                    if (isSamePage && !href.includes('#')) {
                        e.preventDefault(); 
                    }

                    menuDropdown.classList.remove('active');
                    menuTrigger.classList.remove('active');

                    if (href.includes('#')) {
                        const targetId = href.split('#')[1];
                        const targetElem = document.getElementById(targetId);
                        if (targetElem) {
                            e.preventDefault();
                            targetElem.scrollIntoView({ behavior: 'smooth' });
                            history.pushState(null, null, href);
                        }
                    }
                }
            });
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
        "a Full-stack Developer"
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
            typeSpeed = 3500;
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
        ev.title && 
        (ev.title.includes("Will Participate") || ev.title.includes("Currently Participating")) && 
        ev['start-date'] && 
        ev['end-date']
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
                title: ev.title.replace(/(Will Participate \| |Currently Participating \| )/, ""),                dateStr: ev.date,
                startDate: startDate,
                endDate: endDate,
                rawStartDate: ev['start-date']
            };
            isOngoing = true;
        } else if (!isOngoing && startDate > now) {
            const diff = startDate - now;
            if (diff < minDiff) {
                minDiff = diff;
                targetEvent = {
                    title: ev.title.replace("Will Participate | ", ""),
                    dateStr: ev.date,
                    startDate: startDate,
                    endDate: endDate,
                    rawStartDate: ev['start-date']
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
        if (dateEl) dateEl.innerText = "IN PROGRESS...";
        if (timerEl) {
            timerEl.style.fontSize = "1.8rem";
            timerEl.innerHTML = "I am currently in this competition!";
            timerEl.style.color = "#fe4a59";
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
        
        const todayAtMidnight = new Date(currentTime.getFullYear(), currentTime.getMonth(), currentTime.getDate()).getTime();
        const dateParts = targetEvent.rawStartDate.split('T')[0].split('-');
        const eventAtMidnight = new Date(
            parseInt(dateParts[0]), 
            parseInt(dateParts[1]) - 1, 
            parseInt(dateParts[2])
        ).getTime();

        const dayDiff = eventAtMidnight - todayAtMidnight;
        const targetDays = Math.ceil(dayDiff / (1000 * 60 * 60 * 24));

        const timeRemaining = targetEvent.startDate - currentTime;

        if (timeRemaining <= 0) {
            handleIntersectionCelebration();
            return;
        }

        const targetHours = Math.floor((timeRemaining / (1000 * 60 * 60)));
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

let winterCode1 = "montreal";
let winterCode2 = "snow";
let winterInput = "";

document.addEventListener("keydown", (e) => {
    winterInput += e.key.toLowerCase();
    
    if (winterInput.length > winterCode1.length) {
        winterInput = winterInput.slice(-winterCode1.length);
    }
    
    if (winterInput.includes(winterCode1) || winterInput.includes(winterCode2)) {
        startBlizzard();
        winterInput = "";
    }
});

function startBlizzard() {
    if (document.body.classList.contains('blizzard-mode')) return;

    document.body.classList.add('blizzard-mode');

    const snowContainer = document.createElement('div');
    snowContainer.className = 'snow-container';
    snowContainer.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none; z-index: 99999; overflow: hidden;
        opacity: 0; transition: opacity 2s ease;
    `;
    document.body.appendChild(snowContainer);

    setTimeout(() => snowContainer.style.opacity = "1", 50);

    for (let i = 0; i < 100; i++) {
        let snowflake = document.createElement('div');
        let size = Math.random() * 4 + 2;
        let left = Math.random() * 100;
        let duration = Math.random() * 3 + 2;
        let delay = Math.random() * 2;

        snowflake.style.cssText = `
            position: absolute; top: -10px; left: ${left}vw;
            width: ${size}px; height: ${size}px;
            background: white; border-radius: 50%;
            opacity: ${Math.random() * 0.8 + 0.2};
            filter: blur(${Math.random() * 2}px);
            animation: fall ${duration}s linear ${delay}s infinite;
        `;
        snowContainer.appendChild(snowflake);
    }

    if (!document.getElementById('blizzard-style')) {
        const style = document.createElement('style');
        style.id = 'blizzard-style';
        style.innerHTML = `
            @keyframes fall {
                0% { transform: translateY(-10vh) translateX(0); }
                100% { transform: translateY(110vh) translateX(${Math.random() * 20 - 10}vw); }
            }
        `;
        document.head.appendChild(style);
    }

    setTimeout(() => {
        document.body.classList.remove('blizzard-mode');
        
        snowContainer.style.opacity = "0";
        
        setTimeout(() => {
            snowContainer.remove();
        }, 2000); 
    }, 15000);
}
const terminalSecret = "terminal";
let terminalKeys = "";
let sessionHistory = [];
let historyIndex = -1;

document.addEventListener("keydown", (e) => {
    if (document.getElementById('terminal-overlay')) return;
    terminalKeys += e.key.toLowerCase();
    if (terminalKeys.length > terminalSecret.length) {
        terminalKeys = terminalKeys.slice(-terminalSecret.length);
    }
    if (terminalKeys === terminalSecret) {
        initTerminal();
        terminalKeys = "";
    }
});

let virtualPackages = ['dev']; 

function initTerminal() {
    document.body.classList.add('terminal-active');
    const terminalHTML = 
`        <div id="terminal-overlay">
            <div class="terminal-output" id="term-output">
Jongmin OS [Version 1.0.0]
(c) 2026 Jongmin Lee. All rights reserved.

Type 'help' to see a list of available commands.
            </div>
            <div class="terminal-input-line">
                <span class="terminal-prompt">jongmin@portfolio:~$</span>
                <input type="text" id="terminal-input-field" autocomplete="off" spellcheck="false" autofocus>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', terminalHTML);
    const overlay = document.getElementById('terminal-overlay');
    const inputField = document.getElementById('terminal-input-field');
    const outputArea = document.getElementById('term-output');
    requestAnimationFrame(() => { overlay.classList.add('active');
        setTimeout(() => {
            inputField.focus();
        }, 50); 
     });
    
    const commands = ['help', 'neofetch', 'whoami', 'ls', 'cd', 'cat', 'date', 'clear', 'exit', 'uptime', 'npm', 'ping', 'history', 'env', 'df', 'echo', 'reboot', 'sudo', 'cal'];
    const directories = ['projects', 'achievements'];
    const files = ['skills.txt', 'contact.txt', 'hackathons.txt', 'education.txt', 'projects.txt'];

    inputField.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();
            
            const words = this.value.toLowerCase().split(' ');
            const currentWord = words[words.length - 1]; 
            let matches = [];

            if (words.length === 1) {
                matches = commands.filter(cmd => cmd.startsWith(currentWord));
                if (matches.length === 1) this.value = matches[0] + " ";
            } 
            else if (words.length === 2 && words[0] === 'cd') {
                matches = directories.filter(dir => dir.startsWith(currentWord));
                if (matches.length === 1) this.value = `cd ${matches[0]}`;
            }
            else if (words.length === 2 && words[0] === 'cat') {
                matches = files.filter(f => f.startsWith(currentWord));
                if (matches.length === 1) this.value = `cat ${matches[0]}`;
            }

            if (matches.length > 1) {
                return;
            }
        }
    });

    overlay.addEventListener('click', () => inputField.focus());

    inputField.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const cmd = this.value.trim();
            this.value = '';
            if (cmd) {
                sessionHistory.push(cmd);
                historyIndex = -1;
                outputArea.innerHTML += `\n<span class="terminal-prompt">jongmin@portfolio:~$</span> ${cmd}\n`;
                processCommand(cmd, outputArea, overlay);
            }
            overlay.scrollTop = overlay.scrollHeight;
        } else if (e.key === 'ArrowUp') {
            if (sessionHistory.length > 0) {
                if (historyIndex === -1) historyIndex = sessionHistory.length;
                if (historyIndex > 0) {
                    historyIndex--;
                    this.value = sessionHistory[historyIndex];
                }
            }
            e.preventDefault();
        } else if (e.key === 'ArrowDown') {
            if (historyIndex !== -1) {
                if (historyIndex < sessionHistory.length - 1) {
                    historyIndex++;
                    this.value = sessionHistory[historyIndex];
                } else {
                    historyIndex = -1;
                    this.value = "";
                }
            }
        } else if (e.key === 'Escape') {
            closeTerminal(overlay);
        }
    });
}

function processCommand(cmd, outputArea, overlay) {
    const args = cmd.toLowerCase().split(' ');
    const mainCmd = args[0];
    if (!mainCmd) return;

    switch(mainCmd) {
        case 'help':
            outputArea.innerHTML += 
`Available commands:
  <span class="term-keyword">npm install</span>   - Install a new package
  <span class="term-keyword">npm run dev</span>   - Start local development server
  <span class="term-keyword">neofetch</span>      - Display system information
  <span class="term-keyword">whoami</span>        - Display current user info
  <span class="term-keyword">ls</span>            - List directory contents
  <span class="term-keyword">cd</span>            - Navigate to a directory
  <span class="term-keyword">cat</span>           - Read a file
  <span class="term-keyword">df</span>            - Report disk space usage
  <span class="term-keyword">history</span>       - Display command history
  <span class="term-keyword">date</span>          - Print system date and time
  <span class="term-keyword">uptime</span>        - Display how long the system has been running
  <span class="term-keyword">env</span>           - List environment variables
  <span class="term-keyword">echo</span>          - Display a line of text or a string
  <span class="term-keyword">ping</span>          - Send ICMP ECHO_REQUEST
  <span class="term-keyword">cal</span>           - Display a calendar
  <span class="term-keyword">sudo</span>          - Execute a command as the superuser
  <span class="term-keyword">reboot</span>        - Restart the system (Reload page)
  <span class="term-keyword">clear</span>         - Clear the terminal screen
  <span class="term-keyword">exit</span>          - Close the terminal
`;
            break;

        case 'neofetch':
            outputArea.innerHTML += 
`                 <span class="term-keyword">OS:</span> JongminOS v1.0.0
<span style="color:#D80621;">      /\\      </span>   <span class="term-keyword">Host:</span> Montreal, QC
<span style="color:#D80621;">     /  \\     </span>   <span class="term-keyword">Kernel:</span> 18.0.0-student
<span style="color:#D80621;">    /____\\    </span>   <span class="term-keyword">Uptime:</span> 18 years
<span style="color:#D80621;">   /_|  |_\\   </span>   <span class="term-keyword">Packages:</span> Python, Next.js, Flask
<span style="color:#D80621;">     |  |     </span>   <span class="term-keyword">Languages:</span> KR, EN, FR
                 <span class="term-keyword">Hobbies:</span> Badminton, Piano, Movies
`;
            break;

        case 'npm':
            const subCmd = args[1];
            const pkg = args[2];

            if (subCmd === 'install' || subCmd === 'i') {
                if (!pkg) {
                    outputArea.innerHTML += `npm <span style="color: #ff5f56;">ERR!</span> install: Provide a package name.\n`;
                    break;
                }

                if (virtualPackages.includes(pkg)) {
                    outputArea.innerHTML += `npm <span style="color: #fbbf24;">info</span> ${pkg} is already installed in the virtual_registry.\n`;
                    break;
                }
                
                outputArea.innerHTML += `npm <span style="color: #4ade80;">installing</span> ${pkg}...\n`;
                
                const progressId = 'progress-' + Math.random().toString(36).substr(2, 9);
                outputArea.innerHTML += `<div id="${progressId}">[          ] 0%</div>`;
                overlay.scrollTop = overlay.scrollHeight;

                let progress = 0;
                const progressBar = document.getElementById(progressId);
                
                const interval = setInterval(() => {
                    progress += 10;
                    const dots = "=".repeat(progress / 10);
                    const spaces = " ".repeat(10 - (progress / 10));
                    if (progressBar) progressBar.innerHTML = `[${dots}${spaces}] ${progress}%`;

                    if (progress >= 100) {
                        clearInterval(interval);
                        
                        if (!virtualPackages.includes(pkg)) {
                            virtualPackages.push(pkg);
                        }

                        outputArea.innerHTML += `<span style="color: #4ade80;">added 1 package and audited 2 packages in 0.8s</span>\n`;
                        outputArea.innerHTML += `found <span style="color: #4ade80;">0</span> vulnerabilities\n`;
                        overlay.scrollTop = overlay.scrollHeight;
                        
                        const inputField = document.getElementById('terminal-input-field');
                        if (inputField) inputField.focus();
                    }
                }, 150); 
            } 
            else if (subCmd === 'run') {
                if (!pkg) {
                    outputArea.innerHTML += `npm <span style="color: #ff5f56;">ERR!</span> run: Provide a script name\n`;
                    break;
                }

                if (virtualPackages.includes(pkg)) {
                    outputArea.innerHTML += `<span style="color: #4ade80;">> ${pkg}@1.0.0 start</span>\n`;
                    outputArea.innerHTML += `<span style="color: #4ade80;">> node index.js</span>\n\n`;
                    
                    setTimeout(() => {
                        outputArea.innerHTML += `[info] Initializing <span style="color: #3b82f6;">${pkg}</span> build...\n`;
                        outputArea.innerHTML += `<span style="color: #4ade80;">[SUCCESS]</span> App is running on port ${Math.floor(Math.random() * 5000 + 3000)}\n`;
                        overlay.scrollTop = overlay.scrollHeight;
                    }, 600);
                } else {
                    outputArea.innerHTML += `npm <span style="color: #ff5f56;">ERR!</span> missing script: ${pkg}\n`;
                    outputArea.innerHTML += `<span style="color: #666;">Tip: Try running 'npm install ${pkg}' first.</span>\n`;
                }
            } else {
                outputArea.innerHTML += `Usage: npm install [package] | npm run [package]\n`;
            }
            break;

        case 'sl':
            const train = [
                "      ====        ________                ___________ ",
                "  _D _|  |_______/        \\__   _________|           |",
                "   \\_ |===============H======| |   JONGMIN   |_______|",
                "    |=============H==============| |   LEE   |       |",
                "    |_____________oooooooooooooo_| |_________|_______|",
                "     OoooOoooOoooOoooOoooOoooOoooO  OoooOoooOoooOoooO "
            ];

            const slOverlay = document.createElement('div');
            slOverlay.style.position = 'absolute'; 
            slOverlay.style.left = overlay.offsetWidth + 'px';
            slOverlay.style.whiteSpace = 'pre';
            slOverlay.style.fontFamily = 'monospace';
            slOverlay.style.color = '#fff'; 
            slOverlay.style.zIndex = '1000';
            slOverlay.style.pointerEvents = 'none'; 
            slOverlay.innerHTML = train.join('\n');
            overlay.appendChild(slOverlay);

            let currentPos = overlay.offsetWidth;
            const trainWidth = 550;

            const slInterval = setInterval(() => {
                currentPos -= 10; 
                slOverlay.style.left = currentPos + 'px';

                slOverlay.style.top = (overlay.scrollTop + 20) + 'px';

                if (currentPos < -trainWidth) {
                    clearInterval(slInterval);
                    slOverlay.remove();
                    inputField.focus(); 
                }
            }, 33); 

            outputArea.innerHTML += `<span style="color: #666;">Look! A wild Steam Locomotive appeared!</span>\n`;
            overlay.scrollTop = overlay.scrollHeight;
            
            break;

        case 'cal':
            const rightnow = new Date();
            const year = rightnow.getFullYear();
            const month = rightnow.getMonth();
            const today = rightnow.getDate();

            const monthName = rightnow.toLocaleString('default', { month: 'long' });
            
            const firstDay = new Date(year, month, 1).getDay();
            const lastDate = new Date(year, month + 1, 0).getDate();

            let calOutput = `      ${monthName} ${year}\n`;
            calOutput += `Su Mo Tu We Th Fr Sa\n`;

            for (let i = 0; i < firstDay; i++) {
                calOutput += `   `;
            }

            for (let date = 1; date <= lastDate; date++) {
                if (date === today) {
                    calOutput += `<span style="color: #ffffff !important; font-weight: bold;">${date.toString().padStart(2, ' ')}</span> `;
                } else {
                    calOutput += `${date.toString().padStart(2, ' ')} `;
                }

                if ((date + firstDay) % 7 === 0) {
                    calOutput += `\n`;
                }
            }

            outputArea.innerHTML += `<pre style="font-family: monospace; line-height: 1.2;">${calOutput}</pre>`;
            break;

        case 'sudo':
            outputArea.innerHTML += `<span class="term-error">[sudo] password for jongmin: </span>\n`;
            outputArea.innerHTML += `<span class="term-error">Sorry, try again. This incident has been reported to the root user.</span>\n`;
            break;

        case 'echo':
            const message = args.slice(1).join(' ');
            if (!message) {
                outputArea.innerHTML += `\n`;
            } else {
                outputArea.innerHTML += `${message}\n`;
            }
            break;

        case 'catsay':
            const msg = args.slice(1).join(' ') || "Meow! Code is compiling...";
            const border = "-".repeat(msg.length + 4);
            outputArea.innerHTML += 
`  ${border}
  < ${msg} >
  ${border}
   \\
    \\  /\\_/\\
      ( o.o )
       > ^ <
`;
            break;

        case 'df':
            outputArea.innerHTML += 
`Filesystem           Size      Used      Avail  Use%  Mounted on
<span style="color:#FFD700;">/dev/hackathons      7.0G      6.0G      1.0G   86%  /mnt/trophy-case</span>
/dev/other          16.0G      8.4G      7.6G   52%  /home/jongmin

<span class="term-keyword">Status:</span> 6/7 Hackathons won 
Win Rate: <span style="color:#00ff00;">86%</span> [█████████░]
`;
            break;

        case 'reboot':
            const messages = [
                "System is going down for reboot NOW!",
                "Stopping system services...",
                "Unmounting file systems...",
                "Rebooting..."
            ];

            messages.forEach((msg, index) => {
                setTimeout(() => {
                    outputArea.innerHTML += `${msg}\n`;
                    outputArea.scrollTop = outputArea.scrollHeight;
                }, index * 950);
            });

            setTimeout(() => {
                window.location.href = "/";
            }, messages.length * 950);
            break;

        case 'history':
            let historyList = "";
            sessionHistory.forEach((item, index) => {
                historyList += `  ${index + 1}  ${item}\n`;
            });
            outputArea.innerHTML += historyList;
            break;

        case 'env':
            outputArea.innerHTML += `USER=jongmin\nSHELL=/bin/bash\nLANG=en_CA.UTF-8\nLOCATION=Montreal\nSTATUS=Available_For_Hire\n`;
            break;

        case 'date':
            const now = new Date();
            outputArea.innerHTML += `${now.toDateString()} ${now.toTimeString().split(' ')[0]}\n`;
            break;

        case 'whoami':
            outputArea.innerHTML += `Jongmin Lee\nFull-Stack Developer | Student at Dawson College\n`;
            break;

        case 'ls':
            if (args[1] === '-la' || args[1] === '-l') {
                outputArea.innerHTML += 
`drwxr-xr-x  2 jongmin jongmin  4096 Feb 25 23:52 <span class="term-keyword">projects</span>
drwxr-xr-x  2 jongmin jongmin  4096 Feb 10 09:15 <span class="term-keyword">achievements</span>
-rw-r--r--  1 jongmin jongmin  1024 Mar 11 10:19 projects.txt
-rw-r--r--  1 jongmin jongmin  1024 Mar 11 10:09 education.txt
-rw-r--r--  1 jongmin jongmin  1024 Feb 25 12:00 skills.txt
-rw-r--r--  1 jongmin jongmin  1024 Feb 22 11:30 hackathons.txt
-rw-r--r--  1 jongmin jongmin  1024 Feb 20 18:45 contact.txt
`;
            } else {
                outputArea.innerHTML += `<span class="term-keyword">projects/</span>   <span class="term-keyword">achievements/</span>   skills.txt   hackathons.txt   contact.txt   education.txt   projects.txt\n`;
            }
            break;

        case 'cat':
            if (args[1] === 'skills.txt') {
                outputArea.innerHTML += `[Languages] Python, JavaScript\n[Frameworks] Next.js, Flask\n`;
            } else if (args[1] === 'contact.txt') {
                outputArea.innerHTML += `LinkedIn: linkedin.com/in/jo-9m-n1\nGithub: github.com/jo-9m-n1\nGitLab: gitlab.com/jo_9m_n1\n`;
            } else if (args[1] === 'hackathons.txt') {
                outputArea.innerHTML += 
`May 2026 | Upcoming: DawsHacks
Apr 2026 | Upcoming: MariHacks
Apr 2026 | Upcoming: JacHacks
Mar 2026 | Upcoming: Championing AI for good
Mar 2026 | McGill AeroHacks <i class="fa-solid fa-trophy"></i>
Mar 2026 | @HACK <i class="fa-solid fa-trophy"></i>
Mar 2026 | GameJam de la FSÉ
Feb 2026 | Dialogue Internal Hackathon <i class="fa-solid fa-trophy"></i>
Jan 2026 | ConUHacks <i class="fa-solid fa-trophy"></i>
Nov 2025 | HackDécouverte <i class="fa-solid fa-trophy"></i>
May 2025 | Dawson Robotics Hackathon <i class="fa-solid fa-trophy"></i>
`;
            } else if (args[1] === 'education.txt') {
                outputArea.innerHTML += 
`2026 (Est.) - 2029 (Est.) | McGill University
2024 - 2026 (Est.)        | Dawson College
2019 - 2024               | Rosemount High School
`  
            } else if (args[1] === 'projects.txt') {
                outputArea.innerHTML += 
`May 2026 | Currently Working: Chemically Bonded
Mar 2026 | DeckMots
Feb 2026 | Personal Website
Feb 2026 | Dr. Bob <i class="fa-solid fa-trophy"></i>
Dec 2025 | Meeting App
Dec 2025 | J-Score*
` 
            } else if (!args[1]) {
                outputArea.innerHTML += `<span class="term-error">cat: missing file operand</span>\n`;
            } else {
                outputArea.innerHTML += `<span class="term-error">cat: ${args[1]}: No such file</span>\n`;
            }
            break;

        case 'ping':
            const target = args[1] || 'localhost';
            if (target.includes('mcgill')) {
                outputArea.innerHTML += `Pinging mcgill.ca [128.100.0.1]: time=12ms\n<span style="color:#00ff00;">Application status: Accepted</span>\n`;
            } else {
                outputArea.innerHTML += `Pinging ${target} [127.0.0.1]: time&lt;1ms\n`;
            }
            break;

        case 'cd':
            let dest = args[1] ? args[1].replace('/', '') : '';
            
            if (!dest || dest === '~' || dest === 'home') {
                outputArea.innerHTML += `Redirecting to Home...\n`;
                setTimeout(() => {
                    closeTerminal(overlay);
                    setTimeout(() => { window.location.href = '/'; }, 350);
                }, 800);
            } else {
                const targetElement = document.getElementById(dest);
                if (['projects', 'achievements'].includes(dest)) {
                    outputArea.innerHTML += `Navigating to /${dest}...\n`;
                    setTimeout(() => {
                        window.location.href = '/' + dest;
                    }, 800);
                } else {
                    const suggestions = {
                        'project': 'projects',
                        'achievement': 'achievements'
                    };

                    const inputDir = args[1];
                    const correction = suggestions[inputDir];

                    if (correction) {
                        outputArea.innerHTML += `<span class="term-error">cd: ${inputDir}: No such directory. Did you mean '${correction}'?</span>\n`;
                    } else {
                        outputArea.innerHTML += `<span class="term-error">cd: ${inputDir || ''}: No such directory</span>\n`;
                    }
                }
            }
            break;

        case 'clear':
            outputArea.innerHTML = '';
            break;

        case 'exit':
            outputArea.innerHTML += `Logging out...\n`;
            setTimeout(() => closeTerminal(overlay), 500);
            break;

        case 'uptime':
            const date = new Date();
            const timeString = date.toTimeString().split(' ')[0];
            outputArea.innerHTML += ` ${timeString} up 18 years, 3 users, load average: 0.00, 0.01, 0.05\n`;
            break;

        default:
            outputArea.innerHTML += `<span class="term-error">Command not found: ${mainCmd}</span>\n`;
    }
}

function closeTerminal(overlay) {
    overlay.classList.remove('active');
    document.body.classList.remove('terminal-active');
    setTimeout(() => { overlay.remove(); }, 500);
}

document.addEventListener('DOMContentLoaded', () => {
    const trophies = [
        { name: "McGill AeroHacks", type: "Hackathon", year: "2026" },
        { name: "@HACK", type: "Hackathon", year: "2026" },
        { name: "Dialogue Internal Hackathon", type: "Hackathon", year: "2026" },
        { name: "ConUHacks", type: "Hackathon", year: "2026" },
        { name: "HackDécouverte", type: "Hackathon", year: "2025" },
        { name: "Dawson Robotics Hackathon", type: "Hackathon", year: "2025" },
        { name: "Waterloo Cayley Math Contest", type: "Contest", year: "2022" },
        { name: "The Ultimate Math League", type: "Contest", year: "2019" },
        { name: "Ministry of Justice of the Republic of Korea", type: "Contest", year: "2016" },
        { name: "HME Math Contest", type: "Contest", year: "2016" },
        { name: "Sekwang Student Piano Competition", type: "Contest", year: "2015" },
        { name: "HME Math Contest", type: "Contest", year: "2014" },
        { name: "Dental Health Awareness Art Contest", type: "Contest", year: "2013" },
        { name: "International Children's Art Grand Exhibition", type: "Contest", year: "2011" },
        { name: "Children's Day Art Competition", type: "Contest", year: "2011" }
    ];

    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
    let konamiIndex = 0;

    document.addEventListener('keydown', (e) => {
        if (e.key.toLowerCase() === konamiCode[konamiIndex].toLowerCase() || e.key === konamiCode[konamiIndex]) {
            konamiIndex++;
            if (konamiIndex === konamiCode.length) {
                openTrophyRoom();
                konamiIndex = 0;
            }
        } else {
            konamiIndex = 0;
        }

        if (e.key === 'Escape' && document.getElementById('trophy-room')) {
            closeTrophyRoom();
        }
    });

    function openTrophyRoom() {
        if (document.getElementById('trophy-room')) return;

        const room = document.createElement('div');
        room.id = 'trophy-room';        
        room.innerHTML = `
            <div class="trophy-content">
                <button class="close-btn">✕</button>
                <h2 class="trophy-title">THE VAULT</h2>
                <p class="trophy-subtitle">15+ COMPETITION AWARDS</p>
                <div class="shelf-grid">
                    ${trophies.map(t => `
                        <div class="trophy-item">
                            <i class="fa-solid fa-trophy trophy-icon"></i>
                            <div class="trophy-info">
                                <span class="t-name">${t.name}</span>
                                <span class="t-year">${t.year}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        document.body.appendChild(room);

        room.addEventListener('click', (e) => {
            if (e.target === room) {
                closeTrophyRoom();
            }
        });

        const closeBtn = room.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', closeTrophyRoom);
        }

        requestAnimationFrame(() => {
            room.classList.add('active');
        });
    }

    function closeTrophyRoom() {
        const room = document.getElementById('trophy-room');
        if (!room) return;
        
        room.classList.remove('active');
        setTimeout(() => room.remove(), 400);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const buildNumber = document.getElementById('build-number');
    let tapCount = 0;
    let tapTimer;
    let isDeveloper = false;
    let toastTimeout;

    const toast = document.createElement('div');
    toast.id = 'android-toast';
    document.body.appendChild(toast);

    function showToast(msg) {
        toast.textContent = msg;
        toast.classList.add('show');
        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toast.classList.remove('show');
        }, 2000);
    }

    if (buildNumber) {
        buildNumber.addEventListener('click', () => {
            if (isDeveloper) {
                showToast("System is already running in Developer Mode.");
                return;
            }

            tapCount++;
            clearTimeout(tapTimer);

            const remaining = 7 - tapCount;

            if (remaining > 0 && remaining <= 3) {
                showToast(`[SYSTEM] ${remaining} steps away from Developer mode.`);
            } else if (remaining === 0) {
                isDeveloper = true;
                showToast("ACCESS GRANTED: Developer Mode activated.");
                activateDeveloperMode();
            }

            tapTimer = setTimeout(() => { 
                if (!isDeveloper) tapCount = 0; 
            }, 1500);
        });
    }

    function activateDeveloperMode() {
        document.body.spellcheck = false;
        document.designMode = "on";
        document.body.classList.add('developer-mode');

        const styleId = 'dev-mode-styles';
        if (!document.getElementById(styleId)) {
            const style = document.createElement('style');
            style.id = styleId;
            style.innerHTML = `
                body { animation: screenShake 0.4s ease-in-out; }
                
                .developer-mode *:not(#dev-badge):not(#dev-badge *) :hover {
                    outline: 2px solid #ffae00 !important;
                    outline-offset: 4px;
                    background-color: rgba(255, 174, 0, 0.05) !important;
                    cursor: text !important;
                }

                #dev-badge {
                    user-select: none !important;
                    -webkit-user-modify: read-only !important;
                }

                @keyframes screenShake {
                    0%, 100% { transform: translateX(0); }
                    10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
                    20%, 40%, 60%, 80% { transform: translateX(2px); }
                }

                @keyframes badgeEntrance {
                    from { opacity: 0; transform: translateX(-50%) translateY(-20px) scale(0.9); }
                    to { opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }
                }
            `;
            document.head.appendChild(style);
        }

        const badge = document.createElement('div');
        badge.id = 'dev-badge';
        badge.setAttribute('contenteditable', 'false');
        
        badge.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px; pointer-events: none;">
                <div style="width: 8px; height: 8px; background: #ffae00; border-radius: 50%; box-shadow: 0 0 8px #ffae00;"></div>
                <div style="display: flex; flex-direction: column; align-items: flex-start;">
                    <span style="font-size: 10px; color: rgba(255,255,255,0.5); letter-spacing: 1px; line-height: 1;">You can edit text</span>
                    <span style="font-size: 13px; color: #fff; font-weight: 700; margin-top: 4px;">DEVELOPER MODE</span>
                </div>
            </div>
            <div id="exit-btn" style="margin-left: 15px; padding: 4px 10px; background: rgba(255,68,68,0.1); border-radius: 4px; font-size: 10px; color: #ff4444; font-weight: bold; border: 1px solid rgba(255,68,68,0.3); transition: 0.2s;">EXIT</div>
        `;

        badge.style.cssText = `
            position: fixed; top: 30px; left: 50%; transform: translateX(-50%);
            display: flex; align-items: center;
            background: rgba(20, 20, 25, 0.85); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1); padding: 10px 22px; border-radius: 100px;
            z-index: 2147483647; font-family: 'Inter', sans-serif; cursor: default;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            animation: badgeEntrance 0.5s cubic-bezier(0.23, 1, 0.32, 1);
            transition: all 0.3s ease;
        `;

        const exitBtn = badge.querySelector('#exit-btn');
        exitBtn.style.cursor = 'pointer';
        exitBtn.onmouseover = () => { exitBtn.style.background = "rgba(255,68,68,0.2)"; };
        exitBtn.onmouseout = () => { exitBtn.style.background = "rgba(255,68,68,0.1)"; };

        exitBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            document.designMode = "off";
            document.body.spellcheck = true;
            document.body.classList.remove('developer-mode');
            isDeveloper = false;
            tapCount = 0;
            badge.style.opacity = "0";
            badge.style.transform = "translateX(-50%) translateY(-20px)";
            setTimeout(() => badge.remove(), 300);
            showToast("Developer mode disabled.");
        });

        document.body.appendChild(badge);
    }
});

let originalTitle = document.title;
window.addEventListener('blur', () => {
    document.title = "Don't leave me :(";
});
window.addEventListener('focus', () => {
    document.title = originalTitle;
});
