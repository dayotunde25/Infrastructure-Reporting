import os
import hashlib
import uuid
from datetime import datetime
from flask import Blueprint, jsonify, request, current_app, send_from_directory
from werkzeug.utils import secure_filename
from src.models.user import db
from src.models.issue import Issue

issue_bp = Blueprint('issue', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_hashed_filename(original_filename):
    """Generate a hashed filename to avoid duplicates and conflicts"""
    # Get file extension
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    
    # Generate hash based on timestamp and random UUID
    timestamp = str(datetime.utcnow().timestamp())
    random_id = str(uuid.uuid4())
    hash_input = f"{timestamp}_{random_id}_{original_filename}"
    
    # Create SHA256 hash
    file_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    return f"{file_hash}.{ext}" if ext else file_hash

@issue_bp.route('/issues', methods=['GET'])
def get_issues():
    """Get all issues with optional filtering"""
    try:
        # Get query parameters for filtering
        category = request.args.get('category')
        status = request.args.get('status')
        severity = request.args.get('severity')
        
        # Build query
        query = Issue.query
        
        if category and category in Issue.get_categories():
            query = query.filter(Issue.category == category)
        
        if status and status in Issue.get_statuses():
            query = query.filter(Issue.status == status)
            
        if severity and severity in Issue.get_severities():
            query = query.filter(Issue.severity == severity)
        
        # Order by creation date (newest first)
        issues = query.order_by(Issue.created_at.desc()).all()
        
        return jsonify([issue.to_dict() for issue in issues])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@issue_bp.route('/issues', methods=['POST'])
def create_issue():
    """Create a new issue with optional photo upload"""
    try:
        # Handle multipart form data
        data = request.form.to_dict()
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'severity']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate category and severity
        if data['category'] not in Issue.get_categories():
            return jsonify({'error': 'Invalid category'}), 400
            
        if data['severity'] not in Issue.get_severities():
            return jsonify({'error': 'Invalid severity'}), 400
        
        # Handle photo upload
        photo_filename = None
        photo_original_name = None
        
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                # Generate hashed filename
                photo_filename = generate_hashed_filename(file.filename)
                photo_original_name = secure_filename(file.filename)
                
                # Save file
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename)
                file.save(file_path)
        
        # Create issue
        issue = Issue(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            severity=data['severity'],
            latitude=float(data['latitude']) if data.get('latitude') else None,
            longitude=float(data['longitude']) if data.get('longitude') else None,
            address=data.get('address'),
            photo_filename=photo_filename,
            photo_original_name=photo_original_name,
            reporter_name=data.get('reporter_name'),
            reporter_email=data.get('reporter_email'),
            reporter_phone=data.get('reporter_phone')
        )
        
        db.session.add(issue)
        db.session.commit()
        
        return jsonify(issue.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@issue_bp.route('/issues/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    """Get a specific issue by ID"""
    try:
        issue = Issue.query.get_or_404(issue_id)
        return jsonify(issue.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@issue_bp.route('/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    """Update an issue (admin functionality)"""
    try:
        issue = Issue.query.get_or_404(issue_id)
        data = request.json
        
        # Update allowed fields
        if 'status' in data and data['status'] in Issue.get_statuses():
            issue.status = data['status']
            if data['status'] == 'resolved':
                issue.resolved_at = datetime.utcnow()
        
        if 'admin_notes' in data:
            issue.admin_notes = data['admin_notes']
        
        if 'severity' in data and data['severity'] in Issue.get_severities():
            issue.severity = data['severity']
        
        issue.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(issue.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@issue_bp.route('/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    """Delete an issue (admin functionality)"""
    try:
        issue = Issue.query.get_or_404(issue_id)
        
        # Delete associated photo file if it exists
        if issue.photo_filename:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], issue.photo_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.delete(issue)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@issue_bp.route('/issues/<int:issue_id>/photo', methods=['GET'])
def get_issue_photo(issue_id):
    """Get the photo for a specific issue"""
    try:
        issue = Issue.query.get_or_404(issue_id)
        
        if not issue.photo_filename:
            return jsonify({'error': 'No photo available for this issue'}), 404
        
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], issue.photo_filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@issue_bp.route('/issues/export/csv', methods=['GET'])
def export_issues_csv():
    """Export all issues as CSV"""
    try:
        import csv
        import io
        
        # Get all issues
        issues = Issue.query.order_by(Issue.created_at.desc()).all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'ID', 'Title', 'Description', 'Category', 'Severity', 'Status',
            'Latitude', 'Longitude', 'Address', 'Photo', 'Created Date',
            'Updated Date', 'Reporter Name', 'Reporter Email', 'Reporter Phone',
            'Admin Notes', 'Resolved Date'
        ])
        
        writer.writeheader()
        for issue in issues:
            writer.writerow(issue.to_csv_dict())
        
        # Prepare response
        output.seek(0)
        csv_data = output.getvalue()
        output.close()
        
        from flask import Response
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=issues_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@issue_bp.route('/issues/stats', methods=['GET'])
def get_issue_stats():
    """Get statistics about issues"""
    try:
        total_issues = Issue.query.count()
        
        # Count by status
        status_counts = {}
        for status in Issue.get_statuses():
            status_counts[status] = Issue.query.filter(Issue.status == status).count()
        
        # Count by category
        category_counts = {}
        for category in Issue.get_categories():
            category_counts[category] = Issue.query.filter(Issue.category == category).count()
        
        # Count by severity
        severity_counts = {}
        for severity in Issue.get_severities():
            severity_counts[severity] = Issue.query.filter(Issue.severity == severity).count()
        
        return jsonify({
            'total_issues': total_issues,
            'status_counts': status_counts,
            'category_counts': category_counts,
            'severity_counts': severity_counts
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@issue_bp.route('/issues/categories', methods=['GET'])
def get_categories():
    """Get available categories"""
    return jsonify(Issue.get_categories())

@issue_bp.route('/issues/severities', methods=['GET'])
def get_severities():
    """Get available severities"""
    return jsonify(Issue.get_severities())

@issue_bp.route('/issues/statuses', methods=['GET'])
def get_statuses():
    """Get available statuses"""
    return jsonify(Issue.get_statuses())

