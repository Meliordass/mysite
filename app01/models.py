from django.db import models

class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username

class Img(models.Model):
    img_url = models.ImageField(upload_to='img')

class dImg(models.Model):
    img_url = models.ImageField(upload_to='img')
    did = models.ForeignKey(to='Img', to_field="id",on_delete=models.CASCADE)