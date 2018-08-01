import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import LoginForm, RegisterForm, ProfileForm

logger = logging.getLogger(__name__)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(reverse('shop:index'))

        context = {
            'form': RegisterForm(),
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        logger.info("You're in post!!!")

        # リクエストからフォームを作成
        form = RegisterForm(request.POST)
        # バリデーション
        if not form.is_valid():
            # バリデーションNGの場合はアカウント登録画面のテンプレートを再表示
            return render(request, 'accounts/register.html', {'form': form})

        # 保存する前に一旦取り出す
        user = form.save(commit=False)
        # パスワードをハッシュ化してセット
        user.set_password(form.cleaned_data['password'])
        # ユーザーオブジェクトを保存
        user.save()

        # ログイン処理（取得した Userオブジェクトをセッションに保存 & Userデータを更新）
        auth_login(request, user)

        return redirect(settings.LOGIN_REDIRECT_URL)


register = RegisterView.as_view()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """GETリクエスト用のメソッド"""
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(reverse('shop:index'))

        context = {
            'form': LoginForm(),
        }
        # ログイン画面用のテンプレートに値が空のフォームをレンダリング
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        """POSTリクエスト用のメソッド"""
        # リクエストからフォームを作成
        form = LoginForm(request.POST)
        # バリデーション（ユーザーの認証も合わせて実施）
        if not form.is_valid():
            # バリデーションNGの場合はログイン画面のテンプレートを再表示
            return render(request, 'accounts/login.html', {'form': form})

        # ユーザーオブジェクトをフォームから取得
        user = form.get_user()

        # ログイン処理（取得したユーザーオブジェクトをセッションに保存 & ユーザーデータを更新）
        auth_login(request, user)

        # ログイン後処理（ログイン回数を増やしたりする。本来は user_logged_in シグナルを使えばもっと簡単に書ける）
        user.post_login()

        # ロギング
        logger.info("User(id={}) has logged in.".format(user.id))

        # フラッシュメッセージを画面に表示
        messages.info(request, "ログインしました。")

        # ショップ画面にリダイレクト
        return redirect(reverse('shop:index'))


login = LoginView.as_view()


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # ロギング
            logger.info("User(id={}) has logged out.".format(request.user.id))
            # ログアウト処理
            auth_logout(request)

        # フラッシュメッセージを画面に表示
        messages.info(request, "ログアウトしました。")

        return redirect(reverse('accounts:login'))


logout = LogoutView.as_view()


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm(None, instance=request.user)
        context = {
            'form': form,
        }
        return render(request, 'accounts/profile.html', context)

    def post(self, request, *args, **kwargs):
        logger.info("You're in post!!!")

        # フォームを使ってバリデーション
        form = ProfileForm(request.POST, instance=request.user)
        if not form.is_valid():
            return render(request, 'accounts/profile.html', {'form': form})

        # 変更を保存
        form.save()

        # フラッシュメッセージを画面に表示
        messages.info(request, "プロフィールを更新しました。")
        return redirect('/accounts/profile/')


profile = ProfileView.as_view()
