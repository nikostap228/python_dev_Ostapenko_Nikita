from django.db import models

class SpaceType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'space_type'

    def __str__(self):
        return self.name

class EventType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'event_type'

    def __str__(self):
        return self.name

class Log(models.Model):
    datetime = models.DateTimeField()
    user_id = models.IntegerField()
    space_type = models.ForeignKey(SpaceType, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    target_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'logs'

    def __str__(self):
        return f"{self.datetime} - user {self.user_id} - {self.event_type}"