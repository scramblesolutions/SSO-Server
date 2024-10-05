from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Vendor, Pseudonym
from oidc_provider.models import Client, Token, RSAKey, ResponseType
from oidc_provider.lib.utils.token import create_token
from django.utils import timezone
from datetime import timedelta
import json

User = get_user_model()

class VendorModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            client_id="test_client_id"
        )

    def test_vendor_creation(self):
        self.assertEqual(self.vendor.name, "Test Vendor")
        self.assertEqual(self.vendor.client_id, "test_client_id")

class PseudonymModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123"
        )
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            client_id="test_client_id"
        )
        self.pseudonym = Pseudonym.objects.create(
            user=self.user,
            vendor=self.vendor
        )

    def test_pseudonym_creation(self):
        self.assertIsNotNone(self.pseudonym.pseudonym)
        self.assertEqual(self.pseudonym.user, self.user)
        self.assertEqual(self.pseudonym.vendor, self.vendor)

    def test_pseudonym_uniqueness(self):
        # Attempt to create another pseudonym for the same user-vendor pair
        with self.assertRaises(Exception):  # This should raise an IntegrityError
            Pseudonym.objects.create(
                user=self.user,
                vendor=self.vendor
            )

    def test_different_pseudonyms_for_different_vendors(self):
        another_vendor = Vendor.objects.create(
            name="Another Vendor",
            client_id="another_client_id"
        )
        another_pseudonym = Pseudonym.objects.create(
            user=self.user,
            vendor=another_vendor
        )
        self.assertNotEqual(self.pseudonym.pseudonym, another_pseudonym.pseudonym)

class UserInfoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123"
        )
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            client_id="test_client_id"
        )
        self.oidc_client = Client.objects.create(
            name="Test Client",
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uris=["http://example.com"],
        )
        
        # Create response types
        code_response_type, _ = ResponseType.objects.get_or_create(value='code')
        token_response_type, _ = ResponseType.objects.get_or_create(value='token')
        id_token_response_type, _ = ResponseType.objects.get_or_create(value='id_token')
        
        # Add response types to the client
        self.oidc_client.response_types.add(code_response_type, token_response_type, id_token_response_type)
        
        # Create an RSA key for token signing
        RSAKey.objects.create(key='testkey')
        
        # Create a token
        token = create_token(self.user, self.oidc_client, [])
        
        # Create an access token
        self.access_token = Token.objects.create(
            user=self.user,
            client=self.oidc_client,
            expires_at=timezone.now() + timedelta(days=1),
            _scope='openid profile',
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            _id_token=json.dumps(token.id_token)
        )

    def test_userinfo_with_pseudonym(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.access_token.access_token}'
        }
        response = self.client.get(reverse('oidc_provider:userinfo'), **headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotEqual(data['sub'], str(self.user.id))
        pseudonym = Pseudonym.objects.get(user=self.user, vendor=self.vendor)
        self.assertEqual(data['sub'], str(pseudonym.pseudonym))