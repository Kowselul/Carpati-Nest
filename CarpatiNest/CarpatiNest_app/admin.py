from django.contrib import admin
from django.contrib import messages
from .models import Mountain, Refuge, Booking, RefugeImage, Review

class RefugeImageInline(admin.TabularInline):
    model = RefugeImage
    extra = 1

class RefugeAdmin(admin.ModelAdmin):
    inlines = [RefugeImageInline]
    list_display = ('name', 'mountain', 'altitude', 'capacity', 'latitude', 'longitude', 'has_gps_coordinates')
    list_filter = ('mountain',)
    search_fields = ('name', 'description')
    
    fieldsets = (
        ('Informații generale', {
            'fields': ('name', 'mountain', 'description', 'altitude', 'capacity', 'price_per_night')
        }),
        ('Locație GPS', {
            'fields': ('latitude', 'longitude'),
            'description': 'Coordonatele GPS sunt necesare pentru afișarea vremii. '
                          'Introduceți latitudinea și longitudinea în format decimal (ex: 45.4236, 25.4564)'
        }),
        ('Contact și facilități', {
            'fields': ('contact_info', 'facilities'),
            'classes': ('collapse',)
        }),    )
    
    def has_gps_coordinates(self, obj):
        """Indică dacă refugiul are coordonate GPS completate"""
        return bool(obj.latitude and obj.longitude)
    has_gps_coordinates.boolean = True
    has_gps_coordinates.short_description = 'GPS Configurat'
    
    actions = ['populate_gps_coordinates']
    
    def populate_gps_coordinates(self, request, queryset):
        """Populează coordonatele GPS pentru refugiile selectate"""
        # Dicționar cu coordonatele GPS pentru refugiile cunoscute din Carpați
        refuge_coordinates = {
            'Omu': [45.4236, 25.4564], 'Caraiman': [45.4167, 25.4667],
            'Malaiesti': [45.3833, 25.4833], 'Pestera': [45.3981, 25.4456],
            'Piatra Craiului': [45.5167, 25.2167], 'Curmatura': [45.5083, 25.2083],
            'Diana': [45.5333, 25.1833], 'Postavaru': [45.6167, 25.5833],
            'Negoiu': [45.6028, 24.5575], 'Moldoveanu': [45.6031, 24.7369],
            'Podragu': [45.6167, 24.6167], 'Barcaciu': [45.5833, 24.5167],
            'Doamnei': [45.5667, 24.5833], 'Serbota': [45.5833, 24.4833],
            'Gura Zlata': [45.3667, 22.8833], 'Pietrele': [45.3833, 22.8667],
            'Gentiana': [45.3500, 22.8833], 'Parang': [45.3333, 23.6167],
            'Ceahlau': [46.9667, 25.9333], 'Dochia': [46.9500, 25.9167],
            'Borsa': [47.6583, 24.6639], 'Iezer': [47.6333, 24.6167]
        }
        
        updated_count = 0
        for refuge in queryset:
            found = False
            for name_pattern, coords in refuge_coordinates.items():
                if name_pattern.lower() in refuge.name.lower():
                    refuge.latitude = coords[0]
                    refuge.longitude = coords[1]
                    refuge.save()
                    updated_count += 1
                    found = True
                    break
            
            if not found and not refuge.latitude:
                # Coordonate generale pentru zona centrală a Carpaților
                refuge.latitude = 45.5000
                refuge.longitude = 25.0000
                refuge.save()
                updated_count += 1
        
        messages.success(
            request, 
            f'Coordonatele GPS au fost actualizate pentru {updated_count} refugii.'
        )
    
    populate_gps_coordinates.short_description = "Populează coordonatele GPS pentru refugiile selectate"

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('refuge', 'user', 'rating', 'created_at')
    list_filter = ('refuge', 'rating')
    search_fields = ('comment', 'user__username')
    readonly_fields = ('created_at',)

admin.site.register(Mountain)
admin.site.register(Refuge, RefugeAdmin)
admin.site.register(Booking)
admin.site.register(Review, ReviewAdmin)
