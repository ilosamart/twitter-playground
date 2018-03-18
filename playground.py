# -*- coding: utf-8 -*-
import os
import twitter

from django.db.models import Max
from tweet.models import TwitterAccount, TweetPost


TWEETS_PER_REQUEST=200

api = twitter.Api(consumer_key=os.getenv('CONSUMER_KEY'),
                  consumer_secret=os.getenv('CONSUMER_SECRET'),
                  access_token_key=os.getenv('ACCESS_TOKEN'),
                  access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'))


"""
Não encontrado usuário do Twitter: o ex-secretário de Planejamento e Gestão do governo
 Yeda Crusius (PSDB),Mateus Bandeira (Novo);
"""
twitter_accounts=(
    'JoseIvoSartori',
    'Jairo_Jorge',
    'EduardoLeite_',
    'MiguelSRossetto',
    'DeputadoHeinze',
    'antonioweckrs',
    )

for twitter_account in TwitterAccount.objects.all():
    statuses = [1]
    max_id = None
    tweets_count = 0
    print('Lendo tweets de {}'.format(twitter_account.account))
    max_id = twitter_account.tweets.aggregate(max_id=Max('twitter_id'))['max_id']
    while len(statuses)>0:
        statuses = api.GetUserTimeline(screen_name=twitter_account.account,
                                       include_rts=True, exclude_replies=False,
                                       max_id=max_id)
        for status in statuses:
            try:
                new_status = TweetPost()
                new_status.from_status(status)
                new_status.save()
            except Exception as e:
                print(e)
        max_id = statuses[-1:][0].id - 1 if len(statuses) > 0 else None
        # print(len(statuses))
        tweets_count += len(statuses)
        print('.', end="", flush=True)
        # print(statuses)

    print('\nTotal de Tweets para {} : {}'.format(twitter_account, tweets_count))
