import pandas as pd

normal = pd.read_csv("PrednisoneScenarioResults.csv")
missed = pd.read_csv("MissedDoseScenarioResults.csv")

normal_plasma = normal["Prednisone-PlasmaConcentration(ug/L)"].iloc[-1]
missed_plasma = missed["Prednisone-PlasmaConcentration(ug/L)"].iloc[-1]

difference = normal_plasma - missed_plasma

print("Normal Plasma:", normal_plasma)
print("Missed Plasma:", missed_plasma)
print("Difference:", difference)

if difference > 0.2:
    print("Risk Score: HIGH")
elif difference > 0.05:
    print("Risk Score: MODERATE")
else:
    print("Risk Score: LOW")
