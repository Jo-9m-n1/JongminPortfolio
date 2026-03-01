import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates', static_folder='../static')

PROJECTS = [
    {
        'id': 'deckmots',
        'tags': ['hackathon'],
        'title': 'DeckMots',
        'category': 'Hackathon 2026',
        'tech': ['C#', 'Unity'],
        'description': 'Currently developing the website.',
        'full_story': 'Detailed analysis forthcoming.',
        'full_tech': ['C#', 'Unity'],
        'troubles': 'Currently developing the website',
        'collaborators': [{'name': 'James', 'linkedin': 'https://www.linkedin.com/in/james-ferdinand-combista-88039b316/'}, {'name': 'Alex', 'linkedin': 'https://www.linkedin.com/in/alexander-derderian-43b21836b/'}],
        'images': []
    },
    {
        'id': 'chemically-bonding',
        'tags': ['school'],
        'title': 'Chemically Bonding',
        'category': 'School Project 2026',
        'tech': ['Python', 'JavaScript', 'Gemini API'],
        'description': 'Currently developing the website.',
        'full_story': 'Detailed analysis forthcoming.',
        'full_tech': ['Python', 'Flask', 'JavaScript', 'Gemini API', 'SQLite'],
        'troubles': 'Currently developing the website',
        'collaborators': [{'name': 'James', 'linkedin': 'https://www.linkedin.com/in/james-ferdinand-combista-88039b316/'}, {'name': 'Alex', 'linkedin': 'https://www.linkedin.com/in/alexander-derderian-43b21836b/'}],
        'images': []
    },
    {
        'id': 'personal-website',
        'tags': ['personal'],
        'title': 'Personal Website',
        'category': 'Personal Project 2026',
        'tech': ['Python', 'JavaScript'],
        'description': 'Developed a responsive personal portfolio website using Flask and Python for backend.',
        'full_story': 'Detailed analysis forthcoming.',
        'full_tech': ['Python', 'Flask', 'JavaScript'],
        'troubles': 'Detailed analysis forthcoming.',
        'images': ["/static/MyPersonalWebsite1.png", 
                   "/static/MyPersonalWebsite2.png"]
    },
    {
        'id': 'dr-bob',
        'tags': ['hackathon'],
        'title': 'Dr. Bob',
        'award': '2nd Place: Dialogue Challenge at ConUHacks', 
        'category': 'Hackathon 2026',
        'tech': ['Python', 'JavaScript', 'Twilio API', 'Gemini API'],
        'description': 'Developed at a hackathon, Dr. Bob uses Twilio to automate patient intake and history tracking, ensuring medical data is organized for doctors.',
        'full_story': 'Detailed analysis forthcoming.',
        'full_tech': ['Python', 'Flask', 'JavaScript', 'SQLite', 'SQLAlchemy', 'Twilio API', 'Gemini API', 'Web Speech API', 'Geolocation API', 'Werkzeug Security', 'Leaflet.js'],
        'troubles': 'The most complex technical trouble was connecting the Twilio recording with the Gemini API. I had to architect a pipeline that captured patient audio, retrieved the remote recording via webhooks and processed the binary data for AI analysis, while maintaining a low-latency user experience.',
        'collaborators': [{'name': 'Oliver', 'linkedin': 'https://www.linkedin.com/in/oliver-massaad-9765a0276'}],
        'images': ["/static/DrBob5.png", 
                   "/static/DrBob1.png", 
                   "/static/DrBob3.png",
                   "/static/DrBob4.png", 
                   "/static/DrBob2.png", 
                   "/static/DrBob6.png", 
                   "/static/DrBob8.png",
                   "/static/DrBob9.png",
                   "/static/DrBob11.png"]
    },
    {
        'id': 'meeting-app',
        'tags': ['personal'],
        'title': 'Meeting App',
        'category': 'Personal Project 2025',
        'description': 'A tool to find mutual breaks with your friends.',
        'tech': ['Python', 'JavaScript'],
        'full_story': 'Detailed analysis forthcoming.',
        'full_tech': ['Python', 'Flask', 'SQLite', 'JavaScript', 'pdfplumber', 'Regex', 'Werkzeug Security'],
        'troubles': 'Detailed analysis forthcoming.',
        'images': ["/static/MeetingApp1.png",
                   "/static/MeetingApp3.png",
                   "/static/MeetingApp5.png"]
    },
    {
        'id': 'j-score',
        'tags': ['school'],
        'title': 'J-Score*',
        'category': 'School Project 2025',
        'description': 'A precision tool for calculating academic standing (r-score) using the standard deviation.',
        'tech': ['Python', 'JavaScript', 'CSV'],
        'full_story': 'James and I developed the J-Score as the final project for our third-semester programming class at Dawson College, it was the first large-scale collaborative web application I built with a teammate. While we were both familiar with the basics of Git, this project forced us to move from individual workflows to a synchronized development environment. This important skill helped me make application as a team and win few hackathons.',
        'full_tech': ['Python', 'Flask', 'JavaScript', 'CSV'],
        'troubles': "Initially, the Flask application couldn't distinguish which user was requesting a deletion; it would simply remove the top line of the CSV database, regardless of who it belonged to. This created a major data integrity issue. To solve this, I researched how to pass contextual data through the frontend without cluttering the UI. I implemented hidden HTML inputs to bind specific user metadata to the request. This allowed the backend to verify the user’s identity and target the correct row in the CSV file, ensuring that users could only modify their own data. This challenge taught me the vital importance of state management and request context in web applications.",
        'collaborators': [{'name': 'James', 'linkedin': 'https://www.linkedin.com/in/james-ferdinand-combista-88039b316/'}],
        'images': ["/static/J-score1.png",
                   "/static/J-score2.png",
                   "/static/J-score3.png"]
    }
]


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)

@app.route('/achievements')
def achievements():
    competitions = [
        {
            'title': 'Will Participate | DawsHacks',
            'event': 'Dawson College',
            'date': '2026. 05. 02.',
            'start-date': '2026-05-02T08:30:00',
            'end-date': '2026-05-02T19:00:00',
            'desc': 'Currently preparing for this upcoming hackathon...',
            'color': '#cbd5e1',
            'category': 'software canada stem'
        },
        {
            'title': 'Will Participate | MariHacks',
            'event': 'Marianopolis College',
            'date': '2026. 04. 17. - 2026. 04. 18.',
            'start-date': '',
            'end-date': '',
            'desc': 'Currently preparing for this upcoming hackathon...',
            'color': '#cbd5e1',
            'category': 'software canada stem',
        },
        {
            'title': 'Will Participate | JacHacks',
            'event': 'John Abbott College',
            'date': '2026. 04. 11. - 2026. 04. 12.',
            'start-date': '',
            'end-date': '',
            'desc': 'Currently preparing for this upcoming hackathon...',
            'color': '#cbd5e1',
            'category': 'software canada stem'
        },
        {
            'title': 'Will Participate | VanierHacks!',
            'event': 'Vanier College',
            'date': '2026. 03. 21. - 2026. 03. 22.',
            'start-date': '',
            'end-date': '',
            'desc': 'Currently preparing for this upcoming hackathon...',
            'color': '#cbd5e1',
            'category': 'software canada stem'
        },
        {
            'title': 'Will Participate | McGill AeroHacks',
            'event': 'McGill University',
            'date': '2026. 03. 13. - 2026. 03. 15.',
            'start-date': '2026-03-13T12:00:00',
            'end-date': '2026-03-15T17:00:00',
            'desc': 'Currently preparing for this upcoming hackathon...',
            'color': '#cbd5e1',
            'category': 'software hardware canada stem'
        },
        {
            'title': 'Currently Participating | UdeM GameJam',
            'event': 'University of Montreal',
            'date': '2026. 02. 27. - 2026. 03. 01.',
            'start-date': '2026-02-27T16:00:00',
            'end-date': '2026-03-01T17:00:00',
            'desc': 'Currently in this hackathon.',
            'color': '#cbd5e1',
            'category': 'software canada stem'
        },
        {
            'title': 'Award Winner | Dialogue Internal Hackathon',
            'event': 'Dialogue Health Technologies Inc',
            'date': '2026. 02. 12. - 2026. 02. 13.',
            'desc': 'Got invited to their internal hackathon and integrated a skin analysis feature into the Dialogue application, enabling users to receive automated health assessments using Skinive API.',
            'color': '#D4AF37',
            'category': 'software health canada stem'
        },
        {
            'title': '2nd Place | Dialogue Track at ConUHacks',
            'event': 'Concordia University',
            'date': '2026. 01. 24. - 2026. 01. 25.',
            'desc': "Competed in Quebec's largest and Canada's second-largest student-run hackathon with over 850 participants and developed 'Dr. Bob', an AI medical assistant using Python and Gemini API for symptom analysis and a chatbot system. Integrated Leaflet.js and Geolocation APIs to provide real-time location tracking, enabling users to instantly find the nearest clinics.",
            'color': '#D4AF37',
            'category': 'software health canada stem',
            'link_type': 'devpost',
            'link': "https://devpost.com/software/dr-bob?_gl=1*jtzmxn*_gcl_au*NDIyNDEwNzUyLjE3NjkzNTIwMzA.*_ga*MTk0NTUzOTc1NC4xNzY5MzUyMDMx*_ga_0YHJK3Y10M*czE3NzEyNTQ3ODQkbzE1JGcxJHQxNzcxMjU0ODQ0JGo2MCRsMCRoMA.."
        },
        {
            'title': 'Best Use of Gemini API | HackDécouverte',
            'event': 'Concordia University',
            'date': '2025. 11. 29.',
            'desc': "Competed in Concordia's first pre-university hackathon. Developed 'BudgetX', an AI budeting website using Next.js, Gemini API and others.",
            'color': '#D4AF37',
            'category': 'software canada stem',
            'link_type': 'mentormates',
            'link': 'https://www.mentormates.ai/projects/public/8191e37d-b814-48a1-8389-6616ec1491bd'
        },
        {
            'title': '2nd Place | Dawson Robotics Hackathon',
            'event': 'Dawson College',
            'date': '2025. 05. 09.',
            'desc': 'Built and programmed autonomous black line following robotic system and IR remoted control functionality using C++ and the Arduino framework.',
            'color': '#D4AF37',
            'category': 'software hardware canada stem'
        },
        {
            'title': 'Participated | Dawson Science On Tourne',
            'event': 'Dawson College',
            'date': '2025. 04. 04.',
            'desc': 'Designed a drone using 3D printers.',
            'category': 'software hardware canada stem math'
        },
        {
            'title': 'School Champion | Waterloo Cayley Math Contest',
            'event': 'International',
            'date': '2022. 02. 22.',
            'desc': 'Top 25% in the world and school champion.',
            'color': '#D4AF37',
            'category': 'math academic canada stem'
        },
        {
            'title': 'Excellence in Mathematics | The Ultimate Math League',
            'event': 'English Montreal School Board',
            'date': '2019',
            'desc': 'Selected as a school representative and awarded for achieving a top-tier score in a board-wide competitive mathematics league. Recognized for elite problem-solving and analytical reasoning among selected representatives from schools across the English Montreal School Board (EMSB).',
            'color': '#D4AF37',
            'category': 'math academic canada stem'
        },
        {
            'title': "Honorable Mention | 'Bright Society' Creative Writing Contest",
            'event': 'Ministry of Justice of the Republic of Korea',
            'date': '2016. 07. 07.',
            'desc': 'Recognized by the Ministry of Justice for an essay on social ethics and civic values, demonstrating strong communication skills and a deep understanding of community justice.',
            'color': '#D4AF37',
            'category': 'arts'
        },
        {
            'title': 'National Honors | National HME Math Contest',
            'event': 'South Korea',
            'date': '2016. 06. 08.',
            'desc': 'Recognized for outstanding mathematical logic and problem-solving skills at a national level.',
            'color': '#D4AF37',
            'category': 'math academic stem'
        },
        {
            'title': 'Special Merit Award | Sekwang Student Piano Competition',
            'event': 'South Korea',
            'date': '2015. 11. 28.',
            'desc': 'Recognized for exceptional musical interpretation and technical proficiency at a national piano competition.',
            'color': '#D4AF37',
            'category': 'arts'
        },
        {
            'title': 'National 1st Place | National HME Math Contest',
            'event': 'South Korea',
            'date': '2014. 05. 24.',
            'desc': 'Top 1% in South Korea and scored a perfect score.',
            'color': '#D4AF37',
            'category': 'math academic stem'
        },
        {
            'title': '3rd Place | Dental Health Awareness Art Contest',
            'event': 'Gwangju Dental Association',
            'date': '2013. 06. 11.',
            'desc': 'Awarded for creative work in the "Oral Health Awareness" category.',
            'color': '#D4AF37',
            'category': 'health arts'
        },
        {
            'title': "Special Merit Award | International Children's Art Grand Exhibition",
            'event': 'International Culture and Art Education Association',
            'date': '2011. 07. 04.',
            'desc': 'Awarded for exceptional creative vision.',
            'color': '#D4AF37',
            'category': 'arts'
        },
        {
            'title': "1st Place | 10th Children's Day Art Competition",
            'event': 'Kwangju Bank',
            'date': '2011. 05. 27.',
            'desc': 'Awarded the highest honor for exceptional creative expression among preschool participants.',
            'color': '#D4AF37',
            'category': 'arts'
        }
    ]

    certificates = [
        {
            'title': 'SPACE Certificate',
            'event': 'Dawson College',
            'date': 'Working on it',
            'desc': 'SPACE Certificate (Sciences Participating with Arts and Culture in Education).',
            'color': '#cbd5e1',
            'category': 'software hardware canada stem math'
        },
        {
            'title': 'Volunteered more than 100 hours',
            'event': 'Montreal',
            'date': 'Ongoing',
            'desc': '100+ hours of certified community service, demonstrating long-term civic commitment and leadership through various volunteer initiatives.',
            'color': '#D4AF37',
            'category': 'canada job'
        },
        {
            'title': 'Recognition of Student Involvement',
            'event': 'Dawson College',
            'date': 'Fall 2025',
            'desc': '60+ hours of contribution to the Dawson College community through active leadership and support in one semester.',
            'category': 'job canada'
        },
        {
            'title': 'Be There Certificate',
            'event': 'Online',
            'date': '2025. 08. 02.',
            'desc': 'Completed comprehensive mental health support training to better assist people in distress.',
            'category': 'health',
            'link_type': 'certificate',
            'link': "/static/BeThereCertificate.pdf"
        },        
        {
            'title': 'Engineering Intern',
            'event': 'GIO Engineering',
            'date': 'June 2025 - August 2025',
            'desc': 'I developed CAD files tailored for architectural projects which can serve as the foundational blueprints for design and construction phases.',
            'category': 'stem math job software'
        },
        {
            'title': "Dean's List",
            'event': 'Dawson College',
            'date': 'Fall 2024',
            'desc': 'Achieved an overall cumulative average of 85%+.',
            'color': '#D4AF37',
            'category': 'academic canada'
        },
        {
            'title': 'Recognition of Volunteerism from the Dean',
            'event': 'Dawson College',
            'date': '2024. 10. 20.',
            'desc': "Volunteered for Dawson's science open house event.",
            'category': 'job canada',
            'link': "/static/Volunteerism.pdf"
        },
        {
            'title': 'Peer Tutoring',
            'event': 'Rosemount High School',
            'date': 'February 2024 - June 2024',
            'desc': "Tutored math and science to peers.",
            'category': 'canada job stem math'
        },
        {
            'title': 'Music Award',
            'event': 'Rosemount High School',
            'date': '2023',
            'desc': "Won a highschool music award (trumpet).",
            'color': '#D4AF37',
            'category': 'canada arts'

        },
        {
            'title': 'Music Award',
            'event': 'Rosemount High School',
            'date': '2022',
            'desc': "Won a highschool music award (trumpet).",
            'color': '#D4AF37',
            'category': 'canada arts'

        },
        {
            'title': 'Junior Jazz Band',
            'event': 'Rosemount High School',
            'date': 'Fall 2021 - Winter 2022',
            'desc': "Part of the junior jazz band.",
            'category': 'canada arts'

        },
        {
            'title': 'Art-Études Program',
            'event': 'Rosemount High School',
            'date': 'Fall 2019 - Winter 2024',
            'desc': 'The Art-Études program is a specialized Quebec academic stream that compresses the standard curriculum into half-days to allow for intensive, professional-level training in the fine arts. It is designed for high-achieving students who possess the discipline to maintain top grades while dedicating significant daily hours to creative mastery and technical studio work.',
            'category': 'arts canada'
        },
        {
            'title': 'High honor or honor roll',
            'event': 'Rosemount High School',
            'date': 'Fall 2019 - Winter 2024',
            'desc': 'High honor or honor roll in high school every semester, demonstrating a high performance academically.',
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