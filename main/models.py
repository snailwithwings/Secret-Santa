from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class WishlistItem(models.Model):
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )
    item_name = models.CharField(max_length=200)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item_name} ({self.participant.name})"
