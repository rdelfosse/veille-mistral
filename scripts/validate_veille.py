#!/usr/bin/env python3
"""
Script de validation des fichiers de veille.
Vérifie la cohérence des schémas JSON et les règles dures.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def validate_harvest(filepath):
    """Valide un fichier raw/YYYY-WNN.json"""
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        errors.append(f"❌ Fichier invalide ou introuvable: {filepath} ({e})")
        return errors

    # Vérifier la structure de base
    if not isinstance(data, dict):
        errors.append(f"❌ {filepath}: doit être un objet JSON, pas une liste")
        return errors

    if 'metadata' not in data or 'items' not in data:
        errors.append(f"❌ {filepath}: champs 'metadata' ou 'items' manquants")
        return errors

    metadata = data['metadata']
    items = data['items']

    # Vérifier metadata
    required_metadata = ['topic', 'week', 'date_start', 'date_end', 'axes_collected']
    for field in required_metadata:
        if field not in metadata:
            errors.append(f"❌ {filepath}: champ 'metadata.{field}' manquant")

    # Vérifier date_start et date_end
    date_start = None
    date_end = None
    try:
        date_start = datetime.strptime(metadata.get('date_start', ''), '%Y-%m-%d')
        date_end = datetime.strptime(metadata.get('date_end', ''), '%Y-%m-%d')
        if date_start and date_end and date_start > date_end:
            errors.append(f"❌ {filepath}: date_start > date_end")
    except ValueError:
        errors.append(f"❌ {filepath}: format de date invalide (attendu YYYY-MM-DD)")

    # Vérifier chaque item
    required_item_fields = ['title', 'url', 'source', 'source_type', 'date', 'summary']
    for idx, item in enumerate(items):
        item_errors = []
        
        # Vérifier les champs obligatoires
        for field in required_item_fields:
            if field not in item or not item[field]:
                item_errors.append(f"champ '{field}' manquant ou vide")
        
        # Vérifier le format de la date
        if 'date' in item and item['date']:
            try:
                item_date = datetime.strptime(item['date'], '%Y-%m-%d')
                # Vérifier que la date est dans la fenêtre (si dates valides)
                if date_start and date_end:
                    if item_date < date_start or item_date > date_end:
                        item_errors.append(f"date '{item['date']}' hors fenêtre [{metadata['date_start']}, {metadata['date_end']}]")
            except ValueError:
                item_errors.append(f"format de date invalide: '{item['date']}' (attendu YYYY-MM-DD)")
        else:
            item_errors.append("date manquante")
        
        # Vérifier l'URL
        if 'url' in item and item['url']:
            url = item['url']
            if not url.startswith('http'):
                item_errors.append(f"URL invalide: '{url}' (doit commencer par http/https)")
            # Vérifier que ce n'est pas un flux/rubrique
            invalid_patterns = ['/feed/', '/rss/', '/flux/', '.xml', '.rss', '.atom']
            if any(pattern in url.lower() for pattern in invalid_patterns):
                item_errors.append(f"URL suspecte (flux/rubrique): '{url}'")
        
        # Vérifier source_type
        if 'source_type' in item and item['source_type']:
            valid_types = ['rss', 'search', 'blog']
            if item['source_type'] not in valid_types:
                item_errors.append(f"source_type invalide: '{item['source_type']}' (valides: {valid_types})")
        
        if item_errors:
            errors.append(f"❌ {filepath} [item {idx}]: {', '.join(item_errors)}")
    
    # Statistiques
    total_items = len(items)
    if total_items > 0:
        items_with_date = sum(1 for item in items if 'date' in item and item['date'])
        date_coverage = (items_with_date / total_items) * 100
        if date_coverage < 90:
            errors.append(f"⚠️  {filepath}: seulement {date_coverage:.1f}% des items ont une date valide")
        
        if date_start and date_end:
            items_in_window = sum(1 for item in items if 'date' in item and item['date'] and 
                                 date_start <= datetime.strptime(item['date'], '%Y-%m-%d') <= date_end)
            if items_in_window < total_items:
                errors.append(f"⚠️  {filepath}: {total_items - items_in_window} items hors fenêtre temporelle")
    
    return errors


def validate_data(filepath):
    """Valide un fichier data/YYYY-WNN.json"""
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        errors.append(f"❌ Fichier invalide ou introuvable: {filepath} ({e})")
        return errors

    if not isinstance(data, dict):
        errors.append(f"❌ {filepath}: doit être un objet JSON")
        return errors

    if 'metadata' not in data or 'insights' not in data:
        errors.append(f"❌ {filepath}: champs 'metadata' ou 'insights' manquants")
        return errors

    metadata = data['metadata']
    insights = data['insights']

    # Vérifier metadata
    required_metadata = ['topic', 'week', 'date_start', 'date_end', 'stats']
    for field in required_metadata:
        if field not in metadata:
            errors.append(f"❌ {filepath}: champ 'metadata.{field}' manquant")

    # Vérifier stats
    if 'stats' in metadata:
        stats = metadata['stats']
        if 'total_insights' not in stats:
            errors.append(f"❌ {filepath}: champ 'metadata.stats.total_insights' manquant")
        elif stats['total_insights'] != len(insights):
            errors.append(f"❌ {filepath}: stats.total_insights ({stats['total_insights']}) != nombre réel d'insights ({len(insights)})")
        
        if 'by_axis' in stats:
            by_axis_sum = sum(stats['by_axis'].values())
            if by_axis_sum != len(insights):
                errors.append(f"❌ {filepath}: somme(stats.by_axis) ({by_axis_sum}) != total_insights ({len(insights)})")

    # Vérifier chaque insight
    required_insight_fields = ['id', 'title', 'url', 'source', 'source_type', 'date', 'summary', 
                               'axes', 'primary_axis', 'actionability']
    
    for idx, insight in enumerate(insights):
        insight_errors = []
        
        # Champs obligatoires
        for field in required_insight_fields:
            if field not in insight:
                insight_errors.append(f"champ '{field}' manquant")
        
        # Vérifier actionability
        if 'actionability' in insight:
            actionability = insight['actionability']
            if isinstance(actionability, int):
                insight_errors.append(f"actionability doit être un objet, pas un entier (valeur: {actionability})")
            elif isinstance(actionability, dict):
                if 'score' not in actionability:
                    insight_errors.append("actionability.score manquant")
                if 'article_potential' not in actionability:
                    insight_errors.append("actionability.article_potential manquant")
                if 'cross_links' not in actionability:
                    insight_errors.append("actionability.cross_links manquant")
        
        # Vérifier axes
        if 'axes' in insight:
            axes = insight['axes']
            if not isinstance(axes, dict):
                insight_errors.append(f"axes doit être un objet, pas un {type(axes).__name__}")
        
        # Vérifier date
        if 'date' in insight:
            if not insight['date']:
                insight_errors.append("date vide")
            else:
                try:
                    datetime.strptime(insight['date'], '%Y-%m-%d')
                except ValueError:
                    insight_errors.append(f"format de date invalide: '{insight['date']}'")
        else:
            insight_errors.append("date manquante")
        
        # Vérifier primary_axis
        if 'primary_axis' in insight and insight['primary_axis']:
            if 'axes' in insight and isinstance(insight['axes'], dict):
                if insight['primary_axis'] not in insight['axes']:
                    insight_errors.append(f"primary_axis '{insight['primary_axis']}' non présent dans axes")
        
        # Vérifier que summary existe (pas description)
        if 'summary' not in insight and 'description' in insight:
            insight_errors.append("utilise 'summary' au lieu de 'description'")
        
        if insight_errors:
            errors.append(f"❌ {filepath} [insight {idx} - {insight.get('id', 'N/A')}]:")
            for err in insight_errors:
                errors.append(f"   - {err}")
    
    return errors


def validate_topic(topic_path):
    """Valide tous les fichiers d'un topic"""
    all_errors = []
    
    # Valider raw/
    raw_dir = topic_path / "raw"
    if raw_dir.exists():
        for raw_file in sorted(raw_dir.glob("*.json")):
            all_errors.extend(validate_harvest(raw_file))
    
    # Valider data/
    data_dir = topic_path / "data"
    if data_dir.exists():
        for data_file in sorted(data_dir.glob("*.json")):
            all_errors.extend(validate_data(data_file))
    
    return all_errors


def main():
    repo_root = Path(__file__).parent.parent
    topics_dir = repo_root / "topics"
    
    if not topics_dir.exists():
        print(f"❌ Répertoire {topics_dir} introuvable")
        sys.exit(1)
    
    all_errors = []
    has_errors = False
    for topic in sorted(topics_dir.iterdir()):
        if topic.is_dir() and topic.name != "_template":
            errors = validate_topic(topic)
            if errors:
                has_errors = True
                print(f"\n{'='*60}")
                print(f"Topic: {topic.name}")
                print('='*60)
                for error in errors:
                    print(error)
                all_errors.extend(errors)
    
    if not has_errors:
        print("✅ Tous les fichiers de veille sont valides !")
        return 0
    else:
        print(f"\n❌ {len(all_errors)} erreurs trouvées au total")
        return 1


if __name__ == "__main__":
    sys.exit(main())
