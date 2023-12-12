import flask
from flask import Flask, render_template,jsonify,request
from flask_socketio import SocketIO
from flask_cors import CORS,cross_origin
import mysql.connector
from mysql.connector import Error
import datetime
import pytz
import uuid

taipei = pytz.timezone('Asia/Taipei')  
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False

CORS(app, resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])


socketio = SocketIO(app, cors_allowed_origins="*")

def process_data(my_data):
    processed_data = []
    for department in my_data:
        department_dict = {
            'department_id': department[0],
            'department_name': department[1],
            'department_parent': department[2],
            'department_update': department[3].strftime("%Y-%m-%d %H:%M:%S") if department[3] is not None else None,
        }
        processed_data.append(department_dict)
    return processed_data

def process_roles_data(roles_data):
    processed_data = []
    for role in roles_data:
        role_dict = {
            'role_id': role[0],
            'department_id': role[1],
            'role_name': role[2],
            'role_id_superior': role[3],
            'role_update': role[4].strftime("%Y-%m-%d %H:%M:%S") if role[4] is not None else None,
        }
        processed_data.append(role_dict)
    return processed_data

def process_bpm_data(bpm_data):
    processed_data = []
    for bpm in bpm_data:
        bpm_dict = {
            'review_id': bpm[0],
            'review_name': bpm[1],
            'form_id': bpm[2],
            'department_id':bpm[3],
            'role_id': bpm[4],
            'review_content': bpm[5],
            'review_update': bpm[6].strftime("%Y-%m-%d %H:%M:%S") if bpm[6] is not None else None,
        }
        processed_data.append(bpm_dict)
    return processed_data

def process_employee_data(employee_data):
    processed_data = []
    for employee in employee_data:
        employee_dict = {
            'employee_id': employee[0],
            'employee_name': employee[1],
            'department_id': employee[2],
            'role_id': employee[3],
            'employee_email': employee[4],
            'employee_password': employee[5],
            'employee_role': employee[6],
            'employee_update': employee[7].strftime("%Y-%m-%d %H:%M:%S") if employee[7] is not None else None,
        }
        processed_data.append(employee_dict)
    return processed_data

def process_FormCategorys_data(form_data):
    processed_data = []
    for form in form_data:
        form_dict = {
            'form_id': form[0],
            'form_name': form[1],
            'form_updated': form[2].strftime("%Y-%m-%d %H:%M:%S") if form[2] is not None else None,
        }
        processed_data.append(form_dict)
    return processed_data

def process_Process_data(Process_data):
    processed_data = []
    for process in Process_data:
        process_dict = {
            'process_id': process[0],
            'apply_id': process[1],
            'form_type': process[2],
            'task_status': process[3],
            'comment': process[4],
            'applier': process[5],
            'content': process[6],
            'principal_role_id': process[7],
            'principal_employee_id': process[8],
            'apply_date': process[9].strftime("%Y-%m-%d %H:%M:%S") if process[9] is not None else None,
            'expiry_line': process[10].strftime("%Y-%m-%d %H:%M:%S") if process[10] is not None else None,
            'is_deleted': process[11],
            'created_at': process[12].strftime("%Y-%m-%d %H:%M:%S") if process[12] is not None else None,
            'created_by': process[13],
            'updated_at': process[14].strftime("%Y-%m-%d %H:%M:%S") if process[14] is not None else None,
            'updated_by': process[15],
            'department_name': process[16],
            'role_name': process[17],
            'applier_name': process[18],
        }
        processed_data.append(process_dict)
        print("message:Processes dict successfully.")
    return processed_data

def login(data):
    
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
            
        )
        if connection.is_connected():

            cursor = connection.cursor()
           
            cursor.execute(
                f"select employee_id,employee_name, department_id, role_id, employee_email, employee_password, employee_role FROM employees where employee_email ='{data[0]}'  and employee_password = '{data[1]}'"
            )

            data=[]

            for (employee_id,employee_name,department_id, role_id,employee_email, employee_password, employee_role)in cursor:                              
                data = [employee_id,employee_name,department_id, role_id,employee_email, employee_password, employee_role]                                  
                print(data)

            print("message:successfully.")

            return data

    except Error as e:
        print("資料庫連接失敗:", e)        

def addComData(data):
    
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
            
        )
        if connection.is_connected():

            department_update = datetime.datetime.now()

            department_update = department_update.strftime('%Y-%m-%d %H:%M:%S')


            cursor = connection.cursor()

            department_id = str(uuid.uuid4())
           
            cursor.execute(
                f"INSERT INTO departments (department_id, department_name, department_parent,department_update) VALUES ('{department_id}', '{data[0]}', '{data[1]}','{department_update}')"
            )

            connection.commit()
            print("message: User added successfully.")

    except Error as e:
        print("資料庫連接失敗:", e)          

def fetchedData():
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select * FROM departments")
            result = cursor.fetchall()
            print("message:successfully.")
            return result
    except Error as e:
        print("資料庫連接失敗:", e)

def updateComData(department_id, new_department_name, new_department_parent,department_update):
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            department_update = datetime.datetime.now()

            department_update = department_update.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(
                f"UPDATE departments SET department_name = '{new_department_name}', department_parent = '{new_department_parent}', department_update = '{department_update}' WHERE department_id = '{department_id}'"
            )

            connection.commit()
            print("message: Department updated fuuuuck successfully.")

    except Error as e:
        print("資料庫連接失敗:", e)

def addComEmployeeData(data):
    try:
        
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
            
        )
        if connection.is_connected():

            employee_update = datetime.datetime.now()

            employee_update = employee_update.strftime('%Y-%m-%d %H:%M:%S')

            cursor = connection.cursor()

            employee_id = str(uuid.uuid4())
           
            cursor.execute(
                f"INSERT INTO employees (employee_id, employee_name, employee_email, employee_password, role_id, department_id, employee_role, employee_update) VALUES ('{employee_id}', '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{int(data[5])}', '{employee_update}')"
                )

            connection.commit()
            print("message: User added successfully.")
            
    except Error as e:
        print("資料庫連接失敗:", e)     

def fetchedEmployeeData():
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select * FROM employees")
            result = cursor.fetchall()
            print("message:successfully.")
            return result
    except Error as e:
        print("資料庫連接失敗:", e)

def updateEmployeeData(employee_id, new_employee_name, new_department_id, new_role_id, new_employee_email, new_employee_password, new_employee_role, employee_update):
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            employee_update = datetime.datetime.now()

            employee_update = employee_update.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(
                f"UPDATE employees SET employee_name = '{new_employee_name}', department_id = '{new_department_id}', role_id = '{new_role_id}', employee_email = '{new_employee_email}', employee_password = '{new_employee_password}', employee_role = '{new_employee_role}', employee_update = '{employee_update}' WHERE employee_id = '{employee_id}'"
            )

            connection.commit()
            print("message: employee updated successfully.")

    except Error as e:
        print("資料庫連接失敗:", e)

def addComRolesData(data):
    try:
        
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
            
        )
        if connection.is_connected():

            role_update = datetime.datetime.now()

            role_update = role_update.strftime('%Y-%m-%d %H:%M:%S')

            role_id = str(uuid.uuid4())

            cursor = connection.cursor()
           
            cursor.execute(
                f"INSERT INTO roles (role_id, role_name, role_id_superior, department_id, role_update) VALUES ('{role_id}', '{data[0]}', '{data[1]}', '{data[2]}',NOW())"
                )

            connection.commit()
            print("message: User added successfully.")
            
    except Error as e:
        print("資料庫連接失敗:", e)     

def fetchedRolesData():
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select * FROM roles")
            result = cursor.fetchall()
            print("message:successfully.")

            return result
    except Error as e:
        print("資料庫連接失敗:", e)

def updateRoleComData(role_id, new_role_name, new_role_sup,new_department_id,role_update):
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            role_update = datetime.datetime.now()

            role_update = role_update.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(
                f"UPDATE roles SET role_name = '{new_role_name}', role_id_superior = '{new_role_sup}', department_id = '{new_department_id}',role_update = '{role_update}' WHERE role_id = '{role_id}'"
            )

            connection.commit()
            print("message: role updated successfully.")

    except Error as e:
        print("資料庫連接失敗:", e)

def fetchedBpmData():
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select * FROM review")
            result = cursor.fetchall()
            print("message:BPM successfully.")

            return result
    except Error as e:
        print("資料庫連接失敗:", e)

def addComBpmData(data):
    try:
        
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
            
        )
        if connection.is_connected():

            review_update = datetime.datetime.now()

            review_update = review_update.strftime('%Y-%m-%d %H:%M:%S')

            review_id = str(uuid.uuid4())

            cursor = connection.cursor()

            review_content_str = ','.join(data[4])
           
            cursor.execute(
                "INSERT INTO review (review_id, review_name, form_id, department_id, role_id, review_content, review_update) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (review_id, data[0], data[1], data[2], data[3], review_content_str, review_update)
            )
            connection.commit()
            print("message: Bpm added successfully.")
            
    except Error as e:
        print("資料庫連接失敗:", e)     

def fetchedFormCategorysData():
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select * FROM form_categorys")
            result = cursor.fetchall()
            print("message:Form successfully.")

            return result
    except Error as e:
        print("資料庫連接失敗:", e)

def fetchedProcessData():
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select * FROM processes")
            result = cursor.fetchall()
            print("message:Processes successfully.")

            return result
    except Error as e:
        print("資料庫連接失敗:", e)

def tmp(data):
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
                "sql")
            
    except Error as e:
        print("資料庫連接失敗:", e) 

def fetchReviewData(input_data):
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
                f"SELECT review_id, review_name, form_id, department_id, role_id, review_content, review_update  FROM review WHERE form_id = '{input_data[0]}'"
            )

            result_data = []

            for (review_id, review_name, form_id, department_id, role_id, review_content, review_update) in cursor: 
                review_update_str = review_update.strftime("%Y-%m-%d %H:%M:%S")
                result_data.append([review_id, review_name, form_id, department_id, role_id, review_content, review_update_str])


            print("Message:fetchReviewData Successfully.")
            return result_data
    except Error as e:
        print("getReviewData Database connection failed:", e)


# APP端
def appAddComData(data):
    
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
            
        )
        if connection.is_connected():       
                     
          
            # 使用特定的日期和時間                
            apply = datetime.datetime.now()
            expiry = apply + datetime.timedelta(days=7)
          
            # 格式化日期和時間
            apply = apply.strftime('%Y-%m-%d %H:%M:%S')
            expiry = expiry.strftime('%Y-%m-%d %H:%M:%S')


            cursor = connection.cursor()
          
            cursor.execute(
                f"INSERT INTO processes (apply_id, form_type, task_status, comment, applier, content,  principal_role_id, principal_employee_id, apply_date, expiry_line, is_deleted, created_at, created_by, updated_at, updated_by, department_name, role_name, applier_name) VALUES('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}', '{apply}',  '{expiry}','{data[8]}','{apply}' ,'{data[4]}','{apply}', '{data[4]}','{data[9]}','{data[10]}','{data[11]}')"
            )

            connection.commit()
            print("processes INSERT message: User added successfully.")

    except Error as e:
        print("資料庫連接失敗:", e)   
        
def getProcessesData(data):
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
                f"SELECT process_id, apply_id, form_type, task_status, comment, applier, content, principal, is_deleted, created_by, updated_by, applier_name  FROM processes WHERE applier = '{data[0]}' OR principal = '{data[1]}'"
            )

            data_list = []

            for (process_id, apply_id, form_type, task_status, comment, applier, content, principal, is_deleted, created_by, updated_by, applier_name) in cursor: 
                data_list.append([process_id, apply_id, form_type, task_status, comment, applier, content, principal, is_deleted, created_by, updated_by, applier_name])
                print([process_id, apply_id, form_type, task_status, comment, applier, content, principal, is_deleted, created_by, updated_by, applier_name])

            print("Message: Successfully.")
            return data_list

    except Error as e:
        print("Database connection failed:", e)
        
def appUpdateComData(process_id, new_task_status, new_comment,new_updated_by):
    try:
        print("in")
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
                # 使用特定的日期和時間                
            updated_at = datetime.datetime.now()        
          
            # 格式化日期和時間
            updated_at = updated_at.strftime('%Y-%m-%d %H:%M:%S')
           
            cursor.execute(
                f"UPDATE processes SET task_status = '{new_task_status}', comment = '{new_comment}', updated_at = '{updated_at}', updated_by = '{new_updated_by}' WHERE process_id = '{process_id}'"
            )

            connection.commit()
            print("message: Department updated fuuuuck successfully.")

    except Error as e:
        print("資料庫連接失敗:", e)    
        
def getRoleIdSuperior(data):
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
                f"SELECT role_id, role_id_superior FROM roles WHERE role_id = '{data[0]}'"
            )
            
            data = []

            for (role_id, role_id_superior) in cursor: 
                data = [role_id, role_id_superior]
                print(data)

            print("Message: Successfully.")
            return data

    except Error as e:
        print("Database connection failed:", e)

def getRoleEmployeeData(data):
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
                f"SELECT employee_id, employee_name, department_id, role_id  FROM employees WHERE role_id = '{data[0]}'"
            )

            data = []

            for (employee_id, employee_name, department_id, role_id) in cursor: 
                data = [employee_id, employee_name, department_id, role_id]
                print(data)

            print("Message: Successfully.")
            return data

    except Error as e:
        print("Database connection failed:", e)

def getEmployeeData(data):
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
                f"SELECT employee_email, employee_password, employee_id, employee_name, department_id, role_id, employee_role FROM employees WHERE employee_email = '{data[0]}' AND employee_password = '{data[1]}'"
            )

            data = []

            for (employee_email, employee_password, employee_id, employee_name, department_id, role_id, employee_role) in cursor: 
                data = [employee_email, employee_password, employee_id, employee_name, department_id, role_id, employee_role]
                print(data)

            print("Message: Successfully.")
            return data

    except Error as e:
        print("Database connection failed:", e)

def getAllReviewData(data):
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
                f"SELECT review_id, review_name, form_id, department_id, role_id, review_content  FROM review"
            )

            data = []

            for (review_id, review_name, form_id, department_id, role_id, review_content) in cursor: 
                data = [review_id, review_name, form_id, department_id, role_id, review_content]
                print(data)

            print("Message:getAllReviewData Successfully.")
            return data

    except Error as e:
        print("getAllReviewData Database connection failed:", e)

def getReviewData(data):
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
                f"SELECT review_id, review_name, form_id, department_id, role_id, review_content, review_update  FROM review WHERE form_id = '{data[0]}'"
            )

            data = []

            for (review_id, review_name, form_id, department_id, role_id, review_content, review_update) in cursor: 
                data = [review_id, review_name, form_id, department_id, role_id, review_content, review_update]
                print(data)

            print("Message:getReviewData Successfully.")
            return data

    except Error as e:
        print("getReviewData Database connection failed:", e)

@socketio.on('message')     
def handle_message(message):
    print('Received message: ' + message)

@socketio.on("login")
def login_data(data):
    print(data)
    data =  login(data)
    socketio.emit('response', [data[0], data[1], data[2],data[3],data[4],data[5],data[6]])

@socketio.on("addComData")
def add_com_data(data):
    print(data)
    addComData(data)

@socketio.on("fetchedData")
def fetched_data():
    my_data = fetchedData()
    processed_data = process_data(my_data)
    socketio.emit('departmentsData', processed_data)

@socketio.on("updateComData")
def update_com_data(data):
    department_id = data.get('department_id')
    new_department_name = data.get('new_department_name')
    new_department_parent = data.get('new_department_parent')
    department_update = data.get('department_update')
    updateComData(department_id, new_department_name, new_department_parent, department_update)
    print(data)

@socketio.on("addComEmployeeData")
def add_com_employee_data(data):
    print(data)
    addComEmployeeData(data)

@socketio.on("fetchedEmployeeData")
def fetched_employee_data():
    employee_data = fetchedEmployeeData()
    processed_employee_data = process_employee_data(employee_data)
    socketio.emit('employeeData', processed_employee_data)

@socketio.on("updateEmployeeData")
def update_employee_data(data):
    employee_id = data.get('employee_id')
    new_employee_name = data.get('new_employee_name')
    new_department_id = data.get('new_department_id')
    new_role_id = data.get('new_role_id')
    new_employee_email = data.get('new_employee_email')
    new_employee_password = data.get('new_employee_password')
    new_employee_role = data.get('new_employee_role')
    employee_update = data.get('employee_update')
    updateEmployeeData(employee_id, new_employee_name, new_department_id, new_role_id, new_employee_email, new_employee_password, new_employee_role, employee_update)
    print(data)

@socketio.on("addComRolesData")
def add_com_roles_data(data):
    print(data)
    addComRolesData(data)

@socketio.on("fetchedRolesData")
def fetched_roles_data():
    roles_data = fetchedRolesData()
    processed_roles_data = process_roles_data(roles_data)
    socketio.emit('RolesData', processed_roles_data)

@socketio.on("updateRoleComData")
def update_role_com_data(data):
    role_id = data.get('role_id')
    new_role_name = data.get('new_role_name')
    new_role_sup = data.get('new_role_sup')
    new_department_id = data.get('new_department_id')
    role_update = data.get('role_update')
    updateRoleComData(role_id, new_role_name, new_role_sup, new_department_id, role_update)
    print(data)

@socketio.on("fetchedBpmData")
def fetched_bpm_data():
    bpm_data = fetchedBpmData()
    processed_bpm_data = process_bpm_data(bpm_data)
    socketio.emit('BpmData', processed_bpm_data)

@socketio.on("addComBpmData")
def add_com_bpm_data(data):
    print(data)
    addComBpmData(data)

@socketio.on("fetchedFormCategorysData")
def fetched_bpm_data():
    form_data = fetchedFormCategorysData()
    processed_FormCategorys_data = process_FormCategorys_data(form_data)
    socketio.emit('FormCategorysData', processed_FormCategorys_data)

@socketio.on("fetchedProcessData")
def fetched_process_data():
    Process_data = fetchedProcessData()
    processed_Process_data = process_Process_data(Process_data)
    socketio.emit('ProcessData', processed_Process_data)

@socketio.on("fetchReviewData")
def fetch_review_data(data):
    result_data = fetchReviewData(data)
    socketio.emit('ReviewData', result_data)





# app
@socketio.on("tmp")
def add_com_employee_data(data):
    print(data)

@socketio.on("appAddComData")
def app_add_com_data(data):
    print(data)
    appAddComData(data)

@socketio.on("appUpdateComData")
def update_com_data(data):
    process_id = data.get('process_id')
    new_task_status = data.get('new_task_status')
    new_comment = data.get('new_comment')
    new_updated_by = data.get('new_updated_by')
    appUpdateComData(process_id, new_task_status, new_comment,new_updated_by)
    print(data)

@socketio.on("getRoleIdSuperior")
def get_role_id_superior(data):
    print(data)
    data =  getRoleIdSuperior(data)
    socketio.emit('result', [data[0], data[1]])
    
@socketio.on("getRoleEmployeeData")
def get_role_employee_data(data):
    print(data)
    data =  getRoleEmployeeData(data)
    socketio.emit('ProcessData', [data[0], data[1], data[2], data[3]])

@socketio.on("getEmployeeData")
def get_employee_data(data):
    print(data)
    data =  getEmployeeData(data)
    socketio.emit('result', [data[0], data[1], data[2], data[3], data[4], data[5],data[6]])

@socketio.on("getProcessesData")
def get_processes_data():
    ProcessesData = getProcessesData()
    processed_data = process_data(ProcessesData)
    socketio.emit('ProcessesData', processed_data)

@socketio.on("getAllReviewData")
def get_all_review_data():
    # print(form_id)
    data =  getAllReviewData()
    socketio.emit('ReviewData', [data[0], data[1], data[2], data[3], data[4], data[5],data[6]])

@socketio.on("getReviewData")
def get_review_data(data):
    # print(form_id)
    data =  getReviewData(data)
    socketio.emit('ReviewData', [data[0], data[1], data[2], data[3], data[4], data[5],data[6]])



# 创建一个API端点来返回表单类别数据
@app.route('/api/forms')
@cross_origin()
def get_forms():
    
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
                "SELECT * FROM `form_categorys`;")
            i = 0      
            data = {"response": 
       {
           
       }
            }
            
            tmp = 0
            for (formId,formName,formUpdated)in cursor:      
                tmp+=1                           
                data['response']["data"] ={                                  
                    "form_id": formId,   
                    "form_name": formName,   
                    "form_updated":formUpdated,
                }
                print(data)
                return flask.jsonify(data) 
    
     
    except Error as e:
        print("資料庫連接失敗:", e) 
            
@app.route('/api/employees')
@cross_origin()
def get_employees():
    
    try:
        
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
            
        )
        if connection.is_connected():
            cursor = connection.cursor()
           
            cursor.execute("SELECT * FROM `employees`;")

            data = {"response": {"data": []}}  # Initialize an empty list for data

          
            for row in cursor :
                employee_id,employee_name,department_id,role_id,empolyee_email,empolyee_password,empolyee_role,empolyee_update = row    

                data['response']["data"].append({                                  
                    "employee_id": employee_id,        
                    "employee_name": employee_name,   
                    "department_id": department_id,
                    "role_id": role_id,        
                    "empolyee_email": empolyee_email,   
                    "empolyee_password": empolyee_password,
                    "empolyee_role": empolyee_role,        
                    "empolyee_update": empolyee_update,   
                })

            return jsonify(data)  # Return JSON response after processing all rows
    
     
    except Error as e:
        print("Database connection error:", e)  
             
@app.route('/api/processes')
@cross_origin()
def get_processes():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `processes`;")

            data = {"response": {"data": []}}  # Initialize an empty list for data

            for row in cursor:
                process_id, apply_id, form_type, task_status, comment, applier, content, principal_role_id, principal_employee_id, apply_date, expiry_line, is_deleted, created_at, created_by, updated_at, updated_by, department_name, role_name, applier_name = row

                data["response"]["data"].append({
                    "process_id": process_id,
                    "apply_id": apply_id,
                    "form_type": form_type,
                    "task_status": task_status,
                    "comment": comment,
                    "applier": applier,
                    "content": content,
                    "principal_role_id": principal_role_id,
                    "principal_employee_id": principal_employee_id,
                    "apply_date": apply_date,
                    "expiry_line": expiry_line,
                    "is_deleted": is_deleted,
                    "created_at": created_at,
                    "created_by": created_by,
                    "updated_at": updated_at,
                    "updated_by": updated_by,
                    "department_name": department_name,
                    "role_name": role_name, 
                    "applier_name": applier_name,
                })

            return jsonify(data)  # Return JSON response after processing all rows

    except mysql.connector.Error as e:
        print("Database connection error:", e)

@app.route('/api/departments')
@cross_origin()
def get_departments():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `departments`;")

            data = {"response": {"data": []}}  # Initialize an empty list for data

            for row in cursor:
                department_id, department_name, department_parent, department_update= row

                data["response"]["data"].append({
                    "department_id": department_id,
                    "department_name": department_name,
                    "department_parent": department_parent,
                    "department_update": department_update,
                })

            return jsonify(data)  # Return JSON response after processing all rows

    except mysql.connector.Error as e:
        print("Database connection error:", e)

@app.route('/api/roles')
@cross_origin()
def get_roles():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='public.roles',
            user='root',
            password='As2158936'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `roles`;")

            data = {"response": {"data": []}}  # Initialize an empty list for data

            for row in cursor:
                role_id, department_id, role_name, role_id_superior, role_update= row

                data["response"]["data"].append({
                    "role_id": role_id,
                    "department_id": department_id,
                    "role_name": role_name,
                    "role_id_superior": role_id_superior,
                    "role_update": role_update,
                })

            return jsonify(data)  # Return JSON response after processing all rows

    except mysql.connector.Error as e:
        print("Database connection error:", e)

@app.route('/api/review')
def getAllReviewData():
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
                f"SELECT review_id, review_name, form_id, department_id, role_id, review_content  FROM review"
            )

            data = {"response": {"data": []}}  # Initialize an empty list for data

            for row in cursor:
                review_id, review_name, form_id, department_id, role_id, review_content = row 

                data["response"]["data"].append({
                     "review_id": review_id,
                    "review_name": review_name,
                    "form_id": form_id,
                    "department_id": department_id,
                    "role_id": role_id,
                    "review_content": review_content,
                })
                

            return jsonify(data)  # Return JSON response after processing all rows

    except Error as e:
        print("Database connection error:", e)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8686, host="51.79.145.242", allow_unsafe_werkzeug=True)    
