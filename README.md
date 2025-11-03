# final_please
CNSA 11th

app.py : plask 앱 메인 파일
db_models.py : DB 테이블 정의(SQLAlchemy ORM)
config.oy : DB 연결 설정 등 환경 변수
templates/ : HTML 파일들
static/ : CSS. JS, 이미지 등
requirements.txt : 패키지 목록

# DB 제작 완료
1. PostgreSQL에서 DB 생성
code :
    createdb music_recommender
2. 필요한 패키지 설치
code :
    pip install flask psycopg2-binary flask_sqlalchemy
3. Flask 실행
code : 
    python app.py
4. 브라우저에서 확인
    http://~~~~~