from django.contrib import admin
from .models import Mountain, Refuge, Booking, RefugeImage, Review

class RefugeImageInline(admin.TabularInline):
    model = RefugeImage
    extra = 1

class RefugeAdmin(admin.ModelAdmin):
    inlines = [RefugeImageInline]
    list_display = ('name', 'mountain', 'altitude', 'capacity')
    list_filter = ('mountain',)
    search_fields = ('name', 'description')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('refuge', 'user', 'rating', 'created_at')
    list_filter = ('refuge', 'rating')
    search_fields = ('comment', 'user__username')
    readonly_fields = ('created_at',)

admin.site.register(Mountain)
admin.site.register(Refuge, RefugeAdmin)
admin.site.register(Booking)
admin.site.register(Review, ReviewAdmin)
