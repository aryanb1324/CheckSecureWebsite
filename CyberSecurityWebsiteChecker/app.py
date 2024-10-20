from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

# Initialize Flask app
app = Flask(__name__)

# Define routes
@app.route('/')
def home():
    return render_template('index.html')

# Test route (used for debugging)
@app.route('/test')
def test():
    return "<h1>Test Page</h1>"

# Scan route (handles form submission)
@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    if not is_valid_url(url):
        return render_template('error.html', error="Invalid URL provided.")
    try:
        response = requests.get(url)
        html_content = response.text
        vulnerabilities = check_vulnerabilities(html_content, response)
        return render_template('results.html', vulnerabilities=vulnerabilities)
    except requests.exceptions.RequestException as e:
        return render_template('error.html', error=str(e))

# Helper function to validate URL
def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

# Helper function to check for vulnerabilities
def check_vulnerabilities(html_content, response):
    vulnerabilities = []
    soup = BeautifulSoup(html_content, 'html.parser')

    # Check fo  r missing HTTPS
    if not response.url.startswith('https'):
        vulnerabilities.append("Missing HTTPS")

    # Check for insecure form action
    forms = soup.find_all('form')
    for form in forms:
        if form.get('action') and not form['action'].startswith('https'):
            vulnerabilities.append("Insecure form action")

    # Check for missing Content Security Policy
    if 'Content-Security-Policy' not in response.headers:
        vulnerabilities.append("Missing Content Security Policy")

    return vulnerabilities

# Run the app!!
if __name__ == '__main__':
    app.run(debug=True)
