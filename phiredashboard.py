from flask import Flask, render_template, jsonify, request, json, redirect, session
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_required
import cx_Oracle
import json
import cr

app = Flask(__name__)
app.secret_key = 'b"\x00\xf4\xe46\xdc \xe9\xb6L\xe8\xfcx/\x18\xc7\xacq\xa7\xd8\x8b\x18\xdb\xea'
Bootstrap(app)

@app.route("/openCR")
#@login_required
def openCRPage():
  if 'username' in session:
    return cr.getOpenCRs(session['username'])
  return "You are not Logged In!"

@app.route("/openIssues")
#@login_required
def openIssuesPage():
  if 'username' in session:
    return cr.getOpenIssues(session['username'])
  return "You are not Logged In!"

@app.route("/dispIssues")
#@login_required
def showOpenIssues():
  if 'username' in session:
    return render_template('openIssues.html')
  return "You are not Logged In!"

@app.route("/login", methods=['POST'])
def usersLogin():
  _name = request.form['inputName']
  _password = request.form['inputPassword']
  session['username'] = _name
  if _name and _password:
    return redirect("/dispIssues")
  else:
    return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route("/")
def main():
  return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
