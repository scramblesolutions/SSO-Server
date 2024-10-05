from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Vendor, Pseudonym

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