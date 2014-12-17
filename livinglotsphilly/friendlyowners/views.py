from django.core.urlresolvers import reverse

from livinglots_friendlyowners.views import (BaseAddFriendlyOwnerView,
                                             BaseAddFriendlyOwnerSuccessView)

from lots.models import Lot
from phillydata.waterdept.models import WaterParcel
from .forms import FriendlyOwnerForm
from .models import FriendlyOwner


class AddFriendlyOwnerView(BaseAddFriendlyOwnerView):
    form_class = FriendlyOwnerForm
    model = FriendlyOwner

    def get_initial(self):
        initial = super(AddFriendlyOwnerView, self).get_initial()

        # Add parcel(s)
        parcels = WaterParcel.objects.filter(pk=self.request.GET.get('parcels', None))
        initial['parcels'] = parcels
        return initial

    def get_success_url(self):
        if self.request.user.has_perm('friendlyowners:moderate_friendlyowner'):
            return reverse('lots:lot_detail', kwargs={
                'pk': Lot.objects.get(friendlyowner=self.object).pk
            })
        return reverse('friendlyowners:add_success')


class AddFriendlyOwnerSuccessView(BaseAddFriendlyOwnerSuccessView):
    pass
