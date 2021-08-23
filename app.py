from flask import Flask, render_template,request
import requests
from bs4 import BeautifulSoup
import sys


# if (jobCounter == 0):
#     print("No jobs found!")

app = Flask(__name__)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/results', methods = ['POST', 'GET'])
def index():
    URL = "https://*.com/jobs?q=Intern&sort=date&limit=50&fromage=7"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="mosaic-zone-jobcards")
    jobCounter = 0
    jobResults = []

    def checkText(string):
        try:
            return string.lower()
        except:
            return ""

    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form.to_dict()
        category = form_data['Category']
        category = category.lower()

        job_elements = results.find_all("a", class_="resultWithShelf")
        filtered_jobs = results.find_all("span", string=lambda text: category in checkText(text))

        filtered_jobs_info = [span.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent for span in filtered_jobs]

        for job in filtered_jobs_info:
            title_element = job.find("h2", class_="jobTitle").find("span", class_=lambda x: x != 'label')
            company_element = job.find("span", class_="companyName")
            apply_link = job['href']
            jobResults.append({
                "title": title_element.text,
                "company": company_element.text,
                "link": "*.com" + apply_link,
            })
            jobCounter += 1
        return render_template('results.html',results=jobResults)
    # return render_template('results.html', results=jobResults)