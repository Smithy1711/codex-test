# AI Photo Book Site

This project is a minimal example of a web application that lets users upload photos and generate a simple digital photo book with AI-driven designs.

The AI design step is now powered by the OpenAI API. When you submit your photos and prompt, the app uses the `gpt-image-1` model to generate a styled page for each photo. If `OPENAI_API_KEY` is not provided or the request fails, the app falls back to a simple placeholder design.


This project is a minimal example of a web application that lets users upload photos and generate a simple digital photo book with AI-driven designs.

The AI design step is represented here by a placeholder function that overlays the user's prompt onto the uploaded image. In a production system you would replace this with calls to your preferred AI model or service.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open your browser to `http://localhost:5000` to upload photos and create designs. You can select multiple files at once and the app will generate a designed image for each one.

2. Start the server:
   ```bash
   python app.py
   ```
3. Open your browser to `http://localhost:5000` to upload photos and create designs. You can select multiple files at once and the app will generate a designed image for each one.

3. Open your browser to `http://localhost:5000` to upload photos and create designs.

Uploaded images are stored in the `uploads/` directory, and designed images are saved in `designed/`.
Static assets such as `style.css` live in the `static/` folder.
