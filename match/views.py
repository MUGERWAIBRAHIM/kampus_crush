from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomSignupForm,MessageForm,ProfileForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser,Interest,Message
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            CustomUser.is_active = False
            code = generate_code()
            CustomUser.verification_code = code
            verify_code(request)
            return redirect('verify_code') 
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def events(request):
    return render(request, 'view_events.html')

@login_required
def choose_interest(request):
    if request.method == 'POST':
        selected_bracket = request.POST.get('age_bracket')
        selected_interest_ids = request.POST.getlist('interests')

        if not selected_interest_ids:
            # Re-render with error message
            return render(request, 'choose_interest.html', {
                'interests': Interest.objects.all(),
                'error': "Please select at least one interest."
            })

        request.session['selected_bracket'] = selected_bracket
        request.session['selected_interest_ids'] = selected_interest_ids
        return redirect('filtered_matches')  # This should match the URL name for the match results view

    return render(request, 'choose_interest.html', {
        'interests': Interest.objects.all()
    })

@login_required
def filtered_matches(request):
    selected_bracket = request.session.get('selected_bracket')
    selected_interest_ids = list(map(int, request.session.get('selected_interest_ids', [])))
    
    current_user = request.user
    potential_matches = CustomUser.objects.exclude(id=current_user.id)

    matches = []
    for user in potential_matches:
        if user.age_bracket() == selected_bracket:
            shared_interests = user.interests.filter(id__in=selected_interest_ids)
            if shared_interests.exists():
                matches.append(user)

    return render(request, 'filtered_matches.html', {
        'matches': matches,
        'interest_count': len(selected_interest_ids),
        'bracket': selected_bracket
    })

def generate_code():
    return str(random.randint(100000, 999999))

def send_verification_email(user):
    code = generate_code()
    user.verification_code = code
    user.save()

    send_mail(
        'Your Kampus Crush Verification Code',
        f'Hello {user.username}, your verification code is: {code}',
        'noreply@kampuscrush.com',
        [user.email],
        fail_silently=False,
    )

def verify_code(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('account_signup')

    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        code = request.POST.get('code')
        if code == user.verification_code:
            user.is_active = True
            user.email_verified = True
            user.verification_code = ''
            user.save()
            messages.success(request, "Email verified successfully. You can now log in.")
            return redirect('index')
        else:
            messages.error(request, "Incorrect verification code.")

    return render(request, 'verify_code.html')

def get_support(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\n{message}"

        # Optional: send email
        send_mail(
            subject='Support Request from Kampus Krush',
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['mugerwaibrahim90@gmail.com'],
        )

        messages.success(request, 'Your message has been sent successfully!')
    
    return render(request, 'get_support.html')

@login_required
def chat(request, username):
    other_user = CustomUser.objects.get(username=username)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.receiver = other_user
            new_message.save()
            return redirect('chat', username=other_user.username)
    else:
        form = MessageForm()

    return render(request, 'chat.html', {
        'messages': messages,
        'form': form,
        'other_user': other_user
    })

@login_required
def chat_list(request):
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))

    conversation_data = {}

    for msg in messages.order_by('-timestamp'):
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        if other_user not in conversation_data:
            conversation_data[other_user] = msg  # Save the latest message per user

    return render(request, 'chat_list.html', {'conversations': conversation_data})

@login_required
def view_profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})

def view_user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'user_profile.html', {'user_profile': user})
