from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from models import db, User, AttackLog, AIConversation
from ai_engine import DexterAI
from attack_engine import AttackEngine
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mahoraga-sila-divine-8-handled-sword'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize engines
ai_engine = DexterAI()
attack_engine = AttackEngine()

# Creator only - ABSOLUTE ACCESS
CREATOR_USERNAME = "DEXTER"

@app.before_first_request
def create_tables():
    db.create_all()
    # Create creator account
    creator = User.query.filter_by(username=CREATOR_USERNAME).first()
    if not creator:
        creator = User(
            username=CREATOR_USERNAME,
            is_creator=True,
            adaptation_level=99,
            wheel_rotation=999,
            message_count=0
        )
        db.session.add(creator)
        db.session.commit()

@app.route('/')
def index():
    username = request.args.get('user', '')
    return render_template('index.html', username=username)

@app.route('/api/init', methods=['POST'])
def init_user():
    data = request.json
    username = data.get('username', '').upper()
    
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(
            username=username,
            is_creator=(username == CREATOR_USERNAME),
            adaptation_level=1,
            wheel_rotation=0,
            message_count=0
        )
        db.session.add(user)
        db.session.commit()
    else:
        user.message_count += 1
        # Adaptation system - setiap 10 pesan naik level
        if user.message_count % 10 == 0 and user.adaptation_level < 5:
            user.adaptation_level += 1
            user.wheel_rotation += 1
        db.session.commit()
    
    # Update AI & Attack engine level
    ai_engine.set_adaptation_level(user.adaptation_level)
    attack_engine.set_adaptation_level(user.adaptation_level)
    
    return jsonify({
        "username": user.username,
        "is_creator": user.is_creator,
        "level": user.adaptation_level,
        "wheel": user.wheel_rotation,
        "messages": user.message_count
    })

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    username = data.get('username')
    prompt = data.get('prompt')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Generate AI response
    response = ai_engine.generate_response(prompt, username)
    
    # Save conversation
    conv = AIConversation(
        user_id=user.id,
        prompt=prompt,
        response=response
    )
    db.session.add(conv)
    db.session.commit()
    
    return jsonify({
        "response": response,
        "adaptation_level": user.adaptation_level
    })

@app.route('/api/attack/ddos', methods=['POST'])
def attack_ddos():
    data = request.json
    username = data.get('username')
    target = data.get('target')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Level requirement
    if user.adaptation_level < 1:
        return jsonify({"error": "Adaptasi level 1 diperlukan"}), 403
    
    result = attack_engine.ddos_attack(target)
    
    # Log attack
    log = AttackLog(
        user_id=user.id,
        attack_type="DDOS",
        target=target,
        status="success"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(result)

@app.route('/api/attack/otp', methods=['POST'])
def attack_otp():
    data = request.json
    username = data.get('username')
    phone = data.get('phone')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.adaptation_level < 1:
        return jsonify({"error": "Adaptasi level 1 diperlukan"}), 403
    
    result = attack_engine.otp_spam(phone)
    
    log = AttackLog(
        user_id=user.id,
        attack_type="OTP_SPAM",
        target=phone,
        status="success"
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(result)

@app.route('/api/attack/scan', methods=['POST'])
def attack_scan():
    data = request.json
    username = data.get('username')
    target = data.get('target')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.adaptation_level < 2:
        return jsonify({"error": "Adaptasi level 2 diperlukan"}), 403
    
    result = attack_engine.port_scan(target)
    return jsonify(result)

@app.route('/api/ai/analyze', methods=['POST'])
def ai_analyze():
    data = request.json
    username = data.get('username')
    target = data.get('target')
    
    user = User.query.filter_by(username=username).first()
    if user and user.is_creator:
        analysis = ai_engine.analyze_target(target)
        return jsonify({"analysis": analysis})
    return jsonify({"error": "Fitur hanya untuk creator"}), 403

@socketio.on('connect')
def handle_connect():
    emit('response', {'data': 'Wheel berputar. Mahoraga online.'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
