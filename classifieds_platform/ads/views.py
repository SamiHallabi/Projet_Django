from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Ad, Category, AdImage, Message,models,User,Profile
from .forms import AdForm, MessageForm,SearchForm
from django.contrib.auth import logout

def home(request):
    form = SearchForm(request.GET or None)
    ads = Ad.objects.select_related('category').prefetch_related('adimage_set')
    
    if request.GET and form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        location = form.cleaned_data.get('location')
        sort_by = form.cleaned_data.get('sort_by')

        if query:
            ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category:
            ads = ads.filter(category=category)
        if min_price is not None:
            ads = ads.filter(price__gte=min_price)
        if max_price is not None:
            ads = ads.filter(price__lte=max_price)
        if location:
            ads = ads.filter(location__icontains=location)
        if sort_by:
            ads = ads.order_by(sort_by)
        
        if not ads.exists():
            messages.info(request, 'No ads match your search criteria.')

    return render(request, 'home.html', {'ads': ads, 'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            for image in request.FILES.getlist('images'):
                AdImage.objects.create(image=image, ad=ad)
            return redirect('home')
    else:
        form = AdForm()
    return render(request, 'ad_create.html', {'form': form})

def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ad_detail.html', {'ad': ad})

@login_required
def inbox(request):
    # Get all conversations (distinct sender/recipient pairs for the current user)
    received = Message.objects.filter(recipient=request.user).values('sender', 'ad').distinct()
    sent = Message.objects.filter(sender=request.user).values('recipient', 'ad').distinct()
    
    conversations = []
    seen = set()
    
    for msg in received:
        key = (msg['sender'], msg['ad'])
        if key not in seen:
            sender = User.objects.get(id=msg['sender'])
            ad = Ad.objects.get(id=msg['ad']) if msg['ad'] else None
            last_message = Message.objects.filter(
                sender__id=msg['sender'],
                recipient=request.user,
                ad=ad
            ).order_by('-created_at').first()
            unread_count = Message.objects.filter(
                sender__id=msg['sender'],
                recipient=request.user,
                ad=ad,
                is_read=False
            ).count()
            conversations.append({
                'user': sender,
                'ad': ad,
                'last_message': last_message,
                'unread_count': unread_count
            })
            seen.add(key)
    
    for msg in sent:
        key = (msg['recipient'], msg['ad'])
        if key not in seen:
            recipient = User.objects.get(id=msg['recipient'])
            ad = Ad.objects.get(id=msg['ad']) if msg['ad'] else None
            last_message = Message.objects.filter(
                sender=request.user,
                recipient__id=msg['recipient'],
                ad=ad
            ).order_by('-created_at').first()
            conversations.append({
                'user': recipient,
                'ad': ad,
                'last_message': last_message,
                'unread_count': 0
            })
            seen.add(key)
    
    conversations.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else 0, reverse=True)
    return render(request, 'inbox.html', {'conversations': conversations})

@login_required
def conversation(request, user_id, ad_id=None):
    other_user = get_object_or_404(User, id=user_id)
    ad = get_object_or_404(Ad, id=ad_id) if ad_id else None
    
    # Mark messages as read
    Message.objects.filter(
        sender=other_user,
        recipient=request.user,
        ad=ad,
        is_read=False
    ).update(is_read=True)
    
    # Get message thread (renamed from 'messages' to 'message_list')
    message_list = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user),
        ad=ad
    ).order_by('created_at')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = other_user
            message.ad = ad
            message.save()
            messages.success(request, 'Message sent!')  # Use django.contrib.messages
            return redirect('conversation', user_id=user_id, ad_id=ad_id)
    else:
        form = MessageForm()
    
    return render(request, 'conversation.html', {
        'messages': message_list,  # Update template variable
        'form': form,
        'other_user': other_user,
        'ad': ad
    })

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    ads = Ad.objects.filter(user=request.user).select_related('category').prefetch_related('adimage_set')
    return render(request, 'profile.html', {'user': request.user, 'profile': profile, 'ads': ads})

def custom_logout(request):
    logout(request)
    return redirect('home')