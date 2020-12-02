from flask import Flask, Response, make_response
from urllib import parse
import requests
import json


#instance 생성
app = Flask(__name__)

#헬스체크용(호출할일 없을듯)
@app.route('/ping')
def health_check():
    return 'pong'

#구글 스프레드시트 쿼리조회 값 리턴
@app.route('/getlist', methods=["GET"])
def spreadsheets():  
    url = 'https://docs.google.com/spreadsheets/d/16x3q7nPiMAd6HDwVO1MrxdHVkvqldMqhJenHkp6BbUs/gviz/tq?tq='
    tq = 'select B where C is not null and C<=toDate(now()) and A=false'
    
    #쿼리 인코딩
    query = parse.quote_plus(tq)      
    response = requests.get(url+query)

    #json 파싱을 위해서 치환
    response_text = response.text.replace('/*O_o*/\ngoogle.visualization.Query.setResponse(', '').replace(');','')               
    



    # 1) json형태 그대로 리턴 -> groovy에서 처리
    result= make_response(response_text)
    

    ## 2) string으로 리턴해야하는 경우
    # response_json = json.loads(response_text)    
    # rowlist = response_json['table']['rows']
    # todo = []
    # for row in rowlist:        
    #     todo.append(row['c'][0]['v'])    
    # result = ','.join(todo)
    
    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


