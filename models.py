# models.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, pw): self.password_hash = generate_password_hash(pw)
    def check_password(self, pw): return check_password_hash(self.password_hash, pw)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=False)   # False=OFF, True=ON
    energy_usage = db.Column(db.Integer)            # watts
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship("Room", backref="devices")

class EnergyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    ts = db.Column(db.DateTime, default=datetime.utcnow)
    energy_wh = db.Column(db.Integer)   # watt-hours
    device = db.relationship("Device")

class AutomationRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    # trigger types: 'threshold' or 'schedule'
    trigger_type = db.Column(db.String(20), nullable=False)
    # threshold: trigger_device_id, operator, trigger_value (eg energy > 1000)
    trigger_device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    trigger_operator = db.Column(db.String(2))
    trigger_value = db.Column(db.Integer)
    # schedule: cron_time as 'HH:MM' (24h)
    cron_time = db.Column(db.String(5))
    # action: device to act on + action ('on'/'off')
    action_device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    action = db.Column(db.String(10))
    enabled = db.Column(db.Boolean, default=True)
    last_run = db.Column(db.DateTime)

    trigger_device = db.relationship("Device", foreign_keys=[trigger_device_id])
    action_device = db.relationship("Device", foreign_keys=[action_device_id])
