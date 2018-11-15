# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 10:49:32 2018
@author: XinjiaLi
python2
"""

import cv2
import urllib2
import time
import os
http_url='https://api-cn.faceplusplus.com/facepp/v3/detect' #face++ API url
key = "sJVodwPAjfbo18Vc2OCZjIUuM1u2BhMe" #my free key
secret = "29dB1GxL9oXbv7P117CLa4ZyUdHzj0wp" # my secret

def recommend_book(index,imgs,class_name,window):
    print(index)
    j = index
    if j == 1:
        #根据年龄和类别读取第一张推荐商品图片，由于用户不可选"查看上一张"，因此代码单独写
        recommend = cv2.imread('images'+'/'+class_name+'/'+imgs[j-1]) #该类人群推荐第一张书籍的路径
        recommend = cv2.resize(recommend, (804,1024)) #统一尺寸，基本按照我个人电脑的大小，选用一般书籍长宽比
        cv2.putText(recommend,' [d] for the next, [o] to quit',(200,40),cv2.FONT_HERSHEY_COMPLEX,0.8,(0, 0, 256),1) #用户提示语
        cv2.imshow(window,recommend) #展示推荐书籍
        kkk = cv2.waitKey() #等待用户键入
        while ((kkk != ord('d')) and (kkk != ord('o'))): #用户只可键入'd'查看下一页和'o'退出推荐界面,否则无效
            kkk = cv2.waitKey()
        if kkk == ord('d'): #查看下一页
            j = j + 1
            recommend_book(j,imgs,class_name,window)              
        elif kkk == ord('o'):  #退出推荐界面,destroy推荐window.
            cv2.destroyWindow(window)   
    else:
        recommend = cv2.imread('images'+'/'+class_name+'/'+imgs[j-1]) #若不是第一本推荐书籍,用户可选择查看上一页、下一页和退出
        recommend = cv2.resize(recommend, (804,1024)) #统一尺寸
        cv2.putText(recommend,'[d] for the next, [u] for the last, [o] to quit',(70,40),cv2.FONT_HERSHEY_COMPLEX,0.8,(0, 0, 256),1) #用户提示语
        cv2.imshow(window,recommend) #展示推荐书籍
        k = cv2.waitKey() #等待用户键入
        while ((k != ord('d')) and (k !=  ord('u')) and (k != ord('o'))): #用户只可键入'u'查看上一页,'d'查看下一页和'o'退出推荐界面,否则无效
            k = cv2.waitKey()
        if k == ord('d'): #查看下一页
            j = j + 1
            if j <= len(imgs)-1: 
                recommend_book(j,imgs,class_name,window)
            elif j == len(imgs): #若下一页是最后一页，用户在最后一页不可选择查看下一页，因此代码单独写
                recommend = cv2.imread('images'+'/'+class_name+'/'+imgs[j-1])
                recommend = cv2.resize(recommend, (804,1024)) #统一尺寸
                cv2.putText(recommend,'[u] for the last,[o] to quit',(200,40),cv2.FONT_HERSHEY_COMPLEX,0.8,(0, 0, 256),1)  #用户提示语
                cv2.imshow(window,recommend) #展示推荐书籍
                kk = cv2.waitKey() #等待用户键入
                while ((kk != ord('o')) and (kk !=  ord('u'))):  #用户只可键入'u'查看上一页和'o'退出推荐界面,否则无效
                    kk = cv2.waitKey()
                if kk == ord('o'):
                    cv2.destroyWindow(window)
                elif kk == ord('u'):
                    j = j - 1
                    recommend_book(j,imgs,class_name,window)
        elif k == ord('u'):
            j = j - 1
            recommend_book(j,imgs,class_name,window)
        elif k == ord('o'):
            cv2.destroyWindow(window)

cap = cv2.VideoCapture(0) #调用摄像头

#cap.set(640.0 x 480.0) #设置分辨率，当前选用默认分辨率
#只能是如下选择分辨率.
#160.0 x 120.0
#176.0 x 144.0
#320.0 x 240.0
#352.0 x 288.0
#640.0 x 480.0
#1024.0 x 768.0
#1280.0 x 1024.0

i = 1 #截图的用户头像图片保存到本地时计数
while(1):
    ret,frame = cap.read()
    #摄像头截取头像界面的参数,各参数依次是：照片/添加的文字/左上角坐标/字体/字体大小/颜色/字体粗细
    cv2.putText(frame,'please input [s] and get your result',(70,40),cv2.FONT_HERSHEY_COMPLEX,0.8,(0, 0, 256),1)
    #设置摄像头的尺寸，这里对默认尺寸做了长宽各2倍放大
    frame = cv2.resize(frame,None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    cv2.imshow("capture",frame) #展示摄像头
    k=cv2.waitKey(100) #等待键入,100是100个键入.
    if k == ord('q'): #用户键入'q'则退出摄像头界面
        break;
    elif k==ord('s'): #用户键入's'进入推荐书籍进程
        filepath = 'faces/' + str(i) + '.jpg'  #截图的保存路径,i为本次系统开启第i张图片
        i = i + 1

        #将保存的截图写入本地
        cv2.imwrite(filepath, frame)

        #调用face++人脸识别API获得用户年龄和性别信息，根据face++ API doc改写而来
        boundary = '----------%s' % hex(int(time.time() * 1000))
        data = []
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
        data.append(key)
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
        data.append(secret)
        data.append('--%s' % boundary)
        fr=open(filepath,'rb')
        data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
        data.append('Content-Type: %s\r\n' % 'application/octet-stream')
        data.append(fr.read())
        fr.close()
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
        data.append('1')
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
        data.append("gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
        data.append('--%s--\r\n' % boundary)

        http_body='\r\n'.join(data)
        #buld http request
        req=urllib2.Request(http_url)
        #header
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        req.add_data(http_body)

        try:
            # req.add_header('Referer','http://remotserver.com/')
            resp = urllib2.urlopen(req, timeout=5)
            # get response
            qrcont = resp.read()
            #       print qrcont
            dict = eval(qrcont)
            faces = dict['faces']
            #若有多张人脸，采用最显著的top1人脸进行推荐
            attribute = faces[0]['attributes']
            #目前只选用性别和年龄两个属性
            gender = attribute['gender']['value']
            age = attribute['age']['value']
			
            #根据年龄和性别对人进行分类
            if age < 4:   #类别'0_3'
                  class_name = '0_3'
            elif age < 7: #类别'4_6'
                  class_name='4_6'
            elif age < 13: #类别'7_12'
                  class_name = '7_12'
            elif age < 19:  #类别'13_18'
                  class_name = '13_18'
            elif age < 26:  #类别'19_25'
                  class_name = '19_25'
            elif (age < 40 and gender =='Female'): #类别'26_40_F'
                  class_name = '26_40_F'
            elif (age < 40 and gender =='Male'):  #类别'26_40_M'
                  class_name = '26_40_M'
            elif (age < 60 and gender == 'Female'):  #类别'40_60_F'
                  class_name = '40_60_F'
            elif (age < 60 and gender == 'Male'): #类别'40_60_M'
                  class_name = '40_60_M'
            else:
                  class_name = '60'  #类别'60'
            imgs = os.listdir('images'+'/'+class_name)

            #打开显示window,NORMAL_代表可调整
            cv2.namedWindow('showimage',cv2.WINDOW_AUTOSIZE)
            try:
                j = 1
                recommend_book(j,imgs,class_name,'showimage')
            except :
                cap.release()
                cv2.destroyAllWindows()
    
        #若检测失败（例如不存在人脸，则输出'no face has been detected , try again'）
        except:
            print('no face has been detected , try again')
#关闭摄像头及window
cap.release()
cv2.destroyAllWindows()
