from django.db import models
from django.template.defaultfilters import truncatechars
from users.models import User



class RequestLog(models.Model):
    """
    Basic log record describing all user interaction with the UI.
    Will be propagated by a middle ware.
    This will be one BIG DB table!
    """
    duration = models.DecimalField(decimal_places=2, max_digits=4)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    request_url = models.URLField()
    request_querystring = models.TextField()
    request_body = models.TextField()
    response_body = models.TextField()
    request_method = models.CharField(max_length=10)
    request_headers = models.TextField()
    response_status = models.CharField(max_length=4)

    def __str__(self):
        return f"[{self.time.strftime('%Y-%m-%d-%H:%M:%S')}]  {self.request_url}   {self.response_status}"

    @property
    def short_response_body(self):
        return truncatechars(self.response_body, 200)


class ChromeExtensionLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    traceback = models.TextField(null=True)
    local_storage = models.JSONField()
    meta_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
