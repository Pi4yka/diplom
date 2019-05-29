from __future__ import print_function
import os
from flask import Flask, render_template, url_for, request, send_file, redirect, flash
from mailmerge import MailMerge
from datetime import date
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from datetime import datetime

app = Flask(__name__, static_folder='static')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'        

mysql = MySQL(app)

@app.route('/delete/<string:id_data>', methods=["GET","POST"])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s ",[id_data])
    mysql.connection.commit()
    cur.close()
    return redirect ('/users')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        result = cur.fetchall()
    else :
        return redirect ('/addclient')
    return render_template('users.html', result = result)

@app.route('/database', methods=['GET','POST'])
def db():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails ['name']
        address = userDetails ['address']
        serial = userDetails ['serial']
        number = userDetails ['number']
        issued= userDetails ['issued']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("INSERT INTO users(name, address, serial,number,issued) VALUES(%s,%s,%s,%s,%s)",(name,address,serial,number,issued))
        mysql.connection.commit()
        cur.close()
    if resultValue > 0:
        result = cur.fetchall()
    else :
        return render_template ('add_client.html')
    return redirect ('/users')
        
@app.route('/addclient', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails ['name']
        address = userDetails ['address']
        serial = userDetails ['serial']
        number = userDetails ['number']
        issued= userDetails ['issued']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("INSERT INTO users(name, address, serial,number,issued) VALUES(%s,%s,%s,%s,%s)",(name,address,serial,number,issued))
        mysql.connection.commit()
        cur.close()
        if resultValue > 0:
            result = cur.fetchall()
            return redirect ('/users')
        else : 
            return render_template ('add_client.html')
    return render_template ('add_client.html')

@app.route('/', methods=['GET','POST'])
def main():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        result = cur.fetchall()
    else :
        return redirect ('/addclient')
    return render_template ('index.html', result = result)
    
@app.route('/developer')
def develop():
    return render_template ('developer.html')

@app.route('/generate', methods = ["GET","POST"])
def generate():
    target = os.path.join(APP_ROOT, 'static/')

    for template in request.files.getlist("file"):
        print (template)
        filename = template.filename
    document = MailMerge(template)
    print (document.get_merge_fields())
    {'name','address','serial','number','issued'}
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        id = request.form['id']    
        cur.execute("SELECT * FROM users where id = %s",[id])
        result = cur.fetchall()
        for user in result:
            name = user[1]
            address = user[2]
            serial = user[3] 
            number = user[4] 
            issued = user[5] 

        document.merge(
            name = user[1],
            date = '{:%d-%m-%Y}'.format(datetime.now()),
            address = user[2],
            serial = user[3],
            number = user[4],
            issued = user[5]
        )
        document.write('static/test.docx')
    return render_template("complete.html")
@app.route('/return-file/')
def return_file():
    return send_file('static/test.docx', attachment_filename='test.docx')

@app.route('/edit_client/<string:id>', methods=['GET', 'POST'])
def edit_client(id):

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE id = %s", [id])
    client = cur.fetchall()
    cur.close()
    form = request.form
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        serial = request.form['serial']
        number = request.form['number']
        issued = request.form['issued']
        cur = mysql.connection.cursor()
        cur.execute ("UPDATE users SET name=%s, address=%s, serial=%s, number=%s, issued=%s WHERE id=%s",(name, address, serial, number, issued, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('users'))
    return render_template('edituser.html', form=client)
    

if __name__ == '__main__':
    app.run(debug=True)