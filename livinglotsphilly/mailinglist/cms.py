from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class MailingListSignup(models.Model):
    # Cosmetic bits
    button_text = models.CharField(_('button text'), max_length=50,)
    form_url = models.URLField(_('form url'),)
    header_text = models.CharField(_('header text'), max_length=50,)

    # Form parameters
    llr = models.CharField(_('Constant contact: llr'), max_length=50,)
    m = models.CharField(_('Constant contact: m'), max_length=50,)

    class Meta:
        abstract = True
        verbose_name = _('Mailing list signup')
        verbose_name_plural = _('Mailing list signup')

    def render(self, **kwargs):
        ctx = { 'mailinglist': self }
        ctx.update(kwargs)
        return render_to_string([
            'mailinglist/plugin.html',
        ], ctx, context_instance=kwargs.get('context'))
