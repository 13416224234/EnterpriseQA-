from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="user ID")
    username = db.Column(db.String(50), unique=True, nullable=False, comment="username")
    password = db.Column(db.String(255), nullable=False, comment="MD5 password")
    email = db.Column(db.String(100), comment="email")
    real_name = db.Column(db.String(50), comment="real name")
    role = db.Column(db.Enum("admin", "user"), default="user", comment="role")
    avatar = db.Column(db.String(255), comment="avatar")
    status = db.Column(db.SmallInteger, default=1, comment="status: 1 active, 0 disabled")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="created time")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="updated time")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "real_name": self.real_name,
            "role": self.role,
            "avatar": self.avatar,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }