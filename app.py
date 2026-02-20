from flask import Flask, render_template, request , session , url_for,redirect
import sqlite3 as sq

password = "mypassword123"


app = Flask(__name__)
app.secret_key="123"

@app.route("/signup",methods=["GET", "POST"])
def signUp():
        msg = None  
        if request.method == "POST":
            name = request.form.get("name")
            password = request.form.get("password")

            conn = sq.connect("date.db") 
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS login (USERNAME TEXT UNIQUE, PASSWORD BLOB)"
            )
            
            try:
                cursor.execute(
                    "INSERT INTO login (USERNAME, PASSWORD) VALUES (?, ?)", (name, password)
                )
                conn.commit()
                msg = "successfully"  
                session["login"] = name
                return redirect(url_for("home"))
            except sq.IntegrityError:
                msg ="This name has taken. Try anthor name pleas "
         
            conn.close()

        return render_template('sign_up.html', msg=msg )

@app.route("/signin",methods=["GET", "POST"])
def signIn():
    msg = None 

    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        conn = sq.connect("date.db")
        cursor = conn.cursor()

        cursor.execute("SELECT PASSWORD FROM login WHERE username = ?", (name,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            if password == stored_password:  # <-- فحص كلمة المرور هنا
                session["login"] = name
                return redirect(url_for("home"))
            else:
                msg = "كلمة المرور غلط"
        else:
            msg = "الاسم غير موجود"

        conn.close()

    return render_template("sign_in.html", msg=msg)
@app.route("/")
def home():
    if "login" not in session:
        return redirect(url_for("signIn"))
    conn = sq.connect("date.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS the_note(id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT,user  )")
    cursor.execute("SELECT note FROM the_note WHERE user=?",(session['login'],))
    notes=cursor.fetchall()   
    
    conn.commit()
    conn.close()     
    return render_template('home.html',notes=notes)

@app.route("/logout")
def logout():
     session.clear()
     return redirect(url_for("signIn"))

@app.route("/add-note",methods=["GET", "POST"])
def note():
    if "login" in session:    
        if request.method=="POST":  

            conn = sq.connect("date.db")
            cursor = conn.cursor()
            note= request.form.get("note")
            
            cursor.execute("INSERT INTO the_note(note,user) VALUES(?,?)", (note,session['login']))
            conn.commit()
            conn.close() 
            return redirect(url_for("home"))
        return render_template('add.html')
    else:
         msg="you have to sign in first "
         return redirect(url_for("signIn"))
          
app.run(debug=True)

