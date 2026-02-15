const isLoggedIn = document.body.getAttribute('data-logged-in') === 'true';
let currentConversationId = null;
let detectedLocation = null;
let currentLang = 'en';
let recognition; 
let isVoiceActive = false; 

let sidebarChartInstance = null;
let fullChartInstance = null;

const translations = {
    en: {
        loc_success: `✅ <b style="color:#0ea5e9">Location Secured!</b> Dr. Bob can find clinics near you.`,
        loc_fail: `⚠️ <b style="color:#ef4444">Location access denied.</b> I'll need to ask for your city.`,
        placeholder: "Describe symptoms...",
        history: "History",
        new_chat: "New Consultation",
        med_title: "Medical Profile",
        med_desc: "Dr. Bob will share this info with clinics when calling.",
        contacts_title: "Trusted Clinics",
        contacts_desc: "Dr. Bob will prioritize these saved clinics.",
        add_trusted: "Add to Trusted",
        menu_med: "Medical Profile",
        menu_clinics: "Trusted Clinics",
        logout: "Logout",
        login_link: "Login to save history",
        status: "Online",
        dir: "ltr",
        guest: "Guest Mode",
        bob_title: "Assistant Profile",
        bob_desc1: "Bob is a very friendly agent",
        bob_desc2: "He loves chocolates!",
        err_email: "Please enter a valid email address.",
        err_phone: "Format Error! Please use: +1XXXXXXXXXX (No spaces or dashes).",
        address_label: "Addresses",
        email_label: "Emails",
        phone_label: "Phone Numbers",
        cond_label: "Conditions & Allergies",
        ins_label: "Insurance Information",
        addr_placeholder: "Add address...",
        email_placeholder: "Add email...",
        phone_placeholder: "Add phone (+1XXXXXXXXXX)...",
        cond_placeholder: "Add condition...",
        ins_provider_placeholder: "Provider (e.g. SunLife)",
        ins_policy_placeholder: "Policy Number",
        clinic_name_placeholder: "Clinic Name",
        clinic_phone_placeholder: "Phone Number",
        sent_image: "📷 Sent an image",
        sidebar_stats: `<i class="fa-solid fa-chart-line"></i> Health Insights`,
        bob_summary_label: "Bob's Analysis",
        health_title: "Health Analytics",
        health_summary: "I've analyzed your history. You've reported <b>{condition}</b> symptoms <b>{count}</b> times.",
        health_healthy: "You haven't reported any specific symptoms yet. You're looking healthy!",
        symptoms: { 'Cold/Flu': 'Cold', 'Injury': 'Injury', 'Headache': 'Headache', 'Stomach': 'Stomach' },
        tips: {
            'Cold/Flu': "Wash your hands often and consider a flu shot.",
            'Injury': "Try stretching before exercise and wearing protective gear.",
            'Headache': "Stay hydrated and ensure you're getting enough sleep.",
            'Stomach': "Eat smaller meals and avoid trigger foods."
        },
        rename_prompt: "Rename consultation to:",
        delete_confirm: "Are you sure you want to delete this consultation?",
    },
    fr: {
        loc_success: `✅ <b style="color:#0ea5e9">Localisation confirmée!</b> Dr. Bob peut trouver des cliniques.`,
        loc_fail: `⚠️ <b style="color:#ef4444">Accès refusé.</b> Je devrai vous demander votre ville.`,
        placeholder: "Décrivez vos symptômes...",
        history: "Historique",
        new_chat: "Nouvelle Consultation",
        med_title: "Profil Médical",
        med_desc: "Ces infos seront partagées avec les cliniques.",
        contacts_title: "Cliniques de Confiance",
        contacts_desc: "Dr. Bob priorisera ces cliniques.",
        add_trusted: "Ajouter aux favoris",
        menu_med: "Profil Médical",
        menu_clinics: "Cliniques Favorites",
        logout: "Se déconnecter",
        login_link: "Connectez-vous pour sauvegarder",
        status: "En ligne",
        dir: "ltr",
        guest: "Mode Invité",
        bob_title: "Profil Assistant",
        bob_desc1: "Bob est un agent très amical",
        bob_desc2: "Il adore le chocolat !",
        err_email: "Veuillez entrer une adresse courriel valide.",
        err_phone: "Erreur de format ! Utilisez : +1XXXXXXXXXX (sans espaces ni tirets).",
        address_label: "Adresses",
        email_label: "E-mails",
        phone_label: "Téléphones",
        cond_label: "Maladies et Allergies",
        ins_label: "Informations d'assurance",
        addr_placeholder: "Ajouter une adresse...",
        email_placeholder: "Ajouter un e-mail...",
        phone_placeholder: "Ajouter (+1XXXXXXXXXX)...",
        cond_placeholder: "Ajouter une maladie...",
        ins_provider_placeholder: "Fournisseur (ex: SunLife)",
        ins_policy_placeholder: "Numéro de police",
        clinic_name_placeholder: "Nom de la clinique",
        clinic_phone_placeholder: "Numéro de téléphone",
        sent_image: "📷 Image envoyée",
        sidebar_stats: `<i class="fa-solid fa-chart-line"></i> Bilan Santé`,
        bob_summary_label: "L'analyse de Bob",
        health_title: "Analyse de Santé",
        health_summary: "J'ai analysé votre historique. Vous avez signalé <b>{condition}</b> <b>{count}</b> fois.",
        health_healthy: "Vous n'avez signalé aucun symptôme spécifique. Vous semblez en bonne santé !",
        symptoms: { 'Cold/Flu': 'Rhume', 'Injury': 'Blessure', 'Headache': 'Tête', 'Stomach': 'Estomac' },
        tips: {
            'Cold/Flu': "Lavez-vous souvent les mains et envisagez un vaccin antigrippal.",
            'Injury': "Étirez-vous avant l'effort et portez un équipement de protection.",
            'Headache': "Hydratez-vous bien et veillez à dormir suffisamment.",
            'Stomach': "Mangez de plus petits repas et évitez les aliments déclencheurs."
        },
        rename_prompt: "Renommer la consultation en :",
        delete_confirm: "Voulez-vous vraiment supprimer cette consultation ?",
    },
    ko: {
        loc_success: `✅ <b style="color:#0ea5e9">위치 확인 완료!</b> 밥 박사가 가까운 병원을 찾아드립니다.`,
        loc_fail: `⚠️ <b style="color:#ef4444">위치 권한 거부됨.</b> 도시 이름을 직접 입력해야 합니다.`,
        placeholder: "증상을 설명해 주세요...",
        history: "상담 기록",
        new_chat: "새 상담 시작",
        med_title: "의료 프로필",
        med_desc: "예약 전화 시 이 정보가 병원에 공유됩니다.",
        contacts_title: "신뢰하는 병원",
        contacts_desc: "이 병원들을 우선적으로 예약합니다.",
        add_trusted: "신뢰 목록에 추가",
        menu_med: "의료 프로필",
        menu_clinics: "신뢰하는 병원",
        logout: "로그아웃",
        login_link: "기록 저장을 위해 로그인",
        status: "온라인",
        dir: "ltr",
        guest: "게스트 모드",
        bob_title: "어시스턴트 프로필",
        bob_desc1: "밥은 매우 친절한 상담원입니다",
        bob_desc2: "그는 초콜릿을 정말 좋아해요!",
        err_email: "유효한 이메일 주소를 입력해 주세요.",
        err_phone: "형식 오류! +1XXXXXXXXXX 형식으로 입력해 주세요 (공백이나 하이픈 제외).",
        address_label: "주소",
        email_label: "이메일",
        phone_label: "전화번호",
        cond_label: "보유 질환 및 알레르기",
        ins_label: "보험 정보",
        addr_placeholder: "주소 추가...",
        email_placeholder: "이메일 추가...",
        phone_placeholder: "번호 추가 (+1XXXXXXXXXX)...",
        cond_placeholder: "질환 추가...",
        ins_provider_placeholder: "보험사 (예: 삼성생명)",
        ins_policy_placeholder: "증권 번호",
        clinic_name_placeholder: "병원 이름",
        clinic_phone_placeholder: "전화번호",
        sent_image: "📷 사진을 보냈습니다",
        sidebar_stats: `<i class="fa-solid fa-chart-line"></i> 건강 인사이트`,
        bob_summary_label: "밥의 분석 결과",
        health_title: "건강 분석",
        health_summary: "기록을 분석했습니다. <b>{condition}</b> 증상을 <b>{count}</b>번 언급하셨네요.",
        health_healthy: "아직 보고된 증상이 없습니다. 건강해 보이시네요!",
        symptoms: { 'Cold/Flu': '감기', 'Injury': '부상', 'Headache': '두통', 'Stomach': '위장' },
        tips: {
            'Cold/Flu': "손을 자주 씻고 독감 예방 주사 접종을 고려해 보세요.",
            'Injury': "운동 전 스트레칭을 하고 보호 장구를 착용해 보세요.",
            'Headache': "수분을 충분히 섭취하고 충분한 수면을 취하세요.",
            'Stomach': "식사량을 줄여서 자주 먹고 자극적인 음식을 피하세요."
        },
        rename_prompt: "상담 이름을 다음으로 변경:",
        delete_confirm: "이 상담을 삭제하시겠습니까?",
    },
    ar: {
        loc_success: `✅ <b style="color:#0ea5e9">تم تحديد الموقع!</b> يمكن للدكتور بوب العثور على عيادات قريبة.`,
        loc_fail: `⚠️ <b style="color:#ef4444">تم رفض الوصول للموقع.</b> سأحتاج لسؤالك عن مدينتك.`,
        placeholder: "صف الأعراض...",
        history: "السجل الطبي",
        new_chat: "استشارة جديدة",
        med_title: "الملف الطبي",
        med_desc: "سيتم مشاركة هذه المعلومات مع العيادات.",
        contacts_title: "العيادات الموثوقة",
        contacts_desc: "ستكون الأولوية لهذه العيادات عند الحجز.",
        add_trusted: "إضافة للموثوقة",
        menu_med: "الملف الطبي",
        menu_clinics: "العيادات الموثوقة",
        logout: "تسجيل خروج",
        login_link: "سجل الدخول لحفظ السجل",
        status: "متصل",
        dir: "rtl",
        guest: "وضع الضيف",
        bob_title: "ملف المساعد",
        bob_desc1: "بوب عميل ودود للغاية",
        bob_desc2: "إنه يحب الشوكولاتة!",
        err_email: "يرجى إدخال عنوان بريد إلكتروني صالح.",
        err_phone: "خطأ في التنسيق! يرجى استخدام: +1XXXXXXXXXX (بدون مسافات أو فواصل).",
        address_label: "العناوين",
        email_label: "البريد الإلكتروني",
        phone_label: "أرقام الهاتف",
        cond_label: "الأمراض والحساسية",
        ins_label: "معلومات التأمين",
        addr_placeholder: "أضف عنوانًا...",
        email_placeholder: "أضف بريدًا...",
        phone_placeholder: "أضف هاتفًا (+1XXXXXXXXXX)...",
        cond_placeholder: "أضف حالة...",
        ins_provider_placeholder: "شركة التأمين",
        ins_policy_placeholder: "رقم البوليصة",
        clinic_name_placeholder: "اسم العيادة",
        clinic_phone_placeholder: "رقم الهاتف",
        sent_image: "📷 تم إرسال صورة",
        sidebar_stats: `<i class="fa-solid fa-chart-line"></i> رؤى صحية`,
        bob_summary_label: "تحليل بوب",
        health_title: "تحليل الصحة",
        health_summary: "لقد قمت بتحليل سجلك. لقد أبلغت عن <b>{condition}</b> <b>{count}</b> مرات.",
        health_healthy: "لم تبلغ عن أي أعراض محددة بعد. تبدو بصحة جيدة!",
        symptoms: { 'Cold/Flu': 'برد', 'Injury': 'إصابة', 'Headache': 'صداع', 'Stomach': 'معدة' },
        tips: {
            'Cold/Flu': "اغسل يديك كثيرًا وفكر في أخذ لقاح الإنفلونزا.",
            'Injury': "جرب التمدد قبل التمرين وارتداء أدوات الوقاية.",
            'Headache': "حافظ على ترطيب جسمك وتأكد من الحصول على قسط كافٍ من النوم.",
            'Stomach': "تناول وجبات أصغر وتجنب الأطعمة التي تهيج المعدة."
        },
        rename_prompt: "إعادة تسمية الاستشارة إلى:",
        delete_confirm: "هل أنت متأكد أنك تريد حذف هذه الاستشارة؟",
    },
    zh: {
        loc_success: `✅ <b style="color:#0ea5e9">位置已确认！</b> Bob医生正在为您查找附近诊所。`,
        loc_fail: `⚠️ <b style="color:#ef4444">位置访问被拒绝.</b> 我需要询问您所在的城市。`,
        placeholder: "请描述您的症状...",
        history: "历史记录",
        new_chat: "开始新咨询",
        med_title: "医疗档案",
        med_desc: "拨打电话时将与诊所分享此信息。",
        contacts_title: "常用诊所",
        contacts_desc: "Bob医生将优先预约 these 诊所。",
        add_trusted: "添加到常用列表",
        menu_med: "医疗档案",
        menu_clinics: "常用诊所",
        logout: "登出",
        login_link: "登录以保存记录",
        status: "在线",
        dir: "ltr",
        guest: "访客模式",
        bob_title: "助手简介",
        bob_desc1: "Bob是一个非常友好的代理",
        bob_desc2: "他非常喜欢巧克力！",
        err_email: "请输入有效的电子邮件地址。",
        err_phone: "格式错误！请使用：+1XXXXXXXXXX（不含空格或连字符）。",
        address_label: "地址",
        email_label: "电子邮件",
        phone_label: "电话号码",
        cond_label: "疾病与过敏",
        ins_label: "保险信息",
        addr_placeholder: "添加地址...",
        email_placeholder: "添加电子邮件...",
        phone_placeholder: "添加电话 (+1XXXXXXXXXX)...",
        cond_placeholder: "添加病情...",
        ins_provider_placeholder: "保险公司",
        ins_policy_placeholder: "保单号",
        clinic_name_placeholder: "诊所名称",
        clinic_phone_placeholder: "电话号码",
        sent_image: "📷 已发送图片",
        sidebar_stats: `<i class="fa-solid fa-chart-line"></i> 健康洞察`,
        bob_summary_label: "Bob的分析",
        health_title: "健康分析",
        health_summary: "根据记录分析，您已报告 <b>{condition}</b> 症状 <b>{count}</b> 次。",
        health_healthy: "您尚未报告任何具体症状。您看起来很健康！",
        symptoms: { 'Cold/Flu': '感冒', 'Injury': '受伤', 'Headache': '头痛', 'Stomach': '胃痛' },
        tips: {
            'Cold/Flu': "经常洗手，并考虑接种流感疫苗。",
            'Injury': "运动前尝试拉伸并穿戴防护装备。",
            'Headache': "保持水分充足，并确保睡眠充足。",
            'Stomach': "少量多餐，避免食用诱发不适的食物。"
        },
        rename_prompt: "将咨询重命名为：",
        delete_confirm: "您确定要删除此咨询吗？",
    }
};

function safeUpdate(id, text, type = 'text') {
    const el = document.getElementById(id);
    if (!el) return;
    if (type === 'html') el.innerHTML = text;
    else if (type === 'placeholder') el.placeholder = text;
    else el.innerText = text;
}

function scrollToBottom() { 
    const m = document.getElementById('messages'); 
    if(m) m.scrollTop = m.scrollHeight; 
}

function formatText(text) { 
    return text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<b>$1</b>'); 
}

function toggleInputLock(isLocked) {
    const ids = ['userInput', 'sendBtn', 'micBtn', 'cameraBtn'];
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.disabled = isLocked;
    });
    const inputArea = document.querySelector('.input-area');
    if (inputArea) {
        inputArea.style.opacity = isLocked ? "0.6" : "1";
        inputArea.style.pointerEvents = isLocked ? "none" : "auto";
    }
}

function updateUILanguage() {
    const rawCode = document.getElementById('langSelector')?.value || 'en';
    currentLang = translations[rawCode] ? rawCode : 'en';
    localStorage.setItem('dr_bob_lang', currentLang);
    const t = translations[currentLang];
    document.documentElement.setAttribute('dir', t.dir);
    
    const messages = document.getElementById('messages');
    if (messages) messages.style.textAlign = (t.dir === 'rtl') ? 'right' : 'left';
    
    safeUpdate('userInput', t.placeholder, 'placeholder');
    safeUpdate('ui-history', t.history);
    safeUpdate('ui-new-chat', `<i class="fa-solid fa-plus"></i> ${t.new_chat}`, 'html');
    safeUpdate('ui-med-title', t.med_title);
    safeUpdate('ui-med-desc', t.med_desc);
    safeUpdate('ui-contacts-title', t.contacts_title);
    safeUpdate('ui-contacts-desc', t.contacts_desc);
    safeUpdate('ui-add-contact-btn', `<i class="fa-solid fa-plus"></i> ${t.add_trusted}`, 'html');
    safeUpdate('ui-status', t.status);
    safeUpdate('ui-guest-text', t.guest);
    safeUpdate('ui-bob-title', t.bob_title);
    safeUpdate('ui-bob-desc1', t.bob_desc1);
    safeUpdate('ui-bob-desc2', t.bob_desc2);
    safeUpdate('ui-menu-med', t.menu_med);
    safeUpdate('ui-menu-clinics', t.menu_clinics);
    safeUpdate('ui-logout', t.logout);
    safeUpdate('ui-login-link', t.login_link);
    safeUpdate('label-address', t.address_label);
    safeUpdate('label-email', t.email_label);
    safeUpdate('label-phone', t.phone_label);
    safeUpdate('label-condition', t.cond_label);
    safeUpdate('label-insurance', t.ins_label);
    safeUpdate('inputAddress', t.addr_placeholder, 'placeholder');
    safeUpdate('inputEmail', t.email_placeholder, 'placeholder');
    safeUpdate('inputPhone', t.phone_placeholder, 'placeholder');
    safeUpdate('conditionInput', t.cond_placeholder, 'placeholder');
    safeUpdate('inputInsuranceProvider', t.ins_provider_placeholder, 'placeholder');
    safeUpdate('inputInsurancePolicy', t.ins_policy_placeholder, 'placeholder');
    safeUpdate('contactName', t.clinic_name_placeholder, 'placeholder');
    safeUpdate('contactPhone', t.clinic_phone_placeholder, 'placeholder');
    safeUpdate('ui-health-insight-title', translations[currentLang].health_title);
    safeUpdate('ui-sidebar-stats', translations[currentLang].sidebar_stats, 'html');
    safeUpdate('ui-bob-summary-label', translations[currentLang].bob_summary_label);
}

function toggleLangMenu(e) { 
    e.stopPropagation(); 
    document.getElementById('langDropdown')?.classList.toggle('active'); 
}

function selectLang(code, label) { 
    safeUpdate('currentLangDisplay', label); 
    const input = document.getElementById('langSelector'); 
    if(input) input.value = code; 
    updateUILanguage(); 
    document.getElementById('langDropdown')?.classList.remove('active'); 
}

function toggleSidebar() { 
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
        if (sidebar.classList.contains('active') && isLoggedIn) {
            loadConversationList();
            loadHealthStats();
        }
    }
}

function toggleProfileMenu(e) { 
    e.stopPropagation(); 
    document.querySelector('.profile-dropdown')?.classList.toggle('active'); 
}


async function loadHealthStats() {
    const overlay = document.getElementById('sidebarAnalyzing');
    const canvas = document.getElementById('healthChart');
    const analysisBox = document.getElementById('bobAnalysisText');
    
    if (overlay) overlay.style.display = 'flex';
    if (canvas) canvas.style.opacity = '0.2';

    try {
        const res = await fetch('/dr-bob/get_health_stats');
        const rawData = await res.json();
        
        const t = translations[currentLang] || translations['en'];
        const translatedLabels = rawData.labels.map(label => t.symptoms[label] || label);

        let summaryHTML = "";

        if (rawData.counts && rawData.counts.length > 0 && Math.max(...rawData.counts) > 0) {
            const maxVal = Math.max(...rawData.counts);
            const maxIdx = rawData.counts.indexOf(maxVal);
            
            summaryHTML = `<span>${t.health_summary.replace('{condition}', translatedLabels[maxIdx]).replace('{count}', maxVal)}</span>`;

            if (rawData.prevention_type && t.tips && t.tips[rawData.prevention_type]) {
                summaryHTML += `
                    <br><br>
                    <span style="display: block; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px;">
                        <i class="fa-solid fa-lightbulb" style="color: #eab308; margin-right: 4px;"></i>
                        <b>Bob's Suggestion:</b> ${t.tips[rawData.prevention_type]}
                    </span>
                `;
            }
        } else {
            summaryHTML = `<span>${t.health_healthy}</span>`;
        }

        if (analysisBox) {
            analysisBox.innerHTML = summaryHTML;
            analysisBox.style.fontSize = "0.85rem"; 
            analysisBox.style.lineHeight = "1.4";
            analysisBox.style.color = "var(--text-main)";
            analysisBox.style.fontStyle = "normal";
        }

        const chartData = { labels: translatedLabels, counts: rawData.counts };
        renderSidebarChart(chartData);
        renderFullChart(chartData);

        if (overlay) overlay.style.display = 'none';
        if (canvas) canvas.style.opacity = '1';

    } catch (e) {
        console.error("Health stats fetch failed:", e);
        if (overlay) overlay.style.display = 'none';
        if (canvas) canvas.style.opacity = '1';
    }
}

function renderSidebarChart(data) {
    const ctx = document.getElementById('healthChart')?.getContext('2d');
    if (!ctx) return;
    
    if (sidebarChartInstance) sidebarChartInstance.destroy();

    const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent-primary').trim();
    const textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-main').trim();
    
    sidebarChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.counts,
                backgroundColor: accentColor,
                borderRadius: 2,
                barThickness: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { 
                legend: { display: false }, 
                tooltip: { enabled: false }
            },
            layout: {
                padding: { bottom: 0 }
            },
            scales: {
                y: { display: false, beginAtZero: true }, 
                x: { 
                    display: true, 
                    grid: { display: false, drawBorder: false },
                    ticks: {
                        color: textColor,
                        font: { 
                            size: 8, 
                            family: "'Inter', sans-serif"
                        },
                        autoSkip: false,
                        maxRotation: 0,
                        minRotation: 0
                    },
                    border: { display: false }
                } 
            },
            events: [] 
        }
    });
}

function renderFullChart(data) {
    const ctx = document.getElementById('fullHealthChart')?.getContext('2d');
    if (!ctx) return;
    if (fullChartInstance) fullChartInstance.destroy();

    const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent-primary').trim();
    const textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-main').trim();

    fullChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.counts,
                backgroundColor: accentColor,
                borderRadius: 8,
                barThickness: 25
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { 
                    beginAtZero: true, 
                    grid: { color: 'rgba(0,0,0,0.05)' }, 
                    ticks: { 
                        color: textColor, 
                        font: { size: 10 },
                        stepSize: 1 
                    } 
                },
                x: { 
                    grid: { display: false }, 
                    ticks: { color: textColor, font: { size: 10 } } 
                }
            }
        }
    });
}

async function addProfileInfo(type) {
    const inputMap = {
        'address': 'inputAddress',
        'email': 'inputEmail',
        'phone': 'inputPhone'
    };
    
    const input = document.getElementById(inputMap[type]);
    const value = input?.value.trim();
    
    if (!value) return;

    try {
        const res = await fetch('/dr-bob/add_contact', { 
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify({ type, value }) 
        });
        
        if (res.ok) {
            input.value = '';
            loadContacts();
        }
    } catch (e) {
        console.error(`Failed to save ${type}:`, e);
    }
}

async function saveInsurance() {
    const provider = document.getElementById('inputInsuranceProvider').value.trim();
    const policy = document.getElementById('inputInsurancePolicy').value.trim();
    
    if (!provider || !policy) return;

    const combinedValue = `${provider} (Policy: ${policy})`;

    await fetch('/dr-bob/add_contact', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify({ type: 'insurance', value: combinedValue }) 
    });

    document.getElementById('inputInsuranceProvider').value = '';
    document.getElementById('inputInsurancePolicy').value = '';
    loadContacts();
}

function openHealthDashboard() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.remove('active');
    
    const modal = document.getElementById('healthStatsModal');
    if (modal) {
        modal.style.display = 'flex';
        setTimeout(() => modal.classList.add('active'), 10);
        loadHealthStats();
    }
}

function closeHealthStats() {
    const modal = document.getElementById('healthStatsModal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => { modal.style.display = 'none'; }, 400);
    }
}

async function startNewChat() {
    try {
        const res = await fetch('/dr-bob/new_chat', { method: 'POST' });
        const data = await res.json();
        if (data.id) {
            currentConversationId = data.id;
            const messagesContainer = document.getElementById('messages');
            if (messagesContainer) messagesContainer.innerHTML = '';
            const sidebar = document.getElementById('sidebar');
            if (sidebar) sidebar.classList.remove('active');
            await loadConversationList();
            addBotMessage("New consultation started. How can I help you?");
        }
    } catch (e) { console.error(e); }
}

function sendPainMap() {
    const mapHtml = `
    <div class="pain-map-card">
        <div class="map-header">
            <i class="fa-solid fa-user-doctor"></i>
            <span>Tap the Pain Area</span>
        </div>
        
        <div class="human-body-wrapper">
            <svg viewBox="0 0 240 450" id="humanBody">
                
                <circle cx="120" cy="40" r="30" class="body-zone" onclick="selectPart('Head/Face')"/>
                
                <rect x="105" y="72" width="30" height="20" class="body-zone" onclick="selectPart('Neck/Throat')"/>

                <path d="M80,95 L160,95 L150,150 L90,150 Z" class="body-zone" onclick="selectPart('Chest')"/>

                <path d="M90,155 L150,155 L145,210 L95,210 Z" class="body-zone" onclick="selectPart('Stomach')"/>

                <path d="M95,215 L145,215 L155,245 L85,245 Z" class="body-zone" onclick="selectPart('Pelvis/Hips')"/>

                <circle cx="65" cy="105" r="20" class="body-zone" onclick="selectPart('Right Shoulder')"/>
                <circle cx="175" cy="105" r="20" class="body-zone" onclick="selectPart('Left Shoulder')"/>
                
                <rect x="45" y="130" width="30" height="60" rx="10" class="body-zone" onclick="selectPart('Right Arm')"/>
                <rect x="165" y="130" width="30" height="60" rx="10" class="body-zone" onclick="selectPart('Left Arm')"/>
                
                <rect x="40" y="200" width="30" height="70" rx="8" class="body-zone" onclick="selectPart('Right Forearm')"/>
                <rect x="170" y="200" width="30" height="70" rx="8" class="body-zone" onclick="selectPart('Left Forearm')"/>

                <circle cx="55" cy="285" r="15" class="body-zone" onclick="selectPart('Right Hand')"/>
                <circle cx="185" cy="285" r="15" class="body-zone" onclick="selectPart('Left Hand')"/>

                <path d="M90,250 L115,250 L115,340 L85,340 Z" class="body-zone" onclick="selectPart('Right Thigh')"/>
                <path d="M125,250 L150,250 L155,340 L125,340 Z" class="body-zone" onclick="selectPart('Left Thigh')"/>

                <circle cx="100" cy="355" r="14" class="body-joint" onclick="selectPart('Right Knee')"/>
                <circle cx="140" cy="355" r="14" class="body-joint" onclick="selectPart('Left Knee')"/>

                <rect x="88" y="375" width="24" height="75" rx="5" class="body-zone" onclick="selectPart('Right Shin')"/>
                <rect x="128" y="375" width="24" height="75" rx="5" class="body-zone" onclick="selectPart('Left Shin')"/>

            </svg>
        </div>
        <button class="text-link-btn" onclick="this.parentElement.remove()" style="color:var(--text-muted); margin-top:5px; background:none; border:none; text-decoration:underline; cursor:pointer;">Cancel</button>
    </div>`;
    
    addBotMessage(mapHtml);
}

function cancelMapAndAsk() {
    const map = document.querySelector('.pain-map-card');
    if (map) map.remove();

    const messagesContainer = document.getElementById('messages');
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        messagesContainer.appendChild(indicator); 
        indicator.style.display = 'flex'; 
        scrollToBottom();
    }

    fetch('/dr-bob/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            message: "[System Event]: The user closed the pain map. Ask them to describe or type which specific part of their body hurts." 
        })
    })
    .then(response => response.json())
    .then(data => {
        if (indicator) indicator.style.display = 'none';
        
        let botText = data.response.replace("[TRIGGER_PAIN_MAP]", "").trim();
        addBotMessage(formatText(botText));
    });
}

function cancelMapAndAsk() {
    const mapCard = document.querySelector('.pain-map-card');
    if (mapCard) {
        const parentMsg = mapCard.closest('.msg.bot');
        if (parentMsg) parentMsg.remove();
        else mapCard.remove();
    }

    const messagesContainer = document.getElementById('messages');
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        messagesContainer.appendChild(indicator); 
        indicator.style.display = 'flex'; 
        scrollToBottom();
    }

    fetch('/dr-bob/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            message: "[System Event]: User closed the pain map. Ask them which specific part of their body hurts so they can type it.",
            conversation_id: currentConversationId 
        })
    })
    .then(response => response.json())
    .then(data => {
        if (indicator) indicator.style.display = 'none';
        
        let cleanText = data.response.replace("[TRIGGER_PAIN_MAP]", "").trim();
        addBotMessage(formatText(cleanText));
    })
    .catch(err => {
        console.error("Cancel redirect failed:", err);
        if (indicator) indicator.style.display = 'none';
    });
}

function selectPart(partName) {
    const map = document.querySelector('.pain-map-card');
    if(map) {
        map.style.opacity = "0.5";
        map.style.pointerEvents = "none";
    }

    // 2. Show typing indicator
    const messagesContainer = document.getElementById('messages');
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        messagesContainer.appendChild(indicator); 
        indicator.style.display = 'flex'; 
        scrollToBottom();
    }

    // 3. Send to Gemini API
    fetch('dr-bob/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            // Hidden system message
            message: `[System Event]: The user clicked the ${partName} on the visual body map. Acknowledge this and ask a relevant follow-up question. Do NOT include the [TRIGGER_PAIN_MAP] tag in your response.` 
        })
    })
    .then(response => response.json())
    .then(data => {
        if (indicator) indicator.style.display = 'none';

        // --- THE FIX IS HERE ---
        let botText = data.response;
        
        // Remove the tag if it appears so the user never sees it
        if (botText.includes("[TRIGGER_PAIN_MAP]")) {
            botText = botText.replace("[TRIGGER_PAIN_MAP]", "").trim();
        }

        addBotMessage(formatText(botText));
    })
    .catch(err => {
        console.error(err);
        if (indicator) indicator.style.display = 'none';
    });
}

async function loadChat(id) { 
    currentConversationId = id; 
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.remove('active');

    try {
        const res = await fetch(`/get_messages/${id}`);
        const msgs = await res.json();
        const container = document.getElementById('messages');
        const indicator = document.getElementById('typingIndicator');

        if (container) {
            container.innerHTML = ''; 
            
            msgs.forEach(m => {
                if (m.role === 'bot') addBotMessage(formatText(m.content));
                else addUserMessage(m.content);
            });

            if (indicator) {
                container.appendChild(indicator);
                indicator.style.display = 'none'; 
            }
            
            scrollToBottom();
        }
    } catch (e) { console.error("Failed to load chat:", e); }
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const text = input.value.trim();
    
    if (!text && !selectedImageFile) return;

    toggleInputLock(true);

    if (selectedImageFile) {
        addUserMessage(translations[currentLang].sent_image || "📷 Sent an image");
        window.skipVoiceForNextMessage = true; 
    }
    
    if (text) {
        addUserMessage(text);
    }

    input.value = '';

    const messagesContainer = document.getElementById('messages');
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        messagesContainer.appendChild(indicator); 
        indicator.style.display = 'flex'; 
        scrollToBottom();
    }

    const formData = new FormData();
    formData.append('message', text || "📷 Sent an image");
    formData.append('coords', JSON.stringify(detectedLocation));
    formData.append('language', currentLang);
    if (currentConversationId) formData.append('conversation_id', currentConversationId);
    if (selectedImageFile) formData.append('image', selectedImageFile);

    clearImagePreview();

    try {
        const res = await fetch('/dr-bob/chat', { method: 'POST', body: formData });
        const data = await res.json();
        
        if (data.conversation_id) currentConversationId = data.conversation_id;
        if (indicator) indicator.style.display = 'none';
        
        toggleInputLock(false);

        // --- THE FIX STARTS HERE ---
        let botResponse = data.response;

        if (botResponse.includes("[TRIGGER_PAIN_MAP]")) {
            // 1. Remove the trigger tag so the user doesn't see it
            const cleanText = botResponse.replace("[TRIGGER_PAIN_MAP]", "").trim();
            
            // 2. Add the cleaned text message
            addBotMessage(formatText(cleanText));
            
            // 3. Launch the Pain Map!
            setTimeout(() => {
                sendPainMap();
            }, 600);
        } else {
            // Normal response behavior
            addBotMessage(formatText(botResponse));
        }
        // --- THE FIX ENDS HERE ---
        
        loadHealthStats(); 
        if (isLoggedIn) loadConversationList(); 

    } catch (e) { 
        if (indicator) indicator.style.display = 'none';
        addBotMessage("⚠️ Error connecting to server."); 
        toggleInputLock(false);
    }
}

let isElderlyMode = false;

function toggleElderlyMode() {
    isElderlyMode = !isElderlyMode;
    document.body.classList.toggle('elderly-mode', isElderlyMode);
    
    if (isElderlyMode) {
        startVoiceRecognition();
        addBotMessage("Elderly Mode is ON. I am listening to you constantly and texts are bigger.");
    } else {
        stopVoiceMode();
        addBotMessage("Elderly Mode is OFF.");
    }
}

function startVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    if (!recognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            isVoiceActive = true;
            document.getElementById('micBtn')?.classList.add('listening');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            if (transcript.trim()) {
                addUserMessage(transcript);
                sendMessage(transcript);
            }
        };

        recognition.onend = () => {
            document.getElementById('micBtn')?.classList.remove('listening');
            
            if (isElderlyMode && !window.speechSynthesis.speaking) {
                setTimeout(() => {
                    if (isElderlyMode) recognition.start();
                }, 500); 
            }
        };
    }
    
    try { recognition.start(); } catch(e) {}
}

function addBotMessage(html) {
    const container = document.getElementById('messages');
    const indicator = document.getElementById('typingIndicator');
    
    let finalHtml = html;
    let mapData = null;

    if (html.includes("MAP_DATA:")) {
        try {
            let rawData = html.split("MAP_DATA:")[1].split("|TEXT:")[0];
            rawData = rawData.replace(/```json|```/g, "").trim();
            const parsed = JSON.parse(rawData);
            mapData = Array.isArray(parsed) ? parsed : (parsed.clinics || null);
            finalHtml = html.replace(/MAP_DATA:[\s\S]*?(\|TEXT:|$)/, "").trim();
            console.log("📍 Map Data Parsed:", mapData);
        } catch (e) {
            console.error("❌ Map parsing failed:", e);
        }
    }

    const msgDiv = document.createElement('div');
    msgDiv.className = 'msg bot';
    msgDiv.innerHTML = finalHtml || "I found some locations for you:";

    if (indicator) {
        container.insertBefore(msgDiv, indicator);
        indicator.style.display = 'none'; 
    } else {
        container.appendChild(msgDiv);
    }

    if (mapData && mapData.length > 0 && mapData[0].lat) {
        const mapId = 'map-' + Date.now();
        const mapDiv = document.createElement('div');
        mapDiv.id = mapId;
        mapDiv.className = 'clinic-map-container'; 
        msgDiv.appendChild(mapDiv);

        setTimeout(() => {
            if (typeof L === 'undefined') {
                console.error("❌ Leaflet not loaded.");
                return;
            }

            const map = L.map(mapId, { zoomControl: false }).setView([mapData[0].lat, mapData[0].lon], 13);
            
            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO',
                subdomains: 'abcd',
                maxZoom: 20
            }).addTo(map);

            const medicalIcon = L.divIcon({
                html: '<i class="fa-solid fa-location-dot" style="color: #e74c3c; font-size: 24px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));"></i>',
                className: 'custom-medical-icon',
                iconSize: [24, 24],
                iconAnchor: [12, 24],
                popupAnchor: [0, -20]
            });

            mapData.forEach(clinic => {
                if (clinic.lat && clinic.lon) {
                    L.marker([clinic.lat, clinic.lon], { icon: medicalIcon })
                        .addTo(map)
                        .bindPopup(`<strong>${clinic.name}</strong><br>${clinic.dist || clinic.distance} km away`);
                }
            });

            scrollToBottom();
        }, 150);
    }

    scrollToBottom();

    const userInput = document.getElementById('userInput');
    if (userInput && !userInput.disabled) {
        userInput.focus();
    }

    if (isVoiceActive && !window.skipVoiceForNextMessage) {
        speakResponse(finalHtml);
    }
    window.skipVoiceForNextMessage = false;
}

function addUserMessage(text) {
    const container = document.getElementById('messages');
    if (!container) return;
    const msgDiv = document.createElement('div');
    msgDiv.className = 'msg user';
    msgDiv.textContent = text; 
    container.appendChild(msgDiv);
    scrollToBottom();
}

let selectedImageFile = null;

function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        selectedImageFile = file;
        document.getElementById('cameraBtn').classList.add('active-upload');
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('imagePreviewContainer').style.display = 'block';
            scrollToBottom();
        }
        reader.readAsDataURL(file);
    }
}

function clearImagePreview() {
    selectedImageFile = null;
    document.getElementById('imageInput').value = '';
    document.getElementById('imagePreviewContainer').style.display = 'none';
    document.getElementById('cameraBtn').classList.remove('active-upload');
}

function openThemeModal() {
    const modal = document.getElementById('themeModal');
    if (!modal) return;
    modal.style.display = 'flex';
    setTimeout(() => modal.classList.add('active'), 10);
}

function closeThemeModal() {
    const modal = document.getElementById('themeModal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => modal.style.display = 'none', 400);
    }
}

function setTheme(themeName) {
    document.documentElement.setAttribute('data-theme', themeName);
    localStorage.setItem('theme', themeName);
    const icon = document.getElementById('themeBtn')?.querySelector('i');
    if (icon) {
        const iconMap = { medical: 'fa-house', dark: 'fa-moon', comfort: 'fa-mug-hot', forest: 'fa-tree', lavender: 'fa-seedling', crimson: 'fa-heart-pulse', midnight: 'fa-user-ninja', sand: 'fa-wind', cyberpunk: 'fa-bolt' };
        icon.className = `fa-solid ${iconMap[themeName] || 'fa-palette'}`;
    }
    closeThemeModal();
}

function startVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;
    if (isVoiceActive) { stopVoiceMode(); return; }
    recognition = new SpeechRecognition();
    recognition.lang = currentLang === 'ko' ? 'ko-KR' : currentLang; 
    recognition.onstart = () => { isVoiceActive = true; document.getElementById('micBtn')?.classList.add('listening'); };
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById('userInput');
        if (input && transcript.trim()) { input.value = transcript; sendMessage(); }
    };
    recognition.onend = () => { document.getElementById('micBtn')?.classList.remove('listening'); if (isVoiceActive && !window.speechSynthesis.speaking) recognition.start(); };
    recognition.onerror = () => stopVoiceMode();
    recognition.start();
}

function stopVoiceMode() {
    isVoiceActive = false;
    window.speechSynthesis.cancel(); 
    if (recognition) { recognition.onend = null; recognition.stop(); }
    document.getElementById('micBtn')?.classList.remove('listening');
}

function speakResponse(html) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel(); 
    const cleanText = html.replace(/<[^>]*>?/gm, ''); 
    const utterance = new SpeechSynthesisUtterance(cleanText);
    const localeMap = { 'en': 'en-US', 'fr': 'fr-FR', 'ko': 'ko-KR', 'ar': 'ar-SA', 'zh': 'zh-CN' };
    utterance.lang = localeMap[currentLang] || 'en-US';
    utterance.rate = 1.08; 
    utterance.onend = () => { if (isVoiceActive) recognition.start(); };
    window.speechSynthesis.speak(utterance);
}

async function loadConditions() {
    const res = await fetch('/dr-bob/get_conditions');
    const data = await res.json();
    safeUpdate('conditionList', data.map(c => `<div class="condition-item"><span>${c.name}</span><button onclick="deleteCondition(${c.id})"><i class="fa-solid fa-trash"></i></button></div>`).join(''), 'html');
}

async function addCondition() {
    const input = document.getElementById('conditionInput');
    if(!input.value.trim()) return;
    await fetch('/dr-bob/add_condition', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ name: input.value.trim() }) });
    input.value = ''; loadConditions();
}

async function deleteCondition(id) { await fetch(`/delete_condition/${id}`, { method: 'DELETE' }); loadConditions(); }

async function loadContacts() {
    const res = await fetch('/dr-bob/get_contacts');
    const data = await res.json();
    const filterType = (type) => data.filter(c => c.type === type).map(c => `<div class="condition-item"><span>${c.value}</span><button onclick="deleteContact(${c.id})"><i class="fa-solid fa-trash"></i></button></div>`).join('');
    safeUpdate('listAddress', filterType('address'), 'html');
    safeUpdate('listEmail', filterType('email'), 'html');
    safeUpdate('listPhone', filterType('phone'), 'html');
    safeUpdate('listInsurance', filterType('insurance'), 'html');
}

async function addContact(type) {
    let inputId = (type === 'address') ? 'inputAddress' : (type === 'email') ? 'inputEmail' : 'inputPhone';
    const input = document.getElementById(inputId);
    const value = input.value.trim();
    if (!value) return;

    if (type === 'phone') {
        const phoneRegex = /^\+1\d{10}$/;
        if (!phoneRegex.test(value)) {
            alert(translations[currentLang].err_phone);
            return;
        }
    }

    if (type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            alert(translations[currentLang].err_email);
            return;
        }
    }

    try {
        const res = await fetch('/dr-bob/add_contact', { 
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify({ type: type, value: value }) 
        });
        if (res.ok) { 
            input.value = ''; 
            loadContacts(); 
        }
    } catch (e) { 
        console.error(e); 
    }
}

async function deleteContact(id) { await fetch(`/delete_contact/${id}`, { method: 'DELETE' }); loadContacts(); }

function openMedical() { 
    document.getElementById('sidebar')?.classList.remove('active'); 
    const modal = document.getElementById('medicalModal'); 
    modal.style.display = 'flex'; 
    setTimeout(() => modal.classList.add('active'), 10); 
    
    loadConditions(); 
    loadContacts(); 
}

function closeMedical() { const modal = document.getElementById('medicalModal'); modal.classList.remove('active'); setTimeout(() => { modal.style.display = 'none'; }, 400); }

async function loadSavedClinics() {
    const list = document.getElementById('contactList');
    if (!list) return;
    
    try {
        const res = await fetch('/dr-bob/get_saved_clinics');
        const clinics = await res.json();
        
        list.innerHTML = clinics.map(c => `
            <div class="condition-item">
                <span><strong>${c.name}</strong>: ${c.phone}</span>
                <button onclick="deleteSavedClinic(${c.id})" title="Remove">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        `).join('');
    } catch (e) { 
        console.error("Error loading clinics:", e); 
    }
}

async function deleteSavedClinic(id) {
    try {
        const res = await fetch(`/delete_saved_clinic/${id}`, { method: 'DELETE' });
        
        if (res.ok) {
            loadSavedClinics();
        } else {
            alert("Could not delete clinic.");
        }
    } catch (e) { 
        console.error(e); 
    }
}

async function saveClinic() {
    const nameInput = document.getElementById('contactName');
    const phoneInput = document.getElementById('contactPhone');
    
    const name = nameInput.value.trim();
    const phone = phoneInput.value.trim();
    
    if (!name || !phone) return;

    const phoneRegex = /^\+1\d{10}$/;
    if (!phoneRegex.test(phone)) {
        alert(translations[currentLang].err_phone);
        return;
    }

    try {
        const res = await fetch('/dr-bob/add_saved_clinic', { 
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify({ name, phone }) 
        });
        
        if (res.ok) {
            nameInput.value = ''; 
            phoneInput.value = ''; 
            loadSavedClinics();
        }
    } catch (e) {
        console.error("Failed to save clinic:", e);
    }
}

function openContacts() { document.getElementById('sidebar')?.classList.remove('active'); const modal = document.getElementById('contactsModal'); modal.style.display = 'flex'; setTimeout(() => modal.classList.add('active'), 10); loadSavedClinics(); }
function closeContacts() { const modal = document.getElementById('contactsModal'); modal.classList.remove('active'); setTimeout(() => { modal.style.display = 'none'; }, 400); }

window.onload = function() {
    const savedTheme = localStorage.getItem('theme') || 'medical';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    const savedLang = localStorage.getItem('dr_bob_lang') || 'en';
    const langInput = document.getElementById('langSelector');
    if(langInput) langInput.value = savedLang;

    const langNames = { 'en': 'EN', 'fr': 'FR', 'ko': 'KR', 'ar': 'AR', 'zh': 'CN' };
    const currentLabel = langNames[savedLang] || 'English';
    safeUpdate('currentLangDisplay', currentLabel);

    updateUILanguage();

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => { detectedLocation = { lat: pos.coords.latitude, lon: pos.coords.longitude }; toggleInputLock(false); }, 
            () => { addBotMessage(translations[currentLang].loc_fail); toggleInputLock(false); }
        );
    }

    if (isLoggedIn) { 
        loadConversationList(); 
        loadConditions(); 
        loadContacts(); 
        loadSavedClinics(); 
        loadHealthStats(); 
    }

    document.getElementById('userInput')?.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendMessage(); });

    setupPhoneAutoFormat('inputPhone');
    setupPhoneAutoFormat('contactPhone');

    document.addEventListener('click', (e) => {
        const modals = { themeModal: closeThemeModal, medicalModal: closeMedical, contactsModal: closeContacts, healthStatsModal: closeHealthStats };
        for (const [id, closeFunc] of Object.entries(modals)) {
            if (e.target === document.getElementById(id)) closeFunc();
        }
        
        const sidebar = document.getElementById('sidebar');
        if (sidebar?.classList.contains('active') && !sidebar.contains(e.target) && !e.target.closest('.menu-btn')) sidebar.classList.remove('active');
    });
};

function setupPhoneAutoFormat(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;

    el.addEventListener('focus', (e) => {
        if (!e.target.value) {
            e.target.value = '+1';
        }
    });

    el.addEventListener('blur', (e) => {
        if (e.target.value === '+1') {
            e.target.value = '';
        }
    });

    el.addEventListener('input', (e) => {
        if (!e.target.value.startsWith('+1')) {
            e.target.value = '+1' + e.target.value.replace(/[^\d]/g, '').slice(1);
        }
        if (e.target.value.length > 12) {
            e.target.value = e.target.value.slice(0, 12);
        }
    });
}

async function loadConversationList() {
    const list = document.getElementById('conversationList');
    if (!list) return;
    try {
        const res = await fetch('/dr-bob/get_conversations');
        const chats = await res.json();
        list.innerHTML = chats.map((c, i) => `
            <div class="chat-item" style="--i: ${i}">
                <div class="chat-info" onclick="loadChat(${c.id})">
                    <span class="chat-title">${c.title}</span>
                    <span class="chat-date">${c.date}</span>
                </div>
                <div class="chat-actions">
                    <button onclick="event.stopPropagation(); renameChat(${c.id}, '${c.title.replace(/'/g, "\\'")}')">
                        <i class="fa-solid fa-pen"></i>
                    </button>
                    <button onclick="event.stopPropagation(); deleteChat(event, ${c.id})">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </div>
            </div>`).join('');
    } catch (e) { console.error(e); }
}

async function renameChat(id, oldTitle) {
    const newTitle = prompt(translations[currentLang].rename_prompt, oldTitle);
    
    if (!newTitle || newTitle.trim() === "" || newTitle === oldTitle) return;

    try {
        const res = await fetch(`/rename_conversation/${id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: newTitle.trim() })
        });

        if (res.ok) loadConversationList();
    } catch (e) { console.error("Rename failed:", e); }
}

async function deleteChat(event, id) { 
    event.stopPropagation(); 
    if(!confirm(translations[currentLang].delete_confirm)) return; 
    
    await fetch(`/delete_conversation/${id}`, { method: 'DELETE' }); 
    loadConversationList(); 
}