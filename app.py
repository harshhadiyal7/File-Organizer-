import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

# --- Configuration ---
# Define the path for uploaded files.
# The 'os.getcwd()' gets the current working directory of the script.
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploaded_files')

# Define the allowed file extensions.
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}

# --- Create the Flask App ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# A secret key is needed for 'flash' messages to work.
# In a real app, use a more complex, random key.
app.config['SECRET_KEY'] = 'supersecretkey'

# --- Helper Functions ---

def allowed_file(filename):
    """Checks if a filename has one of the allowed extensions."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_folders():
    """Create the necessary folders if they don't already exist."""
    # Create the main upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # Create subfolders for each file type
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'pdf'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'doc'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'image'), exist_ok=True)

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # This block handles the POST request when the form is submitted.
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part in the request. Please select a file.')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No file selected. Please select a file to upload.')
            return redirect(request.url)

        # If the file is valid, process it.
        if file and allowed_file(file.filename):
            # secure_filename cleans up the filename to make it safe.
            filename = secure_filename(file.filename)
            
            # Get the file extension
            extension = filename.rsplit('.', 1)[1].lower()
            
            # Determine the correct subfolder based on the extension
            target_folder = ''
            if extension == 'pdf':
                target_folder = 'pdf'
            elif extension == 'docx':
                target_folder = 'doc'
            elif extension in ['jpg', 'jpeg', 'png']:
                target_folder = 'image'

            # Construct the final save path
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], target_folder, filename)
            
            # Save the file
            file.save(save_path)
            
            # 'flash' is a way to show a one-time message to the user.
            flash(f'Success! File "{filename}" was uploaded and saved in the {target_folder} folder.')
            
            # Redirect back to the upload form.
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid file type. Allowed types are: pdf, docx, jpg, png.')
            return redirect(request.url)

    # This is for the GET request, which just displays the HTML page.
    return render_template('index.html')

# --- Main Execution ---
if __name__ == '__main__':
    # Create the folders before starting the app
    create_folders()
    # Run the Flask app
    # debug=True means the server will auto-reload when you save changes.
    app.run(debug=True)
