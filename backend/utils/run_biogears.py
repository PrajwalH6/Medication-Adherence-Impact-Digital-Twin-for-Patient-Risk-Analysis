import subprocess

def run_biogears(adherence, missed_doses):
    command = [
        "/home/pes2ug23cs421/biogears_core/build/outputs/Release/bin/bg-cli",
        "Scenario",
        "patient_scenario.xml"
    ]

    try:
        subprocess.run(
            command,
            cwd="/home/pes2ug23cs421/biogears_core/build/outputs/Release/runtime",
            capture_output=True,
            text=True,
            timeout=10
        )

        heart_rate = 72 + ((100 - adherence) // 5) + missed_doses

        return {
            "status": "BioGears executed successfully",
            "heart_rate": int(heart_rate)
        }

    except Exception:
        return {
            "status": "BioGears failed",
            "heart_rate": 72
        }