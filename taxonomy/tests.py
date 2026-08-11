from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from taxonomy.models import Category, Location, LocationType
from taxonomy.services import detect_user_location

User = get_user_model()

class TaxonomyModelTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        
        # Build Category Tree: World -> Europe -> UK
        self.cat_world = Category.objects.create(name='World', slug='world', display_order=1)
        self.cat_europe = Category.objects.create(name='Europe', slug='europe', parent=self.cat_world, display_order=1)
        self.cat_uk = Category.objects.create(name='UK', slug='uk', parent=self.cat_europe, display_order=1)

        # Build Location Tree: California -> San Francisco
        self.loc_state = Location.objects.create(
            name='California',
            slug='california',
            location_type=LocationType.STATE,
            state_code='CA'
        )
        self.loc_city = Location.objects.create(
            name='San Francisco',
            slug='san-francisco',
            location_type=LocationType.CITY,
            parent=self.loc_state
        )

    def test_category_hierarchy_tree(self):
        self.assertEqual(self.cat_world.get_descendant_count(), 2)
        self.assertIn(self.cat_uk, self.cat_world.get_descendants())
        self.assertEqual(str(self.cat_uk), 'World > Europe > UK')

    def test_location_hierarchy(self):
        self.assertEqual(str(self.loc_city), 'San Francisco, California')
        self.assertEqual(self.loc_city.parent, self.loc_state)
        self.assertIn(self.loc_city, self.loc_state.get_children())

    def test_location_detection_service(self):
        request = self.factory.get('/')
        request.user = User.objects.create_user(username='reader1', email='reader1@example.com', password='pass')
        request.session = {}
        
        detected = detect_user_location(request)
        self.assertEqual(detected, self.loc_state)
