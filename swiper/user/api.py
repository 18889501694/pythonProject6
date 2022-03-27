from django.core.cache import cache
from lib.http import render_json
from user.logic import send_verify_code, check_vcode, save_upload_file
from user.models import User
from common import error
from user.forms import ProfileForm


def get_verify_code(request):
    """手机注册"""

    phonenum = request.GET.get('phonenum')
    send_verify_code(phonenum)
    return render_json(None)


def login(request):
    """短信验证登录"""

    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    if check_vcode(phonenum, vcode):
        # 获取用户
        user, created = User.objects.get_or_create(phonenum=phonenum)
        # 记录登录状态
        request.session['uid'] = user.id
        return render_json(user.to_dict())

    else:
        return render_json(None, error.VCODE_ERROR)


def get_profile(request):
    """获取个人资料"""
    user = request.user
    key = 'Profile-%s' % user.id
    user_profile = cache.get(key)  # 从缓存里取
    print('从缓存获取:{}'.format(user_profile))
    if not user_profile:  # 缓存里不存在时执行以下命令
        user_profile = user.profile.to_dict()  # 存入数据库
        print('从数据库获取:{}'.format(user_profile))
        cache.set(key, user_profile)  # 数据库存到缓存里面
        print('将数据添加到缓存')
    return render_json(user_profile)  # 如果缓存里匹配到相应数据则return返回


def modify_profile(request):
    """修改个人资料"""
    form = ProfileForm(request.POST)
    if form.is_valid():
        user = request.user
        user.profile.__dict__.update(form.cleaned_data)
        user.profile.save()

        # 修改缓存,保持数据库与缓存不同一致性
        key = 'Profile-%s' % user.id
        cache.set(key, user.profile.to_dict())
        return render_json(None)
    else:
        return render_json(form.errors, error.PROFILE_ERROR)


def upload_avatar(request):
    """头像上传
        1.接收用户上传的头像
        2.定义用户头像名称
        3.异步将头像上传七牛云
        4.将URL保存到数据库
    """
    file = request.FILES.get('avatar')
    if file:
        save_upload_file(request.user, file)
        return render_json(None)
    else:
        return render_json(None, error.FILE_NOT_FOUND)
