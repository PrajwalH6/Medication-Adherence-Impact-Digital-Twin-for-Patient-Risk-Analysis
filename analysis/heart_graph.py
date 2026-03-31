import pandas as pd
import matplotlib.pyplot as plt

normal = pd.read_csv("PrednisoneScenarioResults.csv")
missed = pd.read_csv("MissedDoseScenarioResults.csv")

plt.plot(
    normal["Time(s)"].to_numpy(),
    normal["HeartRate(1/min)"].to_numpy(),
    label="Normal Dose"
)

plt.plot(
    missed["Time(s)"].to_numpy(),
    missed["HeartRate(1/min)"].to_numpy(),
    label="Missed Dose"
)

plt.xlabel("Time (s)")
plt.ylabel("Heart Rate (1/min)")
plt.title("Medication Adherence Impact on Heart Rate")
plt.legend()

plt.savefig("heart_rate_graph.png")
plt.show()
