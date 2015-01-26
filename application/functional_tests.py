from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.utils import override_settings
from selenium import webdriver


class ApplicationFunctionalTests(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def input_into(self, id, value):
        # a helper method to enter a value into a field given that field's id
        element = self.browser.find_element_by_id(id)
        element.send_keys(value)

    def test_happy_path(self):
        # test that a user can provide the minimum required amount of data
        # to the form and submit successfully

        # the user navigates to the site
        self.browser.get('localhost:8081')
        self.assertIn('Hebrew Order of David', self.browser.title)

        # the user enters a valid email address
        self.input_into('id_email', 'test@test.com')

        # the user enters a valid first name
        self.input_into('id_first_name', 'Robert')

        # the user enters a valid last name
        self.input_into('id_last_name', 'Smith')

        # the user enters a valid home address
        self.input_into('id_home_address', '123 Main St.')

        # the user enters a valid home city
        self.input_into('id_home_city', 'Dallas')

        # the user enters a valid home state
        self.input_into('id_home_state', 'TX')

        # the user enters a valid home zip
        self.input_into('id_home_zip', '78001')

        # the user enters a valid home phone
        self.input_into('id_home_phone', '123-456-7890')

        # the user enters a valid work phone
        self.input_into('id_work_phone', '456-123-7890')

        # the user enters a valid mobile phone
        self.input_into('id_mobile_phone', '789-123-4560')

        # the user enters an occupation
        self.input_into('id_occupation', 'Web Application Tester')

        # the user enters a business name
        self.input_into('id_business_name', 'Web Testers R Us')

        # the user enters a business address
        self.input_into('id_business_address', '789 South St.')

        # the user enters a business city
        self.input_into('id_business_city', 'Dallas')

        # the user enters a business state
        self.input_into('id_business_state', 'TX')

        # the user enters a business zip
        self.input_into('id_business_zip', '12345')

        # the user enters a city of birth
        self.input_into('id_city_of_birth', 'Dallas')

        # the user enters a country of birth
        self.input_into('id_country_of_birth', 'USA')

        import ipdb; ipdb.set_trace()

        # the user clicks the submit button
        button = self.browser.find_element_by_class_name('submit-application')
        button.click()
