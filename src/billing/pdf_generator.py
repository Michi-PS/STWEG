"""
STWEG PDF-Rechnungsgenerator
Generiert professionelle Rechnungen basierend auf der analysierten Vorlage
"""

import os
import sys
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal
from typing import Dict, List, Any, Optional

# Projekt-Pfade hinzufügen
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import black, white, grey, Color
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Modelle importieren
from src.models.models import Eigentuemer, Messpunkt, Verbrauchsdaten
from src.models.database import get_db_session


class STWEGPDFGenerator:
    """PDF-Generator für STWEG Rechnungen basierend auf der analysierten Vorlage"""
    
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 2 * cm
        self.content_width = self.page_width - 2 * self.margin
        
        # Farben definieren
        self.primary_color = Color(0.2, 0.4, 0.6)  # Dunkelblau
        self.secondary_color = Color(0.8, 0.8, 0.8)  # Hellgrau
        self.accent_color = Color(0.9, 0.3, 0.3)  # Rot für Beträge
        
        # Styles definieren
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Definiert benutzerdefinierte Styles basierend auf der Vorlage"""
        
        # Header-Style (STWEG)
        self.styles.add(ParagraphStyle(
            name='STWEGHeader',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.primary_color,
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        # Adresse-Style
        self.styles.add(ParagraphStyle(
            name='Address',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=3
        ))
        
        # Rechnungstitel
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.primary_color,
            alignment=TA_LEFT,
            spaceAfter=12
        ))
        
        # Eigentümer-Info
        self.styles.add(ParagraphStyle(
            name='OwnerInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        # Tabellen-Header
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=white,
            alignment=TA_CENTER,
            backColor=self.primary_color
        ))
        
        # Tabellen-Inhalt
        self.styles.add(ParagraphStyle(
            name='TableContent',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT
        ))
        
        # Betrag-Style
        self.styles.add(ParagraphStyle(
            name='Amount',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_RIGHT,
            textColor=self.accent_color
        ))
        
        # Total-Style
        self.styles.add(ParagraphStyle(
            name='Total',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_RIGHT,
            textColor=self.accent_color,
            fontName='Helvetica-Bold'
        ))
    
    def generate_sample_invoice(self, output_path: str = None) -> str:
        """Generiert eine Beispiel-Rechnung mit Test-Daten"""
        
        if not output_path:
            output_path = str(project_root / 'data' / 'exports' / 'invoices' / f'sample_invoice_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        
        # Export-Verzeichnis erstellen
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Beispiel-Daten generieren
        sample_data = self._generate_sample_data()
        
        # PDF erstellen
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        # Story (Inhalt) erstellen
        story = []
        
        # Seite 1: Hauptrechnung
        story.extend(self._create_header_page(sample_data))
        
        # Seite 2: Detailaufstellung
        story.append(PageBreak())
        story.extend(self._create_detail_page(sample_data))
        
        # PDF generieren
        doc.build(story)
        
        print(f"✅ Beispiel-Rechnung generiert: {output_path}")
        return output_path
    
    def _generate_sample_data(self) -> Dict[str, Any]:
        """Generiert realistische Beispiel-Daten für die Rechnung"""
        
        return {
            'invoice_number': f"R-{datetime.now().strftime('%Y%m%d')}-001",
            'invoice_date': date.today().strftime('%d.%m.%Y'),
            'billing_period': '01.01.2024 - 31.12.2024',
            
            'stweg_info': {
                'name': 'STWEG',
                'address': 'Zwischenbächen 115',
                'city': '8048 Zürich'
            },
            
            'owner': {
                'name': 'Tanja & Michi Müller',
                'address': 'Zwischenbächen 115',
                'apartment': '1.3',
                'city': '8048 Zürich',
                'parcel': '26P4'
            },
            
            'property_info': {
                'property': 'Zwischenbächen 115',
                'apartment': '1.3'
            },
            
            'costs': {
                'strom_wasser': {
                    'amount': Decimal('2901.86'),
                    'details': 'gemäss separater Aufstellung'
                },
                'betriebskosten': {
                    'total_building': Decimal('12500.00'),
                    'value_share': Decimal('102.0'),  # Promille
                    'owner_share': Decimal('1275.00')
                },
                'total_nebenkosten': Decimal('4176.86'),
                'akonto_paid': Decimal('3500.00'),
                'difference': Decimal('676.86'),
                'difference_favor': 'STWEG'
            },
            
            'strom_details': {
                'netz_ewz': {
                    'wohnung_hochtarif': {'kwh': 1004, 'promille': 37.69, 'betrag': Decimal('551.64')},
                    'wohnung_niedertarif': {'kwh': 629, 'promille': 14.98, 'betrag': Decimal('219.28')},
                    'ladestation_hochtarif': {'kwh': 1243, 'promille': 46.68, 'betrag': Decimal('683.17')},
                    'ladestation_niedertarif': {'kwh': 1254, 'promille': 29.88, 'betrag': Decimal('437.29')},
                    'total': Decimal('1891.38')
                },
                'waerme': {
                    'netz_ewz': {'total': Decimal('7046.50'), 'promille': 102.0, 'betrag': Decimal('722.05')},
                    'pv': {'total': Decimal('593.46'), 'promille': 102.0, 'betrag': Decimal('60.81')},
                    'total': Decimal('782.86')
                },
                'pv': {
                    'wohnung_hochtarif': {'kwh': 444, 'tarif': 16.40, 'betrag': Decimal('72.79')},
                    'wohnung_niedertarif': {'kwh': 98, 'tarif': 16.40, 'betrag': Decimal('16.06')},
                    'ladestation_hochtarif': {'kwh': 208, 'tarif': 16.40, 'betrag': Decimal('34.05')},
                    'ladestation_niedertarif': {'kwh': 68, 'tarif': 16.40, 'betrag': Decimal('11.16')},
                    'total': Decimal('134.07')
                },
                'total_strom': Decimal('2808.31'),
                'erneuerungsfond': Decimal('194.88')
            },
            
            'wasser_details': {
                'period': 'September 2023 - September 2024',
                'leistungsgebuehr': {'building_total': Decimal('517.18'), 'promille': 115.14, 'betrag': Decimal('59.55')},
                'verbrauch': {'building_total': Decimal('812.5'), 'promille': 115.14, 'betrag': Decimal('93.55')},
                'total': Decimal('153.10')
            },
            
            'totals': {
                'strom_wasser_total': Decimal('2901.86'),
                'erneuerungsfond_total': Decimal('194.88')
            }
        }
    
    def _create_header_page(self, data: Dict[str, Any]) -> List:
        """Erstellt die Kopfzeile der Rechnung (Seite 1)"""
        story = []
        
        # STWEG Header
        story.append(Paragraph("STWEG", self.styles['STWEGHeader']))
        
        # Adresse
        stweg = data['stweg_info']
        story.append(Paragraph(f"{stweg['address']}", self.styles['Address']))
        story.append(Paragraph(f"{stweg['city']}", self.styles['Address']))
        story.append(Spacer(1, 12))
        
        # Empfänger-Adresse
        owner = data['owner']
        story.append(Paragraph(f"{owner['name']}", self.styles['Address']))
        story.append(Paragraph(f"{owner['address']}", self.styles['Address']))
        story.append(Paragraph(f"{owner['city']}", self.styles['Address']))
        story.append(Spacer(1, 12))
        
        # Datum
        story.append(Paragraph(f"Zürich, {data['invoice_date']}", self.styles['Address']))
        story.append(Spacer(1, 20))
        
        # Rechnungstitel
        story.append(Paragraph("Nebenkostenabrechnung", self.styles['InvoiceTitle']))
        story.append(Spacer(1, 12))
        
        # Eigentümer-Informationen
        story.append(Paragraph(f"Liegenschaft: {data['property_info']['property']}", self.styles['OwnerInfo']))
        story.append(Paragraph(f"Eigentümer: {owner['name']}", self.styles['OwnerInfo']))
        story.append(Paragraph(f"Abrechnungsperiode: {data['billing_period']}", self.styles['OwnerInfo']))
        story.append(Paragraph(f"Wohnung: {data['property_info']['apartment']}", self.styles['OwnerInfo']))
        story.append(Spacer(1, 20))
        
        # Hauptkosten-Übersicht
        costs = data['costs']
        
        # Strom- und Wasserkosten
        story.append(Paragraph("Strom- und Wasserkosten", self.styles['InvoiceTitle']))
        story.append(Paragraph(f"Anteil Strom- und Wasserkosten {costs['strom_wasser']['amount']:.2f} CHF", self.styles['OwnerInfo']))
        story.append(Paragraph("(gemäss separater Aufstellung)", self.styles['OwnerInfo']))
        story.append(Spacer(1, 12))
        
        # Betriebskosten
        story.append(Paragraph("Betriebskosten", self.styles['InvoiceTitle']))
        story.append(Paragraph(f"Betriebskosten Liegenschaft {costs['betriebskosten']['total_building']:.2f} CHF", self.styles['OwnerInfo']))
        story.append(Paragraph(f"Wertquote {costs['betriebskosten']['value_share']} ‰", self.styles['OwnerInfo']))
        story.append(Paragraph(f"Anteil Betriebskosten {costs['betriebskosten']['owner_share']:.2f} CHF", self.styles['OwnerInfo']))
        story.append(Spacer(1, 20))
        
        # Zusammenfassung
        story.append(HRFlowable(width="100%", thickness=1, color=self.secondary_color))
        story.append(Spacer(1, 6))
        
        summary_data = [
            ['Total Nebenkosten', f"{costs['total_nebenkosten']:.2f} CHF"],
            ['Akontozahlung geleistet', f"{costs['akonto_paid']:.2f} CHF"],
            ['Differenz zu Gunsten von', f"{costs['difference_favor']} {costs['difference']:.2f} CHF"]
        ]
        
        summary_table = Table(summary_data, colWidths=[8*cm, 4*cm])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTNAME', (1, -1), (1, -1), 'Helvetica-Bold'),  # Letzte Zeile fett
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTSIZE', (1, -1), (1, -1), 12),  # Letzte Zeile größer
            ('TEXTCOLOR', (1, -1), (1, -1), self.accent_color),
            ('LINEBELOW', (0, -1), (-1, -1), 1, self.accent_color),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(summary_table)
        
        return story
    
    def _create_detail_page(self, data: Dict[str, Any]) -> List:
        """Erstellt die Detailseite mit Strom- und Wasserkosten (Seite 2)"""
        story = []
        
        # Titel
        story.append(Paragraph("Abrechnung Strom- und Wasserkosten aus ZEV Zwischenbächen 115", self.styles['InvoiceTitle']))
        story.append(Paragraph(f"Wohnung {data['property_info']['apartment']} {data['owner']['name']} {data['owner']['parcel']} Wohnung {data['property_info']['apartment']}", self.styles['OwnerInfo']))
        story.append(Paragraph(f"Periode {data['billing_period']}", self.styles['OwnerInfo']))
        story.append(Spacer(1, 20))
        
        # Stromverbrauch Netz/EWZ
        story.append(Paragraph("Stromverbrauch Netz/EWZ", self.styles['InvoiceTitle']))
        
        strom_netz = data['strom_details']['netz_ewz']
        strom_table_data = [
            ['Menge [kWh]', 'Promille [‰]', 'Betrag [CHF]'],
            ['Wohnung Hochtarif', f"{strom_netz['wohnung_hochtarif']['kwh']}", f"{strom_netz['wohnung_hochtarif']['promille']}", f"{strom_netz['wohnung_hochtarif']['betrag']:.2f}"],
            ['Wohnung Niedertarif', f"{strom_netz['wohnung_niedertarif']['kwh']}", f"{strom_netz['wohnung_niedertarif']['promille']}", f"{strom_netz['wohnung_niedertarif']['betrag']:.2f}"],
            ['Ladestation eMobilität Hochtarif', f"{strom_netz['ladestation_hochtarif']['kwh']}", f"{strom_netz['ladestation_hochtarif']['promille']}", f"{strom_netz['ladestation_hochtarif']['betrag']:.2f}"],
            ['Ladestation eMobilität Niedertarif', f"{strom_netz['ladestation_niedertarif']['kwh']}", f"{strom_netz['ladestation_niedertarif']['promille']}", f"{strom_netz['ladestation_niedertarif']['betrag']:.2f}"],
            ['Total Stromverbrauch Netz/EWZ', '', '', f"{strom_netz['total']:.2f}"]
        ]
        
        strom_table = Table(strom_table_data, colWidths=[6*cm, 2*cm, 2*cm, 2*cm])
        strom_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(strom_table)
        story.append(Spacer(1, 15))
        
        # Stromverbrauch für Wärme
        story.append(Paragraph("Stromverbrauch für Wärme (Heizung und Warmwasser)", self.styles['InvoiceTitle']))
        
        waerme = data['strom_details']['waerme']
        waerme_table_data = [
            ['Total [CHF]', 'Promille [‰] (gemäss Neovac)', 'Betrag [CHF]'],
            ['Stromkosten aus Netz/EWZ', f"{waerme['netz_ewz']['total']:.2f}", f"{waerme['netz_ewz']['promille']}", f"{waerme['netz_ewz']['betrag']:.2f}"],
            ['Stromkosten aus PV*', f"{waerme['pv']['total']:.2f}", f"{waerme['pv']['promille']}", f"{waerme['pv']['betrag']:.2f}"],
            ['Total Stromverbrauch für Wärme (Heizung und Warmwasser)', '', '', f"{waerme['total']:.2f}"]
        ]
        
        waerme_table = Table(waerme_table_data, colWidths=[6*cm, 3*cm, 3*cm])
        waerme_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(waerme_table)
        story.append(Spacer(1, 15))
        
        # Stromverbrauch aus PV
        story.append(Paragraph("Stromverbrauch aus PV", self.styles['InvoiceTitle']))
        
        pv = data['strom_details']['pv']
        pv_table_data = [
            ['Menge [kWh]', 'Tarif PV [Rp.]', 'Betrag [CHF]'],
            ['Wohnung Hochtarif', f"{pv['wohnung_hochtarif']['kwh']}", f"{pv['wohnung_hochtarif']['tarif']}", f"{pv['wohnung_hochtarif']['betrag']:.2f}"],
            ['Wohnung Niedertarif', f"{pv['wohnung_niedertarif']['kwh']}", f"{pv['wohnung_niedertarif']['tarif']}", f"{pv['wohnung_niedertarif']['betrag']:.2f}"],
            ['Ladestation eMobilität Hochtarif', f"{pv['ladestation_hochtarif']['kwh']}", f"{pv['ladestation_hochtarif']['tarif']}", f"{pv['ladestation_hochtarif']['betrag']:.2f}"],
            ['Ladestation eMobilität Niedertarif', f"{pv['ladestation_niedertarif']['kwh']}", f"{pv['ladestation_niedertarif']['tarif']}", f"{pv['ladestation_niedertarif']['betrag']:.2f}"],
            ['Total Stromverbrauch aus PV*', '', '', f"{pv['total']:.2f}"]
        ]
        
        pv_table = Table(pv_table_data, colWidths=[6*cm, 3*cm, 3*cm])
        pv_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(pv_table)
        story.append(Spacer(1, 15))
        
        # Strom-Totals
        totals_table_data = [
            ['Total Stromkosten (inkl. MwSt)', f"{data['strom_details']['total_strom']:.2f} CHF"],
            ['Davon Einzahlung in Erneuerungsfond*', f"{data['strom_details']['erneuerungsfond']:.2f} CHF"]
        ]
        
        totals_table = Table(totals_table_data, colWidths=[8*cm, 4*cm])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(totals_table)
        story.append(Spacer(1, 20))
        
        # Wasserkosten
        story.append(Paragraph("Wasserkosten", self.styles['InvoiceTitle']))
        story.append(Paragraph(f"{data['wasser_details']['period']}", self.styles['OwnerInfo']))
        
        wasser = data['wasser_details']
        wasser_table_data = [
            ['Gebäude gesamt [CHF]', 'Promille [‰] (gemäss Neovac)', 'Betrag [CHF]'],
            ['Leistungs- und Gebäudegebühr', f"{wasser['leistungsgebuehr']['building_total']:.2f}", f"{wasser['leistungsgebuehr']['promille']}", f"{wasser['leistungsgebuehr']['betrag']:.2f}"],
            ['Wasser-Verbrauch und -Entsorgung', f"{wasser['verbrauch']['building_total']:.2f}", f"{wasser['verbrauch']['promille']}", f"{wasser['verbrauch']['betrag']:.2f}"],
            ['Total Wasserkosten', '', '', f"{wasser['total']:.2f}"]
        ]
        
        wasser_table = Table(wasser_table_data, colWidths=[6*cm, 3*cm, 3*cm])
        wasser_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(wasser_table)
        story.append(Spacer(1, 15))
        
        # Finale Totals
        final_totals_data = [
            ['Total Strom- und Wasserkosten (inkl. MwSt)', f"{data['totals']['strom_wasser_total']:.2f} CHF"],
            ['Davon Einzahlung in Erneuerungsfond*', f"{data['totals']['erneuerungsfond_total']:.2f} CHF"]
        ]
        
        final_totals_table = Table(final_totals_data, colWidths=[8*cm, 4*cm])
        final_totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.accent_color),
            ('LINEBELOW', (0, -1), (-1, -1), 2, self.accent_color),
        ]))
        
        story.append(final_totals_table)
        story.append(Spacer(1, 20))
        
        # Fußnoten
        story.append(Paragraph("Hochtarif Mo - Sa, 6-22 Uhr", self.styles['Address']))
        story.append(Paragraph("Niedertarif übrige Zeit", self.styles['Address']))
        story.append(Paragraph("* Stromkosten für Strom aus PV wird in Erneuerungsfond eingezahlt und ist damit steuerlich abzugsfähig", self.styles['Address']))
        
        return story


def main():
    """Test-Funktion für den PDF-Generator"""
    print("🚀 STWEG PDF-Generator Test")
    print("=" * 40)
    
    generator = STWEGPDFGenerator()
    
    try:
        output_file = generator.generate_sample_invoice()
        print(f"✅ PDF erfolgreich generiert: {output_file}")
        
        # Dateigröße anzeigen
        file_size = Path(output_file).stat().st_size
        print(f"📄 Dateigröße: {file_size / 1024:.1f} KB")
        
    except Exception as e:
        print(f"❌ Fehler beim Generieren der PDF: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
