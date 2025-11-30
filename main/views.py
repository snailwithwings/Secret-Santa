import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, WishlistItem, Assignment


def index(request):
    return render(request, 'index.html')

def homepage(request):
    if request.method == 'POST':
        name = request.POST.get('fname').strip()

        # Save name to session
        request.session['username'] = name

        return redirect('yourperson')

    return render(request, 'homepage.html')

def wish(request):
    participants = User.objects.all()

    if request.method == 'POST':
        participant_id = request.POST.get('personSelect')
        item_name = request.POST.get('itemName')
        details = request.POST.get('details')

        participant = User.objects.get(id=participant_id)

        # Save single item
        WishlistItem.objects.create(
            participant=participant,
            item_name=item_name,
            details=details
        )

        return redirect('wish')

    return render(request, 'wish.html', {'participants': participants})

def yourperson(request):
    name = request.session.get('username', None)

    if not name:
        return redirect('homepage')  # If they didn’t enter a name first

    try:
        participant = User.objects.get(name__iexact=name)  # case-insensitive match
    except User.DoesNotExist:
        return render(request, 'yourperson.html', {
            'participant': None,
            'assigned_person': None,
            'wishlist_items': [],
            'error': f"Name '{name}' not found. Please check spelling."
        })

    try:
        assigned = Assignment.objects.get(giver=participant).receiver
        items = assigned.wishlist_items.all()
    except Assignment.DoesNotExist:
        assigned = None
        items = []

    return render(request, 'yourperson.html', {
        'participant': participant,
        'assigned_person': assigned,
        'wishlist_items': items,
        'error': None
    })

def generate_assignments():
    # Remove old assignments first
    Assignment.objects.all().delete()

    participants = list(User.objects.all())
    receivers = participants.copy()

    # Shuffle until valid (no one gets themselves)
    while True:
        random.shuffle(receivers)
        if all(giver != receiver for giver, receiver in zip(participants, receivers)):
            break

    # Create assignments
    for giver, receiver in zip(participants, receivers):
        Assignment.objects.create(giver=giver, receiver=receiver)
