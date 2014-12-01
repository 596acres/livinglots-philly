from django.conf.urls import patterns, url

from .views import AddFriendlyOwnerView, AddFriendlyOwnerSuccessView


urlpatterns = patterns('',
    url(r'^add/$', AddFriendlyOwnerView.as_view(), name='add'),

    url(r'^add/success/$', AddFriendlyOwnerSuccessView.as_view(),
        name='add_success'),
)
