
from flask import Flask, request, redirect, render_template, url_for
from generatePathMap import mark_static_google_map, parseFlightFile
from werkzeug import secure_filename
import os

UPLOAD_FOLDER = './tmp/'
RES_FOLDER = './static/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['csv', 'txt'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/track', methods=['GET', 'POST'])
def acquireCoordinates():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            prefix = os.path.splitext(filename)[0]
            target = os.path.join(UPLOAD_FOLDER, filename)
            path = parseFlightFile(target)
            if not os.path.exists(RES_FOLDER):
                os.mkdir(RES_FOLDER)
            mark_static_google_map(mapname=RES_FOLDER+prefix, f=path)
            return redirect(url_for('newPathMap', img=prefix+".png"))
    else:
        return render_template('upload.html')


@app.route('/track/show/<img>')
def newPathMap(img):
    return render_template('map.html', img=img)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
