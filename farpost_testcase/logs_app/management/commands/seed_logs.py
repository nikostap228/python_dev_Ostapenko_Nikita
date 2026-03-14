from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Seed space_type and event_type with predefined values in logs_db'

    def handle(self, *args, **options):
        # Получаем модели через apps.get_model (надёжнее прямого импорта)
        SpaceType = apps.get_model('logs_app', 'SpaceType')
        EventType = apps.get_model('logs_app', 'EventType')
        
        db_alias = 'logs_db'  # явно указываем базу данных

        space_types = ['global', 'blog', 'post']
        for name in space_types:
            obj, created = SpaceType.objects.using(db_alias).get_or_create(name=name)
            if created:
                self.stdout.write(f"SpaceType '{name}' created in {db_alias}.")
            else:
                self.stdout.write(f"SpaceType '{name}' already exists.")

        event_types = ['login', 'comment', 'create_post', 'delete_post', 'logout']
        for name in event_types:
            obj, created = EventType.objects.using(db_alias).get_or_create(name=name)
            if created:
                self.stdout.write(f"EventType '{name}' created in {db_alias}.")
            else:
                self.stdout.write(f"EventType '{name}' already exists.")