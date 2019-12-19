from flask import Flask, render_template, request, send_file
from os import path
from time import sleep
from datetime import date
from fpdf import FPDF

import requests
import json
import wget
import traceback

#Global Vars
NASA_URL = "https://api.nasa.gov/planetary/apod?api_key=DlArxIrdbCsDiAB2mA6Jo4m0PBFrWut8VSnkAQDe"

#Internal Functions
def get_img(tdate):

    if tdate != None:
        url = NASA_URL+"&date="+tdate
    else:
        url = NASA_URL

    response = requests.get(url)
    if response.status_code != 200:
        return 1
    else:
        response = response.text
        response = json.loads(response)
        
        exp = response['explanation']
        title = response['title']
        web_url = response['url']

        return (exp,title,web_url)

def download_image(img_url, tdate):

    try:
        wget.download(img_url, 'downloaded_files/'+tdate+'.jpg')
        return 0
    except Exception:
        traceback.print_exc()
        return 1

def create_pdf(title, tdate, desc):
    pdf = FPDF()
    dpath = "./downloaded_files/"+tdate+".jpg"
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=1, align="C")
    pdf.ln(95)
    pdf.image(name = dpath ,x=55, y=20, h=100, w=100)
    pdf.ln()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 5, desc, align="C")
    pdf.output("./downloaded_files/"+tdate+".pdf")

#Main Program starts here

app = Flask(__name__)

#Default Route
@app.route('/') 
def main():
    return render_template('index.html')

#Displays Pic of the day and related info
@app.route('/pod')
def pod():
    tdate = request.args.get('date')
    if tdate == None:
        tdate = str(date.today())
    info = get_img(tdate)
    #Check for error
    if info == 1:
        return render_template('error_404.html'),404
    url = info[2]
    title = info[1]
    expl = info[0]
    img_download = "/download_img?date=" + tdate
    pdf_download = "/download_pdf?date=" + tdate
    return render_template('details.html', title=title, desc=expl, img_url=url, pdf_download_url = pdf_download, img_download_url = img_download)

#Downloads the Image
@app.route('/download_img')
def download_img():
    tdate = request.args.get('date')
    url = get_img(tdate)
    url = url[2]
    if path.exists("./downloaded_files/"+tdate+".jpg") == False:
        rcode = download_image(url, tdate)
        if rcode != 0:
            return render_template("error.html"), 500
        else:
            return send_file("./downloaded_files/"+tdate+".jpg", as_attachment=True)
    else:
        return send_file("./downloaded_files/"+tdate+".jpg", as_attachment=True)

#Downloads the PDF
@app.route('/download_pdf')
def download_pdf():
    tdate = request.args.get('date')
    img_info = get_img(tdate)
    url = img_info[2]
    exp = img_info[0]
    title = img_info[1]
    if path.exists("./downloaded_files/"+tdate+".pdf") == False:

        if path.exists("./downloaded_files/"+tdate+".jpg") == False:
            rcode = download_image(url, tdate)
            if rcode != 0:
                return render_template("error.html"), 500
            else:
                create_pdf(title, tdate, exp)
                return send_file("./downloaded_files/"+tdate+".pdf", as_attachment=True)
        else:
            create_pdf(title, tdate, exp)
            return send_file("./downloaded_files/"+tdate+".pdf", as_attachment=True)
    else:
        return send_file("./downloaded_files/"+tdate+".pdf", as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)