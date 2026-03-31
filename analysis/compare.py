import pandas as pd

normal = pd.read_csv("PrednisoneScenarioResults.csv")
missed = pd.read_csv("MissedDoseScenarioResults.csv")

cols = [
    "Time(s)",
    "HeartRate(1/min)",
    "SystolicArterialPressure(mmHg)",
    "Prednisone-PlasmaConcentration(ug/L)"
]

print("Normal Scenario")
print(normal[cols].tail())

print("\nMissed Dose Scenario")
print(missed[cols].tail())

normal_plasma = normal["Prednisone-PlasmaConcentration(ug/L)"].iloc[-1]
missed_plasma = missed["Prednisone-PlasmaConcentration(ug/L)"].iloc[-1]

print("\nRisk Analysis")

if missed_plasma < normal_plasma:
    print("Risk Increased: delayed medication reduced plasma concentration")
else:
    print("No major risk difference")
