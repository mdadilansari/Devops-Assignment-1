from flask import Flask, request, render_template, redirect, url_for, jsonify, abort

app = Flask(__name__)
WORKOUTS = []  # simple in-memory list

@app.get("/")
def index():
    return render_template("index.html", workouts=WORKOUTS)

@app.post("/add")
def add_workout():
    payload = request.get_json(silent=True) or {}
    workout = request.form.get("workout") or payload.get("workout")
    duration = request.form.get("duration") or payload.get("duration")

    if not workout or duration is None:
        abort(400, description="Missing workout or duration.")

    try:
        duration = int(duration)
    except (TypeError, ValueError):
        abort(400, description="Duration must be a number.")

    WORKOUTS.append({"workout": workout, "duration": duration})

    if request.is_json:
        return jsonify({"status": "ok", "count": len(WORKOUTS)}), 201
    return redirect(url_for("index"))

@app.get("/workouts")
def list_workouts():
    return jsonify(WORKOUTS)

@app.post("/delete/<int:index>")
def delete_workout(index):
    if 0 <= index < len(WORKOUTS):
        removed = WORKOUTS.pop(index)
        if request.is_json:
            return jsonify({"status": "deleted", "workout": removed}), 200
        return redirect(url_for("index"))
    else:
        abort(404, description="Workout not found")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)