from django.core.management.base import BaseCommand
from CarpatiNest_app.models import Mountain

class Command(BaseCommand):
    help = 'Populate the database with Romanian mountains'

    def handle(self, *args, **options):
        mountains = [
            {"name": "Făgăraș", "altitude": 2544, "description": "Cel mai înalt și unul dintre cele mai spectaculoase masive montane din România."},
            {"name": "Piatra Craiului", "altitude": 2238, "description": "Un masiv calcaros spectaculos, cu cea mai lungă creastă calcaroasă din România."},
            {"name": "Bucegi", "altitude": 2505, "description": "Munți celebri pentru formațiunile lor stâncoase spectaculoase, inclusiv Sfinxul și Babele."},
            {"name": "Iezer-Păpușa", "altitude": 2462, "description": "Un masiv montan impresionant, cu peisaje alpine spectaculoase."},
            {"name": "Retezat", "altitude": 2509, "description": "Celebru pentru lacurile glaciare și biodiversitatea unică."},
            {"name": "Călimani", "altitude": 2100, "description": "Cel mai mare masiv vulcanic din România."},
            {"name": "Parâng", "altitude": 2519, "description": "Un masiv montan major din Carpații Meridionali."},
            {"name": "Rodnei", "altitude": 2303, "description": "Cel mai înalt masiv din Carpații Orientali."},
            {"name": "Godeanu", "altitude": 2229, "description": "Un masiv montan sălbatic cu peisaje spectaculoase."},
            {"name": "Ceahlău", "altitude": 1907, "description": "Un munte legendar, considerat sacru în folclorul românesc."},
            {"name": "Căpățânii", "altitude": 2124, "description": "Parte din Carpații Meridionali, cu peisaje diverse."},
            {"name": "Cindrel", "altitude": 2244, "description": "Munți cu relief blând și pajiști alpine extinse."},
            {"name": "Leaota", "altitude": 2133, "description": "Un masiv mai puțin cunoscut, dar cu trasee frumoase."},
            {"name": "Bihor-Vlădeasa", "altitude": 1836, "description": "Cel mai înalt masiv din Munții Apuseni."},
            {"name": "Ciucaș", "altitude": 1954, "description": "Cunoscut pentru formațiunile stâncoase spectaculoase."},
            {"name": "Baiului", "altitude": 1923, "description": "Munți accesibili, perfect pentru drumeții ușoare."},
            {"name": "Bistriței", "altitude": 1859, "description": "Munți care străjuiesc Valea Bistriței."},
            {"name": "Buzăului", "altitude": 1772, "description": "Munți cu peisaje variate și multe atracții naturale."},
            {"name": "Harghita", "altitude": 1801, "description": "Cel mai lung lanț vulcanic din Europa."},
            {"name": "Hășmaș", "altitude": 1792, "description": "Cunoscuți pentru Cheile Bicazului."},
            {"name": "Latoritei", "altitude": 2168, "description": "Un masiv montan cu văi adânci și creste înalte."},
            {"name": "Lotrului", "altitude": 2242, "description": "Munți cu peisaje alpine spectaculoase."},
            {"name": "Metaliferi", "altitude": 1437, "description": "Bogați în resurse minerale."},
            {"name": "Nemira", "altitude": 1649, "description": "Munți cu păduri dese și trasee pitorești."},
            {"name": "Penteleu", "altitude": 1772, "description": "Un masiv izolat cu peisaje sălbatice."},
            {"name": "Postăvarul", "altitude": 1799, "description": "Cunoscut pentru stațiunea Poiana Brașov."},
            {"name": "Rarău-Giumalău", "altitude": 1651, "description": "Munți cu formațiuni geologice interesante."},
            {"name": "Semenic", "altitude": 1445, "description": "Cunoscuți pentru pârtiile de schi."},
            {"name": "Siriu", "altitude": 1657, "description": "Un masiv compact cu trasee frumoase."},
            {"name": "Suhard", "altitude": 1932, "description": "Munți cu relief carstic spectaculos."},
            {"name": "Șureanu", "altitude": 2059, "description": "Bogați în vestigii dacice."},
            {"name": "Tarcău", "altitude": 1662, "description": "Munți cu păduri seculare."},
            {"name": "Țarcu", "altitude": 2190, "description": "Un masiv spectaculos din Carpații Meridionali."},
            {"name": "Tibleș", "altitude": 1839, "description": "Un masiv montan din nordul României."},
            {"name": "Trascău", "altitude": 1436, "description": "Cunoscuți pentru formațiunile carstice."},
            {"name": "Vâlcan", "altitude": 1946, "description": "Munți cu peisaje spectaculoase."},
            {"name": "Vrancei", "altitude": 1785, "description": "Zonă cunoscută pentru activitatea seismică."},
            {"name": "Zarandului", "altitude": 1111, "description": "Munți cu altitudine moderată și trasee accesibile."},
            {"name": "Baraolt", "altitude": 1017, "description": "Munți cu relief domol și păduri dese."},
            {"name": "Bodoc", "altitude": 1193, "description": "Un lanț muntos din Carpații de Curbură."},
            {"name": "Brețcu", "altitude": 1198, "description": "Munți care fac parte din Carpații Orientali."},
            {"name": "Turiei", "altitude": 1288, "description": "Un masiv mai puțin cunoscut din Carpații Orientali."},
        ]

        for mountain_data in mountains:
            Mountain.objects.get_or_create(
                name=mountain_data["name"],
                defaults={
                    "altitude": mountain_data["altitude"],
                    "description": mountain_data["description"]
                }
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully populated mountains database'))
