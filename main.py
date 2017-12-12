import os, io
import image_prescale, resize
import googlecloudaccess
import logging
from google.cloud import storage

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from werkzeug.utils import secure_filename
from shutil import copyfile
from google.appengine.api import app_identity

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

app = Flask(__name__)
app.secret_key = "@ritsukabbsecret_key"
Mobility(app)

# Image Upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@mobile_template('{mobile/}index.html')
def upload(template):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'photo' not in request.files:
            flash( 'Upload fail! Maybe try a different image file (JPG format only)' )
            return redirect(request.url)
        file = request.files['photo']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No file submitted! Try uploading an image file (JPG format only)')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            imageFile = file
            # Create a Cloud Storage client.
            gcs = storage.Client()
            # Get the bucket that the file will be uploaded to.
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
            # Create a new blob and upload the file's content.
            blob = bucket.blob(filename)
            blob.upload_from_file(
                file,
                content_type='image/jpeg'
            )
            blobURL = blob.media_link
            gcs_file = bucket.blob(filename)
            contents = gcs_file.download_as_string()
            jsFile = image_prescale.createJSON(io.BytesIO(contents))
            result = googlecloudaccess.getPrediction(jsFile)
            if result and type(result)!=str:
                result = int(result["predictions"][0]["aestheticScore"][0])
                flash(result)
                flash(blobURL)
                return redirect(url_for('result'))
            else: 
                flash("Cannot get prediction, try again later. \n Error message: " + str(result))
                return redirect(request.url)
        else:
    	    flash( 'Upload fail! Maybe try a different image file (JPG format only)' )
    	    return redirect(request.url)
    elif request.method == 'GET':
        return render_template(template)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

# result page 
@app.route("/result", methods=['GET'])
@mobile_template('{mobile/}result.html')
def result(template):
    return render_template(template)

# about page
@app.route("/about", methods=['GET'])
@mobile_template('{mobile/}about.html')
def about(template):
  return render_template(template)

# for dev test use
if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)
