from django.db import models
from django.utils.translation import gettext as _
class ZoneChoice(models.TextChoices): 
    NORTH = "north",_("North")
    SOUTH = "south",_("South")
    EAST = "east",_("East")
    WEST = "west",_("West")

# Create your models here.
class Zone(models.Model):
    type = models.CharField(_("Zone Type"),choices=ZoneChoice.choices, max_length=50)
    class Meta:
        permissions = [
        ("read_obj", "Read Obj"),
        ("read_all_obj", "Read All Obj"),
        ]

class State(models.Model):
    state_name = models.CharField(_("State Name"), max_length=50)
    zonefk = models.ForeignKey(Zone, verbose_name=_("Zone Foreign Key"), on_delete=models.CASCADE)

class District(models.Model):
    district_name = models.CharField(_("State Name"), max_length=50)
    statefk = models.ForeignKey(State, verbose_name=_("Zone Foreign Key"), on_delete=models.CASCADE)