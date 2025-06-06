from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import sys

class Command(BaseCommand):
    help = 'Trimite un email de test pentru a verifica configurația email'

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str, help='Adresa de email a destinatarului')

    def handle(self, *args, **options):
        recipient = options['recipient']
        subject = 'Test email CarpatiNest'
        message = """
Acesta este un email de test trimis din aplicația CarpatiNest.

Dacă primești acest email, înseamnă că configurația SMTP pentru Gmail funcționează corect.

Cu drag,
Echipa CarpatiNest
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        
        self.stdout.write(f"Se trimite email de test către {recipient}...")
        
        try:
            result = send_mail(
                subject,
                message,
                from_email,
                [recipient],
                fail_silently=False,
            )
            
            if result:
                self.stdout.write(self.style.SUCCESS(f'Email-ul de test a fost trimis cu succes către {recipient}!'))
            else:
                self.stdout.write(self.style.ERROR('Nu s-a putut trimite email-ul de test.'))
                
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Eroare la trimiterea email-ului: {str(e)}'))
            self.stderr.write(self.style.ERROR('Asigură-te că ai configurat corect setările de email în settings.py'))
            sys.exit(1)
