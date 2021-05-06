from django.db.models.signals import pre_save
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password

import hashlib

from .models import Challenge, Submition, Team


@receiver(pre_save, sender=Challenge)
@receiver(pre_save, sender=Submition)
def hash_flag(sender, instance, **kwargs):
    """Flag Hasher.

    Hashes the flag of the challenge before it's saved on the database, to prevent
    access to the plaintext flag if somebody hacks into the platform.
    """
    instance.flag = hashlib.sha512(instance.flag.encode).hexdigest()


@receiver(pre_save, sender=Team)
def hash_password(sender, instance, **kwargs):
    """Password Hasher.

    Hashes the Team password to be stored.
    """
    instance.password = make_password(instance.password)
