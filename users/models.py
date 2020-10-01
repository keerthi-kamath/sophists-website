from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from PIL import Image


ROLE = (
    ('Mentee', "Mentee"),
    ('Mentor', "Mentor"),
)

BATCH = (
    ("2011", "2011"),
    ("2012", "2012"),
    ("2013", "2013"),
    ("2014", "2014"),
    ("2015", "2015"),
    ("2016", "2016"),
    ("2017", "2017"),
    ("2018", "2018"),
    ("2019", "2019"),
    ("2020", "2020"),
    ("2021", "2021")
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    role = models.BooleanField(default=False)
    batch = models.CharField(max_length=10, choices=BATCH, default="2019")
    name = models.CharField(max_length=100, default=None, blank=True, null=True)
    phone = models.PositiveBigIntegerField(default=None, blank=True, null=True)
    college = models.CharField(max_length=300, default=None, blank=True, null=True)
    profession = models.CharField(max_length=100, default=None, blank=True, null=True)
    address = models.TextField(default=None, blank=True, null=True)
    guidance = models.TextField(default=None, blank=True, null=True)
    linkedin = models.URLField(default=None, blank=True, null=True)
    instagram = models.URLField(default=None, blank=True, null=True)
    twitter = models.URLField(default=None, blank=True, null=True)
    github = models.URLField(default=None, blank=True, null=True)
    okr = models.URLField(default=None, blank=True, null=True)
    facebook = models.URLField(default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.user.pk})

    @property
    def get_point(self):
        return self.user.reward_set.aggregate(Sum('badges__points'))['badges__points__sum']

    @property
    def get_number_of_badges(self):
        return self.user.reward_set.count()


class Pomodoro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(default=0)
    energy = models.FloatField(default=0)
    productivity = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.username} - Pomodoro Count : {self.count}'


class Badge(models.Model):
    points = models.IntegerField(default=1)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='badges')
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'Badge: {self.title}'


class Reward(models.Model):
    awarded_by = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decision = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    badges = models.ForeignKey(Badge, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class Teams(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='teams')
    bio = models.TextField()
    members = models.ManyToManyField(Profile)

    def __str__(self):
        return f'{self.name}'


class House(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='house')
    bio = models.TextField()
    teams = models.ManyToManyField(Teams)

    def __str__(self):
        return f'{self.name}'
