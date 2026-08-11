from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User, UserProfile, UserRole

ROLE_GROUP_MAPPING = {
    UserRole.SUPER_ADMIN: 'Super Admin',
    UserRole.ADMIN: 'Admin',
    UserRole.EDITOR: 'Editor',
    UserRole.AUTHOR: 'Author',
    UserRole.MODERATOR: 'Moderator',
    UserRole.SUBSCRIBER: 'Subscriber',
}

def ensure_role_groups_exist():
    """Ensure all role groups exist in Django Auth Group table."""
    for role_code, group_name in ROLE_GROUP_MAPPING.items():
        Group.objects.get_or_create(name=group_name)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Auto-create UserProfile and assign matching Django Group on User save."""
    if created:
        UserProfile.objects.get_or_create(user=instance)

    # Automatically synchronize Django Groups based on user.role
    target_group_name = ROLE_GROUP_MAPPING.get(instance.role)
    if target_group_name:
        group, _ = Group.objects.get_or_create(name=target_group_name)
        # Remove user from other role groups and assign to current group
        all_role_group_names = set(ROLE_GROUP_MAPPING.values())
        groups_to_remove = Group.objects.filter(name__in=all_role_group_names).exclude(id=group.id)
        instance.groups.remove(*groups_to_remove)
        instance.groups.add(group)
