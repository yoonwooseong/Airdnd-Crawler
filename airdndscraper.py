from flask import Flask, render_template, request, redirect
from airbnbsearchlist import get_accommodation_infos
from airbnbdetail import extract_detail

app = Flask("SuperScrapper")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/scrape")
def scrape():
    place = request.args.get('place')
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')
    Query = {'place':place, 'checkin':checkin, 'checkout':checkout}
    if place:
        accommodation_infos = get_accommodation_infos(Query)
        extract_detail(accommodation_infos)

    else:
        return redirect("/")
    return render_template("scrapepage.html", searchingBy=place)

app.run(host="localhost")