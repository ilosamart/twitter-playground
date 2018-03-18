from django.db import models
from twitter.models import Status
from datetime import datetime


# Exceptions

class InvalidTwitterStatusError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(InvalidTwitterStatusError, self).__init__(message)

        # Now for your custom code...
        # self.errors = errors

# Models


class TwitterAccount(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(blank=False, null=False, max_length=40)


class TweetPost(models.Model):
    id = models.AutoField(primary_key=True)
    twitter_id = models.PositiveIntegerField(blank=False, null=False)
    date = models.DateTimeField(blank=False, null=False)
    text = models.CharField(blank=False, null=False, max_length=280)
    posted_by = models.ForeignKey(TwitterAccount, blank=False, null=False, related_name='tweets')

    def from_status(self, status):
        if isinstance(status, Status):
            self.twitter_id = status.id
            self.date = datetime.strptime(status.created_at, '%a %b %d %H:%M:%S %z %Y')
            self.text = status.text
            self.posted_by = TwitterAccount.objects.get(account=status.user.screen_name)
        else:
            raise InvalidTwitterStatusError('Invalid status {}'.format(status))
