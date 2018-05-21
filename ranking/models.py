from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class Publisher(models.Model):
    name = models.CharField(max_length=80, blank=False)

    def __str__(self):
        return '<Publisher %s>' % self.name


class Paper(models.Model):
    title = models.CharField(max_length=140, blank=False)
    slug = models.SlugField(max_length=50, blank=True)  # auto-generated from title
    author = models.CharField(max_length=40, blank=False)
    year = models.IntegerField(null=False)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    abstract = models.TextField(blank=True)
    score = models.FloatField(null=False)

    def short_author(self):
        return self.author.split(' ')[0] + ' et al.'

    def __str__(self):
        return '"%s" by %s' % (self.title, self.short_author())


def length_slugify(value, length):
    slug = slugify(value)[:length]
    if '-' in slug:
        if slug[-1] == '-':
            return slug[:-1]
        else:
            return '-'.join(slug.split('-')[:-1])
    else:
        return slug


@receiver(pre_save, sender=Paper)
def autofill_slug(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.slug:
        instance.slug = length_slugify(instance.title, 50)
