from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.translation import gettext_lazy as _

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        if not user.id:
            user.email = sociallogin.account.extra_data.get('email', '')
            user.first_name = sociallogin.account.extra_data.get('given_name', '')
            user.last_name = sociallogin.account.extra_data.get('family_name', '')
            user.save()
        return user
