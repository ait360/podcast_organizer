from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .forms import UserCreationForm, UserUpdateForm

from .models import User, Profile

from allauth.account.forms import SignupForm





# Register your models here.

class ProfileAdminInline(admin.StackedInline):
    can_delete = False
    model = Profile
    #exclude = ('slug',)

    def view_on_site(self, obj):
        return obj.get_absolute_url()

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = ('username', 'email', 'get_name', 'get_date_joined')
    list_display_links = ('username', 'email')
    ordering = ('email', 'username')
    search_fields = ('username','get_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('email', 'display_picture', 'cover_picture')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', )}), #'date_joined'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    form = UserUpdateForm
    add_form = UserCreationForm
    change_user_password_template = 'admin/auth/user/change_password.html'


    def get_name(self, user):
        return user.profile.name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'profile__name'

    def get_date_joined(self, user):
        return user.date_joined
    get_date_joined.short_description = 'Joined'
    get_date_joined.admin_order_field = 'user__date_joined'

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return tuple()
        inline_instance = ProfileAdminInline(self.model, self.admin_site)
        return (inline_instance,)
