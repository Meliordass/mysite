import shutil
from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.conf import settings
import hashlib
from app01 import models
from app01.models import Img, dImg
from yolov5 import detect
import argparse
import os
import sys
from pathlib import Path


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


class LoginForm(forms.Form):
    username = forms.CharField(label='username',
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=True
                               )
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def home_view(request):
    if request.method == "GET":
        return render(request, 'home_view.html')
    form = LoginForm(data=request.POST)
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    print(user,pwd)
    if user != None and pwd != None:
        if len(models.Admin.objects.filter(username=user,password=pwd)) != 0:
            return redirect("/showImg/")
    return render(request, 'home_view.html', {'form': form})


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    repwd = request.POST.get('repwd')
    if pwd == repwd:
        pass
    else:
        from django.core.exceptions import ValidationError
        raise ValidationError('密码输入不一致')
    print(user,pwd,repwd)
    models.Admin.objects.create(username=user, password=pwd)
    return redirect("/")


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))


def parse_opt(op):

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / r'D:\DLModles\weights\yolov5n-7-k5.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default=op, help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--data', type=str, default=ROOT / r'D:\DLModles\datas\vec\data.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args(args=[])
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    return opt


def uploadImg(request):
    if request.method == 'POST':
        img = Img(img_url=request.FILES.get('img'))
        img.save()
    return render(request, 'imgUpload.html')


def showImg(request):
    imgs = Img.objects.all()
    for i in imgs:
        print(i.img_url)
    # print('img_path:'+imgs[0])
    # print(type(imgs))
    context = {
        'imgs' : imgs
    }
    return render(request, 'showImg.html', context)


def deleteImg(request):
    nid = request.GET.get('nid')

    Img.objects.filter(id=nid).delete()

    return redirect("/showImg/")


def queryImg(request,sid):
    if request.method == "GET":

        row_object = dImg.objects.filter(did_id=sid).last()

        return render(request, 'queryImg.html', {"row_object": row_object})

    return redirect("/showImg/")


def detectImg(request):
    nid = request.GET.get('nid')
    now = Img.objects.filter(id=nid).first().img_url
    now_path = 'D:\pycoder\django_projects\mysite\media' + '\\' + str(now)
    opt = parse_opt(now_path)
    detect.main(opt)
    thi = detect.pp.replace('\\','/')

    # print('thi:'+thi)
    # print('now_path'+now_path)

    # strs = detect.run().replace('\\','/')
    # print(strs)
    # str_path = 'D:\pycoder\django_projects\mysite' + '\\' + strs
    # str_path = str_path.replace('/','\\')
    # dImg.objects.create(img_url=str(strs), did_id=nid)
    # dImg.objects.create(img_url=str_path,did_id=nid)

    nn = shutil.move(thi, 'media')
    dImg.objects.create(img_url=thi, did_id=nid)
    dImg.objects.create(img_url=nn, did_id=nid)
    return redirect("/showImg/")


# def selfshow(request,uid):
#     if request.method == "GET":
#
#         row_object = models.Admin.objects.filter(id=uid).last()
#
#         return render(request, 'selfshow.html', {"row_object": row_object})
#
#     return redirect("/showImg/")