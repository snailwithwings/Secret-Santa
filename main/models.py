from django.db import models

class Group(models.Model):
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return f"Group {self.code}"


class User(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='users')
    is_creator = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.group.code})"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    item_name = models.CharField(max_length=200)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item_name} ({self.user.name})"


class Assignment(models.Model):
    giver = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='given_assignment'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_assignments'
    )

    def __str__(self):
        return f"{self.giver.name} → {self.receiver.name}"

