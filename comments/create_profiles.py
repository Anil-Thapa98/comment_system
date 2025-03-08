from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from your_app.models import Profile  # Replace `your_app` with your app name

class Command(BaseCommand):
    help = 'Create profiles for existing users who do not have one.'

    def handle(self, *args, **kwargs):
        users_without_profile = User.objects.filter(profile__isnull=True)
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
        self.stdout.write(self.style.SUCCESS('Finished creating profiles.'))