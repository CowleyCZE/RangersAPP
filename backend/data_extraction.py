import re
import spacy
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import logging
from dataclasses import dataclass
from enum import Enum

# Nastavení loggingu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentType(Enum):
    TECHNICAL_DRAWING = "technical_drawing"
    BUDGET = "budget"
    PROGRESS_REPORT = "progress_report"
    SPECIFICATION = "specification"
    SAFETY_DOCUMENT = "safety_document"
    UNKNOWN = "unknown"

@dataclass
class ExtractedMeasurement:
    value: float
    unit: str
    context: str
    measurement_type: str
    confidence: float

@dataclass
class ExtractedDate:
    date: datetime
    context: str
    date_type: str
    confidence: float

@dataclass
class ExtractedEntity:
    text: str
    label: str
    context: str
    confidence: float

@dataclass
class ExtractedMilestone:
    description: str
    date: Optional[datetime]
    priority: str
    status: str
    confidence: float

class AdvancedDataExtractor:
    def __init__(self):
        """Inicializace pokročilého extraktoru dat"""
        try:
            self.nlp = spacy.load("cs_core_news_lg")
        except OSError:
            logger.warning("Czech model not found, downloading...")
            spacy.cli.download("cs_core_news_lg")
            self.nlp = spacy.load("cs_core_news_lg")
        
        # Rozšíření pipeline o vlastní komponenty
        self._setup_custom_patterns()
        
    def _setup_custom_patterns(self):
        """Nastavení vlastních vzorů pro rozpoznávání"""
        # Vzory pro rozměry a měření
        self.measurement_patterns = [
            # Základní rozměry
            (r'(\d+(?:[.,]\d+)?)\s*x\s*(\d+(?:[.,]\d+)?)\s*x\s*(\d+(?:[.,]\d+)?)\s*(mm|cm|m)', 'dimensions_3d'),
            (r'(\d+(?:[.,]\d+)?)\s*x\s*(\d+(?:[.,]\d+)?)\s*(mm|cm|m)', 'dimensions_2d'),
            (r'(\d+(?:[.,]\d+)?)\s*(mm|cm|m|kg|t|kN|MPa)', 'single_measurement'),
            
            # Nosnosti a zatížení
            (r'(\d+(?:[.,]\d+)?)\s*(kg/m²|t/m²|kN/m²)', 'load_capacity'),
            (r'nosnost[:\s]*(\d+(?:[.,]\d+)?)\s*(kg|t|kN)', 'load_capacity'),
            (r'zatížení[:\s]*(\d+(?:[.,]\d+)?)\s*(kg|t|kN)', 'load_rating'),
            
            # Teploty a environmentální podmínky
            (r'(-?\d+(?:[.,]\d+)?)\s*°?C', 'temperature'),
            (r'vlhkost[:\s]*(\d+(?:[.,]\d+)?)\s*%', 'humidity'),
            
            # Elektrické parametry
            (r'(\d+(?:[.,]\d+)?)\s*(V|A|W|kW)', 'electrical'),
        ]
        
        # Vzory pro data
        self.date_patterns = [
            (r'(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})', 'dd_mm_yyyy'),
            (r'(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})', 'yyyy_mm_dd'),
            (r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})', 'dd_mm_yyyy_spaced'),
        ]
        
        # Klíčová slova pro milníky
        self.milestone_keywords = {
            'deadline': ['termín', 'deadline', 'dokončení', 'ukončení', 'finalizace'],
            'start': ['začátek', 'start', 'zahájení', 'spuštění'],
            'milestone': ['milník', 'fáze', 'etapa', 'krok', 'úkol'],
            'delivery': ['dodání', 'dodávka', 'předání', 'instalace'],
            'inspection': ['kontrola', 'revize', 'audit', 'přejímka']
        }
        
        # Vzory pro ceny a rozpočty
        self.price_patterns = [
            (r'(\d+(?:\s?\d{3})*(?:[.,]\d{2})?)\s*(Kč|CZK|EUR|€)', 'price'),
            (r'cena[:\s]*(\d+(?:\s?\d{3})*(?:[.,]\d{2})?)', 'price_value'),
            (r'celkem[:\s]*(\d+(?:\s?\d{3})*(?:[.,]\d{2})?)', 'total_price'),
        ]

    def classify_document_type(self, text: str) -> DocumentType:
        """Klasifikace typu dokumentu na základě obsahu"""
        text_lower = text.lower()
        
        # Klíčová slova pro různé typy dokumentů
        type_indicators = {
            DocumentType.TECHNICAL_DRAWING: ['výkres', 'schéma', 'rozměr', 'technický', 'detail', 'řez'],
            DocumentType.BUDGET: ['rozpočet', 'cena', 'kalkulace', 'náklad', 'faktura', 'cenová'],
            DocumentType.PROGRESS_REPORT: ['postup', 'progress', 'stav', 'dokončeno', 'procent'],
            DocumentType.SPECIFICATION: ['specifikace', 'požadavek', 'norma', 'standard', 'parametr'],
            DocumentType.SAFETY_DOCUMENT: ['bezpečnost', 'ochrana', 'riziko', 'nebezpečí', 'bozp']
        }
        
        scores = {}
        for doc_type, keywords in type_indicators.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[doc_type] = score
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return DocumentType.UNKNOWN

    def extract_measurements(self, text: str) -> List[ExtractedMeasurement]:
        """Extrakce rozměrů a měření z textu"""
        measurements = []
        
        for pattern, measurement_type in self.measurement_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Získání kontextu (50 znaků před a po)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    
                    if measurement_type == 'dimensions_3d':
                        # 3D rozměry (délka x šířka x výška)
                        length = float(match.group(1).replace(',', '.'))
                        width = float(match.group(2).replace(',', '.'))
                        height = float(match.group(3).replace(',', '.'))
                        unit = match.group(4)
                        
                        measurements.extend([
                            ExtractedMeasurement(length, unit, context, 'length', 0.9),
                            ExtractedMeasurement(width, unit, context, 'width', 0.9),
                            ExtractedMeasurement(height, unit, context, 'height', 0.9)
                        ])
                    
                    elif measurement_type == 'dimensions_2d':
                        # 2D rozměry (délka x šířka)
                        length = float(match.group(1).replace(',', '.'))
                        width = float(match.group(2).replace(',', '.'))
                        unit = match.group(3)
                        
                        measurements.extend([
                            ExtractedMeasurement(length, unit, context, 'length', 0.8),
                            ExtractedMeasurement(width, unit, context, 'width', 0.8)
                        ])
                    
                    else:
                        # Jednotlivé měření
                        value = float(match.group(1).replace(',', '.'))
                        unit = match.group(2) if len(match.groups()) > 1 else ''
                        
                        measurements.append(
                            ExtractedMeasurement(value, unit, context, measurement_type, 0.7)
                        )
                        
                except (ValueError, IndexError) as e:
                    logger.warning(f"Chyba při zpracování měření: {e}")
                    continue
        
        return measurements

    def extract_dates(self, text: str) -> List[ExtractedDate]:
        """Pokročilá extrakce dat z textu"""
        dates = []
        
        for pattern, date_format in self.date_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                try:
                    # Získání kontextu
                    start = max(0, match.start() - 30)
                    end = min(len(text), match.end() + 30)
                    context = text[start:end].strip()
                    
                    # Parsování data podle formátu
                    if date_format in ['dd_mm_yyyy', 'dd_mm_yyyy_spaced']:
                        day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
                    else:  # yyyy_mm_dd
                        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
                    
                    date = datetime(year, month, day)
                    
                    # Určení typu data na základě kontextu
                    date_type = self._classify_date_type(context)
                    confidence = self._calculate_date_confidence(context, date)
                    
                    dates.append(ExtractedDate(date, context, date_type, confidence))
                    
                except (ValueError, IndexError) as e:
                    logger.warning(f"Chyba při zpracování data: {e}")
                    continue
        
        return dates

    def _classify_date_type(self, context: str) -> str:
        """Klasifikace typu data na základě kontextu"""
        context_lower = context.lower()
        
        if any(word in context_lower for word in ['termín', 'deadline', 'dokončení']):
            return 'deadline'
        elif any(word in context_lower for word in ['začátek', 'start', 'zahájení']):
            return 'start_date'
        elif any(word in context_lower for word in ['dodání', 'dodávka']):
            return 'delivery_date'
        elif any(word in context_lower for word in ['kontrola', 'revize']):
            return 'inspection_date'
        else:
            return 'general_date'

    def _calculate_date_confidence(self, context: str, date: datetime) -> float:
        """Výpočet spolehlivosti extrakce data"""
        confidence = 0.5
        
        # Zvýšení spolehlivosti na základě kontextu
        if any(word in context.lower() for word in ['termín', 'deadline', 'dokončení', 'začátek']):
            confidence += 0.3
        
        # Snížení spolehlivosti pro data v minulosti (pokud nejde o historický dokument)
        if date < datetime.now() - timedelta(days=365):
            confidence -= 0.2
        
        # Zvýšení spolehlivosti pro rozumná budoucí data
        if datetime.now() < date < datetime.now() + timedelta(days=1095):  # 3 roky
            confidence += 0.2
        
        return max(0.1, min(1.0, confidence))

    def extract_milestones(self, text: str) -> List[ExtractedMilestone]:
        """Extrakce milníků projektu"""
        milestones = []
        doc = self.nlp(text)
        
        for sent in doc.sents:
            sent_text = sent.text.strip()
            sent_lower = sent_text.lower()
            
            # Kontrola, zda věta obsahuje klíčová slova pro milníky
            milestone_type = None
            for m_type, keywords in self.milestone_keywords.items():
                if any(keyword in sent_lower for keyword in keywords):
                    milestone_type = m_type
                    break
            
            if milestone_type:
                # Extrakce data z věty
                dates = self.extract_dates(sent_text)
                milestone_date = dates[0].date if dates else None
                
                # Určení priority na základě klíčových slov
                priority = self._determine_priority(sent_lower)
                
                # Určení stavu
                status = self._determine_status(sent_lower)
                
                # Výpočet spolehlivosti
                confidence = self._calculate_milestone_confidence(sent_text, milestone_date)
                
                milestones.append(ExtractedMilestone(
                    description=sent_text,
                    date=milestone_date,
                    priority=priority,
                    status=status,
                    confidence=confidence
                ))
        
        return milestones

    def _determine_priority(self, text: str) -> str:
        """Určení priority milníku"""
        if any(word in text for word in ['kritický', 'důležitý', 'prioritní', 'urgentní']):
            return 'high'
        elif any(word in text for word in ['volitelný', 'dodatečný', 'nice-to-have']):
            return 'low'
        else:
            return 'medium'

    def _determine_status(self, text: str) -> str:
        """Určení stavu milníku"""
        if any(word in text for word in ['dokončeno', 'hotovo', 'splněno', 'completed']):
            return 'completed'
        elif any(word in text for word in ['probíhá', 'in progress', 'zpracovává']):
            return 'in_progress'
        elif any(word in text for word in ['plánováno', 'planned', 'naplánováno']):
            return 'planned'
        else:
            return 'unknown'

    def _calculate_milestone_confidence(self, text: str, date: Optional[datetime]) -> float:
        """Výpočet spolehlivosti milníku"""
        confidence = 0.6
        
        # Zvýšení spolehlivosti pokud má datum
        if date:
            confidence += 0.2
        
        # Zvýšení spolehlivosti na základě struktury textu
        if any(char in text for char in [':', '-', '•']):
            confidence += 0.1
        
        # Zvýšení spolehlivosti pro číslované položky
        if re.match(r'^\d+\.', text.strip()):
            confidence += 0.1
        
        return min(1.0, confidence)

    def extract_prices(self, text: str) -> List[Dict[str, Any]]:
        """Extrakce cen a rozpočtových informací"""
        prices = []
        
        for pattern, price_type in self.price_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Získání kontextu
                    start = max(0, match.start() - 40)
                    end = min(len(text), match.end() + 40)
                    context = text[start:end].strip()
                    
                    # Extrakce hodnoty a měny
                    if price_type == 'price':
                        value_str = match.group(1).replace(' ', '').replace(',', '.')
                        currency = match.group(2)
                    else:
                        value_str = match.group(1).replace(' ', '').replace(',', '.')
                        currency = 'CZK'  # výchozí měna
                    
                    value = float(value_str)
                    
                    prices.append({
                        'value': value,
                        'currency': currency,
                        'type': price_type,
                        'context': context,
                        'confidence': 0.8
                    })
                    
                except (ValueError, IndexError) as e:
                    logger.warning(f"Chyba při zpracování ceny: {e}")
                    continue
        
        return prices

    def extract_technical_specifications(self, text: str) -> Dict[str, Any]:
        """Extrakce technických specifikací"""
        doc = self.nlp(text)
        specifications = {
            'materials': [],
            'standards': [],
            'certifications': [],
            'technical_parameters': []
        }
        
        # Vzory pro materiály
        material_patterns = [
            r'(ocel|kov|hliník|nerez|pozink)',
            r'(S\d{3}|EN\s?\d+)',  # Označení oceli
        ]
        
        # Vzory pro normy a standardy
        standard_patterns = [
            r'(EN\s?\d+(?:-\d+)?)',
            r'(ISO\s?\d+(?:-\d+)?)',
            r'(ČSN\s?\d+(?:\s?\d+)?)',
            r'(DIN\s?\d+)',
        ]
        
        for pattern in material_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                specifications['materials'].append({
                    'material': match.group(1),
                    'context': self._get_context(text, match)
                })
        
        for pattern in standard_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                specifications['standards'].append({
                    'standard': match.group(1),
                    'context': self._get_context(text, match)
                })
        
        return specifications

    def _get_context(self, text: str, match) -> str:
        """Získání kontextu pro match objekt"""
        start = max(0, match.start() - 30)
        end = min(len(text), match.end() + 30)
        return text[start:end].strip()

    def extract_key_data_from_text(self, text: str) -> Dict[str, Any]:
        """
        Hlavní funkce pro pokročilou extrakci klíčových dat z textu
        """
        logger.info("Zahajuji pokročilou extrakci dat z textu")
        
        # Klasifikace typu dokumentu
        doc_type = self.classify_document_type(text)
        
        # Základní zpracování pomocí spaCy
        doc = self.nlp(text)
        
        # Extrakce různých typů dat
        measurements = self.extract_measurements(text)
        dates = self.extract_dates(text)
        milestones = self.extract_milestones(text)
        prices = self.extract_prices(text)
        technical_specs = self.extract_technical_specifications(text)
        
        # Extrakce pojmenovaných entit
        entities = []
        for ent in doc.ents:
            entities.append(ExtractedEntity(
                text=ent.text,
                label=ent.label_,
                context=self._get_entity_context(text, ent),
                confidence=0.7
            ))
        
        # Extrakce klíčových slov a frází
        keywords = self._extract_keywords(doc)
        
        # Sestavení výsledku
        extracted_data = {
            'document_type': doc_type.value,
            'measurements': [
                {
                    'value': m.value,
                    'unit': m.unit,
                    'type': m.measurement_type,
                    'context': m.context,
                    'confidence': m.confidence
                } for m in measurements
            ],
            'dates': [
                {
                    'date': d.date.isoformat(),
                    'type': d.date_type,
                    'context': d.context,
                    'confidence': d.confidence
                } for d in dates
            ],
            'milestones': [
                {
                    'description': m.description,
                    'date': m.date.isoformat() if m.date else None,
                    'priority': m.priority,
                    'status': m.status,
                    'confidence': m.confidence
                } for m in milestones
            ],
            'prices': prices,
            'technical_specifications': technical_specs,
            'entities': [
                {
                    'text': e.text,
                    'label': e.label,
                    'context': e.context,
                    'confidence': e.confidence
                } for e in entities
            ],
            'keywords': keywords,
            'summary': self._generate_summary(doc_type, measurements, dates, milestones, prices)
        }
        
        logger.info(f"Extrakce dokončena. Nalezeno: {len(measurements)} měření, {len(dates)} dat, {len(milestones)} milníků")
        
        return extracted_data

    def _get_entity_context(self, text: str, entity) -> str:
        """Získání kontextu pro pojmenovanou entitu"""
        start = max(0, entity.start_char - 30)
        end = min(len(text), entity.end_char + 30)
        return text[start:end].strip()

    def _extract_keywords(self, doc) -> List[str]:
        """Extrakce klíčových slov a frází"""
        keywords = set()
        
        # Podstatná jména a jejich fráze
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1 and len(chunk.text) > 3:
                keywords.add(chunk.text.lower())
        
        # Důležitá jednotlivá slova
        for token in doc:
            if (token.pos_ in ['NOUN', 'ADJ'] and 
                len(token.text) > 4 and 
                not token.is_stop and 
                not token.is_punct):
                keywords.add(token.lemma_.lower())
        
        return sorted(list(keywords))

    def _generate_summary(self, doc_type: DocumentType, measurements: List[ExtractedMeasurement], 
                         dates: List[ExtractedDate], milestones: List[ExtractedMilestone], 
                         prices: List[Dict]) -> str:
        """Generování shrnutí extrahovaných dat"""
        summary_parts = [f"Typ dokumentu: {doc_type.value}"]
        
        if measurements:
            summary_parts.append(f"Nalezeno {len(measurements)} měření")
        
        if dates:
            summary_parts.append(f"Nalezeno {len(dates)} dat")
        
        if milestones:
            summary_parts.append(f"Nalezeno {len(milestones)} milníků")
        
        if prices:
            total_value = sum(p['value'] for p in prices if p['type'] in ['price', 'total_price'])
            if total_value > 0:
                summary_parts.append(f"Celková hodnota: {total_value:,.2f}")
        
        return "; ".join(summary_parts)

# Globální instance extraktoru
_extractor_instance = None

def get_extractor() -> AdvancedDataExtractor:
    """Získání singleton instance extraktoru"""
    global _extractor_instance
    if _extractor_instance is None:
        _extractor_instance = AdvancedDataExtractor()
    return _extractor_instance

def extract_key_data_from_text(text: str) -> Dict[str, Any]:
    """Wrapper funkce pro kompatibilitu se stávajícím kódem"""
    extractor = get_extractor()
    return extractor.extract_key_data_from_text(text)