import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [adherence, setAdherence] = useState(95);
  const [missedDoses, setMissedDoses] = useState(0);
  const [age, setAge] = useState(38);
  const [result, setResult] = useState(null);
  const [graphUrl, setGraphUrl] = useState("");

  const simulatePatient = async () => {
    const response = await axios.get(
      `http://127.0.0.1:5000/simulate?adherence=${adherence}&missed_doses=${missedDoses}&age=${age}`
    );

    setResult(response.data);

    setGraphUrl(
      `http://127.0.0.1:5000/graph?adherence=${adherence}&missed_doses=${missedDoses}&age=${age}&t=${new Date().getTime()}`
    );

    await axios.get(
      `http://127.0.0.1:5000/save?adherence=${adherence}&missed_doses=${missedDoses}&age=${age}`
    );
  };

  const riskColor = (risk) => {
    if (risk === "Low") return "#16a34a";
    if (risk === "Moderate") return "#f59e0b";
    if (risk === "High") return "#dc2626";
    return "#7f1d1d";
  };

  return (
    <div className="app-container">
      <div className="dashboard-card">

        <h1>Medication Adherence Digital Twin</h1>
        <p className="subtitle">Clinical Monitoring Dashboard</p>

        <div className="input-grid">
          <div className="input-box">
            <label>Adherence %</label>
            <input
              type="number"
              value={adherence}
              onChange={(e) => setAdherence(e.target.value)}
            />
          </div>

          <div className="input-box">
            <label>Missed Doses</label>
            <input
              type="number"
              value={missedDoses}
              onChange={(e) => setMissedDoses(e.target.value)}
            />
          </div>

          <div className="input-box">
            <label>Age</label>
            <input
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
            />
          </div>
        </div>

        <button onClick={simulatePatient}>Run Full Simulation</button>

        {result && (
          <div className="main-grid">

            <div className="left-panel">

              <div className="kpi-grid">
                <div className="kpi-card">
                  <h3>Risk Level</h3>
                  <p style={{ color: riskColor(result.risk_level) }}>
                    {result.risk_level}
                  </p>
                </div>

                <div className="kpi-card">
                  <h3>Heart Rate</h3>
                  <p>{result.heart_rate}</p>
                </div>

                <div className="kpi-card">
                  <h3>Blood Pressure</h3>
                  <p>{result.blood_pressure}</p>
                </div>
              </div>

              <div className="graph-card">
                <h2>Heart Rate Trend</h2>
                <img src={graphUrl} alt="Graph" />
              </div>

            </div>

            <div className="right-panel">

              <div className="info-card">
                <h2>Patient Summary</h2>
                <p>Age: {age}</p>
                <p>Medication Adherence: {adherence}%</p>
                <p>Missed Doses: {missedDoses}</p>
              </div>

              <div className="info-card">
                <h2>Engine Status</h2>
                <p>BioGears Engine Invoked</p>
                <p>Scenario Validation Active</p>
              </div>

              <div className="info-card">
                <h2>Clinical Recommendation</h2>
                <p>
                  Maintain adherence above 90% to reduce cardiovascular risk.
                  Frequent missed doses may increase long-term instability.
                </p>
              </div>

              <div className="info-card">
                <h2>Risk Interpretation</h2>
                <p>
                  Current physiological indicators suggest medication adherence
                  has direct impact on patient stability.
                </p>
              </div>

            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default App;