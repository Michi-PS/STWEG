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
        
        # Alte Upload-Dateien bereinigen (nur die letzten 5 behalten)
        cleanup_old_uploads()
        
        # Datei speichern
        filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = Path(app.config['UPLOAD_FOLDER']) / 'excel' / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        file.save(str(filepath))
        
        # Excel-Datei nur speichern (keine Analyse mit ExcelAnalyzer - NaN-Problem!)
        # Die Analyse erfolgt später über /api/excel/explore/<filename>
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': str(filepath)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def cleanup_old_uploads():
    """Alte Upload-Dateien bereinigen (nur die letzten 5 behalten)"""
    try:
        excel_folder = Path(app.config['UPLOAD_FOLDER']) / 'excel'
        if not excel_folder.exists():
            return
        
        # Alle Excel-Dateien finden und nach Änderungszeit sortieren
        excel_files = []
        for pattern in ['*.xlsx', '*.xls']:
            excel_files.extend(excel_folder.glob(pattern))
        
        # Nach Änderungszeit sortieren (neueste zuerst)
        excel_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        # Nur die letzten 5 Dateien behalten, Rest löschen
        if len(excel_files) > 5:
            for old_file in excel_files[5:]:
                try:
                    old_file.unlink()
                    print(f"🗑️ Alte Upload-Datei gelöscht: {old_file.name}")
                except Exception as e:
                    print(f"⚠️ Fehler beim Löschen von {old_file.name}: {e}")
                    
    except Exception as e:
        print(f"⚠️ Fehler beim Bereinigen alter Uploads: {e}")


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

@app.route('/api/excel/explore/<filename>')
def api_excel_explore(filename):
    """API: ZEV-Datei mit intelligentem Parser erkunden"""
    try:
        filepath = Path(app.config['UPLOAD_FOLDER']) / 'excel' / filename
        
        if not filepath.exists():
            return jsonify({'error': 'Datei nicht gefunden'}), 404
        
        # Simple ZEV-Parser verwenden (NaN-frei)
        from src.excel_analysis.simple_zev_parser import SimpleZEVParser
        parser = SimpleZEVParser()
        
        # ZEV-Datei parsen
        print(f"🔍 DEBUG: Parse ZEV-Datei: {filepath}")
        result = parser.parse_zev_file(str(filepath))
        print(f"🔍 DEBUG: Result: {type(result)}")
        
        print(f"🔍 DEBUG: Final Result: {type(result)}")
        print(f"🔍 DEBUG: Zähler Overview: {len(result['zaehler_overview'])}")
        
        # JSON-Serialisierung testen
        try:
            json.dumps(result)
            print("✅ DEBUG: JSON-Serialisierung erfolgreich")
        except Exception as json_error:
            print(f"❌ DEBUG: JSON-Fehler: {json_error}")
            # Fallback: Minimale Response
            result = {
                'file_name': filename,
                'structure_verified': False,
                'structure_info': {'error': 'JSON-Serialisierung fehlgeschlagen'},
                'summary': {'total_zaehler': 0, 'total_messpunkte': 0},
                'zaehler_overview': []
            }
        
        return jsonify({
            'success': True,
            'result': result
        })
        
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


# ==================== MODUL-APIs ====================

@app.route('/api/modules')
def api_modules():
    """API: Verfügbare Module"""
    return jsonify({
        'modules': [
            {
                'id': 'excel-analysis',
                'name': 'Excel-Analyse & Kostenaufteilung',
                'description': 'Excel-Dateien analysieren und Kosten aufteilen',
                'status': 'active',
                'icon': 'fas fa-file-excel'
            },
            {
                'id': 'development',
                'name': 'Development & Monitoring',
                'description': 'Projektfortschritt und Entwicklungs-Tools',
                'status': 'active',
                'icon': 'fas fa-code'
            },
            {
                'id': 'pdf-billing',
                'name': 'PDF-Rechnungen',
                'description': 'PDF-Rechnungen erstellen und verwalten',
                'status': 'planned',
                'icon': 'fas fa-file-pdf'
            }
        ]
    })


@app.route('/api/modules/status')
def api_modules_status():
    """API: Modul-Status"""
    return jsonify({
        'active_module': 'excel-analysis',
        'modules': {
            'excel-analysis': {
                'status': 'active',
                'last_used': datetime.now().isoformat(),
                'features': ['excel_upload', 'excel_analysis', 'data_management']
            },
            'development': {
                'status': 'active',
                'last_used': datetime.now().isoformat(),
                'features': ['test_monitoring', 'roadmap_view', 'user_stories']
            },
            'pdf-billing': {
                'status': 'planned',
                'last_used': None,
                'features': []
            }
        }
    })


@app.route('/api/modules/excel')
def api_modules_excel():
    """API: Excel-Modul-spezifische Daten"""
    try:
        # Excel-Dateien zählen
        excel_folder = UPLOAD_FOLDER / 'excel'
        excel_files = list(excel_folder.glob('*.xlsx')) + list(excel_folder.glob('*.xls'))
        
        # Letzte Upload-Zeit
        last_upload = None
        last_filename = None
        if excel_files:
            last_file = max(excel_files, key=lambda f: f.stat().st_mtime)
            last_upload = datetime.fromtimestamp(last_file.stat().st_mtime).strftime('%d.%m.%Y %H:%M')
            last_filename = last_file.name
        
        return jsonify({
            'excel_files_count': len(excel_files),
            'last_upload': last_upload,
            'last_filename': last_filename,
            'upload_folder': str(excel_folder),
            'supported_formats': ['.xlsx', '.xls'],
            'files': [f.name for f in excel_files[-5:]]  # Nur die letzten 5 Dateien
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/roadmap')
def api_roadmap():
    """API: Roadmap-Daten (vereinfacht)"""
    try:
        from src.utils.markdown_parser import MarkdownParser
        parser = MarkdownParser(project_root)
        roadmap_data = parser.parse_roadmap()
        
        if 'error' in roadmap_data:
            return jsonify(roadmap_data), 404
        
        # Vereinfachte Antwort für Dashboard
        return jsonify({
            'current_phase': roadmap_data['status']['current_phase'],
            'next_steps': roadmap_data['status']['next_steps'],
            'progress': roadmap_data['status']['progress_percentage'],
            'total_phases': roadmap_data['total_phases'],
            'completed_phases': roadmap_data['completed_phases'],
            'last_updated': datetime.now().isoformat()
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/roadmap/full')
def api_roadmap_full():
    """API: Vollständige Roadmap-Daten mit allen Phasen"""
    try:
        from src.utils.markdown_parser import MarkdownParser
        parser = MarkdownParser(project_root)
        roadmap_data = parser.parse_roadmap()
        
        if 'error' in roadmap_data:
            return jsonify(roadmap_data), 404
        
        return jsonify(roadmap_data)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user-stories')
def api_user_stories():
    """API: User Stories-Daten (vereinfacht)"""
    try:
        from src.utils.markdown_parser import MarkdownParser
        parser = MarkdownParser(project_root)
        user_stories_data = parser.parse_user_stories()
        
        if 'error' in user_stories_data:
            return jsonify(user_stories_data), 404
        
        # Vereinfachte Antwort für Dashboard
        recent_stories = []
        for epic in user_stories_data['epics'][-2:]:  # Letzte 2 Epics
            for story in epic['stories'][-1:]:  # Letzte Story pro Epic
                recent_stories.append(f"US-{story['number']}: {story['title']}")
        
        return jsonify({
            'completed': user_stories_data['completed_stories'],
            'total': user_stories_data['total_stories'],
            'recent_stories': recent_stories,
            'progress_percentage': user_stories_data['progress_percentage'],
            'total_epics': user_stories_data['total_epics']
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user-stories/full')
def api_user_stories_full():
    """API: Vollständige User Stories-Daten mit allen Epics"""
    try:
        from src.utils.markdown_parser import MarkdownParser
        parser = MarkdownParser(project_root)
        user_stories_data = parser.parse_user_stories()
        
        if 'error' in user_stories_data:
            return jsonify(user_stories_data), 404
        
        return jsonify(user_stories_data)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/modules/config')
def api_modules_config():
    """API: Modul-Konfiguration"""
    return jsonify({
        'default_module': 'excel-analysis',
        'auto_refresh_interval': 30000,  # 30 Sekunden
        'features': {
            'sidebar_collapsible': True,
            'module_switching': True,
            'responsive_design': True
        },
        'theme': {
            'primary_color': '#0d6efd',
            'sidebar_width': '250px'
        }
    })


if __name__ == '__main__':
    # Datenbank initialisieren
    create_tables()
    
    print("🚀 STWEG Web-Interface startet...")
    print(f"📁 Upload-Verzeichnis: {UPLOAD_FOLDER}")
    print(f"📁 Export-Verzeichnis: {EXPORT_FOLDER}")
    print("🌐 Dashboard: http://localhost:5000")
    print("📊 API-Status: http://localhost:5000/api/status")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
