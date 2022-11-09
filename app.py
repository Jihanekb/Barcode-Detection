# import the necessary packages
import datetime
from flask import Flask, render_template, url_for, Response, request, send_from_directory
import numpy as np
import cv2
import time
import os, sys
import barcode_detection

global capture, switch
switch = 1
capture = 0
camera = cv2.VideoCapture(0)

#make shots directory to save pics
try:
    os.mkdir('./static/shots')
except OSError as error:
    pass

app = Flask(__name__)
def generate_frame():
    

    while True:
        # grab the current frame and then handle if the frame is returned
        success, frame = camera.read()
        global capture
        # check to see if we have reached the end of the
        # video
        if success:    
            if(capture):
                capture=0
                p = os.path.sep.join(['static/shots', "Image.png"])
                cv2.imwrite(p, frame)
                image = cv2.imread("static/shots/Image.png")
                barcode_detection.detectimage(image)
        # detect the barcode in the image
        box = barcode_detection.detectvid(frame)
        # if a barcode was found, draw a bounding box on the frame
        if box is not None:
            cv2.drawContours(frame, [box], -1, (0, 255, 0), 3)

        try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
                pass


@app.route('/')
def index():
    return render_template('Page-1.html')

@app.route('/video')
def video():
    return Response(generate_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/processing')
def processing():
    imageList = os.listdir('static/shots')
    #print(imageList)
    #imagelist = ['shots/' + image for image in imageList]
    return render_template("test.html")


@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        request.form.get('click') 
            global capture
            capture=1 

        elif  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0)
                switch=1                 
    elif request.method=='GET':
        return render_template('Page-1.html')
    return render_template('Page-1.html')

if __name__ == "__main__":
    app.run()