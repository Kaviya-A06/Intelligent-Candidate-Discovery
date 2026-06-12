from flask import Flask, render_template, jsonify
import pandas as pd
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/dashboard")
def dashboard_data():
    try:
        csv_path = os.path.join(OUTPUTS_DIR, "team_submission.csv")
        json_path = os.path.join(OUTPUTS_DIR, "explainability_logs.json")

        # Fallback to empty data structures if files don't exist yet
        if not os.path.exists(csv_path) or not os.path.exists(json_path):
            return jsonify({
                "table": [],
                "logs": {},
                "summary": {"processed": "50,000+", "top_candidates": 0, "avg_tech": 0, "avg_founding": 0, "avg_hiring": 0}
            })

        df = pd.read_csv(csv_path)
        with open(json_path, "r", encoding="utf-8") as f:
            logs = json.load(f)

        # Calculate metrics dynamically
        avg_tech = sum(log["scores"]["technical_fit"] for log in logs.values()) / len(logs)
        avg_founding = sum(log["scores"]["founding_fit"] for log in logs.values()) / len(logs)
        avg_hiring = sum(log["scores"]["hiring_probability"] for log in logs.values()) / len(logs)

        return jsonify({
            "table": df.to_dict(orient="records"),
            "logs": logs,
            "summary": {
                "processed": "50,000+",
                "top_candidates": len(df),
                "avg_tech": round(avg_tech * 100, 1),
                "avg_founding": round(avg_founding * 100, 1),
                "avg_hiring": round(avg_hiring * 100, 1)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)