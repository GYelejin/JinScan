from flask import Flask, render_template, request, redirect, url_for
from scanner import ScanProfile
from db import *

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/profiles")
def profiles():
    profiles = get_profiles()
    return render_template("profiles.html", profiles=profiles)

@app.route("/results")
def results():
    results = get_scan_results()[::-1]
    return render_template("results.html", results=results)

@app.route("/scan_report/<int:scan_id>")
def scan_report(scan_id):
    scan_result = get_scan_report(scan_id)
    return render_template("scan_report.html", scan_result=scan_result)

@app.route("/add_profile")
def add_profile():
    return render_template("add_profile.html")

@app.route("/add_profile", methods=["POST"])
def add_profile_submit():
    login = request.form["login"]
    password = request.form["password"]
    port = request.form["port"]
    host = request.form["host"]
    profile = ScanProfile(login, password, host, port)
    scan_profile(profile)
    return redirect(url_for('profiles'))

@app.route("/delete_profile", methods=["POST"])
def delete_profile_route():
    profile_id = request.form["profile_id"]
    delete_profile(profile_id)
    return redirect(url_for('profiles'))

@app.route("/scan", methods=["POST"])
def scan():
    profile_id = request.form["profile_id"]
    row = get_profile(profile_id)[0]
    profile = ScanProfile(*row)
    scan_id = scan_profile(profile, profile_id=profile_id)
    return redirect(url_for('scan_report', scan_id=scan_id))

if __name__ == "__main__":
    create_tables()
    app.run()
