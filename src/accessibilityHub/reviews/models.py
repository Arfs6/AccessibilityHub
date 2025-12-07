from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from utils import decimal2Base36


class Owner(models.Model):
    """Represents an owner of a tool."""

    name = models.CharField(max_length=128)
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=128, default='')
    verified = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a string representation of the object.
        Mainly for admin site.
        """
        return f'Owner: {self.name}'

    @classmethod
    def allVerified(cls):
        """Return all verified Owner objects."""
        return cls.objects.filter(verified=True)

    def save(self, *args, **kwargs):
        """Does some tasks before saving the object.
        Primarily add some fields to the model.
        """
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def base36Id(self):
        """Returns the base36 equivalent of the owner's id."""
        return decimal2Base36(self.id)


class Tool(models.Model):
    """Represents a tool."""

    name = models.CharField(max_length=128)
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='tools')
    slug = models.SlugField(max_length=128, default='')
    verified = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    @classmethod
    def allVerified(cls):
        """Return all verified Tool objects."""
        return cls.objects.filter(verified=True, owner__verified=True)

    def save(self, *args, **kwargs):
        """Does some tasks before saving the object.
        Primarily add some fields to the model.
        """
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def avgRating(self) -> float | None:
        """Returns the average rating of a tool.
        Returns None if there aren't any rating.
        """
        reviews: list[Review] = self.reviews.all()
        if not reviews:
            return

        total_rating = sum(review.rating for review in reviews)
        return total_rating / len(reviews)


class Review(models.Model):
    """Represents a review of a tool."""

    ratingChoices = (
        (1, 'Non-Accessible'),
        (2, 'Partially Accessible'),
        (3, 'Mostly Accessible'),
        (4, 'Highly Accessible'),
        (5, 'Fully Accessible'),
    )
    rating = models.PositiveSmallIntegerField(choices=ratingChoices)
    comment = models.TextField(null=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='reviews')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
