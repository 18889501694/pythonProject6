import logging

from common import error
from lib.http import render_json

log = logging.getLogger('err')


def perm_require(perm_name):
    def deco(view_func):
        def wrap(request):
            user = request.user
            if user.vip.has_perm(perm_name):
                response = view_func(request)
                return response
            else:
                # 前端提示客户没有权限
                log.error(f'{request.user.nickname}not has{perm_name}')
                return render_json(None, error.NOT_HAS_PERM)

        return wrap

    return deco
