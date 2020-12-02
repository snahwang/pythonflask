from flask import Flask, Response, make_response
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
    url = 'https://docs.google.com/spreadsheets/d/16x3q7nPiMAd6HDwVO1MrxdHVkvqldMqhJenHkp6BbUs/gviz/tq?tq='
    tq = 'select B where C is not null and C<=toDate(now()) and A=false'   
    query = parse.quote_plus(tq)      
    response = requests.get(url+query)    
    response_text = response.text.replace('/*O_o*/\ngoogle.visualization.Query.setResponse(', '').replace(');','')               
    response_json = json.loads(response_text)    
    rowlist = response_json['table']['rows']
    todo = []
    
    
    for row in rowlist:
        d = {}
        d['todo'] = row['c'][0]['v']        
        todo.append(d)
    
    # print (todo)
    result = json.dumps(todo, ensure_ascii=False, separators=(',',':'))
    return result




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


