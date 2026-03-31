import pandas as pd
import matplotlib.pyplot as plt

normal = pd.read_csv("PrednisoneScenarioResults.csv")
missed = pd.read_csv("MissedDoseScenarioResults.csv")

x1 = normal["Time(s)"].to_numpy()
y1 = normal["Prednisone-PlasmaConcentration(ug/L)"].to_numpy()

x2 = missed["Time(s)"].to_numpy()
y2 = missed["Prednisone-PlasmaConcentration(ug/L)"].to_numpy()

plt.plot(x1, y1, label="Normal Dose")
plt.plot(x2, y2, label="Missed Dose")

plt.xlabel("Time (s)")
plt.ylabel("Prednisone Plasma Concentration (ug/L)")
plt.title("Medication Adherence Impact on Plasma Concentration")
plt.legend()

plt.savefig("comparison_graph.png")
plt.show()
