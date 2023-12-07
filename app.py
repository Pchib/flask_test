import os
import uuid
import openai
from flask import Flask, jsonify, request, send_from_directory, flash, redirect
UPLOAD_FOLDER = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

api_key = open_file('openaiapikey2.txt')

# Create the UPLOAD_FOLDER directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.root_path + '/static', filename)

@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    file_name = str(uuid.uuid4()) + ".mp3"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(full_file_name)

    # Read the content of the file
    with open(full_file_name, 'rb') as audio_file:
        openai.api_key = api_key
        result = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
        # result = openai.Audio.create_transcription(
        #     model="whisper-1",
        #     audio_file=audio_file,
        # )


    return jsonify({'transcription': result.text}), 200

if __name__ == '__main__':
    app.run(debug=True)




# import os
# import uuid
# import openai
# from flask import Flask, jsonify, request, redirect, flash
# import io

# UPLOAD_FOLDER = 'files'

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def open_file(filepath):
#     with open(filepath, 'r', encoding='utf-8') as infile:
#         return infile.read()

# api_key = open_file('openaiapikey2.txt')

# # Create the UPLOAD_FOLDER directory if it doesn't exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/')
# def root():
#     return app.send_static_file('index.html')

# @app.route('/save-record', methods=['POST'])
# def save_record():
#     # check if the post request has the file part
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)

#     file = request.files['file']
#     # if the user does not select a file, the browser also
#     # submits an empty part without a filename
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)

#     # Read the content of the file
#     audio_content = io.BytesIO(file.read())

#     openai.api_key = api_key

#     result = openai.audio.transcriptions.create(model="whisper-1", file=audio_content)
#     # result = openai.Audio.create_transcription(
#     #     model="whisper-1",
#     #     audio_file=audio_content,
#     # )

#     return jsonify({'transcription': result.text}), 200

# if __name__ == '__main__':
#     app.run(debug=True)


# import os
# import uuid
# import openai
# from flask import Flask, jsonify, request, redirect, flash
# import io

# UPLOAD_FOLDER = 'files'

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def open_file(filepath):
#     with open(filepath, 'r', encoding='utf-8') as infile:
#         return infile.read()

# api_key = open_file('openaiapikey2.txt')

# # Create the UPLOAD_FOLDER directory if it doesn't exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/')
# def root():
#     return app.send_static_file('index.html')

# @app.route('/save-record', methods=['POST'])
# def save_record():
#     # check if the post request has the file part
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)

#     file = request.files['file']
#     # if the user does not select a file, the browser also
#     # submits an empty part without a filename
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)

#     # Check if the file format is supported
#     allowed_formats = {'flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm'}
#     if file.filename.split('.')[-1] not in allowed_formats:
#         return jsonify({'transcription': "bad"}), 400

#     # Read the content of the file
#     audio_content = io.BytesIO(file.read())
#     print(audio_content)
#     openai.api_key = api_key

#     # Specify the file format explicitly
#     result = openai.audio.transcriptions.create(model="whisper-1", file=audio_content)

#     return jsonify({'transcription': result.text}), 200

# if __name__ == '__main__':
#     app.run(debug=True)
