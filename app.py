from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
import openai
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DESIGN_FOLDER'] = 'designed'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DESIGN_FOLDER'], exist_ok=True)

# Placeholder AI design function
# In a real implementation this would call an AI service or model
# to generate designs based on the user's prompt

def apply_ai_design(image_path, prompt):
    """Apply an AI generated design to the uploaded image."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                n=1,
                size="1024x1024",
            )
            image_url = response.data[0].url
            r = requests.get(image_url)
            output_path = os.path.join(app.config['DESIGN_FOLDER'], os.path.basename(image_path))
            with open(output_path, 'wb') as f:
                f.write(r.content)
            return output_path
        except Exception as e:
            print("OpenAI API error:", e)

    # Fallback: simple overlay if API key is missing or request fails
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        text = f"Design: {prompt}"
        draw.text((10, 10), text, fill=(255, 0, 0), font=font)
        output_path = os.path.join(app.config['DESIGN_FOLDER'], os.path.basename(image_path))
        img.save(output_path)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def upload_photo():
    if request.method == 'POST':
        files = request.files.getlist('photos')
        if not files:
            return 'No file part', 400
        prompt = request.form.get('prompt', '')
        designed_files = []
        for file in files:
            if file.filename == '':
                continue
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            designed_path = apply_ai_design(upload_path, prompt)
            designed_files.append(os.path.basename(designed_path))
        if not designed_files:
            return 'No selected file', 400
        return render_template('photo.html', filenames=designed_files)
        if 'photo' not in request.files:
            return 'No file part', 400
        file = request.files['photo']
        prompt = request.form.get('prompt', '')
        if file.filename == '':
            return 'No selected file', 400
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        designed_path = apply_ai_design(upload_path, prompt)
        return redirect(url_for('view_photo', filename=os.path.basename(designed_path)))
    return render_template('upload.html')

@app.route('/photo/<filename>')
def view_photo(filename):
    return render_template('photo.html', filenames=[filename])
    return render_template('photo.html', filename=filename)

@app.route('/designed/<filename>')
def designed_file(filename):
    return send_from_directory(app.config['DESIGN_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
