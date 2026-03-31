import pandas as pd
import matplotlib.pyplot as plt

normal = pd.read_csv("PrednisoneScenarioResults.csv")
missed = pd.read_csv("MissedDoseScenarioResults.csv")

plt.plot(
    normal["Time(s)"].to_numpy(),
    normal["SystolicArterialPressure(mmHg)"].to_numpy(),
    label="Normal Dose"
)

plt.plot(
    missed["Time(s)"].to_numpy(),
    missed["SystolicArterialPressure(mmHg)"].to_numpy(),
    label="Missed Dose"
)

plt.xlabel("Time (s)")
plt.ylabel("Systolic Pressure (mmHg)")
plt.title("Medication Adherence Impact on Blood Pressure")
plt.legend()

plt.savefig("pressure_graph.png")
plt.show()
