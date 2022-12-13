from flask import Flask, render_template, url_for, request, redirect
from flask import session as login_session
import pyrebase
import os

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)
Config = {
  'apiKey': "AIzaSyBQYtiUyRAcXiQ8qLyyCkdiI6AF83pb0eU",
  'authDomain': "khamal-4e080.firebaseapp.com",
  'databaseURL': "https://khamal-4e080-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "khamal-4e080",
  'storageBucket': "khamal-4e080.appspot.com",
  'messagingSenderId': "1039871863429",
  'appId': "1:1039871863429:web:5b6700e56f79c7b52257ec",
  'measurementId': "G-S7WYG1TWRG",
  "databaseURL":"https://khamal-4e080-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase=pyrebase.initialize_app(Config)
auth = firebase.auth()
db=firebase.database()



UPLOAD_FOLDER = 'static/images/thumbs'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
@app.route('/get_pet')
def get_pet():
    pet = db.child("Pets").child(login_session["user"]
    ["localId"]).get().val()
    return render_template("my_pet.html", pet = pet)



@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        photo = request.files['pet_pic']
        upload_file(photo)
        pet = {"name": name, "pic": photo.filename}
        db.child("Pets").push(pet)
        return redirect('/')
    else:
        return render_template('add_post.html')


#####
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




def upload_file(file):
    if request.method == 'POST':
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(UPLOAD_FOLDER + "/" + filename)

@app.route('/')  # '/' for the default page
def home():
    pet=db.child("Pets").child().get().val()
    return render_template('index.html',pet=pet)


@app.route('/add_post')  # '/' for the default page
def add_post():
    return render_template('add_post.html')


if __name__ == "__main__":  # Makes sure this is the main process
    app.run(debug=True)
