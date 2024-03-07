import cv2
import numpy as np
import face_recognition
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import csv 
path = "ImagesAttendance"
images = []
classNames = []
myList = os.listdir(path)

# Dictionary to store student-parent email mapping
student_parents = {
    "KIRAN HANDE":"kiranhande2001@gmail.com",
    "AVISHKAR DUREKAR":"avishkardurekar171@gmail.com",
    "TUSHAR BHAIREMANE":"tsmane789@gmail.com"
    # Add more students and their parent email addresses
}

attendance_marked = set()  # Set to store the students whose attendance has been marked

for cl in myList:
    curImg = cv2.imread(os.path.join(path, cl))
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    if name in attendance_marked:
        return
    
    if name == "Unknown":
        name = "VISITOR"
        
    # Rest of the code to mark attendance and send email goes here

    
    file_path = 'smart_attendace_system\\Attendance.csv'
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as f:
            f.write('S.No.,Name,Time,Date')
            
    with open(file_path, 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList[1:]:
            entry = line.strip().split(',')
            if len(entry) >= 2:
                nameList.append(entry[1])
        if name not in nameList:
            count = len(myDataList)  # set count to the next available number
            f.write(f'{count},{name},{current_time},{current_date}\n')
            print(f"Attendance marked for {name}")
            attendance_marked.add(name)  # Add the student to the attendance marked set
            
            # send email to parent
            if name in student_parents:
                toaddr = student_parents[name]
                subject = "Attendance Notification"
                body = f"Dear Parent,\nyour child, {name}, is present in class today.\n\nRegards,\nTSSM'S BSCOER NARHE PUNE"

                # create the email message
                msg = MIMEMultipart()
                msg['From'] = "kiranhande8408@gmail.com"
                msg['To'] = toaddr
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                # send the email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("kiranhande8408@gmail.com", 'wiwrunaamfxtkyib')
                server.send_message(msg)
                print(f"Email sent to {toaddr}")

                # close the server connection
                server.quit()
            
    f.close()


encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)

# Send attendance report to teacher
teacher_subject = "Attendance Report"
teacher_body = "Attendance Report attached."

while True:
    ret, frame = cap.read()
    if not ret:
        break

    imgS = cv2.resize(frame, (0, 0), None, 1, 1)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            top, right, bottom, left = faceLoc
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # Detect the eyes in the face
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml').detectMultiScale(gray, 1.3, 5)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            markAttendance(name)
        else:
             name = "Unknown"
             top, right, bottom, left = faceLoc
             cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
             font = cv2.FONT_HERSHEY_DUPLEX
             cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

             markAttendance(name)    

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
fromaddr = 'kiranhande8408@gmail.com'  
recipients = ['kiranhande2001@gmail.com']
# recipients = ['hande6701@gmail.com', 'kiranhande2001@gmail.com','mhaseavi188@gmail.com','snbhore_entc@tssm.edu.in','prajaktagaikwad2013@gmail.com','pnshinde2@gmail.com','vijayjadhav741@gmail.com','sadabadiger@gmail.com']  # list of recipient email addresses
username = 'kiranhande8408@gmail.com'   
password = 'wiwrunaamfxtkyib'
date = datetime.date.today()
subject = "Attendance of {:%d %b %Y}".format(date)

# read the CSV file and create an HTML table
table = '<table border="1">'
with open('smart_attendace_system\\Attendance.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    table += '<tr>{}</tr>'.format(''.join(f'<th>{h}</th>' for h in header))
    for row in reader:
        table += '<tr>{}</tr>'.format(''.join(f'<td>{r}</td>' for r in row))
table += '</table>'
# loop over recipients and send email to each
for toaddrs in recipients:
    # create the email message
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg['Subject'] = subject
    msg.attach(MIMEText(table, 'html'))

    # send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    print('Email sent successfully to', toaddrs)
    server.quit()

 
