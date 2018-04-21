from django.core.exceptions import PermissionDenied
from django.urls import reverse


class SitePermissionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # リクエストへの前処理をここに記述

        response = self.get_response(request)

        # レスポンスへの後処理をここに記述

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ビューを呼び出す直前に呼び出される処理"""
        has_site_permission = False
        if request.user.is_superuser or request.user.is_staff:
            has_site_permission = True

        admin_index = reverse('admin:index')
        # 権限を持っていないユーザーが「/admin/」配下にアクセスしたら 403エラー
        if request.path.startswith(admin_index):
            if not has_site_permission:
                raise PermissionDenied

        request.user.has_site_permission = has_site_permission
