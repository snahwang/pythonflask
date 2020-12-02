from flask import Flask, Response
from urllib import parse
import requests
import json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/ping')
def health_check():
    return 'pong'

@app.route('/sunheetodo', methods=["GET"])
def spreadsheets():  
    url = 'url' #스프레드시트 url
    tq = 'query' #검색하려는쿼리
    query = parse.quote_plus(tq)      
    response = requests.get(url+query)    
    response_text = response.text.replace('/*O_o*/\ngoogle.visualization.Query.setResponse(', '').replace(');','')               
    response_json = json.loads(response_text)    
    rowlist = response_json['table']['rows']
    todo = []
    
    case = {}
    for row in rowlist:
        d = {}
        d['todo'] = row['c'][0]['v']        
        todo.append(d)
    case['list'] = todo
    
    # print (todo)
    result = Response(json.dumps(case, ensure_ascii=False, separators=(',',':')))
    result.headers['Content-Type'] = 'application/json'
    return result




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


