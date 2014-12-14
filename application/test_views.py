from django.test import TestCase, Client


# Create your tests here.
class RoutesTest(TestCase):
    """Test that URL routes return working pages."""
    def test_new(self):
        c = Client()
        response = c.get('/')
        self.assertEquals(response.status_code, 200)
        response = c.get('/polls')
        self.assertEquals(response.status_code, 200)
        response = c.get('/post')
        self.assertEquals(response.status_code, 200)
