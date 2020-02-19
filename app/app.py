import os
from flask import Flask, flash, request, redirect, url_for ,session , jsonify
from werkzeug.utils import secure_filename
import mysql.connector
import json
import asyncio
from io import BytesIO
# from fastai import *
# from fastai.vision import *
import copy 


from PIL import Image
import torch
from ResNet import *
from Config import *

import torch.nn as nn
from torch.autograd import Variable
import torchvision.transforms.functional as F




class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

# UPLOAD_FOLDER = '/Users/wooseungjin/Documents/dockerSettingTest/second/app/downloads'
# UPLOAD_FOLDER = '/app'
UPLOAD_FOLDER = '/app/downloads'


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['upload_folder'] = UPLOAD_FOLDER


config_server = {
        'user': 'root',
        'password': 'hy940817',
        'host': 'db',
        # 'host' : 'localhost',
        'port': '3306',
        'database': 'plants_db',
        'auth_plugin':'mysql_native_password'
    }

# classes = ['anthurium_bacterialblight',
#   'anthurium_bacterialwilt',
#   'anthurium_blacknose',
#   'anthurium_healthy',
#   'anthurium_phytophthorapythium',
#   'anthurium_rhizoctoniarootrot',
#   'crotons_healthy',
#   'crotons_mealybugs',
#   'crotons_scaleinsects',
#   'dracaenamarginata_healthy',
#   'dracaenamarginata_insectpests',
#   'dracaenamarginata_soil',
#   'dracaenamarginata_temperature',
#   'goldenpothos_bacterialleafspot',
#   'goldenpothos_bacterialwilt',
#   'goldenpothos_healthy',
#   'goldenpothos_phytophthoraroorot',
#   'luckyboomboo_bamboomites',
#   'luckyboomboo_healthy',
#   'luckyboomboo_powderymildew',
#   'mothorchid_bacterialbrownspot',
#   'mothorchid_blackrot',
#   'mothorchid_botrytis',
#   'mothorchid_healthy',
#   'peacelily_healthy',
#   'peacelily_insectinfection',
#   'peacelily_lackofwater',
#   'peacelily_overwatering',
#   'peacelily_sunburn',
#   'ponytailpalm_bugs',
#   'ponytailpalm_cylindrocladium',
#   'ponytailpalm_healthy',
#   'snakeplant_brownspots',
#   'snakeplant_healthy',
#   'snakeplant_wateroversupply',
#   'syngonium_bacterialleafblight',
#   'syngonium_bacterialstemrot',
#   'syngonium_healthy']

path = '/app'
model_file_name = 'plantDoctorModel'
# model_file_name = 'ResNet34_50_model'



# async def setup_learner():
#     data_bunch = ImageDataBunch.single_from_classes(path, classes,
#         ds_tfms=get_transforms(), size=224).normalize(imagenet_stats)
#     learn = cnn_learner(data_bunch, models.resnet34, pretrained=False)
#     learn.load(model_file_name)
#     return learn

# loop = asyncio.get_event_loop()
# tasks = [asyncio.ensure_future(setup_learner())]
# learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
# loop.close()


device = torch.device("cpu")


# initialize training configuration
config = Config()

net = resnet50(num_classes = config.classes).to(device)

net.load_state_dict(torch.load(os.path.join(config.net_base_path, config.net),map_location=device)['model'])
net = net.to(device)

# evaluation mode
net.eval()

sig = nn.Sigmoid()




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/classify', methods=['GET','POST'])
def classify():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({'result': "no file"})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return jsonify({'result': "no selected file"})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['upload_folder'], filename))
            # with open(UPLOAD_FOLDER+"/"+filename, 'rb') as f:
            #     img_bytes = f.read()
            # img = open_image(BytesIO(img_bytes))
            # predicted = str(learn.predict(img)[0])
            
            img = Image.open(UPLOAD_FOLDER+"/"+filename)
            img_resize = img.resize((224,224))
            img_tensor = F.to_tensor(img_resize).unsqueeze(0)

            img_features = net.forward(Variable(img_tensor).to(device))

            score, predicted = torch.max(img_features, 1)

            if sig(score) < config.threshold:
                return jsonify({"result":"wrongImange"})

            print(config.accuracy[predicted])
            
            resultOfNetwork=config.accuracy[predicted]
            
            split_data = resultOfNetwork.split("_")
            plant_name = split_data[0]
            plant_disease = split_data[1] 
            vallidationAC = split_data[2]
            
            connection = mysql.connector.connect(**config_server)
            cursor = connection.cursor()
            cursor.execute('INSERT INTO results (plant_name , disease_name , file_name) VALUES (%s,%s,%s)' , (plant_name,plant_disease,filename))
            connection.commit()
            cursor.close()
            connection.close()
            
            result = plant_name+","+plant_disease
            
            return jsonify({"result":result})

    return jsonify({'result': "get"})


def get_plants_information():
    connection = mysql.connector.connect(**config_server)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM plants')
    results = [{plant_name,plant_information} for ( plant_id, plant_name, plant_information) in cursor]
    cursor.close()
    connection.close()

    return results

@app.route('/getPlantsData')
def getPlantsData():
    return json.dumps(get_plants_information(), cls=SetEncoder)


def get_diseases_information():
    connection = mysql.connector.connect(**config_server)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM diseases')
    results = [{disease_name,plant_name,disease_symptoms,disease_treatment} for (disease_name,plant_name,disease_symptoms,disease_treatment) in cursor]
    cursor.close()
    connection.close()

    return results

@app.route('/getDiseasesData')
def getDiseasesData():
    return json.dumps(get_diseases_information(), cls=SetEncoder)

def get_results():
    connection = mysql.connector.connect(**config_server)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM results')
    results = [{plant_name,disease_name,file_name} for (result_id ,plant_name,disease_name,file_name) in cursor]
    cursor.close()
    connection.close()

    return results

@app.route('/admin/getResults')
def getResults():
    return json.dumps(get_results(), cls=SetEncoder)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
