from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from db_models import db, User

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config.get('SECRET_KEY', 'dev_secret')  # 세션용 비밀키 설정

# DB 초기화
db.init_app(app)

# ---------------------- 기본 라우트 ----------------------

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return f"🎵 안녕하세요, {user.name}님! 음악 추천 시스템에 오신 것을 환영합니다."
    return redirect(url_for('login_page'))

# ---------------------- 회원가입 / 로그인 ----------------------

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# 회원가입 API
@app.route('/api/signup', methods=['POST'])
def signup_api():
    data = request.get_json()
    name = data.get('name')
    password = generate_password_hash(data.get('password'))
    gender = data.get('gender')
    age = data.get('age')
    preferred_genre = data.get('preferred_genre')

    if User.query.filter_by(name=name).first():
        return jsonify({'success': False, 'message': '이미 존재하는 이름입니다.'}), 400

    new_user = User(name=name, gender=gender, age=age,
                    preferred_genre=preferred_genre, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': True})

# 로그인 API
@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    user = User.query.filter_by(name=name).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': '아이디 또는 비밀번호가 올바르지 않습니다.'}), 401

    session['user_id'] = user.user_id
    return jsonify({'success': True})

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login_page'))

# ---------------------- 앱 실행 ----------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 테이블 생성
    app.run(debug=True)
