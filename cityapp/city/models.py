# Create your models here.
from community_user.models import CommunityUser
from django.db import models
from django.utils import timezone


class City(models.Model):
    created_by = models.ForeignKey(CommunityUser, related_name="city_author", on_delete=models.CASCADE, blank=True,
                                   null=True)
    name = models.CharField(max_length=55, unique=True)
    country_name = models.CharField(max_length=55)
    geolocation = models.CharField(max_length=55)
    image = models.ImageField(upload_to='media/city')
    creation_date = models.DateTimeField(editable=False)
    modification_date = models.DateTimeField(editable=False)

    # Displaying city's name
    def __str__(self):
        return self.name

    # Creation Date and Modification Date while creating and update
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = timezone.now()
        self.modification_date = timezone.now()
        return super(City, self).save(*args, **kwargs)


#def save_city(sender, instance, **kwargs):
    # to do --> action send


#post_save.connect(save_city, sender=City)