from datetime import datetime
from extensions import db

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="document ID")
    filename = db.Column(db.String(255), nullable=False, comment="filename")
    file_path = db.Column(db.String(500), nullable=False, comment="file path")
    file_type = db.Column(db.String(50), comment="file type")
    file_size = db.Column(db.Integer, comment="file size")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, comment="uploader ID")
    user = db.relationship("User", backref="documents", lazy=True)
    status = db.Column(db.SmallInteger, default=1, comment="status: 1 normal, 0 deleted")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="created time")

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "user_id": self.user_id,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }