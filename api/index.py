import sys
from pathlib import Path
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# For the main page stats only
PORTFOLIO_STATS = {
    'competitions': 20,
    'hackathons': 11,
    'prize': 4000,
    'projects': 9
}

LANGUAGES = ['en', 'ko', 'fr']

TRANSLATIONS = {

    'en': {
        'terminal': 'Terminal',
        'resume': 'Resume',
        'nav_home': 'Home',
        'nav_achievements': 'Achievements',
        'nav_projects': 'Projects',
        'nav_about_me': 'About Me',
        'navigation': 'Navigation',
        'back': 'Back',
        'showing_results': 'Showing {n} of {total} milestones',
        'showing_projects': 'Showing {n} of {total} projects',
        'lang_beta_tooltip': 'Translation feature is in BETA — descriptions are still being translated.',

        'name': 'Jongmin Lee',
        'about': 'Incoming McGill Computer Science',
        'btn_achievements': 'Achievements',
        'btn_view_my_work': 'View My Work',

        'stat_competition_wins': 'Competition Awards',
        'stat_hackathon_wins': 'Hackathon Awards',
        'stat_prize': 'Hackathon Prizes',
        'stat_projects': 'Projects',

        'section_highlights': 'Highlights',
        'section_about_me': 'About Me',
        'section_education': 'Education',
        'section_experience': 'Experience',

        'scale_global': 'GLOBAL SCALE',
        'scale_national': 'NATIONAL SCALE',
        'scale_regional': 'REGIONAL SCALE',
        'more_awards': 'MORE AWARDS',

        'hl_cayley_subtitle': 'School Champion · Top 25% Worldwide',
        'contest_HME': 'HME Math Contest',
        'hl_hme_subtitle': 'National 1st Place · Top 0.1% in Korea',
        'hl_conuhacks_subtitle': '2nd Place | Dialogue Track',
        'hl_hack_subtitle': '3rd Place | Beginner Track',
        'hl_jachacks_subtitle': '1st Place',
        'hl_aerohacks_subtitle': '1st Place',

        'edu_expected': 'EXPECTED',
        'edu_enrolled': 'ENROLLED',
        'edu_graduated': 'GRADUATED',
        'edu_mcgill_university': 'McGill University',
        'edu_mcgill_degree': 'Computer Science | Bachelor of Science',
        'edu_mcgill_years': '2026 (Est.) - 2029 (Est.)',
        'edu_dawson_college': 'Dawson College',
        'edu_dawson_degree': 'Science, Computer Science & Mathematics',
        'edu_rosemount_degree': 'Secondary School Diploma',
        'edu_deans_list': "Dean's List",
        'edu_recognition': 'Recognition of Student Involvement',
        'edu_space': 'SPACE Certificate',
        'edu_leadership': 'Campus Life Leadership Award',
        'edu_rosemount_high_school': 'Rosemount High School',
        'edu_high_honor_roll': 'High Honor Roll',
        'edu_honor_roll': 'Honor Roll',
        'edu_art_etudes': 'Art-Études Program',

        'portfolio_insights' : 'Portfolio Insights',
        'key_projects': 'Key Projects',
        'award_distribution': 'Awards Distribution',
        'hackathon_progress': 'Hackathon Progress',
        'graph': 'Cumulative awards vs hackathons attended',

        'about_html': (
            'My name is <strong>Jongmin Lee</strong>. I am a 19-year-old Korean student living in Montreal, Canada. '
            'Having recently graduated from Dawson College in Computer Science, I am continuing my studies in Computer Science at McGill University (U1). '
            'I am proud to be <strong>trilingual</strong>, speaking Korean, English, and French. '
            'I am a <strong class="pop-up"> 9x hackathon winner'
            '<span class="pop-up-text">'
            '<strong style="color: #0d6efd;">Hackathon Podium Finishes:</strong><br>'
            'JACHacks (1st · Special Award)<br>'
            'McGill AeroHacks (1st)<br>'
            'Brim Track at MPC Hacks (2nd · Special Award)<br>'
            'Dialogue Track at ConUHacks (2nd)<br>'
            'Dawson Robotics Hackathon 2025 (2nd)<br>'
            'Dawson Robotics Hackathon 2026 (3rd)<br>'
            'Beginner Track at @HACK (3rd)<br>'
            'HackDécouverte (Special Award)<br>'
            'Dialogue Internal (Special Award)<br>'
            '</span></strong> with over '
            '<strong class="pop-up">15 STEM competition awards'
            '<span class="pop-up-text">'
            '<strong style="color: #0d6efd;">STEM Competition Awards:</strong><br>'
            "HME Math Contest '14 (National 1st)<br>"
            'Waterloo Cayley Math Contest (School Champion)<br>'
            'JACHacks (1st · Special Award)<br>'
            'McGill AeroHacks (1st)<br>'
            'Brim Track MPC Hacks (2nd · Special Award)<br>'
            'Dialogue Track at ConUHacks (2nd)<br>'
            'Dawson Robotics Hackathon 2025 (2nd)<br>'
            'Dawson Robotics Hackathon 2026 (3rd)<br>'
            'Beginner Track at @HACK (3rd)<br>'
            'HackDécouverte (Special Award)<br>'
            'Dialogue Internal (Special Award)<br>'
            'The Ultimate Math League (Special Award)<br>'
            "HME Math Contest '16 (Special Award)<br>"
            '</span></strong> in total. '
            'I have experience coding in <strong>Python, JavaScript, C++, C#, and C</strong>.'
        ),

        'snow_hint': 'Type "snow"',

        'projects_title': 'Projects',
        'subtitle_journey': "Jongmin's journey from South Korea to Canada",
        'filter_show_all': 'Show All',
        'filter_gold': 'Gold',
        'filter_team': 'Team',
        'filter_hackathon': 'Hackathon',
        'filter_school': 'School',
        'filter_personal': 'Personal',
        'no_projects_match': 'No projects match these filters.',
        'reset_filters': 'Reset Filters',
        'teammate': 'Teammate',
        'teammates': 'Teammates',
        'read_full_story': 'Read the full story',

        'the_journey': 'The Journey',
        'originally_published': 'Originally published',
        'updated_label': 'Updated:',
        'published_label': 'Published',
        'project_gallery': 'Project Gallery',
        'live_demo': 'Live Demonstration',
        'full_tech_stack': 'Full Tech Stack',
        'engineering_challenges': 'Engineering Challenges',
        'link_singular': 'Link',
        'link_plural': 'Links',
        'launch_live_app': 'Launch Live App',

        'achievements_title': 'Academic & Competitive Milestones',
        'next_competition': 'MY NEXT COMPETITION',
        'filter_canada': 'Canada',
        'filter_experience': 'Experience',
        'filter_stem': 'STEM',
        'filter_arts': 'Arts',
        'filter_software': 'Software',
        'filter_hardware': 'Hardware',
        'filter_math': 'Math',
        'filter_health': 'Health',
        'filter_academic': 'Academic',
        'no_milestones_match': 'No milestones match these filters.',
        'try_different_combination': 'Try selecting a different combination of tags.',
        'section_competitions': 'Competitions',
        'section_certificates': 'Certificates & Awards',
        'view_courses': 'View Courses',
        'non_elective_courses': 'Non-elective courses',
        'semesters': 'Semesters',
        'courses_label': 'Courses'
    },

    'ko': {
        'terminal': '터미널',
        'resume': '이력서',
        'nav_home': '홈',
        'nav_achievements': '수상',
        'nav_projects': '프로젝트',
        'nav_about_me': '소개',
        'navigation': '메뉴',
        'back': '뒤로',
        'showing_results': '전체 {total}개 중 {n}개 표시',
        'showing_projects': '전체 {total}개 프로젝트 중 {n}개 표시',
        'lang_beta_tooltip': '번역 기능은 베타 단계입니다 — 일부 설명만 번역되어 있습니다.',

        'name': '이종민',
        'about': '맥길 대학교 컴퓨터공학 예비 신입생',
        'btn_achievements': '수상 보기',
        'btn_view_my_work': '프로젝트 보기',

        'stat_competition_wins': '대회 수상',
        'stat_hackathon_wins': '해커톤 수상',
        'stat_prize': '해커톤 상금',
        'stat_projects': '프로젝트',

        'section_highlights': '주요 성과',
        'section_about_me': '소개',
        'section_education': '학력',
        'section_experience': '경력',

        'scale_global': '국제 규모',
        'scale_national': '전국 규모',
        'scale_regional': '지역 규모',
        'more_awards': '수상 기록 보기',

        'hl_cayley_subtitle': '전교 1위 · 전 세계 상위 25%',
        'contest_HME': 'HME 수학경시대회',
        'hl_hme_subtitle': '전국 1위 · 한국 상위 0.1%',
        'hl_conuhacks_subtitle': '2위 | Dialogue 부문',
        'hl_hack_subtitle': '3위 | 초보 부문',
        'hl_jachacks_subtitle': '1위',
        'hl_aerohacks_subtitle': '1위',

        'edu_expected': '예정',
        'edu_enrolled': '재학 중',
        'edu_graduated': '졸업',
        'edu_mcgill_university': '맥길 대학교',
        'edu_mcgill_degree': '컴퓨터 과학 | 학사',
        'edu_mcgill_years': '2026 (예정) - 2029 (예정)',
        'edu_dawson_college': 'Dawson College',
        'edu_dawson_degree': '과학, 컴퓨터 과학 및 수학',
        'edu_rosemount_degree': '고등학교 졸업장',
        'edu_deans_list': '학장 명단',
        'edu_recognition': '교내 활동 인증',
        'edu_space': 'SPACE 수료증',
        'edu_leadership': '리더쉽 상',
        'edu_rosemount_high_school': 'Rosemount 고등학교',
        'edu_high_honor_roll': '최우수 명예 학생',
        'edu_honor_roll': '명예 학생',
        'edu_art_etudes': '예술 및 스터디 프로그램',

        'portfolio_insights' : '포트폴리오 인사이트',
        'key_projects': '주요 프로젝트',
        'award_distribution': '수상 분포',
        'hackathon_progress': '해커톤 성과 추이',
        'graph': '해커톤 참가 횟수 대비 누적 수상 실적',
        'chart_grade' : '학업',
        'chart_webdev': '웹 개발',
        'chart_math': '수학',
        'chart_robotics': '로봇공학',
        'chart_other': '기타',
        'chart_attended': '참가한 해커톤',
        'chart_awards': '해커톤 수상',
        'chart_sequence': '해커톤 참가 회차',
        'chart_cumulative': '누적 횟수',
        'filter_all' : '전체',
        'general': '일반',
        'chart_art': '미술',
        'chart_music': '음악',
        'chart_leadership': '리더쉽',
        'dialogue_hackathon': 'Dialogue 사내 해커톤',

        'about_html': (
            '안녕하세요, 캐나다 몬트리올 Dawson College에서 컴퓨터 과학을 졸업후, McGill University에서 컴퓨터 과학을 공부할 예정인 <strong>이종민</strong>입니다. '
            '저는 한국어, 영어, 프랑스어를 모두 구사하는 <strong>3개 국어 사용자</strong>입니다. '
            '저는 <strong class="pop-up">해커톤 9회 우승자'
            '<span class="pop-up-text">'
            '<strong style="color: #0d6efd;">해커톤 입상 기록:</strong><br>'
            'JACHacks (1위 · 특별상)<br>'
            'McGill AeroHacks (1위)<br>'
            'Brim 부문 MPC Hacks (2위 · 특별상)<br>'
            'Dialogue 부문 ConUHacks (2위)<br>'
            'Dawson Robotics Hackathon 2025 (2위)<br>'
            'Dawson Robotics Hackathon 2026 (3위)<br>'
            '초보 부문 @HACK (3위)<br>'
            'HackDécouverte (특별상)<br>'
            'Dialogue Internal (특별상)<br>'
            '</span></strong>이며, '
            '<strong class="pop-up">STEM 관련 대회를 15회 이상 수상'
            '<span class="pop-up-text">'
            '<strong style="color: #0d6efd;">STEM 대회 수상:</strong><br>'
            "HME 수학 경시대회 '14 (전국 1위)<br>"
            'Waterloo Cayley Math Contest (학교 챔피언)<br>'
            'JACHacks (1위 · 특별상)<br>'
            'McGill AeroHacks (1위)<br>'
            'Brim 부문 MPC Hacks (2위 · 특별상)<br>'
            'Dialogue Track at ConUHacks (2위)<br>'
            'Dawson Robotics Hackathon 2025 (2위)<br>'
            'Dawson Robotics Hackathon 2026 (3위)<br>'
            'Beginner Track at @HACK (3위)<br>'
            'HackDécouverte (특별상)<br>'
            'Dialogue Internal (특별상)<br>'
            'The Ultimate Math League (특별상)<br>'
            "HME 수학 경시대회 '16 (특별상)<br>"
            '</span></strong>한 경력이 있습니다. '
            '또한 <strong>Python, JavaScript, C++, C#, C</strong> 코딩 경험이 있습니다.'
        ),

        'snow_hint': '"snow" 입력',

        'vault': '트로피 진열장',
        'vault_subtitle': '대회 우승',

        'projects_title': '프로젝트',
        'subtitle_journey': '한국에서 캐나다까지 종민의 여정',
        'filter_show_all': '전체 보기',
        'filter_gold': '골드',
        'filter_team': '팀 프로젝트',
        'filter_hackathon': '해커톤',
        'filter_school': '학교',
        'filter_personal': '개인',
        'no_projects_match': '조건에 맞는 프로젝트가 없습니다.',
        'reset_filters': '필터 초기화',
        'teammate': '팀원',
        'teammates': '팀원',
        'read_full_story': '자세히 보기',

        'the_journey': '여정',
        'originally_published': '최초 게시',
        'updated_label': '마지막 업데이트:',
        'published_label': '게시',
        'project_gallery': '프로젝트 갤러리',
        'live_demo': '라이브 시연',
        'full_tech_stack': '전체 기술 스택',
        'engineering_challenges': '엔지니어링 난제',
        'link_singular': '링크',
        'link_plural': '링크',
        'launch_live_app': '라이브 앱 실행',

        'achievements_title': '학업 및 대회 성과',
        'next_competition': '다가오는 대회',
        'filter_canada': '캐나다',
        'filter_experience': '경력',
        'filter_stem': 'STEM',
        'filter_arts': '예술',
        'filter_software': '소프트웨어',
        'filter_hardware': '하드웨어',
        'filter_math': '수학',
        'filter_health': '의학',
        'filter_academic': '학업',
        'no_milestones_match': '조건에 맞는 성과가 없습니다.',
        'try_different_combination': '다른 태그 조합을 선택해 보세요.',
        'section_competitions': '대회',
        'section_certificates': '자격증 및 수료증',
        'view_courses': '과목 보기',
        'non_elective_courses': '필수 과목',
        'semesters': '학기',
        'courses_label': '과목'
    },

    'fr': {
        'terminal': 'Terminal',
        'resume': 'CV',
        'nav_home': 'Accueil',
        'nav_achievements': 'Réalisations',
        'nav_projects': 'Projets',
        'nav_about_me': 'À propos',
        'navigation': 'Navigation',
        'back': 'Retour',
        'showing_results': 'Affichage de {n} sur {total} réalisations',
        'showing_projects': 'Affichage de {n} sur {total} projets',

        'name': 'Jongmin Lee',
        'about': "Futur étudiant en informatique à McGill",
        'btn_achievements': 'Réalisations',
        'btn_view_my_work': 'Voir mes projets',

        'stat_competition_wins': 'Compétitions remportées',
        'stat_hackathon_wins': 'Hackathons remportés',
        'stat_prize': 'Prix de hackathon',
        'stat_projects': 'Projets',

        'section_highlights': 'Faits saillants',
        'section_about_me': 'À propos',
        'section_education': 'Formation',
        'section_experience': 'Expérience',

        'scale_global': 'ÉCHELLE MONDIALE',
        'scale_national': 'ÉCHELLE NATIONALE',
        'scale_regional': 'ÉCHELLE RÉGIONALE',
        'more_awards': 'PLUS DE PRIX',

        'hl_cayley_subtitle': "Champion de l'école · Top 25 % mondial",
        'contest_HME': 'HME Math Contest',
        'hl_hme_subtitle': '1ʳᵉ Place Nationale · Top 0.1 % en Corée',
        'hl_conuhacks_subtitle': '2ᵉ Place | Piste Dialogue',
        'hl_hack_subtitle': '3ᵉ place | Piste débutant',
        'hl_jachacks_subtitle': '1ʳᵉ Place',
        'hl_aerohacks_subtitle': '1ʳᵉ Place',

        'edu_expected': 'PRÉVU',
        'edu_enrolled': 'INSCRIT',
        'edu_graduated': 'DIPLÔMÉ',
        'edu_mcgill_university': 'Université McGill',
        'edu_mcgill_degree': 'Informatique | Baccalauréat ès sciences',
        'edu_mcgill_years': '2026 (Prévu) - 2029 (Prévu)',
        'edu_dawson_college': 'Collège Dawson',
        'edu_dawson_degree': 'Sciences, informatique et mathématiques',
        'edu_rosemount_degree': "Diplôme d'études secondaires",
        'edu_deans_list': "Liste d'honneur du doyen",
        'edu_recognition': "Reconnaissance de l'engagement étudiant",
        'edu_space': 'Certificat SPACE', 
        'edu_leadership': 'Prix de leadership',
        'edu_rosemount_high_school': 'École secondaire Rosemount',
        'edu_high_honor_roll': "Tableau d'honneur supérieur",
        'edu_honor_roll': "Tableau d'honneur",
        'edu_art_etudes': 'Programme Arts-Études',

        'portfolio_insights' : 'Aperçu du portfolio',
        'key_projects': 'Projets Clés',
        'award_distribution': 'Répartition des prix',
        'hackathon_progress': 'Progression aux hackathons',
        'graph': 'Récompenses cumulées vs participations aux hackathons',
        'chart_grade' : 'Scolaire',
        'chart_webdev': 'Dev Web',
        'chart_robotics': 'Robotique',
        'chart_other': 'Autre',
        'chart_total': 'TOTAL',
        'chart_attended': 'Hackathons participés',
        'chart_awards': 'Prix remportés',
        'chart_sequence': 'Séquence de hackathon',
        'chart_cumulative': 'Compte cumulé',
        'filter_all': 'Tous',
        'general': 'Général',
        'chart_music': 'Musique',
        'dialogue_hackathon': 'Hackathon interne de Dialogue',

        'about_html': (
            "Je m'appelle <strong>Jongmin Lee</strong>. Je suis un étudiant coréen de 19 ans vivant à Montréal, au Canada. "
            "Récemment diplômé en informatique du Collège Dawson, je poursuis mes études en informatique à l'Université McGill (U1). "
            "Je suis fier d'être <strong>trilingue</strong>, parlant le coréen, l'anglais et le français. "
            'Je suis <strong class="pop-up">9x gagnant de hackathons'
            '<span class="pop-up-text">'
            '<strong style="color: #0d6efd;">Podiums de hackathons :</strong><br>'
            'JACHacks (1ʳᵉ · Prix Spécial)<br>'
            'McGill AeroHacks (1ʳᵉ)<br>'
            'Brim Track à MPC Hacks (2ᵉ · Prix Spécial)<br>'
            'Dialogue Track à ConUHacks (2ᵉ)<br>'
            'Dawson Robotics Hackathon 2025 (2ᵉ)<br>'
            'Dawson Robotics Hackathon 2026 (3ᵉ)<br>'
            'Beginner Track à @HACK (3ᵉ)<br>'
            'HackDécouverte (Prix spécial)<br>'
            'Dialogue Internal (Prix Spécial)<br>'
            '</span></strong> avec plus de '
            '<strong class="pop-up">15 prix en STIM'
            '<span class="pop-up-text">'
            '<strong style="color: #0d6efd;">Prix en STIM :</strong><br>'
            "HME Math Contest '14 (1ʳᵉ nationale)<br>"
            "Waterloo Cayley Math Contest (Champion de l'école)<br>"
            'JACHacks (1ʳᵉ · Prix spécial)<br>'
            'McGill AeroHacks (1ʳᵉ)<br>'
            'Brim Track à MPC Hacks (2ᵉ · Prix Spécial)<br>'
            'Dialogue Track à ConUHacks (2ᵉ)<br>'
            'Dawson Robotics Hackathon 2025 (2ᵉ)<br>'
            'Dawson Robotics Hackathon 2026 (3ᵉ)<br>'
            'Beginner Track à @HACK (3ᵉ)<br>'
            'HackDécouverte (Prix Spécial)<br>'
            'Dialogue Internal (Prix Spécial)<br>'
            'The Ultimate Math League (Prix Spécial)<br>'
            "HME Math Contest '16 (Prix Spécial)<br>"
            '</span></strong> au total. '
            "J'ai de l'expérience en programmation en <strong>Python, JavaScript, C++, C# et C</strong>."
        ),

        'snow_hint': 'Tapez « snow »',
        'vault': 'La chambre des trophées',
        'vault_subtitle': 'Victoires en compétition',

        'projects_title': 'Projets',
        'subtitle_journey': 'Le parcours de Jongmin, de la Corée du Sud au Canada',
        'filter_show_all': 'Tout afficher',
        'filter_gold': 'Or',
        'filter_team': 'Équipe',
        'filter_hackathon': 'Hackathon',
        'filter_school': 'École',
        'filter_personal': 'Personnel',
        'no_projects_match': 'Aucun projet ne correspond à ces filtres.',
        'reset_filters': 'Réinitialiser les filtres',
        'teammate': 'Coéquipier',
        'teammates': 'Coéquipiers',
        'read_full_story': 'Lire le récit complet',

        'the_journey': 'Le parcours',
        'originally_published': "Publié à l'origine",
        'updated_label': 'Mis à jour :',
        'published_label': 'Publié',
        'project_gallery': 'Galerie du projet',
        'live_demo': 'Démonstration en direct',
        'full_tech_stack': 'Pile technologique complète',
        'engineering_challenges': 'Défis techniques',
        'link_singular': 'Lien',
        'link_plural': 'Liens',
        'launch_live_app': "Lancer l'application en direct",

        'achievements_title': 'Jalons Académiques et Compétitifs',
        'next_competition': 'PROCHAINE COMPÉTITION',
        'filter_canada': 'Canada',
        'filter_experience': 'Expérience',
        'filter_stem': 'STIM',
        'filter_arts': 'Arts',
        'filter_software': 'Logiciel',
        'filter_hardware': 'Matériel',
        'filter_math': 'Mathématiques',
        'filter_health': 'Santé',
        'filter_academic': 'Scolaire',
        'no_milestones_match': 'Aucun jalon ne correspond à ces filtres.',
        'try_different_combination': "Essayez une autre combinaison d'étiquettes.",
        'section_competitions': 'Compétitions',
        'section_certificates': 'Certificats et prix',
        'view_courses': 'Voir les cours',
        'non_elective_courses': 'Cours non optionnels',
        'semesters': 'Semestres',
        'courses_label': 'Cours',
    },
}

def current_lang():
    lang = request.cookies.get('lang', 'en')
    return lang if lang in LANGUAGES else 'en'

def current_theme():
    theme = request.cookies.get('theme', 'light')
    return theme if theme in ('light', 'dark') else 'light'

def tr(value):
    if isinstance(value, dict):
        lang = current_lang()
        return value.get(lang) or value.get('en') or ''
    return value

@app.context_processor
def inject_lang():
    lang = current_lang()
    return {
        't': TRANSLATIONS[lang],
        'lang': lang,
        'LANGUAGES': LANGUAGES,
        'theme': current_theme(),
        'stats': PORTFOLIO_STATS,
        'experiences': get_processed_experiences()
    }

app.jinja_env.filters['tr'] = tr

@app.route('/set-language/<lang>')
def set_language(lang):
    if lang not in LANGUAGES:
        lang = 'en'

    target = request.args.get('next') or request.referrer or '/'
    if not target.startswith('/'):
        target = '/'

    response = make_response(redirect(target))
    response.set_cookie(
        'lang', lang,
        max_age=60 * 60 * 24 * 365,
        path='/',
        samesite='Lax',
        httponly=False,
    )
    return response

EXPERIENCES = [
    {
        'company': {'en': 'GIO Engineering', 'ko': '지오 엔지니어링', 'fr': 'GIO Engineering'},
        'roles': [
            {
                'title': {'en': 'Engineering Intern', 'ko': '엔지니어링 인턴', 'fr': 'Stagiaire en ingénierie'},
                'start_date': (2025, 6),
                'end_date': (2025, 8),
                'description': {
                    'en': 'I developed CAD files tailored for architectural projects which can serve as the foundational blueprints for design and construction phases.',
                    'ko': '건축 프로젝트를 위한 CAD 파일을 개발했으며, 이는 설계 및 건설 단계를 위한 기초 청사진 역할을 합니다.',
                    'fr': 'J\'ai développé des fichiers CAO adaptés aux projets architecturaux, servant de plans directeurs fondamentaux pour les phases de conception et de construction.'
                }
            }
        ]
    },
    {
        'company': {'en': 'Rosemount High School', 'ko': 'Rosemount 고등학교', 'fr': 'École secondaire Rosemount'},
        'roles': [
            {
                'title': {'en': 'Peer Tutor', 'ko': '교내 과외 선생님', 'fr': 'Tuteur scolaire'},
                'start_date': (2024, 2),
                'end_date': (2024, 6),
                'description': {
                    'en': 'Provided academic support in mathematics and science to fellow students, helping them improve their understanding and performance.',
                    'ko': '도움이 필요한 동료 학생들에게 수학과 과학을 가르쳤습니다.',
                    'fr': 'Accompagnement académique de pairs pour renforcer leur compréhension des concepts complexes en mathématiques et en sciences.'
                },
            }
        ]
    }
]

MONTHS = {
    'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'ko': ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
    'fr': ['Janv', 'Févr', 'Mars', 'Avril', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc']
}

def format_duration(start_year, start_month, end_year, end_month):
    total_months = (end_year - start_year) * 12 + (end_month - start_month) + 1
    years = total_months // 12
    months = total_months % 12
    
    res = {'en': '', 'ko': '', 'fr': ''}
    
    if years > 0:
        res['en'] += f"{years} yr{'s' if years > 1 else ''}"
        res['ko'] += f"{years}년"
        res['fr'] += f"{years} an{'s' if years > 1 else ''}"
    if months > 0:
        if years > 0:
            res['en'] += " "
            res['ko'] += " "
            res['fr'] += " "
        res['en'] += f"{months} mo{'s' if months > 1 else ''}"
        res['ko'] += f"{months}개월"
        res['fr'] += f"{months} mois"
        
    if years == 0 and months == 0:
        res = {'en': '0 mos', 'ko': '0개월', 'fr': '0 mois'}
    
    return res

def format_date_str(start_year, start_month, end_year, end_month, is_present=False, show_duration=True):
    s_m_en = MONTHS['en'][start_month - 1]
    s_m_ko = MONTHS['ko'][start_month - 1]
    s_m_fr = MONTHS['fr'][start_month - 1]
    
    if is_present:
        e_en = "Present"
        e_ko = "현재"
        e_fr = "Présent"
    else:
        e_en = f"{MONTHS['en'][end_month - 1]} {end_year}"
        e_ko = f"{end_year}년 {MONTHS['ko'][end_month - 1]}"
        e_fr = f"{MONTHS['fr'][end_month - 1]} {end_year}"
        
    dur_str_en = ""
    dur_str_ko = ""
    dur_str_fr = ""
    
    if show_duration:
        dur = format_duration(start_year, start_month, end_year, end_month)
        dur_str_en = f" · {dur['en']}"
        dur_str_ko = f" · {dur['ko']}"
        dur_str_fr = f" · {dur['fr']}"
    
    return {
        'en': f"{s_m_en} {start_year} - {e_en}{dur_str_en}",
        'ko': f"{start_year}년 {s_m_ko} - {e_ko}{dur_str_ko}",
        'fr': f"{s_m_fr} {start_year} - {e_fr}{dur_str_fr}"
    }

def get_processed_experiences():
    now = datetime.now()
    curr_year = now.year
    curr_month = now.month
    
    processed = []
    for exp in EXPERIENCES:
        earliest_start = (9999, 12)
        latest_end = (0, 1)
        is_current_company = False
        
        show_dur = len(exp['roles']) > 1
        proc_roles = []
        for role in exp['roles']:
            sy, sm = role['start_date']
            
            is_present_tuple = isinstance(role['end_date'], tuple) and len(role['end_date']) == 2 and str(role['end_date'][1]).lower() == 'present'
            if role['end_date'] is None or role['end_date'] == 'present' or is_present_tuple:
                ey, em = curr_year, curr_month
                is_present = True
                is_current_company = True
            else:
                ey, em = role['end_date']
                is_present = False
            
            if (sy, sm) < earliest_start:
                earliest_start = (sy, sm)
                
            if is_present or (ey, em) > latest_end:
                if not is_current_company or is_present: 
                    latest_end = (ey, em)
            
            date_str = format_date_str(sy, sm, ey, em, is_present, show_dur)
            
            proc_roles.append({
                'title': role['title'],
                'date': date_str,
                'description': role['description']
            })
            
        comp_dur = format_duration(earliest_start[0], earliest_start[1], latest_end[0], latest_end[1])
        
        processed.append({
            'company': exp['company'],
            'duration': comp_dur,
            'roles': proc_roles
        })
        
    return processed

PROJECTS = [
    {
        'id': 'CashFlux',
        'tags': ['hackathon', 'team'],
        'title': {
            'en': 'CashFlux',
            'ko': 'CashFlux',
            'fr': 'CashFlux'
        },
        'award': {
            'en': '2nd Place | Brim Track at MPC Hacks',
            'ko': '2등 | Brim 부문 MPC Hacks',
            'fr': '2ᵉ Place | Piste Brim à MPC Hacks'
        },
        'second_award': {
            'en': 'Best Use of ElevenLabs | MPC Hacks',
            'ko': 'ElevenLabs 최고 활용상 | MPC Hacks',
            'fr': 'Meilleure utilisation d\'ElevenLabs | MPC Hacks'
        },
        'tech': ['Python', 'JavaScript', 'Gemini API', 'ElevenLabs'],
        'description': {
            'en': 'An ultimate AI powered expense tracking application.',
            'ko': ' ',
            'fr': ' '
        },
        'full_story': {
            'en': '',
            'ko': '',
            'fr': ''
        },
        'full_tech': ['Python', 'Flask', 'JavaScript', 'Gemini API', 'ElevenLabs', 'Vultr', 'MongoDB'],
        'troubles': {
            'en': '',
            'ko': '',
            'fr': ''
        },
        'collaborators': [{'name': 'Juan', 'linkedin': 'https://www.linkedin.com/in/juan-duran-6aa742205/'}, {'name': 'Kunya', 'linkedin': 'https://www.linkedin.com/in/kunya-zhang-19aa50250/'}, {'name': 'Édouard', 'linkedin': 'https://www.linkedin.com/in/edouardchasse/'}],
        'images': ["/static/CashFlux/CashFlux1.png",
            "/static/CashFlux/CashFlux2.png",
            "/static/CashFlux/CashFlux3.png",
            "/static/CashFlux/CashFlux4.png",
            "/static/CashFlux/CashFlux5.png",
            "/static/CashFlux/CashFlux6.png"],
        'thumbnail': "/static/CashFlux/CashFlux.png",
        'external_links': [
            {
                'name': {'en': 'View Project on Devpost', 'ko': 'Devpost에서 프로젝트 보기', 'fr': 'Voir le Projet sur Devpost'},
                'url': 'https://devpost.com/software/mpc-hacks-2026',
                'icon': 'fa-solid fa-code-branch'
            },
            {
                'name': {'en': 'View Demo Video on YouTube', 'ko': 'YouTube에서 데모 영상 보기', 'fr': 'Voir la Vidéo de Démo sur YouTube'},
                'url': 'https://youtu.be/_azDjQU3Vx4',
                'icon': 'fa-brands fa-youtube'
            }
        ]
    },
    {
        'id': 'chemically-bonded',
        'tags': ['school', 'team'],
        'title': {
            'en': 'Chemically Bonded',
            'ko': 'Chemically Bonded',
            'fr': 'Chemically Bonded'
        },
        'category': {
            'en': 'School Project 2026',
            'ko': '학교 프로젝트 2026',
            'fr': 'Projet Scolaire 2026'
        },
        'tech': ['Python', 'JavaScript', 'Gemini API'],
        'description': {
            'en': 'A specialized AI chatbot for chemistry, achieving a <strong>27.1x reduction in latency</strong> for generating 3D molecular models compared to Claude Sonnet 4.6 (internal testing).',
            'ko': '화학에 특화된 AI 챗봇을 개발하여, 3D 분자 모델 생성 지연 시간을 Claude Sonnet 4.6 대비 <strong>27.1배 단축</strong>시켰습니다 (자체 테스트).',
            'fr': "Conçu un chatbot IA spécialisé en chimie, atteignant une <strong>réduction de latence de 27,1x</strong> pour la génération de modèles moléculaires 3D par rapport à Claude Sonnet 4.6 (tests internes)."
        },
        'full_story': {
            'en': 'This chemistry-related AI chatbot (similar to Dr. Bob) was developped as part of an Integrative Project (IP) at Dawson College in collaboration with James and Alex. It is designed to help students struggling in General Chemistry (202-SN1-RE), by displaying interactive 3D VSEPR models and Lewis structure with explanation genreated by Gemini API.',
            'ko': '현재 James, Alex와 함께 Dawson College의 통합 프로젝트(IP) 과제로 화학 관련 AI 웹사이트를 개발하고 있습니다.',
            'fr': "Je développe actuellement, avec James et Alex, un site web IA lié à la chimie pour notre Projet d'intégration (PI) au Collège Dawson."
        },
        'full_tech': ['Python', 'Flask', 'JavaScript', 'Gemini API', 'SQLite', 'RDKit'],
        'troubles': {
            'en': 'Currently developing the website.',
            'ko': '현재 웹사이트를 개발 중입니다.',
            'fr': 'Le site est actuellement en cours de développement.'
        },
        'collaborators': [{'name': 'James', 'linkedin': 'https://www.linkedin.com/in/james-ferdinand-combista-88039b316/'}, {'name': 'Alex', 'linkedin': 'https://www.linkedin.com/in/alexander-derderian-43b21836b/'}],
        'images': ["/static/ChemicallyBonded/ChemicallyBonded1.png",
            "/static/ChemicallyBonded/ChemicallyBonded2.png",
            "/static/ChemicallyBonded/ChemicallyBonded3.png"],
        'thumbnail': "/static/ChemicallyBonded/ChemicallyBonded.png",
        'external_links': [
            {
                'name': {'en': 'View Project on GitHub', 'ko': 'GitHub에서 프로젝트 보기', 'fr': 'Voir le Projet sur GitHub'},
                'url': 'https://github.com/Jo-9m-n1/ChemicallyBonded',
                'icon': 'fa-brands fa-github'
            },
            {
                'name': {'en': 'View Report', 'ko': '보고서 보기', 'fr': 'Voir le Rapport'},
                'url': '/static/ChemicallyBonded/Chemically_Bonded_report.pdf',
                'icon': 'fa-solid fa-file-pdf'
            },
            {
                'name': {'en': 'View Poster', 'ko': '포스터 보기', 'fr': "Voir l'Affiche"},
                'url': '/static/ChemicallyBonded/Chemically_Bonded_poster.pdf',
                'icon': 'fa-solid fa-file-pdf'
            }
        ]
    },
    {
        'id': 'ourcampus',
        'tags': ['hackathon', 'team'],
        'title': {'en': 'OurCampus', 'ko': 'OurCampus', 'fr': 'OurCampus'},
        'award': {
            'en': '1st Place | JACHacks',
            'ko': '1위 | JACHacks',
            'fr': '1ʳᵉ Place | JACHacks'
        },
        'second_award': {
            'en': 'Best Science Students Project | JACHacks',
            'ko': '최우수 과학 학생 프로젝트상 | JACHacks',
            'fr': 'Meilleur projet d\'étudiants en sciences | JACHacks'
        },
        'tech': ['Next.js', 'Python', 'Gemini API'],
        'description': {
            'en': 'An award-winning project, OurCampus is designed to help students find community by showing mutual breaks and a population heatmap of a campus.',
            'ko': '해커톤에서 개발한 수상작 OurCampus는 공통 휴식 시간과 캠퍼스 인구 히트맵을 통해 학생들이 커뮤니티를 형성할 수 있도록 도와줍니다.',
            'fr': "Projet primé développé lors d'un hackathon, OurCampus aide les étudiants à créer une communauté en affichant les pauses communes et une carte thermique de la population sur le campus."
        },
        'full_story': {
            'en': 'Our team developed a web platform designed to optimize the student campus experience. Building on the foundation of my previous project, "Meeting App", the application leverages the Gemini API to convert uploaded PDF schedules into structured digital formats. The platform also streamlines club management by identifying optimal meeting times based on mutual availability. Additionally, I developed a Campus Heat Map feature that provides real-time visualization of the room occupancy by integrating the Unifi API to track device connectivity across 100+ campus access points. To ensure long-term utility, I architected a data pipeline to export access point metrics into CSV files, enabling the IT and security department to audit traffic patterns without specialized software.',
            'ko': '우리 팀은 학생들의 캠퍼스 경험을 향상시키기 위한 웹 플랫폼을 개발했습니다. 이전 프로젝트인 "Meeting App"을 기반으로, Gemini API를 활용해 업로드된 PDF 시간표를 정형화된 디지털 데이터로 변환합니다. 또한 서로의 가능한 시간을 분석해 최적의 모임 시간을 찾아주어 동아리 운영을 효율화합니다. 추가로 캠퍼스 내 100개 이상의 액세스 포인트의 기기 연결 상태를 Unifi API로 추적해 강의실 점유율을 실시간으로 시각화하는 Campus Heat Map 기능을 개발했습니다. 장기적인 활용을 위해, 액세스 포인트 데이터를 CSV로 추출하는 데이터 파이프라인을 설계하여 IT 및 보안팀이 별도의 전문 소프트웨어 없이도 트래픽 패턴을 분석할 수 있도록 했습니다.',
            'fr': "Notre équipe a développé une plateforme web visant à optimiser l'expérience étudiante sur le campus. S'appuyant sur mon précédent projet « Meeting App », l'application utilise l'API Gemini pour convertir les horaires PDF téléversés en formats numériques structurés. La plateforme simplifie aussi la gestion des clubs en identifiant les meilleurs créneaux de réunion selon les disponibilités communes. J'ai également développé une fonctionnalité « Campus Heat Map » qui visualise en temps réel l'occupation des salles en intégrant l'API Unifi pour suivre la connectivité des appareils sur plus de 100 points d'accès du campus. Pour assurer une utilité à long terme, j'ai conçu un pipeline de données qui exporte les métriques des points d'accès en CSV, permettant aux équipes TI et sécurité d'auditer les flux sans logiciel spécialisé."
        },
        'full_tech': ['Next.js', 'Chart.js', 'Node.js', 'TypeScript', 'Python', 'Gemini API', 'Elevenlabs API', 'Prisma', 'React', 'Socket.io', 'Supabase', 'Tailwind'],
        'troubles': {
            'en': "The primary challenge with overlaying data (number of devices) onto a map image is the fluidity of the web. When using standard pixel values, the dots remain fixed while the map image scales up or down to fit different screen sizes. This causes the markers to drift from their intended landmarks. To solve this, I developed a Python script that calculates the position as a ratio of the image's dimensions instead of recording a static pixel location. This ensures the dots stay pinned to the exact location regardless of the screen size and allows new access points to be added easily, providing better <strong>scalability</strong> to departements in need.",
            'ko': '데이터(기기 수)를 지도 이미지 위에 오버레이할 때의 가장 큰 어려움은 웹의 가변성이었습니다. 픽셀 값을 고정으로 사용하면 화면 크기에 따라 지도 이미지가 확대·축소되어도 점들은 그대로 머물러, 의도한 위치에서 벗어나게 됩니다. 이를 해결하기 위해 정적인 픽셀 좌표가 아닌, 이미지의 크기에 대한 비율로 위치를 계산하는 Python 스크립트를 개발했습니다. 덕분에 화면 크기와 상관없이 점이 정확한 위치에 고정되며, 새로운 액세스 포인트도 손쉽게 추가할 수 있어 필요한 부서에 더 나은 <strong>확장성</strong>을 제공합니다.',
            'fr': "Le principal défi pour superposer des données (nombre d'appareils) sur une image de carte est la fluidité du web. Avec des valeurs en pixels fixes, les points restent figés tandis que l'image de la carte s'agrandit ou se réduit selon la taille de l'écran, ce qui décale les marqueurs de leurs repères. Pour résoudre cela, j'ai développé un script Python qui calcule la position comme un ratio des dimensions de l'image plutôt qu'une coordonnée en pixels statique. Les points restent ainsi épinglés exactement au bon endroit, peu importe la taille de l'écran, et de nouveaux points d'accès peuvent être ajoutés facilement, offrant une meilleure <strong>évolutivité</strong> aux départements qui en ont besoin."
        },
        'collaborators': [{'name': 'Brian', 'linkedin': 'https://www.linkedin.com/in/brian-kim-33348a354/'}, {'name': 'Deven'}, {'name': 'Matteo', 'linkedin': 'https://www.linkedin.com/in/matteo-rombola-287a3b402/'}],
        'images': ["/static/OurCampus/OurCampus1.png",
                   "/static/OurCampus/OurCampus2.png",
                   "/static/OurCampus/OurCampus3.png",
                   "/static/OurCampus/OurCampus4.png",
                   "/static/OurCampus/OurCampus5.png",
                   "/static/OurCampus/OurCampus6.png"],
        'thumbnail': '/static/OurCampus/OurCampus.png/',
        'external_links': [
            {
                'name': {'en': 'View Project on Devpost', 'ko': 'Devpost에서 프로젝트 보기', 'fr': 'Voir le Projet sur Devpost'},
                'url': 'https://devpost.com/software/ourcampus-t2u5fs',
                'icon': 'fa-solid fa-code-branch'
            },
            {
                'name': {'en': 'View Demo Video on YouTube', 'ko': 'YouTube에서 데모 영상 보기', 'fr': 'Voir la Vidéo de Démo sur YouTube'},
                'url': 'https://www.youtube.com/watch?v=IXy2J-jF7Ec',
                'icon': 'fa-brands fa-youtube'
            }
        ],
        'published': {'en': 'April 13, 2026', 'ko': '2026년 4월 13일', 'fr': 'le 13 avril 2026'},
        'updated': {'en': 'April 18, 2026', 'ko': '2026년 4월 18일', 'fr': 'le 18 avril 2026'}
    },
    {
        'id': 'liminal',
        'tags': ['hackathon', 'team'],
        'title': {'en': 'Liminal', 'ko': 'Liminal', 'fr': 'Liminal'},
        'category': {
            'en': 'Hackathon 2026',
            'ko': '해커톤 2026',
            'fr': 'Hackathon 2026'
        },
        'tech': ['Python', 'mmBERT', 'NLP', 'Cohere Command-R'],
        'description': {
            'en': 'A dual-tier AI guardrail system to detect mental health crises in youth facing virtual assistants, <strong>improving crisis recall by 9x</strong> (102 dataset test).',
            'ko': 'AI 챗봇을 사용하는 청소년의 정신 건강 위기를 감지하는 2단계 AI 가드레일 시스템으로, 위기 상황 재현율(recall)을 <strong>9배 향상</strong>시켰습니다 (102개 데이터셋 기준).',
            'fr': "Un système de garde-fou IA à deux niveaux pour détecter les crises de santé mentale chez les jeunes face à des assistants virtuels, <strong>améliorant le rappel des crises de 9×</strong> (test sur 102 données)."
        },
        'full_story': {
            'en': 'During spring break, my team and I developed an AI guardrail system designed to detect mental health crisis in youth interacting with our AI model. Initially, we trained the model on the provided seed dataset; however, we soon realized it was overfitting, as evidenced by perfect 1.000 recall and precision scores. To address this, we engineered a synthetic data pipeline that stress-tested our ungoverned model, successfully diversifying the training data and resolving the overfitting issues.This project taught me a great deal, as it was my first time working with an AI model as a developer. Through this experience, I learned the fundamentals of how to train and refine an AI model, which is an important asset these days.',
            'ko': '봄방학 동안, 저희 팀은 AI 모델과 상호작용하는 청소년의 정신 건강 위기를 감지하는 AI 가드레일 시스템을 개발했습니다. 처음에는 제공된 시드 데이터셋으로 모델을 학습시켰지만, recall과 precision이 모두 1.000으로 완벽하게 나오는 것을 보고 과적합 문제를 발견했습니다. 이를 해결하기 위해 가드레일이 없는 모델을 스트레스 테스트하는 합성 데이터 파이프라인을 구축하여 학습 데이터를 다양화하고 과적합 문제를 해결했습니다. 개발자로서 AI 모델을 직접 다뤄본 것은 이번이 처음이었기에 많은 것을 배울 수 있었습니다. 이 경험을 통해 AI 모델을 학습하고 개선하는 방법의 기본을 익혔으며, 이는 요즘 매우 중요한 자산이 되었습니다.',
            'fr': "Pendant la semaine de relâche, mon équipe et moi avons développé un système de garde-fou IA conçu pour détecter les crises de santé mentale chez les jeunes interagissant avec notre modèle d'IA. Au départ, nous avons entraîné le modèle sur le jeu de données de départ fourni; nous avons cependant rapidement constaté un surapprentissage, avec des scores parfaits de 1,000 en rappel et en précision. Pour résoudre cela, nous avons conçu un pipeline de données synthétiques qui a soumis notre modèle non régulé à des tests de stress, diversifiant ainsi efficacement les données d'entraînement et corrigeant le surapprentissage. Ce projet m'a beaucoup appris, car c'était la première fois que je travaillais avec un modèle d'IA en tant que développeur. J'y ai appris les bases de l'entraînement et du raffinement d'un modèle d'IA, une compétence essentielle de nos jours."
        },
        'full_tech': ['Python', 'PyTorch', 'Cohere API', 'HuggingFace Transformers', 'Mistral AI', 'Regex Safety-Nets', 'Synthetic Data Pipelining'],
        'troubles': {
            'en': 'Initially, we trained our model on the provided seed dataset (n=98), achieving a near-perfect F1 score. However, we suspected overfitting due to the small sample size. Test run against an external dataset (n=102) confirmed that our concerns were valid, as performance dropped significantly. To improve the generalization, we leveraged Gemini to generate synthetic data, <strong>diversifying</strong> our training set and <strong>robustifying</strong> the model.',
            'ko': '처음에는 제공된 시드 데이터셋(n=98)으로 모델을 학습시켜 거의 완벽한 F1 점수를 얻었습니다. 그러나 표본 크기가 작아 과적합이 의심됐고, 외부 데이터셋(n=102)으로 테스트해 본 결과 성능이 크게 떨어져 우려가 사실로 확인됐습니다. 일반화 성능을 높이기 위해 Gemini를 활용해 합성 데이터를 생성하여 학습 데이터를 <strong>다양화</strong>하고 모델을 <strong>견고하게</strong> 만들었습니다.',
            'fr': "Au départ, nous avons entraîné notre modèle sur le jeu de données de départ fourni (n=98), obtenant un score F1 quasi parfait. Nous soupçonnions toutefois un surapprentissage en raison de la petite taille de l'échantillon. Un test sur un jeu de données externe (n=102) a confirmé nos doutes : les performances ont chuté de façon significative. Pour améliorer la généralisation, nous avons utilisé Gemini pour générer des données synthétiques, <strong>diversifiant</strong> ainsi notre ensemble d'entraînement et <strong>renforçant</strong> le modèle."
        },
        'collaborators': [{'name': 'Édouard', 'linkedin': 'https://www.linkedin.com/in/edouardchasse/'}, {'name': 'Natalia', 'linkedin': 'https://www.linkedin.com/in/natalia-sendrea/'}, {'name': 'Nashra', 'linkedin': 'https://www.linkedin.com/in/nashra-babar/'}],
        'thumbnail': "/static/Liminal.png",
        'external_links': [
            {
                'name': {'en': 'View Report', 'ko': '보고서 보기', 'fr': 'Voir le Rapport'},
                'url': '/static/Mila_report.pdf',
                'icon': 'fa-solid fa-file-pdf'
            },
            {
                'name': {'en': 'View Certificate', 'ko': '수료증 보기', 'fr': 'Voir le Certificat'},
                'url': '/static/LiminalCertificate.pdf',
                'icon': 'fa-solid fa-file-pdf'
            }
        ],
        'published': {'en': 'April 15, 2026', 'ko': '2026년 4월 15일', 'fr': 'le 15 avril 2026'}
    },
    {
        'id': 'deckmots',
        'tags': ['hackathon', 'team'],
        'title': {'en': 'DeckMots', 'ko': 'DeckMots', 'fr': 'DeckMots'},
        'category': {
            'en': 'Hackathon 2026',
            'ko': '해커톤 2026',
            'fr': 'Hackathon 2026'
        },
        'tech': ['C#', 'Unity'],
        'description': {
            'en': 'Developed with Unity at a French GameJam, DeckMots is a local 2-player game where you draft teams of unique characters. To block incoming attacks, the defending player must answer a timed French question.',
            'ko': '프랑스어 게임잼에서 Unity로 개발한 2인용 로컬 멀티플레이 게임입니다. 고유한 캐릭터들로 팀을 구성하며, 상대의 공격을 방어하려면 제한 시간 내에 프랑스어 문제를 풀어야 합니다.',
            'fr': "Créé avec Unity lors d'un GameJam, DeckMots est un jeu multijoueur local où deux joueurs forment des équipes de personnages uniques. Pour bloquer une attaque, le défenseur doit répondre à une question de français chronométrée."
        },
        'full_story': {
            'en': 'My teammates, James, Alex and I developed this game during a hackathon (GameJam) at the University of Montreal (UdeM). This was my first French hackathon and my first time building a functional game, which was an eye-opening moment for me. The challenge was to create an educational game for international students aged 11 - 12 to learn French. Inspired by the mechanics of Pokémon, we built a multiplayer card game where players defend against attacks by correctly answering French language questions. Working with Unity on a project of this scale was difficult but it was a rewarding learning curve. Although we did not win anything, I am incredibly proud of how efficiently my team worked to deliver a fully functional game.',
            'ko': '저는 팀원 James, Alex와 함께 Université de Montréal(UdeM)에서 열린 해커톤(GameJam)에서 이 게임을 개발했습니다. 저의 첫 프랑스어 해커톤이자 처음으로 실제로 동작하는 게임을 만드는 경험이어서 시야가 크게 넓어졌습니다. 과제는 11~12세 국제 학생들이 프랑스어를 배울 수 있는 교육용 게임을 만드는 것이었습니다. 포켓몬의 메커니즘에서 영감을 받아, 플레이어가 프랑스어 문제를 맞히며 상대의 공격을 방어하는 멀티플레이 카드 게임을 만들었습니다. 이 정도 규모의 프로젝트를 Unity로 진행하는 것은 어려웠지만 보람찬 학습이었습니다. 비록 수상하지는 못했지만, 짧은 시간 안에 완성된 게임을 만들어낸 팀의 효율성이 매우 자랑스럽습니다.',
            'fr': "Mes coéquipiers James et Alex, et moi avons développé ce jeu lors d'un hackathon (GameJam) à l'Université de Montréal (UdeM). C'était mon premier hackathon en français et la première fois que je créais un jeu fonctionnel, une expérience qui a ouvert mes horizons. Le défi consistait à créer un jeu éducatif pour aider des élèves internationaux de 11 à 12 ans à apprendre le français. Inspirés par les mécaniques de Pokémon, nous avons conçu un jeu de cartes multijoueur où les joueurs se défendent contre les attaques en répondant correctement à des questions de français. Travailler sur un projet de cette envergure avec Unity a été difficile, mais l'apprentissage en a valu la peine. Même si nous n'avons rien gagné, je suis incroyablement fier de l'efficacité avec laquelle mon équipe a livré un jeu pleinement fonctionnel."
        },
        'full_tech': ['C#', 'Unity', 'JSON'],
        'troubles': {
            'en': "Initially, we wanted to develop this as an online multiplayer game. However, after several hours of server development, we realized we did not have the necessary access to utilize Unity Relay. Consequently, we had to pivot our strategy to a local multiplayer format on one device. While an online experience would have been ideal, this constraint allowed us to focus on perfecting the core gameplay mechanics within the hackathon's timeframe of 3 days.",
            'ko': '처음에는 온라인 멀티플레이 게임으로 개발하려 했습니다. 하지만 서버 개발에 몇 시간을 투자한 뒤에야 Unity Relay를 사용할 수 있는 권한이 없다는 사실을 알게 됐습니다. 그 결과 한 기기에서 진행하는 로컬 멀티플레이로 전략을 변경해야 했습니다. 온라인 환경이 이상적이었겠지만, 이 제약 덕분에 3일의 해커톤 기간 동안 핵심 게임플레이를 다듬는 데 집중할 수 있었습니다.',
            'fr': "Au départ, nous voulions développer ce jeu en multijoueur en ligne. Toutefois, après plusieurs heures de développement côté serveur, nous avons réalisé que nous n'avions pas les accès nécessaires pour utiliser Unity Relay. Nous avons donc dû pivoter vers un format multijoueur local sur un seul appareil. Une expérience en ligne aurait été idéale, mais cette contrainte nous a permis de nous concentrer sur la mise au point des mécaniques de jeu principales dans les 3 jours du hackathon."
        },
        'collaborators': [{'name': 'James', 'linkedin': 'https://www.linkedin.com/in/james-ferdinand-combista-88039b316/'}, {'name': 'Alex', 'linkedin': 'https://www.linkedin.com/in/alexander-derderian-43b21836b/'}],
        'images': ["/static/DeckMot/DeckMot1.png",
                   "/static/DeckMot/DeckMot2.png",
                   "/static/DeckMot/DeckMot3.png",
                   "/static/DeckMot/DeckMot4.png",
                   "/static/DeckMot/DeckMot5.png"],
        'thumbnail': "/static/DeckMot/DeckMot.webp",
        'external_links': [
            {
                'name': {'en': 'View Project on Itch.io', 'ko': 'Itch.io에서 프로젝트 보기', 'fr': 'Voir le Projet sur Itch.io'},
                'url': 'https://itch.io/jam/hackathon-pedagogique-udem-2026/rate/4338079',
                'icon': 'fa-solid fa-code-branch'
            },
            {
                'name': {'en': 'View Certificate', 'ko': '수료증 보기', 'fr': 'Voir le Certificat'},
                'url': '/static/DeckMotCertificate.pdf',
                'icon': 'fa-solid fa-file-pdf'
            }
        ],
        'published': {'en': 'March 3, 2026', 'ko': '2026년 3월 3일', 'fr': 'le 3 mars 2026'},
        'updated': {'en': 'March 9, 2026', 'ko': '2026년 3월 9일', 'fr': 'le 9 mars 2026'}
    },
    {
        'id': 'personal-website',
        'tags': ['personal'],
        'title': {'en': 'Personal Website', 'ko': '개인 웹사이트', 'fr': 'Site Web Personnel'},
        'category': {'en': 'Personal Project 2026', 'ko': '개인 프로젝트 2026', 'fr': 'Projet Personnel 2026'},
        'tech': ['Python', 'JavaScript'],
        'description': {
            'en': 'A responsive personal portfolio website using Flask and Python for backend.',
            'ko': 'Flask와 Python을 백엔드로 사용하는 반응형 개인 포트폴리오 웹사이트입니다.',
            'fr': 'Un site web portfolio personnel et adaptatif, utilisant Flask et Python en backend.'
        },
        'full_story': {
            'en': 'I developed this interactive website to provide a deeper look into my background. It includes my key projects, skills, professional experiences and a collection of awards that I have earned throughout my journey (with more being added soon from my archives). As a bonus, I have hidden a few Easter eggs throughout my website for you to find them. Good luck :)',
            'ko': '저는 저의 경력과 배경을 더 깊이 보여주기 위해 이 인터랙티브 웹사이트를 개발했습니다. 주요 프로젝트, 기술 스택, 경력, 그리고 지금까지 받아온 수상 기록(아카이브에서 곧 더 추가될 예정)이 포함되어 있습니다. 보너스로, 사이트 곳곳에 이스터에그를 숨겨두었으니 찾아보세요 :)',
            'fr': "J'ai développé ce site web interactif pour offrir un regard plus approfondi sur mon parcours. Vous y trouverez mes projets clés, mes compétences, mes expériences professionnelles et une collection de prix obtenus tout au long de mon parcours (d'autres seront ajoutés sous peu depuis mes archives). En prime, j'ai caché quelques easter eggs un peu partout sur le site, à vous de les trouver :)"
        },
        'full_tech': ['Python', 'Flask', 'JavaScript'],
        'images': ["/static/MyPersonalWebsite/MyPersonalWebsite1.png",
                   "/static/MyPersonalWebsite/MyPersonalWebsite2.png",
                   "/static/MyPersonalWebsite/MyPersonalWebsite3.png",
                   "/static/MyPersonalWebsite/MyPersonalWebsite4.png"],
        'thumbnail': "/static/MyPersonalWebsite/MyPersonalWebsite.png",
        'published': {'en': 'March 3, 2026', 'ko': '2026년 3월 3일', 'fr': 'le 3 mars 2026'},
        'updated': {'en': 'March 4, 2026', 'ko': '2026년 3월 4일', 'fr': 'le 4 mars 2026'}
    },
    {
        'id': 'dr-bob',
        'tags': ['hackathon', 'team'],
        'title': {'en': 'Dr. Bob', 'ko': 'Bob 박사', 'fr': 'Dr. Bob'},
        'award': {
            'en': '2nd Place | Dialogue Track at ConUHacks',
            'ko': '2등 | Dialogue 부문 ConUHacks',
            'fr': '2ᵉ Place | Piste Dialogue à ConUHacks'
        },
        'tech': ['Python', 'JavaScript', 'Twilio API', 'Gemini API'],
        'description': {
            'en': 'An award-winning project, Dr. Bob uses Twilio to automate patient intake and history tracking, ensuring medical data is organized for doctors.',
            'ko': '해커톤에서 개발한 수상작 Bob 박사는 Twilio를 활용해 환자 접수와 진료 이력 관리를 자동화하여, 의사가 의료 데이터를 체계적으로 확인할 수 있도록 합니다.',
            'fr': "Projet primé développé lors d'un hackathon, Dr. Bob utilise Twilio pour automatiser l'accueil des patients et le suivi des antécédents médicaux, en s'assurant que les données médicales sont bien organisées pour les médecins."
        },
        'full_story': {
            'en': "Oliver and I developed Dr. Bob for our second hackathon. Out of 10 sponsor challenges offered, we picked the Dialogue Track because we both have non-English and non-French speaking parents and understand how difficult it is to make a medical appointment in Canada when you are not fluent in neither in English nor French. We wanted to support the Allophone community, which is why our application is offered in 5 languages: English, French, Korean, Chinese and Arabic. Since this was our second hackathon, we worked more efficiently than we did during our first one. However, we still ran into some hurdles, such as complex merge conflicts that we had to resolve. This was also our first time integrating an AI (Gemini) chatbot, which provided a great learning opportunity. We had to learn how to write prompts to ensure that Bob's responses remained accurate and on-track. Initially, the AI's replies were occasionally unpredictable, but we refined our prompts to ensure that the application delivered a reliable experience to our users. This experience helped me build Chemically Bonded which also uses a same AI API.",
            'ko': 'Oliver와 저는 두 번째 해커톤에서 Dr. Bob을 개발했습니다. 10개의 스폰서 챌린지 중 Dialogue 트랙을 선택했는데, 둘 다 영어와 프랑스어를 못하시는 부모님이 계셔서 캐나다에서 영어나 프랑스어가 능숙하지 않을 때 진료 예약을 잡는 것이 얼마나 어려운지 잘 알기 때문입니다. 영어가 모국어가 아닌 커뮤니티(Allophone)를 돕고 싶었고, 그래서 저희 앱은 영어, 프랑스어, 한국어, 중국어, 아랍어의 5개 언어를 지원합니다. 두 번째 해커톤이라 처음보다 훨씬 효율적으로 작업할 수 있었지만, 복잡한 머지 충돌 등 여러 어려움도 있었습니다. AI(Gemini) 챗봇을 통합한 것도 이번이 처음이었기에 좋은 학습 기회였습니다. Bob의 답변이 정확하고 일관되도록 프롬프트 작성법을 익혀야 했고, 초기에는 답변이 예측 불가능할 때도 있었지만 프롬프트를 정교하게 다듬어 사용자에게 안정적인 경험을 제공할 수 있게 되었습니다. 이 경험은 같은 AI API를 사용하는 Chemically Bonded를 만드는 데에도 큰 도움이 되었습니다.',
            'fr': "Oliver et moi avons développé Dr. Bob lors de notre deuxième hackathon. Parmi les 10 défis commandités proposés, nous avons choisi la piste Dialogue parce que nos parents respectifs ne parlent ni anglais ni français, et nous savons à quel point il peut être difficile de prendre un rendez-vous médical au Canada lorsqu'on ne maîtrise pas ces deux langues. Nous voulions soutenir la communauté allophone, c'est pourquoi notre application est offerte en 5 langues : anglais, français, coréen, chinois et arabe. Comme c'était notre deuxième hackathon, nous avons travaillé plus efficacement que la première fois. Nous avons tout de même rencontré quelques obstacles, comme des conflits de fusion (merge) complexes à résoudre. C'était aussi notre première intégration d'un chatbot IA (Gemini), ce qui a été une belle occasion d'apprentissage. Il a fallu apprendre à rédiger des prompts pour que les réponses de Bob restent précises et pertinentes. Au début, les réponses de l'IA étaient parfois imprévisibles, mais nous avons affiné nos prompts pour offrir une expérience fiable aux utilisateurs. Cette expérience m'a beaucoup aidé à bâtir Chemically Bonded, qui utilise la même API d'IA."
        },
        'full_tech': ['Python', 'Flask', 'JavaScript', 'SQLite', 'SQLAlchemy', 'Twilio API', 'Gemini API', 'Web Speech API', 'Geolocation API', 'Werkzeug Security', 'Leaflet.js'],
        'troubles': {
            'en': 'The most complex technical trouble was connecting the Twilio recording with the Gemini API. I had to architect a pipeline that captured patient audio, retrieved the remote recording via webhooks and processed the binary data for AI analysis, while maintaining a <strong>low-latency</strong> user experience.',
            'ko': '가장 복잡했던 기술적 난제는 Twilio 녹음을 Gemini API와 연결하는 것이었습니다. 환자의 음성을 캡처하고, 웹훅으로 원격 녹음을 가져온 뒤 바이너리 데이터를 AI 분석에 맞게 처리하면서도 <strong>낮은 지연 시간</strong>을 유지하는 파이프라인을 설계해야 했습니다.',
            'fr': "Le défi technique le plus complexe a été de connecter l'enregistrement Twilio à l'API Gemini. J'ai dû concevoir un pipeline qui capturait l'audio du patient, récupérait l'enregistrement à distance via des webhooks et traitait les données binaires pour l'analyse par l'IA, tout en maintenant une <strong>faible latence</strong> côté utilisateur."
        },
        'collaborators': [{'name': 'Oliver', 'linkedin': 'https://www.linkedin.com/in/oliver-massaad-9765a0276'}],
        'images': ["/static/DrBob/DrBob5.png", 
                   "/static/DrBob/DrBob1.png", 
                   "/static/DrBob/DrBob3.png",
                   "/static/DrBob/DrBob4.png", 
                   "/static/DrBob/DrBob2.png", 
                   "/static/DrBob/DrBob6.png", 
                   "/static/DrBob/DrBob8.png",
                   "/static/DrBob/DrBob9.png",
                   "/static/DrBob/DrBob11.png"],
        'thumbnail': '/static/DrBob/DrBob.png/',
        'external_links': [
            {
                'name': {'en': 'View Project on Devpost', 'ko': 'Devpost에서 프로젝트 보기', 'fr': 'Voir le Projet sur Devpost'},
                'url': 'https://devpost.com/software/dr-bob',
                'icon': 'fa-solid fa-code-branch'
            }
        ],
        'published': {'en': 'March 2, 2026', 'ko': '2026년 3월 2일', 'fr': 'le 2 mars 2026'},
        'updated': {'en': 'March 23, 2026', 'ko': '2026년 3월 23일', 'fr': 'le 23 mars 2026'}
    },
    {
        'id': 'meeting-app',
        'tags': ['personal'],
        'title': {'en': 'Meeting App', 'ko': 'Meeting App', 'fr': 'Meeting App'},
        'category': {'en': 'Personal Project 2025', 'ko': '개인 프로젝트 2025', 'fr': 'Projet Personnel 2025'},
        'description': {
            'en': 'A social application to find mutual breaks with your friends by uploading the PDF version of your school schedule.',
            'ko': '학교 시간표 PDF를 업로드해 친구들과 공통 휴식 시간을 찾을 수 있는 소셜 앱입니다.',
            'fr': "Une application sociale qui permet de trouver des pauses communes avec vos amis en téléversant la version PDF de votre horaire scolaire."
        },
        'tech': ['Python', 'JavaScript'],
        'full_story': {
            'en': "This project began as a 'Tinder-style' concept for Cégep students to discover mutual breaks and schedule some meetups. It eventually evolved into a more versatile application, allowing the users to find common free time with any of their friends.",
            'ko': "이 프로젝트는 Cégep 학생들이 공통 휴식 시간을 찾아 모임을 잡을 수 있도록 돕는 '틴더 스타일' 콘셉트로 시작했습니다. 이후 어떤 친구와도 공통의 여가 시간을 쉽게 찾을 수 있는 보다 범용적인 애플리케이션으로 발전했습니다.",
            'fr': "Ce projet a commencé comme un concept « à la Tinder » pour aider les étudiants du Cégep à découvrir leurs pauses communes et à organiser des rencontres. Il a ensuite évolué vers une application plus polyvalente, permettant aux utilisateurs de trouver du temps libre commun avec n'importe lequel de leurs amis."
        },
        'full_tech': ['Python', 'Flask', 'SQLite', 'JavaScript', 'pdfplumber', 'Regex', 'Werkzeug Security'],
        'images': ["/static/MeetingApp/MeetingApp1.png",
                   "/static/MeetingApp/MeetingApp3.png",
                   "/static/MeetingApp/MeetingApp5.png"],
        'thumbnail': '/static/MeetingApp/MeetingApp.png/',
        'published': {'en': 'March 4, 2026', 'ko': '2026년 3월 4일', 'fr': 'le 4 mars 2026'}
    },
    {
        'id': 'j-score',
        'tags': ['school', 'team'],
        'title': {'en': 'J-score*', 'ko': 'J-score*', 'fr': 'J-score*'},
        'category': {'en': 'School Project 2025', 'ko': '학교 프로젝트 2025', 'fr': 'Projet Scolaire 2025'},
        'description': {
            'en': 'A precision tool for calculating academic standing (r-score) using the standard deviation, group-strength and more.',
            'ko': '표준편차, 그룹 강도 등을 활용해 학업 성적(R-score)을 정밀하게 계산해 주는 도구입니다.',
            'fr': "Un outil de précision pour calculer la cote scolaire (cote R) en utilisant l'écart-type, la force du groupe et plus encore."
        },
        'tech': ['Python', 'JavaScript', 'CSV'],
        'full_story': {
            'en': 'James and I developed J-score* as the final project for our third-semester programming class at Dawson College, it was the first large-scale collaborative web application I built with a teammate. While we were both familiar with the basics of Git, this project forced us to move from individual workflows to a synchronized development environment. This important skill helped me build applications within a team and eventually win a few hackathons.',
            'ko': 'James와 저는 Dawson College 3학기 프로그래밍 수업의 최종 프로젝트로 J-score*를 개발했습니다. 팀원과 함께 만든 첫 대규모 협업 웹 애플리케이션이었습니다. 둘 다 Git의 기본은 알고 있었지만, 이 프로젝트를 통해 개인 작업 흐름에서 동기화된 협업 개발 환경으로 전환해야 했습니다. 이 중요한 역량 덕분에 이후 팀으로 애플리케이션을 만들고 여러 해커톤에서 수상할 수 있었습니다.',
            'fr': "James et moi avons développé J-score* comme projet final pour notre cours de programmation de troisième session au Collège Dawson; c'était la première application web collaborative à grande échelle que je bâtissais avec un coéquipier. Bien que nous connaissions tous les deux les bases de Git, ce projet nous a forcés à passer d'un flux de travail individuel à un environnement de développement synchronisé. Cette compétence essentielle m'a ensuite permis de bâtir des applications en équipe et de remporter quelques hackathons."
        },
        'full_tech': ['Python', 'Flask', 'JavaScript', 'CSV', 'Supabase'],
        'troubles': {
            'en': "Initially, the Flask application couldn't distinguish which user was requesting a deletion; it would simply remove the top line of the CSV database, regardless of who it belonged to. This created a major data integrity issue. To solve this, I researched how to pass contextual data through the frontend without cluttering the UI. I implemented hidden HTML inputs to bind specific user metadata to the request. This allowed the backend to verify the user's identity and target the correct row in the CSV file, ensuring that users could only modify their own data. This challenge taught me the vital importance of state management and request context in web applications.",
            'ko': '처음에는 Flask 애플리케이션이 어떤 사용자가 삭제를 요청했는지 구분하지 못하고, 사용자와 상관없이 CSV 데이터베이스의 맨 윗줄을 삭제해 버렸습니다. 이는 데이터 무결성에 큰 문제였습니다. 이를 해결하기 위해 UI를 어지럽히지 않으면서 컨텍스트 데이터를 프론트엔드를 통해 전달하는 방법을 조사했고, 숨겨진 HTML input을 사용해 요청에 사용자 메타데이터를 포함시켰습니다. 덕분에 백엔드가 사용자의 신원을 검증하고 CSV 파일에서 올바른 행을 대상으로 삼아, 사용자가 자신의 데이터만 수정할 수 있도록 보장할 수 있었습니다. 이 과정에서 웹 애플리케이션에서 상태 관리와 요청 컨텍스트가 얼마나 중요한지 배울 수 있었습니다.',
            'fr': "Au départ, l'application Flask ne pouvait pas distinguer quel utilisateur demandait une suppression; elle retirait simplement la première ligne de la base de données CSV, peu importe à qui elle appartenait. Cela posait un grave problème d'intégrité des données. Pour résoudre cela, j'ai cherché comment transmettre des données contextuelles via le frontend sans encombrer l'interface. J'ai implémenté des champs HTML cachés pour lier des métadonnées spécifiques à l'utilisateur à la requête. Le backend pouvait ainsi vérifier l'identité de l'utilisateur et cibler la bonne ligne dans le fichier CSV, garantissant que les utilisateurs ne pouvaient modifier que leurs propres données. Ce défi m'a appris l'importance vitale de la gestion d'état et du contexte de requête dans les applications web."
        },
        'collaborators': [{'name': 'James', 'linkedin': 'https://www.linkedin.com/in/james-ferdinand-combista-88039b316/'}],
        'images': ["/static/J-score/J-score1.png",
                   "/static/J-score/J-score2.png",
                   "/static/J-score/J-score3.png"],
        'thumbnail': '/static/J-score/J-score.png/',
        'external_links': [
            {
                'name': {'en': 'View Project', 'ko': '프로젝트 보기', 'fr': 'Voir le Projet'},
                'url': 'https://j-score.vercel.app/',
                'icon': 'fa-solid fa-code-branch'
            },
            {
                'name': {'en': 'View Project on GitHub', 'ko': 'GitHub에서 프로젝트 보기', 'fr': 'Voir le Projet sur GitHub'},
                'url': 'https://github.com/Jo-9m-n1/J-score',
                'icon': 'fa-brands fa-github'
            }
        ],
        'published': {'en': 'February 15, 2026', 'ko': '2026년 2월 15일', 'fr': 'le 15 février 2026'},
        'updated': {'en': 'March 4, 2026', 'ko': '2026년 3월 4일', 'fr': 'le 4 mars 2026'}
    }
]

COURSES = {
    'dawson': [
        { 'name': {'en': 'Introduction to Programming', 'ko': '프로그래밍 개론', 'fr': 'Introduction à la programmation'}, 'code': '420-SF1-RE', 'semester': {'en': 'Fall 2024', 'ko': '2024년 가을학기', 'fr': 'Automne 2024'}, 'group': 'programming' },
        { 'name': {'en': 'Differential Calculus', 'ko': '미분적분학', 'fr': 'Calcul différentiel'}, 'code': '201-SN2-RE', 'semester': {'en': 'Fall 2024', 'ko': '2024년 가을학기', 'fr': 'Automne 2024'}, 'mcgill': 'MATH 140', 'group': 'math' },
        { 'name': {'en': 'Discrete Mathematics', 'ko': '이산수학', 'fr': 'Mathématiques discrètes'}, 'code': '201-SF5-RE', 'semester': {'en': 'Fall 2024', 'ko': '2024년 가을학기', 'fr': 'Automne 2024'}, 'mcgill': 'MATH 240', 'group': 'math' },
        { 'name': {'en': 'Data Structure and Object Oriented Programming', 'ko': '자료구조 및 객체지향 프로그래밍', 'fr': 'Structures de données et programmation orientée objet'}, 'code': '420-SF2-RE', 'semester': {'en': 'Winter 2025', 'ko': '2025년 겨울학기', 'fr': 'Hiver 2025'}, 'group': 'programming' },
        { 'name': {'en': 'Integral Calculus', 'ko': '적분학', 'fr': 'Calcul intégral'}, 'code': '201-SN3-RE', 'semester': {'en': 'Winter 2025', 'ko': '2025년 겨울학기', 'fr': 'Hiver 2025'}, 'mcgill': 'MATH 141', 'group': 'math' },
        { 'name': {'en': 'Mechanics', 'ko': '역학', 'fr': 'Mécanique'}, 'code': '203-SN1-RE', 'semester': {'en': 'Winter 2025', 'ko': '2025년 겨울학기', 'fr': 'Hiver 2025'}, 'mcgill': 'PHYS 131', 'group': 'physics' },
        { 'name': {'en': 'Program Development in a Graphical Environment', 'ko': '그래픽 환경에서의 프로그램 개발', 'fr': 'Développement de programmes dans un environnement graphique'}, 'code': '420-SF3-RE', 'semester': {'en': 'Fall 2025', 'ko': '2025년 가을학기', 'fr': 'Automne 2025'}, 'group': 'programming' },
        { 'name': {'en': 'Probability and Statistics', 'ko': '확률과 통계', 'fr': 'Probabilités et statistiques'}, 'code': '201-SN1-RE', 'semester': {'en': 'Fall 2025', 'ko': '2025년 가을학기', 'fr': 'Automne 2025'}, 'mcgill': 'MATH 203', 'group': 'math' },
        { 'name': {'en': 'Electricity and Magnetism', 'ko': '전자기학', 'fr': 'Électricité et magnétisme'}, 'code': '203-SN2-RE', 'semester': {'en': 'Fall 2025', 'ko': '2025년 가을학기', 'fr': 'Automne 2025'}, 'mcgill': 'PHYS 142', 'group': 'physics' },
        { 'name': {'en': 'General Chemistry', 'ko': '일반화학', 'fr': 'Chimie générale'}, 'code': '202-SN1-RE', 'semester': {'en': 'Fall 2025', 'ko': '2025년 가을학기', 'fr': 'Automne 2025'}, 'mcgill': 'CHEM 110', 'group': 'chemistry' },
        { 'name': {'en': 'Integrative Project in Computer Science and Mathematics', 'ko': '컴퓨터 과학 및 수학 통합 프로젝트', 'fr': 'Projet d\'intégration en informatique et mathématiques'}, 'code': '420-SF4-RE', 'semester': {'en': 'Winter 2026', 'ko': '2026년 겨울학기', 'fr': 'Hiver 2026'}, 'group': 'programming' },
        { 'name': {'en': 'Linear Algebra and Vector Geometry', 'ko': '선형대수학 및 벡터기하학', 'fr': 'Algèbre linéaire et géométrie vectorielle'}, 'code': '201-SN4-RE', 'semester': {'en': 'Winter 2026', 'ko': '2026년 겨울학기', 'fr': 'Hiver 2026'}, 'mcgill': 'MATH 133', 'group': 'math' },
        { 'name': {'en': 'Waves and Modern Physics', 'ko': '파동 및 현대물리학', 'fr': 'Ondes et physique moderne'}, 'code': '203-SN3-RE', 'semester': {'en': 'Winter 2026', 'ko': '2026년 겨울학기', 'fr': 'Hiver 2026'}, 'mcgill': 'PHYS 131 & 142', 'group': 'physics' }
    ],
    'mcgill': [
        { 'name': {'en': 'Introduction to Computer Science (Est.)', 'ko': '컴퓨터 과학 개론 (예정)', 'fr': 'Introduction à l\'informatique (Prévu)'}, 'code': 'COMP 250', 'semester': {'en': 'Fall 2026', 'ko': '2026년 가을학기', 'fr': 'Automne 2026'}, 'group': 'programming', 'gpa': '--' },
        { 'name': {'en': 'Introduction to Software Systems (Est.)', 'ko': '소프트웨어 시스템 개론 (예정)', 'fr': 'Introduction aux systèmes logiciels (Prévu)'}, 'code': 'COMP 206', 'semester': {'en': 'Fall 2026', 'ko': '2026년 가을학기', 'fr': 'Automne 2026'}, 'group': 'programming', 'gpa': '--' },
        { 'name': {'en': 'Calculus 3 (Est.)', 'ko': '미적분학 3 (예정)', 'fr': 'Calcul 3 (Prévu)'}, 'code': 'MATH 222', 'semester': {'en': 'Fall 2026', 'ko': '2026년 가을학기', 'fr': 'Automne 2026'}, 'group': 'math', 'gpa': '--' }
    ]
}

EDUCATION_SCHOOLS = {
    'dawson': {
        'id': 'dawson',
        'name': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
        'accent': '#145CB1',
        'years': '2024 - 2026',
        'status_key': 'edu_graduated',
        'degree_key': 'edu_dawson_degree',
        'badges': ['edu_deans_list', 'edu_space', 'edu_recognition', 'edu_leadership'],
    },
    'mcgill': {
        'id': 'mcgill',
        'name': {'en': 'McGill University', 'ko': '맥길 대학교', 'fr': 'Université McGill'},
        'accent': '#ED1B2F',
        'years': {'en': '2026 (Est.) - 2029 (Est.)', 'ko': '2026 (예정) - 2029 (예정)', 'fr': '2026 (Prévu) - 2029 (Prévu)'},
        'status_key': 'edu_expected',
        'degree_key': 'edu_mcgill_degree',
        'badges': [],
    },
}

COURSE_GROUP_LABELS = {
    'programming': {'en': 'Programming', 'ko': '프로그래밍', 'fr': 'Programmation'},
    'math': {'en': 'Math', 'ko': '수학', 'fr': 'Mathématiques'},
    'physics': {'en': 'Physics', 'ko': '물리학', 'fr': 'Physique'},
    'chemistry': {'en': 'Chemistry', 'ko': '화학', 'fr': 'Chimie'},
    'general': {'en': 'General', 'ko': '일반', 'fr': 'Général'},
}


def normalize_course_group(group):
    key = str(group or 'general').strip().lower()
    if key.startswith('prog'):
        return 'programming'
    if key.startswith('math'):
        return 'math'
    if key.startswith('phys') or key.startswith('pyh'):
        return 'physics'
    if key.startswith('chem'):
        return 'chemistry'
    return key if key in COURSE_GROUP_LABELS else 'general'


def group_courses_by_semester(courses):
    grouped = {}
    for course in courses:
        semester_dict = course.get('semester')
        if isinstance(semester_dict, dict):
            sem_key = semester_dict.get('en', 'Other')
        else:
            sem_key = semester_dict or 'Other'
        grouped.setdefault(sem_key, []).append(course)
    return grouped

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/education')
def education():
    school = request.args.get('school', 'mcgill')
    if school not in EDUCATION_SCHOOLS:
        school = 'mcgill'
    school_info = EDUCATION_SCHOOLS[school]
    courses = COURSES.get(school, [])
    grouped_courses = group_courses_by_semester(courses)
    return render_template(
        'education.html',
        school=school,
        school_info=school_info,
        schools=EDUCATION_SCHOOLS,
        school_order=['mcgill', 'dawson'],
        grouped_courses=grouped_courses,
        courses=courses,
        course_group_labels=COURSE_GROUP_LABELS,
        normalize_group=normalize_course_group,
    )

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)

@app.route('/achievements')
def achievements():
    competitions = [
        {
            'title': {'en': '2nd Place | Brim Track at MPC Hacks', 'ko': '2등 | Brim 부문 MPC Hacks', 'fr': '2ᵉ Place | Piste Brim à MPC Hacks'},
            'event': {'en': 'Polytechnique Montréal', 'ko': 'Polytechnique Montréal', 'fr': 'Polytechnique Montréal'},
            'date': '2026. 05. 30. - 2026. 05. 31.',
            'color': '#D4AF37',
            'category': 'software canada stem',
            'external_links': [
                {
                    'name': {'en': 'View Project on Devpost', 'ko': 'Devpost에서 프로젝트 보기', 'fr': 'Voir le Projet sur Devpost'},
                    'url': 'https://devpost.com/software/mpc-hacks-2026',
                    'icon': 'fa-solid fa-code-branch'
                },
                {
                    'name': {'en': 'View Demo Video on YouTube', 'ko': 'YouTube에서 데모 영상 보기', 'fr': 'Voir la Vidéo de Démo sur YouTube'},
                    'url': 'https://www.youtube.com/watch?v=_azDjQU3Vx4&feature=youtu.be',
                    'icon': 'fa-brands fa-youtube'
                }
            ]
        },
        {
            'title': {'en': '3rd Place | Dawson Robotics Hackathon 2026', 'ko': '3등 | Dawson Robotics Hackathon 2026', 'fr': '3ᵉ Place | Dawson Robotics Hackathon 2026'},
            'event': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
            'date': '2026. 05. 06. - 2026. 05. 08.',
            'desc': {
                'en': 'Built and programmed an autonomous black line following robot with IR remote control functionality using Python and the Raspberry Pi Pico.',
                'ko': 'Python과 Raspberry Pi Pico를 사용해 IR 리모컨 제어 기능을 갖춘 자율 검정선 추적 로봇을 제작하고 프로그래밍했습니다.',
                'fr': "Construit et programmé un robot autonome de suivi de ligne noire avec contrôle par télécommande IR, en utilisant Python et le Raspberry Pi Pico."
            },
            'color': '#D4AF37',
            'category': 'hardware software canada stem'
        },
        {
            'title': {'en': 'Participated | Cursor Hackathon Montreal', 'ko': '참가 | Cursor Hackathon Montreal', 'fr': 'Participation | Cursor Hackathon Montreal'},
            'event': 'Botpress Inc',
            'date': '2026. 05. 02.',
            'desc': {
                'en': "Participated in a high intensity AI 'vibe-coding' hackathon, using Cursor to rapidly develop an application.",
                'ko': 'Cursor를 활용해 빠르게 애플리케이션을 개발하는 고강도 AI "바이브 코딩" 해커톤에 참가했습니다.',
                'fr': "Participation à un hackathon IA « vibe-coding » de haute intensité, en utilisant Cursor pour développer rapidement une application."
            },
            'category': 'software canada stem'
        },
        {
            'title': {'en': '1st Place | JACHacks', 'ko': '1등 | JACHacks', 'fr': '1ʳᵉ Place | JACHacks'},
            'event': {'en': 'John Abbott College', 'ko': 'John Abbott College', 'fr': 'Collège John Abbott'},
            'date': '2026. 04. 11. - 2026. 04. 12.',
            'desc': {
                'en': 'Awarded First Place and Best Science Student Project, receiving an $800 cash prize.',
                'ko': '1위와 최우수 과학 학생 프로젝트상을 수상하고 800달러의 상금을 받았습니다.',
                'fr': "Lauréat de la 1ʳᵉ place et du prix du meilleur projet d'étudiant en sciences, avec un prix en argent de 800 $."
            },
            'color': '#D4AF37',
            'category': 'software canada stem',
            'external_links': [
                {
                    'name': {'en': 'View Project on Devpost', 'ko': 'Devpost에서 프로젝트 보기', 'fr': 'Voir le Projet sur Devpost'},
                    'url': 'https://devpost.com/software/ourcampus-t2u5fs',
                    'icon': 'fa-solid fa-code-branch'
                },
                {
                    'name': {'en': 'View Demo Video on YouTube', 'ko': 'YouTube에서 데모 영상 보기', 'fr': 'Voir la Vidéo de Démo sur YouTube'},
                    'url': 'https://www.youtube.com/watch?v=IXy2J-jF7Ec',
                    'icon': 'fa-brands fa-youtube'
                }
            ]
        },
        {
            'title': {'en': 'Participated | Championing AI for good', 'ko': '참가 | Championing AI for good', 'fr': 'Participation | Championing AI for good'},
            'event': 'Mila',
            'date': '2026. 03. 16. - 2026. 03. 23.',
            'desc': {
                'en': 'Collaborated with Team Liminal to develop an AI-driven solution for youth mental health. Implemented robust AI guardrails and adversarial red-teaming to ensure safe, empathetic interactions for high-stakes social impact, <strong>improving crisis recall by 9x</strong>.',
                'ko': '팀 Liminal과 협업하여 청소년 정신 건강을 위한 AI 기반 솔루션을 개발했습니다. 견고한 AI 가드레일과 적대적 레드팀(red-team) 평가를 통해 사회적 영향력이 큰 상황에서도 안전하고 공감적인 상호작용을 보장했으며, <strong>위기 상황 재현율을 9배 향상</strong>시켰습니다.',
                'fr': "Collaboration avec l'équipe Liminal pour développer une solution IA dédiée à la santé mentale des jeunes. Mise en place de garde-fous IA robustes et de tests adversariaux (red-teaming) pour garantir des interactions sûres et empathiques dans un contexte à fort impact social, <strong>améliorant le rappel des crises de 9×</strong>."
            },
            'category': 'software canada stem health',
            'external_links': [
                {
                    'name': {'en': 'View Report', 'ko': '보고서 보기', 'fr': 'Voir le Rapport'},
                    'url': '/static/Mila_report.pdf',
                    'icon': 'fa-solid fa-file-pdf'
                },
                {
                    'name': {'en': 'View Certificate', 'ko': '수료증 보기', 'fr': 'Voir le Certificat'},
                    'url': '/static/LiminalCertificate.pdf',
                    'icon': 'fa-solid fa-file-pdf'
                }
            ]
        },
        {
            'title': {'en': 'Participated | VanierHacks', 'ko': '참가 | VanierHacks', 'fr': 'Participation | VanierHacks'},
            'event': {'en': 'Vanier College', 'ko': 'Vanier College', 'fr': 'Collège Vanier'},
            'date': '2026. 03. 21. - 2026. 03. 22.',
            'desc': {
                'en': 'Achieved 8th place in a 25-team Cybersecurity CTF hackathon with a total score of 3,035 points.',
                'ko': '25개 팀이 참가한 사이버보안 CTF 해커톤에서 총 3,035점을 획득해 8위에 올랐습니다.',
                'fr': "Obtenu la 8ᵉ place dans un hackathon CTF de cybersécurité comptant 25 équipes, avec un total de 3 035 points."
            },
            'category': 'software canada stem',
            'external_links': [
                {
                    'name': {'en': 'View the Progression Chart', 'ko': '점수 변동 차트 보기', 'fr': 'Voir le Graphique de Progression'},
                    'url': '/static/Progression_Vanier.png',
                    'icon': 'fa-solid fa-chart-line'
                }
            ]
        },
        {
            'title': {'en': '1st Place | McGill AeroHacks', 'ko': '1등 | McGill AeroHacks', 'fr': '1ʳᵉ Place | McGill AeroHacks'},
            'event': {'en': 'McGill University', 'ko': '맥길 대학교', 'fr': 'Université McGill'},
            'date': '2026. 03. 13. - 2026. 03. 15.',
            'desc': {
                'en': "<strong>Won McGill's first drone hackathon with 220+ participants</strong> using a pocket-sized ESP32-powered drone and two webcams.",
                'ko': '포켓 사이즈 ESP32 드론과 두 대의 웹캠을 사용하여 <strong>220명 이상이 참가한 McGill 최초의 드론 해커톤에서 우승</strong>했습니다.',
                'fr': "<strong>Remporté le premier hackathon de drones de McGill avec plus de 220 participants</strong> en utilisant un drone de poche propulsé par un ESP32 et deux webcams."
            },
            'color': '#D4AF37',
            'category': 'software hardware canada stem',
            'external_links': [
                {
                    'name': {'en': 'View Award', 'ko': '상장 보기', 'fr': 'Voir le Prix'},
                    'url': '/static/AeroHacks.pdf/',
                    'icon': 'fa-solid fa-award'
                },
                {
                    'name': {'en': 'View Project on Devpost', 'ko': 'Devpost에서 프로젝트 보기', 'fr': 'Voir le Projet sur Devpost'},
                    'url': 'https://devpost.com/software/the-ganders',
                    'icon': 'fa-solid fa-code-branch'
                }
            ]
        },
        {
            'title': {'en': '3rd Place | Beginner Track at @HACK', 'ko': '3등 | 초보 부문 @HACK', 'fr': '3ᵉ Place | Piste Débutant à @HACK'},
            'event': {'en': 'Concordia University', 'ko': '콩코디아 대학교', 'fr': 'Université Concordia'},
            'date': '2026. 03. 07. - 2026. 03. 08.',
            'desc': {
                'en': 'Competed in my first-ever Cybersecurity CTF hackathon, placing 9th overall <strong>out of 120 teams</strong> and 3rd in the beginner track out of 87 teams. Scored 4,100 points and won an $800 cash prize.',
                'ko': '저의 첫 사이버보안 CTF 해커톤에 참가해 <strong>120개 팀 중</strong> 종합 9위, 초보 부문 87개 팀 중 3위를 차지했습니다. 4,100점을 획득하고 800달러의 상금을 받았습니다.',
                'fr': "Participation à mon tout premier hackathon CTF en cybersécurité : classé 9ᵉ au général <strong>sur 120 équipes</strong> et 3ᵉ dans la piste débutant sur 87 équipes. 4 100 points et un prix en argent de 800 $."
            },
            'color': '#D4AF37',
            'category': 'software hardware canada stem',
            'external_links': [
                {
                    'name': {'en': 'View the Progression Chart', 'ko': '점수 변동 차트 보기', 'fr': 'Voir le Graphique de Progression'},
                    'url': '/static/Progression_Concordia.png',
                    'icon': 'fa-solid fa-chart-line'
                }
            ]
        },
        {
            'title': {'en': 'Participated | GameJam de la FSÉ', 'ko': '참가 | GameJam de la FSÉ', 'fr': 'Participation | GameJam de la FSÉ'},
            'event': {'en': 'University of Montreal', 'ko': '몬트리올 대학교', 'fr': 'Université de Montréal'},
            'date': '2026. 02. 27. - 2026. 03. 01.',
            'desc': {
                'en': 'Participated in a French GameJam and made DeckMot, a card game to help users learn French in a fun way using Unity and C#.',
                'ko': '프랑스어 GameJam에 참가해 Unity와 C#으로 프랑스어를 재미있게 배울 수 있는 카드 게임 DeckMot을 만들었습니다.',
                'fr': "Participation à un GameJam francophone où j'ai créé DeckMot, un jeu de cartes pour aider les utilisateurs à apprendre le français de manière ludique avec Unity et C#."
            },
            'category': 'software canada stem',
            'external_links': [
                {
                    'name': {'en': 'View Project on Itch.io', 'ko': 'Itch.io에서 프로젝트 보기', 'fr': 'Voir le Projet sur Itch.io'},
                    'url': 'https://itch.io/jam/hackathon-pedagogique-udem-2026/rate/4338079',
                    'icon': 'fa-solid fa-code-branch'
                },
                {
                    'name': {'en': 'View Certificate', 'ko': '수료증 보기', 'fr': 'Voir le Certificat'},
                    'url': '/static/DeckMotCertificate.pdf',
                    'icon': 'fa-solid fa-file-pdf'
                }
            ]
        },
        {
            'title': {'en': 'Best New Genre | Dialogue Internal Hackathon', 'ko': '최우수 신규 부문상 | Dialogue 사내 해커톤', 'fr': 'Meilleure nouvelle catégorie | Hackathon interne Dialogue'},
            'event': 'Dialogue Health Technologies Inc',
            'date': '2026. 02. 12. - 2026. 02. 13.',
            'desc': {
                'en': 'Got invited to their internal hackathon and integrated a skin analysis feature into the Dialogue application, enabling users to receive automated health assessments using Skinive API.',
                'ko': 'Dialogue의 사내 해커톤에 초청받아, Skinive API를 활용해 Dialogue 앱에 피부 분석 기능을 통합하여 사용자가 자동 건강 평가를 받을 수 있도록 했습니다.',
                'fr': "Invité à leur hackathon interne, j'ai intégré une fonctionnalité d'analyse de la peau à l'application Dialogue, permettant aux utilisateurs d'obtenir des évaluations de santé automatisées via l'API Skinive."
            },
            'color': '#D4AF37',
            'category': 'software health canada stem'
        },
        {
            'title': {'en': '2nd Place | Dialogue Track at ConUHacks', 'ko': '2등 | Dialogue 부문 ConUHacks', 'fr': '2ᵉ Place | Piste Dialogue à ConUHacks'},
            'event': {'en': 'Concordia University', 'ko': '콩코디아 대학교', 'fr': 'Université Concordia'},
            'date': '2026. 01. 24. - 2026. 01. 25.',
            'desc': {
                'en': "Competed in <strong>Quebec's largest and Canada's second-largest</strong> student-run hackathon with over <strong>900 participants</strong> and developed Dr. Bob, an AI medical assistant using Python and Gemini API for symptom analysis and a chatbot system. Integrated Leaflet.js and Geolocation APIs to provide real-time location tracking, enabling users to instantly find the nearest clinics.",
                'ko': '<strong>900명 이상</strong>이 참가한 <strong>퀘벡 최대, 캐나다 2위 규모</strong>의 학생 주최 해커톤에서 Python과 Gemini API를 활용해 증상 분석과 챗봇 기능을 갖춘 AI 의료 어시스턴트 Dr. Bob을 개발했습니다. Leaflet.js와 Geolocation API를 연동해 실시간 위치 추적을 구현, 사용자가 가까운 병원을 즉시 찾을 수 있도록 했습니다.',
                'fr': "Participation au <strong>plus grand hackathon étudiant du Québec et au deuxième en importance au Canada</strong>, avec plus de <strong>900 participants</strong>. J'y ai développé Dr. Bob, un assistant médical IA utilisant Python et l'API Gemini pour l'analyse de symptômes et un système de chatbot. J'ai intégré Leaflet.js et les API de géolocalisation pour offrir un suivi en temps réel, permettant aux utilisateurs de trouver instantanément les cliniques les plus proches."
            },
            'color': '#D4AF37',
            'category': 'software health canada stem',
            'external_links': [
                {
                    'name': {'en': 'View Project on Devpost', 'ko': 'Devpost에서 프로젝트 보기', 'fr': 'Voir le Projet sur Devpost'},
                    'url': 'https://devpost.com/software/dr-bob',
                    'icon': 'fa-solid fa-code-branch'
                }
            ]
        },
        {
            'title': {'en': 'Best Use of Gemini API | HackDécouverte', 'ko': 'Gemini API 최우수 활용상 | HackDécouverte', 'fr': "Meilleure utilisation de l'API Gemini | HackDécouverte"},
            'event': {'en': 'Concordia University', 'ko': '콩코디아 대학교', 'fr': 'Université Concordia'},
            'date': '2025. 11. 29.',
            'desc': {
                'en': "Competed in Concordia's first pre-university hackathon. Developed BudgetX, an AI budeting website using Next.js, Gemini API and others.",
                'ko': 'Concordia의 첫 대입 학생 전용 해커톤에 참가해 Next.js, Gemini API 등을 활용한 AI 가계부 웹사이트 BudgetX를 개발했습니다.',
                'fr': "Participation au tout premier hackathon pré-universitaire de Concordia. Développé BudgetX, un site web de budget IA utilisant Next.js, l'API Gemini et d'autres outils."
            },
            'color': '#D4AF37',
            'category': 'software canada stem',
            'external_links': [
                {
                    'name': {'en': 'View Project on MentorMates', 'ko': 'MentorMates에서 프로젝트 보기', 'fr': 'Voir le Projet sur MentorMates'},
                    'url': 'https://www.mentormates.ai/projects/public/8191e37d-b814-48a1-8389-6616ec1491bd',
                    'icon': 'fa-solid fa-code-branch'
                }
            ]
        },
        {
            'title': {'en': '2nd Place | Dawson Robotics Hackathon 2025', 'ko': '2등 | Dawson Robotics Hackathon 2025', 'fr': '2ᵉ Place | Dawson Robotics Hackathon 2025'},
            'event': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
            'date': '2025. 05. 09.',
            'desc': {
                'en': 'Built and programmed autonomous black line following robotic system and IR remoted control functionality using C++ and the Arduino framework.',
                'ko': 'C++과 Arduino 프레임워크를 사용해 IR 리모컨 제어 기능을 갖춘 자율 검정선 추적 로봇 시스템을 제작하고 프로그래밍했습니다.',
                'fr': "Construit et programmé un système robotique autonome de suivi de ligne noire avec contrôle par télécommande IR, en utilisant C++ et le framework Arduino."
            },
            'color': '#D4AF37',
            'category': 'software hardware canada stem'
        },
        {
            'title': {'en': 'Participated | Dawson Science On Tourne', 'ko': '참가 | Dawson Science On Tourne', 'fr': 'Participation | Dawson Science On Tourne'},
            'event': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
            'date': '2025. 04. 04.',
            'desc': {
                'en': 'Designed a drone using 3D printers.',
                'ko': '3D 프린터를 활용해 드론을 설계했습니다.',
                'fr': "Conception d'un drone à l'aide d'imprimantes 3D."
            },
            'category': 'software hardware canada stem'
        },
        {
            'title': {'en': 'School Champion | Waterloo Cayley Math Contest', 'ko': '교내 1위 | Waterloo Cayley Math Contest', 'fr': "Champion de l'école | Waterloo Cayley Math Contest"},
            'event': {'en': 'International', 'ko': '국제 대회', 'fr': 'International'},
            'date': '2022. 02. 22.',
            'desc': {
                'en': 'Top 25% worldwide and school champion.',
                'ko': '전 세계 상위 25%, 교내 1위.',
                'fr': "Top 25 % mondial et champion de l'école."
            },
            'color': '#D4AF37',
            'category': 'math academic canada stem'
        },
        {
            'title': {'en': 'Excellence in Mathematics | The Ultimate Math League', 'ko': '수학 우수상 | The Ultimate Math League', 'fr': 'Excellence en mathématiques | The Ultimate Math League'},
            'event': {'en': 'English Montreal School Board', 'ko': 'English Montreal School Board', 'fr': 'Commission scolaire English-Montréal'},
            'date': '2019',
            'desc': {
                'en': 'Selected as a school representative and awarded for achieving a top-tier score in a board-wide competitive mathematics league. Recognized for elite problem-solving and analytical reasoning among selected representatives from schools across the English Montreal School Board (EMSB).',
                'ko': '학교 대표로 선발되어 EMSB(English Montreal School Board) 전역의 학교 대표들이 참가한 수학 리그에서 최상위권 점수를 기록해 수상했습니다. 선발된 대표들 사이에서 뛰어난 문제 해결 능력과 분석적 사고력을 인정받았습니다.',
                'fr': "Choisi comme représentant de l'école et récompensé pour avoir obtenu un score parmi les meilleurs dans une ligue de mathématiques à l'échelle de la commission scolaire. Reconnu pour son habileté élite en résolution de problèmes et en raisonnement analytique parmi les représentants sélectionnés des écoles de la Commission scolaire English-Montréal (EMSB)."
            },
            'color': '#D4AF37',
            'category': 'math academic canada stem'
        },
        {
            'title': {'en': "Honorable Mention | 'Bright Society' Creative Writing Contest", 'ko': "입선 | 밝은 사회를 위한 글짓기 대회", 'fr': "Mention honorable | Concours d'écriture créative « Bright Society »"},
            'event': {'en': 'Ministry of Justice of the Republic of Korea', 'ko': '대한민국 법무부', 'fr': 'Ministère de la Justice de la République de Corée'},
            'date': '2016. 07. 07.',
            'desc': {
                'en': 'Recognized by the Ministry of Justice for an essay on social ethics and civic values, demonstrating strong communication skills and a deep understanding of community justice.',
                'ko': '사회 윤리와 시민적 가치에 관한 글로 법무부로부터 표창을 받았으며, 뛰어난 소통 능력과 공동체 정의에 대한 깊은 이해를 인정받았습니다.',
                'fr': "Reconnu par le ministère de la Justice pour un essai sur l'éthique sociale et les valeurs civiques, démontrant de solides compétences en communication et une compréhension approfondie de la justice communautaire."
            },
            'color': '#D4AF37',
            'category': 'arts'
        },
        {
            'title': {'en': 'National Honors | National HME Math Contest', 'ko': '전국 우수상 | HME 수학경시대회', 'fr': 'Mention nationale | Concours national HME de mathématiques'},
            'event': {'en': 'South Korea', 'ko': '대한민국', 'fr': 'Corée du Sud'},
            'date': '2016. 06. 08.',
            'desc': {
                'en': 'Recognized for outstanding mathematical logic and problem-solving skills at a national level.',
                'ko': '전국 단위 대회에서 뛰어난 수리 논리와 문제 해결 능력을 인정받아 수상했습니다.',
                'fr': "Reconnu pour une logique mathématique et des compétences de résolution de problèmes exceptionnelles à l'échelle nationale."
            },
            'color': '#D4AF37',
            'category': 'math academic stem'
        },
        {
            'title': {'en': 'Special Merit Award | Sekwang Student Piano Competition', 'ko': '학년준차상 | 세광 학생피아노 경연대회', 'fr': 'Mention spéciale | Concours de piano étudiant Sekwang'},
            'event': {'en': 'South Korea', 'ko': '대한민국', 'fr': 'Corée du Sud'},
            'date': '2015. 11. 28.',
            'desc': {
                'en': 'Recognized for exceptional musical interpretation and technical proficiency at a national piano competition.',
                'ko': '전국 피아노 경연대회에서 뛰어난 음악적 해석과 기교를 인정받아 수상했습니다.',
                'fr': "Reconnu pour une interprétation musicale et une maîtrise technique exceptionnelles lors d'un concours national de piano."
            },
            'color': '#D4AF37',
            'category': 'arts'
        },
        {
            'title': {'en': 'National 1st Place | National HME Math Contest', 'ko': '전국 1위 | HME 수학경시대회', 'fr': '1ʳᵉ Place nationale | Concours national HME de mathématiques'},
            'event': {'en': 'South Korea', 'ko': '대한민국', 'fr': 'Corée du Sud'},
            'date': '2014. 05. 24.',
            'desc': {
                'en': 'Top 0.1% in South Korea with a perfect score.',
                'ko': '만점으로 한국 상위 0.1%를 기록했습니다.',
                'fr': 'Top 0.1 % en Corée du Sud avec une note parfaite.'
            },
            'color': '#D4AF37',
            'category': 'math academic stem'
        },
        {
            'title': {'en': '3rd Place | Dental Health Awareness Art Contest', 'ko': '3등 | 치아 사랑 사생대회', 'fr': "3ᵉ Place | Concours d'art sur la sensibilisation à la santé dentaire"},
            'event': {'en': 'Gwangju Dental Association', 'ko': '광주광역시치과의사회', 'fr': 'Association dentaire de Gwangju'},
            'date': '2013. 06. 11.',
            'desc': {
                'en': 'Awarded for creative work in the "Oral Health Awareness" category.',
                'ko': '"구강 건강 인식" 부문에서 창의적인 작품으로 수상했습니다.',
                'fr': "Récompensé pour un travail créatif dans la catégorie « Sensibilisation à la santé buccodentaire »."
            },
            'color': '#D4AF37',
            'category': 'health arts'
        },
        {
            'title': {'en': "Special Merit Award | International Children's Art Grand Exhibition", 'ko': '특선상 | 국제 아동미술대제전', 'fr': "Mention spéciale | Grande exposition internationale d'art pour enfants"},
            'event': {'en': 'International Culture and Art Education Association', 'ko': '국제 문화예술교육회', 'fr': "Association internationale d'éducation culturelle et artistique"},
            'date': '2011. 07. 04.',
            'desc': {
                'en': 'Awarded for exceptional creative vision.',
                'ko': '뛰어난 창의적 시각을 인정받아 수상했습니다.',
                'fr': 'Récompensé pour une vision créative exceptionnelle.'
            },
            'color': '#D4AF37',
            'category': 'arts'
        },
        {
            'title': {'en': "1st Place | 10th Children's Day Art Competition", 'ko': '1등 | 제10회 어린이날 그림대회', 'fr': "1ʳᵉ Place | 10ᵉ concours d'art de la Fête des enfants"},
            'event': {'en': 'Kwangju Bank', 'ko': '광주은행', 'fr': 'Banque Kwangju'},
            'date': '2011. 05. 27.',
            'desc': {
                'en': 'Awarded the highest honor for exceptional creative expression among preschool participants.',
                'ko': '미취학 아동 참가자 중 뛰어난 창의적 표현으로 최우수상을 받았습니다.',
                'fr': "Récompensé du plus grand honneur pour une expression créative exceptionnelle parmi les participants d'âge préscolaire."
            },
            'color': '#D4AF37',
            'category': 'arts'
        }
    ]

    certificates = [
        {
            'title': {'en': 'Campus Life Leadership Award', 'ko': '리더십 상', 'fr': 'Prix de leadership'},
            'event': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
            'date': '2026. 06. 23.',
            'desc': {
                'en': 'This prestigious $750 graduation award is presented to a single graduating student who has demonstrated exceptional leadership and made the most significant contribution to student life and the campus community throughout their time at Dawson College.',
                'ko': 'Dawson College 졸업생 전체 중 단 한 명에게만 수여되는 750달러 상당의 영예로운 상으로, 재학 기간 동안 탁월한 리더십을 발휘하여 학생 커뮤니티와 캠퍼스 생활 발전에 가장 크게 기여한 학생에게 주어집니다.',
                'fr': "Ce prestigieux prix de fin d'études de 750 $ est décerné à un seul étudiant diplômé ayant fait preuve d'un leadership exceptionnel et ayant apporté la contribution la plus significative à la vie étudiante et à la communauté du Collège Dawson tout au long de son parcours."
            },
            'color': '#D4AF37',
            'category': 'canada',
            'external_links': [
                {
                    'name': {'en': 'View Award', 'ko': '상장 보기', 'fr': 'Voir le Prix'},
                    'url': 'https://www.dawsoncollege.qc.ca/awards-scholarships/award-recipients/lee-jongmin//',
                    'icon': 'fa-solid fa-award'
                }
            ]
        },
        {
            'title': {'en': 'SPACE Certificate', 'ko': 'SPACE 수료증', 'fr': 'SPACE Certificate'},
            'event': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
            'date': '2026. 05. 31.',
            'desc': {
                'en': 'The SPACE Certificate recognizes students for excellence in multidisciplinary projects that integrate science, technology, and the arts in Dawson College.',
                'ko': 'SPACE Certificate는 Dawson College에서 과학, 기술, 예술을 통합한 다학제 프로젝트에서 우수성을 보인 학생들을 인증하는 자격입니다.',
                'fr': "Le SPACE Certificate reconnaît les étudiants pour leur excellence dans des projets multidisciplinaires qui intègrent la science, la technologie et les arts au Collège Dawson."
            },
            'category': 'software hardware canada stem math arts'
        },
        {
            'title': {'en': 'Volunteered more than 100 hours', 'ko': '봉사 시간 100시간 이상 달성', 'fr': 'Plus de 100 heures de bénévolat'},
            'event': {'en': 'Montreal', 'ko': '몬트리올', 'fr': 'Montréal'},
            'date': {'en': 'Ongoing', 'ko': '진행 중', 'fr': 'En cours'},
            'desc': {
                'en': '100+ hours of certified community service, demonstrating long-term civic commitment and leadership through various volunteer initiatives.',
                'ko': '다양한 자원봉사 활동을 통해 시민적 책임과 리더십을 꾸준히 보여준 100시간 이상의 공인 지역사회 봉사활동을 하였습니다.',
                'fr': "Plus de 100 heures de service communautaire certifié, témoignant d'un engagement civique et d'un leadership à long terme à travers diverses initiatives bénévoles."
            },
            'color': '#D4AF37',
            'category': 'canada job'
        },
        {
            'title': {'en': 'Recognition of Student Involvement', 'ko': '학생 활동 인증', 'fr': "Reconnaissance de l'engagement étudiant"},
            'event': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
            'date': {'en': 'Winter 2026', 'ko': '2026년 겨울학기', 'fr': 'Hiver 2026'},
            'desc': {
                'en': '60+ hours of contribution to the Dawson College community through active leadership and support in one semester (winter 2026).',
                'ko': '2026년 겨울학기 한 학기 동안 적극적인 리더십과 지원을 통해 Dawson College 커뮤니티에 60시간 이상 기여했습니다.',
                'fr': "Plus de 60 heures de contribution à la communauté du Collège Dawson grâce à un leadership actif et un soutien lors d'une session (Hiver 2026)."
            },
            'category': 'canada'
        },
        {
            'title': {'en': 'Recognition of Student Involvement', 'ko': '학생 활동 인증', 'fr': "Reconnaissance de l'engagement étudiant"},
            'event': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
            'date': {'en': 'Fall 2025', 'ko': '2025년 가을학기', 'fr': 'Automne 2025'},
            'desc': {
                'en': '60+ hours of contribution to the Dawson College community through active leadership and support in one semester (fall 2025).',
                'ko': '2025년 가을학기 한 학기 동안 적극적인 리더십과 지원을 통해 Dawson College 커뮤니티에 60시간 이상 기여했습니다.',
                'fr': "Plus de 60 heures de contribution à la communauté du Collège Dawson grâce à un leadership actif et un soutien lors d'une session (Automne 2025)."
            },
            'category': 'canada'
        },
        {
            'title': {'en': 'Be There Certificate', 'ko': 'Be There Certificate', 'fr': 'Be There Certificate'},
            'event': {'en': 'Online', 'ko': '온라인', 'fr': 'En ligne'},
            'date': '2025. 08. 02.',
            'desc': {
                'en': 'Completed comprehensive mental health support training to better assist people in distress.',
                'ko': '어려움을 겪는 사람들을 더 잘 돕기 위한 포괄적인 정신 건강 지원 훈련을 수료했습니다.',
                'fr': "Formation complète en soutien en santé mentale, afin de mieux aider les personnes en détresse."
            },
            'category': 'health stem',
            'external_links': [
                {
                    'name': {'en': 'View Certificate', 'ko': '수료증 보기', 'fr': 'Voir le Certificat'},
                    'url': '/static/BeThereCertificate.pdf',
                    'icon': 'fa-solid fa-file-pdf'
                }
            ]
        },
        {
            'title': {'en': "Dean's List", 'ko': '학장 명단', 'fr': "Liste d'honneur du doyen"},
            'event': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
            'date': {'en': 'Fall 2024', 'ko': '2024년 가을학기', 'fr': 'Automne 2024'},
            'desc': {
                'en': 'Achieved an academic average above 85% with a full course load and no failed components.',
                'ko': '전체 과목을 이수하면서도 낙제 없이 평균 85% 이상의 성적을 달성했습니다.',
                'fr': "Moyenne académique supérieure à 85 % avec une charge de cours complète et sans aucun échec."
            },
            'color': '#D4AF37',
            'category': 'academic canada'
        },
        {
            'title': {'en': 'Recognition of Volunteerism from the Dean', 'ko': '학장 자원봉사 표창', 'fr': 'Reconnaissance du doyen pour le bénévolat'},
            'event': {'en': 'Dawson College', 'ko': 'Dawson College', 'fr': 'Collège Dawson'},
            'date': '2024. 10. 20.',
            'desc': {
                'en': "Volunteered for Dawson's science open house event.",
                'ko': 'Dawson의 과학 오픈하우스 행사에 자원봉사로 참여했습니다.',
                'fr': "Bénévole lors de la journée portes ouvertes en sciences de Dawson."
            },
            'category': 'canada',
            'external_links': [
                {
                    'name': {'en': 'View Proof', 'ko': '증빙 보기', 'fr': 'Voir la Preuve'},
                    'url': '/static/Volunteerism.pdf',
                    'icon': 'fa-solid fa-file-pdf'
                }
            ]
        },
        {
            'title': {'en': 'Music achievement Award', 'ko': '음악 성취상', 'fr': 'Prix de réussite musicale'},
            'event': {'en': 'Rosemount High School', 'ko': 'Rosemount 고등학교', 'fr': 'École secondaire Rosemount'},
            'date': '2023',
            'desc': {
                'en': 'Won a high school music award (trumpet).',
                'ko': '고등학교 음악상(트럼펫)을 수상했습니다.',
                'fr': 'Lauréat d\'un prix de musique au secondaire (trompette).'
            },
            'color': '#D4AF37',
            'category': 'canada arts'

        },
        {
            'title': {'en': 'Musician Award', 'ko': '음악인상', 'fr': 'Prix du musicien'},
            'event': {'en': 'Rosemount High School', 'ko': 'Rosemount 고등학교', 'fr': 'École secondaire Rosemount'},
            'date': '2022',
            'desc': {
                'en': 'Won a high school music award (trumpet).',
                'ko': '고등학교 음악상(트럼펫)을 수상했습니다.',
                'fr': 'Lauréat d\'un prix de musique au secondaire (trompette).'
            },
            'color': '#D4AF37',
            'category': 'canada arts'

        },
        {
            'title': {'en': 'Junior Jazz Band', 'ko': '주니어 재즈 밴드', 'fr': 'Harmonie jazz junior'},
            'event': {'en': 'Rosemount High School', 'ko': 'Rosemount 고등학교', 'fr': 'École secondaire Rosemount'},
            'date': {'en': 'Fall 2021 - Winter 2022', 'ko': '2021년 가을 - 2022년 겨울', 'fr': 'Automne 2021 - Hiver 2022'},
            'desc': {
                'en': 'Part of the junior jazz band and played the trumpet.',
                'ko': '주니어 재즈 밴드에 소속되어 트럼펫을 연주했습니다.',
                'fr': "Membre de l'harmonie jazz junior, à la trompette."
            },
            'category': 'canada arts'

        },
        {
            'title': {'en': 'Art-Études Program', 'ko': '예술 및 스터디 프로그램', 'fr': 'Programme Arts-Études'},
            'event': {'en': 'Rosemount High School', 'ko': 'Rosemount 고등학교', 'fr': 'École secondaire Rosemount'},
            'date': {'en': 'Fall 2019 - Winter 2024', 'ko': '2019년 가을 - 2024년 겨울', 'fr': 'Automne 2019 - Hiver 2024'},
            'desc': {
                'en': 'The Art-Études program is a specialized Quebec academic stream that compresses the standard curriculum into half-days to allow for intensive, professional-level training in the fine arts. It is designed for high-achieving students who possess the discipline to maintain top grades while dedicating significant daily hours to creative mastery and technical studio work.',
                'ko': 'Art-Études(예술 및 스터디) 프로그램은 일반 교과 과정을 반나절로 압축해 미술 분야의 집중적이고 전문가 수준의 훈련을 가능하게 하는 퀘벡의 특화된 학업 과정입니다. 매일 상당한 시간을 창작과 스튜디오 작업에 쏟으면서도 최상위 성적을 유지할 수 있는 자기 관리 능력을 갖춘 우수 학생들을 위한 프로그램입니다.',
                'fr': "Le programme Arts-Études est une filière scolaire québécoise spécialisée qui compresse le curriculum standard en demi-journées afin de permettre une formation intensive de niveau professionnel en beaux-arts. Il s'adresse aux élèves performants ayant la discipline nécessaire pour maintenir des notes élevées tout en consacrant chaque jour de longues heures à la maîtrise créative et au travail technique en studio."
            },
            'category': 'arts canada'
        },
        {
            'title': {'en': 'High honor or honor roll', 'ko': '최우수/명예 학생 명단', 'fr': "Tableau d'honneur supérieur ou tableau d'honneur"},
            'event': {'en': 'Rosemount High School', 'ko': 'Rosemount 고등학교', 'fr': 'École secondaire Rosemount'},
            'date': {'en': 'Fall 2019 - Winter 2024', 'ko': '2019년 가을 - 2024년 겨울', 'fr': 'Automne 2019 - Hiver 2024'},
            'desc': {
                'en': 'High honor or honor roll in high school <strong>every semester</strong>, demonstrating a high performance academically.',
                'ko': '고등학교 <strong>모든 학기</strong>에서 최우수 또는 명예 학생 명단에 올라 뛰어난 학업 성과를 보여주었습니다.',
                'fr': "Inscrit au tableau d'honneur supérieur ou au tableau d'honneur <strong>chaque session</strong> du secondaire, témoignant d'une performance académique élevée."
            },
            'color': '#D4AF37',
            'category': 'academic canada'
        }
    ]
    return render_template('achievements.html', competitions=competitions, certificates=certificates)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    if 0 <= project_id < len(PROJECTS):
        project = PROJECTS[project_id]
        return render_template('project_detail.html', p=project)
    return "Project not found", 404

if __name__ == '__main__':
    app.run(debug=True)
