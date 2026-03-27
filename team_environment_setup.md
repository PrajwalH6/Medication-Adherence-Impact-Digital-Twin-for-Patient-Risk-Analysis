# Medication Adherence Impact Digital Twin for Patient Risk Analysis
## Team Environment Setup Guide

This file ensures every team member uses the same Ubuntu environment.

---

## 1. Install Required Packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git cmake build-essential libxerces-c-dev libssl-dev zlib1g-dev
```

---

## 2. Clone BioGears

```bash
cd ~
git clone https://github.com/BioGearsEngine/core.git
cd core
```

---

## 3. Build BioGears

```bash
mkdir build
cd build
cmake ..
make -j1
```

---

## 4. Clone Project Repository

```bash
cd ~
git clone https://github.com/PrajwalH6/Medication-Adherence-Impact-Digital-Twin-for-Patient-Risk-Analysis.git
```

---

## 5. Copy Project Scenario Files Into BioGears Runtime

```bash
cp ~/Medication-Adherence-Impact-Digital-Twin-for-Patient-Risk-Analysis/scenarios/*.xml ~/core/build/runtime/Scenarios/Drug/
```

---

## 6. Run Normal Scenario

```bash
cd ~/core/build/runtime
../outputs/Release/bin/bg-cli Scenario Scenarios/Drug/PrednisoneScenario.xml
```

---

## 7. Run Delayed Dose Scenario

```bash
../outputs/Release/bin/bg-cli Scenario Scenarios/Drug/MissedDoseScenario.xml
```

---

## 8. Output Files

Generated outputs appear in:

```bash
~/core/build/runtime/Scenarios/Drug/
```

Important files:
- PrednisoneScenarioResults.csv
- MissedDoseScenarioResults.csv

---

## 9. Push New Changes to GitHub

```bash
cd ~/Medication-Adherence-Impact-Digital-Twin-for-Patient-Risk-Analysis
git add .
git commit -m "updated project files"
git push origin main
```

---

## 10. Important Rule

Do NOT upload:
- core/
- build/
- generated/

Upload only:
- scenarios/
- results/
- README.md
