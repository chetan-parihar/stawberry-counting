import numpy as np
import cv2 

vdo="video.mp4"
cam=cv2.VideoCapture(vdo)
detections=[]
f_list=[]

num=1
while True:

    close_f,frame=cam.read()#repet video

    if close_f is False:
        cam=cv2.VideoCapture(vdo)
        close_f,frame=cam.read()

    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)#convert to thresh
    
    
    hsv=cv2.GaussianBlur(hsv,(11,11),0)
    l_b=np.array([3,133,86])
    u_b=np.array([24,255,255])
    mask=cv2.inRange(hsv,l_b,u_b)
    
    hsv_frame=cv2.bitwise_and(frame,frame,mask=mask)
    gray_frame=cv2.cvtColor(hsv_frame,cv2.COLOR_BGR2GRAY)
    _,threshold=cv2.threshold(gray_frame,1,255,cv2.THRESH_BINARY)
    threshold[600:2000,1000:1500]=0
    threshold[10:600,850:1500]=0

    contours,_=cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    len_of_counts=len(contours)
    # print(len_of_counts)
#object detection
    for cnt in contours:
        
        if cv2.contourArea(cnt)>190:
            (x,y,w,h)=cv2.boundingRect(cnt)

            # detections.append([x,y,w,h])
            lenth_of_f_lis=len(f_list)

            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            # temp_list.append([x,y,w,h])


            if len(f_list)<=0:              # IF EMTY LIST THEN ADD 
                f_list.append([x,y,w,h])


            if len(f_list)>0:               #  IF NOT EAMTY THEN CHECK IS IT THEAR OR NOT
                temp_list=[]    

                for i in range(0,lenth_of_f_lis):
                    
                    t_x=f_list[i][0]
                    t_y=f_list[i][1]
                    t_w=f_list[i][2]
                    t_h=f_list[i][3]
                    
                    t_cx = (t_x + t_x + t_w) // 2
                    t_cy = (t_y + t_y + t_h) // 2   


                    # t_cx=f_list[i][0]
                    # t_cy=f_list[i][1]
                    n=50
                    if ((t_cx+n >=cx) and (t_cx-n<=cx))and((t_cy+n) >=cy and (t_cy-n)<=cy):
                        f_list[i][0]=x
                        f_list[i][1]=y
                        f_list[i][2]=w
                        f_list[i][3]=h


                        break
                        
                    else:
                        temp_list.append([x,y,w,h])
                        
                        if len(temp_list)>=lenth_of_f_lis:
                            f_list.append([x,y,w,h])
                            num=num+1

                    if len(f_list)>15:
                        f_list.pop(0)
            
            
            # print(f_list)
            cv2.rectangle(frame,(0,10),(500,200),(0,0,0),-1)
            cv2.putText(frame,str("Stawberry's"),(270,150),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),1)
            cv2.putText(frame,str(num),(290,100),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,100),2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,250),2)
            cv2.circle(frame,(cx,cy),1,(255,0,0),3)
    frame=frame[30:1000,250:3500]
    cv2.imshow("frame",frame)

    key=cv2.waitKey(1)
    
    
    if key==ord("q"):
        break