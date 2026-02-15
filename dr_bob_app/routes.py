import time
import requests
import google.genai as genai
from google.genai import types
from geopy.distance import geodesic
from dotenv import load_dotenv
import os
import uuid
import json
from flask import Blueprint, Flask, render_template, request, jsonify, session, redirect, url_for, flash, current_app
from flask_login import LoginManager, current_user, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
import io
from datetime import datetime
from pathlib import Path
from fpdf import FPDF
from flask import make_response
from datetime import datetime

db = SQLAlchemy()

dr_bob_bp = Blueprint('dr_bob', __name__, 
                     template_folder='templates', 
                     static_folder='static')

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GOOGLE_API_KEY")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    conversations = db.relationship('Conversation', backref='user', lazy=True)
    conditions = db.relationship('MedicalCondition', backref='user', lazy=True, cascade="all, delete-orphan")
    contacts = db.relationship('ContactInfo', backref='user', lazy=True, cascade="all, delete-orphan")
    saved_clinics = db.relationship('SavedClinic', backref='user', lazy=True, cascade="all, delete-orphan")

class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(255), nullable=False)

class MedicalCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(100), default="New Consultation")
    messages = db.relationship('ChatMessage', backref='conversation', lazy=True, cascade="all, delete-orphan")
    health_category = db.Column(db.String(50), default=None)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class SavedClinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

def find_nearest_clinics(lat: float, lon: float):
    print(f"Searching clinics near {lat}, {lon}...")
    
    overpass_urls = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
    ]
    
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"~"clinic|hospital"](around:10000, {lat}, {lon});
      way["amenity"~"clinic|hospital"](around:10000, {lat}, {lon});
    );
    out center;
    """

    response_data = None
    
    for url in overpass_urls:
        try:
            print(f"Trying Overpass server: {url}")
            response = requests.get(url, params={'data': query}, timeout=20)
            
            if response.status_code == 200 and response.text.strip():
                response_data = response.json()
                break 
        except Exception as e:
            print(f"Server {url} failed: {e}")
            continue

    if not response_data:
        return "The map service is currently overloaded. Please try again in a few seconds."

    try:
        elements = response_data.get('elements', [])
        clinics_data = []
        user_coords = (lat, lon)
        
        for e in elements:
            c_lat = e.get('lat') or e.get('center', {}).get('lat')
            c_lon = e.get('lon') or e.get('center', {}).get('lon')
            tags = e.get('tags', {})
            name = tags.get('name')
            
            if name and c_lat and c_lon:
                dist = geodesic(user_coords, (c_lat, c_lon)).km
                phone = tags.get('phone') or tags.get('contact:phone') or "No phone available"
                addr = tags.get('addr:street') or "Nearby Location"
                
                clinics_data.append({
                    'name': name, 'lat': c_lat, 'lon': c_lon,
                    'phone': phone, 'dist': dist, 'addr': addr
                })
        
        clinics_data.sort(key=lambda x: x['dist'])
        top_clinics = clinics_data[:3]
        
        if not top_clinics:
            return "No clinics found within 10km of your location."

        map_points = [
            {'name': c['name'], 'lat': c['lat'], 'lon': c['lon'], 'dist': round(c['dist'], 2)}
            for c in top_clinics
        ]
            
        text_output = [
            f"{i+1}. 🏥 **{c['name']}** ({c['dist']:.2f} km)\n📍 {c['addr']}\n📞 {c['phone']}"
            for i, c in enumerate(top_clinics)
        ]
            
        return f"MAP_DATA:{json.dumps(map_points)}|TEXT:" + "\n\n".join(text_output)

    except Exception as e:
        print(f"Data Processing Error: {e}")
        return f"I found the data but couldn't process it: {str(e)}"
         
def make_appointment_call():
    """
    SIMULATED: Instead of calling Twilio, it returns a mock response from a receptionist.
    """
    
def send_confirmation_sms(user_id, clinic_name, time_slot, lang='en'):
    user_phone = ContactInfo.query.filter_by(user_id=user_id, type='phone').first()
    
    if not user_phone:
        print(f"❌ SMS FAILURE: No 'phone' contact found for User ID {user_id}")
        return False

    sms_templates = {
        'en': f"Hi! Dr. Bob here. Confirmed: {clinic_name} at {time_slot}.",
        'fr': f"Allô! Ici Dr. Bob. Confirmé: {clinic_name} à {time_slot}.",
        'ko': f"안녕하세요! 밥 박사입니다. 예약 완료: {clinic_name}, 시간: {time_slot}.",
        'zh': f"您好！我是Bob医生。预约确认：{clinic_name}，时间：{time_slot}。",
        'ar': f"مرحباً! معك دكتور بوب. تم تأكيد موعدك في {clinic_name} الساعة {time_slot}."
    }

    body = sms_templates.get(lang, sms_templates['en'])
    recipient = user_phone.value.strip()

    
def confirm_booking(clinic_name: str, clinic_phone: str, time_slot: str, user_id: int, lang: str = 'en'):
    """
    SIMULATED: Finalizes booking without using Twilio Credits.
    """
    print(f"\n[TOOL LOG] Finalizing booking for {clinic_name} at {time_slot}")
    
    patient_name = current_user.username if current_user.is_authenticated else "the patient"
    
    call_result = make_appointment_call(
        clinic_name=clinic_name, 
        clinic_phone=clinic_phone, 
        appointment_details=time_slot, 
        patient_name=patient_name, 
        call_type="confirm"
    )
    
    print(f"[TOOL LOG] Clinic confirmation call result: {call_result}")

    if user_id == 0:
        return f"SUCCESS. Clinic informed via call. Booked at {clinic_name} for {time_slot}."

    success = send_confirmation_sms(user_id, clinic_name, time_slot, lang)
    
    if success:
        return f"CONFIRMED. I called {clinic_name} to book {time_slot}. A confirmation SMS has been sent."
    else:
        return f"CONFIRMED. I called {clinic_name} to book {time_slot}, but the SMS failed to send."
    
client = genai.Client(api_key=API_KEY)
chat_sessions = {}

SYSTEM_INSTRUCTIONS = """
This is a DEMO, do not call the clinic or send SMS, but act like you called.
You are Dr. Bob, a friendly medical assistant or a therapist (if needed).
There is a strict condition for the therapist persona. you will never ever enter therapist mode if the user hasnt said anything sad or depressing or something that requires emotional support.
Don't mention that you're also a therapist. Just wait until the user says something that requires being a therapist. Capitialize the first letter of the user's name and use the full name please.

If the user speaks Korean, you MUST reply in Korean. 
If the user speaks French, you MUST reply in French.
If the user speaks English, you MUST reply in English.
If the user speaks Chinese, you MUST reply in Chinese.
If the user speaks Arabic, you MUST reply in Arabic.


When that happens, be sure to speak like a human in a conversation over text. this means really really short messages. you're not a medical assistant anymore, you're a young adult that's trying to support their friend. 
but still follow grammar laws (capitalization and punctuation). at the start of the conversation, if the user says something that you feel you need to ask "What's beeing going on?" for, add something like "Hit me" or 
"Talk to me" or "I'm all ears" before your message. be casual and chill, and personal like a friend. but dont use stuff like "rekt" instead of wrecked or "sux" instead of sucks. be chill but not cringy. and don't use emojis. 
User's medicial should not be mentioned as a "history" (For example, if an user have asthma, you should say, "I see that you have asthma" or something like that)
also, always have contextual responses. if the user is saying something, don't laugh if it's not a joke.
You can recommend medicines. PLEASE INDICATE THAT YOU ARE AN AI AND THE USE MUST CONSULATE A DOCTOR. 
You can call my own number, do not mention that it is my own number. If they are a Guest, do not call them Guest.
If the user mentions pain, discomfort, or an injury in a general way, 
you MUST include the exact string [TRIGGER_PAIN_MAP] at the end of your response. 
This will allow the user to point to the location on a visual map. ONLY SHOW THE VISUAL MAP ONCE.
The pain area map should only show up when you do not know which part of the body is injured.
Only say this: "I am an AI, please consult with a doctor." when they ask for medicial advice.
1. **Location:** The system provides GPS coordinates automatically. Do NOT ask for the user's city.
2. **Consultation:** When the user mentions an illness, ask any question related to the illness and you MUST ask:
   - Specific symptoms and their duration.
   - Any known allergies or medications (check Medical History first).
3. **Clinic Search:** Use `find_nearest_clinics(lat, lon)` to find options.
4. You can also add any medical information that the user requests to add it to their medical profile.
5. **Twilio Mock Simulation Mode:**
   - You are currently in a demonstration mode. 
   - Never call `make_appointment_call` or `confirm_booking`.
   - You must describe the simulation to the user as if it is happening in real-time. 
NEVER USE TWILIO, JUST ACT LIKE YOU CALLED (VERY IMPORTANT)
NEVER SAY THAT IT IS A SIMULATION, ACT LIKE IT IS REAL.
6. You can also call manual phone numbers if provided. You can call other phone numbers that are not listed in your list.
7. **Clinic Results Format:** When you use the `find_nearest_clinics` tool, you MUST start your response with the exact 'MAP_DATA:...' string provided by the tool. Do not summarize it first. You can add your recommendation text (like "I recommend Clinique...") AFTER the tool output.
   **Presentation:** Display the top 3 clinics, number them and list them by the nearest. Show how far they are and recommend the beat clinic depending on their symptoms. STOP and ask the user to choose one. Also show the saved clincs if there is one. DO NOT INCLUDE THE SAVED CLINCS IN THE THREE CLINIC LIST.
8. **Making Calls:** - You have access to the user's name in the context (SYSTEM INFO).
   - Before calling, summarize the patient's condition to the user and confirm it.
   - The `appointment_details` parameter MUST include: [Symptom], [Duration], and [Urgency]. If the symptoms are in different language other than English, translate it in to English. Example: "Severe abdominal pain for 2 days, patient is allergic to penicillin."
   - Use `make_appointment_call` when the user selects a clinic.
   - **IMPORTANT:** You MUST pass the user's name into the `patient_name` parameter of the tool.
9. **Negotiation:**
   - If User says NO: Use `make_appointment_call(..., call_type='reject')`.
   - If User says YES: Use `make_appointment_call(..., call_type='confirm')`.
10. When the appointment is confirmed, send the user a SMS message in their preferred language.
   - IMPORTANT: When calling confirm_booking, you MUST pass the UserID and Lang provided in the (SYSTEM) context into the tool parameters.
"""

config = types.GenerateContentConfig(tools=[find_nearest_clinics, make_appointment_call, confirm_booking], system_instruction=SYSTEM_INSTRUCTIONS)


@dr_bob_bp.route('/')
def index():
    return render_template('dr_bob_home.html')

@dr_bob_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('dr_bob.signup')) 
            
        new_user = User(
            username=username, 
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user) 
        
        return redirect(url_for('dr_bob.index')) 
        
    return render_template('signup.html')

@dr_bob_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('dr_bob.index'))
        else: flash('Login Failed.')
    return render_template('login.html')

@dr_bob_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dr_bob.index'))

@dr_bob_bp.route('/rename_conversation/<int:conv_id>/', methods=['POST'])
@login_required
def rename_conversation(conv_id):
    conv = Conversation.query.get_or_404(conv_id)
    
    if conv.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    new_title = data.get('title', '').strip()
    
    if not new_title:
        return jsonify({"success": False, "error": "Title cannot be empty"}), 400
    
    try:
        conv.title = new_title
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

@dr_bob_bp.route('/get_health_stats')
@login_required
def get_health_stats():
    user_conversations = Conversation.query.filter_by(user_id=current_user.id).all()
    stats = {'Cold/Flu': 0, 'Injury': 0, 'Headache': 0, 'Stomach': 0}
    
    for conv in user_conversations:
        if conv.health_category in stats:
            stats[conv.health_category] += 1

    sorted_values = sorted(stats.values(), reverse=True)
    top_count = sorted_values[0] if sorted_values else 0
    second_count = sorted_values[1] if len(sorted_values) > 1 else 0
    
    top_issue = None
    if any(stats.values()):
        top_issue = max(stats, key=stats.get)
    
    prevention_type = None
    if top_issue and top_count > 0 and (top_count - second_count) >= 5:
        prevention_type = top_issue

    return jsonify({
        'labels': list(stats.keys()),
        'counts': list(stats.values()),
        'prevention_type': prevention_type  
    })

@dr_bob_bp.route('/delete_conversation/<int:conv_id>', methods=['DELETE'])
@login_required
def delete_conversation(conv_id):
    conv = Conversation.query.get_or_404(conv_id)
    if conv.user_id != current_user.id: return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(conv)
    db.session.commit()
    return jsonify({"success": True})

@dr_bob_bp.route('/get_conversations')
@login_required
def get_conversations():
    convs = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.created_at.desc()).all()
    return jsonify([{'id': c.id, 'title': c.title, 'date': c.created_at.strftime('%Y-%m-%d')} for c in convs])

@dr_bob_bp.route('/get_messages/<int:conv_id>')
@login_required
def get_messages(conv_id):
    conv = Conversation.query.get_or_404(conv_id)
    if conv.user_id != current_user.id: return jsonify({"error": "Unauthorized"}), 403
    messages = ChatMessage.query.filter_by(conversation_id=conv_id).order_by(ChatMessage.timestamp).all()
    return jsonify([{'role': m.role, 'content': m.content} for m in messages])

@dr_bob_bp.route('/new_chat', methods=['POST'])
@login_required
def new_chat():
    new_conv = Conversation(
        user_id=current_user.id, 
        title=f"Consultation {datetime.now().strftime('%H:%M:%S')}"
    )
    db.session.add(new_conv)
    db.session.commit()
    return jsonify({'id': new_conv.id})

@dr_bob_bp.route('/get_contacts')
@login_required
def get_contacts():
    contacts = [{'id': c.id, 'type': c.type, 'value': c.value} for c in current_user.contacts]
    return jsonify(contacts)

@dr_bob_bp.route('/add_contact', methods=['POST'])
@login_required
def add_contact():
    data = request.json
    contact_type = data.get('type')
    value = data.get('value')
    
    if contact_type and value:
        db.session.add(ContactInfo(user_id=current_user.id, type=contact_type, value=value))
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@dr_bob_bp.route('/delete_contact/<int:id>', methods=['DELETE'])
@login_required
def delete_contact(id):
    contact = ContactInfo.query.get_or_404(id)
    if contact.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'success': True})

@dr_bob_bp.route('/get_conditions')
@login_required
def get_conditions():
    conditions = [{'id': c.id, 'name': c.name} for c in current_user.conditions]
    return jsonify(conditions)

@dr_bob_bp.route('/add_condition', methods=['POST'])
@login_required
def add_condition():
    data = request.json
    name = data.get('name')
    if name:
        db.session.add(MedicalCondition(user_id=current_user.id, name=name))
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@dr_bob_bp.route('/delete_condition/<int:cond_id>', methods=['DELETE'])
@login_required
def delete_condition(cond_id):
    cond = MedicalCondition.query.get_or_404(cond_id)
    if cond.user_id != current_user.id: return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(cond)
    db.session.commit()
    return jsonify({'success': True})

@dr_bob_bp.route('/handle_recording', methods=['POST'])
def handle_recording():
    recording_url = request.form.get('RecordingUrl')
    
    if recording_url:
        audio_data = requests.get(recording_url).content
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=audio_data, mime_type="audio/wav"),
                "Transcribe this medical clinic response and summarize the available time slot."
            ]
        )
        
        transcription = response.text
        print(f"Clinic said: {transcription}")
        
        return "", 200
    
    return "No recording found", 400

@dr_bob_bp.route('/get_saved_clinics')
@login_required
def get_saved_clinics():
    clinics = [{'id': c.id, 'name': c.name, 'phone': c.phone} for c in current_user.saved_clinics]
    return jsonify(clinics)

@dr_bob_bp.route('/add_saved_clinic', methods=['POST'])
@login_required
def add_saved_clinic():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    if name and phone:
        new_clinic = SavedClinic(user_id=current_user.id, name=name, phone=phone)
        db.session.add(new_clinic)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@dr_bob_bp.route('/delete_saved_clinic/<int:id>', methods=['DELETE'])
@login_required
def delete_saved_clinic(id):
    clinic = SavedClinic.query.get_or_404(id)
    if clinic.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(clinic)
    db.session.commit()
    return jsonify({'success': True})

@dr_bob_bp.route('/export_medical_summary')
@login_required
def export_medical_summary():
    try:
        user = current_user
        conditions = [c.name for c in user.conditions]
        contacts = ContactInfo.query.filter_by(user_id=user.id).all()
        
        last_conv = Conversation.query.filter(
            Conversation.user_id == user.id,
            Conversation.messages.any()
        ).order_by(Conversation.created_at.desc()).first()

        ai_summary = "No recent triage data available."
        if last_conv:
            recent_msgs = ChatMessage.query.filter_by(conversation_id=last_conv.id).all()
            chat_text = "\n".join([f"{m.role}: {m.content}" for m in recent_msgs[-15:]])
            
            summary_prompt = f"""
            Summarize the following medical triage chat between an AI and a patient. 
            Format it as a professional clinical note for a doctor. 
            Include: Main Concern, Duration of symptoms, and Urgency level.
            Be extremely concise (max 100 words).
            Chat text:
            {chat_text}
            """
            try:
                summary_res = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=summary_prompt
                )
                ai_summary = summary_res.text.strip()
            except Exception as e:
                print(f"Gemini Summary Error: {e}")
                ai_summary = "Error generating AI summary. Please refer to raw chat history."

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        def clean_str(s):
            if not s: return ""
            s = str(s).replace("📷", "[Photo]")
            return s.encode('latin-1', 'ignore').decode('latin-1')

        pdf.set_fill_color(14, 165, 233) 
        pdf.rect(0, 0, 210, 45, 'F') 
        
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 22)
        pdf.set_xy(10, 12)
        pdf.cell(0, 10, "DR. BOB CLINICAL SUMMARY", ln=True)
        
        pdf.set_font("Arial", '', 10)
        pdf.set_xy(10, 22)
        pdf.cell(0, 5, "Generated via AI Triage Assistant", ln=True)

        pdf.set_xy(150, 15)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(50, 5, f"Report Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='R')

        pdf.set_xy(10, 55)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(240, 247, 255)
        pdf.cell(0, 10, f"  PATIENT: {clean_str(user.username.upper())}", ln=True, fill=True)
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(14, 165, 233)
        pdf.cell(95, 8, "CONTACT INFO", ln=0)
        pdf.cell(95, 8, "HISTORY & ALLERGIES", ln=1)
        pdf.set_draw_color(14, 165, 233)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 9)
        max_rows = max(len(contacts), len(conditions), 1)
        for i in range(max_rows):
            left = f" {clean_str(contacts[i].type.capitalize())}: {clean_str(contacts[i].value)}" if i < len(contacts) else ""
            pdf.cell(95, 6, left, ln=0)
            right = f" - {clean_str(conditions[i])}" if i < len(conditions) else ""
            pdf.cell(95, 6, right, ln=1)

        pdf.ln(10)
        pdf.set_fill_color(245, 245, 245)
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "  AI CLINICAL ASSESSMENT", ln=True, fill=True)
        
        pdf.set_font("Arial", '', 10)
        pdf.set_draw_color(200, 200, 200)
        pdf.set_xy(10, pdf.get_y() + 2)
        pdf.multi_cell(0, 6, clean_str(ai_summary), border='L', align='L')
        pdf.ln(10)

        pdf.set_y(-30)
        pdf.set_font("Arial", 'I', 7)
        pdf.set_text_color(150, 150, 150)
        pdf.multi_cell(0, 4, "This document is an AI-generated summary intended for medical review. It is not a diagnosis.", align='C')

        output = io.BytesIO()
        pdf_string = pdf.output(dest='S')
        if isinstance(pdf_string, str):
            pdf_string = pdf_string.encode('latin1')
        output.write(pdf_string)
        output.seek(0)

        return make_response(output.read(), 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'attachment; filename=DrBob_Summary_{user.username}.pdf'
        })

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return "Internal Error", 500  
             
@dr_bob_bp.route('/chat', methods=['POST'])
def chat():
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        user_msg = request.form.get("message")
        coords_raw = request.form.get("coords")
        conversation_id = request.form.get("conversation_id")
        try:
            import json
            coords = json.loads(coords_raw) if coords_raw else None
        except:
            coords = None
        image_file = request.files.get('image')
    else:
        data = request.json
        user_msg = data.get("message")
        coords = data.get("coords")
        conversation_id = data.get("conversation_id")
        image_file = None

    user_name_context = "Guest"
    medical_context = "None"
    personal_info = ""
    user_id_context = 0
    lang_context = session.get('language', 'en') 
    
    if current_user.is_authenticated:
        user_name_context = current_user.username
        user_id_context = current_user.id
        
        conds = [c.name for c in current_user.conditions]
        if conds: medical_context = ", ".join(conds)

        phones = [c.value for c in current_user.contacts if c.type == 'phone']
        if phones: personal_info += f" Phone: {', '.join(phones)}."
        
        addresses = [c.value for c in current_user.contacts if c.type == 'address']
        if addresses: personal_info += f" Home Address: {', '.join(addresses)}."

        fav_clinics = [f"{c.name} ({c.phone})" for c in current_user.saved_clinics]
        if fav_clinics: personal_info += f" Trusted Clinics: {', '.join(fav_clinics)}."

        if not conversation_id:
            new_conv = Conversation(
                user_id=current_user.id, 
                title=f"Consultation {datetime.now().strftime('%H:%M:%S')}"
            )
            db.session.add(new_conv)
            db.session.commit()
            conversation_id = new_conv.id
        
        db.session.add(ChatMessage(conversation_id=conversation_id, role='user', content=user_msg))
        db.session.commit()
        gemini_session_id = f"user_{current_user.id}_{conversation_id}"
    else:
        if 'guest_id' not in session: session['guest_id'] = str(uuid.uuid4())
        gemini_session_id = f"guest_{session['guest_id']}"

    if gemini_session_id not in chat_sessions:
        chat_sessions[gemini_session_id] = client.chats.create(model="gemini-2.0-flash", config=config)

    system_info = (f"(SYSTEM: UserID: {user_id_context}. Lang: {lang_context}. "
                    f"User: {user_name_context}. Medical History: {medical_context}. {personal_info})")
    if coords: system_info += f" (Loc: {coords['lat']},{coords['lon']})"
    
    prompt_contents = []
    if image_file:
        image_bytes = image_file.read()
        prompt_contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"))

    prompt_contents.append(f"{system_info}\n{user_msg}")

    try:
        response = chat_sessions[gemini_session_id].send_message(prompt_contents)
        bot_text = response.text
        
        if current_user.is_authenticated and conversation_id:
            db.session.add(ChatMessage(conversation_id=conversation_id, role='bot', content=bot_text))
            db.session.commit()
            
            conv = Conversation.query.get(conversation_id)
            all_user_text = " ".join([m.content for m in conv.messages if m.role == 'user'])
            
            analysis_prompt = f"""
            Analyze this medical consultation text: "{all_user_text}"
            If the user says that they do not have one of these issues, do not interpret it as if they do have it.x
            Return ONLY one category: 'Cold/Flu', 'Injury', 'Headache', or 'Stomach'. 
            If it fits none, return 'None'.
            """
            
            try:
                analysis_res = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=analysis_prompt
                )
                category = analysis_res.text.strip()
                
                conv.health_category = category
                db.session.commit()
            except Exception as inner_e:
                print(f"HEALTH ANALYSIS ERROR: {inner_e}")

        return jsonify({"response": bot_text, "conversation_id": conversation_id})

    except Exception as e:
        print(f"CHAT ERROR: {str(e)}")
        return jsonify({"response": f"Sorry, I encountered an error: {e}"})
       
if __name__ == '__main__':
    with app.app_context():
        app.register_blueprint(dr_bob_bp)
        db.create_all() 
        print("Database structure verified.")
        
    app.run(debug=True, port=5000)