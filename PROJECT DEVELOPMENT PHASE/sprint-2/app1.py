from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
app = Flask(__name__)
app.secret_key = 'a'
Conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tbd72327;PWD=ftnrC2umf9VxgMW1" ,'','')

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login1')
def login1():
    return render_template('login.html')
@app.route('/register1')
def register1():
    return render_template('register.html')
@app.route('/about1')
def about1():
    return render_template('about.html')
@app.route('/help1')
def help1():
    return render_template('help.html')
@app.route('/report')
def report():
    return render_template('report.html')
@app.route('/lists1')
def lists1():
    return render_template('lists1.html')
    
    
    
@app.route('/pie')
def google_pie_chart():
    data={'total widrawal money':'50000','food':20000,'travel':8000,'shopping':7000,'others':6000,'save':16000}
    return render_template('pie.html',data=data)
       
    
@app.route('/login', methods =['GET', 'POST'])
def login():

    msg = ''
    if request.method == 'POST'and 'username' in request.form and 'password' in request.form:
         username = request.form['username']
         password = request.form['password']
         stmt = ibm_db.prepare(Conn,'SELECT * FROM users WHERE username = ? AND password = ?')
         ibm_db.bind_param(stmt,1,username)
         ibm_db.bind_param(stmt,2,password) 
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         if account:
             session['loggedin'] = True
             session['username'] = account['USERNAME']
             msg = 'Logged in successfully !'
             return render_template('hi.html', msg = msg)
         else:
             msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg) 

@app.route('/logout')
def logout():
     session.pop('loggedin', None)
     session.pop('id', None)
     session.pop('username', None)
     return redirect(url_for('login'))
@app.route('/register', methods =['GET', 'POST'])
def register():
     global email
     msg = ''
     if request.method == 'POST':
         username = request.form['username']
         email = request.form['email']
         accno = request.form['accno']
         password = request.form['password']
         confirmpassword = request.form['confirmpassword']
         phone_no=request.form['no']
         user_id=request.form['userid']
         sql = "SELECT * FROM users WHERE username = ? "
         stmt = ibm_db.prepare(Conn,sql)
         ibm_db.bind_param(stmt,1,username)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)
         if account:
             msg = 'Account already exists !'
         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
             msg = 'Invalid email address !'
         elif not re.match(r'[A-Za-z0-9]+', username):
             msg = 'Username must contain only characters and numbers !'
         elif not username or not password or not email:
             msg = 'Please fill out the form !'
         elif password!=confirmpassword:
             msg='password and confirm password not match!!'
         else:
             insert_sql = "INSERT INTO users VALUES (?, ?, ?,?,?,?)"
             stmt = ibm_db.prepare(Conn,insert_sql)
             ibm_db.bind_param(stmt, 1, username)
             ibm_db.bind_param(stmt, 2, email)
             ibm_db.bind_param(stmt, 3, accno)
             ibm_db.bind_param(stmt, 4, password)
             ibm_db.bind_param(stmt, 5, phone_no)
             ibm_db.bind_param(stmt, 6, user_id)
             ibm_db.execute(stmt)
             msg = 'You have successfully registered !'
     elif request.method == 'POST':
          msg = 'Please fill out the form !'

     return render_template('register.html', msg = msg) 

@app.route('/lists1', methods =['GET', 'POST'])    
def category():
    global userid
    msg = ''
    if request.method == 'POST':
         food = request.form['Food']
         shopping = request.form['Shopping']
         travel = request.form['Travelling']
         rent = request.form['Rent']
         others = request.form['others']
         user_id = request.form['userid']
         email="SELECT EMAIL FROM USERS "
         sql = "SELECT * FROM EXPENSES WHERE FOOD = ? AND SHOPPING = ? AND TRAVELLING = ? AND RENT = ? AND OTHERS = ?  AND user_id = ? "
         stmt = ibm_db.prepare(Conn,sql)
         ibm_db.bind_param(stmt,1,food)
         ibm_db.bind_param(stmt,2,shopping)
         ibm_db.bind_param(stmt,3,travel)
         ibm_db.bind_param(stmt,4,rent)
         ibm_db.bind_param(stmt,5,others)
    
         ibm_db.bind_param(stmt,6,user_id)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)        
         insert_sql = "INSERT INTO EXPENSES VALUES ( ?, ?, ?, ?, ?, ?)"
         stmt = ibm_db.prepare(Conn,insert_sql)
         ibm_db.bind_param(stmt, 1, food)
         ibm_db.bind_param(stmt, 2, shopping)
         ibm_db.bind_param(stmt, 3, travel)
         ibm_db.bind_param(stmt, 4, rent)
         ibm_db.bind_param(stmt, 5, others)
         ibm_db.bind_param(stmt,6,email)
         ibm_db.execute(stmt)
         msg = 'You have updated successfully'
         return render_template('pie.html', msg = msg)
     
@app.route('/salary_de', methods =['GET', 'POST'])    
def salary():
    msg = ''
    if request.method == 'POST':
         email = request.form['userid']
         sa = request.form['Salary']
         li = request.form['Limit']
         sql = "SELECT * FROM salary_details WHERE EMAIL = ? AND SALARY = ? AND LIMIT = ? "
         stmt = ibm_db.prepare(Conn,sql)
         ibm_db.bind_param(stmt,1,email)
         ibm_db.bind_param(stmt,2,sa)
         ibm_db.bind_param(stmt,3,li)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)
         insert_sql = "INSERT INTO salary_details VALUES ( ?, ?, ? )"
         stmt = ibm_db.prepare(Conn,insert_sql)
         ibm_db.bind_param(stmt,1,email)
         ibm_db.bind_param(stmt,2,sa)
         ibm_db.bind_param(stmt,3,li)
         ibm_db.execute(stmt)
         msg = 'You have updated successfully'
         return render_template('lists1.html', msg = msg)

if __name__=='__main__':
    app.run(debug=True)
    