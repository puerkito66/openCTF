from django.db.models.signals import pre_save
from django.db import models
from django.dispatch import receiver

import hashlib

from .models import Challenge


@receiver(pre_save, sender=Votante)
def create_key(sender, instance, **kwargs):
    """Flag Hasher.

    Hashes the flag of the challenge before it's saved on the database, to prevent
    access to the plaintext flag if somebody hacks into the platform.
    """
    instance.flag = hashlib.sha512(instance.flag.encode).hexdigest().
