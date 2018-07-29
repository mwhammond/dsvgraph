from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

import grakn
import uuid

client = grakn.Client(uri='http://35.197.194.67:4567', keyspace='dsvgraph')

class CustomUser(AbstractUser):
	# add additional fields in here

	def __str__(self):
		return self.email


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created: 
        print(instance.username)
        print(instance.email)

        client.execute('insert $x isa person, has email "'+instance.email+'", has name "'+instance.username+'";') # dictionaries are nested structures

        #profile, new = UserProfile.objects.get_or_create(user=instance)		