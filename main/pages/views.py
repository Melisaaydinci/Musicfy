from django.shortcuts import render,redirect
from music.models import Music
from user.models import CustomUser
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from user.form import LoginForm,RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from django.http import JsonResponse
import pandas as pd
from listening.models import MusicListening
from django.db.models import Q
from .controller import get_id
from .recommendation import create_popularity_recommendation,user_based_recommendation
from user.models import CustomUser


def bring_youtube_id(all_musics):
    for music in all_musics:
        if music.youtube_id is None or music.youtube_id == '':
            youtube_id = get_id(music.title + ' ' + music.artist_name + ' ' + music.release)
            music.youtube_id = youtube_id
            music.save()

def home_page(request):
    """ Popular based recommendation"""

    all_listenings=MusicListening.objects.all()
    df_listenings = pd.DataFrame(list(all_listenings.values()))
    popular_music_ids=create_popularity_recommendation(df_listenings,7)
    popular_musics = Music.objects.filter(id__in=popular_music_ids)
    popular_musics = sorted(popular_musics, key=lambda x: popular_music_ids.index(x.id))
    """"""
    

    all_musics=Music.objects.all()[:15] 
    playlist_own_id=list(Music.objects.all()[6:15].values_list('id', flat=True))
    playlist_id=list(Music.objects.all()[6:15].values_list('youtube_id', flat=True))
    playlist_title=list(Music.objects.all()[6:15].values_list('title', flat=True))
    playlist_release=list(Music.objects.all()[6:15].values_list('release', flat=True))
    playlist_own_id = json.dumps(playlist_own_id)
    playlist_id = json.dumps(playlist_id)
    playlist_title = json.dumps(playlist_title)
    playlist_release= json.dumps(playlist_release)
    musics = Music.objects.all()[:5]
    recommended_musics=musics
    if request.user.is_authenticated:
        user= CustomUser.objects.get(username= request.user.username)     
        favorite_musics = user.favorites.all().values_list('id', flat=True)
    else:
        favorite_musics = []
    
    """api yoksa burayı kapa"""
    bring_youtube_id(all_musics)
    bring_youtube_id(popular_musics)
    bring_youtube_id(recommended_musics)

    context={
        'musics':musics,
        'popular_musics':popular_musics,
        'recommended_musics':recommended_musics,
        'favorite_musics':favorite_musics,
        'playlist_id':playlist_id,
        'playlist_title':playlist_title,
        'playlist_release':playlist_release,
        'playlist_own_id':playlist_own_id
    }
    return render(request,'index.html',context)

def music_page(request,music_id):
    only_music = Music.objects.get(id=music_id)
    if request.method=="GET":
            if request.user.is_authenticated:
                user= CustomUser.objects.get(username= request.user.username)
                listening_exists = MusicListening.objects.filter(listener=user, music=only_music).exists()
        
                # Eğer böyle bir öge yoksa, yeni bir öge oluştur
                if not listening_exists:
                    listening = MusicListening(listener=user, music=only_music)
                    listening.save()
                else:
                        listening=MusicListening.objects.get(listener=user,music=only_music)
                        listening.increment_listen_count()
                        
                
        #Favorites.objects.filter(user=request.user).values_list('camp__slug', flat=True)
    playlist_own_id=list(Music.objects.all()[6:15].values_list('id', flat=True))
    playlist_id=list(Music.objects.all()[6:15].values_list('youtube_id', flat=True))
    playlist_title=list(Music.objects.all()[6:15].values_list('title', flat=True))
    playlist_release=list(Music.objects.all()[6:15].values_list('release', flat=True))
    playlist_id = json.dumps(playlist_id)
    playlist_title = json.dumps(playlist_title)
    playlist_release= json.dumps(playlist_release)
    playlist_own_id=json.dumps(playlist_own_id)
    if request.user.is_authenticated:
        user= CustomUser.objects.get(username= request.user.username)
        favorite_musics = user.favorites.all().values_list('id', flat=True)
        #Favorites.objects.filter(user=request.user).values_list('camp__slug', flat=True)
    else:
        favorite_musics = []
    context={
        'only_music':only_music,
        'favorite_musics':favorite_musics,
        'playlist_id':playlist_id,
        'playlist_title':playlist_title,
        'playlist_release':playlist_release,
        'playlist_own_id':playlist_own_id
    }
    return render(request,'music_play.html',context)

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('Username')
            password = form.cleaned_data.get('Password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    auth_login(request, user)
                
                    user= CustomUser.objects.get(username= request.user.username)
                    if not user.is_staff:
                        """User based recommendation"""
                        """Kapatmak istersen alttakileri sil"""
                        
                        print("kullanıcının id si",user.id)
                        recommend=user_based_recommendation(user.id,5)
                        user_based_ids=recommend['song'].tolist()
                        recommended_musics = Music.objects.filter(title__in=user_based_ids)
            
                    return redirect('home_page')
            else:
                form.add_error(None, "Kullanıcı adı veya şifre hatalı.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
 
def signup_page(request):   
    if request.method == 'POST':
        print("posta giriyorum")
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("user özellikleri",user)
            auth_login(request, user)
            # Başarılı kayıt yapıldıktan sonra yönlendirme yapılabilir veya başka bir işlem gerçekleştirilebilir
            return redirect('home_page')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})
    

@login_required
def logout_page(request):
    logout(request)
    return redirect('home_page')


@login_required
def favorite_page(request):
    user= CustomUser.objects.get(username= request.user.username)
    favorite_musics = user.favorites.all()
    playlist_own_id=list(Music.objects.all()[6:15].values_list('id', flat=True))
    playlist_id=list(Music.objects.all()[6:15].values_list('youtube_id', flat=True))
    playlist_title=list(Music.objects.all()[6:15].values_list('title', flat=True))
    playlist_release=list(Music.objects.all()[6:15].values_list('release', flat=True))
    playlist_own_id=json.dumps(playlist_own_id)
    playlist_id = json.dumps(playlist_id)
    playlist_title = json.dumps(playlist_title)
    playlist_release= json.dumps(playlist_release)
    context={
        'favorite_musics':favorite_musics,
        'playlist_id':playlist_id,
        'playlist_title':playlist_title,
        'playlist_release':playlist_release,
        'playlist_own_id':playlist_own_id
    }
    return render(request,'favorites.html',context=context)

@login_required
def profile_page(request):
    user= CustomUser.objects.get(username= request.user.username)
    context={
        'user':user,
    }
    return render(request,'profile.html',context=context)

@login_required
def add_or_remove_favorite(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body) 
        music_slug= data.get('music_slug')
        music = Music.objects.get(id=music_slug)
        user= CustomUser.objects.get(username= request.user.username)
        if music in user.favorites.all():
            user.favorites.remove(music)
            music.decrement_favorite_count()
            return JsonResponse({'status': 'removed'})
        else:
            user.favorites.add(music)
            music.increment_favorite_count()
            return JsonResponse({'status': 'added'})
    return JsonResponse({'status': 'error'})

@login_required
def listen_music(request):
    if request.method=="POST":
        music_id = request.POST.get('music_id')
        music = Music.objects.get(id=music_id)

        # Müzik dinleme nesnesini oluştur ve dinleme sayısını artır
        music_listening, created = MusicListening.objects.get_or_create(user=request.user, music=music)
        music_listening.listen_count += 1
        music_listening.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Kullanıcı oturumu açık değil.'}, status=401)


def search_music(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        musics = Music.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))[:10]
        data = [{'id': music.id, 'text': music.title} for music in musics]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

