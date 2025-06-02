from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.db.models import Avg
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
    available_spots = refuge.get_available_spots(today)
    
    if request.method == 'POST':
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
        else:
            booking_form = BookingForm(request.POST, refuge=refuge)
            booking_form.refuge_instance = refuge  # Setăm refugiul pentru validare
            if booking_form.is_valid():
                booking_date = booking_form.cleaned_data.get('booking_date')
                members_count = booking_form.cleaned_data.get('members_count')
                
                # Verifică disponibilitatea în ziua selectată
                available_on_selected_date = refuge.get_available_spots(booking_date)
                
                # Verifică dacă există suficiente locuri disponibile pentru numărul de membri
                if members_count > available_on_selected_date:
                    booking_form.add_error('members_count', f'Nu sunt suficiente locuri disponibile pentru data selectată. Locuri disponibile: {available_on_selected_date}')
                elif available_on_selected_date == 0:
                    booking_form.add_error('booking_date', 'Nu mai sunt locuri disponibile pentru această dată!')
                else:
                    booking = booking_form.save(commit=False)
                    booking.user = request.user
                    booking.refuge = refuge
                    booking.save()
                    
                    # Verifică dacă au mai rămas locuri disponibile după scăderea celor rezervate
                    if available_on_selected_date - members_count == 0:
                        messages.info(request, 'Ai rezervat ultimele locuri disponibile pentru această dată!')
                    
                    messages.success(request, 'Rezervarea a fost creată cu succes!')
                    
                    # Dacă cererea este AJAX, returnează un răspuns JSON
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': True, 'message': 'Rezervarea a fost creată cu succes!'})
                    
                    return redirect('CarpatiNest_app:mountain_refuges', mountain_id=refuge.mountain.id)
            review_form = ReviewForm(instance=user_review)
    else:
        booking_form = BookingForm(initial={'refuge': refuge})
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
            available_spots = refuge.get_available_spots(booking_date)
            
            return JsonResponse({
                'refuge_id': refuge_id,
                'date': date_str,
                'available_spots': available_spots,
                'is_available': available_spots > 0
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Metoda nepermisă'}, status=405)