#!/usr/bin/env python
"""
Taekwondo Management System - User Manual Web Server
Run this file and open http://127.0.0.1:5000 in browser
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading
import time

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taekwondo Management System - User Manual</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .header h1 {
            color: #333;
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 16px;
        }
        
        .version-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 10px;
        }
        
        .nav-tabs {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
            background: white;
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .nav-btn {
            padding: 12px 24px;
            background: #f0f0f0;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .nav-btn:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }
        
        .nav-btn.active {
            background: #667eea;
            color: white;
        }
        
        .content {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            min-height: 500px;
        }
        
        .section {
            display: none;
        }
        
        .section.active {
            display: block;
        }
        
        h2 {
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        h3 {
            color: #555;
            margin: 20px 0 10px 0;
        }
        
        h4 {
            color: #667eea;
            margin: 15px 0 10px 0;
        }
        
        .card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
        }
        
        .card-warning {
            background: #fff3cd;
            border-left-color: #ffc107;
        }
        
        .card-success {
            background: #d4edda;
            border-left-color: #28a745;
        }
        
        .card-info {
            background: #d1ecf1;
            border-left-color: #17a2b8;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background: #667eea;
            color: white;
        }
        
        tr:hover {
            background: #f5f5f5;
        }
        
        code {
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 14px;
        }
        
        .url-box {
            background: #2d2d2d;
            color: #fff;
            padding: 15px;
            border-radius: 10px;
            font-family: monospace;
            font-size: 16px;
            margin: 10px 0;
        }
        
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
        }
        
        .badge-paid { background: #28a745; color: white; }
        .badge-pending { background: #ffc107; color: #333; }
        .badge-overdue { background: #dc3545; color: white; }
        
        .footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
            font-size: 12px;
        }
        
        @media (max-width: 768px) {
            .nav-btn { padding: 8px 16px; font-size: 12px; }
            .content { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🥋 Taekwondo Management System</h1>
            <p>Complete User Manual - Parent & Admin Guide</p>
            <span class="version-badge">Version 2.0 | April 2026</span>
        </div>
        
        <div class="nav-tabs">
            <button class="nav-btn active" onclick="showSection('overview')">📖 Overview</button>
            <button class="nav-btn" onclick="showSection('getting-started')">🚀 Getting Started</button>
            <button class="nav-btn" onclick="showSection('parent')">👨‍👩‍👧 Parent Portal</button>
            <button class="nav-btn" onclick="showSection('admin')">👨‍💼 Admin Guide</button>
            <button class="nav-btn" onclick="showSection('fees')">💰 Fee Management</button>
            <button class="nav-btn" onclick="showSection('attendance')">📋 Attendance</button>
            <button class="nav-btn" onclick="showSection('contacts')">📞 Contacts</button>
            <button class="nav-btn" onclick="showSection('troubleshoot')">🔧 Troubleshoot</button>
        </div>
        
        <div class="content">
            <!-- OVERVIEW SECTION -->
            <div id="overview" class="section active">
                <h2>📖 System Overview</h2>
                <p>Taekwondo Management System is a complete solution for managing Taekwondo clubs, students, fees, attendance, and parent communications.</p>
                
                <h3>User Roles</h3>
                <table>
                    <thead>
                        <tr><th>Role</th><th>Responsibilities</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>👨‍👩‍👧 <strong>Parent</strong></td><td>View child's fees, download receipts, check attendance, view schedule</td></tr>
                        <tr><td>🥋 <strong>Coach</strong></td><td>Mark attendance, view students</td></tr>
                        <tr><td>👨‍💼 <strong>Club Admin</strong></td><td>Manage coaches, schools, contacts, fees, attendance</td></tr>
                        <tr><td>⭐ <strong>Super Admin</strong></td><td>Manage ALL clubs, system settings</td></tr>
                    </tbody>
                </table>
                
                <div class="card card-info">
                    <strong>💡 Key Features:</strong>
                    <ul style="margin-top: 10px; margin-left: 20px;">
                        <li>Multiple club/tenant support</li>
                        <li>PDF receipt generation with permanent receipt numbers</li>
                        <li>Parent portal with child information</li>
                        <li>Attendance tracking with statistics</li>
                        <li>Contact management for emergency info</li>
                        <li>Mobile responsive design (works on tablet/phone)</li>
                    </ul>
                </div>
            </div>
            
            <!-- GETTING STARTED SECTION -->
            <div id="getting-started" class="section">
                <h2>🚀 Getting Started</h2>
                
                <h3>Starting the Server</h3>
                <div class="card">
                    <p>Run the batch file:</p>
                    <div class="url-box">start_server.bat</div>
                    <p>Or manually:</p>
                    <div class="url-box">
                        cd C:\\Users\\amyru\\taekwondo_system<br>
                        venv\\Scripts\\activate<br>
                        python manage.py runserver 0.0.0.0:8000
                    </div>
                </div>
                
                <h3>Access URLs</h3>
                <table>
                    <tr><th>Device</th><th>URL</th></tr>
                    <tr><td>💻 Laptop</td><td><code>http://127.0.0.1:8000/</code></td></tr>
                    <tr><td>📱 Tablet/Phone (same WiFi)</td><td><code>http://192.168.0.179:8000/</code></td></tr>
                </table>
                
                <h3>Default Login Credentials</h3>
                <div class="card">
                    <strong>👨‍💼 Super Admin:</strong><br>
                    Username: <code>joe</code><br>
                    Password: (your password)<br><br>
                    
                    <strong>👨‍👩‍👧 Parent:</strong><br>
                    IC Number: (student's IC number)<br>
                    Password: <code>123456</code>
                </div>
            </div>
            
            <!-- PARENT PORTAL SECTION -->
            <div id="parent" class="section">
                <h2>👨‍👩‍👧 Parent Portal Guide</h2>
                
                <h3>How to Login</h3>
                <div class="card">
                    <ol style="margin-left: 20px;">
                        <li>Go to home page (<code>http://192.168.0.179:8000/</code>)</li>
                        <li>Click <strong>"Parent Portal"</strong> card</li>
                        <li>Enter <strong>Student IC Number</strong></li>
                        <li>Enter <strong>Password</strong> (default: 123456)</li>
                        <li>Click <strong>"View Child Info"</strong></li>
                    </ol>
                </div>
                
                <h3>Parent Dashboard Tabs</h3>
                
                <h4>💰 Fees Tab</h4>
                <ul>
                    <li>View all monthly fees with amounts and due dates</li>
                    <li>Check payment status: <span class="badge badge-paid">PAID</span> <span class="badge badge-pending">PENDING</span> <span class="badge badge-overdue">OVERDUE</span></li>
                    <li><strong>Download PDF Receipt</strong> - Click download button next to paid fees</li>
                    <li>Total overdue amount shown at top</li>
                </ul>
                
                <h4>📝 Attendance Tab</h4>
                <ul>
                    <li>View attendance summary (Present/Absent counts)</li>
                    <li>See attendance rate percentage</li>
                    <li>Detailed attendance history with dates</li>
                </ul>
                
                <h4>📅 Class Schedule Tab</h4>
                <ul>
                    <li>View weekly class schedule</li>
                    <li>Shows day, time, belt level, instructor</li>
                </ul>
                
                <h4>📞 Contact Info Tab</h4>
                <ul>
                    <li>View coach and emergency contact information</li>
                    <li>Click phone number to call directly</li>
                    <li>Click email to send message</li>
                </ul>
                
                <h3>Multiple Children</h3>
                <div class="card card-info">
                    If you have multiple children, child selector buttons appear at the top.<br>
                    Click different child names to switch between them.
                </div>
                
                <h3>Downloading Receipt</h3>
                <div class="card card-success">
                    <strong>📄 Receipt Number is PERMANENT!</strong><br>
                    Once a fee is marked as paid, a receipt number (e.g., REC-000085) is generated and NEVER changes.<br>
                    You can download the same receipt anytime.
                </div>
            </div>
            
            <!-- ADMIN GUIDE SECTION -->
            <div id="admin" class="section">
                <h2>👨‍💼 Admin Guide</h2>
                
                <h3>How to Login as Admin</h3>
                <div class="card">
                    <ol style="margin-left: 20px;">
                        <li>Go to home page</li>
                        <li>Click <strong>"Coach Login"</strong> card</li>
                        <li>Enter username and password</li>
                        <li>Click <strong>"Enter Dojang"</strong></li>
                    </ol>
                </div>
                
                <h3>Admin Dashboard Cards</h3>
                <table>
                    <tr><th>Card</th><th>Function</th></tr>
                    <tr><td>⚙️ Admin Panel</td><td>Django admin interface (full control)</td></tr>
                    <tr><td>📊 Dashboard</td><td>Statistics and reports</td></tr>
                    <tr><td>💰 Fees Management</td><td>Manage student fees, mark paid</td></tr>
                    <tr><td>📞 Contact Management</td><td>Manage contact info (Club Admin only)</td></tr>
                    <tr><td>📋 Attendance</td><td>Mark student attendance</td></tr>
                </table>
                
                <h3>Club Admin Only Features</h3>
                <ul>
                    <li><strong>Manage Coaches</strong> - Add, edit, delete coaches</li>
                    <li><strong>Manage Schools</strong> - Add, edit, delete schools</li>
                    <li><strong>Assign Coaches to Schools</strong></li>
                    <li><strong>Contact Management</strong> - Add/Edit/Delete contacts</li>
                </ul>
                
                <h3>Super Admin Features</h3>
                <ul>
                    <li><strong>Club Switcher</strong> - Switch between different clubs</li>
                    <li>Access to ALL clubs data</li>
                    <li>System-wide settings via Django Admin</li>
                </ul>
            </div>
            
            <!-- FEE MANAGEMENT SECTION -->
            <div id="fees" class="section">
                <h2>💰 Fee Management Guide</h2>
                
                <h3>Marking a Fee as Paid</h3>
                <div class="card">
                    <ol style="margin-left: 20px;">
                        <li>Go to <strong>Fees Management</strong> from dashboard</li>
                        <li>Click on student name</li>
                        <li>Find the pending fee</li>
                        <li>Click <strong>"Mark as Paid"</strong> button</li>
                    </ol>
                </div>
                
                <h3>What Happens When Marking Paid?</h3>
                <div class="card card-success">
                    ✅ Status changes to "PAID"<br>
                    ✅ Paid date is recorded<br>
                    ✅ <strong>Receipt number auto-generates</strong> (e.g., REC-000086)<br>
                    ✅ Parent can immediately download receipt
                </div>
                
                <h3>Receipt Number Format</h3>
                <div class="url-box">REC-XXXXXX (6 digits, based on Fee ID)</div>
                
                <h3>Generating Monthly Fees</h3>
                <div class="card">
                    <p>Run this command to generate fees for all students:</p>
                    <div class="url-box">python manage.py generate_monthly_fees</div>
                    <p>For specific month:</p>
                    <div class="url-box">python manage.py generate_monthly_fees --month=2026-04</div>
                </div>
            </div>
            
            <!-- ATTENDANCE SECTION -->
            <div id="attendance" class="section">
                <h2>📋 Attendance Management</h2>
                
                <h3>Taking Attendance</h3>
                <div class="card">
                    <ol style="margin-left: 20px;">
                        <li>Go to <strong>Attendance</strong> from dashboard</li>
                        <li>Select class/session</li>
                        <li>Check present students</li>
                        <li>Submit attendance</li>
                    </ol>
                </div>
                
                <h3>Parent View</h3>
                <p>Parents can see their child's attendance history including:</p>
                <ul>
                    <li>Date of each class</li>
                    <li>Present/Absent status</li>
                    <li>Attendance rate percentage</li>
                </ul>
            </div>
            
            <!-- CONTACTS SECTION -->
            <div id="contacts" class="section">
                <h2>📞 Contact Management</h2>
                
                <h3>Adding a Contact (Club Admin)</h3>
                <div class="card">
                    <ol style="margin-left: 20px;">
                        <li>Go to <strong>Contact Management</strong> from dashboard</li>
                        <li>Click <strong>"+ Add Contact"</strong></li>
                        <li><strong>Option A:</strong> Select from existing user (auto-fills details)</li>
                        <li><strong>Option B:</strong> Manual entry (type all details)</li>
                        <li>Check "Emergency Contact" if applicable</li>
                        <li>Click <strong>"Save"</strong></li>
                    </ol>
                </div>
                
                <h3>Where Contacts Appear</h3>
                <div class="card card-info">
                    Contacts appear in Parent Portal under <strong>"📞 Contact Info"</strong> tab.<br>
                    Emergency contacts show 🚨 icon with "EMERGENCY" badge.
                </div>
                
                <h3>Editing/Deleting Contacts</h3>
                <ul>
                    <li>Click <strong>"Edit"</strong> on any contact card to modify</li>
                    <li>Click <strong>"Delete"</strong> to remove contact</li>
                </ul>
            </div>
            
            <!-- TROUBLESHOOTING SECTION -->
            <div id="troubleshoot" class="section">
                <h2>🔧 Troubleshooting Guide</h2>
                
                <h3>Tablet Cannot Connect</h3>
                <div class="card card-warning">
                    <strong>Problem:</strong> "127.0.0.1 refused to connect"<br><br>
                    <strong>Solutions:</strong>
                    <ul style="margin-top: 10px;">
                        <li>Make sure both devices on same WiFi network</li>
                        <li>Check laptop IP: Run <code>ipconfig</code> (Windows) or <code>ifconfig</code> (Mac)</li>
                        <li>Use correct IP: <code>http://192.168.x.x:8000/</code> (not 127.0.0.1)</li>
                        <li>Temporarily disable Windows Firewall</li>
                        <li>Restart server: <code>python manage.py runserver 0.0.0.0:8000</code></li>
                    </ul>
                </div>
                
                <h3>Receipt Won't Open</h3>
                <div class="card card-warning">
                    <strong>Solutions:</strong>
                    <ul>
                        <li>Check <code>reportlab</code> is installed: <code>pip show reportlab</code></li>
                        <li>Ensure fee status is "PAID"</li>
                        <li>Check receipt number exists in database</li>
                    </ul>
                </div>
                
                <h3>Parent Cannot Login</h3>
                <div class="card card-warning">
                    <strong>Solutions:</strong>
                    <ul>
                        <li>Verify student IC number is correct</li>
                        <li>Check student has parent linked in database</li>
                        <li>Default password is <code>123456</code></li>
                        <li>Check student is active (<code>is_active=True</code>)</li>
                    </ul>
                </div>
                
                <h3>Contact Info Not Showing</h3>
                <div class="card card-warning">
                    <strong>Solutions:</strong>
                    <ul>
                        <li>Add contacts via Contact Management page</li>
                        <li>Ensure contact belongs to correct club</li>
                        <li>Check parent's student is in that club</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            © 2026 Taekwondo Management System | All Rights Reserved
        </div>
    </div>
    
    <script>
        function showSection(sectionId) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Remove active class from all buttons
            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected section
            document.getElementById(sectionId).classList.add('active');
            
            // Highlight clicked button
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
"""

class ManualHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML.encode('utf-8'))
    
    def log_message(self, format, *args):
        pass  # Suppress console logs

def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')

def run_manual_server():
    port = 5000
    server = HTTPServer(('127.0.0.1', port), ManualHandler)
    
    print("\n" + "="*50)
    print("  TAEKWONDO SYSTEM - USER MANUAL")
    print("="*50)
    print(f"\n  Manual is running at:")
    print(f"  http://127.0.0.1:{port}")
    print(f"\n  Press Ctrl+C to stop the manual server")
    print("="*50 + "\n")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  Manual server stopped.\n")

if __name__ == "__main__":
    run_manual_server()