from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_booking_confirmation_email(booking):
    """
    Trimite un email de confirmare utilizatorului după ce a efectuat o rezervare.
    
    Args:
        booking: Instanța obiectului Booking care tocmai a fost creat
    """
    # Verificăm că booking-ul are toate informațiile necesare
    if not booking or not hasattr(booking, 'refuge') or not booking.refuge:
        print("ERROR: Booking sau refuge lipsește")
        return False
        
    if not hasattr(booking, 'user') or not booking.user or not booking.user.email:
        print("ERROR: User sau email lipsește")
        return False
    
    # Construiește subiectul emailului
    subject = f'Confirmare rezervare - {booking.refuge.name}'
    
    # Adresa de la care se trimite emailul
    from_email = settings.DEFAULT_FROM_EMAIL
    if not from_email:
        print("WARNING: DEFAULT_FROM_EMAIL nu este configurat, se folosește valoarea implicită")
        from_email = 'noreply@carpatinest.ro'
    
    # Adresa de email a destinatarului
    to_email = booking.user.email
    
    # Obține domeniul site-ului pentru link-uri
    from django.contrib.sites.shortcuts import get_current_site
    from django.http import HttpRequest
    
    # Creăm un request fals pentru a putea folosi get_current_site
    request = HttpRequest()
    request.META['SERVER_NAME'] = 'localhost'
    request.META['SERVER_PORT'] = '8000'
      # Construim URL-ul de bază
    try:
        site = get_current_site(request)
        protocol = 'http' if settings.DEBUG else 'https'
        site_url = f"{protocol}://{site.domain}"
    except Exception as e:
        print(f"ERROR la construirea site_url: {e}")
        site_url = "http://localhost:8000"
    
    # Context pentru template-ul de email
    context = {
        'booking': booking,
        'user': booking.user,
        'refuge': booking.refuge,
        'mountain': booking.refuge.mountain,
        'site_url': site_url,
    }
    
    # Render template-ul HTML pentru email
    html_content = render_to_string('emails/booking_confirmation.html', context)
    
    # Versiunea text simplu a emailului (pentru clienții care nu pot afișa HTML)
    text_content = strip_tags(html_content)
    
    # Creează mesajul email
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    
    # Adaugă versiunea HTML
    email.attach_alternative(html_content, "text/html")
    
    # Trimite emailul
    email.send()
    
    return True
