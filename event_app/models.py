from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('manager', 'Event Manager'),
        ('participant', 'Participant'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=USER_TYPES, default="participant")

    def is_manager(self):
        return self.role == 'manager'

    def is_participant(self):
        return self.role == 'participant'

    def __str__(self):
        return self.username
    
class Category(models.Model):

    CATEGORY_TYPES = (
        ('Standup Comedy Shows','Standup Comedy Shows'),
        ('Music Concerts','Music Concerts'),
        ('Festivals','Festivals'),
        ('Party','Party'),
    )

    name = models.CharField(max_length=20, choices=CATEGORY_TYPES,default="standup_comedy_shows" )
    
    def __str__(self):
        return self.name
    
class EventQuerySet(models.QuerySet):
    def for_manager(self,user):
        if user.is_manager():
            return self.filter(created_by=user)
        return self.none()

class Event(models.Model):

    title = models.CharField(max_length=255)
    photo =models.ImageField(upload_to='events/',blank=True,null=True)
    description = models.TextField(blank=True, null=True)   
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    cost_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text = "Cost per person for attending the event."
    )
    available_slots = models.IntegerField(
        default=0,
        help_text="Number of available slots for the event."
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,related_name='events')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(CustomUser, through='Registration', related_name='participated_events')

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return self.title
   
class Registration(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    registration_date  = models.DateTimeField(auto_now_add=True)
    persons = models.IntegerField(default=1)
    contact_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter a valid contact number without spaces or special characters."
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Total cost of registration (calculated automatically)."
    )

    class Meta:
        unique_together = ('event','user')
    
    def __str__(self):
        return f'{self.user.username} - {self.event.title}'
    
    def clean(self):
        if self.persons < 1:
            raise ValidationError("Number of persons must be at least 1.")
        if self.event.available_slots < self.persons:
            raise ValidationError("Not enough available slots for the number of person registered.")  
        super().clean()

    def save(self,*args,**kwargs):
        self.total_cost = self.persons * self.event.cost_per_person

        self.event.available_slots -= self.persons
        self.event.save()
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}" 
    
