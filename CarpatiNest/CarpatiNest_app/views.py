from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.db.models import Avg
from django.urls import reverse
from django.core.exceptions import ValidationError
from .forms import PersonalInfoForm, EmailChangeForm, CustomPasswordChangeForm, CustomAuthenticationForm, CustomRegistrationForm, CustomLoginForm, AccountSettingsForm, BookingForm, ReviewForm
from .models import Mountain, Refuge, Booking, Review
from datetime import date
import random

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm

def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cont creat cu succes! Te poți autentifica acum.')
            return redirect('CarpatiNest_app:login')
    else:
        form = CustomRegistrationForm()
    return render(request, 'register.html', {'form': form})

def index(request):
    return render(request, 'index.html')

@login_required
def account_settings(request):
    if request.method == 'POST':
        if 'personal_info' in request.POST:
            personal_form = PersonalInfoForm(request.POST, instance=request.user)
            if personal_form.is_valid():
                personal_form.save()
                messages.success(request, 'Informațiile personale au fost actualizate cu succes.')
                return redirect('CarpatiNest_app:account_settings')
            
        elif 'email_change' in request.POST:
            email_form = EmailChangeForm(request.POST)
            if email_form.is_valid():
                request.user.email = email_form.cleaned_data['email']
                request.user.save()
                messages.success(request, 'Adresa de email a fost actualizată cu succes.')
                return redirect('CarpatiNest_app:account_settings')
            
        elif 'password_change' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Parola a fost schimbată cu succes.')
                return redirect('CarpatiNest_app:account_settings')
    else:
        personal_form = PersonalInfoForm(instance=request.user)
        email_form = EmailChangeForm()
        password_form = CustomPasswordChangeForm(request.user)
    
    context = {
        'personal_form': personal_form,
        'email_form': email_form,
        'password_form': password_form,
        'current_email': request.user.email
    }
    return render(request, 'account_settings.html', context)

@login_required
def mountain_selection(request):
    mountains = Mountain.objects.all()
    context = {
        'mountains': mountains
    }
    return render(request, 'mountains.html', context)

@login_required
def mountain_refuges(request, mountain_id):
    mountain = get_object_or_404(Mountain, id=mountain_id)
    refuges = Refuge.objects.filter(mountain=mountain)
    context = {
        'mountain': mountain,
        'refuges': refuges
    }
    return render(request, 'refuges.html', context)

@login_required
def booking_view(request, refuge_id):
    refuge = get_object_or_404(Refuge, id=refuge_id)
    reviews = Review.objects.filter(refuge=refuge).select_related('user')
    user_review = Review.objects.filter(refuge=refuge, user=request.user).first() if request.user.is_authenticated else None
    
    # Calculează locurile disponibile pentru data curentă
    today = date.today()
    
    # Calculează direct locurile disponibile pentru data curentă
    bookings_today = Booking.objects.filter(
        refuge=refuge,
        booking_date=today,
        status__in=['pending', 'confirmed']
    )
    reserved_spots_today = sum(booking.members_count for booking in bookings_today)
    available_spots = max(0, refuge.capacity - reserved_spots_today)
    
    if request.method == 'POST':
        # Procesare recenzii - această ramură nu ar trebui să conducă la duplicarea rezervărilor
        if 'review_form' in request.POST:
            review_form = ReviewForm(request.POST, instance=user_review)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.refuge = refuge
                review.save()
                messages.success(request, 'Recenzia a fost adăugată cu succes!')
                return redirect('CarpatiNest_app:booking', refuge_id=refuge.id)
            booking_form = BookingForm(refuge=refuge)
        
        # Procesare rezervări
        else:
            # Verificăm dacă este cerere AJAX pentru a preveni dublarea rezervărilor
            is_ajax_request = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            booking_form = BookingForm(request.POST, refuge=refuge)
            if booking_form.is_valid():
                booking_date = booking_form.cleaned_data.get('booking_date')
                members_count = booking_form.cleaned_data.get('members_count')
                
                # Import tranzacții pentru a asigura atomicitatea operațiunilor
                from django.db import transaction
                
                try:
                    # Folosim tranzacții pentru a preveni race condition-uri și inconsistența datelor
                    with transaction.atomic():
                        # Verificăm din nou locurile disponibile în interiorul tranzacției
                        # pentru a avea cea mai actualizată stare a datelor
                        bookings_for_date = Booking.objects.filter(
                            refuge=refuge,
                            booking_date=booking_date,
                            status__in=['pending', 'confirmed']
                        ).select_for_update()  # Adăugăm select_for_update pentru a bloca rândurile pe durata tranzacției
                        
                        reserved_spots = sum(booking.members_count for booking in bookings_for_date)
                        available_on_selected_date = max(0, refuge.capacity - reserved_spots)
                        
                        # Verificăm din nou disponibilitatea în interiorul tranzacției
                        if members_count > available_on_selected_date:
                            booking_form.add_error('members_count', 
                                f'Nu sunt suficiente locuri disponibile pentru data selectată. Locuri disponibile: {available_on_selected_date}')
                            raise ValidationError('Numărul de membri depășește locurile disponibile.')
                        
                        elif available_on_selected_date == 0:
                            booking_form.add_error('booking_date', 'Nu mai sunt locuri disponibile pentru această dată!')
                            raise ValidationError('Nu mai sunt locuri disponibile pentru această dată.')
                        
                        # Verificăm existența unei rezervări identice pentru același utilizator, refugiu și dată
                        existing_booking = Booking.objects.filter(
                            user=request.user,
                            refuge=refuge,
                            booking_date=booking_date,
                            status__in=['pending', 'confirmed']
                        ).first()
                        
                        if existing_booking:
                            # Deja există o rezervare, o folosim pe cea existentă
                            booking = existing_booking
                            messages.info(request, 'Rezervarea ta există deja.')
                            # Nu scădem din nou locurile disponibile, deoarece rezervarea există deja
                            remaining_spots = available_on_selected_date
                        else:
                            # Nu există, creăm o nouă rezervare
                            booking = booking_form.save(commit=False)
                            booking.user = request.user
                            booking.refuge = refuge
                            booking.save()
                              # Calculează locurile disponibile după această rezervare
                            remaining_spots = available_on_selected_date - members_count
                            
                            # Verifică dacă au mai rămas locuri disponibile după scăderea celor rezervate
                            if remaining_spots == 0:
                                messages.info(request, 'Ai rezervat ultimele locuri disponibile pentru această dată!')
                            messages.success(request, 'Rezervarea a fost creată cu succes!')
                
                    # Generăm URL-ul pentru redirecționare
                    redirect_url = request.build_absolute_uri(
                        reverse('CarpatiNest_app:booking_confirmation', kwargs={'booking_id': booking.id})
                    )
                    
                    # Răspuns pentru cereri AJAX
                    if is_ajax_request:
                        return JsonResponse({
                            'success': True, 
                            'message': 'Rezervarea a fost creată cu succes!',
                            'available_spots': remaining_spots,
                            'redirect_url': redirect_url
                        }, status=201)  # 201 Created pentru a indica succes
                    
                    # Redirectionare standard pentru cereri non-AJAX
                    return redirect('CarpatiNest_app:booking_confirmation', booking_id=booking.id)
                    
                except ValidationError as e:
                    # Gestionăm erorile de validare
                    error_message = str(e)
                    
                    # Răspuns pentru cereri AJAX
                    if is_ajax_request:
                        return JsonResponse({
                            'success': False,
                            'error': error_message
                        }, status=400)  # 400 Bad Request
                    else:
                        # Pentru cereri non-AJAX, afișăm mesaj de eroare și reîncărcăm pagina
                        messages.error(request, error_message)
                        return redirect('CarpatiNest_app:booking', refuge_id=refuge.id)
                
                except Exception as e:
                    # Gestionăm orice alte excepții neașteptate
                    error_message = f"A apărut o eroare neașteptată: {str(e)}"
                    
                    # Răspuns pentru cereri AJAX
                    if is_ajax_request:
                        return JsonResponse({
                            'success': False,
                            'error': error_message
                        }, status=500)  # 500 Internal Server Error
                    else:
                        # Pentru cereri non-AJAX
                        messages.error(request, error_message)
                        return redirect('CarpatiNest_app:booking', refuge_id=refuge.id)
            
            # Dacă formularul nu este valid, pregătim răspunsul adecvat
            else:
                if is_ajax_request:
                    errors = {field: [str(error) for error in errors_list] for field, errors_list in booking_form.errors.items()}
                    return JsonResponse({
                        'success': False,
                        'errors': errors
                    }, status=400)
                    
            # Inițializăm formularul pentru recenzii
            review_form = ReviewForm(instance=user_review)
    else:
        booking_form = BookingForm(refuge=refuge)
        review_form = ReviewForm(instance=user_review)
    
    # Calculează media rating-urilor
    average_rating = reviews.values_list('rating', flat=True).aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'refuge': refuge,
        'form': booking_form,
        'review_form': review_form,
        'reviews': reviews,
        'user_review': user_review,
        'average_rating': average_rating,
        'total_reviews': reviews.count(),
        'available_spots': available_spots  # Adăugare locuri disponibile în context
    }
    return render(request, 'booking.html', context)

@login_required
def booking_confirmation(request, booking_id):
    """
    Pagină de confirmare după efectuarea unei rezervări
    """
    try:
        # Verificăm că utilizatorul poate vedea doar rezervările proprii
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        # Verificăm dacă rezervarea nu a fost anulată
        if booking.status == 'canceled':
            messages.error(request, 'Această rezervare a fost anulată.')
            return redirect('CarpatiNest_app:my_bookings')
        
        # Stocăm în sesiune că această rezervare a fost deja afișată 
        # pentru a preveni retrimiterea formularului la reîmprospătarea paginii
        booking_session_key = f"booking_{booking.refuge.id}_{booking.user.id}_{request.session.session_key}"
        request.session[booking_session_key] = True
        
        context = {
            'booking': booking
        }
        return render(request, 'booking_confirmation.html', context)
    except Booking.DoesNotExist:
        messages.error(request, 'Rezervarea nu a fost găsită sau nu aveți permisiunea să o accesați.')
        return redirect('CarpatiNest_app:mountain_selection')
    except Exception as e:
        messages.error(request, f'A apărut o eroare: {str(e)}')
        return redirect('CarpatiNest_app:mountain_selection')

@login_required
def my_bookings(request):
    """
    Pagină pentru vizualizarea tuturor rezervărilor unui utilizator
    """
    today = date.today()
    
    # Obține rezervările active (cele care nu sunt anulate și data este în viitor sau azi)
    active_bookings = Booking.objects.filter(
        user=request.user,
        booking_date__gte=today,
        status__in=['pending', 'confirmed']
    ).order_by('booking_date').select_related('refuge', 'refuge__mountain')
    
    # Obține rezervările trecute (data este în trecut)
    past_bookings = Booking.objects.filter(
        user=request.user,
        booking_date__lt=today
    ).order_by('-booking_date').select_related('refuge', 'refuge__mountain')
    
    # Adaugă pentru fiecare rezervare un flag care indică dacă utilizatorul a lăsat un review
    for booking in past_bookings:
        booking.reviewed = Review.objects.filter(
            user=request.user,
            refuge=booking.refuge
        ).exists()
    
    context = {
        'bookings': active_bookings,
        'past_bookings': past_bookings,
        'today': today,
    }
    return render(request, 'my_bookings.html', context)

@login_required
def cancel_booking(request, booking_id):
    """
    Anulează o rezervare existentă
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Verifică dacă rezervarea poate fi anulată (nu este deja anulată și data nu a trecut)
    if booking.status != 'canceled' and booking.booking_date >= date.today():
        booking.status = 'canceled'
        booking.save()
        messages.success(request, 'Rezervarea a fost anulată cu succes.')
    else:
        messages.error(request, 'Rezervarea nu poate fi anulată.')
        
    return redirect('CarpatiNest_app:my_bookings')

def check_availability(request):
    """
    API endpoint pentru verificarea disponibilității pentru o anumită dată și refugiu
    """
    if request.method == 'GET':
        refuge_id = request.GET.get('refuge_id')
        date_str = request.GET.get('date')
        
        if not refuge_id or not date_str:
            return JsonResponse({'error': 'Parametri lipsă'}, status=400)
        
        try:
            # Convertește string-ul de dată în obiect date
            booking_date = date.fromisoformat(date_str)
            
            refuge = get_object_or_404(Refuge, id=refuge_id)
            
            # Calculează locurile disponibile
            bookings_for_date = Booking.objects.filter(
                refuge=refuge,
                booking_date=booking_date,
                status__in=['pending', 'confirmed']
            )
            
            reserved_spots = sum(booking.members_count for booking in bookings_for_date)
            available_spots = max(0, refuge.capacity - reserved_spots)
            
            return JsonResponse({
                'refuge_id': refuge_id,
                'date': date_str,
                'available_spots': available_spots,
                'is_available': available_spots > 0
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Metoda nepermisă'}, status=405)