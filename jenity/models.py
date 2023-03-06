
import pytz
import datetime

from django.db import models
from jenity.createCookieId import createSessionIdForCookie

paris_tz = pytz.timezone('Europe/Paris')


class Channel(models.Model):

    created_at = models.DateField(auto_now = True)
    description = models.TextField(null = False)
    name = models.TextField(null = False, unique = True)

    def __unicode__(self):
        return f"{self.code}"

    def __str__(self) -> str:
        return f"Channel : [{self.created_at}, {self.description}, {self.name}]"

class CookieApp(models.Model):

    sessionId = models.TextField(null = True)
    created_at = models.DateField(auto_now = True)
    expire_at = models.DateTimeField(null = True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.sessionId = createSessionIdForCookie(200)
            self.expire_at = datetime.datetime.now(paris_tz) + datetime.timedelta(hours=1)
        super().save(*args, **kwargs)

    def __unicode__(self):
        return f"{self.code}"
    
    def __str__(self) -> str:
        return f"Cookie : [{self.sessionId}, {self.created_at}, {self.expire_at}]"


class UserApp(models.Model):

    email = models.TextField(null = False, unique = True)
    password = models.TextField(null = False)
    username = models.TextField(null = False)
    isLogged = models.BooleanField(default= False)
    cookie = models.ForeignKey(CookieApp, on_delete=models.SET_NULL, null = True)
    current_channel_id = models.ForeignKey(Channel, default=1, on_delete=models.SET_DEFAULT, null=False)

    def __unicode__(self):
        return f"{self.code}"

    def __str__(self) -> str:
        return f"User : [{self.email}, {self.password}, {self.username}, {self.isLogged}, {self.cookie}, {self.current_channel_id}]"

class Message(models.Model):

    content = models.TextField(null = False)
    created_at = models.DateField(auto_now = True)
    updated_at = models.DateField(auto_now = True)
    channel_id = models.ForeignKey(Channel, on_delete = models.CASCADE, null = False, blank = False)
    user_id = models.ForeignKey(UserApp, on_delete = models.CASCADE, null = False, blank = False)

    def __unicode__(self):
        return f"{self.code}"

    def __str__(self) -> str:
        return f"Message : [{self.content}, {self.created_at}, {self.updated_at}, {self.channel_id}, {self.user_id}]"
