from django import template
from django.core.urlresolvers import reverse

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

register = template.Library()


class PreviewUrl(AsTag):
    options = Options(
        Argument('flatblock', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=True),
    )

    def get_value(self, context, flatblock):
        # If flatblock.mailing_set, return that preview, reversed
        if flatblock.mailing_set.exists():
            return reverse('mailings_preview', kwargs={
                'pk': flatblock.mailing_set.all()[0].pk,
            })

        # TODO: Elif flatblock.notification_set ...
        return ''

register.tag(PreviewUrl)
