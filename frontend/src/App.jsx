import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [adherence, setAdherence] = useState(95);
  const [missedDoses, setMissedDoses] = useState(0);
  const [age, setAge] = useState(38);
  const [result, setResult] = useState(null);
  const [graphUrl, setGraphUrl] = useState("");
  const [comparison, setComparison] = useState(null);
  const [monteCarlo, setMonteCarlo] = useState(null);

  const simulatePatient = async (profile = "manual") => {
    const response = await axios.get(
      `http://127.0.0.1:5000/simulate?adherence=${adherence}&missed_doses=${missedDoses}&age=${age}&profile=${profile}`
    );

    setResult(response.data);
    setAdherence(response.data.adherence_percent);
    setMissedDoses(response.data.missed_doses);
    setAge(response.data.age);

    setGraphUrl(
      `http://127.0.0.1:5000/graph?adherence=${response.data.adherence_percent}&missed_doses=${response.data.missed_doses}&age=${response.data.age}&t=${Date.now()}`
    );

    await axios.get(
      `http://127.0.0.1:5000/save?adherence=${response.data.adherence_percent}&missed_doses=${response.data.missed_doses}&age=${response.data.age}`
    );
  };

  const runComparison = async () => {
    const nominal = await axios.get("http://127.0.0.1:5000/simulate?profile=nominal");
    const high = await axios.get("http://127.0.0.1:5000/simulate?profile=high");
    setComparison({ nominal: nominal.data, high: high.data });
  };

  const runMonteCarlo = async () => {
    const response = await axios.get("http://127.0.0.1:5000/montecarlo");
    setMonteCarlo(response.data);
  };

  const riskClass = (risk) => {
    if (risk === "Low") return "risk-low";
    if (risk === "Moderate") return "risk-mod";
    if (risk === "High") return "risk-high";
    return "risk-crit";
  };

  const twinDotColor = (risk) => {
    if (risk === "Low") return "#0f9e6d";
    if (risk === "Moderate") return "#c47a10";
    if (risk === "High") return "#d63a3a";
    return "#8b1a1a";
  };

  const mcPercent = monteCarlo
    ? Math.round((monteCarlo.high_risk_runs / monteCarlo.total_runs) * 100)
    : 0;

  return (
    <div className="app-container">
      <div className="dashboard-card">

        {/* ── Header ── */}
        <div className="header">
          <div className="header-left">
            <h1>Medication Adherence Digital Twin</h1>
            <p className="subtitle">Advanced physiological monitoring and risk simulation</p>
          </div>
          <div className="header-badge">
            <span />
            Engine Active
          </div>
        </div>

        {/* ── Inputs ── */}
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

        {/* ── Buttons ── */}
        <div className="button-row">
          <button className="primary-button btn-primary" onClick={() => simulatePatient()}>
            Manual Simulation
          </button>
          <button className="primary-button" onClick={() => simulatePatient("nominal")}>
            Nominal Profile
          </button>
          <button className="primary-button" onClick={() => simulatePatient("high")}>
            High Risk Profile
          </button>
          <button className="primary-button" onClick={runComparison}>
            Compare Profiles
          </button>
          <button className="primary-button" onClick={runMonteCarlo}>
            Monte Carlo Analysis
          </button>
        </div>

        {/* ── Results ── */}
        {result && (
          <div className="main-grid">

            {/* Left Panel */}
            <div className="left-panel">

              {/* KPI Row */}
              <div className="kpi-grid">
                <div className="kpi-card risk-card">
                  <h3>Risk Level</h3>
                  <p className={riskClass(result.risk_level)}>{result.risk_level}</p>
                </div>
                <div className="kpi-card">
                  <h3>Heart Rate</h3>
                  <p>{result.heart_rate}</p>
                </div>
                <div className="kpi-card">
                  <h3>Blood Pressure</h3>
                  <p>{result.blood_pressure}</p>
                </div>
                <div className="kpi-card">
                  <h3>Instability Score</h3>
                  <p>{result.instability_score}</p>
                </div>
                <div className="kpi-card">
                  <h3>Recovery Time</h3>
                  <p>{result.recovery_time}</p>
                </div>
                <div className="kpi-card">
                  <h3>Alert Probability</h3>
                  <p>{result.probability_alert}</p>
                </div>
              </div>

              {/* Graph */}
              <div className="graph-card">
                <h2>7-Day Heart Rate Simulation</h2>
                <img src={graphUrl} alt="Heart Rate Graph" />
              </div>

              {/* Comparison Table */}
              {comparison && (
                <div className="info-card comparison-card">
                  <h2>Profile Comparison</h2>
                  <table>
                    <thead>
                      <tr>
                        <th>Metric</th>
                        <th>Nominal</th>
                        <th>High Risk</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Heart Rate</td>
                        <td>{comparison.nominal.heart_rate}</td>
                        <td>{comparison.high.heart_rate}</td>
                      </tr>
                      <tr>
                        <td>Risk Level</td>
                        <td>{comparison.nominal.risk_level}</td>
                        <td>{comparison.high.risk_level}</td>
                      </tr>
                      <tr>
                        <td>Instability</td>
                        <td>{comparison.nominal.instability_score}</td>
                        <td>{comparison.high.instability_score}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Right Panel */}
            <div className="right-panel">

              {/* Patient Summary */}
              <div className="info-card">
                <h2>Patient Summary</h2>
                <div className="info-row">
                  <span>Age</span>
                  <span className="val">{age} yrs</span>
                </div>
                <div className="info-row">
                  <span>Adherence</span>
                  <span className="val">{adherence}%</span>
                </div>
                <div className="info-row">
                  <span>Missed Doses</span>
                  <span className="val">{missedDoses}</span>
                </div>
              </div>

              {/* BioGears Status */}
              <div className="info-card">
                <h2>BioGears Status</h2>
                <div className="status-line">
                  <span className="status-dot" />
                  Engine executed successfully
                </div>
                <div className="status-line">
                  <span className="status-dot" />
                  Scenario validated
                </div>
              </div>

              {/* Digital Twin State */}
              <div className="info-card">
                <h2>Digital Twin State</h2>
                <div className="twin-indicator-wrap">
                  <div
                    className="twin-indicator"
                    style={{ background: twinDotColor(result.risk_level) }}
                  />
                  <div>
                    <div className="twin-label">{result.risk_level} Risk</div>
                    <div className="twin-sub">Simulation running</div>
                  </div>
                </div>
              </div>

              {/* Monte Carlo */}
              {monteCarlo && (
                <div className="info-card">
                  <h2>Monte Carlo Risk Distribution</h2>
                  <div className="info-row">
                    <span>Total runs</span>
                    <span className="val">{monteCarlo.total_runs}</span>
                  </div>
                  <div className="info-row">
                    <span>High risk runs</span>
                    <span className="val">{monteCarlo.high_risk_runs}</span>
                  </div>
                  <div className="info-row">
                    <span>High risk rate</span>
                    <span className="val">{mcPercent}%</span>
                  </div>
                  <div className="mc-bar">
                    <div className="mc-fill" style={{ width: `${mcPercent}%` }} />
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;