#coding=utf-8
from PIL import Image  
import pylab
import os
import time
import random
from PIL import ImageDraw
import numpy as np


cut = 'adb shell screencap -p /sdcard/autojump.png'
push = 'adb pull /sdcard/autojump.png . '
jump = 'adb shell input swipe {x} {y} {x} {y} {time}'
diff_num=int(30)
def cha(a,b):
    if a>b:
        return a-b
    else:
        return b-a

#draw.ellipse((x1-10,y1-10,x1+10,y1+10),'yellowgreen','wheat')
#region.show()


while True:
    #1
    
    #手机截屏
    os.system(cut)
    time.sleep(0.01)

    #截图上传
    os.system(push)
    time.sleep(0.03)
    #2
    
    im=Image.open(r"autojump.png")
    #im.show()
    im.convert("RGB")
    box=(0,400,1080,1920)
    region=im.crop(box)
    pic=np.array(region)
    (w,h)=region.size
    pix=region.load()
    draw=ImageDraw.Draw(region)

    
    def getTopPoint():
        #region.show()
        '''
        for i in range(0,1519):
            for j in range(0,1079):
                    for k in range(0,3):
                            print(im[i:j:k])
                    print('|')
            print('\n')

        ''' 
        topx=-1
        topy=-1
        print(w,' ',h)
        for j in range(1,h-1):
            for i in range(0,w-1):
                (h1,h2,h3,xx)=pix[i,j];
                (h4,h5,h6,yy)=pix[i,j-1];
                sum=cha(h1,h4)+cha(h2,h5)+cha(h3,h6)
                if sum>diff_num:
                    print(i,j,pix[i,j])
                    topx=i
                    topy=j
                    break
            if topx!=-1:
                for i in range(w-1,0,-1):
                    '''
                    sum=0
                    for k in range(0,2):
                        sum+=cha(pix[i,j,k],pix[0,0,0])
                    '''
                    (h1,h2,h3,xx)=pix[i,j];
                    (h4,h5,h6,yy)=pix[i,j-1];
                    sum=cha(h1,h4)+cha(h2,h5)+cha(h3,h6)
                    if sum>diff_num:
                        print(i,j,pix[i,j])
                        topx=(topx+i)//2
                        break
                break
                    
        print(topx,' ',topy)
        print(pix[0,0])
        draw.ellipse((topx-10,topy-10,topx+10,topy+10),'yellowgreen','wheat')
        return (topx,topy)

    def getNowPoint():
        Nowx=-1
        Nowy=-1
        for i in range(0,w-1):
            for j in range(0,h-1):
                if pix[i,j]==(43,43,73,255) and i+73<h and j+1<w and pix[i+73,j+1]==(58,54,81,255):
                    Nowx=i
                    Nowy=j
        Nowx+=37
        print(Nowx,' ',Nowy)
        draw.ellipse((Nowx-10,Nowy-10,Nowx+10,Nowy+10),'yellowgreen','wheat')
        return (Nowx,Nowy)

    def getAimPoint(x1,y1,x2,y2):
        k=(990-873)/(378-177)
        y1=y2-k*cha(x1,x2)
        print(x1,' ',y1)
        draw.ellipse((x1-10,y1-10,x1+10,y1+10),'yellowgreen','wheat')
        return (x1,y1)
                    
    (x1,y1)=getTopPoint()
    (x2,y2)=getNowPoint()
    (x1,y1)=getAimPoint(x1,y1,x2,y2)
    #region.show()
    #3
    
    #两点距离公式
    s = (cha(x1,x2)**2 + cha(y1,y2)**2)**0.5
    
    #手指点击位置一般在中间偏下。取随机值混淆系统检测

    w = int(w*random.uniform(0.45,0.55))
    h = int(h*random.uniform(0.7,0.8))

    
    #print(s)1.38 2.05

    #分辨率与按压时间(ms)的系数
    ratio = 1.38

    #随机更改按压时间使他不是一个整百数
    s = s*ratio + random.randint(-10,10)  
    s = int(s)

    #pylab.close()
    #像手机发送跳远按压时间
    os.system(jump.format(x=w,y=h,time=s))
    time.sleep((s+500)/1000)
    input("Press enter key to continue...")
    #4
    
    #break
