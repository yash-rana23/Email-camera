import cv2
import smtplib
import winsound
import imghdr


from email.message import EmailMessage

msg=EmailMessage()
msg['Subject']='Alert : Intruder'
msg['From']='Sender email'
msg['To']='Recievers Email'
msg.set_content("Hye , There is an intruder in your house . We are ATTaching the images below donot forget to check them out ")






camera = cv2.VideoCapture("theif3.mp4")
i=0
while camera.isOpened():
   r, frame = camera.read()
   r, frame2 = camera.read()
   difference = cv2.absdiff(frame, frame2)
   gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
   blur = cv2.GaussianBlur(gray, (5, 5), 0)
   _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
   dil = cv2.dilate(thresh, None, iterations=3)
   contours, _ = cv2.findContours(dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   count=1

   for c in contours:
        if cv2.contourArea(c) < 9000:
           continue
         
        winsound.PlaySound('f2.wav',winsound.SND_ASYNC)
        cv2.imwrite("location for output images in local" % i, frame2)
       
        with open('location of output images with name' % i,'rb') as m:
         file_data=m.read()
         file_type=imghdr.what(m.name)
         file_name=m.name
        msg.add_attachment(file_data, maintype = 'image',subtype=file_type,filename = file_name)
            

        
        i+=1
        if i%10==0:
           server=smtplib.SMTP_SSL('smtp.gmail.com',465)
           server.login("your email","Password")
           server.send_message(msg)
           print("email sent")
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
   
    
       
        
   
   if cv2.waitKey(10) ==ord('q'):
       break
   
   cv2.imshow("output",blur)
   cv2.imshow("output2",frame)





