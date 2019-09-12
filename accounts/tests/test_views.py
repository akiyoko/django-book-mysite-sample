from django.contrib.auth import get_user_model
from django.test import TestCase, modify_settings, override_settings


class TestRegisterView(TestCase):
    """RegisterViewのテスト"""

    def setUp(self):
        # Note: Use -v 3 option!
        # print("# {} is running!".format(self.id()))
        # データベースに登録済みのユーザーを self.user にセット
        self.user = get_user_model().objects.create_user(
            username='admin', email='admin@example.com', password='pass')

    def test_get_success(self):
        """
        「/accounts/register/」へのGETリクエストをすると、
        ユーザー登録画面に遷移することを検証
        """
        # テストクライアントでGETリクエストをシミュレート
        response = self.client.get('/accounts/register/')

        # レスポンスを検証する
        self.assertEqual(response.status_code, 200)
        # エラーメッセージが出ないことを検証
        self.assertFalse(response.context['form'].errors)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_get_by_unauthenticated_user(self):
        """
        ログイン済みのユーザーが「/accounts/register/」へのGETリクエストをすると、
        ショップ画面にリダイレクトされることを検証
        """
        # テストクライアントでログインをシミュレート
        # 認証成功なら、クライアント内部の Cookie およびセッションにユーザーの情報を保持
        logged_in = self.client.login(username=self.user.username, password='pass')
        # 念のためログイン成功したかどうかを検証
        self.assertTrue(logged_in)

        # ログイン済みの Cookie を保持したクライアントでGETリクエストを実行
        response = self.client.get('/accounts/register/')

        # レスポンスを検証する
        self.assertRedirects(response, '/shop/')

    def test_post_success(self):
        """
        「/accounts/register/」へのPOSTリクエストをすると、
        ユーザー登録が成功することを検証
        """
        # テストクライアントでPOSTリクエストをシミュレート
        response = self.client.post('/accounts/register/', {
            'username': 'user',
            'email': 'user@example.com',
            'password': 'pass',
            'password2': 'pass',
        })

        # レスポンスを検証する
        self.assertRedirects(response, '/accounts/profile/')
        # 新しいユーザーが登録されたことを検証
        self.assertTrue(get_user_model().objects.filter(username='user').exists())

    def test_post_with_same_username(self):
        """
        「/accounts/register/」へのPOSTリクエストをする際、
        すでに登録済みのユーザーが存在する場合にユーザー登録が失敗することを検証
        """
        # テストクライアントでPOSTリクエストをシミュレート
        response = self.client.post('/accounts/register/', {
            'username': self.user.username,
            'email': self.user.email,
            'password': 'pass',
            'password2': 'pass',
        })

        # レスポンスを検証する
        self.assertEqual(response.status_code, 200)
        # フォームに保持されたエラーメッセージを検証
        self.assertFormError(response, 'form', 'username',
                             '同じユーザー名が既に登録済みです。')
        self.assertTemplateUsed(response, 'accounts/register.html')
        # 新しいユーザーが登録されていないことを検証
        self.assertFalse(get_user_model().objects.filter(username='user').exists())
