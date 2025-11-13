from django.shortcuts import render, redirect
from .models import User, WishlistItem


def index(request):
    return render(request, 'index.html')

def homepage(request):
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
    # THIS WHOLE THING NEEDS TO BE CHANGED ONCE EVERYONE HAS FILLED IN THEIR WISHLIST
    participant = User.objects.first()

    return render(request, 'yourperson.html', {
        'participant': participant,
        'wishlist_items': participant.wishlist_items.all()
    })
