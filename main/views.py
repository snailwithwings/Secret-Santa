from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Group, User, WishlistItem, Assignment
import random


def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('fname').strip()

        # CREATE NEW GROUP
        if action == 'create':
            while True:
                new_code = str(random.randint(0, 9999)).zfill(4)
                if not Group.objects.filter(code=new_code).exists():
                    break

            group = Group.objects.create(code=new_code)

            # Creator always first + auto-set
            user = User.objects.create(name=name, group=group, is_creator=True)

            request.session['username'] = name
            request.session['group_code'] = group.code
            return redirect('homepage')

        # JOIN EXISTING GROUP
        if action == 'join':
            code = request.POST.get('groupCode', '').strip()

            try:
                group = Group.objects.get(code=code)
            except Group.DoesNotExist:
                return render(request, 'index.html', {
                    'error': f"Group '{code}' not found."
                })

            # Check if they already exist in this group
            existing_user = User.objects.filter(name__iexact=name, group=group).first()

            if existing_user:
                # Re-login returning user
                request.session['username'] = existing_user.name
                request.session['group_code'] = code
                return redirect('homepage')

            # Otherwise create a new user joining this group
            user = User.objects.create(name=name, group=group)

            request.session['username'] = name
            request.session['group_code'] = code
            return redirect('homepage')

    return render(request, 'index.html')



def homepage(request):
    name = request.session.get('username')
    code = request.session.get('group_code')

    if not name or not code:
        return redirect('index')

    group = Group.objects.get(code=code)

    user = User.objects.filter(name__iexact=name, group=group).first()
    if not user:
        # Should not happen normally, but safety check:
        return redirect('index')

    if request.method == 'POST' and user.is_creator:
        new_budget = request.POST.get('budget')
        if new_budget and new_budget.isdigit():
            group.budget = int(new_budget)
            group.save()
            return redirect('homepage')  # refresh page after saving

    return render(request, 'homepage.html', {
        'user': user,
        'group': group,
        'is_creator': user.is_creator
    })


def wish(request):
    name = request.session.get('username')
    code = request.session.get('group_code')
    group = Group.objects.get(code=code)
    user = User.objects.get(name__iexact=name, group=group)

    if request.method == 'POST':
        WishlistItem.objects.create(
            user=user,
            item_name=request.POST.get('itemName'),
            details=request.POST.get('details')
        )
        return redirect('homepage')

    return render(request, 'wish.html', {
        'group': group,
        'user': user
    })


def generate_assignments(request):
    name = request.session.get('username')
    code = request.session.get('group_code')

    group = Group.objects.get(code=code)
    user = User.objects.get(name__iexact=name, group=group)

    if not user.is_creator:
        return HttpResponse("Only the group creator can assign!")

    Assignment.objects.filter(giver__group=group).delete()
    users = list(group.users.all())
    receivers = users.copy()

    while True:
        random.shuffle(receivers)
        if all(g != r for g, r in zip(users, receivers)):
            break

    for g, r in zip(users, receivers):
        Assignment.objects.create(giver=g, receiver=r)

    return redirect('homepage')


def yourperson(request):
    name = request.session.get('username')
    code = request.session.get('group_code')

    if not name or not code:
        return redirect('index')

    group = Group.objects.get(code=code)
    user = User.objects.get(name__iexact=name, group=group)

    try:
        assigned = Assignment.objects.get(giver=user).receiver
        items = assigned.wishlist_items.all()
    except Assignment.DoesNotExist:
        assigned = None
        items = []

    return render(request, 'yourperson.html', {
        'user': user,
        'assigned_person': assigned,
        'wishlist_items': items,
        'group': group
    })

# def edit_group_budget(request, group_id):
#     group = get_object_or_404(Group, id=group_id)

#     if request.method == 'POST':
#         new_budget = request.POST.get('budget')
#         if new_budget and new_budget.isdigit():
#             group.budget = int(new_budget)
#             group.save()
#             return redirect('homepage', group_id=group.id)

#     return render(request, 'homepage.html', {'group': group})