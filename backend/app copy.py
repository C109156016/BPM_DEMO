import flask
from flask import Flask, render_template,jsonify
from flask_socketio import SocketIO
from flask_cors import CORS,cross_origin
import mysql.connector
from mysql.connector import Error
import datetime


app = Flask(__name__,
            static_url_path='/python',   
            static_folder='static',      
            template_folder='templates') 
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False

CORS(app, resources={r"/*": {"origins": "http://51.79.145.242:3000"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

socketio = SocketIO(app, cors_allowed_origins="*")



def connectDB_getData():

    try:

        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
            
        )
        if connection.is_connected():

            cursor = connection.cursor()
           
            cursor.execute(
                "SELECT * FROM `user_index`;")
            i = 0
            data = {"response": 
            {

            }
            }
            tmp  = 0
            for (userId,userEmail,userName,userPassword,gender)in cursor:
                tmp+=1
            data['response']["data"] = {
                                        "userId": userId,
                                        "userEmail":userEmail,
                                        "userName":userName,
                                        'userPassword':userPassword,
                                        'gender':gender,
                                        }
            print(data)
            return flask.jsonify(data)
    except Error as e:
        print("資料庫連接失敗:", e)



@app.route("/list")
@cross_origin()
def Checklist():

    data = {"count": "loginCount",
             "max":30,
              "current_time":"now"
            }
    return flask.jsonify(data)



if __name__ == '__main__':
    socketio.run(app, debug=True, port=8686, host="51.79.145.242", allow_unsafe_werkzeug=True)