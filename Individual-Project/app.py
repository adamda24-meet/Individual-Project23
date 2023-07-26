from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={"apiKey": "AIzaSyBh1FwzILt8ttA5R5oIkJn5mL01NrJNGr8",
  "authDomain": "adamproject-61546.firebaseapp.com",
  "databaseURL": "https://adamproject-61546-default-rtdb.firebaseio.com",
  "projectId": "adamproject-61546",
  "storageBucket": "adamproject-61546.appspot.com",
  "messagingSenderId": "736680971813",
  "appId": "1:736680971813:web:411e3574268189c79179cc","databaseURL":"https://adamproject-61546-default-rtdb.firebaseio.com/"}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_student'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"full_name":full_name,"username": username ,"bio": bio,"email":email}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_student'))
        except Exception as e:
            print("SIGN UP ERROR:", e)
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/home', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['urname']
        try:
            student= {"name": name }
            db.child("Students").push(student)
            return redirect(url_for('display_users'))
        except:
            print("Couldn't add student")
    return render_template("home.html")

@app.route('/add_student')
def add_student1():
    return render_template("add_student.html")

@app.route("/display_users")
def display_users():
    # Gets all the users from the database
    students = db.child("Students").get().val()
    return render_template("display_users.html", students=students)

@app.route('/delete/<string:uid>')
def delete(uid):
    try:
        # print('db:', db.child("Students").child(UID).get().val())
        print(uid)
        db.child("Students").child(uid).remove()
        return redirect(url_for('display_users'))
    except:
        error = "Couldn’t remove object"
    return render_template('signin.html')


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/all_tweets')
def all_tweets():
    tweets=db.child("Tweets").get().val()
    return render_template("all_tweets.html", tweets=tweets)




#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)