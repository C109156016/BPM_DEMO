# import flask
# from flask import Flask, render_template,jsonify
# from flask_socketio import SocketIO
# from flask_cors import CORS,cross_origin
# import mysql.connector
# from mysql.connector import Error
# import datetime

# app = Flask(__name__)
# app.config["DEBUG"] = True
# app.config['JSON_AS_ASCII'] = False

# CORS(form_category, resources={r"/*": {"origins": "http://51.79.145.242:3000"}},
#      supports_credentials=True,
#      allow_headers=["Content-Type", "Authorization"],
#      methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# socketio = SocketIO(form_category, cors_allowed_origins="*")
# # 创建一个API端点来返回表单类别数据

# def get_forms():
    
#     try:
        
#         connection = mysql.connector.connect(
#             host='localhost',
#             database='public.roles',
#             user='root',
#             password='As2158936'
            
#         )
#         if connection.is_connected():

#             cursor = connection.cursor()
           
#             cursor.execute(
#                 "SELECT * FROM `form_categorys`;")
#             i = 0      
        
        
#             data = {"response":   }
            
#             tmp = 0
#             for (categoryId,categoryName,formId,formName,isDeleted)in cursor:                                 
#                 data['response']["data"] ={                                  
#                     "category_id": categoryId,        
#                     "category_name": categoryName,   
#                     "form_id": formId,   
#                     "form_name": formName,   
#                     "is_deleted": isDeleted,                         
#                 }
#                 print(data)
#                 return flask.jsonify(data) 
    
     
#     except Error as e:
#         print("資料庫連接失敗:", e) 
            
# @app.route('/api/forms')
# @cross_origin()       
# def Checklist():

#     data = {"count": "loginCount",
#              "max":30,
#               "current_time":"now"
#             }
#     return flask.jsonify(data)

# if __name__ == '__main__':
#     app.run(form_category,debug=True)