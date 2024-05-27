from django.contrib import admin
from .models import Music
from listening.models import MusicListening
class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release', 'artist_name', 'year','youtube_id',)
    search_fields = ('title', 'artist_name')
    list_filter = ('release', 'year')

class MusicListeningAdmin(admin.ModelAdmin):
    list_display = ('listener', 'music', 'listen_count')
    list_filter = ('listener', 'music')

admin.site.register(Music, MusicAdmin)
admin.site.register(MusicListening, MusicListeningAdmin)