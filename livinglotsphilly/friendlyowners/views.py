from django.core.urlresolvers import reverse

from livinglots_friendlyowners.views import (BaseAddFriendlyOwnerView,
                                             BaseAddFriendlyOwnerSuccessView)

from .forms import FriendlyOwnerForm
from .models import FriendlyOwner


class AddFriendlyOwnerView(BaseAddFriendlyOwnerView):
    form_class = FriendlyOwnerForm
    model = FriendlyOwner

    def get_success_url(self):
        return reverse('friendlyowners:add_success')


class AddFriendlyOwnerSuccessView(BaseAddFriendlyOwnerSuccessView):
    pass
