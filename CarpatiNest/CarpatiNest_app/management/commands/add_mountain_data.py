# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from CarpatiNest_app.models import Mountain, Refuge

class Command(BaseCommand):
    help = 'Add mountains and refuges data'

    def handle(self, *args, **kwargs):
        # Mountain altitudes
        mountain_altitudes = {
            'Muntii Fagaras': 2544,  # Varful Moldoveanu
            'Muntii Piatra Craiului': 2238,  # Varful La Om
            'Muntii Retezat': 2509,  # Varful Peleaga
            'Muntii Rodnei': 2303,  # Varful Pietrosul
            'Muntii Bucegi': 2505,  # Varful Omu
            'Muntii Parang': 2519,  # Varful Parangul Mare
            'Muntii Capatanii': 2124,  # Varful Nedeia
            'Muntii Hasmas': 1792,  # Varful Hasmasul Mare
        }

        # Mountain and refuge data
        mountains_data = {
            'Muntii Fagaras': [
                ('Refugiul Scara', 18),
                ('Refugiul Zarna', 10),
                ('Refugiul Vistea Mare', 15),
                ('Refugiul Iezer', 30),
                ('Refugiul Caltun', 22),
                ('Refugiul Turnuri', 14),
                ('Refugiul Podragu', 20),
                ('Refugiul Valea Sambetei', 14),
                ('Refugiul Balea', 10),
            ],
            'Muntii Piatra Craiului': [
                ('Refugiul Grind I', 14),
                ('Refugiul Grind II', 8),
                ('Refugiul Varful Ascutit', 8),
                ('Refugiul Saua Funduri', 6),
                ('Refugiul Diana', 8),
                ('Refugiul Sperantelor', 8),
                ('Refugiul Spirla', 8),
            ],
            'Muntii Retezat': [
                ('Refugiul Bucura', 25),
                ('Refugiul Poiana Pelegii', 15),
                ('Refugiul Buta', 15),
            ],
            'Muntii Rodnei': [
                ('Refugiul sub Varful Ineu', 10),
                ('Refugiul Lala', 8),
                ('Refugiul Gargalau', 8),
                ('Refugiul Puzdrele', 6),
                ('Refugiul Saua Galatului', 8),
            ],
            'Muntii Bucegi': [
                ('Refugiul Omu', 12),
                ('Refugiul Strunga', 10),
                ('Refugiul Tiganesti', 10),
                ('Refugiul Batrana', 6),
            ],
            'Muntii Parang': [
                ('Refugiul Carja', 16),
            ],
            'Muntii Capatanii': [
                ('Refugiul Gerea', 14),
            ],
            'Muntii Hasmas': [
                ('Refugiul Varful Lacauti', 8),
            ],
        }

        for mountain_name, refuges in mountains_data.items():
            mountain, created = Mountain.objects.get_or_create(
                name=mountain_name,
                defaults={
                    'description': f'Muntii {mountain_name.split()[1]} sunt un masiv montan din Carpatii Romanesti.',
                    'altitude': mountain_altitudes[mountain_name]
                }
            )
            status = 'Created' if created else 'Updated'
            if not created:
                mountain.altitude = mountain_altitudes[mountain_name]
                mountain.save(update_fields=['altitude'])
            self.stdout.write(self.style.SUCCESS(f'{status} mountain: {mountain_name}'))
            
            for refuge_name, capacity in refuges:
                defaults = {
                    'capacity': capacity,
                    'description': f'Refugiu montan situat in {mountain_name}.',
                    'altitude': mountain_altitudes[mountain_name] - 200  # Approximate refuge altitude
                }
                refuge, created = Refuge.objects.update_or_create(
                    name=refuge_name,
                    mountain=mountain,
                    defaults=defaults
                )
                status = 'Created' if created else 'Updated'
                self.stdout.write(self.style.SUCCESS(f'{status} refuge: {refuge_name}'))
