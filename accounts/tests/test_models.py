from django.contrib.auth import get_user_model
from django.test import TestCase


class TestCustomUser(TestCase):

    def setUp(self):
        # Note: Use -v 3 option!
        # print("# {} is running!".format(self.id()))
        pass

    def test_post_login(self):
        """
        post_login() を実行すると login_count が +1 されて保存されることを検証
        """
        # テストで利用するレコードを作成
        user = get_user_model().objects.create_user('user', password='pass')

        # 事前状態の検証
        self.assertEqual(user.login_count, 0)

        # テスト対象メソッドを呼び出す
        user.post_login()

        # 事後状態の検証
        self.assertEqual(user.login_count, 1)
        self.assertEqual(get_user_model().objects.get(pk=user.id).login_count, 1)
