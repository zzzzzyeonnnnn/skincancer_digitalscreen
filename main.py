import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model

def getPrediction(filename):
    #클래스 레이블 정의
    classes = ['Actinic keratoses', 'Basal cell carcinoma',
               'Benign keratosis-like', 'Dermatofibroma', 'Melanoma',
               'Melanocytic nevi', 'Vascular lesions']

    #LabelEncoder를 사용해 클래스 레이블을 숫자로 인코딩
    le = LabelEncoder()
    le.fit(classes)
    le.inverse_transform([2])

    #load model
    my_model=load_model("model/HAM10000_epoch100.h5")

    SIZE = 32 #크기 정의
    img_path = 'static/images/' + filename #이미지 경우, 사용자가 업로드 하는 경로
    img = np.asarray(Image.open(img_path).resize((SIZE, SIZE))) #넘파이 배열로 반환

    img = img/255. #정규화

    img = np.expand_dims(img, axis=0) #치수를 오른쪽으로 확장

    pred = my_model.predict(img) #모델을 사용해서 이미지 진단 예측

    pred_class = le.inverse_transform([np.argmax(pred)])[0] #예측 결과를 역변환해서 클래스를 가져옴
    print('Diagnosis is: ', pred_class) #에측 진단값
    return pred_class

#test_prediction = getPrediction('example.jpg')

