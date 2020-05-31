from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.utils.text import slugify
import django



# Create your models here.



class Annotation(models.Model):
    #name = models.CharField(max_length=120)
    annotation = JSONField(blank=True, null=True)

    #def save(self, *args, **kwargs):
        #if not self.annotation['@context'] == "http://www.w3.org/ns/anno.jsonld":
        #    print("not valid")
        #    raise django.core.exceptions.ValidationError('Invalid schema.')
        #    return False
        #elif  self.annotation['body'] == "":
        #    raise django.core.exceptions.ValidationError('Invalid schema.')
        #    return False
        #elif  self.annotation['target'] == "":
        #    raise django.core.exceptions.ValidationError('Invalid schema.')
        #    return False
        #else:
        #    return super(Annotation, self).save(*args, **kwargs)


    #created = models.DateTimeField(editable=False)
    #slug = models.SlugField(unique=True, max_length=150, editable=False)
    #
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created = timezone.now()
    #         self.slug = self.get_slug()
    #     return super(Annotation, self).save(*args, **kwargs)
    #
    # def get_slug(self):
    #     slug = slugify(self.name.replace("ı","i"))
    #     unique= slug
    #     number = 1
    #
    #     while Annotation.objects.filter(slug = unique).exists():
    #         unique = '{}-{}'.format(slug, number)
    #         number += 1
    #
    #     return unique




#annotations format will be like
# class Annotation {
#   constructor(object = { id: null, target: null }) { //uuid can also apply to Body and Target.
#     this['@context'] = 'http://www.w3.org/ns/anno.jsonld';
#     this.type = 'Annotation';
#     this.id = object.id; //An Annotation must have exactly 1 URL that identifies it.
#     this.id = hexId;
#     this.userId = "annonymous";
#     this.target = object.target; //There must be 1 or more target relationships associated with an Annotation
#     this.body = {type: "text"};
#     if (typeof object.motivation != 'undefined') { this.motivation = object.motivation }
#     if (typeof object.canonical != 'undefined') { this.canonical = object.canonical }
#     if (typeof object.bodyValue != 'undefined') { this.bodyValue = object.bodyValue }
#     if (typeof object.body != 'undefined') { this.body = object.body }
#
#     return this;
#   }
# }