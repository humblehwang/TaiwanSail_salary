
from flask import Flask, redirect, url_for, request, render_template,jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer    
from flask import Flask, request
import json

import pandas as pd
import numpy as np
import os

# Custom Response Format
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,            
    }  





def checkSalary(ID):

    data = []
    file_list = os.listdir("file")
    file_list.sort()
    df = []
    month = []
    for index in range(len(file_list)):
        if file_list[index] == '.ipynb_checkpoints':
            continue
            
        file_name = "file/" + file_list[index]
        df_tmp = pd.read_csv(file_name,error_bad_lines=False,encoding="UTF-8")
        df_tmp = df_tmp.fillna(0)
        df.append(df_tmp)
        month.append(file_name[9])
    check = 1    
    for i in range(len(df)):
        data_tmp = []
        data_tmp.append(month[i])
        for j in range(len(df[i])):
            if df[i]['ID'][j] == 0:
                continue
            
            if ID in df[i]["ID"][j]:
                data_tmp.append(df[i]['Name'][j])
                data_tmp.append(df[i]['ID'][j])
                data_tmp.append(df[i]['SocialSecurityDays'][j])
                data_tmp.append(df[i]['Character'][j])
                data_tmp.append(df[i]['Class'][j])
                data_tmp.append(df[i]['AirLove'][j])
                data_tmp.append(df[i]['Other'][j])
                data_tmp.append(df[i]['Subtraction'][j])
                data_tmp.append(df[i]['total'][j])
                data_tmp.append(df[i]['Net salary'][j])
                print(data_tmp) 
                check = 0
                break;
        
        #print(data_tmp)        
        #data_tmp.append(month[i])
        data.append(data_tmp)
      
    return data,check


app = Flask(__name__)
print('Server start. Check http://140.113.73.55:3251/')


@app.route('/', methods=['GET', 'POST']) 
def index():
    return   render_template("home.html")


    
    
@app.route('/getsalary', methods=['GET', 'POST']) 
def getSalary():
    print("salary")

    #print("request",request.values['ID'])
    if request.method == 'POST': 
        data = json.loads(request.data)
        data,check = checkSalary(data['ID'])
        
        if check == 1:
            print("No This User ID")

        else:
            print(data)

     
        _Response["responseText"] = render_template("salary.html", flag=check,data_list = data)
        return jsonify(_Response)    
   

if __name__ == '__main__':
    # Serve the app with gevent
    http_server = WSGIServer(('',3251), app)
    http_server.serve_forever() 