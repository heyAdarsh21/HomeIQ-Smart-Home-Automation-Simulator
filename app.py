import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

DB_PW = os.environ.get("PGPASSWORD", "Adarsh2001")
DB_USER = os.environ.get("PGUSER", "postgres")
DB_HOST = os.environ.get("PGHOST", "localhost")
DB_NAME = os.environ.get("PGDATABASE", "project_smarthome")
DB_PORT = os.environ.get("PGPORT", "5432")

DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-change-me")

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Boolean, default=False)
    energy_usage = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "status": self.status, "energy_usage": self.energy_usage}

def create_tables():
    """Create DB tables (run once)."""
    with app.app_context():
        db.create_all()
        print("Tables created (users, devices).")

@app.route("/")
def index():

    devices = Device.query.order_by(Device.id).all()
    active_count = sum(1 for d in devices if d.status)
    total_energy_active = sum((d.energy_usage or 0) for d in devices if d.status)
    return render_template("dashboard.html",
                           devices=devices,
                           active_count=active_count,
                           total_energy=total_energy_active)


@app.route("/toggle/<int:device_id>", methods=["POST"])
def toggle(device_id):
    d = Device.query.get_or_404(device_id)
    d.status = not d.status
    db.session.add(d)
    db.session.commit()
    return jsonify({"ok": True, "id": d.id, "status": d.status})


@app.route("/add", methods=["POST"])
def add_device():
    name = request.form.get("name", "").strip()
    energy = request.form.get("energy", type=int) or 0
    if not name:
        flash("Name required")
        return redirect(url_for("index"))
    d = Device(name=name, energy_usage=energy, status=False)
    db.session.add(d)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:device_id>", methods=["POST"])
def delete_device(device_id):
    d = Device.query.get_or_404(device_id)
    db.session.delete(d)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/stats")
def stats():
    devices = Device.query.all()
    active_count = sum(1 for d in devices if d.status)
    total_energy_active = sum((d.energy_usage or 0) for d in devices if d.status)
    return jsonify({"active_count": active_count, "total_energy": total_energy_active})

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("User already exists (username or email).")
            return redirect(url_for("register"))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registered. Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Logged in.")
            return redirect(url_for("index"))
        flash("Invalid credentials.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("login"))

@app.route("/ping")
def ping():
    return "pong"


if __name__ == "__main__":
    app.run(debug=True)
