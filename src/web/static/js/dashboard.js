/**
 * STWEG Dashboard JavaScript
 * Interaktive Funktionalität für das Dashboard
 */

// Globale Variablen
let refreshInterval;
let testRunning = false;

// Initialisierung beim Laden der Seite
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 STWEG Dashboard initialisiert');
    
    // Initiale Daten laden
    loadProjectStatus();
    loadTestStatus();
    
    // Auto-Refresh alle 30 Sekunden
    refreshInterval = setInterval(() => {
        loadProjectStatus();
        if (!testRunning) {
            loadTestStatus();
        }
    }, 30000);
    
    // Event Listeners
    setupEventListeners();
    
    // Debug: Button-Event-Listener testen
    const testButton = document.querySelector('button[onclick="runTests()"]');
    if (testButton) {
        console.log('✅ Test-Button gefunden:', testButton);
    } else {
        console.log('❌ Test-Button nicht gefunden');
    }
});

/**
 * Event Listeners einrichten
 */
function setupEventListeners() {
    // Excel Upload Form
    const excelForm = document.getElementById('excel-upload-form');
    if (excelForm) {
        excelForm.addEventListener('submit', handleExcelUpload);
    }
}

/**
 * Projekt-Status laden
 */
async function loadProjectStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (response.ok) {
            updateProjectStatus(data);
        } else {
            console.error('Fehler beim Laden des Projekt-Status:', data.error);
        }
    } catch (error) {
        console.error('Netzwerk-Fehler beim Laden des Status:', error);
    }
}

/**
 * Projekt-Status im UI aktualisieren
 */
function updateProjectStatus(data) {
    // Projekt-Phase
    const projectPhase = document.getElementById('project-phase');
    const projectStatus = document.getElementById('project-status');
    if (projectPhase && data.project_status) {
        projectPhase.textContent = data.project_status.phase;
        projectStatus.textContent = data.project_status.status;
    }
    
    // Datenbank-Statistiken
    if (data.database) {
        updateElement('eigentuemer-count', data.database.eigentuemer_count);
        updateElement('active-eigentuemer', `${data.database.active_eigentuemer} aktiv`);
        updateElement('messpunkte-count', data.database.messpunkte_count);
        updateElement('verbrauchsdaten-count', `${data.database.verbrauchsdaten_count} Verbrauchsdaten`);
        updateElement('rechnungen-count', data.database.rechnungen_count);
    }
    
    // Progress Bar
    if (data.project_status && data.project_status.progress) {
        const progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            progressBar.style.width = `${data.project_status.progress}%`;
            progressBar.textContent = `${data.project_status.progress}%`;
        }
    }
}

/**
 * Test-Status laden
 */
async function loadTestStatus() {
    try {
        const response = await fetch('/api/tests');
        const data = await response.json();
        
        if (response.ok) {
            updateTestStatus(data);
        } else {
            console.error('Fehler beim Laden der Tests:', data.error);
            showTestError(data.error);
        }
    } catch (error) {
        console.error('Netzwerk-Fehler beim Laden der Tests:', error);
        showTestError('Netzwerk-Fehler');
    }
}

/**
 * Test-Status im UI aktualisieren
 */
function updateTestStatus(data) {
    const testStatus = document.getElementById('test-status');
    const testResults = document.getElementById('test-results');
    
    if (data.success) {
        // Tests erfolgreich - Spinner verstecken, Ergebnisse anzeigen
        testStatus.style.display = 'none';  // Spinner verstecken
        testResults.style.display = 'block';
        
        if (data.summary) {
            updateElement('tests-passed', data.summary.passed || 0);
            updateElement('tests-failed', data.summary.failed || 0);
            updateElement('tests-total', data.summary.total || 0);
        }
        
        updateElement('test-timestamp', new Date(data.timestamp).toLocaleString('de-DE'));
        
        // Visual feedback
        const testStats = testResults.querySelectorAll('.test-stat');
        testStats.forEach(stat => stat.classList.add('fade-in'));
        
    } else {
        // Tests fehlgeschlagen
        showTestError(data.errors || 'Tests fehlgeschlagen');
    }
}

/**
 * Test-Fehler anzeigen
 */
function showTestError(error) {
    const testStatus = document.getElementById('test-status');
    testStatus.style.display = 'block';  // Element sichtbar machen
    testStatus.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle"></i>
            <strong>Test-Fehler:</strong> ${error}
        </div>
    `;
}

/**
 * Tests ausführen
 */
async function runTests() {
    console.log('🧪 runTests() aufgerufen');
    
    if (testRunning) {
        console.log('⚠️ Tests laufen bereits');
        return;
    }
    
    console.log('🚀 Starte Tests...');
    testRunning = true;
    const testStatus = document.getElementById('test-status');
    
    console.log('test-status element:', testStatus);
    if (!testStatus) {
        console.error('❌ test-status Element nicht gefunden!');
        return;
    }
    
    // Loading-State anzeigen
    testStatus.style.display = 'block';  // Element sichtbar machen
    testStatus.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Tests werden ausgeführt...</span>
            </div>
            <p class="mt-2">Tests werden ausgeführt...</p>
        </div>
    `;
    
    try {
        const response = await fetch('/api/tests');
        const data = await response.json();
        
        if (response.ok) {
            updateTestStatus(data);
        } else {
            showTestError(data.error);
        }
    } catch (error) {
        showTestError('Netzwerk-Fehler');
    } finally {
        testRunning = false;
    }
}

/**
 * Excel-Upload verarbeiten
 */
async function handleExcelUpload(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('excel-file');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Bitte wählen Sie eine Datei aus');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    const analysisDiv = document.getElementById('excel-analysis');
    const analysisContent = document.getElementById('analysis-content');
    
    // Loading-State
    analysisContent.innerHTML = `
        <div class="text-center">
            <div class="spinner-border spinner-border-sm text-primary" role="status">
                <span class="visually-hidden">Analysiere...</span>
            </div>
            <span class="ms-2">Analysiere Excel-Datei...</span>
        </div>
    `;
    analysisDiv.style.display = 'block';
    
    try {
        const response = await fetch('/api/excel/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayExcelAnalysis(data.analysis);
            fileInput.value = ''; // Reset file input
        } else {
            analysisContent.innerHTML = `
                <div class="alert alert-danger">
                    <strong>Fehler:</strong> ${data.error}
                </div>
            `;
        }
    } catch (error) {
        analysisContent.innerHTML = `
            <div class="alert alert-danger">
                <strong>Netzwerk-Fehler:</strong> ${error.message}
            </div>
        `;
    }
}

/**
 * Excel-Analyse anzeigen
 */
function displayExcelAnalysis(analysis) {
    const analysisContent = document.getElementById('analysis-content');
    
    let html = `
        <div class="alert alert-success">
            <strong>Analyse erfolgreich!</strong>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <h6>📊 Tabellenblätter:</h6>
                <ul>
                    ${analysis.sheets.map(sheet => `<li><code>${sheet}</code></li>`).join('')}
                </ul>
            </div>
            <div class="col-md-6">
                <h6>📋 Status:</h6>
                <span class="badge ${analysis.validation_status === 'valid' ? 'bg-success' : 'bg-warning'}">
                    ${analysis.validation_status}
                </span>
            </div>
        </div>
    `;
    
    // Spalten anzeigen
    if (analysis.columns) {
        html += '<h6>📝 Spalten pro Tabellenblatt:</h6>';
        for (const [sheetName, columns] of Object.entries(analysis.columns)) {
            html += `
                <div class="mb-2">
                    <strong>${sheetName}:</strong>
                    <div class="ms-3">
                        ${columns.map(col => `<code class="me-1">${col}</code>`).join('')}
                    </div>
                </div>
            `;
        }
    }
    
    // Validierungsfehler anzeigen
    if (analysis.validation_errors && analysis.validation_errors.length > 0) {
        html += `
            <div class="alert alert-warning mt-3">
                <h6>⚠️ Validierungsfehler:</h6>
                <ul class="mb-0">
                    ${analysis.validation_errors.map(error => `<li>${error}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    analysisContent.innerHTML = html;
}

/**
 * Beispieldaten erstellen
 */
async function createSampleData() {
    if (!confirm('Beispieldaten erstellen? Dies wird die Datenbank mit Test-Daten füllen.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/database/sample-data', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert(`Beispieldaten erfolgreich erstellt!\n\nEigentümer: ${data.created.eigentuemer}\nMesspunkte: ${data.created.messpunkte}\nVerbrauchsdaten: ${data.created.verbrauchsdaten}\nRechnungen: ${data.created.rechnungen}`);
            loadProjectStatus(); // Status aktualisieren
        } else {
            alert(`Fehler: ${data.error}`);
        }
    } catch (error) {
        alert(`Netzwerk-Fehler: ${error.message}`);
    }
}

/**
 * Datenbank leeren
 */
async function clearDatabase() {
    if (!confirm('Datenbank wirklich leeren? Alle Daten gehen verloren!')) {
        return;
    }
    
    try {
        const response = await fetch('/api/database/clear', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Datenbank erfolgreich geleert!');
            loadProjectStatus(); // Status aktualisieren
        } else {
            alert(`Fehler: ${data.error}`);
        }
    } catch (error) {
        alert(`Netzwerk-Fehler: ${error.message}`);
    }
}

/**
 * Excel-Datei erkunden
 */
async function exploreCurrentFile() {
    console.log('🔍 exploreCurrentFile() aufgerufen');
    
    const fileInput = document.getElementById('excel-file');
    const file = fileInput.files[0];
    
    console.log('📁 Datei-Input:', fileInput);
    console.log('📄 Ausgewählte Datei:', file);
    
    if (!file) {
        console.log('❌ Keine Datei ausgewählt');
        alert('Bitte wählen Sie zuerst eine Excel-Datei aus!');
        return;
    }
    
    try {
        console.log('🚀 Starte Excel-Erkundung...');
        
        // Datei hochladen
        const formData = new FormData();
        formData.append('file', file);
        
        console.log('📤 Lade Datei hoch...');
        const uploadResponse = await fetch('/api/excel/upload', {
            method: 'POST',
            body: formData
        });
        
        console.log('📥 Upload-Response:', uploadResponse.status);
        const uploadData = await uploadResponse.json();
        console.log('📊 Upload-Daten:', uploadData);
        
        if (!uploadResponse.ok) {
            throw new Error(uploadData.error);
        }
        
        // Datei erkunden
        console.log('🔍 Erkunde Datei...');
        const exploreResponse = await fetch(`/api/excel/explore/${uploadData.filename}`);
        console.log('📥 Explore-Response:', exploreResponse.status);
        
        const exploreData = await exploreResponse.json();
        console.log('📊 Explore-Daten:', exploreData);
        
        if (!exploreResponse.ok) {
            throw new Error(exploreData.error);
        }
        
        // Ergebnisse anzeigen
        console.log('🎨 Zeige Ergebnisse an...');
        displayExplorationResults(exploreData.result);
        
    } catch (error) {
        console.error('❌ Fehler bei der Excel-Erkundung:', error);
        alert(`Fehler bei der Excel-Erkundung: ${error.message}`);
    }
}

/**
 * Erkundungs-Ergebnisse anzeigen (ZEV-spezifisch)
 */
function displayExplorationResults(result) {
    const analysisDiv = document.getElementById('excel-analysis');
    const contentDiv = document.getElementById('analysis-content');
    
    // Status-Badge
    const statusBadge = result.structure_verified ? 
        '<span class="badge bg-success">✅ Struktur verifiziert</span>' : 
        '<span class="badge bg-danger">❌ Struktur-Probleme</span>';
    
    let html = `
        <div class="exploration-results">
            <h6 class="text-primary mb-3">
                <i class="fas fa-search"></i> 🔍 ZEV-Bilanz Analyse: ${result.file_name}
                ${statusBadge}
            </h6>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card border-info">
                        <div class="card-header bg-info text-white">
                            <h6 class="mb-0">📊 ZEV-Übersicht</h6>
                        </div>
                        <div class="card-body">
                            <p><strong>Gesamt Zähler:</strong> ${result.summary.total_zaehler}</p>
                            <p><strong>Hauptzähler:</strong> ${result.summary.hauptzaehler}</p>
                            <p><strong>Unterzähler:</strong> ${result.summary.unterzaehler}</p>
                            <p><strong>Virtuelle Zähler:</strong> ${result.summary.virtuelle_zaehler}</p>
                            <p><strong>Gesamt Messpunkte:</strong> ${result.summary.total_messpunkte}</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card border-success">
                        <div class="card-header bg-success text-white">
                            <h6 class="mb-0">📈 Struktur-Info</h6>
                        </div>
                        <div class="card-body">
    `;
    
    if (result.structure_info.errors && result.structure_info.errors.length > 0) {
        html += `
            <div class="alert alert-danger">
                <strong>Fehler:</strong>
                <ul class="mb-0">
        `;
        result.structure_info.errors.forEach(error => {
            html += `<li>${error}</li>`;
        });
        html += `</ul></div>`;
    }
    
    if (result.structure_info.warnings && result.structure_info.warnings.length > 0) {
        html += `
            <div class="alert alert-warning">
                <strong>Warnungen:</strong>
                <ul class="mb-0">
        `;
        result.structure_info.warnings.forEach(warning => {
            html += `<li>${warning}</li>`;
        });
        html += `</ul></div>`;
    }
    
    if (result.structure_info.month_columns && result.structure_info.month_columns.length > 0) {
        html += `<p><strong>Monatsdaten:</strong> ${result.structure_info.month_columns.length} Monate erkannt</p>`;
    }
    
    html += `
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-3">
                <h6 class="text-warning">📋 Zähler-Details:</h6>
    `;
    
    result.zaehler_overview.forEach((zaehler, index) => {
        // Badge-Farben für verschiedene Zähler-Typen
        let typeBadge, typeIcon;
        if (zaehler.type === 'hauptzaehler') {
            typeBadge = 'bg-primary';
            typeIcon = '⚡';
        } else if (zaehler.type === 'unterzaehler') {
            typeBadge = 'bg-warning';
            typeIcon = '🔌';
        } else if (zaehler.type === 'virtueller_zaehler') {
            typeBadge = 'bg-info';
            typeIcon = '🏠';
        } else if (zaehler.type === 'virtueller_unterzaehler') {
            typeBadge = 'bg-secondary';
            typeIcon = '🏡';
        } else {
            typeBadge = 'bg-light text-dark';
            typeIcon = '❓';
        }
        
                html += `
                    <div class="card mt-2">
                        <div class="card-header">
                            <h6 class="mb-0">
                                ${typeIcon} Zähler: ${zaehler.id}
                                <span class="badge ${typeBadge}">${zaehler.type}</span>
                            </h6>
                        </div>
                        <div class="card-body">
                            <p><strong>Code & Name:</strong> ${zaehler.code_und_name}</p>
                            <p><strong>Messpunkte:</strong> ${zaehler.messpunkte_count}</p>
                            ${zaehler.parent_id ? `<p><strong>Parent:</strong> <span class="badge bg-light text-dark">${zaehler.parent_id}</span></p>` : ''}
                `;
                
                // Messpunkt-Details anzeigen (falls vorhanden)
                if (zaehler.messpunkte_details && zaehler.messpunkte_details.length > 0) {
                    html += `
                        <div class="mt-3">
                            <h6 class="text-info">📊 Messpunkt-Details:</h6>
                    `;
                    
                    zaehler.messpunkte_details.forEach((mp, mpIdx) => {
                        html += `
                            <div class="border rounded p-2 mb-2">
                                <strong>${mp.name}</strong>
                        `;
                        
                        // Werte anzeigen
                        if (mp.values && Object.keys(mp.values).length > 0) {
                            html += `<div class="mt-1"><small class="text-muted">Monatswerte: `;
                            const valuePairs = Object.entries(mp.values);
                            
                            // Werte in einer übersichtlichen Tabelle anzeigen
                            if (valuePairs.length > 6) {
                                // Viele Werte: Als kompakte Liste
                                valuePairs.forEach(([month, val], valIdx) => {
                                    const badgeClass = val > 0 ? 'bg-success' : 'bg-light text-muted';
                                    html += `<span class="badge ${badgeClass} me-1 mb-1">${month}: ${val}</span>`;
                                });
                            } else {
                                // Wenige Werte: Als Tabelle
                                html += `<div class="table-responsive mt-2">`;
                                html += `<table class="table table-sm table-bordered">`;
                                html += `<thead><tr>`;
                                valuePairs.forEach(([month, val]) => {
                                    html += `<th class="text-center">${month}</th>`;
                                });
                                html += `</tr></thead><tbody><tr>`;
                                valuePairs.forEach(([month, val]) => {
                                    const cellClass = val > 0 ? 'table-success' : 'table-light';
                                    html += `<td class="text-center ${cellClass}"><strong>${val}</strong></td>`;
                                });
                                html += `</tr></tbody></table></div>`;
                            }
                            html += `</small></div>`;
                        } else {
                            html += `<div class="mt-1"><small class="text-muted">Keine Werte gefunden</small></div>`;
                        }
                        
                        html += `</div>`;
                    });
                    
                    html += `</div>`;
                } else {
                    // Fallback: Nur Namen anzeigen
                    html += `
                        <div class="mt-2">
                            <p><strong>Messpunkt-Namen:</strong></p>
                            <div class="row">
                    `;
                    
                    zaehler.messpunkte_names.forEach(mp => {
                        html += `
                            <div class="col-md-4 mb-1">
                                <span class="badge bg-light text-dark">${mp}</span>
                            </div>
                        `;
                    });
                    
                    if (zaehler.messpunkte_count > 3) {
                        html += `
                            <div class="col-md-4 mb-1">
                                <span class="badge bg-light text-muted">... und ${zaehler.messpunkte_count - 3} weitere</span>
                            </div>
                        `;
                    }
                    
                    html += `
                            </div>
                        </div>
                    `;
                }
                
                html += `
                        </div>
                    </div>
                `;
    });
    
    html += `
            </div>
        </div>
    `;
    
    contentDiv.innerHTML = html;
    analysisDiv.style.display = 'block';
}

/**
 * Hilfsfunktion: Element-Text aktualisieren
 */
function updateElement(id, text) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = text;
    }
}

/**
 * Hilfsfunktion: Toast-Benachrichtigung anzeigen
 */
function showToast(message, type = 'info') {
    // Einfache Toast-Implementierung
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <span>${message}</span>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove nach 5 Sekunden
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 5000);
}

// Globale Funktionen für HTML-Buttons
window.runTests = runTests;
window.createSampleData = createSampleData;
window.clearDatabase = clearDatabase;
