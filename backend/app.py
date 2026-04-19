from utils.run_biogears import run_biogears
import matplotlib
matplotlib.use('Agg')

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import pandas as pd
from models.patient_model import calculate_patient

app = Flask(__name__)
CORS(app)

# ----------------------------
# Home
# ----------------------------
@app.route("/")
def home():
    return "DT Project Backend Running"

# ----------------------------
# Simulation
# ----------------------------
@app.route("/simulate")
def simulate():
    adherence = int(request.args.get("adherence", 100))
    missed_doses = int(request.args.get("missed_doses", 0))
    age = int(request.args.get("age", 40))

    result = calculate_patient(adherence, missed_doses, age)

    patient_data = {
        "patient_id": 1,
        "age": age,
        "adherence_percent": adherence,
        "missed_doses": missed_doses,
        "risk_level": result["risk_level"],
        "heart_rate": result["heart_rate"],
        "blood_pressure": result["blood_pressure"]
    }
    biogears_output = run_biogears()
    print("BioGears Engine Log:")
    print(biogears_output)
    return jsonify(patient_data)

# ----------------------------
# Graph
# ----------------------------
@app.route("/graph")
def graph():
    adherence = int(request.args.get("adherence", 100))
    missed_doses = int(request.args.get("missed_doses", 0))
    age = int(request.args.get("age", 40))

    result = calculate_patient(adherence, missed_doses, age)

    values = []

    for i in range(5):
        values.append(result["heart_rate"] + (i * missed_doses))

    plt.figure(figsize=(6, 4))
    plt.plot(values, marker='o')
    plt.grid(True)
    plt.title("Heart Rate Trend")
    plt.xlabel("Time")
    plt.ylabel("Heart Rate")

    filepath = "/mnt/c/Users/pajju/OneDrive/Desktop/dt_project/biogears/outputs/heart_rate.png"
    plt.savefig(filepath)
    plt.close()

    return send_file(filepath, mimetype='image/png')

# ----------------------------
# CSV Save
# ----------------------------
@app.route("/save")
def save():
    adherence = int(request.args.get("adherence", 100))
    missed_doses = int(request.args.get("missed_doses", 0))
    age = int(request.args.get("age", 40))

    result = calculate_patient(adherence, missed_doses, age)

    data = {
        "Age": [age],
        "Adherence": [adherence],
        "Missed Doses": [missed_doses],
        "Risk": [result["risk_level"]],
        "Heart Rate": [result["heart_rate"]],
        "Blood Pressure": [result["blood_pressure"]]
    }

    df = pd.DataFrame(data)

    filepath = "/mnt/c/Users/pajju/OneDrive/Desktop/dt_project/biogears/outputs/patient_output.csv"
    df.to_csv(filepath, index=False)

    return jsonify({
        "message": "CSV saved successfully",
        "file": filepath
    })

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
