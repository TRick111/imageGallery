import os
import requests
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)
staticFilePath = "./static/images/"

snapshotURL = 'http://192.168.100.123:8080/?action=snapshot'

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        if request.form.get('action') == "snapshot":
            try:
                r_image = requests.get( snapshotURL )
                filename = datetime.datetime.now().strftime("%m%d_%H:%M:%S")
                with open( staticFilePath + f'{filename}.jpeg', 'wb' ) as f:
                    f.write( r_image.content )
            except requests.exceptions.ConnectionError as e:
                message = "ストリーミングサーバーとの接続に失敗しました" 
                print( e )       

    imageNames = os.listdir( staticFilePath )
    imageNames.sort( key=lambda s: os.path.getctime(os.path.join(staticFilePath, s) ) )
    return render_template( "index.html", images = imageNames, message = message, filePath = staticFilePath )

