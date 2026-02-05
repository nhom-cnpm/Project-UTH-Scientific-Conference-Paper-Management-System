from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import USER

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return JsonResponse({"error": "Thiếu dữ liệu"}, status=400)

    # check trùng
    if NguoiDung.objects.filter(TaiKhoan=username).exists():
        return JsonResponse({"error": "Tài khoản đã tồn tại"}, status=400)

    user = NguoiDung.objects.create(
        TaiKhoan=username,
        MatKhau=password,
        Email=email,
        VaiTro="Member"
    )

    return JsonResponse({
        "message": "Đăng ký thành công",
        "id": user.MaNguoiDung
    })
