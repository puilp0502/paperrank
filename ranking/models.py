from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=80, blank=False)

    def __str__(self):
        return '<Publisher %s>' % self.name


class Paper(models.Model):
    title = models.CharField(max_length=140, blank=False)
    author = models.CharField(max_length=40, blank=False)
    year = models.IntegerField(null=False)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    score = models.FloatField(null=False)

    def short_author(self):
        return self.author.split(' ')[0] + ' et al.'

    def __str__(self):
        return '"%s" by %s' % (self.title, self.short_author())
