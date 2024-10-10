from oidc_provider.models import Client
from oidc_provider.scopes import ScopeClaims
from .models import Vendor, Pseudonym

class CustomScopeClaims(ScopeClaims):

    def create_response_dic(self):
        # Get the client_id from the token
        client_id = self.token.client.client_id

        # Get or create the vendor
        vendor, _ = Vendor.objects.get_or_create(client_id=client_id)

        # Get or create the pseudonym for this user and vendor
        pseudonym, _ = Pseudonym.objects.get_or_create(user=self.user, vendor=vendor)

        # Use the pseudonym instead of the real user id
        self.id_token.update({
            'sub': str(pseudonym.pseudonym),
        })

        return super().create_response_dic()

    def info_profile(self):
        # This scope is used to share basic profile information
        return {
            'name': self.user.get_full_name(),
            'given_name': self.user.first_name,
            'family_name': self.user.last_name,
            'email': self.user.email,
            'nickname': self.user.username,
        }

    def info_picture(self):
        # This scope is used to share the user's profile picture
        profile = self.user.profile
        return {
            'picture': profile.profile_image.url if profile.profile_image else None,
        }

    def info_bio(self):
        # This scope is used to share the user's bio
        profile = self.user.profile
        return {
            'bio': profile.bio,
        }