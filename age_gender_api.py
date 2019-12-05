import os
import glob
import shutil
import base64
import uuid
import time
from PIL import Image
from flask import Flask
from flask import Flask, request, redirect
from flask_cors import CORS, cross_origin
import requests
from flask import make_response
from pyagender import PyAgender
import cv2
from keras import backend as K
#set FLASK_ENV=development
app = Flask(__name__)
cors = CORS(app, allow_headers='*')
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/faceanalytics/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def img_clss():
    new_file_id=uuid.uuid1() 
    try:
        data_file = request.files['img']
        file_name = data_file.name
        data_file.save(f'{os.getcwd()}/images/{data_file.filename}')
        data_file.close()    
        img_file = os.listdir(f'{os.getcwd()}/images/')       
        print('Image ',img_file[0])
        
        agender = PyAgender() 
        path = os.path.join(f'{os.getcwd()}/images/', img_file[0])
        print('Path ', path)
        faces = agender.detect_genders_ages(cv2.imread(path))
        print('Faces ',faces)
        if faces[0]['gender'] < 0.5:
            faces[0]['gender'] = 'male'
        else:
            faces[0]['gender'] = 'female'
        faces[0]['age'] = str(faces[0]['age'] ).split('.')[0]
        print(faces[0])
        resp = make_response(faces[0])
        resp.headers.set('Content-Type','multipart/form-data')
        print('Response ', resp)
        return resp

    except Exception as e:
        print(e)
        try:
            # Camera capture
            path1 = f'{os.getcwd()}/images/'
            image_string = str(request.form.get('file_string'))
            image_newstring = image_string.replace("data:image/jpeg;base64,", "") 
            imgdata = base64.b64decode(image_newstring)
            filename = os.path.join(path1 , new_file_id.hex+'.jpg')
            with open(filename, 'wb') as f:
                f.write(imgdata)
                f.close()
            img_file = os.listdir(f'{os.getcwd()}/images/')
            print('Image ',img_file[0])
            
            agender = PyAgender() 
            path = os.path.join(f'{os.getcwd()}/images/', img_file[0])
            print('Path ',path)
            faces = agender.detect_genders_ages(cv2.imread(path))
            print('Faces ' ,faces)
            if faces[0]['gender'] < 0.5:
                faces[0]['gender'] = 'male'
            else:
                faces[0]['gender'] = 'female'
            faces[0]['age'] = str(faces[0]['age'] ).split('.')[0]
            print(faces[0])
            resp = make_response(faces[0])
            resp.headers.set('Content-Type','multipart/form-data')
            target_dir=f'{os.getcwd()}/images/'
            with os.scandir(target_dir) as entries:
                for entry in entries:
                    time.sleep(1)
                    if entry.is_file() or entry.is_symlink():
                        os.remove(entry)
            print('Response ', resp)
            return resp
            
        except Exception as e:
            print(e)
            print("Something went wrong with your image. Kindly try with different image")
       
    finally:
        target_dir=f'{os.getcwd()}/images/'
        with os.scandir(target_dir) as entries:
            for entry in entries:
                time.sleep(1)
                print(entry)
                if entry.is_file() or entry.is_symlink():
                    os.remove(entry)
        print("Image Deleted")
#K.clear_session()        
app.run(host='172.19.50.38',port=8000, threaded=False)# change IP as per the hosting machine 