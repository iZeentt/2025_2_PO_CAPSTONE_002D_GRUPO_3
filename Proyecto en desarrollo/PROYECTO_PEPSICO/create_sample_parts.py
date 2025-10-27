#!/usr/bin/env python3
"""
Script para crear repuestos de ejemplo en el sistema
"""
from app import create_app
from extensions import db
from models import Part, User

def create_sample_parts():
    app = create_app()
    with app.app_context():
        # Buscar el usuario asistente de repuestos
        user = User.query.filter_by(role='parts_assistant').first()
        
        if not user:
            print("❌ No se encontró ningún usuario con rol 'parts_assistant'")
            print("   Ejecuta primero: python create_parts_assistant_user.py")
            return
        
        # Repuestos de ejemplo
        sample_parts = [
            {
                'code': 'FIL-001',
                'name': 'Filtro de Aceite',
                'description': 'Filtro de aceite compatible con motores diesel',
                'stock': 25,
                'min_stock': 5
            },
            {
                'code': 'FIL-002',
                'name': 'Filtro de Aire',
                'description': 'Filtro de aire de alta eficiencia',
                'stock': 15,
                'min_stock': 5
            },
            {
                'code': 'FIL-003',
                'name': 'Filtro de Combustible',
                'description': 'Filtro de combustible diesel',
                'stock': 20,
                'min_stock': 5
            },
            {
                'code': 'PAST-001',
                'name': 'Pastillas de Freno',
                'description': 'Juego de pastillas de freno delanteras',
                'stock': 12,
                'min_stock': 3
            },
            {
                'code': 'PAST-002',
                'name': 'Pastillas de Freno Traseras',
                'description': 'Juego de pastillas de freno traseras',
                'stock': 8,
                'min_stock': 3
            },
            {
                'code': 'ACE-001',
                'name': 'Aceite Motor 15W-40',
                'description': 'Aceite mineral para motor diesel (20L)',
                'stock': 30,
                'min_stock': 10
            },
            {
                'code': 'ACE-002',
                'name': 'Aceite Motor 10W-30',
                'description': 'Aceite sintético para motor diesel (20L)',
                'stock': 18,
                'min_stock': 8
            },
            {
                'code': 'BAND-001',
                'name': 'Banda Serpentina',
                'description': 'Banda serpentina multi-accesorios',
                'stock': 6,
                'min_stock': 2
            },
            {
                'code': 'BAT-001',
                'name': 'Batería 12V 100Ah',
                'description': 'Batería libre de mantenimiento',
                'stock': 4,
                'min_stock': 2
            },
            {
                'code': 'LLANT-001',
                'name': 'Llanta 295/80R22.5',
                'description': 'Llanta para camión carga pesada',
                'stock': 16,
                'min_stock': 4
            },
            {
                'code': 'LIQ-001',
                'name': 'Líquido Refrigerante',
                'description': 'Anticongelante verde (20L)',
                'stock': 22,
                'min_stock': 8
            },
            {
                'code': 'BUJ-001',
                'name': 'Bujías Precalentamiento',
                'description': 'Juego de bujías para motor diesel',
                'stock': 3,
                'min_stock': 4
            }
        ]
        
        created = 0
        skipped = 0
        
        for part_data in sample_parts:
            # Verificar si ya existe
            existing = Part.query.filter_by(code=part_data['code']).first()
            if existing:
                print(f"⏭️  {part_data['code']} ya existe, omitiendo...")
                skipped += 1
                continue
            
            # Crear repuesto
            part = Part(
                code=part_data['code'],
                name=part_data['name'],
                description=part_data['description'],
                stock=part_data['stock'],
                min_stock=part_data['min_stock'],
                created_by=user.id
            )
            db.session.add(part)
            created += 1
            print(f"✓ Creado: {part_data['code']} - {part_data['name']}")
        
        db.session.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ Proceso completado:")
        print(f"   Repuestos creados: {created}")
        print(f"   Repuestos omitidos: {skipped}")
        print(f"   Total: {created + skipped}")
        
        # Mostrar alerta de stock bajo
        low_stock = Part.query.filter(Part.stock <= Part.min_stock).all()
        if low_stock:
            print(f"\n⚠️  Alertas de Stock Bajo ({len(low_stock)}):")
            for p in low_stock:
                print(f"   • {p.code} - {p.name}: Stock {p.stock} (Mínimo: {p.min_stock})")

if __name__ == '__main__':
    create_sample_parts()
