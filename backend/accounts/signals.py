from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    groups = {
        1: "Customer",
        2: "Vendor",
        3: "Shopora Team"
    }

    for group_id, name in groups.items():
        Group.objects.get_or_create(
            id=group_id,
            defaults={"name": name}
        )
