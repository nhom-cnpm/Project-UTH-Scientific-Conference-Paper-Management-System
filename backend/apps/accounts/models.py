from django.db import models

class USER(models.Model):
    MaNguoiDung = models.AutoField(primary_key=True)
    HoTen = models.CharField(max_length=100)
    TaiKhoan = models.CharField(max_length=50, unique=True)
    MatKhau = models.CharField(max_length=255)
    Email = models.EmailField()
    VaiTro = models.CharField(max_length=20, default="Member")

    class Meta:
        db_table = "USER"

