import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask, render_template, abort

app = Flask(__name__, template_folder='../templates', static_folder='../static')


PROJECTS = [
    {
        'id': 'dr-bob',
        'title': 'Dr. Bob',
        'award': '2nd Place: Dialogue Challenge at ConUHacks', 
        'category': 'Hackathon 2026',
        'description': 'Medical triage assistant using Flask and Twilio for patient communication.',
        'full_story': 'Developed at a hackathon, Dr. Bob uses Twilio to automate patient intake and history tracking, ensuring medical data is organized for doctors.',
        'tech': ['Python', 'JS', 'SQLite', 'Twilio API', 'Gemini API', 'Web Speech API', 'Geolocation API'],
        'collaborators': ['Oliver']

    },
    {
        'id': 'j-score',
        'title': 'J-Score Calculator',
        'category': 'School Project 2025',
        'description': 'A precision tool for calculating academic standing (r-score) using standard deviation.',
        'tech': ['Python', 'JS', 'CSV'],
        'collaborators': ['James']
    }
]


@app.route('/')
def home():
    return render_template('index.html', projects=PROJECTS)


@app.route('/achievements')
def achievements():
    competitions = [
        {
            'title': 'Will Participate: DawsHacks',
            'event': 'Dawson College',
            'date': '2026. 05. 02.',
            'desc': 'Will do something...',
            'color': '#cbd5e1',
            'category': 'software canada stem'
        },
        {
            'title': 'Will Participate: MariHacks',
            'event': 'Marianopolis College',
            'date': '2026. 04. 17. - 2026. 04. 18.',
            'desc': 'Will do something...',
            'color': '#cbd5e1',
            'category': 'software canada stem'

        },
        {
            'title': 'Will Participate: JacHacks',
            'event': 'John Abbott College',
            'date': '2026. 04. 11. - 2026. 04. 12.',
            'desc': 'Will do something...',
            'color': '#cbd5e1',
            'category': 'software canada stem'
        },
        {
            'title': 'Will Participate: VanierHacks!',
            'event': 'Vanier College',
            'date': '2026. 03. 21. - 2026. 03. 22.',
            'desc': 'Will do something...',
            'color': '#cbd5e1',
            'category': 'software canada stem'
        },
        {
            'title': 'Will Participate: McGill AeroHacks',
            'event': 'McGill University',
            'date': '2026. 03. 13. - 2026. 03. 15.',
            'desc': 'Will do something...',
            'color': '#cbd5e1',
            'category': 'software hardware canada stem'
        },
        {
            'title': 'Will Participate: UdeM Hacks',
            'event': 'University of Montreal',
            'date': '2026. 03. 07. - 2026. 03. 08.',
            'desc': 'Will do something...',
            'color': '#cbd5e1',
            'category': 'software canada stem'
        },
        {
            'title': 'Participated: Dialogue Employees Hackathon',
            'event': 'Dialogue Health Technologies Inc',
            'date': '2026. 02. 12. - 2026. 02. 13.',
            'desc': 'Got invited to their internal hackathon and integrated a skin analysis feature into the Dialogue application, enabling users to receive automated health assessments.',
            'category': 'software health API canada stem'
        },
        {
            'title': '2nd Place: Dialogue Challenge at ConUHacks X',
            'event': 'Concordia University',
            'date': '2026. 01. 24. - 2026. 01. 25.',
            'desc': "Competed in Quebec's largest 24 hour hackathon and developed 'Dr. Bob', an AI medical assistant using Python and Gemini API for symptom analysis and a chatbot system. Integrated Leaflet.js and Geolocation APIs to provide real-time location tracking, enabling users to instantly find the nearest clinics.",
            'color': '#D4AF37',
            'category': 'software health API canada stem'
        },
        {
            'title': 'Best Use of Gemini API: HackDécouverte',
            'event': 'Concordia University',
            'date': '2025. 11. 29.',
            'desc': "Developed 'BudgetX', an AI budeting website using Gemini API and others.",
            'color': '#D4AF37',
            'category': 'software API canada stem'
        },
        {
            'title': '2nd Place: Dawson Robotics Hackathon',
            'event': 'Dawson College',
            'date': '2025. 05. 09.',
            'desc': 'Built and programmed autonomous black line following robotic system and IR remoted control functionality using C++ and the Arduino framework.',
            'color': '#D4AF37',
            'category': 'software hardware canada stem'
        },
        {
            'title': 'Participated: Dawson Science On Tourne',
            'event': 'Dawson College',
            'date': '2025. 04. 04.',
            'desc': 'Made a drone using 3D printers.',
            'category': 'software hardware canada stem'
        },
        {
            'title': 'School Champion: Waterloo Cayley Math Contest',
            'event': 'International',
            'date': '2022. 02. 22.',
            'desc': 'Top 25% in the world and school champion.',
            'color': '#D4AF37',
            'category': 'math academic canada stem'
        },
        {
            'title': "Honorable Mention: 'Bright Society' Creative Writing Contest",
            'event': 'Ministry of Justice of the Republic of Korea',
            'date': '2016. 07. 07.',
            'desc': 'Recognized by the Ministry of Justice for an essay on social ethics and civic values, demonstrating strong communication skills and a deep understanding of community justice.',
            'color': '#D4AF37',
            'category': 'arts'
        },
        {
            'title': 'Honors: National HME Math Contest',
            'event': 'South Korea',
            'date': '2016. 06. 08.',
            'desc': 'Recognized for outstanding mathematical logic and problem-solving skills at a national level.',
            'color': '#D4AF37',
            'category': 'math academic stem'
        },
        {
            'title': 'National 1st Place: National HME Math Contest',
            'event': 'South Korea',
            'date': '2014. 05. 24.',
            'desc': 'Top 1% in South Korea and scored a perfect score.',
            'color': '#D4AF37',
            'category': 'math academic stem'
        },
        {
            'title': '3rd Place: Dental Health Awareness Art Contest',
            'event': 'Gwangju Dental Association',
            'date': '2013. 06. 11.',
            'desc': 'Awarded for creative work in the "Oral Health Awareness" category.',
            'color': '#D4AF37',
            'category': 'health arts'
        },
        {
            'title': "Special Merit Award: International Children's Art Grand Exhibition",
            'event': 'International Culture and Art Education Association',
            'date': '2011. 07. 04.',
            'desc': 'Awarded for exceptional creative vision.',
            'color': '#D4AF37',
            'category': 'arts'
        },
        {
            'title': "1st Place: 10th Children's Day Art Competition",
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
            'category': 'software hardware canada stem'
        },
        {
            'title': 'Volunteered more than 100 hours',
            'event': 'Montreal',
            'date': 'Ongoing',
            'desc': '100+ hours of certified community service, demonstrating long-term civic commitment and leadership through various volunteer initiatives.',
            'color': '#D4AF37',
            'category': 'volunteering canada'
        },
        {
            'title': 'Recognition of Student Involvement',
            'event': 'Dawson College',
            'date': 'Fall 2025',
            'desc': '60+ hours of contribution to the Dawson College community through active leadership and support in one semester.',
            'category': 'volunteering canada'
        },
        {
            'title': 'Be There Certificate',
            'event': 'Online',
            'date': '2025. 08. 02.',
            'desc': 'Completed comprehensive mental health support training to better assist people in distress.',
            'category': 'health'
        },        
        {
            'title': 'Member of Dawson Graph Theory Research Team',
            'event': 'Dawson College',
            'date': 'Winter 2025',
            'desc': 'Did research on graph theory.',
            'category': 'stem math canada'
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
            'category': 'volunteering canada'
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
            'desc': 'High honor or honor roll in high school every semester.',
            'color': '#D4AF37',
            'category': 'academic canada'
        }
    ]
    return render_template('achievements.html', competitions=competitions, certificates=certificates)

if __name__ == '__main__':
    app.run(debug=True)