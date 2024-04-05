from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from googletrans import Translator
import polib

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_po_file():
    file = request.files['file']
    language = file.filename[0:2]
    if file and file.filename.endswith('.po'):
        # Read file content
        po_content = file.read().decode('utf-8')

        # Translate content
        translated_content = translate_content(po_content, language)

        # Return translated content
        return jsonify({'translated_content': translated_content})
    else:
        return jsonify({'error': 'Invalid file format'})

def translate_content(po_content, language):
    translator = Translator()
    pofile = polib.pofile(po_content)

    for entry in pofile:
        if not entry.msgstr:
            entry.msgstr = translator.translate(entry.msgid, dest=language).text

    return str(pofile)

if __name__ == '__main__':
    app.run(debug=True)
