#!/root/poc-6666/proj1/proj1/virtualenv/bin/python3
import os
from flask import Flask, redirect, request, url_for, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv("db_root_password")
app.config['MYSQL_DB'] = "Customer"

mysql = MySQL(app)

@app.route('/')
def redirect_index():
    return render_template("index.html")

@app.route('/read_customer')
def read_customer():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM cust ''')
        rs = cursor.fetchall()
        print(rs)
        if request.args:
            return render_template('read.html', customers=rs, message=request.args["message"])
        else:
            return render_template('read.html', customers=rs)
        cursor.close
    except ConnectionError as c:
        return render_template('error.html', err=c.args)
    except Exception as e:
        print(e)
        return render_template('error.html', err=e.args[0])

@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'GET':
        return render_template("create.html")
    else:
        name = request.form["name"]
        surname = request.form["surname"]
        DOB = request.form["DOB"]
        address = request.form["address"]
        try:
            cursor = mysql.connection.cursor()
            query = "insert into cust (c_name, c_surname, c_dob, c_address) values (%s,%s,%s,%s)"
            data = (name,surname,DOB,address)
            cursor.execute(query,data)
            mysql.connection.commit()
            return redirect(url_for('read_customer',message="Customer Created Successfully"))
        except ConnectionError as c:
            return render_template('error.html', err=c.args)
        except Exception as e:
            return render_template('error.html', err=e.args[0])
        finally:
            cursor.close()

@app.route('/update_customer', methods = ["GET", "POST"])
def update_customer():
    if request.method == 'GET':
        return render_template("update.html")
    else:
        eid = request.form["eid"]
        name = request.form["name"]
        surname = request.form["surname"]
        DOB = request.form["DOB"]
        address = request.form["address"]
        try:
            cursor = mysql.connection.cursor()
            query = f"select count(*) from cust where id = {eid} "
            cursor.execute(query)
            rs=cursor.fetchone()
            print(rs)
            if rs[0]:
                query = "update cust set c_name=%s, c_surname=%s, c_dob=%s, c_address=%s where id = %s"
                data = (name, surname, DOB, address,eid)
                cursor.execute(query, data)
                mysql.connection.commit()
            else:
                raise Exception("Invalid ID")
            return redirect(url_for('read_customer'))
        except ConnectionError as c:
            return render_template('error.html', err=c.args)
        except Exception as e:
            return render_template('error.html', err=e.args[0])
        finally:
            cursor.close()

@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if request.method == 'GET':
        return render_template('delete.html')
    else:
        eid = request.form["eid"]
        try:
            cursor = mysql.connection.cursor()
            query = f"delete from cust where id = {eid}"
            cursor.execute(query)
            mysql.connection.commit()
            if cursor.rowcount:
                return redirect(url_for('read_customer', message="Customer Deleted Successfuly"))
            else:
                raise Exception("Invalid ID")
        except ConnectionError as c:
            return render_template('error.html', err=c.args)
        except Exception as e:
            return render_template('error.html', err=e.args[0])
        finally:
            cursor.close()


if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
