from livinglots_pathways.views import (BasePathwaysDetailView,
                                       BasePathwaysListView)

from .models import Pathway


class PathwaysFeinCMSMixin(object):

    def render_to_response(self, context, **response_kwargs):
        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            return self.get_template_names(), context

        return super(PathwaysFeinCMSMixin, self).render_to_response(
            context, **response_kwargs)


class PathwaysDetailView(BasePathwaysDetailView):
    model = Pathway


class PathwaysListView(BasePathwaysListView):
    model = Pathway
