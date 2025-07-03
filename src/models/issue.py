from datetime import datetime
from src.models.user import db

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic issue information
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # road, water, power, other
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    status = db.Column(db.String(20), nullable=False, default='reported')  # reported, verified, in_progress, resolved
    
    # Location information
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(500), nullable=True)
    
    # Photo information
    photo_filename = db.Column(db.String(255), nullable=True)
    photo_original_name = db.Column(db.String(255), nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    reporter_name = db.Column(db.String(100), nullable=True)
    reporter_email = db.Column(db.String(120), nullable=True)
    reporter_phone = db.Column(db.String(20), nullable=True)
    
    # Admin notes
    admin_notes = db.Column(db.Text, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Issue {self.id}: {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'severity': self.severity,
            'status': self.status,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'photo_filename': self.photo_filename,
            'photo_original_name': self.photo_original_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'reporter_name': self.reporter_name,
            'reporter_email': self.reporter_email,
            'reporter_phone': self.reporter_phone,
            'admin_notes': self.admin_notes,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }

    def to_csv_dict(self):
        """Return a dictionary suitable for CSV export"""
        return {
            'ID': self.id,
            'Title': self.title,
            'Description': self.description,
            'Category': self.category,
            'Severity': self.severity,
            'Status': self.status,
            'Latitude': self.latitude,
            'Longitude': self.longitude,
            'Address': self.address,
            'Photo': self.photo_original_name,
            'Created Date': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'Updated Date': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else '',
            'Reporter Name': self.reporter_name,
            'Reporter Email': self.reporter_email,
            'Reporter Phone': self.reporter_phone,
            'Admin Notes': self.admin_notes,
            'Resolved Date': self.resolved_at.strftime('%Y-%m-%d %H:%M:%S') if self.resolved_at else ''
        }

    @staticmethod
    def get_categories():
        return ['road', 'water', 'power', 'other']

    @staticmethod
    def get_severities():
        return ['low', 'medium', 'high', 'critical']

    @staticmethod
    def get_statuses():
        return ['reported', 'verified', 'in_progress', 'resolved']

