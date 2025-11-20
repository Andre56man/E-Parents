from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Grade, Attendance, Assignment
from notifications.models import create_notification


@receiver(post_save, sender=Grade)
def notify_parent_on_grade(sender, instance, created, **kwargs):
    """
    Créer une notification pour les parents lorsqu'une note est ajoutée
    """
    if created:
        student = instance.student
        parents = student.parents.all()
        
        for parent in parents:
            create_notification(
                recipient=parent,
                notification_type='GRADE',
                title=f'Nouvelle note en {instance.subject.name}',
                message=f'{student.get_full_name()} a reçu une note de {instance.value}/20 en {instance.subject.name} ({instance.get_grade_type_display()})',
                student=student,
                class_obj=student.current_class
            )


@receiver(post_save, sender=Attendance)
def notify_parent_on_attendance(sender, instance, created, **kwargs):
    """
    Créer une notification pour les parents lorsqu'une absence/retard est enregistré
    """
    if created:
        student = instance.student
        parents = student.parents.all()
        
        for parent in parents:
            create_notification(
                recipient=parent,
                notification_type='ATTENDANCE',
                title=f'{instance.get_status_display()} - {student.get_full_name()}',
                message=f'{student.get_full_name()} a été marqué(e) comme {instance.get_status_display().lower()} le {instance.date.strftime("%d/%m/%Y")}',
                student=student,
                class_obj=instance.class_obj
            )


@receiver(post_save, sender=Assignment)
def notify_parent_on_assignment(sender, instance, created, **kwargs):
    """
    Créer une notification pour les parents lorsqu'un devoir est publié
    """
    if created:
        students = instance.class_obj.students.all()
        
        for student in students:
            parents = student.parents.all()
            
            for parent in parents:
                create_notification(
                    recipient=parent,
                    notification_type='ASSIGNMENT',
                    title=f'Nouveau devoir : {instance.title}',
                    message=f'Un nouveau devoir a été publié en {instance.subject.name} pour {instance.class_obj.name}. Date limite : {instance.due_date.strftime("%d/%m/%Y à %H:%M")}',
                    student=student,
                    class_obj=instance.class_obj
                )

