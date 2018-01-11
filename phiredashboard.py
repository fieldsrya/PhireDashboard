#!/usr/local/bin/python3
from flask import Flask, render_template, jsonify, request, json, redirect, session, make_response
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_required
import cx_Oracle
import json
import cr
import refreshProj
import requests
from datetime import datetime, timedelta

LOGIN_URL='https://cs.manage.catalystnpd.uc.edu/psp/ps/EMPLOYEE/HRMS/?&cmd=login&languageCd=ENG'

app = Flask(__name__)
app.secret_key = 'b"\x00\xf4\xe46\xdc \xe9\xb6L\xe8\xfcx/\x18\xc7\xacq\xa7\xd8\x8b\x18\xdb\xea'
Bootstrap(app)

@app.route("/dash/refreshProj", methods=['GET','POST'])
#@login_required
def getRefreshProjects():
  if 'username' in session:
    if 'testEnvironment' in request.args:
      environment = request.args.get('testEnvironment')
      return refreshProj.getProjects(environment)
    return "No Value Given for env!!"
  return "You are not Logged In!"

@app.route("/dash/openCR")
#@login_required
def openCRPage():
  if 'username' in session:
    return cr.getOpenCRs(session['username'])
  return "You are not Logged In!"

@app.route("/dash/openIssues")
#@login_required
def openIssuesPage():
  if 'username' in session:
    return cr.getOpenIssues(session['username'])
  return "You are not Logged In!"

@app.route("/dash/dispIssues")
#@login_required
def showOpenIssues():
  if 'username' in session:
    return render_template('openIssues.html')
  return "You are not Logged In!"

@app.route("/dash/refreshIssues", methods=['GET','POST'])
#@login_required
def refreshIssues():
  if 'username' in session:
    return render_template('refreshProjects.html')
  return "You are not Logged In!"


@app.route("/dash/login", methods=['POST'])
def usersLogin():
  _name = request.form['inputName']
  _password = request.form['inputPassword']
  session['username'] = _name
  session['password'] = _password
  cookie_expire = datetime.now()
  cookie_expire = cookie_expire + timedelta(seconds=5)
  if _name and _password:
    resp = make_response(redirect("/dash/dispIssues"))
    payload = {'userid': _name, 'pwd': _password}
    with requests.Session() as s:
      s.post(LOGIN_URL, data=payload)
      cj = s.cookies.get_dict()
    for c, cvalue in cj.items():
      resp.set_cookie(c, value=cvalue, max_age=18000, domain='.manage.catalystnpd.uc.edu',secure=True)
    return resp
  else:
    return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route("/dash")
def main():
  return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
