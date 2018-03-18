from django.contrib import admin
from .models import TwitterAccount, TweetPost
from datetime import datetime


class TweetPostInline(admin.TabularInline):
    model = TweetPost

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


@admin.register(TwitterAccount)
class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ('account', )
    # readonly_fields = list_display
    # inlines = (TweetPostInline, )
    change_form_template = 'admin/tweet_change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['tweets_timeline'] = {}
        if object_id:
            max_count = 0
            new_dict = {}
            for item in TwitterAccount.objects.get(pk=object_id).tweets\
                    .order_by('date'):
                index = '{}-{}'.format(item.date.year, item.date.month)
                if index in new_dict:
                    new_dict[index] += 1
                    if new_dict[index] > max_count:
                        max_count = new_dict[index]
                else:
                    new_dict[index] = 1
            extra_context['tweets_timeline']['tweets'] = new_dict
            extra_context['tweets_timeline']['max_count'] = max_count

        return super(TwitterAccountAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
