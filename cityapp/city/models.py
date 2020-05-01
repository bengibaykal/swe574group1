from django.db import models
from django.utils import timezone
# Create your models here.

class City(models.Model):
    #builderID = models.ForeignKey(CommunityUser)
    name = models.CharField(max_length=55, unique=True)
    country_name = models.CharField(max_length=55)
    geolocation = models.CharField(max_length=55)
    image = models.ImageField(upload_to='media/city')
    creation_date = models.DateTimeField()
    modification_date = models.DateTimeField()

    def __str__(self):
        return self.name

    #Creation Date ve Modification Date icin duzenleme
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = timezone.now()
        self.modification_date = timezone.now()
        return super(City, self).save(*args, **kwargs)


