from flask import Flask, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from pdf2image import convert_from_path, convert_from_bytes 
import cv2
from PIL import Image
import pytesseract
import easyocr
from pytesseract import Output
from matplotlib import pyplot as plt
import numpy as np

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
custom_config = r'--oem 1 --psm 6'

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
  return 'Hello world!'

@app.route('/uploader', methods = ['POST'])
def upload_file():
  # try:
    if request.method == 'POST':
      if 'file' not in request.files:
        return 'No file part'

      f = request.files['file']
      if f.filename == '':
        return "No file selected"
      
      if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        pages = convert_from_bytes(f.read(), 500)
        page = pages[0]
        img = np.array(page)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        invert = 255 - thresh

        img = invert
        output = ""
        print(img.shape)

        # top
        y=700
        x=0
        h=550
        w=4134
        crop = img[y:y+h, x:x+w]
        crop = cv2.resize(crop, (crop.shape[1]*2, crop.shape[0]*2))
        x = pytesseract.image_to_string(crop,config=custom_config, lang='eng')
        # print(x)
        output += x
        # cv2.imwrite('top.jpg', crop)

        # left
        y=1250
        x=0
        h=4597
        w=2067

        crop = img[y:y+h, x:x+w]
        # cv2.imwrite('left.jpg', crop)
        crop = cv2.resize(crop, (crop.shape[1]*2, crop.shape[0]*2))
        x = pytesseract.image_to_string(crop,config=custom_config, lang='eng')

        # print(x)
        output += x

        # right
        y=1250
        x=2067
        h=4597
        w=2067
        crop = img[y:y+h, x:x+w]
        # cv2.imwrite('right.jpg', crop)
        crop = cv2.resize(crop, (crop.shape[1]*2, crop.shape[0]*2))
        x = pytesseract.image_to_string(crop,config=custom_config, lang='eng')
        # print(x)
        output += x
        return output

  # except:
  #    return 'Error'

app.run(host='localhost', port=8000, debug=True)