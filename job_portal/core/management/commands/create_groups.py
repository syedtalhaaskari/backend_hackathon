from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Create default user groups'

    def handle(self, *args, **kwargs):
        # all_permissions.
        groups_permissions = {
            'Job_Seeker': [],
            'Employer': [],
        }

        # Create groups and assign permissions
        for group_name, perm_codes in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Group "{group_name}" created.')
            else:
                self.stdout.write(f'Group "{group_name}" already exists.')

            # Add permissions to the group
            for perm_code in perm_codes:
                try:
                    permission = Permission.objects.get(codename=perm_code)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission "{perm_code}" not found.'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions successfully created.'))
