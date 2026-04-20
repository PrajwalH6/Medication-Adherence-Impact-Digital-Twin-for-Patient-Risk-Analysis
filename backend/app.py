from utils.run_biogears import run_biogears
import matplotlib
matplotlib.use('Agg')

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import pandas as pd
import random
from models.patient_model import calculate_patient

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "DT Project Backend Running"

@app.route("/simulate")
def simulate():
    profile = request.args.get("profile", "manual")

    if profile == "nominal":
        adherence = random.randint(90, 100)
        missed_doses = random.randint(0, 2)
        age = random.randint(30, 45)

    elif profile == "high":
        adherence = random.randint(40, 70)
        missed_doses = random.randint(4, 8)
        age = random.randint(60, 75)

    else:
        adherence = int(request.args.get("adherence", 100))
        missed_doses = int(request.args.get("missed_doses", 0))
        age = int(request.args.get("age", 40))

    result = calculate_patient(adherence, missed_doses, age)

    biogears_output = run_biogears(adherence, missed_doses)

    patient_data = {
        "patient_id": 1,
        "age": age,
        "adherence_percent": adherence,
        "missed_doses": missed_doses,
        "risk_level": result["risk_level"],
        "heart_rate": biogears_output["heart_rate"],
        "blood_pressure": result["blood_pressure"],
        "instability_score": 100 - adherence + missed_doses * 2,
        "recovery_time": "4 days" if missed_doses > 3 else "1 day",
        "probability_alert": "78%" if adherence < 60 else "15%"
    }

    print(biogears_output)

    return jsonify(patient_data)

@app.route("/graph")
def graph():
    adherence = int(request.args.get("adherence", 100))
    missed_doses = int(request.args.get("missed_doses", 0))
    age = int(request.args.get("age", 40))

    result = calculate_patient(adherence, missed_doses, age)

    values = []
    current_hr = result["heart_rate"]

    for day in range(7):
        if day == 2:
            current_hr += missed_doses * 2
        elif day == 4:
            current_hr -= 3
        values.append(current_hr)

    plt.figure(figsize=(7, 4))
    plt.plot(values, marker='o')
    plt.grid(True)
    plt.title("7-Day Heart Rate Simulation")
    plt.xlabel("Day")
    plt.ylabel("Heart Rate")

    filepath = "/mnt/c/Users/pajju/OneDrive/Desktop/dt_project/biogears/outputs/heart_rate.png"
    plt.savefig(filepath)
    plt.close()

    return send_file(filepath, mimetype='image/png')

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

@app.route("/montecarlo")
def montecarlo():
    high_count = 0

    for _ in range(20):
        adherence = random.randint(40, 70)
        missed_doses = random.randint(4, 8)

        result = calculate_patient(adherence, missed_doses, 65)

        if result["risk_level"] == "High":
            high_count += 1

    return jsonify({
        "high_risk_runs": high_count,
        "total_runs": 20
    })

if __name__ == "__main__":
    app.run(debug=True)