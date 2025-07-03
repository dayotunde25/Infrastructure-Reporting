#!/usr/bin/env python3
"""
Demo data creation script for Infrastructure Issue Reporter
Creates sample issues and admin user for testing
"""

import os
import sys
import hashlib
import uuid
from datetime import datetime, timedelta
import random

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import User, db
from src.models.issue import Issue
from src.main import app

def generate_demo_filename(original_name):
    """Generate a demo filename for testing"""
    timestamp = str(datetime.utcnow().timestamp())
    random_id = str(uuid.uuid4())
    hash_input = f"{timestamp}_{random_id}_{original_name}"
    file_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else 'jpg'
    return f"{file_hash}.{ext}"

def create_demo_data():
    """Create demo data for testing"""
    
    with app.app_context():
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User.create_admin_user(
                username='admin',
                email='admin@infrastructure-reporter.local',
                password='admin123'
            )
            db.session.add(admin)
            print("✓ Created admin user (username: admin, password: admin123)")
        else:
            print("✓ Admin user already exists")

        # Demo issues data
        demo_issues = [
            {
                'title': 'Large pothole on Main Street',
                'description': 'There is a significant pothole near the intersection of Main Street and Oak Avenue. It\'s about 2 feet wide and 6 inches deep, causing vehicles to swerve dangerously. This has been an ongoing issue for several weeks and poses a safety hazard, especially during rainy weather when the hole fills with water and becomes less visible.',
                'category': 'road',
                'severity': 'high',
                'latitude': 40.7589,
                'longitude': -73.9851,
                'address': '123 Main Street, New York, NY',
                'reporter_name': 'John Smith',
                'reporter_email': 'john.smith@email.com',
                'reporter_phone': '(555) 123-4567',
                'status': 'reported'
            },
            {
                'title': 'Broken water main flooding sidewalk',
                'description': 'A water main has burst underneath the sidewalk on Elm Street, causing continuous flooding. The water is flowing into the street and creating hazardous conditions for pedestrians and drivers. The issue started yesterday morning and has been getting progressively worse.',
                'category': 'water',
                'severity': 'critical',
                'latitude': 40.7505,
                'longitude': -73.9934,
                'address': '456 Elm Street, New York, NY',
                'reporter_name': 'Sarah Johnson',
                'reporter_email': 'sarah.j@email.com',
                'status': 'verified'
            },
            {
                'title': 'Flickering streetlight creating safety concern',
                'description': 'The streetlight at the corner of Pine Street and 2nd Avenue has been flickering intermittently for the past week. During the evening hours, this creates a safety concern for pedestrians and makes the intersection poorly lit. The light sometimes goes completely dark for several minutes at a time.',
                'category': 'power',
                'severity': 'medium',
                'latitude': 40.7282,
                'longitude': -73.9942,
                'address': 'Corner of Pine Street and 2nd Avenue, New York, NY',
                'reporter_name': 'Mike Davis',
                'reporter_email': 'mike.davis@email.com',
                'reporter_phone': '(555) 987-6543',
                'status': 'in_progress'
            },
            {
                'title': 'Damaged storm drain cover',
                'description': 'The storm drain cover on Oak Avenue is cracked and partially collapsed. This creates a tripping hazard for pedestrians and could potentially cause damage to vehicles. The metal grating is sharp and exposed, making it particularly dangerous for cyclists and pedestrians.',
                'category': 'other',
                'severity': 'medium',
                'latitude': 40.7614,
                'longitude': -73.9776,
                'address': '789 Oak Avenue, New York, NY',
                'reporter_name': 'Lisa Chen',
                'reporter_email': 'lisa.chen@email.com',
                'status': 'reported'
            },
            {
                'title': 'Resolved: Fixed broken traffic signal',
                'description': 'The traffic signal at the intersection of Broadway and 42nd Street was malfunctioning, showing red in all directions. This was causing significant traffic delays and safety concerns. The issue has been resolved and normal traffic flow has been restored.',
                'category': 'power',
                'severity': 'high',
                'latitude': 40.7580,
                'longitude': -73.9855,
                'address': 'Broadway and 42nd Street, New York, NY',
                'reporter_name': 'Robert Wilson',
                'reporter_email': 'robert.w@email.com',
                'reporter_phone': '(555) 456-7890',
                'status': 'resolved',
                'admin_notes': 'Contacted ConEd and traffic signal was repaired within 4 hours. Issue resolved successfully.',
                'resolved_at': datetime.utcnow() - timedelta(days=2)
            }
        ]

        # Create demo issues
        created_count = 0
        for issue_data in demo_issues:
            # Check if issue already exists (by title)
            existing = Issue.query.filter_by(title=issue_data['title']).first()
            if not existing:
                # Create timestamps
                created_at = datetime.utcnow() - timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                issue = Issue(
                    title=issue_data['title'],
                    description=issue_data['description'],
                    category=issue_data['category'],
                    severity=issue_data['severity'],
                    latitude=issue_data.get('latitude'),
                    longitude=issue_data.get('longitude'),
                    address=issue_data.get('address'),
                    reporter_name=issue_data.get('reporter_name'),
                    reporter_email=issue_data.get('reporter_email'),
                    reporter_phone=issue_data.get('reporter_phone'),
                    status=issue_data.get('status', 'reported'),
                    admin_notes=issue_data.get('admin_notes'),
                    resolved_at=issue_data.get('resolved_at'),
                    created_at=created_at,
                    updated_at=created_at
                )
                
                db.session.add(issue)
                created_count += 1
        
        # Commit all changes
        db.session.commit()
        
        print(f"✓ Created {created_count} demo issues")
        print(f"✓ Total issues in database: {Issue.query.count()}")
        
        print("\n" + "="*50)
        print("DEMO DATA CREATION COMPLETE")
        print("="*50)
        print("Admin Login Credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nApplication URL: http://localhost:5001")
        print("Admin Dashboard: http://localhost:5001/admin.html")
        print("="*50)

if __name__ == '__main__':
    create_demo_data()

