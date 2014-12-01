from admin_tools.dashboard import modules

from flatblocks.models import FlatBlock


class EditEmailsModule(modules.DashboardModule):
    slugs = {
        'Organizers welcome': 'organize.mailings.0',
        'Organizers, new file': 'organize.notifications.organizers.new_file',
        'Organizers, new note': 'organize.notifications.organizers.new_note',
        'Organizers, new photo': 'organize.notifications.organizers.new_photo',
    }
    template = 'phillyorganize/admin_dashboard/edit_emails.html'
    title = 'Edit email templates'

    def get_email_template(self, name):
        return {
            'name': name,
            'flatblock': FlatBlock.objects.get(slug=self.slugs[name]),
        }

    def init_with_context(self, context):
        templates = [self.get_email_template(name) for name in self.slugs.keys()]
        context.update({
            'templates': templates,
        })
        return context
