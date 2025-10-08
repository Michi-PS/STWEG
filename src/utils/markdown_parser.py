"""
Markdown-Parser für STWEG-Dokumentation
Parst ROADMAP.md und USER_STORIES.md in strukturierte Daten
"""

import re
from typing import Dict, List, Any
from pathlib import Path


class MarkdownParser:
    """Parser für Markdown-Dokumentation"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def parse_roadmap(self) -> Dict[str, Any]:
        """Parse ROADMAP.md als priorisiertes Backlog"""
        roadmap_file = self.project_root / 'ROADMAP.md'
        
        if not roadmap_file.exists():
            return {'error': 'ROADMAP.md nicht gefunden'}
        
        with open(roadmap_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Priorisierte User Stories extrahieren
        priorities = self._extract_priorities(content)
        
        # Status und Metriken extrahieren
        status = self._extract_backlog_status(content)
        
        return {
            'priorities': priorities,
            'status': status,
            'total_stories': status.get('total_stories', 0),
            'completed_stories': status.get('completed_stories', 0),
            'progress_percentage': status.get('progress_percentage', 0)
        }
    
    def parse_user_stories(self) -> Dict[str, Any]:
        """Parse USER_STORIES.md in strukturierte Daten"""
        user_stories_file = self.project_root / 'USER_STORIES.md'
        
        if not user_stories_file.exists():
            return {'error': 'USER_STORIES.md nicht gefunden'}
        
        with open(user_stories_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Epics extrahieren
        epics = self._extract_epics(content)
        
        # Status berechnen
        total_stories = sum(len(epic.get('stories', [])) for epic in epics)
        completed_stories = sum(
            len([s for s in epic.get('stories', []) if s.get('status') == 'completed'])
            for epic in epics
        )
        
        return {
            'epics': epics,
            'total_epics': len(epics),
            'total_stories': total_stories,
            'completed_stories': completed_stories,
            'progress_percentage': round((completed_stories / total_stories * 100) if total_stories > 0 else 0, 1)
        }
    
    def _extract_phases(self, content: str) -> List[Dict[str, Any]]:
        """Extrahiert Phasen aus ROADMAP.md"""
        phases = []
        
        # Suche nach ## Phase X: Pattern
        phase_pattern = r'## Phase (\d+):\s*([^\n]+)'
        phase_matches = re.findall(phase_pattern, content)
        
        for phase_num, phase_title in phase_matches:
            phase_info = {
                'number': int(phase_num),
                'title': phase_title.strip(),
                'status': 'planned',
                'sprints': []
            }
            
            # Status bestimmen
            if f'Phase {phase_num}' in content:
                phase_section = self._extract_section(content, f'Phase {phase_num}')
                if '100%' in phase_section or 'Abgeschlossen' in phase_section:
                    phase_info['status'] = 'completed'
                elif 'AKTUELL' in phase_section or 'IN BEARBEITUNG' in phase_section:
                    phase_info['status'] = 'current'
            
            # Sprints extrahieren
            sprint_pattern = r'### Sprint (\d+\.\d+):\s*([^\n]+)'
            sprint_matches = re.findall(sprint_pattern, phase_section)
            
            for sprint_num, sprint_title in sprint_matches:
                phase_info['sprints'].append({
                    'number': sprint_num,
                    'title': sprint_title.strip(),
                    'status': 'planned'
                })
            
            phases.append(phase_info)
        
        return phases
    
    def _extract_epics(self, content: str) -> List[Dict[str, Any]]:
        """Extrahiert Epics aus USER_STORIES.md"""
        epics = []
        
        # Suche nach ## Epic X: Pattern
        epic_pattern = r'## Epic (\d+):\s*([^\n]+)'
        epic_matches = re.findall(epic_pattern, content)
        
        for epic_num, epic_title in epic_matches:
            epic_info = {
                'number': int(epic_num),
                'title': epic_title.strip(),
                'stories': []
            }
            
            # User Stories in diesem Epic extrahieren
            epic_section = self._extract_section(content, f'Epic {epic_num}')
            story_pattern = r'### US-(\d+):\s*([^\n]+)'
            story_matches = re.findall(story_pattern, epic_section)
            
            for story_num, story_title in story_matches:
                story_info = {
                    'number': int(story_num),
                    'title': story_title.strip(),
                    'status': 'planned',
                    'description': ''
                }
                
                # Status bestimmen
                story_section = self._extract_section(epic_section, f'US-{story_num}')
                if '[x]' in story_section:
                    story_info['status'] = 'completed'
                elif '[ ]' in story_section:
                    story_info['status'] = 'planned'
                
                # Beschreibung extrahieren (erste Zeile nach dem Titel)
                lines = story_section.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith(f'### US-{story_num}'):
                        if i + 1 < len(lines) and lines[i + 1].strip():
                            story_info['description'] = lines[i + 1].strip()
                        break
                
                epic_info['stories'].append(story_info)
            
            epics.append(epic_info)
        
        return epics
    
    def _extract_milestones(self, content: str) -> List[Dict[str, Any]]:
        """Extrahiert Meilensteine aus ROADMAP.md"""
        milestones = []
        
        # Suche nach Muster: M1 (Woche X): Beschreibung
        milestone_pattern = r'(M\d+)\s*\(Woche\s*(\d+)\):\s*([^\n]+)'
        milestone_matches = re.findall(milestone_pattern, content)
        
        for milestone_id, week, description in milestone_matches:
            milestones.append({
                'id': milestone_id,
                'week': int(week),
                'description': description.strip(),
                'status': 'planned'
            })
        
        return milestones
    
    def _extract_status(self, content: str) -> Dict[str, Any]:
        """Extrahiert aktuellen Status aus ROADMAP.md"""
        status = {
            'current_phase': 'Phase 7: UI-Modularisierung',
            'progress_percentage': 85,
            'next_steps': []
        }
        
        # Nächste Schritte extrahieren
        if 'Nächste Schritte' in content:
            next_steps_section = self._extract_section(content, 'Nächste Schritte')
            step_pattern = r'-\s*([^\n]+)'
            steps = re.findall(step_pattern, next_steps_section)
            status['next_steps'] = [step.strip() for step in steps[:3]]  # Nur die ersten 3
        
        return status
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extrahiert einen Abschnitt aus dem Markdown-Content"""
        lines = content.split('\n')
        section_lines = []
        in_section = False
        
        for i, line in enumerate(lines):
            if section_name in line and line.startswith('##'):
                in_section = True
                section_lines.append(line)
            elif in_section and line.startswith('##') and not line.startswith('###') and section_name not in line:
                # Stoppe nur bei echten ## Headern (nicht bei ###)
                break
            elif in_section:
                section_lines.append(line)
        
        return '\n'.join(section_lines)
    
    def _extract_priorities(self, content: str) -> List[Dict[str, Any]]:
        """Extrahiert priorisierte User Stories aus der Roadmap"""
        priorities = []
        
        # Einfache Extraktion: Suche nach User Stories mit einfacherem Pattern
        lines = content.split('\n')
        current_priority = None
        current_stories = []
        
        for i, line in enumerate(lines):
            # Prioritäts-Header erkennen
            if line.startswith('## 🎯'):
                if current_priority and current_stories:
                    priorities.append({
                        'name': current_priority,
                        'stories': current_stories
                    })
                
                # Neue Priorität bestimmen
                if 'KRITISCH' in line.upper():
                    current_priority = 'kritisch'
                elif 'HOCH' in line.upper():
                    current_priority = 'hoch'
                elif 'MITTEL' in line.upper():
                    current_priority = 'mittel'
                elif 'NIEDRIG' in line.upper():
                    current_priority = 'niedrig'
                else:
                    current_priority = 'niedrig'
                
                current_stories = []
            
            # User Story erkennen
            elif line.startswith('### US-') and i < len(lines) - 1:
                # Story-Details aus den nächsten Zeilen extrahieren
                story_data = self._extract_story_from_lines(lines, i)
                if story_data:
                    story_data['priority'] = current_priority
                    current_stories.append(story_data)
        
        # Abgeschlossene Stories hinzufügen
        if current_priority and current_stories:
            priorities.append({
                'name': current_priority,
                'stories': current_stories
            })
        
        return priorities
    
    def _extract_story_from_lines(self, lines: List[str], start_index: int) -> Dict[str, Any]:
        """Extrahiert eine User Story aus den Zeilen ab dem gegebenen Index"""
        if start_index >= len(lines):
            return None
        
        title = lines[start_index].replace('### ', '').strip()
        
        # Status, Epic, As, Want, So_that aus den nächsten Zeilen extrahieren
        status = "Geplant"
        epic = "Unbekannt"
        as_user = "Administrator"
        want = "Funktionalität"
        so_that = "der Workflow verbessert wird"
        
        # Schaue in den nächsten 10 Zeilen nach Details
        for i in range(start_index + 1, min(start_index + 10, len(lines))):
            line = lines[i].strip()
            
            if line.startswith('**Status:**'):
                status = line.replace('**Status:**', '').strip()
            elif line.startswith('**Epic:**'):
                epic = line.replace('**Epic:**', '').strip()
            elif line.startswith('**Als**'):
                as_user = line.replace('**Als**', '').strip()
            elif line.startswith('**möchte ich**'):
                want = line.replace('**möchte ich**', '').strip()
            elif line.startswith('**damit**'):
                so_that = line.replace('**damit**', '').strip()
                break
        
        return {
            'title': title,
            'status': self._normalize_status(status),
            'epic': epic,
            'as': as_user,
            'want': want,
            'so_that': so_that,
            'acceptance_criteria': []  # Vereinfacht für jetzt
        }
    
    def _extract_priority_from_title(self, title: str, content: str) -> str:
        """Extrahiert die Priorität einer User Story basierend auf dem Kontext"""
        # Suche nach dem Abschnitt, in dem die Story steht
        lines = content.split('\n')
        current_section = None
        
        for i, line in enumerate(lines):
            if title in line and line.startswith('###'):
                # Schaue zurück nach dem nächsten ## Header
                for j in range(i-1, -1, -1):
                    if lines[j].startswith('## 🎯'):
                        current_section = lines[j].lower()
                        break
                break
        
        if current_section:
            if 'kritisch' in current_section:
                return 'kritisch'
            elif 'hoch' in current_section:
                return 'hoch'
            elif 'mittel' in current_section:
                return 'mittel'
            elif 'niedrig' in current_section:
                return 'niedrig'
        
        return 'niedrig'
    
    def _extract_stories_from_priority(self, content: str) -> List[Dict[str, Any]]:
        """Extrahiert User Stories aus einem Prioritäts-Abschnitt"""
        stories = []
        
        # User Story Pattern
        story_pattern = r'### ([^-]+)\s*\*\*Status:\*\*\s*([^*]+)\s*\*\*Epic:\*\*\s*([^*]+)\s*\*\*Als\*\* ([^*]+) \*\*möchte ich\*\* ([^*]+) \*\*damit\*\* ([^*]+)'
        
        matches = re.findall(story_pattern, content, re.DOTALL)
        
        for title, status, epic, as_user, want, so_that in matches:
            # Akzeptanzkriterien extrahieren
            acceptance_criteria = self._extract_acceptance_criteria(content, title)
            
            stories.append({
                'title': title.strip(),
                'status': self._normalize_status(status.strip()),
                'epic': epic.strip(),
                'as': as_user.strip(),
                'want': want.strip(),
                'so_that': so_that.strip(),
                'acceptance_criteria': acceptance_criteria
            })
        
        return stories
    
    def _extract_acceptance_criteria(self, content: str, story_title: str) -> List[str]:
        """Extrahiert Akzeptanzkriterien für eine User Story"""
        # Suche nach dem Akzeptanzkriterien-Block für diese Story
        pattern = rf'### {re.escape(story_title)}.*?### |\Z'
        story_section = re.search(pattern, content, re.DOTALL)
        
        if not story_section:
            return []
        
        criteria = []
        lines = story_section.group(0).split('\n')
        
        for line in lines:
            if line.strip().startswith('- ['):
                # Entferne Checkbox-Syntax und extrahiere Text
                criteria_text = re.sub(r'^- \[[ x]\]\s*', '', line.strip())
                if criteria_text:
                    criteria.append(criteria_text)
        
        return criteria
    
    def _extract_backlog_status(self, content: str) -> Dict[str, Any]:
        """Extrahiert Status-Informationen aus dem Backlog"""
        status = {}
        
        # Gesamtstatistiken extrahieren
        stats_pattern = r'\*\*Gesamt:\*\*\s*(\d+)\s*User Stories\s*\|\s*\*\*Abgeschlossen:\*\*\s*(\d+)\s*\|\s*\*\*In Bearbeitung:\*\*\s*(\d+)\s*\|\s*\*\*Geplant:\*\*\s*(\d+)'
        stats_match = re.search(stats_pattern, content)
        
        if stats_match:
            total, completed, in_progress, planned = map(int, stats_match.groups())
            status.update({
                'total_stories': total,
                'completed_stories': completed,
                'in_progress_stories': in_progress,
                'planned_stories': planned,
                'progress_percentage': round((completed / total) * 100) if total > 0 else 0
            })
        
        return status
    
    def _normalize_status(self, status: str) -> str:
        """Normalisiert Status-Strings"""
        status_lower = status.lower()
        if 'abgeschlossen' in status_lower or 'completed' in status_lower or '✅' in status:
            return 'completed'
        elif 'bearbeitung' in status_lower or 'progress' in status_lower or '🔄' in status:
            return 'in-progress'
        elif 'geplant' in status_lower or 'planned' in status_lower or '📋' in status:
            return 'planned'
        else:
            return 'planned'
