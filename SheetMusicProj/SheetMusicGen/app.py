from flask import Flask, request, send_file, render_template
from basic_pitch.inference import predict_and_save
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Run transcription
    predict_and_save(
        [filepath],
        output_directory=RESULT_FOLDER,
        save_midi=True,
        save_model_outputs=False,
        save_notes=False
    )

    midi_path = os.path.join(RESULT_FOLDER, file.filename.replace(".wav", ".mid"))
    return send_file(midi_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
