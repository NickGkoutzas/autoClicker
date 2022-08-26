# Nick Gkoutzas - Feb 2022 --------------
# --------------- Last update: Aug 26 2022
#----------------------------------------

from selenium import webdriver
from datetime import datetime , time , date
import time , datetime , os , sys , smtplib , linecache , socket , imaplib , email , traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.firefox.options import Options



# Fill the information !!!
#====================================
FROM_EMAIL = "Fill"                    
FROM_PWD = "Fill"   # app password           
ToMe = "Fill"
ToOther = "Fill"
site_username = "Fill"
site_password = "Fill"
PATH_NAME = "Fill"
#====================================

SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993





def read_NumberOfMachines(file_name):
    numOfMach = open(file_name , 'r')
    numberOfMachines__ = numOfMach.read()
    numOfMach.close()
    return int(numberOfMachines__)







def read_file_from_email(file_name):
    __file = open(file_name , 'r')
    link = __file.readline()
    __file.close()
    return str(link)






def write_EDIT__file_NumberOfMachines(file_name , number):     # File: NumberOfMachines.txt
    delay = open(file_name , 'w')
    delay.write( str(number) )
    delay.flush()
    delay.close()







def replace_line(file_name , line_num , text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = str(text[line_num]) + "\n"
    out = open(file_name, 'w')
    out.writelines(lines)
    out.flush()
    out.close()






def delete_line(file_name , line_num , text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = ""
    out = open(file_name, 'w')
    out.writelines(lines)
    out.flush()
    out.close()




def writeAppTerminated(file_name , number):
    appTerminated_ = open(file_name , 'w')
    appTerminated_.write( str(number) )
    appTerminated_.flush()
    appTerminated_.close()






def read_URL_machines_FILE(file__ , which_line):
    URL_machine = linecache.getline(file__ , which_line).strip("\n")
    return str(URL_machine)





def delete_from_URL_MACHINES_FILE(file__ , URL):
    for i in range( read_NumberOfMachines("NumberOfMachines.txt") ):
        URL_machine = linecache.getline(file__ , i+1).strip("\n")
        if(URL == URL_machine):
            delete_line("URL_machines.txt" , i , "")
            break




def changeDelayOnceWrite(file_name , number): # in the beginning 'number' must be '1'... -> 'change_delay_once.txt'
    once = open(file_name , 'w')
    once.write( str(number) )
    once.flush()
    once.close()



totalUpdateOfTheDay = 200
totalUpdates = int( open("totalUpdates.txt").read() )
numOfMachines = read_NumberOfMachines("NumberOfMachines.txt")      # number of machines
machinesEachUpdate = [int] * numOfMachines
currentPosUpdate = int( open("updateNumber.txt").read() )    # current position of update
bad_internet_connection = 0
finished_earlier = True





def send_email(SUBJECT , message , send_to):
    global FROM_EMAIL , FROM_PWD
    FROM = FROM_EMAIL
    TO = send_to

    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    HTML_BODY = MIMEText(message, 'html')
    MESSAGE.attach(HTML_BODY)
    server = smtplib.SMTP("smtp.gmail.com:587")    
    password = FROM_PWD
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM , TO , MESSAGE.as_string() )
    server.quit()
    return TO




send_email("'CarClicker app terminated' error corrected", "'CarClicker app terminated' error successfully corrected.<br>" , ToMe)

if( int( open("app_terminated.txt").read() ) == 1):
    print("All files reset...")
    send_email("'CarClicker app terminated' error corrected", "'CarClicker app terminated' error successfully corrected.<br>" , ToMe)
    send_email("'CarClicker app terminated' error corrected", "'CarClicker app terminated' error successfully corrected.<br>" , ToOther)
    writeAppTerminated("app_terminated.txt" , 0)
    os.system("python3 " + PATH_NAME + "/reset_all_files.py")
else:
    print("Computing time for updates...")
    changeDelayOnceWrite("change_delay_once.txt" , 1)





def read_TXT_FILE_from_gmail():
    global ToOther , ToMe

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL , FROM_PWD)
    mail.select('inbox')
    
    data = mail.search(None, 'ALL')
    mail_ids = data[1]
    id_list = mail_ids[0].split()   
    latest_email_id = int(id_list[-1])
    check_last_N_emails = 10+1
    msg=0
    for e in range(latest_email_id , latest_email_id - check_last_N_emails , -1):
        data = mail.fetch(str(e), '(RFC822)' )
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                try:
                    msg = email.message_from_string(str(arr[1] , 'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    
                except:
                    break

        for part in msg.walk():
            filename__ = part.get_filename()
            if filename__:
                open(PATH_NAME + str(filename__) , "wb").write(part.get_payload(decode=True))
               
        if( not "20 errors occured" in email_subject and (email_from == ToOther or email_from == ToMe) ):
            if(email_subject == "delete"):
                exists = 0
                
                for s in range(read_NumberOfMachines("NumberOfMachines.txt") ):
                    if( read_file_from_email(filename__) in open("URL_machines.txt").read() ):
                        delete_line("MachinesEachUpdate.txt" , s - 1, machinesEachUpdate)
                        delete_from_URL_MACHINES_FILE("URL_machines.txt" , read_file_from_email(filename__) )
                        exists = 1
                        break
                
                
                now = datetime.datetime.now()
                if(exists == 0 and read_file_from_email(filename__) in open("URL_machines.txt").read() ):    # the url that sent me ,does not exist in my list
                    send_email("Problem: Machine can not be deleted in 'www.car.gr'" , read_file_from_email(filename__) + " does not exist in the list .<br>Time: " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                    send_email("Problem: Machine can not be deleted in 'www.car.gr'" , read_file_from_email(filename__) + " does not exist in the list .<br>Time: " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
                    pass

                elif(exists == 1):
                    send_email("List updated in 'www.car.gr': A machine deleted " , read_file_from_email(filename__) + " deleted successfully.<br>List of all machines updated at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)  + "<br>You may not be able to see the machine on the site, because the administrator has removed it." + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                    send_email("List updated in 'www.car.gr': A machine deleted " , read_file_from_email(filename__) + " deleted successfully.<br>List of all machines updated at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "<br>You may not be able to see the machine on the site, because the administrator has removed it." + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
                        
                    write_EDIT__file_NumberOfMachines("NumberOfMachines.txt" , read_NumberOfMachines("NumberOfMachines.txt") - 1 )
                return


            elif(email_subject == "insert"):
                now = datetime.datetime.now()
                if(not read_file_from_email(filename__) in open("URL_machines.txt").read() ):
                    write_EDIT__file_NumberOfMachines("NumberOfMachines.txt" , read_NumberOfMachines("NumberOfMachines.txt") + 1 )
                    with open("URL_machines.txt", "a") as __file__:
                        __file__.write(read_file_from_email(filename__) + "\n")

                    with open("MachinesEachUpdate.txt", "a") as __file:
                        __file.write(str(0) + "\n")

                    send_email("List updated in 'www.car.gr': A machine inserted " , read_file_from_email(filename__) + " inserted successfully.<br>List of all machines updated at " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)+ "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                    send_email("List updated in 'www.car.gr': A machine inserted " , read_file_from_email(filename__) + " inserted successfully.<br>List of all machines updated at " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)+ "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
                    return

        else:
            continue





on_time = datetime.datetime.strptime('07:00:00' , '%H:%M:%S').time()    # start updates at this time
off_time = datetime.datetime.strptime('23:55:00' , '%H:%M:%S').time()   # stop updates at this time
now = datetime.datetime.now()




if( int( open("change_delay_once.txt").read() == 1 ) ):
    if(os.path.exists(PATH_NAME + "geckodriver.log")):   # file path may not be the same
        os.remove(PATH_NAME + "geckodriver.log")





def __internetStatusError__Read(file_name): # '0' at start   , '1' if internet connection error 
    status = open(file_name , 'r')
    fileStat = status.read()
    status.close()
    return int(fileStat)



def __internetStatusError__Write(file_name , status): # '1' if an error occured , else '0' -> normal
    delay = open(file_name , 'w')
    delay.write( str(status) )
    delay.flush()
    delay.close()




def check_internet_connection():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False



def __totalErrorsOfDay__R(file_name):
    errors__ = open(file_name , 'r')
    numOfErrors = errors__.read()
    errors__.close()
    return int(numOfErrors)



def __totalErrorsOfDay__W(file_name):
    numOfErrors = int( __totalErrorsOfDay__R(file_name) )
    numOfErrors += 1
    errors__ = open(file_name , 'w')
    errors__.write( str(numOfErrors) )
    errors__.flush()
    errors__.close()



def updatesStartedAt():
    now = datetime.datetime.now()
    return ( str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))



def computeDelay(endTimeHours , endTimeMinutes , endTimeSeconds):
    global totalUpdateOfTheDay
    now = datetime.datetime.now()
    currentTime = datetime.datetime(now.year, now.month , now.day , now.hour , now.minute , now.second)
    finalTime = datetime.datetime(now.year, now.month , now.day , endTimeHours , endTimeMinutes , endTimeSeconds)
    difference = abs(finalTime - currentTime)
    return int ( ( ( ( int(difference.total_seconds() ) / 60 ) / (totalUpdateOfTheDay - int( open("totalUpdates.txt").read() ) ) ) * 60 ) - 10 )  # in seconds




def computeTimeSleep(hour__ , minute__ , second__):
    now = datetime.datetime.now()
    currentTime = datetime.datetime(now.year, now.month , now.day , now.hour , now.minute , now.second)
    startTime = datetime.datetime(now.year, now.month , now.day , hour__ , minute__ , second__)
    difference = abs(currentTime - startTime)
    return int(difference.total_seconds() )



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




def readTotalUpdates():
    read_update = open("totalUpdates.txt" , 'r')
    return int( read_update.read() )




def error_and_back_to_internet():
    if( not check_internet_connection() ):
        print("Disconnected from the network ... Please wait")
        __totalErrorsOfDay__W("totalErrors.txt")
        
        __internetStatusError__Write("internet_statusError.txt" , 1)
        fileInternetError = open("internet_error_DATE.txt", "w")    # open the file
        now = datetime.datetime.now()
        fileInternetError.write( str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )   # write the number in the file
        fileInternetError.flush()
        fileInternetError.close()

        while( not check_internet_connection() or __internetStatusError__Read("internet_statusError.txt") ):
            time.sleep(1)
            if( check_internet_connection() ):
                print("Connection restored. Connected... Done")
                write_delay("delay.txt" , computeDelay(23 , 55 , 0) )
                __internetStatusError__Write("internet_statusError.txt" , 0)
                now = datetime.datetime.now()
                send_email("[SOLVED] Internet connection error" , "There was a problem connecting<br>to the network at " + str( open("internet_error_DATE.txt").read() ) + "<br><br>Possible problems:<br>1) Ethernet cable disconnected<br>2) Bad Wi-Fi connection<br>3) Power outage<br>" + "<br>Connection restored at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                send_email("[SOLVED] Internet connection error" , "There was a problem connecting<br>to the network at " + str( open("internet_error_DATE.txt").read() ) + "<br><br>Possible problems:<br>1) Ethernet cable disconnected<br>2) Bad Wi-Fi connection<br>3) Power outage<br>" + "<br>Connection restored at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
                print("Sent email due to network disconnection... > " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))






options = Options()
options.add_argument('--headless')
error_and_back_to_internet()
driver = webdriver.Firefox(options=options)     # call Firefox 
error_and_back_to_internet()


try:
    error_and_back_to_internet()
    
    link_site = "https://www.car.gr"    # link for car.gr 
    driver.get(link_site)        # open car.gr site
    time.sleep(1)
    error_and_back_to_internet()
    #cookies = driver.find_element_by_css_selector(".css-ofc9r3")      # accept cookies
    cookies = driver.find_element_by_css_selector("button.css-1jlb8eq:nth-child(3)")      # accept cookies

    cookies.click()
    time.sleep(1)
    error_and_back_to_internet()

    driver.get("https://www.car.gr/login/")
    error_and_back_to_internet()

    username_input = driver.find_element_by_css_selector("#ui-id-2 > div:nth-child(2) > div:nth-child(2) > input:nth-child(1)").send_keys(site_username)    # give username
    error_and_back_to_internet()

    password_input = driver.find_element_by_css_selector("#ui-id-2 > div:nth-child(3) > div:nth-child(2) > input:nth-child(1)").send_keys(site_password)     # give password
    time.sleep(1)
    error_and_back_to_internet()
    
    log_in_button = driver.find_element_by_css_selector(".col-sm-offset-6 > button:nth-child(1)")   # press login button
    error_and_back_to_internet()
    
    log_in_button.click()
    time.sleep(1)  
    error_and_back_to_internet()

    with open("change_delay_once.txt" , 'r'):
        if( changeDelayOnceRead("change_delay_once.txt") == 1 ):
            write_delay("delay.txt" , computeDelay(23 , 55 , 0) )
            changeDelayOnceWrite("change_delay_once.txt" , 0) # now you can't change anything in file -> (delay.txt)


    #======================================================================================================================================================================

    


    with open("MachinesEachUpdate.txt") as fileEach:
        for i in range(0 , read_NumberOfMachines("NumberOfMachines.txt") ):
            machinesEachUpdate[i] = int(fileEach.readline())
            line = linecache.getline("MachinesEachUpdate.txt" , i+1)
    line = linecache.getline("MachinesEachUpdate.txt" , 0)
    with open("totalUpdates.txt") as fileTotal:
        totalUpdates = int(fileTotal.read())


    # main loop
    while(True):    
        current_time = datetime.datetime.now().time()   # get current time

        if(not current_time < on_time and not current_time >= off_time):

            if( readTotalUpdates() < totalUpdateOfTheDay ):

                read_TXT_FILE_from_gmail() # check if the admin of the site sent an email...

                with open("updateNumber.txt") as file:
                    currentPosUpdate = int(file.read())  # read the number from file
                    machine = driver.get( read_URL_machines_FILE("URL_machines.txt" , currentPosUpdate + 1) )

                
                error_and_back_to_internet()
                updateMachine = driver.find_element_by_css_selector("div.list-group-item:nth-child(1)")     # find the update button
                error_and_back_to_internet()
                #updateMachine.click()       # press the "update" button


                machinesEachUpdate[currentPosUpdate] += 1
                with open("updateNumber.txt" , 'r') as file:
                    replace_line("MachinesEachUpdate.txt" , int( file.read() ) , machinesEachUpdate)
                
                totalUpdates += 1
                with open("totalUpdates.txt" , 'w') as fileTotal:
                    fileTotal.write(str(totalUpdates))   # write the number in the file
                    fileTotal.flush() 
                
                with open("totalUpdates.txt" , 'r') as fileTotal_R:
                    if( int(fileTotal_R.read()) == 1 ):
                        today = date.today()
                        str_date = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
                        send_email("Updates started" , "This email informs you that the updates for '" + str(str_date) + "' started at " + updatesStartedAt() + \
                                         "<br><br><br>Note:<br>If you want to insert or delete a machine<br>(URL-LINK), follow the steps below:<br><br><br> \
                                         * Insert a new machine in the list?<br>" + "&nbsp;" * 5 +  \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                     "     with subject: 'insert'" + "<br>" + "&nbsp;" * 5 + \
                                                     "     and message: attach a txt file (e.g: a.txt) that <br>" + "&nbsp;" * 5 +" contains the link-machine you want to add.<br><br> \
                                        * Delete an existing machine from the list?<br>" + "&nbsp;" * 5 + \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                     "     with subject: 'delete'" + "<br>" + "&nbsp;" * 5 + \
                                                     "     and message: attach a txt file (e.g: a.txt) that <br>" + "&nbsp;" * 5 +" contains the link-machine you want to delete.<br><br>" \
                                        "Remember to add" + "&nbsp;" * 5 + "'.txt'" +"&nbsp;" * 5 + "at the end of file.<br>You'll receive a notification of your action.<br><br>" + "&nbsp;" * 60\
                                         + "Written in Python" , ToMe)
                        send_email("Updates started" , "This email informs you that the updates for '" + str(str_date) + "' started at " + updatesStartedAt() + \
                                         "<br><br><br>Note:<br>If you want to insert or delete a new machine<br>(URL-LINK), follow the steps below:<br><br><br> \
                                         * Insert a new machine in the list?<br>" + "&nbsp;" * 5 +  \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                     "     with subject: 'insert'" + "<br>" + "&nbsp;" * 5 + \
                                                     "     and message: attach a txt file (e.g: a.txt) that <br>" + "&nbsp;" * 5 +" contains the link-machine you want to add.<br><br> \
                                        * Delete an existing machine from the list?<br>" + "&nbsp;" * 5 + \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                     "     with subject: 'delete'" + "<br>" + "&nbsp;" * 5 + \
                                                     "     and message: attach a txt file (e.g: a.txt) that <br>" + "&nbsp;" * 5 +" contains the link-machine you want to delete.<br><br>" \
                                        "Remember to add" + "&nbsp;" * 5 + "'.txt'" +"&nbsp;" * 5 + "at the end of file.<br>You'll receive a notification of your action.<br><br>" + "&nbsp;" * 60\
                                         + "Written in Python" , ToOther)
                        print("Emails sent... Purpose: New day, new updates.")
                        now = datetime.datetime.now()
                        print("Running... >  " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
                    now = datetime.datetime.now()
                    print("Total updates till now, (" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "): " + open("totalUpdates.txt").read())
                 
                currentPosUpdate += 1       # increase current position of machine update
                with open("updateNumber.txt" , 'w') as file:
                    file.write(str(currentPosUpdate))   # write the number in the file
                    file.flush()    
                

            if(currentPosUpdate == read_NumberOfMachines("NumberOfMachines.txt")):  # if update of all machines finished
                currentPosUpdate = 0                    # start again
                file = open("updateNumber.txt", "w")    # open the file
                file.write(str(currentPosUpdate))   # write the number in the file
                file.flush() 

            if( read_error("run_after_error.txt") == 1 ):
                now = datetime.datetime.now()
                send_email("The errors just solved in 'www.car.gr'" , "The errors in 'www.car.gr' solved." + "&nbsp;" * 7 + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                send_email("The errors just solved in 'www.car.gr'" , "The errors in 'www.car.gr' solved." + "&nbsp;" * 7 + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
                write_error("run_after_error.txt" , 0)
                print("Emails sent... Purpose: Unrecognized errors solved.")
                print("Running normally again, due to 20 errors...  >  " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
            
            
            if(finished_earlier and readTotalUpdates() == totalUpdateOfTheDay ):
                finished_earlier = False
                print( str(totalUpdateOfTheDay) + " updates have been performed before 23:55:00 .Sleeping till 23:55:00 ...")
                sleep__ = computeTimeSleep(23 , 55 , 0)
                time.sleep(sleep__)
            

            elif (readTotalUpdates() < totalUpdateOfTheDay ):
                for i in range( 1 , int( open("delay.txt").read() ) ):   # sleeping... & checking for network disconnection
                    time.sleep(1)
                    error_and_back_to_internet()
                

            

        elif(current_time > off_time):

                all_machines_updates_number = "&nbsp;" * 2 + "#" + "&nbsp;" * 3 + "Updates" + "&nbsp;" * 5 + "per" + "&nbsp;" * 5 + "&nbsp;" + "URL<br>"
                line = linecache.getline("MachinesEachUpdate.txt" , 0)
                k = 0
                with open("totalUpdates.txt") as fileTotal , open("MachinesEachUpdate.txt") as fileEach:
                    for line in fileEach.readlines():
                        if(k + 1 < 10):
                            all_machines_updates_number += "(" + str(k+1) + ")" + "&nbsp;" * 7 + str(line) + "&nbsp;" * 21 + read_URL_machines_FILE("URL_machines.txt" , k+1) + "<br>"  
                        else:
                            all_machines_updates_number += "(" + str(k+1) + ")" + "&nbsp;" * 5 + str(line) + "&nbsp;" * 21 + read_URL_machines_FILE("URL_machines.txt" , k+1) + "<br>" 
                        k += 1
                        line = linecache.getline("MachinesEachUpdate.txt" , k+1)
                    today = date.today()
                    str_date = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
                    send_email("'www.car.gr' Update ~ " + str_date , open("totalUpdates.txt").read() + " updates were performed successfully.<br>Total errors during the day: " + str(__totalErrorsOfDay__R("totalErrors.txt")) + "<br>" + all_machines_updates_number + "<br><br>" + "&nbsp;" * 60\
                                         + "Written in Python" , ToMe)
                    send_email("'www.car.gr' Update ~ " + str_date , open("totalUpdates.txt").read() + " updates were performed successfully.<br>Total errors during the day: " + str(__totalErrorsOfDay__R("totalErrors.txt")) + "<br>" + all_machines_updates_number + "<br><br>" + "&nbsp;" * 60\
                                         + "Written in Python" , ToOther)
                    print("Emails just sent... Purpose: " + str(open("totalUpdates.txt").read()) + " updates were performed successfully.")
                
                # reset all files for the new day    
                os.system("python3 " + PATH_NAME + "/reset_all_files.py")
                
                if(os.path.exists(PATH_NAME + "geckodriver.log")):   # file path may not be the same
                    os.remove(PATH_NAME + "geckodriver.log")

                # executes only once per day...
                print("Sleeping till next day...")
                time.sleep(10*60)
                print("Waiting till 06:59:50 pm ...")
                time.sleep( computeTimeSleep(6 , 59 , 50) )  # sleep till tomorrow morning at 7pm                
                
                driver.quit()   # quit firefox
                try:
                    os.system("python3 " + PATH_NAME + "/carClicker.py") # run again from the top
                except:
                    send_email("SOS. CarClicker app terminated unexpectedly", "CarClicker app terminated unexpectedly.<br>" + "The system tried to re-run the app with no success.<br>" + "This email sent in order to tell you to manually start the app again." , ToMe)
                    send_email("SOS. CarClicker app terminated unexpectedly", "CarClicker app terminated unexpectedly.<br>" + "The system tried to re-run the app with no success.<br>" + "This email sent in order to tell you to manually start the app again." , ToOther)




except: # if anything is wrong
    print("AN ERROR OCCURED. Trying again. Loading...")
    read_TXT_FILE_from_gmail() # check if the admin of the site sent an email...
                
    __totalErrorsOfDay__W("totalErrors.txt")
    writeNumOfErrors("let_20_errors_happen.txt" , readNumOfErrors("let_20_errors_happen.txt") + 1)


    if( readNumOfErrors("let_20_errors_happen.txt") == 20):
        with open("updateNumber.txt") as file:
            today = date.today()
            str_date = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
            send_email("20 errors occured in 'www.car.gr'  " + str_date , "20 errors occured while the application was running.Trying to restart application...<br>" + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
            send_email("20 errors occured in 'www.car.gr'  " + str_date , "20 errors occured while the application was running.Trying to restart application...<br>" + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
            print("Emails just sent... Purpose: Unrecognized error")
            write_error("run_after_error.txt" , 1)
            writeNumOfErrors("let_20_errors_happen.txt" , 0)
    driver.quit()   # quit firefox
    try:
        os.system("python3 " + PATH_NAME + "/carClicker.py") # run again from the top
    except:
        writeAppTerminated("app_terminated.txt" , 1)
        print("CarClicker app terminated unexpectedly")
        send_email("SOS. CarClicker app terminated unexpectedly", "CarClicker app terminated unexpectedly.<br>" + "The system tried to re-run the app with no success.<br>" + "This email sent in order to tell you to manually start the app again." , ToMe)
        send_email("SOS. CarClicker app terminated unexpectedly", "CarClicker app terminated unexpectedly.<br>" + "The system tried to re-run the app with no success.<br>" + "This email sent in order to tell you to manually start the app again." , ToOther)



