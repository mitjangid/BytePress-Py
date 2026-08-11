from django.test import TestCase
from django.contrib.auth.models import Group
from accounts.models import User, UserProfile, UserRole

class UserAccountTests(TestCase):

    def test_create_standard_user_default_role(self):
        user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='password123'
        )
        self.assertEqual(user.role, UserRole.SUBSCRIBER)
        self.assertFalse(user.is_verified_author)
        self.assertIsNotNone(user.profile)
        self.assertTrue(user.profile.newsletter_opt_in)

    def test_role_group_synchronization(self):
        editor_user = User.objects.create_user(
            username='editorjane',
            email='jane@example.com',
            password='password123',
            role=UserRole.EDITOR
        )
        self.assertTrue(editor_user.is_editor)
        self.assertTrue(editor_user.is_staff)
        self.assertTrue(editor_user.groups.filter(name='Editor').exists())

    def test_author_properties(self):
        author_user = User.objects.create_user(
            username='reporterbob',
            email='bob@example.com',
            password='password123',
            role=UserRole.AUTHOR,
            first_name='Bob',
            last_name='Reporter'
        )
        self.assertTrue(author_user.is_author)
        self.assertFalse(author_user.is_editor)
        self.assertEqual(author_user.display_name, 'Bob Reporter')
