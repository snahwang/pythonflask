from flask import Flask, Response, render_template
from urllib import parse
import requests
import json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/ping')
def health_check():
    return 'pong'

@app.route('/todo/<username>', methods=["GET"])
def spreadsheets(username):  
    url = 'https://docs.google.com/spreadsheets/d/16x3q7nPiMAd6HDwVO1MrxdHVkvqldMqhJenHkp6BbUs/gviz/tq?tq='
    tq = 'select B where C is not null and C<=toDate(now()) and A=false'   

    if username =='sunhee':
        sheetid = '&gid=1386834576'
    elif username == 'bk':
        sheetid = '&gid=1864599306'
    else :
        tq = 'select B where B is not null and A=false'   
        sheetid = '&gid=186639618'
    
    #print (url)
    query = parse.quote_plus(tq)      
    response = requests.get(url+query + sheetid)    
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


@app.route('/', methods=["GET"])
def allsheet():  
    url = 'https://docs.google.com/spreadsheets/d/16x3q7nPiMAd6HDwVO1MrxdHVkvqldMqhJenHkp6BbUs/gviz/tq?tq='
    tq = 'select B where C is not null and C<=toDate(now()) and A=false'   
    sunhee = {}
    byungkyu = {}
    things = {}
    
    for i in range(1, 4): 
        
        if i == 1:
            sheetid = '&gid=1386834576'
            query = parse.quote_plus(tq)      
            response = requests.get(url+query + sheetid)    
            response_text = response.text.replace('/*O_o*/\ngoogle.visualization.Query.setResponse(', '').replace(');','')               
            response_json = json.loads(response_text)    
            rowlist = response_json['table']['rows']        
            cnt = 0;

            for row in rowlist:
                cnt+=1
                sunhee[cnt] = row['c'][0]['v']

        elif i == 2:
            sheetid = '&gid=1864599306'
            query = parse.quote_plus(tq)      
            response = requests.get(url+query + sheetid)    
            response_text = response.text.replace('/*O_o*/\ngoogle.visualization.Query.setResponse(', '').replace(');','')               
            response_json = json.loads(response_text)    
            rowlist = response_json['table']['rows']
            cnt = 0;           
            
            for row in rowlist:    
                cnt+=1
                byungkyu[cnt] = row['c'][0]['v']     

        else :
            tq = 'select B where B is not null and A=false'   
            sheetid = '&gid=186639618'

            query = parse.quote_plus(tq)      
            response = requests.get(url+query + sheetid)    
            response_text = response.text.replace('/*O_o*/\ngoogle.visualization.Query.setResponse(', '').replace(');','')               
            response_json = json.loads(response_text)    
            rowlist = response_json['table']['rows']
            cnt = 0;
            
            for row in rowlist:
                cnt+=1
                things[cnt] = row['c'][0]['v']  
        
    # render
    return render_template('index.html', sunheetodo=sunhee, bktodo =byungkyu, buy = things )



if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=80)


