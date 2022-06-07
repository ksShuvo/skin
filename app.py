import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash, jsonify
from PIL import Image
import datetime
import re
import base64
from flask_cors import CORS
from io import BytesIO

from predict_model import predict


app = Flask(__name__)
# app = Flask(__name__, static_folder="images")
CORS(app)
app.config['SECRET_KEY'] = "myspecial"



APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return img

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST","GET"])
def upload():
    if request.method == 'GET':
        flash("this method is not allowed","error")
        return redirect(url_for('index'))

    target = os.path.join(APP_ROOT, 'images/')
    
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print("\n\n>>",request.files.getlist("file"),"<<\n\n")

    uploaded_file = request.files.getlist("file")[0]
    print(">>>",uploaded_file.filename)
    if uploaded_file.filename == '':
        flash("invalid file","error")
        return redirect(url_for("index"))
    
    print("{} is the file name".format(uploaded_file.filename))
    filename = uploaded_file.filename

    time = str(datetime.datetime.today().strftime('%H-%M-%S'))
    date = str(datetime.date.today())
    extension = os.path.splitext(filename)[1]

    new_file_name = time + "_" + date + extension

    destination = "/".join([target, new_file_name])
    print ("Accept incoming file:", filename)
    print ("Save it to:", destination)
    uploaded_file.save(destination)


    # for upload in request.files.getlist("file"):
    #     print(upload)
    #     print("{} is the file name".format(upload.filename))
    #     filename = upload.filename
    #     destination = "/".join([target, filename])
    #     print ("Accept incoming file:", filename)
    #     print ("Save it to:", destination)
    #     upload.save(destination)


    print("\n\n\n---------",destination)
    
    ans = predict(destination)

    print("\n\n\n",ans,"\n\n\n")

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete_display_image.html", image_name=new_file_name, ans = ans)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)

# @app.route('/result/<filename>')
# def show_result(filename):
#     image_name = filename
#     print("filename",filename)
#     return render_template("complete_display_image.html",image_name = image_name)


@app.route("/upload1", methods=["POST","GET"])
def process_image1():
    if request.method == 'GET':
        return jsonify({"ans" : "this method is not allowed"}),405
    file = request.form['image']

    if file == 'null':
        return jsonify({"ans" : "image is not valid"})

    target = os.path.join(APP_ROOT, 'images/')

    print("\n\n target",target,"\n\n")

    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))

    time = str(datetime.datetime.today().strftime('%H-%M-%S'))

    date = str(datetime.date.today())

    file_name = new_file_name = time + "_" + date + '.jpg'

    destination = "/".join([target,file_name])

    img = base64_to_image(file, destination)

    ans = predict(destination)

    return jsonify({"ans" : ans})

if __name__ == "__main__":
    app.run(port=4555, debug=True)
