from django.core.management.base import BaseCommand
from django.apps import apps

Mountain = apps.get_model('CarpatiNest_app', 'Mountain')
Refuge = apps.get_model('CarpatiNest_app', 'Refuge')

class Command(BaseCommand):
    help = 'Updates the mountains in the database to keep only those with mountain shelters'

    def handle(self, *args, **kwargs):
        # Date despre refugii pentru fiecare munte
        mountain_refuges = {
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
            'Muntii Bucegi': [
                ('Refugiul Omu', 12),
                ('Refugiul Strunga', 10),
                ('Refugiul Tiganesti', 10),
                ('Refugiul Batrana', 6),
            ],
            'Muntii Rodnei': [
                ('Refugiul sub Varful Ineu', 10),
                ('Refugiul Lala', 8),
                ('Refugiul Gargalau', 8),
                ('Refugiul Puzdrele', 6),
                ('Refugiul Saua Galatului', 8),
            ],
            'Muntii Hasmas': [
                ('Refugiul Varful Lacauti', 8),
            ],
        }

        # Lista muntilor cu refugii
        mountain_names = list(mountain_refuges.keys())

        # Sterge toti muntii care nu sunt in lista
        Mountain.objects.exclude(name__in=mountain_names).delete()

        # Pentru fiecare nume de munte din listă
        for name in mountain_names:
            # Verifică dacă muntele există deja
            mountain, created = Mountain.objects.get_or_create(
                name=name,
                defaults={
                    'altitude': {
                        'Muntii Fagaras': 2544,  # Varful Moldoveanu
                        'Muntii Rodnei': 2303,   # Varful Pietrosul
                        'Muntii Bucegi': 2505,   # Varful Omu
                        'Muntii Piatra Craiului': 2238,  # Varful La Om
                        'Muntii Hasmas': 1792,   # Varful Hasmasul Mare
                    }.get(name),
                    'description': {
                        'Muntii Fagaras': 'Cel mai inalt si spectaculos masiv muntos din Carpatii Romanesti, cu numeroase trasee si refugii montane.',
                        'Muntii Rodnei': 'Cel mai inalt masiv muntos din Carpatii Orientali, cunoscut pentru peisajele alpine si biodiversitatea bogata.',
                        'Muntii Bucegi': 'Masiv muntos impresionant, celebru pentru formatiunile sale stancoase si reteaua densa de trasee turistice.',
                        'Muntii Piatra Craiului': 'Cel mai lung si mai spectaculos creasta calcaroasa din Carpatii Romanesti, paradis pentru alpinisti.',
                        'Muntii Hasmas': 'Masiv calcaros spectaculos, parte din Carpatii Orientali, cu peisaje unice si biodiversitate bogata.'
                    }.get(name)
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Adaugat muntele "{name}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Actualizat muntele "{name}"'))

            # Adaugam refugiile pentru acest munte
            if name in mountain_refuges:
                for refuge_name, capacity in mountain_refuges[name]:
                    refuge, created = Refuge.objects.update_or_create(
                        name=refuge_name,
                        mountain=mountain,
                        defaults={
                            'capacity': capacity,
                            'description': f'Refugiu montan situat in {name}.',
                            'altitude': mountain.altitude - 200  # Altitudine aproximativă
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Adaugat refugiul "{refuge_name}"'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Actualizat refugiul "{refuge_name}"'))

        self.stdout.write(self.style.SUCCESS('Actualizarea muntilor si refugiilor s-a incheiat cu succes!'))
