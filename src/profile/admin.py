from sqladmin import ModelView

from src.profile.models import Profile


class ProfileAdmin(ModelView, model=Profile):
    column_list = [Profile.id, Profile.name, Profile.created_at]
    icon = 'fa fa-'
    column_sortable_list = [Profile.id, Profile.name, Profile.created_at]
    column_default_sort = (Profile.created_at, True)
    page_size = 50
    page_size_options = [25, 50, 100, 200]