#!/usr/bin/env python3
"""
ACEP HIPAA Security Rule Web Audit Assistant
A Flask-based audit tool for HIPAA Security Rule compliance assessment
Created by Chaitanya Eshwar Prasad
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hipaa-audit-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('database', exist_ok=True)

# Database configuration
DATABASE = 'database/hipaa_audit.db'

# Template helper functions
def get_file_icon(filename):
    """Get Bootstrap icon class based on file extension"""
    if not filename:
        return 'bi-file'
    
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    icon_map = {
        'pdf': 'bi-file-pdf',
        'doc': 'bi-file-word',
        'docx': 'bi-file-word',
        'xls': 'bi-file-excel',
        'xlsx': 'bi-file-excel',
        'ppt': 'bi-file-ppt',
        'pptx': 'bi-file-ppt',
        'jpg': 'bi-file-image',
        'jpeg': 'bi-file-image',
        'png': 'bi-file-image',
        'gif': 'bi-file-image',
        'txt': 'bi-file-text',
        'zip': 'bi-file-zip',
        'rar': 'bi-file-zip',
        'mp4': 'bi-file-play',
        'avi': 'bi-file-play',
        'mov': 'bi-file-play'
    }
    
    return icon_map.get(ext, 'bi-file')

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if not size_bytes:
        return '0 B'
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"

# Register template filters
app.jinja_env.filters['get_file_icon'] = get_file_icon
app.jinja_env.filters['format_file_size'] = format_file_size

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with required tables"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # HIPAA Security Rule Requirements table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS hipaa_requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            status TEXT DEFAULT 'Not Assessed',
            notes TEXT,
            assessed_by TEXT,
            assessed_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Evidence table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            description TEXT,
            uploaded_by TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (requirement_id) REFERENCES hipaa_requirements (requirement_id)
        )
    ''')
    
    # Add description column if it doesn't exist (for existing databases)
    try:
        conn.execute('ALTER TABLE evidence ADD COLUMN description TEXT')
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Risk register table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            likelihood INTEGER NOT NULL CHECK (likelihood BETWEEN 1 AND 5),
            impact INTEGER NOT NULL CHECK (impact BETWEEN 1 AND 5),
            risk_score INTEGER GENERATED ALWAYS AS (likelihood * impact) STORED,
            mitigation TEXT,
            owner TEXT,
            status TEXT DEFAULT 'Open',
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # PHI Tracking table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS phi_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phi_type TEXT NOT NULL,
            description TEXT,
            classification TEXT NOT NULL,
            access_patterns TEXT,
            disposal_procedures TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Business Associate Management table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS business_associates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            contract_status TEXT DEFAULT 'Active',
            compliance_status TEXT DEFAULT 'Under Review',
            last_assessment_date DATE,
            next_assessment_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    # Create default admin user if not exists
    admin_exists = conn.execute('SELECT id FROM users WHERE username = ?', ('acep',)).fetchone()
    if not admin_exists:
        password_hash = generate_password_hash('acep123')
        conn.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                    ('acep', password_hash, 'acep@chaitanyaeshwarprasad.com'))
        conn.commit()
    
    # Load HIPAA Security Rule requirements if not exists
    requirements_exist = conn.execute('SELECT COUNT(*) as count FROM hipaa_requirements').fetchone()
    if requirements_exist['count'] == 0:
        load_hipaa_requirements(conn)
    
    conn.close()

def load_hipaa_requirements(conn):
    """Load HIPAA Security Rule requirements into database"""
    requirements = [
        # Administrative Safeguards
        ('A.1', 'Security Management Process', 'Implement policies and procedures to prevent, detect, contain, and correct security violations. This includes risk analysis, risk management, sanction policy, and information system activity review.', 'Administrative Safeguards'),
        ('A.2', 'Assigned Security Responsibility', 'Identify the security official who is responsible for the development and implementation of the policies and procedures required by the Security Rule.', 'Administrative Safeguards'),
        ('A.3', 'Workforce Security', 'Implement procedures for the authorization and/or supervision of workforce members who work with ePHI, and procedures for determining access to ePHI.', 'Administrative Safeguards'),
        ('A.4', 'Information Access Management', 'Implement policies and procedures for granting access to ePHI, including access authorization, access establishment, and access modification.', 'Administrative Safeguards'),
        ('A.5', 'Security Awareness and Training Program', 'Implement a security awareness and training program for all members of the workforce, including management.', 'Administrative Safeguards'),
        ('A.6', 'Security Incident Procedures', 'Implement policies and procedures to address security incidents, including identification and response to suspected or known security incidents.', 'Administrative Safeguards'),
        ('A.7', 'Contingency Plan', 'Establish policies and procedures for responding to an emergency or other occurrence that damages systems containing ePHI.', 'Administrative Safeguards'),
        ('A.8', 'Evaluation', 'Perform a periodic technical and non-technical evaluation to establish the extent to which an entity\'s security policies and procedures meet the requirements of the Security Rule.', 'Administrative Safeguards'),
        ('A.9', 'Business Associate Contracts and Other Arrangements', 'Document the satisfactory assurances required by the Privacy Rule through written contracts or other arrangements with business associates.', 'Administrative Safeguards'),
        
        # Physical Safeguards
        ('P.1', 'Facility Access Controls', 'Implement policies and procedures to limit physical access to electronic information systems and the facility or facilities in which they are housed.', 'Physical Safeguards'),
        ('P.2', 'Workstation Use', 'Implement policies and procedures that specify the proper functions to be performed, the manner in which those functions are to be performed, and the physical attributes of the surroundings of a specific workstation or class of workstation.', 'Physical Safeguards'),
        ('P.3', 'Workstation Security', 'Implement physical safeguards for all workstations that access ePHI to restrict access to authorized users.', 'Physical Safeguards'),
        ('P.4', 'Device and Media Controls', 'Implement policies and procedures that govern the receipt and removal of hardware and electronic media that contain ePHI into and out of a facility.', 'Physical Safeguards'),
        
        # Technical Safeguards
        ('T.1', 'Access Control', 'Implement technical policies and procedures for electronic information systems that maintain ePHI to allow access only to those persons or software programs that have been granted access rights.', 'Technical Safeguards'),
        ('T.2', 'Audit Controls', 'Implement hardware, software, and/or procedural mechanisms that record and examine activity in information systems that contain or use ePHI.', 'Technical Safeguards'),
        ('T.3', 'Integrity', 'Implement policies and procedures to protect ePHI from improper alteration or destruction.', 'Technical Safeguards'),
        ('T.4', 'Person or Entity Authentication', 'Implement procedures to verify that a person or entity seeking access to ePHI is the one claimed.', 'Technical Safeguards'),
        ('T.5', 'Transmission Security', 'Implement technical security measures to guard against unauthorized access to ePHI that is being transmitted over an electronic communications network.', 'Technical Safeguards')
    ]
    
    for requirement_id, title, description, category in requirements:
        conn.execute('''
            INSERT OR IGNORE INTO hipaa_requirements (requirement_id, title, description, category)
            VALUES (?, ?, ?, ?)
        ''', (requirement_id, title, description, category))
    
    conn.commit()

# Authentication helper functions
def login_required(f):
    """Decorator to require login for routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with HIPAA compliance overview"""
    conn = get_db_connection()
    
    # Get requirement statistics
    total_requirements = conn.execute('SELECT COUNT(*) as count FROM hipaa_requirements').fetchone()['count']
    compliant_requirements = conn.execute("SELECT COUNT(*) as count FROM hipaa_requirements WHERE status = 'Compliant'").fetchone()['count']
    non_compliant_requirements = conn.execute("SELECT COUNT(*) as count FROM hipaa_requirements WHERE status = 'Not Compliant'").fetchone()['count']
    not_applicable_requirements = conn.execute("SELECT COUNT(*) as count FROM hipaa_requirements WHERE status = 'Not Applicable'").fetchone()['count']
    not_assessed_requirements = conn.execute("SELECT COUNT(*) as count FROM hipaa_requirements WHERE status = 'Not Assessed'").fetchone()['count']
    
    # Get risk statistics
    total_risks = conn.execute('SELECT COUNT(*) as count FROM risks').fetchone()['count']
    high_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score >= 15').fetchone()['count']
    medium_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score >= 8 AND risk_score < 15').fetchone()['count']
    low_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score < 8').fetchone()['count']
    
    # Get PHI tracking statistics
    total_phi_types = conn.execute('SELECT COUNT(*) as count FROM phi_tracking').fetchone()['count']
    
    # Get Business Associate statistics
    total_business_associates = conn.execute('SELECT COUNT(*) as count FROM business_associates').fetchone()['count']
    active_business_associates = conn.execute("SELECT COUNT(*) as count FROM business_associates WHERE contract_status = 'Active'").fetchone()['count']
    
    # Get recent activity
    recent_requirements = conn.execute('''
        SELECT requirement_id, title, status, assessed_at 
        FROM hipaa_requirements 
        WHERE assessed_at IS NOT NULL 
        ORDER BY assessed_at DESC 
        LIMIT 5
    ''').fetchall()
    
    # Calculate compliance percentage
    assessed_requirements = total_requirements - not_assessed_requirements
    compliance_percentage = round((compliant_requirements / assessed_requirements * 100) if assessed_requirements > 0 else 0, 1)
    
    # Get current date and time
    current_date = datetime.now().strftime('%d %B %Y')
    current_time = datetime.now().strftime('%H:%M')
    
    conn.close()
    
    return render_template('dashboard.html',
                         total_requirements=total_requirements,
                         compliant_requirements=compliant_requirements,
                         non_compliant_requirements=non_compliant_requirements,
                         not_applicable_requirements=not_applicable_requirements,
                         not_assessed_requirements=not_assessed_requirements,
                         compliance_percentage=compliance_percentage,
                         total_risks=total_risks,
                         high_risks=high_risks,
                         medium_risks=medium_risks,
                         low_risks=low_risks,
                         total_phi_types=total_phi_types,
                         total_business_associates=total_business_associates,
                         active_business_associates=active_business_associates,
                         recent_requirements=recent_requirements,
                         current_date=current_date,
                         current_time=current_time)

@app.route('/audit')
@login_required
def audit_checklist():
    """HIPAA Security Rule requirements checklist"""
    conn = get_db_connection()
    
    # Get all requirements grouped by category
    requirements = conn.execute('''
        SELECT * FROM hipaa_requirements 
        ORDER BY category, requirement_id
    ''').fetchall()
    
    # Group by category
    categories = {}
    for req in requirements:
        if req['category'] not in categories:
            categories[req['category']] = []
        categories[req['category']].append(req)
    
    conn.close()
    
    return render_template('audit_checklist.html', categories=categories)

@app.route('/audit/update', methods=['POST'])
@login_required
def update_requirement():
    """Update requirement status and notes"""
    requirement_id = request.form['requirement_id']
    status = request.form['status']
    notes = request.form['notes']
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE hipaa_requirements 
        SET status = ?, notes = ?, assessed_by = ?, assessed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
        WHERE requirement_id = ?
    ''', (status, notes, session['username'], requirement_id))
    conn.commit()
    conn.close()
    
    flash('Requirement updated successfully!', 'success')
    return redirect(url_for('audit_checklist'))

@app.route('/evidence')
@login_required
def evidence():
    """Evidence management for HIPAA requirements"""
    conn = get_db_connection()
    
    # Get all evidence with requirement details
    evidence_list = conn.execute('''
        SELECT e.*, h.title as requirement_title, h.requirement_id
        FROM evidence e
        JOIN hipaa_requirements h ON e.requirement_id = h.requirement_id
        ORDER BY e.uploaded_at DESC
    ''').fetchall()
    
    # Get requirements for dropdown
    requirements = conn.execute('SELECT requirement_id, title FROM hipaa_requirements ORDER BY requirement_id').fetchall()
    
    # Calculate today's uploads
    today = datetime.now().strftime('%Y-%m-%d')
    today_uploads = sum(1 for e in evidence_list if e['uploaded_at'] and str(e['uploaded_at'])[:10] == today)
    
    conn.close()
    
    return render_template('evidence.html', evidence_list=evidence_list, requirements=requirements, today_uploads=today_uploads)

@app.route('/evidence/upload', methods=['POST'])
@login_required
def upload_evidence():
    """Upload evidence file"""
    if 'file' not in request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('evidence'))
    
    file = request.files['file']
    requirement_id = request.form['requirement_id']
    description = request.form['description']
    
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('evidence'))
    
    if file:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO evidence (requirement_id, filename, original_filename, file_path, file_size, description, uploaded_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (requirement_id, unique_filename, filename, file_path, file_size, description, session['username']))
        conn.commit()
        conn.close()
        
        flash('Evidence uploaded successfully!', 'success')
    
    return redirect(url_for('evidence'))

@app.route('/evidence/download/<int:evidence_id>')
@login_required
def download_evidence(evidence_id):
    """Download evidence file"""
    conn = get_db_connection()
    evidence = conn.execute('SELECT * FROM evidence WHERE id = ?', (evidence_id,)).fetchone()
    conn.close()
    
    if evidence:
        return send_file(evidence['file_path'], as_attachment=True, download_name=evidence['original_filename'])
    
    flash('Evidence not found!', 'error')
    return redirect(url_for('evidence'))

@app.route('/evidence/delete/<int:evidence_id>', methods=['POST'])
@login_required
def delete_evidence(evidence_id):
    """Delete evidence file"""
    conn = get_db_connection()
    evidence = conn.execute('SELECT * FROM evidence WHERE id = ?', (evidence_id,)).fetchone()
    
    if evidence:
        # Delete file from filesystem
        try:
            os.remove(evidence['file_path'])
        except:
            pass
        
        # Delete from database
        conn.execute('DELETE FROM evidence WHERE id = ?', (evidence_id,))
        conn.commit()
        flash('Evidence deleted successfully!', 'success')
    else:
        flash('Evidence not found!', 'error')
    
    conn.close()
    return redirect(url_for('evidence'))

@app.route('/risks')
@login_required
def risk_register():
    """Risk register for HIPAA compliance"""
    conn = get_db_connection()
    
    risks = conn.execute('''
        SELECT * FROM risks 
        ORDER BY risk_score DESC, created_at DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('risk_register.html', risks=risks)

@app.route('/risks/add', methods=['POST'])
@login_required
def add_risk():
    """Add new risk to register"""
    title = request.form['title']
    description = request.form['description']
    likelihood = int(request.form['likelihood'])
    impact = int(request.form['impact'])
    mitigation = request.form['mitigation']
    owner = request.form['owner']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO risks (title, description, likelihood, impact, mitigation, owner, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, likelihood, impact, mitigation, owner, session['username']))
    conn.commit()
    conn.close()
    
    flash('Risk added successfully!', 'success')
    return redirect(url_for('risk_register'))

@app.route('/risks/update/<int:risk_id>', methods=['POST'])
@login_required
def update_risk(risk_id):
    """Update existing risk"""
    title = request.form['title']
    description = request.form['description']
    likelihood = int(request.form['likelihood'])
    impact = int(request.form['impact'])
    mitigation = request.form['mitigation']
    owner = request.form['owner']
    status = request.form['status']
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE risks 
        SET title = ?, description = ?, likelihood = ?, impact = ?, mitigation = ?, owner = ?, status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (title, description, likelihood, impact, mitigation, owner, status, risk_id))
    conn.commit()
    conn.close()
    
    flash('Risk updated successfully!', 'success')
    return redirect(url_for('risk_register'))

@app.route('/risks/delete/<int:risk_id>', methods=['POST'])
@login_required
def delete_risk(risk_id):
    """Delete risk from register"""
    conn = get_db_connection()
    conn.execute('DELETE FROM risks WHERE id = ?', (risk_id,))
    conn.commit()
    conn.close()
    
    flash('Risk deleted successfully!', 'success')
    return redirect(url_for('risk_register'))

@app.route('/phi-tracking')
@login_required
def phi_tracking():
    """PHI tracking and management"""
    conn = get_db_connection()
    
    phi_types = conn.execute('SELECT * FROM phi_tracking ORDER BY created_at DESC').fetchall()
    
    conn.close()
    
    return render_template('phi_tracking.html', phi_types=phi_types)

@app.route('/phi-tracking/add', methods=['POST'])
@login_required
def add_phi_type():
    """Add new PHI type"""
    phi_type = request.form['phi_type']
    description = request.form['description']
    classification = request.form['classification']
    access_patterns = request.form['access_patterns']
    disposal_procedures = request.form['disposal_procedures']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO phi_tracking (phi_type, description, classification, access_patterns, disposal_procedures)
        VALUES (?, ?, ?, ?, ?)
    ''', (phi_type, description, classification, access_patterns, disposal_procedures))
    conn.commit()
    conn.close()
    
    flash('PHI type added successfully!', 'success')
    return redirect(url_for('phi_tracking'))

@app.route('/phi-tracking/update/<int:phi_id>', methods=['POST'])
@login_required
def update_phi_type(phi_id):
    """Update existing PHI type"""
    phi_type = request.form['phi_type']
    description = request.form['description']
    classification = request.form['classification']
    access_patterns = request.form['access_patterns']
    disposal_procedures = request.form['disposal_procedures']
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE phi_tracking 
        SET phi_type = ?, description = ?, classification = ?, access_patterns = ?, disposal_procedures = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (phi_type, description, classification, access_patterns, disposal_procedures, phi_id))
    conn.commit()
    conn.close()
    
    flash('PHI type updated successfully!', 'success')
    return redirect(url_for('phi_tracking'))

@app.route('/phi-tracking/delete/<int:phi_id>', methods=['POST'])
@login_required
def delete_phi_type(phi_id):
    """Delete PHI type"""
    conn = get_db_connection()
    conn.execute('DELETE FROM phi_tracking WHERE id = ?', (phi_id,))
    conn.commit()
    conn.close()
    
    flash('PHI type deleted successfully!', 'success')
    return redirect(url_for('phi_tracking'))

@app.route('/business-associates')
@login_required
def business_associates():
    """Business Associate management"""
    conn = get_db_connection()
    
    business_associates_list = conn.execute('SELECT * FROM business_associates ORDER BY created_at DESC').fetchall()
    
    conn.close()
    
    return render_template('business_associates.html', business_associates=business_associates_list)

@app.route('/business-associates/add', methods=['POST'])
@login_required
def add_business_associate():
    """Add new Business Associate"""
    name = request.form['name']
    contact_person = request.form['contact_person']
    email = request.form['email']
    phone = request.form['phone']
    contract_status = request.form.get('contract_status', 'Active')
    compliance_status = request.form.get('compliance_status', 'Not Assessed')
    last_assessment_date = request.form.get('last_assessment_date')
    next_assessment_date = request.form.get('next_assessment_date')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO business_associates (name, contact_person, email, phone, contract_status, compliance_status, last_assessment_date, next_assessment_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, contact_person, email, phone, contract_status, compliance_status, last_assessment_date, next_assessment_date))
    conn.commit()
    conn.close()
    
    flash('Business Associate added successfully!', 'success')
    return redirect(url_for('business_associates'))

@app.route('/business-associates/edit/<int:ba_id>', methods=['POST'])
@login_required
def edit_business_associate(ba_id):
    """Edit Business Associate"""
    name = request.form['name']
    contact_person = request.form['contact_person']
    email = request.form['email']
    phone = request.form['phone']
    contract_status = request.form.get('contract_status', 'Active')
    compliance_status = request.form.get('compliance_status', 'Not Assessed')
    last_assessment_date = request.form.get('last_assessment_date')
    next_assessment_date = request.form.get('next_assessment_date')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE business_associates 
        SET name = ?, contact_person = ?, email = ?, phone = ?, contract_status = ?, compliance_status = ?, last_assessment_date = ?, next_assessment_date = ?
        WHERE id = ?
    ''', (name, contact_person, email, phone, contract_status, compliance_status, last_assessment_date, next_assessment_date, ba_id))
    conn.commit()
    conn.close()
    
    flash('Business Associate updated successfully!', 'success')
    return redirect(url_for('business_associates'))

@app.route('/business-associates/assess/<int:ba_id>', methods=['POST'])
@login_required
def conduct_assessment(ba_id):
    """Conduct Business Associate Assessment"""
    compliance_status = request.form['compliance_status']
    assessment_date = request.form['assessment_date']
    assessment_notes = request.form.get('assessment_notes', '')
    next_assessment_date = request.form.get('next_assessment_date')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE business_associates 
        SET compliance_status = ?, last_assessment_date = ?, next_assessment_date = ?
        WHERE id = ?
    ''', (compliance_status, assessment_date, next_assessment_date, ba_id))
    conn.commit()
    conn.close()
    
    flash('Assessment completed successfully!', 'success')
    return redirect(url_for('business_associates'))

@app.route('/reports')
@login_required
def reports():
    """Report generation interface"""
    conn = get_db_connection()
    
    # Get summary statistics for reports
    total_requirements = conn.execute('SELECT COUNT(*) as count FROM hipaa_requirements').fetchone()['count']
    compliant_requirements = conn.execute("SELECT COUNT(*) as count FROM hipaa_requirements WHERE status = 'Compliant'").fetchone()['count']
    total_risks = conn.execute('SELECT COUNT(*) as count FROM risks').fetchone()['count']
    high_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score >= 15').fetchone()['count']
    
    conn.close()
    
    return render_template('reports.html', 
                         total_requirements=total_requirements,
                         compliant_requirements=compliant_requirements,
                         total_risks=total_risks,
                         high_risks=high_risks)

@app.route('/reports/generate', methods=['POST'])
@login_required
def generate_report():
    """Generate HIPAA compliance report"""
    try:
        report_type = request.form.get('report_type', 'compliance')
        
        conn = get_db_connection()
        
        if report_type == 'compliance':
            # Generate compliance report
            try:
                requirements = conn.execute('''
                    SELECT * FROM hipaa_requirements 
                    ORDER BY category, requirement_id
                ''').fetchall()
                
                # Get evidence with LEFT JOIN to handle cases where there's no evidence
                evidence = conn.execute('''
                    SELECT e.*, h.title as requirement_title 
                    FROM evidence e 
                    LEFT JOIN hipaa_requirements h ON e.requirement_id = h.requirement_id
                ''').fetchall()
                
                risks = conn.execute('SELECT * FROM risks ORDER BY risk_score DESC').fetchall()
                
                # Calculate compliance statistics
                total_requirements = len(requirements) if requirements else 0
                compliant_requirements = len([r for r in requirements if r['status'] == 'Compliant']) if requirements else 0
                non_compliant_requirements = len([r for r in requirements if r['status'] == 'Not Compliant']) if requirements else 0
                not_applicable_requirements = len([r for r in requirements if r['status'] == 'Not Applicable']) if requirements else 0
                not_assessed_requirements = len([r for r in requirements if r['status'] == 'Not Assessed']) if requirements else 0
                
                # Calculate compliance percentage
                assessed_requirements = total_requirements - not_assessed_requirements
                compliance_percentage = round((compliant_requirements / assessed_requirements * 100) if assessed_requirements > 0 else 0, 1)
                
                # Get evidence count
                evidence_count = len(evidence) if evidence else 0
                
                # Get risk statistics
                high_risks = len([r for r in risks if r['risk_score'] >= 15]) if risks else 0
                medium_risks = len([r for r in risks if 8 <= r['risk_score'] < 15]) if risks else 0
                low_risks = len([r for r in risks if r['risk_score'] < 8]) if risks else 0
                
                conn.close()
                
                # Debug information
                print(f"DEBUG: Generating report with {total_requirements} requirements, {evidence_count} evidence, {len(risks) if risks else 0} risks")
                
                return render_template('report.html',
                                     report_type='HIPAA Security Rule Compliance Report',
                                     requirements=requirements or [],
                                     evidence=evidence or [],
                                     risks=risks or [],
                                     total_requirements=total_requirements,
                                     total_controls=total_requirements,
                                     compliant_requirements=compliant_requirements,
                                     compliant_controls=compliant_requirements,
                                     non_compliant_controls=non_compliant_requirements,
                                     non_compliant_requirements=non_compliant_requirements,
                                     not_applicable_requirements=not_applicable_requirements,
                                     not_applicable_controls=not_applicable_requirements,
                                     not_assessed_requirements=not_assessed_requirements,
                                     not_assessed_controls=not_assessed_requirements,
                                     compliance_percentage=compliance_percentage,
                                     evidence_count=evidence_count,
                                     high_risks=high_risks,
                                     medium_risks=medium_risks,
                                     low_risks=low_risks,
                                     generated_at=datetime.now())
            
            except Exception as db_error:
                conn.close()
                print(f"Database error in report generation: {db_error}")
                flash(f'Database error while generating report: {str(db_error)}', 'error')
                return redirect(url_for('reports'))
        elif report_type == 'evidence':
            # Generate evidence report
            try:
                evidence = conn.execute('''
                    SELECT e.*, h.title as requirement_title 
                    FROM evidence e 
                    LEFT JOIN hipaa_requirements h ON e.requirement_id = h.requirement_id
                    ORDER BY e.uploaded_at DESC
                ''').fetchall()
                
                # Calculate today's uploads
                today = datetime.now().strftime('%Y-%m-%d')
                today_uploads = sum(1 for e in evidence if e['uploaded_at'] and str(e['uploaded_at'])[:10] == today) if evidence else 0
                
                conn.close()
                
                return render_template('evidence_report.html',
                                     evidence=evidence or [],
                                     today_uploads=today_uploads,
                                     generated_at=datetime.now(),
                                     generated_by=session['username'])
            except Exception as db_error:
                conn.close()
                print(f"Database error in evidence report: {db_error}")
                flash(f'Database error while generating evidence report: {str(db_error)}', 'error')
                return redirect(url_for('reports'))
                
        elif report_type == 'risk':
            # Generate risk report
            try:
                risks = conn.execute('SELECT * FROM risks ORDER BY risk_score DESC').fetchall()
                
                conn.close()
                
                return render_template('risk_report.html',
                                     risks=risks or [],
                                     generated_at=datetime.now(),
                                     generated_by=session['username'])
            except Exception as db_error:
                conn.close()
                print(f"Database error in risk report: {db_error}")
                flash(f'Database error while generating risk report: {str(db_error)}', 'error')
                return redirect(url_for('reports'))
        else:
            conn.close()
            flash('Invalid report type!', 'error')
            return redirect(url_for('reports'))
            
    except Exception as general_error:
        print(f"General error in report generation: {general_error}")
        flash(f'Error generating report: {str(general_error)}', 'error')
        return redirect(url_for('reports'))

@app.route('/api/requirements')
@login_required
def api_requirements():
    """API endpoint for requirements data"""
    conn = get_db_connection()
    
    requirements = conn.execute('''
        SELECT requirement_id, title, status, category, assessed_at
        FROM hipaa_requirements 
        ORDER BY category, requirement_id
    ''').fetchall()
    
    conn.close()
    
    return jsonify([dict(req) for req in requirements])

@app.route('/api/compliance-stats')
@login_required
def api_compliance_stats():
    """API endpoint for compliance statistics"""
    conn = get_db_connection()
    
    # Get compliance statistics
    total_requirements = conn.execute('SELECT COUNT(*) as count FROM hipaa_requirements').fetchone()['count']
    compliant_requirements = conn.execute("SELECT COUNT(*) as count FROM hipaa_requirements WHERE status = 'Compliant'").fetchone()['count']
    non_compliant_requirements = conn.execute("SELECT COUNT(*) as count FROM hipaa_requirements WHERE status = 'Not Compliant'").fetchone()['count']
    not_applicable_requirements = conn.execute("SELECT COUNT(*) as count FROM hipaa_requirements WHERE status = 'Not Applicable'").fetchone()['count']
    not_assessed_requirements = conn.execute("SELECT COUNT(*) as count FROM hipaa_requirements WHERE status = 'Not Assessed'").fetchone()['count']
    
    # Get risk statistics
    total_risks = conn.execute('SELECT COUNT(*) as count FROM risks').fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'total': total_requirements,
        'compliant': compliant_requirements,
        'non_compliant': non_compliant_requirements,
        'not_applicable': not_applicable_requirements,
        'not_assessed': not_assessed_requirements,
        'total_risks': total_risks
    })

@app.route('/api/evidence-stats')
@login_required
def api_evidence_stats():
    """API endpoint for evidence statistics"""
    conn = get_db_connection()
    
    total_evidence = conn.execute('SELECT COUNT(*) as count FROM evidence').fetchone()['count']
    total_size = conn.execute('SELECT SUM(file_size) as size FROM evidence').fetchone()['size'] or 0
    
    conn.close()
    
    return jsonify({
        'total': total_evidence,
        'total_size': total_size
    })

@app.route('/api/ba-stats')
@login_required
def api_ba_stats():
    """API endpoint for business associate statistics"""
    conn = get_db_connection()
    
    total_ba = conn.execute('SELECT COUNT(*) as count FROM business_associates').fetchone()['count']
    active_ba = conn.execute("SELECT COUNT(*) as count FROM business_associates WHERE contract_status = 'Active'").fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'total': total_ba,
        'active': active_ba
    })

@app.route('/debug/database')
@login_required
def debug_database():
    """Debug endpoint to check database status"""
    try:
        conn = get_db_connection()
        
        # Check if tables exist and have data
        tables_info = {}
        
        # Check hipaa_requirements
        req_count = conn.execute('SELECT COUNT(*) as count FROM hipaa_requirements').fetchone()['count']
        req_sample = conn.execute('SELECT requirement_id, title, status FROM hipaa_requirements LIMIT 3').fetchall()
        tables_info['hipaa_requirements'] = {
            'count': req_count,
            'sample': [dict(r) for r in req_sample]
        }
        
        # Check evidence
        evidence_count = conn.execute('SELECT COUNT(*) as count FROM evidence').fetchone()['count']
        tables_info['evidence'] = {'count': evidence_count}
        
        # Check risks
        risk_count = conn.execute('SELECT COUNT(*) as count FROM risks').fetchone()['count']
        tables_info['risks'] = {'count': risk_count}
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'database_file': DATABASE,
            'tables': tables_info
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'database_file': DATABASE
        })

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
