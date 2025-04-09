import requests
from flask import Flask, render_template_string, request, send_file
import os
from datetime import datetime

app = Flask(__name__)

def get_location(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url)
        data = response.json()

        city = data.get("city", "Brak informacji")
        region = data.get("region", "Brak informacji")
        country = data.get("country", "Brak informacji")
        loc = data.get("loc", "Brak informacji")

        return city, region, country, loc
    except:
        return "Brak informacji", "Brak informacji", "Brak informacji", "Brak informacji"

@app.route('/')
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    city, region, country, loc = get_location(user_ip)

    with open("log.txt", "a") as log:
        log.write(f"[{datetime.now()}] IP: {user_ip}, Miasto: {city}, Region: {region}, Kraj: {country}, Lokacja: {loc}\n")

    html_content = """
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hello</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                text-align: center;
            }
            .container {
                margin-top: 50px;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                width: 80%;
                max-width: 500px;
                margin-left: auto;
                margin-right: auto;
            }
            h1 {
                color: #333;
            }
            .button {
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                cursor: pointer;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 20px;
            }
            .button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello</h1>
            <p>Kliknij poniżej, aby pobrać plik:</p>
            <a href="/download" class="button">Pobierz plik</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/download')
def download_file():
    file_path = "/data/data/com.termux/files/home/cupp/wordlists/maks.txt"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Plik nie został znaleziony", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)