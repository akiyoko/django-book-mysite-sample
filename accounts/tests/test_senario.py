import os

import chromedriver_binary
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class TestLoginSenario(StaticLiveServerTestCase):
    """ログインのシナリオテスト

    https://chromedriver.chromium.org/downloads
    を確認し、Chromeのバージョンに合わせてchromedriver-binaryをインストールする。
    例えば、Chromeのバージョンが76であれば、pip install chromedriver-binary==76.0.3809.126.0
    """

    SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # エラー時のスクリーンショット格納ディレクトリを作成
        os.makedirs(cls.SCREENSHOT_DIR, exist_ok=True)

        # Note: ChromeDriverのパスを通すためにimportが必要
        print(chromedriver_binary.chromedriver_filename)
        chrome_options = webdriver.ChromeOptions()
        # headlessモード
        # chrome_options.add_argument('--headless')
        cls.selenium = webdriver.Chrome(chrome_options=chrome_options)
        cls.selenium.implicitly_wait(5)

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com', password='secret')
        # 前回エラー時のスクリーンショットを削除しておく
        if os.path.exists(self._get_screenshot_filepath()):
            os.remove(self._get_screenshot_filepath())

    def tearDown(self):
        # スクリーンショットを撮る
        self.selenium.save_screenshot(self._get_screenshot_filepath())
        # # エラーが発生したらスクリーンショットを撮る
        # for method, error in self._outcome.errors:
        #     if error:
        #         self.selenium.save_screenshot(self._get_screenshot_filepath())
        #         break
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        # Note: ChromeDriverをheadlessモードで利用する場合、
        #       tearDownClassでcls.selenium.quit()を実行すると、
        #       「ConnectionResetError: [WinError 10054] 既存の接続はリモート ホストに強制的に切断されました。」
        #       というエラーが頻繁に発生してしまう
        cls.selenium.quit()
        super().tearDownClass()

    def _get_screenshot_filepath(self):
        return os.path.join(self.SCREENSHOT_DIR, '{}.png'.format(self.id()))

    def test_login(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/admin/login/'))
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//input[@value="ログイン"]').click()
        self.assertEqual(self.selenium.title, "サイト管理 | Django サイト管理")
