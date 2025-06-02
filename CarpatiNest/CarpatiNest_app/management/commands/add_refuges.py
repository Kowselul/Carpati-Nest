from django.core.management.base import BaseCommand
from CarpatiNest_app.models import Mountain, Refuge

class Command(BaseCommand):
    help = 'Adds all mountain refuges to the database'

    def handle(self, *args, **kwargs):
        # Dicționar cu refugiile pentru fiecare munte
        mountain_refuges = {
            'Munții Făgăraș': [
                'Refugiul Scara',
                'Refugiul Cațaveiu',
                'Refugiul Viștea Mare',
                'Refugiul Zârna',
                'Refugiul Iezer',
                'Refugiul Călțun',
                'Refugiul Turnuri',
                'Refugiul Podragu',
                'Refugiul Valea Sâmbetei',
                'Refugiul Bâlea',
            ],
            'Munții Rodnei': [
                'Refugiul de sub Vârful Ineu',
                'Refugiul Lala',
                'Refugiul Gărgălău',
                'Refugiul Puzdrele',
                'Refugiul Șaua Galațului',
                'Refugiul Șaua Obârșia Rebrii',
            ],
            'Munții Bucegi': [
                'Refugiul Șaua Țigănești',
                'Refugiul Strunga',
                'Refugiul Țigănești',
                'Refugiul Bătrâna',
                'Refugiul Omu',
                'Refugiul Salvamont Mălăiești',
            ],
            'Munții Piatra Craiului': [
                'Refugiul Diana',
                'Refugiul Speranțelor',
                'Refugiul Lehmann (Vârful Ascuțit)',
                'Refugiul Grind 1',
                'Refugiul Grind 2 (Șaua Grindului)',
                'Refugiul Șaua Funduri',
                'Refugiul Șpirla',
            ],
            'Munții Cindrel': [
                'Refugiul Cindrel',
            ],
            'Munții Hășmaș': [
                'Refugiul panoramic de pe Vârful Ucigașul (Ghilcoș)',
            ],
        }

        # Șterge toate refugiile existente
        Refuge.objects.all().delete()

        # Adaugă refugiile pentru fiecare munte
        for mountain_name, refuges in mountain_refuges.items():
            try:
                mountain = Mountain.objects.get(name=mountain_name)
                for refuge_name in refuges:
                    refuge = Refuge.objects.create(
                        name=refuge_name,
                        mountain=mountain,
                        description=f'Refugiu montan în {mountain.name}'
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Adăugat refugiul "{refuge_name}" în {mountain_name}'
                        )
                    )
            except Mountain.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'Muntele "{mountain_name}" nu există în baza de date'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS('Toate refugiile au fost adăugate cu succes!')
        )
