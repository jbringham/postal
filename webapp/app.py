"""
This file contains <TODO>

Team 5 - Postalrific

Names:
    Jacob Bringham
    Parth Parikh
    Jacob Campbell
    Jack Button
"""

from flask import Flask, render_template, request, redirect, flash
import psycopg2 as psycopg
from psycopg2.errors import NumericValueOutOfRange 
import json
import re


config = json.load(open("config.json", "r"))
conn = psycopg.connect(f"host={str(config['host'])} dbname=postal user={str(config['user'])} password={str(config['password'])}") 
cur = conn.cursor()

app = Flask(__name__, template_folder="template")
app.secret_key = "postal"

@app.route("/agi", methods=["GET", "POST"])
@app.route("/agi.html", methods=["GET", "POST"])
def agi():
    if request.method == "POST":
        agi_per_county = request.form.get("agi_per_county").strip()

        if re.match("^-?\d+(\.\d+)?$", agi_per_county) is None:
            flash("AGI must be numeric!")
            return render_template("agi.html")

        try:
            cur.execute("SELECT * FROM counties_with_agi_lt(%s);", (agi_per_county,)) 
            agi = cur.fetchall()
        except NumericValueOutOfRange:
            conn.rollback()
            flash("Input was too large!")
            return render_template("agi.html")
        
        if len(agi) >= 1:
            return render_template("agi.html", agi_per_county=agi_per_county, agi=agi)
        else:
            flash(f"Database did not contain results for '{agi_per_county}'")
            return render_template("agi.html", agi_per_county=agi_per_county)

    else:
        return render_template("agi.html")


@app.route("/")
@app.route("/index.html")
def index():
    """
    Handles serving the home page for our application.
    """
    return render_template("index.html")


@app.route("/comp", methods=["GET", "POST"])
@app.route("/compind.html", methods=["GET", "POST"])
def compIndex():
    if request.method == "POST":
        compind = request.form.get("compind") 

        if re.match("^-?\d+(\.\d+)?$", compind) is None:
            flash(f"Comp Index must be numeric!")
            return render_template("compind.html")

        cur.execute("SELECT * FROM counties_with_compind_lt(%s)", (compind,)) 
        comp = cur.fetchall()
        return render_template("compind.html", compind=compind, comp=comp)
    else:
        return render_template("compind.html")

@app.route("/popCapita", methods=["GET", "POST"])
@app.route("/pop_capita.html", methods=["GET", "POST"])
def pop_per_cap():
    if request.method == "POST":
        pop_per_capita = request.form.get("pop_per_capita") 

        if re.match("^\d+$", pop_per_capita) is None:
            flash(f"Population per capita must be a positive whole number!")
            return render_template("pop_capita.html")

        cur.execute("SELECT * FROM counties_with_population_capita(%s);", (pop_per_capita,)) 
        pop = cur.fetchall()
        return render_template("pop_capita.html", pop_per_capita=pop_per_capita, pop=pop)
    else:
        return render_template("pop_capita.html")

@app.route("/cont_disct", methods=["GET", "POST"])
@app.route("/cont_disct.html", methods=["GET", "POST"])
def postOffice_by_year():
    if request.method == "POST":
        year = request.form.get("year") 

        if re.match("^\d+$", year) is None:
            flash(f"Year must be a positive whole number!")
            return render_template("cont_disct.html")

        cur.execute("SELECT * FROM counties_with_established_offices(%s);", (year,)) 
        established = cur.fetchall()
        return render_template("cont_disct.html", year=year, established=established)
    else:
        return render_template("cont_disct.html")

race_dict = {"white" : 5, "african_american" : 6, "asian": 7, "other_pop" : 8}

@app.route("/officeCapita", methods=["GET", "POST"])
@app.route("/office_capita.html", methods=["GET", "POST"])
def office_per_cap():
    if request.method == "POST":
        offices_per_capita = request.form.get("offices_per_capita")
        
        if re.match("^\d+$", offices_per_capita) is None:
            flash(f"Offices per capita must be a positive whole number!")
            return render_template("office_capita.html")

        race = request.form.get("race")  
        cur.execute("SELECT * FROM counties_with_races_capita(%s);", (offices_per_capita,)) 
        county_with_race = cur.fetchall()

        # Check if race in race_dict
        if not race in race_dict:
            flash(f"Please select one of the dropdown items!")
            return render_template("office_capita.html")

        return render_template("office_capita.html", \
            offices_per_capita=offices_per_capita, race_str=race.title(), race=int(race_dict[race]), county_with_race=county_with_race)
    else:
        return render_template("office_capita.html")
 

