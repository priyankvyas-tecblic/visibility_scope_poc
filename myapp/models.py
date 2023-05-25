from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

class ZoneChoice(models.TextChoices): 
    NORTH = "north",_("North")
    SOUTH = "south",_("South")
    EAST = "east",_("East")
    WEST = "west",_("West")

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
    district_name = models.CharField(_("Name"), max_length=50)
    statefk = models.ForeignKey(State, verbose_name=_("Foreign Key"), on_delete=models.CASCADE)
    
class Premise(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    district_fk = models.ForeignKey(District, verbose_name=_("Foreign Key"), on_delete=models.CASCADE)

class Warehouse(models.Model):
    name = models.CharField(_("Warehouse Name"), max_length=50)
    premise_fk = models.ForeignKey(Premise, verbose_name=_("Foreign Key"), on_delete=models.CASCADE)
    
class UserRoleChoices(models.TextChoices):
    OH = "operational_head", _("operational_head")
    ZH = "zonal_head", _("zonal_head")
    SC = "state_coordinator", _("state_coordinator")
    AMO = "asset_monitoring_officer", _("area_monitoring_officer")
    AM = "area_manager", _("area_manager")
    WHS = "warehouse_supervisor", _("warehouse_supervisor")

class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        user_role,
        password=None,
        *args,
        **kwargs,
    ):
        if not email:
            raise ValueError("User must have an email address")
        if super().get_queryset().filter(email=self.normalize_email(email)):
            raise ValueError("User with this email address already exists")
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            user_role=user_role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        password=None,
    ):
        user = self.create_user(
            email,
            password=password,
            user_role=1,
        )
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        return self.model.objects.create_user(**kwargs)

class User(AbstractBaseUser):
    email = models.EmailField(_("Email"), max_length=255, unique=True)
    password = models.CharField(_("Password"), max_length=200)
    user_role = models.PositiveSmallIntegerField(
        _("User Role"), choices=UserRoleChoices.choices
    )
    is_active = models.BooleanField(_("Active Status"), default=True)
    is_superuser = models.BooleanField(_("Superuser Status"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "user_role"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
