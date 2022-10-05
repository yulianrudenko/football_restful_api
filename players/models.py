from django.db import models


class Club(models.Model):
    title = models.CharField(max_length=55, unique=True)
    country = models.CharField(max_length=55)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class Player(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    age = models.IntegerField()
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.age}'
