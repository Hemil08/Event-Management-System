from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Registration, Event, CustomUser

@receiver(post_delete,sender=Registration)
def update_event_slots_on_delete(sender,instance,**kwargs):
    instance.event.available_slots += instance.persons
    instance.event.save()

@receiver(post_save,sender=Event)
def notify_participants_on_event_update(sender, instance, created, **kwargs):
    if created:
        return
    
    # Get all participants registered for the event
    participants = CustomUser.objects.filter(role="participant",registration__event=instance)

    subject = f"Update: Event '{instance.title}' has been updated! "

    message = (
        f"Dear Participant,\n\n"
        f"The event '{instance.title}' you registered for has been updated. \n\n"
        "Please check the event details for more information.\n\n"
    )

    recipients = [user.email for user in participants]
    if recipients:
        send_mail(subject,message,"sorathiyahemil2023@gmail.com",recipients,fail_silently=False)

@receiver(post_delete,sender=Event)
def notify_participants_on_Event_delete(sender,instance, **kwargs):
    participants = CustomUser.objects.filter(role="participants",registration__event=instance)

    subject = f"Important: Event '{instance.title}' has been canceled!"
    message = (
        f"Dear Participant"
        f"We regret to inform you that the event '{instance.title}' has been canceled.\n"
        f"We apologize for any inconvenience.\n\n"
        "Thank you for your understanding.\n\n"
    )

    recipients = [user.email for user in participants]
    if recipients:
        send_mail(subject,message,"sorathiyahemil2023@gmail.com",recipients,fail_silently=False)

@receiver(post_save,sender=Registration)
def notify_manager_when_event_full(sender,instance,**kwargs):
    event = instance.event

    total_registration = event.participants.count()

    if total_registration >= event.available_slots:
        manager = event.created_by

        if manager:
            subject = f"Event '{event.title}' is fully Booked!"

            message = (
                f"Dear {manager.username},\n\n"
                f"Your event '{event.title}' is now fully booked.\n"
                f"No more participants can register.\n\n"
                "Best regards,\nEvent Management Team"
            )
            send_mail(subject, message, "sorathiyahemil2023@gmail.com", [manager.email], fail_silently=False)