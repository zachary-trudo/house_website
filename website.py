from flask import Flask, request,  redirect, url_for, flash, render_template
import datetime
from TorrentAdapter import TorrentAdapter
import tablib
import os

UPLOAD_FOLDER = '/home/zatrudo/house_website/torrent_files'
UPLOAD_HISTORY = '/home/zatrudo/house_website/upload_history'
ALLOWED_EXTENSIONS = set(['torrent'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "Alphabet"


tadapt = TorrentAdapter()
downloads = tablib.Dataset()

def check_allowed_extension(filename):
  """ Checks a filename to ensure the extension is correct.

  Args:
    filename (str): name of the file

  Returns:
    bool: True if allowed, false otherwise.
  """
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def secure_filename(filename):
  """ Ensures no funny stuff with filenames

  Args:
    filename (str): name of the file

  Returns:
    str: basename of the file.
  """
  return os.path.basename(filename)

def save_torrent_file(filename, torrent_file,  username):
  """ Saves the file in the torrent folder and logs the upload.

  Args:
    filename (str): name of the file
    torrent_file (file): the file to be saved
    username (str): person who uploaded the file

  Returns:
    bool: indicates success
  """
  retVal = True
  try:
    with open(UPLOAD_HISTORY, 'a') as uh:
      uh.write("{filename}, {username}, {timestamp}\n".format(filename=filename, 
                                                            username=username, 
                                                            timestamp=datetime.datetime.now()))
    torrent_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  except:
    retVal = False
  return retVal

def start_torrent_download(filename):
  """ Utilizes the torrent adapter to start a download

  Args:
    filename (str): name of the file for the torrent.

  Returns:
    bool: indicates success
  """
  return tadapt.start_download(filename)
  
def update_download_info():
  """ Reads the UPLOAD_HISTORY file and updates the download dataset. """
  with open(UPLOAD_HISTORY, 'r') as uh:
    downloads.csv = uh.read()
  file_statuses = []
  for ordered_dict in downloads.dict:
    filename = ordered_dict["Torrent Name"]
    file_statuses.append(tadapt.check_download(filename))
  if len(file_statuses) > 0:
    clean_statuses = [a[1] if a[0] else 0.0 for a in file_statuses]
    downloads.append_col(clean_statuses, header='Download percent')

update_download_info()

def upload_validated(request):
  """ Validates that the upload has been correctly formatted. """
  if 'file' not in request.files:
    flash('No file part')
    return False 
  if not request.form.get('username', None):
    flash('No username part')
    return False 
  torrent_file = request.files['file']
  if torrent_file.filename == '':
    flash('No selected file')
    return False 
  if torrent_file and check_allowed_extension(torrent_file.filename):
    return True


def render_successful_upload(request):
  """ Renders the webpage for a successful upload.

  Args:
    request (request): request object with the form upload information

  Returns:
    webpage: Don't know the type... but it works.
  """
  torrent_file = request.files['file']
  filename = secure_filename(torrent_file.filename)
  username = request.form['username']
  save_torrent_file(filename, torrent_file, request.form['username'])
  dl_success = start_torrent_download(filename)
  update_download_info()
  return render_template('successful_upload.html', 
                         username=username, 
                         filename=filename, 
                         download_success=dl_success, 
                         downloads=downloads)


def render_index():
  """ Renders index

  Returns:
    Cool Index webpage
  """
  return render_template("index.html", downloads=downloads)



@app.route('/', methods=['GET', 'POST'])
def upload_file():
  """ Lets a user upload a file and renders the torrent start bar.
  
  If anything in that process goes wrong it renders the basic webpage.

  Returns:
    Cool Webpages
  """
  retVal = None 
  if request.method == 'POST' and upload_validated(request):
      retVal = render_successful_upload(request) 
  else:
    retVal = render_index()
  return retVal 
