# Selects desired class to see if any open spots

# selenium is a package designed to help navigate web pages
from selenium import webdriver

# twilio is a free website that gives you a phone number you can send texts from via python (or others) api
from twilio.rest import Client

import time

data_dict = {
    'subject' : 'CSE',
    'course_number' : '476',
}
while True:
    # using chrome to access web
    driver = webdriver.Chrome(executable_path=r'C:\Users\fulch\PycharmProjects\personal-queue\chromedriver_win32/chromedriver.exe')

    # open website
    driver.get('https://schedule.msu.edu')

    subject_box = driver.find_element_by_id('MainContent_ddlSubject')
    subject_box.send_keys(data_dict['subject'])

    course_number_box = driver.find_element_by_id('MainContent_txtCourseNumber')
    course_number_box.send_keys(data_dict['course_number'])

    submit_button = driver.find_element_by_id('MainContent_btnSubmit')
    submit_button.click()

    enrolled_currently = driver.find_element_by_class_name('enrolled-currently')
    num_enrolled_currently = int(enrolled_currently.text)

    enrollment_limit = driver.find_element_by_class_name('enrollment-limit')
    num_enrollment_limit = int(enrollment_limit.text)

    if num_enrolled_currently < num_enrollment_limit:
        # send open seat notification
        accountSid = 'ACf4c53f1ca6e788b018db6c0ae0406f82'
        authToken = '0c176ca99bfbaed97c0c3c62871c2664'
        twilioClient = Client(accountSid, authToken)
        myTwilioNumber = '+19472829158'
        destCellPhone = '+12489713220'
        subject = data_dict['subject']
        num = data_dict['course_number']
        bdy = f"~{subject} {num} OPEN SEAT~\n{num_enrolled_currently} ENROLLED OUT OF LIMIT {num_enrollment_limit}"
        myMessage = twilioClient.messages.create(body=bdy, from_=myTwilioNumber, to=destCellPhone)
        print("sent text to 2489713220 with body",bdy)
    else:
        print("no open seats at ",end='')
        tm = time.time()
        print(time.ctime(tm))
    driver.close()
    time.sleep(60)