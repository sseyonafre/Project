from flask import Flask, render_template, request
import pickle
import pandas as pd
import jwt
import time
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html'), 200

@app.route('/stat')
def stat():
    load_dotenv()
    METABASE_URL = str(os.environ.get('METABASEURL'))
    METABASE_SECRET_KEY = str(os.environ.get('METABASEKEY'))

    payload = {
      "resource": {"dashboard": 1},
      "params": {
    
      },
      "exp": round(time.time()) + (60 * 10) # 10 minute expiration
        }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl = METABASE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"
    
    return render_template('stat.html',iframeUrl=iframeUrl), 200


@app.route('/user',methods=['GET', 'POST'])
def user(age=None):
    if request.method == 'GET':
        temp = request.args.get('model')
        if temp == '노인':
            return render_template('senior.html',age=temp), 200

        elif temp == '성인':
            return render_template('middle.html',age=temp), 200
        
        elif temp == '청소년':
            return render_template('youth.html',age=temp), 200    
        
        elif temp == '유소년':
            return render_template('underaged.html',age=temp), 200

    if request.method == 'POST':
        temp = request.args.get('model')            
        if temp == '노인':
            with open('senior.pickle','rb') as pickle_file:
                model = pickle.load(pickle_file)
                def predict_grade(ageClass, ageDegree, height, weight, trunkFlexion, BMI, standsit, twominwalk, threeMwalk):
                    df = pd.DataFrame(
                    data=[[ageClass, ageDegree, height, weight, trunkFlexion, BMI, standsit, twominwalk, threeMwalk]], 
                    columns=['ageClass', 'ageDegree', 'height', 'weight', 'trunkFlexion', 'BMI', 'standsit', 'twominwalk', 'threeMwalk']
                    )
                    pred = model.predict(df)[0]

                    return pred
        
            
            data2 = request.form['ageDegree']
            data1 = (int(data2)//10)*10
            data3 = request.form['height']
            data4 = request.form['weight']
            data5 = request.form['trunkFlexion']
            data6 = int(data4) / (int(data3) *0.01)**2
            data7 = request.form['standsit']
            data8 = request.form['twominwalk']
            data9 = request.form['threeMwalk']

            result = predict_grade(data1, data2, data3, data4, data5, data6, data7, data8, data9)

            return render_template('result.html', result=result)
        elif temp == '성인':
            with open('middle.pickle','rb') as pickle_file:
                model = pickle.load(pickle_file)
                def predict_grade(ageClass, ageDegree, height, weight, trunkFlexion, BMI, situp, standinglongjump):
                    df = pd.DataFrame(
                    data=[[ageClass, ageDegree, height, weight, trunkFlexion, BMI, situp, standinglongjump]], 
                    columns=['ageClass', 'ageDegree', 'height', 'weight', 'trunkFlexion', 'BMI', 'situp', 'standinglongjump']
                    )
                    pred = model.predict(df)[0]

                    return pred
        
            data2 = request.form['ageDegree']
            data1 = (int(data2)//10)*10
            data3 = request.form['height']
            data4 = request.form['weight']
            data5 = request.form['trunkFlexion']
            data6 = int(data4) / (int(data3) *0.01)**2
            data7 = request.form['situp']
            data8 = request.form['standinglongjump']

            result = predict_grade(data1, data2, data3, data4, data5, data6, data7, data8)

            return render_template('result.html', result=result)
        elif temp == '청소년':
            with open('youth.pickle','rb') as pickle_file:
                model = pickle.load(pickle_file)
                def predict_grade(ageDegree, height, weight,jump, trunkFlexion, IllinoisAgility, BMI, standinglongjump):
                    df = pd.DataFrame(
                    data=[[ageDegree, height, weight, jump, trunkFlexion, IllinoisAgility, BMI, standinglongjump]], 
                    columns=['ageDegree', 'height', 'weight', 'jump','trunkFlexion', 'IllinoisAgility','BMI', 'standinglongjump']
                    )
                    pred = model.predict(df)[0]

                    return pred
        
            data1 = request.form['ageDegree']
            data2 = request.form['height']
            data3 = request.form['weight']
            data4 = request.form['jump']
            data5 = request.form['trunkFlexion']
            data6 = request.form['IllinoisAgility']
            data7 = int(data3) / (int(data2) *0.01)**2
            data8 = request.form['standinglongjump']
            

            result = predict_grade(data1, data2, data3, data4, data5, data6, data7, data8)

            return render_template('result.html', result=result)
        elif temp == '유소년':
            with open('underaged.pickle','rb') as pickle_file:
                model = pickle.load(pickle_file)
                def predict_grade(ageDegree, height, weight, crunch, trunkFlexion, BMI, standinglongjump):
                    df = pd.DataFrame(
                    data=[[ageDegree, height, weight, crunch, trunkFlexion, BMI, standinglongjump]], 
                    columns=['ageDegree', 'height', 'weight','crunch', 'trunkFlexion','BMI', 'standinglongjump']
                    )
                    pred = model.predict(df)[0]

                    return pred
        
            data1 = request.form['ageDegree']
            data2 = request.form['height']
            data3 = request.form['weight']
            data4 = request.form['crunch']
            data5 = request.form['trunkFlexion']
            data6 = int(data3) / (int(data2) *0.01)**2
            data7 = request.form['standinglongjump']
            

            result = predict_grade(data1, data2, data3, data4, data5, data6, data7) 
            return render_template('result.html', result=result)
            #하나라도 안넣어주면 오류가 생김.. 이걸 어떻게 바꿀 수 없을까...

@app.route('/how')
def how():
    return render_template('how.html'), 200  

@app.route('/exercise')
def exercise():
    return render_template('exercise.html'), 200   

def model():
    import model
    return model  
def load_db():
    import load
    return load


# 매일 변경사항 업데이트
# scheduler = BackgroundScheduler({'apscheduler.timezone':'Asia/Seoul'})
# # 데이터수집, 적재
# scheduler.add_job(func=load_db, trigger='interval', days=1)

# # 데이터 추출 및 모델링
# scheduler.add_job(func = model, trigger= 'interval', days=1)

# scheduler.start()



if __name__=="__main__":
    app.run() #host='0.0.0.0'

#헤로쿠로 배포하였당. https://projectsection3.herokuapp.com/