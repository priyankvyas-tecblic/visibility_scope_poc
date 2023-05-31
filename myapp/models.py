from django.db import models
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
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
    name = models.CharField(_("State Name"), max_length=50)
    fk = models.ForeignKey(Zone, verbose_name=_("Zone Foreign Key"), on_delete=models.CASCADE)

class District(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    fk = models.ForeignKey(State, verbose_name=_("Foreign Key"), on_delete=models.CASCADE)

class Cluster(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    fk = models.ForeignKey(District, verbose_name=_("Foreign Key"), on_delete=models.CASCADE)
    
class Premise(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    fk = models.ForeignKey(Cluster, verbose_name=_("Foreign Key"), on_delete=models.CASCADE)

class Warehouse(models.Model):
    name = models.CharField(_("Warehouse Name"), max_length=50)
    fk = models.ForeignKey(Premise, verbose_name=_("Foreign Key"), on_delete=models.CASCADE)

class UserRole(models.Model):
    name = models.CharField(max_length=50)
    rank = models.PositiveIntegerField()
    
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
            user_role="operational_head",
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        return self.model.objects.create_user(**kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), max_length=255, unique=True)
    password = models.CharField(_("Password"), max_length=200)
    user_role = models.CharField(
        _("User Role"), max_length=30, choices=UserRoleChoices.choices
    )
    is_active = models.BooleanField(_("Active Status"), default=True)
    is_staff = models.BooleanField(_("Staff Status"), default=False)
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

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
class SpecificPermission(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, related_name="specific_permissions")
    zone_fk = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True)
    state_fk = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    district_fk = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    cluster_fk = models.ForeignKey(Cluster, on_delete=models.CASCADE, null=True, blank=True)
    premise_fk = models.ForeignKey(Premise, on_delete=models.CASCADE, null=True, blank=True)
    warehouse_fk = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True)
    
