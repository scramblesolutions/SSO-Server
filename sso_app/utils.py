# utils.py
from oidc_provider.lib.claims import ScopeClaims

class CustomScopeClaims(ScopeClaims):
    print('yes there')
    info_profile = (
        'profile_detail',
        'Access to profile details i.e. profile image and bio',
    )

    def _claim_profile(self):
        print('yes there')
        dic = super(CustomScopeClaims, self)._claim_profile()
        if dic is None:
            dic = {}
        dic['profile_image'] = self.user.profile.profile_image.url if self.user.profile.profile_image else ''
        dic['bio'] = self.user.profile.bio
        return dic
