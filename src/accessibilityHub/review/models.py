from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify
from typing import Optional

from utils import decimal2Base36


class Owner(models.Model):
    """Represents an owner of a tool.
    """
    name = models.CharField(max_length=128)
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=128)

    def save(self, *args, **kwargs):
        """Does some tasks before saving the object.
        Primarily add some fields to the model.
        """
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def base36Id(self):
        """Returns the base36 equivalent of the owner's id.
        """
        return decimal2Base36(self.id)


class Tool(models.Model):
    """Represents a tool.
    """
    name = models.CharField(max_length=128)
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='tools')
    slug = models.SlugField(max_length=128)

    def save(self, *args, **kwargs):
        """Does some tasks before saving the object.
        Primarily add some fields to the model.
        """
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def avgRating(self) -> Optional[float]:
        """Returns the average rating of a tool.
        Returns None if there aren't any rating.
        """
        reviews: list[Review] = self.reviews.all()
        if not reviews:
            return

        total_rating = sum(review.rating for review in reviews)
        return total_rating / len(reviews)


class Review(models.Model):
    """Represents a review of a tool.
    """
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    comment = models.TextField(null=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='reviews')
    createdAt = models.DateTimeField(default=timezone.now)
