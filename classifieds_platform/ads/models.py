from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ad_images/')

    def __str__(self):
        return self.image.name

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"From {self.sender} about {self.ad} at {self.created_at}"

    class Meta:
        ordering = ['created_at']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
class Report(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')

    def __str__(self):
        return f"Report on {self.ad} by {self.user}"
    
from django.db import models
from django.contrib.auth.models import User
from .models import Ad

class Question(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()  # Question ou réponse
    is_answer = models.BooleanField(default=False)  # True pour réponse, False pour question
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')  # Pour lier réponse à question

    def __str__(self):
        return f"{'Answer' if self.is_answer else 'Question'} by {self.user.username} on {self.ad.title}"

    class Meta:
        ordering = ['created_at']