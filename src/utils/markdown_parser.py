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
        """Parse ROADMAP.md in strukturierte Daten"""
        roadmap_file = self.project_root / 'ROADMAP.md'
        
        if not roadmap_file.exists():
            return {'error': 'ROADMAP.md nicht gefunden'}
        
        with open(roadmap_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Phasen extrahieren
        phases = self._extract_phases(content)
        
        # Milestones extrahieren
        milestones = self._extract_milestones(content)
        
        # Status extrahieren
        status = self._extract_status(content)
        
        return {
            'phases': phases,
            'milestones': milestones,
            'status': status,
            'total_phases': len(phases),
            'completed_phases': len([p for p in phases if p.get('status') == 'completed'])
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
