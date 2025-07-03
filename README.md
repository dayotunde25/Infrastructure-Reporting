# Infrastructure Issue Reporter

A production-ready, locally deployable web application that allows citizens to report infrastructure issues (e.g., potholes, broken pipes, faulty power lines) using geotagged photos. The application stores all data and media locally, works over LAN/intranet without internet access, and includes an admin dashboard for government officials or NGO partners to view, manage, and export reports.

## Features

### Core Functionality
- **Issue Reporting Interface**: Web form with photo upload, geolocation (auto or manual), category selection, severity levels, and contact information
- **Interactive Map View**: Display all submitted issues as markers on an interactive map using Leaflet with offline OpenStreetMap tiles
- **Admin Dashboard**: Comprehensive management interface with filtering, status updates, and export capabilities
- **Offline Operation**: Fully functional without internet connectivity, using local storage and cached map tiles

### Technical Features
- **Local Data Storage**: SQLite database with all data stored locally
- **File Management**: Secure photo storage with hashed filenames to prevent duplication
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **RESTful API**: Clean API endpoints for all CRUD operations
- **Authentication**: Secure admin login with password hashing
- **Export Functionality**: CSV export for external data analysis

## Technology Stack

- **Backend**: Python Flask with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (local storage)
- **Maps**: Leaflet.js with OpenStreetMap tiles
- **Authentication**: Flask sessions with bcrypt password hashing
- **File Storage**: Local filesystem with secure hashed filenames

## Project Structure

```
infrastructure-reporter/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── models/
│   │   ├── user.py            # User model with admin authentication
│   │   └── issue.py           # Issue model for infrastructure reports
│   ├── routes/
│   │   ├── user.py            # User-related routes
│   │   ├── issue.py           # Issue CRUD operations
│   │   └── auth.py            # Authentication routes
│   ├── static/
│   │   ├── index.html         # Main application interface
│   │   ├── admin.html         # Admin dashboard
│   │   ├── css/               # Stylesheets
│   │   ├── js/                # JavaScript files
│   │   └── uploads/           # Photo storage directory
│   └── database/
│       └── app.db             # SQLite database file
├── venv/                      # Python virtual environment
├── create_demo_data.py        # Demo data creation script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Quick Start

1. **Clone or extract the project**:
   ```bash
   cd infrastructure-reporter
   ```

2. **Set up Python virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create demo data** (optional but recommended):
   ```bash
   python create_demo_data.py
   ```

5. **Start the application**:
   ```bash
   python src/main.py
   ```

6. **Access the application**:
   - Main application: http://localhost:5001
   - Admin dashboard: http://localhost:5001/admin.html

### Admin Login Credentials
- **Username**: admin
- **Password**: admin123

*Note: Change these credentials in production by creating a new admin user.*

## Usage Guide

### For Citizens (Reporting Issues)

1. **Access the Application**: Open http://localhost:5001 in your web browser
2. **Report an Issue**:
   - Fill in the issue title and description
   - Select the appropriate category (Road, Water, Power, Other)
   - Choose severity level (Low, Medium, High, Critical)
   - Upload a photo (optional but recommended)
   - Use "Get Current Location" or manually enter coordinates
   - Provide contact information (optional)
   - Submit the report

3. **View Issues**:
   - Use the "Map View" tab to see issues on an interactive map
   - Use the "All Issues" tab to browse all reports with filtering options

### For Administrators

1. **Access Admin Dashboard**: Click "Admin" in the navigation or go to http://localhost:5001/admin.html
2. **Login**: Use the admin credentials (admin/admin123)
3. **Manage Issues**:
   - View statistics dashboard with issue counts by status
   - Filter issues by category, status, or other criteria
   - Update issue status (Reported → Verified → In Progress → Resolved)
   - Add admin notes to issues
   - Export data as CSV for external analysis

## API Documentation

### Issue Endpoints

- `GET /api/issues` - Retrieve all issues
- `POST /api/issues` - Create a new issue
- `GET /api/issues/<id>` - Get specific issue
- `PUT /api/issues/<id>` - Update issue (admin only)
- `DELETE /api/issues/<id>` - Delete issue (admin only)
- `GET /api/issues/categories` - Get available categories
- `GET /api/issues/export` - Export issues as CSV (admin only)

### Authentication Endpoints

- `POST /api/auth/login` - Admin login
- `POST /api/auth/logout` - Admin logout
- `GET /api/auth/status` - Check authentication status

### Example API Usage

```javascript
// Create a new issue
fetch('/api/issues', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        title: 'Pothole on Main Street',
        description: 'Large pothole causing traffic issues',
        category: 'road',
        severity: 'high',
        latitude: 40.7589,
        longitude: -73.9851,
        reporter_name: 'John Doe',
        reporter_email: 'john@example.com'
    })
});
```

## Deployment Options

### Local Development
The application runs on `localhost:5001` by default and is suitable for development and testing.

### LAN/Intranet Deployment
To make the application accessible to other devices on your network:

1. **Find your local IP address**:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. **Update the Flask configuration** in `src/main.py`:
   ```python
   app.run(host='0.0.0.0', port=5001, debug=False)
   ```

3. **Access from other devices**: Use your IP address (e.g., http://192.168.1.100:5001)

### Production Deployment
For production use, consider:

1. **Use a production WSGI server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5001 src.main:app
   ```

2. **Set up a reverse proxy** with Nginx or Apache
3. **Configure SSL/HTTPS** for secure communication
4. **Set up regular database backups**
5. **Change default admin credentials**

## Configuration

### Environment Variables
You can configure the application using environment variables:

- `FLASK_ENV`: Set to 'production' for production deployment
- `DATABASE_URL`: Custom database location (default: src/database/app.db)
- `UPLOAD_FOLDER`: Custom upload directory (default: src/static/uploads)
- `SECRET_KEY`: Flask secret key for sessions (auto-generated if not set)

### Database Configuration
The application uses SQLite by default, which is perfect for local deployment. For larger deployments, you can configure PostgreSQL by updating the database URL in `src/main.py`.

## Security Considerations

- **Admin Authentication**: Passwords are hashed using bcrypt
- **File Upload Security**: Only image files are allowed, with secure filename generation
- **SQL Injection Protection**: SQLAlchemy ORM provides protection against SQL injection
- **Session Security**: Flask sessions are used for admin authentication
- **Input Validation**: All user inputs are validated and sanitized

## Troubleshooting

### Common Issues

1. **Port 5001 already in use**:
   ```bash
   # Find and kill the process using port 5001
   lsof -ti:5001 | xargs kill -9
   ```

2. **Database errors**:
   ```bash
   # Delete and recreate the database
   rm src/database/app.db
   python create_demo_data.py
   ```

3. **Permission errors on uploads**:
   ```bash
   # Ensure upload directory has proper permissions
   chmod 755 src/static/uploads
   ```

4. **Map not loading**:
   - Check internet connectivity for initial tile download
   - Ensure Leaflet.js files are properly loaded

### Logs and Debugging
- Flask debug mode is enabled by default in development
- Check the console output for error messages
- Browser developer tools can help debug frontend issues

## Contributing

This is a self-contained application designed for local deployment. For modifications:

1. Follow PEP 8 coding standards for Python code
2. Test all changes thoroughly before deployment
3. Update documentation for any new features
4. Ensure backward compatibility with existing data

## License

This project is designed for local government and NGO use. Please ensure compliance with local data protection and privacy regulations when deploying.

## Support

For technical support or questions about deployment:
- Check the troubleshooting section above
- Review the API documentation for integration questions
- Ensure all prerequisites are properly installed

---

**Version**: 1.0.0  
**Last Updated**: June 2025  
**Compatibility**: Python 3.8+, Modern web browsers

