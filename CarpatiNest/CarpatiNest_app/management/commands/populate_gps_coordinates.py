from django.core.management.base import BaseCommand
from CarpatiNest_app.models import Refuge


class Command(BaseCommand):
    help = 'Populează coordonatele GPS pentru refugiile din Carpați'
    
    def handle(self, *args, **options):
        # Dicționar cu coordonatele GPS pentru refugiile cunoscute din Carpați
        refuge_coordinates = {
            # Munții Bucegi
            'Omu': {'lat': 45.4236, 'lon': 25.4564},
            'Refugiul Omu': {'lat': 45.4236, 'lon': 25.4564},
            'Caraiman': {'lat': 45.4167, 'lon': 25.4667},
            'Malaiesti': {'lat': 45.3833, 'lon': 25.4833},
            'Pestera': {'lat': 45.3981, 'lon': 25.4456},
            
            # Munții Piatra Craiului
            'Piatra Craiului': {'lat': 45.5167, 'lon': 25.2167},
            'Curmatura': {'lat': 45.5083, 'lon': 25.2083},
            'Diana': {'lat': 45.5333, 'lon': 25.1833},
            
            # Munții Postăvaru
            'Postavaru': {'lat': 45.6167, 'lon': 25.5833},
            'Cristianul Mare': {'lat': 45.6083, 'lon': 25.5667},
            
            # Munții Fagaras
            'Negoiu': {'lat': 45.6028, 'lon': 24.5575},
            'Moldoveanu': {'lat': 45.6031, 'lon': 24.7369},
            'Podragu': {'lat': 45.6167, 'lon': 24.6167},
            'Barcaciu': {'lat': 45.5833, 'lon': 24.5167},
            'Doamnei': {'lat': 45.5667, 'lon': 24.5833},
            'Serbota': {'lat': 45.5833, 'lon': 24.4833},
            
            # Munții Retezat
            'Gura Zlata': {'lat': 45.3667, 'lon': 22.8833},
            'Pietrele': {'lat': 45.3833, 'lon': 22.8667},
            'Gentiana': {'lat': 45.3500, 'lon': 22.8833},
            
            # Munții Parâng
            'Parang': {'lat': 45.3333, 'lon': 23.6167},
            'Cuntu': {'lat': 45.3167, 'lon': 23.6333},
            
            # Munții Ceahlău
            'Ceahlau': {'lat': 46.9667, 'lon': 25.9333},
            'Dochia': {'lat': 46.9500, 'lon': 25.9167},
            
            # Munții Rodna
            'Borsa': {'lat': 47.6583, 'lon': 24.6639},
            'Iezer': {'lat': 47.6333, 'lon': 24.6167},
            
            # Munții Maramures
            'Creasta Cocosului': {'lat': 47.7167, 'lon': 24.5833},
            'Pop Ivan': {'lat': 47.9333, 'lon': 24.6167},
        }
        
        updated_count = 0
        not_found_count = 0
        
        self.stdout.write("Începem actualizarea coordonatelor GPS...")
        
        for refuge in Refuge.objects.all():
            refuge_name = refuge.name.strip()
            coordinates_found = False
            
            # Căutăm o potrivire exactă sau parțială
            for name_pattern, coords in refuge_coordinates.items():
                if (name_pattern.lower() in refuge_name.lower() or 
                    refuge_name.lower() in name_pattern.lower()):
                    
                    refuge.latitude = coords['lat']
                    refuge.longitude = coords['lon']
                    refuge.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Actualizat: {refuge_name} -> '
                            f'Lat: {coords["lat"]}, Lon: {coords["lon"]}'
                        )
                    )
                    updated_count += 1
                    coordinates_found = True
                    break
            
            if not coordinates_found:
                self.stdout.write(
                    self.style.WARNING(
                        f'Coordonate negăsite pentru: {refuge_name}'
                    )
                )
                not_found_count += 1
        
        # Adăugăm coordonate generale pentru refugiile rămase
        for refuge in Refuge.objects.filter(latitude__isnull=True, longitude__isnull=True):
            refuge.latitude = 45.5000  
            refuge.longitude = 25.0000
            refuge.save()
            
            self.stdout.write(
                self.style.WARNING(
                    f'Coordonate generale adăugate pentru: {refuge.name}'
                )
            )
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Refugii actualizate: {updated_count}'
            )
        )
        
        self.stdout.write(
            self.style.SUCCESS('Coordonatele GPS au fost actualizate cu succes!')
        )
