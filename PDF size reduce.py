# This is to check if the code is changed or not


import os
import subprocess
from flask import Flask, request, send_file, render_template_string, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = '''
<!doctype html>
<title>PDF Compressor</title>
<h2>🗜️ PDF Compressor</h2>
<form method=post enctype=multipart/form-data>
  <label>Select PDF to compress:</label><br>
  <input type=file name=pdf required><br><br>
  <label>New filename (without .pdf):</label><br>
  <input type=text name=newname required><br><br>
  <button type=submit>Compress</button>
</form>
{% if download_url %}
<hr>
<p>✅ Compression complete.</p>
<a href="{{ download_url }}">Download Compressed PDF</a>
{% endif %}
'''

def compress_pdf(input_path, output_path, quality='ebook'):
    subprocess.run([
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS=/{quality}',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={output_path}',
        input_path
    ], check=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    download_url = None

    if request.method == 'POST':
        file = request.files['pdf']
        new_name = request.form['newname'].strip()
        
        if file.filename == '' or not file.filename.endswith('.pdf'):
            return '❌ Please upload a valid PDF file.', 400

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        temp_output = os.path.join(UPLOAD_FOLDER, 'compressed_temp.pdf')
        final_output = os.path.join(UPLOAD_FOLDER, f'{new_name}.pdf')

        file.save(input_path)

        try:
            compress_pdf(input_path, temp_output)
            os.rename(temp_output, final_output)
            download_url = url_for('download_file', filename=f'{new_name}.pdf')
        except Exception as e:
            return f'❌ Compression failed: {e}', 500
        finally:
            os.remove(input_path)

    return render_template_string(HTML_TEMPLATE, download_url=download_url)

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
