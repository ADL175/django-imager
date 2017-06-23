"""Define the Imager Profile class and its methods."""


from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible


class ImagerActiveManager(models.Manager):
    """Manager for the ImagerProfile active API."""

    def get_queryset(self):
        """Return query of active users."""
        return super(ImagerActiveManager, self).get_queryset().filter(is_active=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """A profile for users to our application."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, default='')
    age = models.IntegerField(default=18)
    camera_type = models.CharField(max_length=255, default='Kodak')
    job = models.CharField(max_length=255, default='')
    url = models.URLField(max_length=200, default='')
    active = ImagerActiveManager()

    STYLE_CHOICES = (
        ('MONO', 'Monochrome'),
        ('MACRO', 'Macro'),
        ('MICRO', 'Micro'),
        ('PORTRAIT', 'Portrait'),
        ('LANDSCAPE', 'Landscape'),
    )
    photography_style = models.CharField(
        max_length=255,
        choices=STYLE_CHOICES,
        default='PORTRAIT',
    )

    SOCIAL_CHOICES = (
        ('PEASANT', 'Peasant'),
        ('BANDIT', 'Bandit'),
        ('YEOMAN', 'Yeoman'),
        ('MANATARMS', 'Man-at-arms'),
        ('KNIGHT', 'Knight'),
        ('ROYALTY', 'Royalty'),
        ('WIZARD', 'Wizard'),

    )
    social_status = models.CharField(
        max_length=255,
        choices=SOCIAL_CHOICES,
        default='PEASANT',
    )

    @property
    def is_active(self):
        """Return whether or not this profile is active."""
        return self.user.is_active

    def __str__(self):
        """Define a str representation of an Imager Profile."""
        return '(Username: {}, Location: {}, Age: {}, Camera Type: {}, \
        Job: {}, Social Status: {}, Style: {}, URL: {})'\
        .format(
            self.user,
            self.location,
            self.age,
            self.camera_type,
            self.job,
            self.social_status,
            self.photography_style,
            self.url
        )


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    """Instantiate a profile for a new user."""
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance']
        )
        new_profile.save()


# LOOK UP MANAGER IN DJANGO DOCS FOR ACTIVE THING

# LOOK AT DOCS FOR ONETOFONEFIELD OPTIONS, on_delete cascade
