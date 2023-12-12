# from flask import Flask, jsonify

# app = Flask(__name__)
# if __name__ == '__main__':
#     app.run(debug=True)

# # 创建一个API端点来返回表单类别数据
# @app.route('/api/forms', methods=['GET'])
# def get_forms():
    
#     try:
        
#         connection = mysql.connector.connect(
#             host='localhost',
#             database='public.roles',
#             user='root',
#             password='As2158936'
            
#         )
#           if connection.is_connected():

#             cursor = connection.cursor()
           
#             cursor.execute(
#                 "SELECT * FROM `form_categorys`;")
#             i = 0      
        
        
#             data = {"response": 
       
#             }
            
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
            
        

#     return jsonify(forms_data)
