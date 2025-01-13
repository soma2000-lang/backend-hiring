from django.db.models.signals import post_save
from django.dispatch import receiver
from website.models import Jobs, UserRecords


@receiver(post_save, sender=Jobs)
def update_total_job_in_site(sender, instance, **kwargs):
    '''
    this update the total job in the site
    '''
    site= instance.site

    total_job = Jobs.objects.filter(site=site).count()
    site.total_jobs = total_job
    site.save()

@receiver(post_save, sender=UserRecords)
def update_total_user_in_site(sender, instance,**kwargs):
    '''
    this update the total user in the site
    '''
    site= instance.site
    total_user = UserRecords.objects.filter(site=site).count()
    site.total_users = total_user
    site.save()
   