from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
    flash
)

import os
import joblib

from predict import predict_dataset

app = Flask(__name__)
app.secret_key = "network_intrusion_secret"

# ===========================
# Configuration
# ===========================

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ===========================
# Load Model & Encoders
# ===========================

MODEL = joblib.load("models/random_forest_model.pkl")
SCALER = joblib.load("models/scaler.pkl")

PROTOCOL_ENCODER = joblib.load("models/protocol_encoder.pkl")
SERVICE_ENCODER = joblib.load("models/service_encoder.pkl")
FLAG_ENCODER = joblib.load("models/flag_encoder.pkl")

print("=" * 60)
print("Network Intrusion Detection System")
print("=" * 60)
print("Model Loaded Successfully")
print("Scaler Loaded Successfully")
print("Encoders Loaded Successfully")
print("=" * 60)

# ===========================
# Home Page
# ===========================

@app.route("/")
def home():
    return render_template("index.html")


# ===========================
# Upload Page
# ===========================

@app.route("/upload")
def upload():
    return render_template("upload.html")


# ===========================
# Prediction
# ===========================

@app.route("/predict", methods=["POST"])
def predict():

    if "dataset" not in request.files:
        flash("Please select a dataset.")
        return redirect(url_for("upload"))

    file = request.files["dataset"]

    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("upload"))

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    print("=" * 60)
    print("Dataset Uploaded")
    print(filepath)
    print("=" * 60)

    result = predict_dataset(
        filepath,
        MODEL,
        SCALER,
        PROTOCOL_ENCODER,
        SERVICE_ENCODER,
        FLAG_ENCODER
    )

    return render_template(
        "result.html",
        total_records=result["total"],
        normal=result["normal"],
        attack=result["attack"],
        output_file=result["output_file"],
        preview=result["preview"]
    )


# ===========================
# Download Predictions
# ===========================

@app.route("/download")
def download():

    output_path = os.path.join(
        app.config["OUTPUT_FOLDER"],
        "predictions.csv"
    )

    if os.path.exists(output_path):
        return send_file(
            output_path,
            as_attachment=True
        )

    flash("Prediction file not found.")
    return redirect(url_for("home"))


# ===========================
# About
# ===========================

@app.route("/about")
def about():
    return render_template("about.html")


# ===========================
# Error Pages
# ===========================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


# ===========================
# Run Flask
# ===========================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )