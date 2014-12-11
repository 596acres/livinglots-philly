from operator import itemgetter
import re

from django.template.loader import render_to_string
from django.views.generic import View

from actstream.models import Action
from braces.views import JSONResponseMixin
from elephantblog.models import Entry
from twitter_feed.models import Tweet


def _clean_html(html):
    html, n = re.subn(r'\s+', ' ', html)
    return html.strip().replace('\n', '')


class CombinedActivityFeed(JSONResponseMixin, View):

    def get_actions(self):
        """Get actions, records of someone doing something on the site."""

        def as_html(action):
            templates = [
                'actstream/%s/action.html' % action.verb.replace(' ', '_'),
                'actstream/action.html',
            ]
            return _clean_html(render_to_string(templates, {'action': action}))

        def as_dict(action):
            return {
                'html': as_html(action),
                'time': action.timestamp,
                'type': 'action',
            }

        return [as_dict(a) for a in Action.objects.all()]

    def get_blog_posts(self):
        def as_html(entry):
            return _clean_html(render_to_string('elephantblog/entry_activity_stream.html',
                                                { 'entry': entry }))

        def as_dict(entry):
            return {
                'html': as_html(entry),
                'time': entry.published_on,
                'type': 'blog',
            }

        return [as_dict(e) for e in Entry.objects.active()]

    def get_tweets(self):
        def as_html(tweet):
            return _clean_html(render_to_string('twitter_feed/tweet_activity_stream.html',
                                                { 'tweet': tweet }))

        def as_dict(tweet):
            return {
                'html': as_html(tweet),
                'time': tweet.published_at,
                'type': 'tweet',
            }

        return [as_dict(e) for e in Tweet.objects.all()]

    def get_activities(self, page=1, per_page=20):
        """Get combined, sorted activities, paginated"""
        activities = self.get_actions() + self.get_blog_posts() + self.get_tweets()
        activities = sorted(activities, key=itemgetter('time'), reverse=True)
        return activities[(page - 1) * per_page:page * per_page]

    def get(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))
        return self.render_json_response(self.get_activities(page=page))
