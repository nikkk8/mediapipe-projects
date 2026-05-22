import cv2
import mediapipe as mp

mphands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils

hand=mphands.Hands()

video=cv2.VideoCapture(0)
while True:
    suc,img=video.read()
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hand.process(img1)
    print(result.multi_hand_landmarks)
    tipids=[4,8,12,16,20]
    lmlst=[]
    if result.multi_hand_landmarks:
        for handlm in result.multi_hand_landmarks:
            for id,lm in enumerate(handlm.landmark):
                #print(id,lm)
                lmlst.append([id,lm.x,lm.y])
            #print(lmlst)
            if len(lmlst)==21:
                fingerlist=[]
                #thumb
                if lmlst[20][1]<lmlst[8][1]:
                    if lmlst[4][1]<lmlst[3][1]:
                        fingerlist.append(0)
                    else:
                        fingerlist.append(1)

                else:
                    if lmlst[4][1]>lmlst[3][1]:
                        fingerlist.append(0)
                    else:
                        fingerlist.append(1)

                #other fingers
                for i in range(5):
                    if lmlst[tipids[i]][2]>lmlst[tipids[i]-2][2]:
                        fingerlist.append(0)
                    else:
                        fingerlist.append(1)
                print(fingerlist)
                fingercount=fingerlist.count(1)
                cv2.putText(img,str(fingercount),(35,400),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)

                mp_drawing.draw_landmarks(img,handlm,mphands.HAND_CONNECTIONS)

    cv2.imshow('Webcam',img)
    if cv2.waitKey(1)&0XFF==ord('q'):
        break
video.release()
cv2.destroyAllWindows()