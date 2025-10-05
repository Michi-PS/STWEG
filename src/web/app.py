"""
STWEG Web-Interface
Flask-Anwendung mit Dashboard und API-Endpunkten
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

# Projekt-Pfade hinzufügen
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS

# Modelle importieren
from src.models.models import Base, Eigentuemer, Messpunkt, Verbrauchsdaten, Rechnung
from src.models.database import get_db_session, create_tables
from src.excel_analysis.excel_analyzer import ExcelAnalyzer

app = Flask(__name__)
CORS(app)

# Konfiguration
app.config['SECRET_KEY'] = 'stweg-development-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Upload-Verzeichnisse
UPLOAD_FOLDER = project_root / 'data' / 'uploads'
EXPORT_FOLDER = project_root / 'data' / 'exports'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['EXPORT_FOLDER'] = str(EXPORT_FOLDER)


@app.route('/')
def dashboard():
    """Hauptdashboard"""
    return render_template('dashboard.html')


@app.route('/api/status')
def api_status():
    """API: Aktueller Projektstatus"""
    try:
        # Datenbank-Status
        session = get_db_session()
        
        stats = {
            'timestamp': datetime.now().isoformat(),
            'project_status': {
                'phase': 'Phase 3: UX & Visualisierung',
                'progress': 65,
                'status': 'In Entwicklung'
            },
            'database': {
                'eigentuemer_count': session.query(Eigentuemer).count(),
                'messpunkte_count': session.query(Messpunkt).count(),
                'verbrauchsdaten_count': session.query(Verbrauchsdaten).count(),
                'rechnungen_count': session.query(Rechnung).count(),
                'active_eigentuemer': session.query(Eigentuemer).filter(Eigentuemer.aktiv == True).count()
            },
            'files': {
                'upload_folder': str(UPLOAD_FOLDER),
                'export_folder': str(EXPORT_FOLDER)
            }
        }
        
        session.close()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tests')
def api_tests():
    """API: Test-Status"""
    try:
        # Tests ausführen und Ergebnis parsen
        python_cmd = sys.executable  # Verwendet den gleichen Python-Interpreter
        result = subprocess.run([
            python_cmd, '-m', 'pytest', 'tests/', '--tb=short', '-q'
        ], capture_output=True, text=True, cwd=project_root)
        
        # Test-Ergebnisse parsen
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'exit_code': result.returncode,
            'success': result.returncode == 0,
            'output': result.stdout,
            'errors': result.stderr,
            'summary': parse_test_output(result.stdout)
        }
        
        return jsonify(test_results)
        
    except Exception as e:
        import traceback
        error_details = {
            'error': str(e),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().isoformat(),
            'project_root': str(project_root),
            'python_cmd': sys.executable
        }
        return jsonify(error_details), 500


@app.route('/api/excel/upload', methods=['POST'])
def api_excel_upload():
    """API: Excel-Datei hochladen und analysieren"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Keine Datei ausgewählt'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Keine Datei ausgewählt'}), 400
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Nur Excel-Dateien (.xlsx, .xls) erlaubt'}), 400
        
        # Datei speichern
        filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = Path(app.config['UPLOAD_FOLDER']) / 'excel' / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        file.save(str(filepath))
        
        # Excel-Datei analysieren
        analyzer = ExcelAnalyzer()
        analysis_result = analyzer.analyze_file(str(filepath))
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': str(filepath),
            'analysis': analysis_result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/excel/analyze/<filename>')
def api_excel_analyze(filename):
    """API: Hochgeladene Excel-Datei analysieren"""
    try:
        filepath = Path(app.config['UPLOAD_FOLDER']) / 'excel' / filename
        
        if not filepath.exists():
            return jsonify({'error': 'Datei nicht gefunden'}), 404
        
        analyzer = ExcelAnalyzer()
        analysis_result = analyzer.analyze_file(str(filepath))
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/database/sample-data', methods=['POST'])
def api_create_sample_data():
    """API: Beispieldaten erstellen"""
    try:
        session = get_db_session()
        
        # Beispieldaten erstellen
        eigentuemer = Eigentuemer.create_sample_data(session)
        messpunkte = Messpunkt.create_sample_data(session)
        verbrauchsdaten = Verbrauchsdaten.create_sample_data(session)
        rechnungen = Rechnung.create_sample_data(session)
        
        session.close()
        
        return jsonify({
            'success': True,
            'created': {
                'eigentuemer': len(eigentuemer),
                'messpunkte': len(messpunkte),
                'verbrauchsdaten': len(verbrauchsdaten),
                'rechnungen': len(rechnungen)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/database/clear', methods=['POST'])
def api_clear_database():
    """API: Datenbank leeren"""
    try:
        from src.models.database import drop_tables, create_tables
        
        drop_tables()
        create_tables()
        
        return jsonify({'success': True, 'message': 'Datenbank geleert'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def parse_test_output(output):
    """Parst pytest-Ausgabe und extrahiert Zusammenfassung"""
    lines = output.split('\n')
    summary = {'total': 0, 'passed': 0, 'failed': 0, 'errors': 0}
    
    for line in lines:
        # Verschiedene pytest-Formate unterstützen
        if 'passed' in line and ('failed' in line or 'warning' in line or 'in ' in line):
            # Beispiele: 
            # "24 passed, 1 warning in 0.59s"
            # "5 passed, 2 failed in 2.34s"
            # "3 passed, 1 error in 1.23s"
            
            import re
            
            # Regex für verschiedene Formate
            passed_match = re.search(r'(\d+)\s+passed', line)
            failed_match = re.search(r'(\d+)\s+failed', line)
            error_match = re.search(r'(\d+)\s+error', line)
            warning_match = re.search(r'(\d+)\s+warning', line)
            
            if passed_match:
                summary['passed'] = int(passed_match.group(1))
            if failed_match:
                summary['failed'] = int(failed_match.group(1))
            if error_match:
                summary['errors'] = int(error_match.group(1))
            
            # Total berechnen
            summary['total'] = summary['passed'] + summary['failed'] + summary['errors']
            break
    
    return summary


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint nicht gefunden'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Interner Server-Fehler'}), 500


if __name__ == '__main__':
    # Datenbank initialisieren
    create_tables()
    
    print("🚀 STWEG Web-Interface startet...")
    print(f"📁 Upload-Verzeichnis: {UPLOAD_FOLDER}")
    print(f"📁 Export-Verzeichnis: {EXPORT_FOLDER}")
    print("🌐 Dashboard: http://localhost:5000")
    print("📊 API-Status: http://localhost:5000/api/status")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
