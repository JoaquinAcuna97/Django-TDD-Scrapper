from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import unittest



class StartServer(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.browser.quit()

    def test_can_start_server(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Hotel Scrapping', self.browser.title)
        #self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()