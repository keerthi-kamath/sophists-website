from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    comments = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Events(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    date_and_time = models.CharField(max_length=50)
    link = models.URLField(default='https://us02web.zoom.us/j/89238479481?pwd=VG5SRzZlUjBWQUpBd1NEbm4yS2Z1Zz09')
    poster = models.ImageField(upload_to='events')

    def __str__(self):
        return self.title
