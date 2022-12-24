from django.db import models


class datalist(models.Model):
    CoachName = models.CharField(max_length=100)
    Day = models.CharField(max_length=20)
    TotalSlotFrom = models.TimeField()
    TotalSlotuntil = models.TimeField()

    def __str__(self):
        return '%s %s' % (self.CoachName, self.Day)


class Booktime(models.Model):
    CoachName = models.ForeignKey(
        datalist, on_delete=models.CASCADE, related_name='coaches')
    Slotperiodfrom = models.TimeField(default=None)

    def __str__(self):
        return '%s %s' % (self.CoachName, self.Slotperiodfrom)
