from flask import Flask, render_template, request, session, redirect, url_for
import ibm_db
from PyPDF2 import PdfFileReader
from gensim.summarization import summarize

app = Flask(__name__)
app.secret_key = 'Kabilan0021@'
 
conn = ibm_db.connect("DATABASE = bludb;HOSTNAME = b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud; PORT = 31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt; UID = clq78863; PASSWORD = c1xTE3BxdSUtpas2 ", "", "")
print("Connection Succesfull")

# Routes
@app.route('/')
def home():
    return render_template('index.html')



@app.route("/login", methods = ['GET', 'POST'])
def login():
    global u_name,u_pass,conn
    if request.method == 'POST':
        u_name = request.form["uname"]
        u_pass = request.form['pword']
        #print("The name of the user : {} and password : {}". format(u_name, u_pass))
        if not ibm_db.active(conn):
            conn = ibm_db.connect("DATABASE = bludb;HOSTNAME = b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud; PORT = 31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt; UID = clq78863; PASSWORD = c1xTE3BxdSUtpas2", "", "")

        sql  = "SELECT * from USERS WHERE USERNAME =  ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, u_name)
        ibm_db.bind_param(stmt, 2, u_pass)
        ibm_db.execute(stmt)
        info = ibm_db.fetch_assoc(stmt)
        print(info)
        if info : 
            session['id'] = True
            session['username'] = u_name

            return redirect(url_for("home"))
        else:
            msg_w = "Check the Email and Password you have entered"
            return render_template("login.html", msg_w = msg_w ) 
            
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    global conn
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not ibm_db.active(conn):
            conn = ibm_db.connect("DATABASE = bludb;HOSTNAME = b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud; PORT = 31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt; UID = clq78863; PASSWORD = c1xTE3BxdSUtpas2", "", "")

        # Insert new user into the database
        query = f"INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?, ?)"
        stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        ibm_db.commit(conn)
        ibm_db.close(conn)

        return render_template('login.html')

    return render_template('register.html')

@app.route('/summarize', methods=['POST'])
def summarize_text():
    # Get uploaded file from the request
    file = request.files['pdf_file']

    # Read the PDF file
    pdf = PdfFileReader(file)
    text = ""

    # Extract text from each page of the PDF
    for page in range(pdf.getNumPages()):
        text += pdf.getPage(page).extractText()

    # Summarize the text
    summary = summarize(text)

    # Render the template with the summary
    return render_template('summary.html', summary=summary)



if __name__=="__main__":
    app.run(debug=True)