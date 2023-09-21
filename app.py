from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename #보안파일 가져오기 보안상 이유로 사용자에게 항목을 올바르게 업로드하도록 요청
#쉽게 해킹할 수 없도록 파일 이름을 보호해야함을 의미
#wsgi 호환 권한으로 작업
from main import getPrediction
import os

UPLOAD_FOLDER = 'static/images/' #업로드된 이미지 파일이 저장될 디렉토리를 지정

app = Flask(__name__, static_folder="static")

app.secret_key = "secret key" #보안 유지
#쿠키의 소유자에 의해 발행.
#해당 쿠키를 변경하도록 쿠키를 변경할 수 없습니다. 쿠키를 추가하는 전체 요점인 비밀 키를 알아야 합니다.

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #업로드 폴더를 앱으로 정의.

@app.route('/') #'/'결로에 접근했을 때 실행
def index():
    return render_template('index.html') #템플릿 렌더링

@app.route('/', methods=['POST']) #'/'경로에 요청이 들어왔을 때 실행되는 함수
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part') #메세지 저장 후
            return redirect(request.url)
        file = request.files['file'] #요청 도트 URL로 리디렉션을 반환
        if file.filename == '': #파일명이 공백이면 파일이 없다는 의미
            flash('No file selected for uploading') #업로드 파일 선택하지 않고 flash하면 됨
            return redirect(request.url) #해당 URL이 무엇이든 리디렉션 request.url을 반환합니다.
        if file: #해당 파일이 있는 경우 계속 진행하여 파일 이름을 가져옵니다.
            filename = secure_filename(file.filename)#file.filename이지만 암호화하거나 보안을 유지합니다.
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #파일을 로컬에 저장.
            #이름을 가져오고 해당 파일을 로컬에 저장하고 생성한다.
            #getPrediction(filename)
            # 실수였던 예측 파일 이름을 가져오는 것과 같기 때문에?
            label = getPrediction(filename) #예측 파일 이름을 가져오고 레이블을 플래시함
            flash(label) #파일 이름이 있는 경우 레이블
            #예측을 하고 이를 레이블과 플래시에 할당한다.
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename) #전체파일 이름 플래쉬
            #레이블을 알고 싶고, 파일 이름도 알고 싶기 때문에 flash 두 번 씀
            flash(full_filename)
            return redirect('/') #홈페이지로 리디렉션

        #홈페이지에 계속 머물면서 백엔드에 있는 메인 도트 파이와 상호 작용하고 있습니다.

if __name__ == "__main__": #이름이 도메인과 같다면 앱 실행
    app.run()