/**
 * STWEG Dashboard JavaScript
 * Interaktive Funktionalität für das Dashboard
 */

// Globale Variablen
let refreshInterval;
let testRunning = false;
let currentModule = 'excel-analysis'; // Standard-Modul

// Initialisierung beim Laden der Seite
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 STWEG Dashboard initialisiert');
    
    // Modul-System initialisieren
    initializeModuleSystem();
    
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
 * Modul-System initialisieren
 */
function initializeModuleSystem() {
    console.log('🔧 Initialisiere Modul-System...');
    
    // Modul-Links mit Event-Listeners versehen
    const moduleLinks = document.querySelectorAll('.module-link');
    console.log(`📋 Gefundene Modul-Links: ${moduleLinks.length}`);
    
    moduleLinks.forEach((link, index) => {
        const moduleName = link.getAttribute('data-module');
        console.log(`🔗 Link ${index + 1}: ${moduleName}`);
        
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const module = this.getAttribute('data-module');
            console.log(`🖱️ Klick auf Modul: ${module}`);
            if (module) {
                switchModule(module);
            }
        });
    });
    
    // Standard-Modul aktivieren
    switchModule(currentModule);
    
    console.log('✅ Modul-System initialisiert');
}

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

// Globale Variable für aktuell hochgeladene Datei
let currentUploadedFile = null;

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
            // Aktuell hochgeladene Datei speichern
            currentUploadedFile = data.filename;
            console.log('📁 Aktuell hochgeladene Datei:', currentUploadedFile);
            
            // Direkt erkunden nach Upload
            await exploreUploadedFile(currentUploadedFile);
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
 * Excel-Datei erkunden (ohne erneuten Upload)
 */
async function exploreCurrentFile() {
    console.log('🔍 exploreCurrentFile() aufgerufen');
    
    if (!currentUploadedFile) {
        console.log('❌ Keine Datei hochgeladen');
        alert('Bitte laden Sie zuerst eine Excel-Datei hoch!');
        return;
    }
    
    console.log('📁 Verwende bereits hochgeladene Datei:', currentUploadedFile);
    await exploreUploadedFile(currentUploadedFile);
}

/**
 * Hochgeladene Excel-Datei erkunden (ohne erneuten Upload)
 */
async function exploreUploadedFile(filename) {
    console.log('🔍 exploreUploadedFile() aufgerufen für:', filename);
    
    const analysisDiv = document.getElementById('excel-analysis');
    const analysisContent = document.getElementById('analysis-content');
    
    // Loading-State
    analysisContent.innerHTML = `
        <div class="text-center">
            <div class="spinner-border spinner-border-sm text-primary" role="status">
                <span class="visually-hidden">Erkunde...</span>
            </div>
            <span class="ms-2">Erkunde Excel-Datei...</span>
        </div>
    `;
    analysisDiv.style.display = 'block';
    
    try {
        console.log('🚀 Starte Excel-Erkundung für:', filename);
        
        // Datei erkunden (OHNE erneuten Upload!)
        const exploreResponse = await fetch(`/api/excel/explore/${filename}`);
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
        analysisContent.innerHTML = `
            <div class="alert alert-danger">
                <strong>Fehler bei der Excel-Erkundung:</strong> ${error.message}
            </div>
        `;
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

/**
 * Modul wechseln
 */
function switchModule(moduleName) {
    console.log(`🔄 Wechsle zu Modul: ${moduleName}`);
    
    // Aktuelles Modul verstecken
    const currentModuleElement = document.getElementById(`${currentModule}-module`);
    if (currentModuleElement) {
        currentModuleElement.style.display = 'none';
        console.log(`✅ Aktuelles Modul versteckt: ${currentModule}`);
    } else {
        console.log(`❌ Aktuelles Modul nicht gefunden: ${currentModule}`);
    }
    
    // Neues Modul anzeigen
    const newModuleElement = document.getElementById(`${moduleName}-module`);
    if (newModuleElement) {
        newModuleElement.style.display = 'block';
        console.log(`✅ Neues Modul angezeigt: ${moduleName}`);
    } else {
        console.log(`❌ Neues Modul nicht gefunden: ${moduleName}`);
    }
    
    // Sidebar-Links aktualisieren
    const moduleLinks = document.querySelectorAll('.module-link');
    moduleLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-module') === moduleName) {
            link.classList.add('active');
        }
    });
    
    // Modul-Titel aktualisieren
    const moduleTitle = document.getElementById('module-title');
    if (moduleTitle) {
        const titles = {
            'excel-analysis': 'Excel-Analyse & Kostenaufteilung',
            'development': 'Development & Monitoring',
            'pdf-billing': 'PDF-Rechnungen & Billing',
            'eigentuemer-management': 'Eigentümer-Management'
        };
        moduleTitle.textContent = titles[moduleName] || moduleName;
    }
    
    // Current module aktualisieren
    currentModule = moduleName;
    
    // Modul-spezifische Daten laden
    loadModuleData(moduleName);
    
    console.log(`✅ Modul gewechselt zu: ${moduleName}`);
}

/**
 * Modul-spezifische Daten laden
 */
async function loadModuleData(moduleName) {
    console.log(`📊 Lade Daten für Modul: ${moduleName}`);
    
    switch (moduleName) {
        case 'excel-analysis':
            // Excel-Analyse-spezifische Daten laden
            await loadExcelModuleData();
            break;
        case 'development':
            // Development-spezifische Daten laden
            await loadDevelopmentModuleData();
            break;
        case 'pdf-billing':
            // PDF-Billing-spezifische Daten laden
            await loadPDFBillingModuleData();
            break;
        case 'eigentuemer-management':
            // Eigentümer-Management-spezifische Daten laden
            await loadEigentuemerManagementModuleData();
            break;
    }
}

/**
 * Excel-Modul-Daten laden
 */
async function loadExcelModuleData() {
    console.log('📊 Lade Excel-Modul-Daten...');
    
    try {
        const response = await fetch('/api/modules/excel');
        if (response.ok) {
            const data = await response.json();
            updateExcelModuleData(data);
            
            // Aktuell hochgeladene Datei setzen (falls vorhanden)
            if (data.last_filename && !currentUploadedFile) {
                currentUploadedFile = data.last_filename;
                console.log('📁 Aktuell hochgeladene Datei aus API gesetzt:', currentUploadedFile);
            }
        }
    } catch (error) {
        console.log('ℹ️ Excel-Modul-API noch nicht implementiert');
    }
}

/**
 * Development-Modul-Daten laden
 */
async function loadDevelopmentModuleData() {
    console.log('🔧 Lade Development-Modul-Daten...');
    
    try {
        // Vollständige Roadmap laden und anzeigen
        const roadmapResponse = await fetch('/api/roadmap/full');
        if (roadmapResponse.ok) {
            const roadmapData = await roadmapResponse.json();
            createSimpleRoadmapView(roadmapData);
        }
        
        // Vollständige User Stories laden und anzeigen
        const userStoriesResponse = await fetch('/api/user-stories/full');
        if (userStoriesResponse.ok) {
            const userStoriesData = await userStoriesResponse.json();
            createSimpleUserStoriesView(userStoriesData);
        }
        
        // Test-Status für Development-Modul aktualisieren
        updateDevelopmentTestStatus();
        
    } catch (error) {
        console.log('ℹ️ Development-Modul-APIs noch nicht vollständig implementiert');
    }
}

/**
 * Excel-Modul-Daten aktualisieren
 */
function updateExcelModuleData(data) {
    // Excel-spezifische UI-Elemente aktualisieren
    if (data.excel_files_count) {
        updateElement('excel-files-count', data.excel_files_count);
    }
    if (data.last_upload) {
        updateElement('last-upload', data.last_upload);
    }
}

/**
 * Development-Test-Status aktualisieren
 */
function updateDevelopmentTestStatus() {
    // Test-Status für Development-Modul aktualisieren
    const testsPassed = document.getElementById('tests-passed');
    const testsFailed = document.getElementById('tests-failed');
    
    if (testsPassed && testsFailed) {
        const passed = testsPassed.textContent;
        const failed = testsFailed.textContent;
        
        updateElement('tests-passed-dev', passed);
        updateElement('tests-failed-dev', failed);
    }
}

/**
 * Roadmap-Inhalt aktualisieren
 */
function updateRoadmapContent(data) {
    const roadmapContent = document.getElementById('roadmap-content');
    if (roadmapContent && data) {
        // Vereinfachte Roadmap-Anzeige
        let html = '<div class="roadmap-summary">';
        
        if (data.current_phase) {
            html += `
                <div class="alert alert-primary">
                    <h6><i class="fas fa-flag"></i> Aktuelle Phase</h6>
                    <strong>${data.current_phase}</strong>
                </div>
            `;
        }
        
        if (data.next_steps && data.next_steps.length > 0) {
            html += '<h6><i class="fas fa-list"></i> Nächste Schritte:</h6><ul>';
            data.next_steps.forEach(step => {
                html += `<li>${step}</li>`;
            });
            html += '</ul>';
        }
        
        html += '</div>';
        roadmapContent.innerHTML = html;
    }
}

/**
 * User Stories-Inhalt aktualisieren
 */
function updateUserStoriesContent(data) {
    const userStoriesContent = document.getElementById('user-stories-content');
    if (userStoriesContent && data) {
        // Vereinfachte User Stories-Anzeige
        let html = '<div class="user-stories-summary">';
        
        if (data.completed && data.total) {
            html += `
                <div class="alert alert-success">
                    <h6><i class="fas fa-check-circle"></i> Fortschritt</h6>
                    <strong>${data.completed}/${data.total}</strong> User Stories abgeschlossen
                </div>
            `;
            
            // Update counters
            updateElement('user-stories-completed', data.completed);
            updateElement('user-stories-total', data.total);
        }
        
        if (data.recent_stories && data.recent_stories.length > 0) {
            html += '<h6><i class="fas fa-clock"></i> Aktuelle Stories:</h6><ul>';
            data.recent_stories.forEach(story => {
                html += `<li>${story}</li>`;
            });
            html += '</ul>';
        }
        
        html += '</div>';
        userStoriesContent.innerHTML = html;
    }
}

/**
 * Priorisiertes Backlog anzeigen (ersetzt die alte Roadmap-Ansicht)
 */
function createSimpleRoadmapView(data) {
    const content = document.getElementById('roadmap-content');
    
    if (!data || data.error) {
        content.innerHTML = '<p class="text-danger">Fehler beim Laden der Backlog-Daten</p>';
        return;
    }
    
    let html = `
        <div class="row text-center mb-3">
            <div class="col-4">
                <div class="card bg-light">
                    <div class="card-body p-2">
                        <h5 class="text-primary">${data.total_stories || 0}</h5>
                        <small class="text-muted">User Stories</small>
                    </div>
                </div>
            </div>
            <div class="col-4">
                <div class="card bg-light">
                    <div class="card-body p-2">
                        <h5 class="text-success">${data.completed_stories || 0}</h5>
                        <small class="text-muted">Abgeschlossen</small>
                    </div>
                </div>
            </div>
            <div class="col-4">
                <div class="card bg-light">
                    <div class="card-body p-2">
                        <h5 class="text-info">${data.progress_percentage || 0}%</h5>
                        <small class="text-muted">Fortschritt</small>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="progress mb-3" style="height: 20px;">
            <div class="progress-bar bg-success" role="progressbar" style="width: ${data.progress_percentage || 0}%">
                ${data.progress_percentage || 0}%
            </div>
        </div>
    `;
    
    // Priorisiertes Backlog anzeigen
    html += '<h6 class="mb-3"><i class="fas fa-list-ol text-primary"></i> Priorisiertes Backlog:</h6>';
    
    if (data.priorities && data.priorities.length > 0) {
        data.priorities.forEach(priority => {
            if (!priority.stories || priority.stories.length === 0) return;
            
            const priorityColors = {
                'kritisch': 'danger',
                'hoch': 'warning', 
                'mittel': 'info',
                'niedrig': 'secondary',
                'abgeschlossen': 'success'
            };
            
            const priorityIcons = {
                'kritisch': 'fas fa-exclamation-triangle',
                'hoch': 'fas fa-arrow-up',
                'mittel': 'fas fa-minus',
                'niedrig': 'fas fa-arrow-down',
                'abgeschlossen': 'fas fa-check-circle'
            };
            
            html += `
                <div class="card mb-4">
                    <div class="card-header bg-${priorityColors[priority.name]} text-white">
                        <h6 class="mb-0">
                            <i class="${priorityIcons[priority.name]}"></i> 
                            Priorität ${priority.name.charAt(0).toUpperCase() + priority.name.slice(1)}
                            <span class="badge bg-light text-dark ms-2">${priority.stories.length} Stories</span>
                        </h6>
                    </div>
                    <div class="card-body p-0">
            `;
            
            priority.stories.forEach(story => {
                const statusClass = story.status === 'completed' ? 'success' : 
                                  story.status === 'in-progress' ? 'warning' : 'secondary';
                const statusText = story.status === 'completed' ? 'Abgeschlossen' : 
                                 story.status === 'in-progress' ? 'In Bearbeitung' : 'Geplant';
                
                html += `
                    <div class="border-bottom p-3">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <div class="flex-grow-1">
                                <h6 class="mb-2">
                                    <i class="fas fa-clipboard-list text-info"></i> 
                                    ${story.title}
                                </h6>
                                <div class="text-muted mb-2">
                                    <strong>Als</strong> ${story.as}<br>
                                    <strong>möchte ich</strong> ${story.want}<br>
                                    <strong>damit</strong> ${story.so_that}
                                </div>
                                <small class="text-info">
                                    <i class="fas fa-layer-group"></i> ${story.epic}
                                </small>
                            </div>
                            <div class="ms-3 text-end">
                                <span class="badge bg-${statusClass} mb-1">${statusText}</span><br>
                                <small class="text-muted">${story.priority}</small>
                            </div>
                        </div>
                        
                        ${story.acceptance_criteria && story.acceptance_criteria.length > 0 ? `
                            <div class="mt-3">
                                <h6 class="text-muted mb-2">Akzeptanzkriterien:</h6>
                                <ul class="list-unstyled mb-0">
                                    ${story.acceptance_criteria.map(criteria => 
                                        `<li><i class="fas fa-check text-success me-2"></i>${criteria}</li>`
                                    ).join('')}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                `;
            });
            
            html += '</div></div>';
        });
    }
    
    content.innerHTML = html;
}

/**
 * Verbesserte User Stories-Ansicht mit vollständigem Text und priorisiertem Backlog
 */
function createSimpleUserStoriesView(data) {
    const content = document.getElementById('user-stories-content');
    
    if (!data || data.error) {
        content.innerHTML = '<p class="text-danger">Fehler beim Laden der User Stories-Daten</p>';
        return;
    }
    
    // Layout: Links Backlog, rechts Epics/Stories
    let html = `
        <div class="row">
            <!-- Links: Priorisiertes Backlog -->
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h6 class="mb-0"><i class="fas fa-list-ol"></i> Priorisiertes Backlog</h6>
                    </div>
                    <div class="card-body p-0" style="max-height: 600px; overflow-y: auto;">
    `;
    
    // Backlog-Daten aus Roadmap laden
    if (data.backlog && data.backlog.priorities) {
        Object.entries(data.backlog.priorities).forEach(([priority, stories]) => {
            if (stories.length === 0) return;
            
            const priorityColors = {
                'kritisch': 'danger',
                'hoch': 'warning', 
                'mittel': 'info',
                'niedrig': 'secondary'
            };
            
            const priorityIcons = {
                'kritisch': 'fas fa-exclamation-triangle',
                'hoch': 'fas fa-arrow-up',
                'mittel': 'fas fa-minus',
                'niedrig': 'fas fa-arrow-down'
            };
            
            html += `
                <div class="border-bottom">
                    <div class="p-3 bg-light">
                        <h6 class="mb-2 text-${priorityColors[priority]}">
                            <i class="${priorityIcons[priority]}"></i> 
                            Priorität ${priority.charAt(0).toUpperCase() + priority.slice(1)}
                            <span class="badge bg-${priorityColors[priority]} ms-2">${stories.length}</span>
                        </h6>
                    </div>
                    <div class="p-2">
            `;
            
            stories.forEach(story => {
                html += `
                    <div class="d-flex align-items-center p-2 border-bottom">
                        <div class="flex-grow-1">
                            <strong class="text-primary">${story.id}</strong>
                            <div class="text-muted small">${story.title}</div>
                            <small class="text-info">${story.epic}</small>
                        </div>
                        <div class="ms-2">
                            <span class="badge bg-secondary">${story.status}</span>
                        </div>
                    </div>
                `;
            });
            
            html += '</div></div>';
        });
    }
    
    html += `
                    </div>
                </div>
            </div>
            
            <!-- Rechts: Epics & Stories -->
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h6 class="mb-0"><i class="fas fa-layer-group"></i> Epics & User Stories</h6>
                    </div>
                    <div class="card-body p-0" style="max-height: 600px; overflow-y: auto;">
    `;
    
    // Epics anzeigen
    if (data.epics && data.epics.length > 0) {
        data.epics.forEach(epic => {
            html += `
                <div class="border-bottom">
                    <div class="p-3 bg-light">
                        <h6 class="mb-2 text-success">
                            <i class="fas fa-layer-group"></i> ${epic.title}
                            <span class="badge bg-success ms-2">${epic.stories ? epic.stories.length : 0} Stories</span>
                        </h6>
                    </div>
                    <div class="p-2">
            `;
            
            if (epic.stories && epic.stories.length > 0) {
                epic.stories.forEach(story => {
                    const statusClass = story.status === 'completed' ? 'success' : 
                                      story.status === 'in-progress' ? 'warning' : 'secondary';
                    const statusText = story.status === 'completed' ? 'Abgeschlossen' : 
                                     story.status === 'in-progress' ? 'In Bearbeitung' : 'Geplant';
                    
                    html += `
                        <div class="p-3 border-bottom">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div class="flex-grow-1">
                                    <h6 class="mb-2 text-primary">
                                        <i class="fas fa-clipboard-list"></i> ${story.id}: ${story.title}
                                    </h6>
                                    <div class="user-story-text text-muted small mb-2">
                                        <strong>Als</strong> ${story.as || 'Administrator'}<br>
                                        <strong>möchte ich</strong> ${story.want || story.description || 'Funktionalität'}<br>
                                        <strong>damit</strong> ${story.so_that || 'der Workflow verbessert wird'}
                                    </div>
                                </div>
                                <div class="ms-3 text-end">
                                    <span class="badge bg-${statusClass} mb-1">${statusText}</span>
                                </div>
                            </div>
                            
                            ${story.acceptance_criteria && story.acceptance_criteria.length > 0 ? `
                                <div class="mt-2">
                                    <h6 class="text-muted small mb-2">Akzeptanzkriterien:</h6>
                                    <ul class="list-unstyled mb-0 small">
                                        ${story.acceptance_criteria.map(criteria => 
                                            `<li><i class="fas fa-check text-success me-2"></i>${criteria}</li>`
                                        ).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                        </div>
                    `;
                });
            }
            
            html += '</div></div>';
        });
    }
    
    html += `
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Zusammenfassung unten -->
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <div class="row text-center">
                            <div class="col-3">
                                <div class="card bg-light">
                                    <div class="card-body p-2">
                                        <h5 class="text-primary">${data.total_epics || 0}</h5>
                                        <small class="text-muted">Epics</small>
                                    </div>
                                </div>
                            </div>
                            <div class="col-3">
                                <div class="card bg-light">
                                    <div class="card-body p-2">
                                        <h5 class="text-success">${data.completed_stories || 0}</h5>
                                        <small class="text-muted">Abgeschlossen</small>
                                    </div>
                                </div>
                            </div>
                            <div class="col-3">
                                <div class="card bg-light">
                                    <div class="card-body p-2">
                                        <h5 class="text-info">${data.total_stories || 0}</h5>
                                        <small class="text-muted">Gesamt</small>
                                    </div>
                                </div>
                            </div>
                            <div class="col-3">
                                <div class="card bg-light">
                                    <div class="card-body p-2">
                                        <h5 class="text-warning">${data.progress_percentage || 0}%</h5>
                                        <small class="text-muted">Fortschritt</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    content.innerHTML = html;
}

/**
 * PDF-Billing-Modul-Daten laden
 */
async function loadPDFBillingModuleData() {
    console.log('📄 Lade PDF-Billing-Modul-Daten...');
    
    try {
        // PDF-Statistiken laden (falls verfügbar)
        const invoicesResponse = await fetch('/api/billing/status');
        if (invoicesResponse.ok) {
            const invoicesData = await invoicesResponse.json();
            updatePDFBillingModuleData(invoicesData);
        }
        
    } catch (error) {
        console.log('ℹ️ PDF-Billing-Modul-APIs noch nicht vollständig implementiert');
    }
}

/**
 * PDF-Billing-Modul-Daten aktualisieren
 */
function updatePDFBillingModuleData(data) {
    // PDF-spezifische UI-Elemente aktualisieren
    if (data.invoices_count !== undefined) {
        document.getElementById('pdf-invoices-count').textContent = data.invoices_count;
    }
    if (data.last_invoice) {
        document.getElementById('last-invoice').textContent = data.last_invoice;
    }
}

/**
 * Beispiel-Rechnung generieren
 */
async function generateSampleInvoice() {
    console.log('📄 Generiere Beispiel-Rechnung...');
    
    const resultDiv = document.getElementById('pdf-generation-result');
    const resultText = document.getElementById('pdf-result-text');
    const downloadBtn = document.getElementById('download-pdf-btn');
    
    // Loading-State
    resultText.innerHTML = `
        <div class="text-center">
            <div class="spinner-border spinner-border-sm text-primary" role="status">
                <span class="visually-hidden">Generiere PDF...</span>
            </div>
            <span class="ms-2">Generiere PDF-Rechnung...</span>
        </div>
    `;
    resultDiv.style.display = 'block';
    downloadBtn.style.display = 'none';
    
    try {
        const response = await fetch('/api/billing/generate-sample', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultText.innerHTML = `
                <strong>PDF erfolgreich generiert!</strong><br>
                <small class="text-muted">Datei: ${data.filename}</small>
            `;
            
            // Download-Button konfigurieren
            downloadBtn.onclick = () => {
                window.open(data.download_url, '_blank');
            };
            downloadBtn.style.display = 'inline-block';
            
            // Modul-Daten aktualisieren
            setTimeout(() => {
                loadPDFBillingModuleData();
            }, 1000);
            
        } else {
            resultText.innerHTML = `
                <div class="text-danger">
                    <strong>Fehler:</strong> ${data.error}
                </div>
            `;
        }
    } catch (error) {
        resultText.innerHTML = `
            <div class="text-danger">
                <strong>Netzwerk-Fehler:</strong> ${error.message}
            </div>
        `;
    }
}

/**
 * Rechnungsvorlage anzeigen
 */
function showInvoicePreview() {
    console.log('👁️ Zeige Rechnungsvorlage...');
    
    // Öffne die Original-Vorlage in einem neuen Tab
    const templateUrl = '/data/sample/Rechnung.pdf';
    window.open(templateUrl, '_blank');
}

/**
 * Eigentümer-Management-Modul-Daten laden
 */
async function loadEigentuemerManagementModuleData() {
    console.log('👥 Lade Eigentümer-Management-Modul-Daten...');
    
    try {
        // Eigentümer-Daten laden
        await loadEigentuemerList();
        
    } catch (error) {
        console.log('ℹ️ Eigentümer-Management-Modul-APIs noch nicht vollständig implementiert');
    }
}

/**
 * Eigentümer-Liste laden
 */
async function loadEigentuemerList() {
    const loadingDiv = document.getElementById('eigentuemer-loading');
    const listDiv = document.getElementById('eigentuemer-list');
    
    // Loading-State anzeigen
    loadingDiv.style.display = 'block';
    listDiv.innerHTML = '';
    
    try {
        const response = await fetch('/api/eigentuemer');
        const data = await response.json();
        
        if (response.ok) {
            // Status-Cards aktualisieren
            updateEigentuemerStatusCards(data);
            
            // Eigentümer-Liste anzeigen
            displayEigentuemerList(data.eigentuemer);
            
        } else {
            listDiv.innerHTML = `
                <div class="alert alert-danger">
                    <strong>Fehler:</strong> ${data.error}
                </div>
            `;
        }
    } catch (error) {
        listDiv.innerHTML = `
            <div class="alert alert-danger">
                <strong>Netzwerk-Fehler:</strong> ${error.message}
            </div>
        `;
    } finally {
        loadingDiv.style.display = 'none';
    }
}

/**
 * Eigentümer-Status-Cards aktualisieren
 */
function updateEigentuemerStatusCards(data) {
    document.getElementById('eigentuemer-total-count').textContent = data.total_count || 0;
    document.getElementById('eigentuemer-active-count').textContent = `${data.active_count || 0} aktiv`;
    
    // Anteil-Summe berechnen
    const anteilSum = data.eigentuemer.reduce((sum, eig) => sum + (eig.anteil || 0), 0);
    document.getElementById('anteile-sum').textContent = `${Math.round(anteilSum * 100)}%`;
    
    // Messpunkte zählen
    const messpunkteTotal = data.eigentuemer.reduce((sum, eig) => sum + (eig.messpunkte_count || 0), 0);
    document.getElementById('messpunkte-total').textContent = messpunkteTotal;
}

/**
 * Eigentümer-Liste anzeigen
 */
function displayEigentuemerList(eigentuemer) {
    const listDiv = document.getElementById('eigentuemer-list');
    
    if (!eigentuemer || eigentuemer.length === 0) {
        listDiv.innerHTML = `
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                Keine Eigentümer gefunden. 
                <button type="button" class="btn btn-sm btn-success ms-2" onclick="showCreateEigentuemerModal()">
                    <i class="fas fa-plus"></i> Ersten Eigentümer erstellen
                </button>
            </div>
        `;
        return;
    }
    
    let html = `
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Wohnung</th>
                    <th>Anteil</th>
                    <th>Kontakt</th>
                    <th>Status</th>
                    <th>Messpunkte</th>
                    <th>Aktionen</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    eigentuemer.forEach(eig => {
        const statusBadge = eig.aktiv ? 
            '<span class="badge bg-success">Aktiv</span>' : 
            '<span class="badge bg-secondary">Inaktiv</span>';
        
        const kontakt = [];
        if (eig.email) kontakt.push(`<i class="fas fa-envelope"></i> ${eig.email}`);
        if (eig.telefon) kontakt.push(`<i class="fas fa-phone"></i> ${eig.telefon}`);
        const kontaktHtml = kontakt.length > 0 ? kontakt.join('<br>') : '<span class="text-muted">-</span>';
        
        html += `
            <tr class="${eig.aktiv ? '' : 'table-secondary'}">
                <td>
                    <strong>${eig.name}</strong>
                </td>
                <td>
                    <span class="badge bg-info">${eig.wohnung}</span>
                </td>
                <td>
                    ${eig.anteil_prozent}%
                    <small class="text-muted">(${eig.anteil})</small>
                </td>
                <td>
                    ${kontaktHtml}
                </td>
                <td>
                    ${statusBadge}
                </td>
                <td>
                    <span class="badge bg-primary">${eig.messpunkte_count}</span>
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button type="button" class="btn btn-outline-primary" onclick="editEigentuemer(${eig.id})" title="Bearbeiten">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button type="button" class="btn btn-outline-${eig.aktiv ? 'warning' : 'success'}" 
                                onclick="toggleEigentuemerStatus(${eig.id}, ${!eig.aktiv})" 
                                title="${eig.aktiv ? 'Deaktivieren' : 'Aktivieren'}">
                            <i class="fas fa-${eig.aktiv ? 'pause' : 'play'}"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    });
    
    html += `
            </tbody>
        </table>
    `;
    
    listDiv.innerHTML = html;
}

/**
 * Eigentümer bearbeiten
 */
async function editEigentuemer(eigentuemerId) {
    try {
        console.log(`✏️ Bearbeite Eigentümer: ${eigentuemerId}`);
        
        // Eigentümer-Daten laden
        const response = await fetch(`/api/eigentuemer/${eigentuemerId}`);
        if (!response.ok) {
            throw new Error(`Fehler beim Laden: ${response.statusText}`);
        }
        
        const data = await response.json();
        const eigentuemer = data.eigentuemer;
        
        // Edit-Modal anzeigen
        showEditEigentuemerModal(eigentuemer);
        
    } catch (error) {
        console.error('Edit-Fehler:', error);
        showToast(`Fehler beim Laden der Eigentümer-Daten: ${error.message}`, 'error');
    }
}

/**
 * Edit-Eigentümer-Modal anzeigen
 */
function showEditEigentuemerModal(eigentuemer) {
    // Modal-HTML erstellen
    const modalHtml = `
        <div class="modal fade" id="editEigentuemerModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-edit text-primary"></i> Eigentümer bearbeiten
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="editEigentuemerForm">
                            <div class="mb-3">
                                <label for="editName" class="form-label">Name *</label>
                                <input type="text" class="form-control" id="editName" value="${eigentuemer.name}" required>
                            </div>
                            <div class="mb-3">
                                <label for="editWohnung" class="form-label">Wohnung *</label>
                                <input type="text" class="form-control" id="editWohnung" value="${eigentuemer.wohnung}" required>
                            </div>
                            <div class="mb-3">
                                <label for="editAnteil" class="form-label">Anteil (0.0 - 1.0) *</label>
                                <input type="number" class="form-control" id="editAnteil" 
                                       value="${eigentuemer.anteil}" min="0" max="1" step="0.001" required>
                                <div class="form-text">Aktuell: ${eigentuemer.anteil_prozent}%</div>
                            </div>
                            <div class="mb-3">
                                <label for="editEmail" class="form-label">E-Mail</label>
                                <input type="email" class="form-control" id="editEmail" value="${eigentuemer.email || ''}">
                            </div>
                            <div class="mb-3">
                                <label for="editTelefon" class="form-label">Telefon</label>
                                <input type="tel" class="form-control" id="editTelefon" value="${eigentuemer.telefon || ''}">
                            </div>
                            <div class="mb-3">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="editAktiv" ${eigentuemer.aktiv ? 'checked' : ''}>
                                    <label class="form-check-label" for="editAktiv">
                                        Aktiv
                                    </label>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Abbrechen</button>
                        <button type="button" class="btn btn-primary" onclick="updateEigentuemer(${eigentuemer.id})">
                            <i class="fas fa-save"></i> Speichern
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Bestehendes Modal entfernen
    const existingModal = document.getElementById('editEigentuemerModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Neues Modal hinzufügen
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Modal anzeigen
    const modal = new bootstrap.Modal(document.getElementById('editEigentuemerModal'));
    modal.show();
}

/**
 * Eigentümer aktualisieren
 */
async function updateEigentuemer(eigentuemerId) {
    try {
        // Formular-Daten sammeln
        const formData = {
            name: document.getElementById('editName').value.trim(),
            wohnung: document.getElementById('editWohnung').value.trim(),
            anteil: parseFloat(document.getElementById('editAnteil').value),
            anteil_prozent: parseFloat(document.getElementById('editAnteil').value) * 100,
            email: document.getElementById('editEmail').value.trim() || null,
            telefon: document.getElementById('editTelefon').value.trim() || null,
            aktiv: document.getElementById('editAktiv').checked
        };
        
        // Validierung
        if (!formData.name || !formData.wohnung) {
            throw new Error('Name und Wohnung sind Pflichtfelder');
        }
        
        if (formData.anteil < 0 || formData.anteil > 1) {
            throw new Error('Anteil muss zwischen 0.0 und 1.0 liegen');
        }
        
        console.log('📝 Aktualisiere Eigentümer:', formData);
        
        // API-Aufruf
        const response = await fetch(`/api/eigentuemer/${eigentuemerId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Fehler: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        // Modal schließen
        const modal = bootstrap.Modal.getInstance(document.getElementById('editEigentuemerModal'));
        modal.hide();
        
        // Erfolg-Meldung
        showToast(`Eigentümer "${formData.name}" erfolgreich aktualisiert!`, 'success');
        
        // Liste aktualisieren
        refreshEigentuemerList();
        
    } catch (error) {
        console.error('Update-Fehler:', error);
        showToast(`Fehler beim Aktualisieren: ${error.message}`, 'error');
    }
}

/**
 * Eigentümer-Status umschalten
 */
async function toggleEigentuemerStatus(eigentuemerId, newStatus) {
    console.log(`🔄 Ändere Status von Eigentümer ${eigentuemerId} zu: ${newStatus}`);
    
    try {
        const response = await fetch(`/api/eigentuemer/${eigentuemerId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                aktiv: newStatus
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message, 'success');
            // Liste aktualisieren
            await loadEigentuemerList();
        } else {
            showToast(`Fehler: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`Netzwerk-Fehler: ${error.message}`, 'error');
    }
}

/**
 * Eigentümer-Liste aktualisieren
 */
function refreshEigentuemerList() {
    console.log('🔄 Aktualisiere Eigentümer-Liste...');
    loadEigentuemerList();
}

/**
 * Eigentümer-Daten exportieren
 */
async function exportEigentuemerData(format = 'json') {
    try {
        console.log(`📥 Exportiere Eigentümer-Daten als ${format.toUpperCase()}...`);
        showToast('Export wird vorbereitet...', 'info');
        
        const response = await fetch(`/api/eigentuemer/export?format=${format}`);
        
        if (!response.ok) {
            throw new Error(`Export fehlgeschlagen: ${response.statusText}`);
        }
        
        if (format === 'json') {
            const data = await response.json();
            console.log('Export-Daten:', data);
            
            // JSON-Datei herunterladen
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `eigentuemer_export_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showToast(`Export erfolgreich: ${data.total_count} Eigentümer`, 'success');
        } else {
            // CSV/Excel-Datei herunterladen
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = response.headers.get('Content-Disposition')?.split('filename=')[1] || `eigentuemer_export.${format}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showToast(`Export erfolgreich: ${format.toUpperCase()}-Datei heruntergeladen`, 'success');
        }
        
    } catch (error) {
        console.error('Export-Fehler:', error);
        showToast(`Export fehlgeschlagen: ${error.message}`, 'error');
    }
}

/**
 * Eigentümer-Statistiken anzeigen
 */
function showEigentuemerStats() {
    console.log('📊 Zeige Eigentümer-Statistiken...');
    showToast('Statistik-Funktion wird implementiert...', 'info');
}

/**
 * Eigentümer-Erstellen Modal anzeigen
 */
function showCreateEigentuemerModal() {
    console.log('➕ Zeige Eigentümer-Erstellen Modal...');
    
    // Modal anzeigen
    const modal = new bootstrap.Modal(document.getElementById('createEigentuemerModal'));
    modal.show();
}

/**
 * Neuen Eigentümer erstellen
 */
async function createEigentuemer() {
    console.log('💾 Erstelle neuen Eigentümer...');
    
    // Formular-Daten sammeln
    const formData = {
        name: document.getElementById('create-name').value,
        wohnung: document.getElementById('create-wohnung').value,
        anteil: parseFloat(document.getElementById('create-anteil').value),
        email: document.getElementById('create-email').value || null,
        telefon: document.getElementById('create-telefon').value || null,
        aktiv: document.getElementById('create-aktiv').checked
    };
    
    // Validierung
    if (!formData.name || !formData.wohnung || formData.anteil === undefined) {
        showToast('Bitte füllen Sie alle Pflichtfelder aus.', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/eigentuemer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message, 'success');
            
            // Modal schließen
            const modal = bootstrap.Modal.getInstance(document.getElementById('createEigentuemerModal'));
            modal.hide();
            
            // Formular zurücksetzen
            document.getElementById('create-eigentuemer-form').reset();
            document.getElementById('create-aktiv').checked = true;
            
            // Liste aktualisieren
            await loadEigentuemerList();
            
        } else {
            showToast(`Fehler: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`Netzwerk-Fehler: ${error.message}`, 'error');
    }
}

/**
 * Hilfsfunktionen für Status
 */
function getPhaseStatusIcon(status) {
    switch (status) {
        case 'completed': return '✅';
        case 'current': return '🔄';
        case 'planned': return '📋';
        default: return '❓';
    }
}

function getPhaseStatusClass(status) {
    switch (status) {
        case 'completed': return 'bg-success';
        case 'current': return 'bg-primary';
        case 'planned': return 'bg-secondary';
        default: return 'bg-light text-dark';
    }
}

/**
 * Sidebar ein-/ausblenden
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}

// Globale Funktionen für HTML-Buttons
window.runTests = runTests;
window.createSampleData = createSampleData;
window.clearDatabase = clearDatabase;
window.switchModule = switchModule;
window.toggleSidebar = toggleSidebar;
