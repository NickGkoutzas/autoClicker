# Nick Gkoutzas , Feb 4 2022


from selenium import webdriver
from datetime import datetime , time , date
import time , datetime , os , sys , smtplib , linecache
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.firefox.options import Options


totalUpdateOfTheDay = 200
totalUpdates = 0
numOfMachines = 42      # number of machines
machinesEachUpdate = [int] * numOfMachines
currentPosUpdate = 0    # current position of update

on_time = datetime.datetime.strptime('07:00:00' , '%H:%M:%S').time()    # start updates at this time
off_time = datetime.datetime.strptime('23:55:00' , '%H:%M:%S').time()   # stop updates at this time
now = datetime.datetime.now()

if( int( open("change_delay_once.txt").read() == 1 ) ):
    if(os.path.exists("/home/nick/autoClicker/geckodriver.log")):
        os.remove("/home/nick/autoClicker/geckodriver.log")

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)     # call Firefox 


def updatesStartedAt():
    return ( str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))



def computeDelay(endTimeHours , endTimeMinutes , endTimeSeconds , TotalUpdates__):
    currentTime = datetime.datetime(now.year, now.month , now.day , now.hour , now.minute , now.second)
    finalTime = datetime.datetime(now.year, now.month , now.day , endTimeHours , endTimeMinutes , endTimeSeconds)
    difference = finalTime - currentTime
    return ( ( ( ( ( int(difference.total_seconds() ) / 60 ) / TotalUpdates__) * 60 ) ) - 5 )  # in seconds



def read_delay(file_name):
    delay = open(file_name , 'r')
    numR = delay.read()
    delay.close()
    return float(numR)



def write_delay(file_name , writeDelay):    # in the beginning 'writeDelay' must be '5'... -. 'delay.txt'
    delay = open(file_name , 'w')
    delay.write( str(writeDelay) )
    delay.flush()
    delay.close()



def write_error(file_name , write__):    # in the beginning it's '0'
    error__ = open(file_name , 'w')
    error__.write( str(write__) )
    error__.flush()
    error__.close()



def read_error(file_name):   
    error__ = open(file_name , 'r')
    return int(error__.read() )



def replace_line(file_name , line_num , text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = str(text[line_num]) + "\n"
    out = open(file_name, 'w')
    out.writelines(lines)
    out.flush()
    out.close()



def changeDelayOnceWrite(file_name , number): # in the beginning 'number' must be '1'... -> 'change_delay_once.txt'
    once = open(file_name , 'w')
    once.write( str(number) )
    once.flush()
    once.close()



def changeDelayOnceRead(file_name): 
    once = open(file_name , 'r')
    return int( once.read() )



def writeNumOfErrors(file_name , number):
    write_err = open(file_name , 'w')
    write_err.write( str(number) )
    write_err.flush()
    write_err.close()



def readNumOfErrors(file_name):
    read_err = open(file_name , 'r')
    return int( read_err.read() )



def writeBoolErrors(number): # in the beginning must be '0'
    write_err = open("error_in_the_beginning.txt" , 'w')
    write_err.write( str(number) )
    write_err.flush()
    write_err.close()



def readTotalUpdates():
    read_update = open("totalUpdates.txt" , 'r')
    return int( read_update.read() )



def email_sendToMixalis(SUBJECT , message):
    FROM = "FROM"
    TO = "TO-1"

    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    HTML_BODY = MIMEText(message, 'html')
    MESSAGE.attach(HTML_BODY)
    server = smtplib.SMTP("smtp.gmail.com:587")    
    password = "passcode"
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM , TO , MESSAGE.as_string() )
    server.quit()
    return TO


def email_sendToMe(SUBJECT , message):
    FROM = "FROM"
    TO = "TO-2"

    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    HTML_BODY = MIMEText(message, 'html')
    MESSAGE.attach(HTML_BODY)
    server = smtplib.SMTP("smtp.gmail.com:587")    
    password = "passcode"
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM , TO , MESSAGE.as_string() )
    server.quit()
    return TO



# Go to this link
# https://www.youtube.com/redirect?v=YPiHBtddefI&redir_token=QUFFLUhqa3phOTlrSjk3RWpRNThXSHJBUDNobzRpNXlFZ3xBQ3Jtc0ttbzhFSXhmai1Mb19ORG9NYzVGa2lwcVNyWG9TYnkxWDZPd1RiQ2JPX05LTlRPQVpTeVMwN0tQWFN6SlZwWThCZFBWcmhFQTZfSlkwVzZ5NXVYaWNVRjVzYTdpT015bXY5UnVqTWFXcmpvQURIVHRBNA%3D%3D&event=video_description&q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps%3Fpli%3D1
# to enable 'less secure apps' 



try:
    writeBoolErrors(0) # before join URLs

    link_site = "https://www.car.gr"    # link for car.gr 
    driver.get(link_site)        # open car.gr site
    time.sleep(1)

    cookies = driver.find_element_by_css_selector(".css-ofc9r3")      # accept cookies
    cookies.click()
    time.sleep(1)
    
    driver.get("https://www.car.gr/login/")
    
    username_input = driver.find_element_by_css_selector("#ui-id-2 > div:nth-child(2) > div:nth-child(2) > input:nth-child(1)").send_keys("username")    # give username
    password_input = driver.find_element_by_css_selector("#ui-id-2 > div:nth-child(3) > div:nth-child(2) > input:nth-child(1)").send_keys("password")     # give password
    time.sleep(1)

    log_in_button = driver.find_element_by_css_selector(".col-sm-offset-6 > button:nth-child(1)")   # press login button
    log_in_button.click()
    time.sleep(1)  


    with open("change_delay_once.txt" , 'r'):
        if( changeDelayOnceRead("change_delay_once.txt") == 1 ):
            write_delay("delay.txt" , computeDelay(23 , 55 , 0 , totalUpdateOfTheDay) )
            changeDelayOnceWrite("change_delay_once.txt" , 0) # now you can't change anything in file -> (delay.txt)

    writeBoolErrors(1) # after join URLs

    #======================================================================================================================================================================

    # a list for all URL's of machines. Total: 42
    Machines =     [
            "https://www.car.gr/xyma/view/26033392-epaggelmatiko-plyntirio-electrolux-w3400h-45-kg-electronord-gr" ,
            "https://www.car.gr/xyma/view/23254261-epaggelmatikos-kylindros-siderwmatos-airon-gmp-1400es-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/319444580-viomixaniko-stegnwtirio-imatismoy-passat-145-kg-zitiste-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/316373940-epaggelmatiko-stegnwtirio-electrolux-t-4250-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14783340-vrastiras-kafe-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/29972104-epaggelmatiko-plyntirio-electrolux-w-120-mp-16-kg-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14783918-psyktis-xymwn-usm-40-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/34778934-epaggelmatiko-plyntirio-electrolux-w-4180-h-21-kg-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14774559-kylindriko-siderwtirio-gmp-120-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/24188596-viomixanika-stegnwtiria-royxwn-passat-wwwelectronordgr" , 
            "https://www.car.gr/xyma/view/14783852-plato-ilektriko-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14772758-epaggelmatiko-plyntirio-electrolux-w-3130-h-18kg-wwwelectronordgr" ,
            "https://www.car.gr/xyma/view/14783805-frapiera-tvs-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/18465617-diplwtiki-mixani-jean-michel-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14773144-epaggelmatiko-stegnwtirio-podab-huebsch-17kg-wwwelectronordgr" ,
            "https://www.car.gr/xyma/view/29609265-epaggelmatiko-plyntirio-electrolux-w4130h-17kg-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/18465177-epaggelmatiko-stegnwtirio-electrolux-t-5250-wwwelectronordgr" ,
            "https://www.car.gr/xyma/view/14783647-tostiera-dipli-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14757302-epaggelmatiko-plyntirio-electrolux-w-365-h-95kg-wwwelectronordgr" ,
            "https://www.car.gr/xyma/view/14778226-pagomixani-c-250-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/319160527-epaggelmatiko-stegnwtirio-electrolux-t-4350-20-kg-electronord-gr" ,
            "https://www.car.gr/xyma/view/14783770-plato-gkazioy-1001-lm-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/18465809-diplwtiki-mixani-amko-zitiste-mas-prosfora-electronord-gr" ,
            "https://www.car.gr/xyma/view/14773137-epaggelmatiko-stegnwtirio-electrolux-t-4250-17kg-wwwelectronordgr" ,
            "https://www.car.gr/xyma/view/14772647-epaggelmatiko-plyntirio-electrolux-w-3105-h-14kg-wwwelectronordgr" ,
            "https://www.car.gr/xyma/view/14783410-soypiera-vrastiras-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/35748091-epaggelmatiko-stegnwtirio-electrolux-t-4250-17-kg-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14783936-dipli-estia-thermansews-gf-2-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14757176-epaggelmatiko-plyntirio-electrolux-fle-350-40-kg-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14774620-viomixaniko-kylindriko-siderwtirio-dreher-380-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14783835-gyros-gkazioy-4pg-t-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/319160971-epaggelmatiko-stegnwtirio-electrolux-t-4250-17-kg-electronord-gr" ,
            "https://www.car.gr/xyma/view/14748000-epaggelmatiko-plyntirio-electrolux-fle-120-fc-17kg-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14783678-vafliera-viron-2-dipli-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/26034156-diplwtiki-mixani-petsetwn-olma-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14757111-epaggelmatiko-plyntirio-electrolux-fle-403-mp-50-kg-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14783609-tostiera-ravdwti-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14773072-epaggelmatiko-stegnwtirio-electrolux-200-t-12kg-wwwelectronordgr" ,
            "https://www.car.gr/xyma/view/14783556-tostiera-dipli-ravdwti-zitiste-mas-prosfora-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14772787-viomixanika-plyntiria-electrolux-fle-810-90-kg-wwwelectronord-gr" ,
            "https://www.car.gr/xyma/view/14773094-epaggelmatiko-stegnwtirio-electrolux-tt-200-12kg-wwwelectronordgr" ,
            "https://www.car.gr/xyma/view/14783584-tostiera-epaggelmatiki-moni-zitiste-mas-prosfora-wwwelectronord-gr"
    ]



    with open("MachinesEachUpdate.txt") as fileEach:
        for i in range(0 , numOfMachines):
            machinesEachUpdate[i] = int(fileEach.readline())
            line = linecache.getline("MachinesEachUpdate.txt" , i+1)
    line = linecache.getline("MachinesEachUpdate.txt" , 0)
    with open("totalUpdates.txt") as fileTotal:
        totalUpdates = int(fileTotal.read())


    # main loop
    while(True):    # for ever
        current_time = datetime.datetime.now().time()   # get current time
        if(not current_time < on_time and not current_time >= off_time):
  
            if( readTotalUpdates() < 200 ):
                with open("updateNumber.txt") as file:
                    currentPosUpdate = int(file.read())  # read the number from file
                    machine = driver.get( Machines[currentPosUpdate] )  # go to machine's link
                
                updateMachine = driver.find_element_by_css_selector("div.list-group-item:nth-child(1)")     # find the update button
                updateMachine.click()       # press the "update" button


                machinesEachUpdate[currentPosUpdate] += 1
                with open("updateNumber.txt") as file:
                    replace_line("MachinesEachUpdate.txt" , int( file.read() ) , machinesEachUpdate)

                totalUpdates += 1
                fileTotal = open("totalUpdates.txt", "w")    # open the file
                fileTotal.write(str(totalUpdates))   # write the number in the file
                fileTotal.flush() 
                
                with open("totalUpdates.txt" , 'r') as fileTotal_R:
                    if( int(fileTotal_R.read()) == 1 ):
                        today = date.today()
                        str_date = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
                        email_sendToMixalis("Updates started" , "This email informs you that the updates for '" + str(str_date) + "' started at " + updatesStartedAt() )
                        email_sendToMe("Updates started" , "This email informs you that the updates for '" + str(str_date) + "' started at " + updatesStartedAt() )
                        print("Email sent... Done")
                        print("Running... >  " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
                    print("Total updates till now: " + open("totalUpdates.txt").read())
                currentPosUpdate += 1       # increase current position of machine update
                file = open("updateNumber.txt", "w")    # open the file
                file.write(str(currentPosUpdate))   # write the number in the file
                file.flush()    

            if(currentPosUpdate == numOfMachines):  # if update of all machines finished
                currentPosUpdate = 0                    # start again
                file = open("updateNumber.txt", "w")    # open the file
                file.write(str(currentPosUpdate))   # write the number in the file
                file.flush() 

            if( read_error("run_after_error.txt") == 1 ):
                email_sendToMixalis("Error solved in 'www.car.gr'" , "The error in 'www.car.gr' solved." + "&nbsp;" * 7 + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
                email_sendToMe("Error solved in 'www.car.gr'" , "The error in 'www.car.gr' solved." + "&nbsp;" * 7 + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
                write_error("run_after_error.txt" , 0)
                print("Running normally again, due to an error...  >  " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )

            time.sleep( read_delay("delay.txt") )              # wait for X minutes



        elif(current_time > off_time):
            if( int( open("change_delay_once.txt").read() == 0 ) ): # change_delay_once.txt is '0' , then it goes to '1'
                all_machines_updates_number = "&nbsp;" * 2 + "#" + "&nbsp;" * 3 + "Updates" + "&nbsp;" * 5 + "per" + "&nbsp;" * 5 + "&nbsp;" + "URL<br>"
                line = linecache.getline("MachinesEachUpdate.txt" , 0)
                k = 0
                with open("totalUpdates.txt") as fileTotal , open("MachinesEachUpdate.txt") as fileEach:
                    for line in fileEach.readlines():
                        if(k + 1 < 10):
                            all_machines_updates_number += "(" + str(k+1) + ")" + "&nbsp;" * 7 + str(line) + "&nbsp;" * 21 + Machines[k] + "<br>"  
                        else:
                            all_machines_updates_number += "(" + str(k+1) + ")" + "&nbsp;" * 5 + str(line) + "&nbsp;" * 21 + Machines[k] + "<br>" 
                        k += 1
                        line = linecache.getline("MachinesEachUpdate.txt" , k+1)
                    today = date.today()
                    str_date = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
                    email_sendToMixalis("'www.car.gr' Update ~ " + str_date , open("totalUpdates.txt").read() + " updates were performed successfully.<br>" + all_machines_updates_number)
                    email_sendToMe("'www.car.gr' Update ~ " + str_date , open("totalUpdates.txt").read() + " updates were performed successfully.<br>" + all_machines_updates_number)
                    print("Email just sent... Purpose: Success")
                
                # reset all files for the new day    
                
                if(os.path.exists("/home/nick/autoClicker/geckodriver.log")):
                    os.remove("/home/nick/autoClicker/geckodriver.log")
                file = open("updateNumber.txt", "w")    # open the file
                file.write(str(0))   # write the number in the file
                file.flush() 
                file.close()

                fileTotal = open("totalUpdates.txt", "w")    # open the file
                fileTotal.write(str(0))   # write the number in the file
                fileTotal.flush()
                fileTotal.close()

                fileEach = open("MachinesEachUpdate.txt" , "w")
                for i in range(0 , numOfMachines):
                    fileEach.write(str(0) + "\n")
                fileEach.close()

                # executes only once per day...
                time.sleep( (6*3600) + (45*60) )    # sleep for 6 hours & 55 minutes (23:55:00 - 06:50:00)

                changeDelayOnceWrite("change_delay_once.txt" , 1)
                writeNumOfErrors("let_5_errors_happen.txt" , 0)
                writeBoolErrors(0)
                write_delay("delay.txt" , 5)
                write_error("run_after_error.txt" , 0)

            

except: # if anything is wrong
        if( int( open("error_in_the_beginning.txt").read() ) == 0):
            if( readNumOfErrors("let_5_errors_happen.txt") <= 5):
                with open("error_in_the_beginning.txt") as fileError:
                    writeNumOfErrors("let_5_errors_happen.txt" , readNumOfErrors("let_5_errors_happen.txt") + 1)
                    changeDelayOnceWrite("change_delay_once.txt" , 1)
                    writeBoolErrors(0)
                    write_delay("delay.txt" , 5)
        else:
            print("AN ERROR OCCURED. Trying again. Loading...")
            with open("updateNumber.txt") as file:
                today = date.today()
                str_date = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
                email_sendToMixalis("ERROR OCCURED in 'www.car.gr'  " + str_date , "An error occured while the application was running.Trying to restart firefox...   Note: If this e-mail reappears, check the raspberry pi, otherwise the problem will have already been solved.")
                email_sendToMe("ERROR OCCURED in 'www.car.gr'  " + str_date , "An error occured while the application was running.Trying to restart firefox...   Note: If this e-mail reappears, check the raspberry pi, otherwise the problem will have already been solved.")

            print("Email just sent... Purpose: Error")
            write_error("run_after_error.txt" , 1)
        driver.quit()   # quit firefox
        os.execv(sys.executable, ["python3"] + sys.argv)    # run again from the top
