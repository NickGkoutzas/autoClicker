# Nick Gkoutzas - Feb 2022 ---------------
# --------------- Last update: Oct 28 2022
# ----------------------------------------

from selenium import webdriver
from datetime import datetime , time , date
import time , datetime , os , sys , smtplib , linecache , socket , imaplib , email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By



#=====================================================================================
lines = tuple(open("passwords.txt" , 'r'))
FROM_EMAIL = lines[0] 
FROM_PWD = lines[1]            
ToMe = lines[2]
ToOther = lines[3]     
site_username = lines[4]   
site_password = lines[5]    
PATH_NAME = lines[6]  
#=====================================================================================

SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993





def read_NumberOfMachines(file_name):
    numOfMach = open(file_name , 'r')
    numberOfMachines__ = numOfMach.read()
    numOfMach.close()
    return int(numberOfMachines__)







def read_file_from_email(file_name):
    __file = open(file_name , 'r')
    link = __file.readline()#.strip("\n")
    __file.close()
    return str(link)




def read_file_from_email_GitHub(file_name):
    __file = open(file_name , 'r')
    number = __file.readline()#.strip("\n")
    __file.close()
    return int(number)




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






def delete_line(file_name , line_num):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = ""
    out = open(file_name, 'w')
    out.writelines(lines)
    out.flush()
    out.close()






def read_URL_machines_FILE(file__ , which_line):
    URL_machine = linecache.getline(file__ , which_line).strip("\n")
    return str(URL_machine)





def delete_from_URL_MACHINES_FILE(file__ , URL):
    for i in range( read_NumberOfMachines("URL_machines.txt") ):
        URL_machine = linecache.getline(file__ , i+1).strip("\n")
        if(URL == URL_machine):
            delete_line("URL_machines.txt" , i , "")
            break







totalUpdateOfTheDay = 200
totalUpdates = int( open("totalUpdates.txt").read() )
numOfMachines = read_NumberOfMachines("NumberOfMachines.txt")      # number of machines
machinesEachUpdate = [int] * numOfMachines
currentPosUpdate = int( open("updateNumber.txt").read() )    # current position of update
bad_internet_connection = 0
sec__ = 0
min__ = 0
hour__ = 0






def time_correction():
    global  hour__ , min__ , sec__
    if(now.second < 10):
        sec__ = str(0) + str(now.second)
    else:
        sec__ = str(now.second)
    if(now.minute < 10):
        min__ = str(0) + str(now.minute)
    else:
        min__ = str(now.minute)
    if(now.hour < 10):
        hour__ = str(0) + str(now.hour)
    else:
        hour__ = str(now.hour)
    return sec__ , min__ , hour__





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






def changeDelayOnceWrite(file_name , number): # in the beginning 'number' must be '1'... -> 'change_delay_once.txt'
    once = open(file_name , 'w')
    once.write( str(number) )
    once.flush()
    once.close()




def read_GitHubUpdatesNumber(file_name):
    file_ = open(file_name , 'r')
    number = file_.read()
    file_.close()
    return int(number)





def write_GitHubUpdatesNumber(file_name , number):
    file_w = open(file_name , 'w')
    file_w.write(str(number))
    file_w.flush()
    file_w.close()





def read_TXT_FILE_from_gmail():
    global FROM_EMAIL , FROM_PWD
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL , FROM_PWD)
    mail.select('inbox')
    
    data = mail.search(None, 'ALL')
    mail_ids = data[1]
    id_list = mail_ids[0].split()   
    latest_email_id = int(id_list[-1])
    check_last_N_emails = 11
    for e in range(latest_email_id , latest_email_id - check_last_N_emails , -1):
        data = mail.fetch(str(e), '(RFC822)' )
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1],'utf-8'))
                email_subject = msg['subject']
                email_date = msg['Date']

        for part in msg.walk():
            filename__ = part.get_filename()
            if filename__:
                open(PATH_NAME + str(filename__) , "wb").write(part.get_payload(decode=True))
               
        if(not "20 errors occured" in email_subject):

            if(email_subject == "delete" or email_subject == "Delete"):
                exists = 0
                for s in range(read_NumberOfMachines("NumberOfMachines.txt") ):
                    if( read_file_from_email("\n" + filename__) in open("URL_machines.txt").read() ):
                        delete_line("MachinesEachUpdate.txt" , s+1)
                        delete_line("URL_machines.txt" , s+1)
                        exists = 1
                        break

                now = datetime.datetime.now()
                time_correction()
                if(exists == 0 and read_file_from_email("\n" + filename__) in open("URL_machines.txt").read() and filename__ == "delete.txt"):    # the url that sent me ,does not exist in my list
                    send_email("Problem: Machine can not be deleted in 'www.car.gr'" , read_file_from_email("\n" + filename__) + " does not exist in the list .<br>Time: " +  hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                    send_email("Problem: Machine can not be deleted in 'www.car.gr'" , read_file_from_email("\n" + filename__) + " does not exist in the list .<br>Time: " +  hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
                    pass

                elif(exists == 1 and filename__ == "delete.txt"):
                    send_email("List updated in 'www.car.gr': A machine deleted " , read_file_from_email("\n" + filename__) + " deleted successfully.<br>List of all machines updated at " +  hour__ + ":" + min__ + ":" + sec__  + "<br>You may not be able to see the machine on the site, because the administrator has removed it." + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                    send_email("List updated in 'www.car.gr': A machine deleted " , read_file_from_email("\n" + filename__) + " deleted successfully.<br>List of all machines updated at " +  hour__ + ":" + min__ + ":" + sec__ + "<br>You may not be able to see the machine on the site, because the administrator has removed it." + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
                    write_EDIT__file_NumberOfMachines("NumberOfMachines.txt" , read_NumberOfMachines("NumberOfMachines.txt") - 1 )



            if(email_subject == "insert" or email_subject == "Insert"):

                now = datetime.datetime.now()
                time_correction()
                if(not read_file_from_email("\n" + filename__) in open("URL_machines.txt").read() and filename__ == "insert.txt"):
                    write_EDIT__file_NumberOfMachines("NumberOfMachines.txt" , read_NumberOfMachines("NumberOfMachines.txt") + 1 )
                    with open("URL_machines.txt", "a") as __file__:
                        __file__.write(read_file_from_email("\n" + filename__) + "\n")

                    with open("MachinesEachUpdate.txt", "a") as __file:
                        __file.write(str(0) + "\n")

                    send_email("List updated in 'www.car.gr': A machine inserted " , read_file_from_email("\n" + filename__) + " inserted successfully.<br>List of all machines updated at " + hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                    send_email("List updated in 'www.car.gr': A machine inserted " , read_file_from_email("\n" + filename__) + " inserted successfully.<br>List of all machines updated at " + hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)



            if(email_subject == "update" or email_subject == "Update"):
                now = datetime.datetime.now()
                listOfMonths = ["Jan" , "Feb" , "Mar" , "Apr" , "May" , "Jun" , "Jul" , "Aug" , "Sep" , "Oct" , "Nov" , "Dec"]
                dateOfToday = str(now.day) + " " + listOfMonths[int(now.month) - 1] + " " + str(now.year)
                date_of_email_update = ''

                for _string_ in range(5 , 16):
                    date_of_email_update += str(email_date[_string_])

                if(date_of_email_update == dateOfToday and not read_file_from_email_GitHub("\n" + filename__) == read_GitHubUpdatesNumber("GitHubUpdatesNumber.txt") and filename__ == "update.txt"):
                    time_correction()
                    write_GitHubUpdatesNumber("GitHubUpdatesNumber.txt" , read_GitHubUpdatesNumber("GitHubUpdatesNumber.txt") + 1 ) # increase update number (GitHub upates) by 1
                    print("===============================================")
                    print("Program stopped running, because an update version will be downloaded from GitHub.\nThe update program will start in 7 minutes.\nDO NOT terminate the program !!!\nTime: " + hour__ + ":" + min__ + ":" + sec__ )
                    send_email("Update new version from GitHub" , "Program stopped running, because an update version will be downloaded from GitHub.\nThe update program will start in 7 minutes.<br>DO NOT terminate the program !!!<br>Time: " + hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python", ToMe)
                    send_email("Update new version from GitHub" , "Program stopped running, because an update version will be downloaded from GitHub.\nThe update program will start in 7 minutes.<br>DO NOT terminate the program !!!<br>Time: " + hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python", ToOther)

                    print("===============================================")
                    time.sleep(7 * 60)  # sleep for 7 minutes
                    print("The new version is currently being downloaded and will be run at a moment...")
                    os.system("wget 'https://github.com/NickGkoutzas/autoClicker/raw/main/carClicker.py' && mv carClicker.py.1 carClicker.py")
                    driver.quit()   # quit firefox
                    time.sleep(5)
                    changeDelayOnceWrite("change_delay_once.txt" , 1)
                    os.system("python3 carClicker.py")







on_time = datetime.datetime.strptime('02:00:00' , '%H:%M:%S').time()    # start updates at this time
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
    if(now.second < 10):
        sec__ = str(0) + str(now.second)
    else:
        sec__ = str(now.second)
    return ( str(hour__) + ":" + str(min__) + ":" + str(sec__))



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




def write_error(file_name , write__):    # in the beginning it's '0'
    error__ = open(file_name , 'w')
    error__.write( str(write__) )
    error__.flush()
    error__.close()



def read_error(file_name):   
    error__ = open(file_name , 'r')
    return int(error__.read() )




def write_delay(file_name , writeDelay):    # in the beginning 'writeDelay' must be '5'... -. 'delay.txt'
    delay = open(file_name , 'w')
    delay.write( str(writeDelay) )
    delay.flush()
    delay.close()




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
        time_correction()
        fileInternetError.write( hour__ + ":" + min__ + ":" + sec__ )   # write the number in the file
        fileInternetError.flush()
        fileInternetError.close()

        while( not check_internet_connection() or __internetStatusError__Read("internet_statusError.txt") ):
            time.sleep(1)
            if( check_internet_connection() ):
                print("Connection restored. Connected... Done")
                write_delay("delay.txt" , computeDelay(23 , 55 , 0) )
                __internetStatusError__Write("internet_statusError.txt" , 0)
                now = datetime.datetime.now()
                time_correction()
                send_email("[SOLVED] Internet connection error" , "There was a problem connecting<br>to the network at " + str( open("internet_error_DATE.txt").read() ) + "<br><br>Possible problems:<br>1) Ethernet cable disconnected<br>2) Bad Wi-Fi connection<br>3) Power outage<br>" + "<br>Connection restored at " +  hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                send_email("[SOLVED] Internet connection error" , "There was a problem connecting<br>to the network at " + str( open("internet_error_DATE.txt").read() ) + "<br><br>Possible problems:<br>1) Ethernet cable disconnected<br>2) Bad Wi-Fi connection<br>3) Power outage<br>" + "<br>Connection restored at " +  hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
                print("Sent email due to network disconnection... > " + hour__ + ":" + min__ + ":" + sec__)
                break






options = Options()
options.add_argument('--headless')
error_and_back_to_internet()
driver = webdriver.Firefox(options=options)            # call Firefox ( ** hide window **)


try:
    error_and_back_to_internet()
    print("          -> APPLICATION STARTED <-\n===============================================")
    print("Opening 'www.car.gr' page...") 
    link_site = "https://www.car.gr"    # link for car.gr
    driver.get(link_site)               # open car.gr site
    time.sleep(1)
    error_and_back_to_internet()
    global cookies

    try:
        cookies = driver.find_element(By.CSS_SELECTOR , ".css-ofc9r3")                              # accept cookies
    except:
        try:
            cookies = driver.find_element(By.CSS_SELECTOR , "button.css-1jlb8eq:nth-child(3)")      # accept cookies
        except:
            cookies = driver.find_element(By.CSS_SELECTOR , ".css-ofc9r3 > span:nth-child(1)")      # accept cookies
    print("Accepting cookies...")
    cookies.click()
    time.sleep(1)
    error_and_back_to_internet()
    print("Going to login page...")
    driver.get("https://www.car.gr/login/")
    error_and_back_to_internet()
    print("Entering username and password in login page...")
    username_input = driver.find_element(By.CSS_SELECTOR , "#ui-id-2 > div:nth-child(2) > div:nth-child(2) > input:nth-child(1)").send_keys(site_username)     # give username
    error_and_back_to_internet()

    password_input = driver.find_element(By.CSS_SELECTOR , "#ui-id-2 > div:nth-child(3) > div:nth-child(2) > input:nth-child(1)").send_keys(site_password)     # give password
    time.sleep(1)
    error_and_back_to_internet()
    
    log_in_button = driver.find_element(By.CSS_SELECTOR , ".col-sm-offset-6 > button:nth-child(1)")   # press login button
    error_and_back_to_internet()
    
    log_in_button.click()
    
    current_time = datetime.datetime.now().time()   # get current time
    if(not current_time < on_time and not current_time >= off_time):
        print("Username and password acceptance...\nUpdates will start soon...\n===============================================\n") 
    else:
        print("Username and password acceptance...\nUpdates will start at 07:00:00 in the morning.\n===============================================\n") 
    time.sleep(1)  
    error_and_back_to_internet()

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
                read_TXT_FILE_from_gmail() # check if the user of the site sent an email...
                write_delay("delay.txt" , computeDelay(23 , 55 , 0) )

                with open("updateNumber.txt") as file:
                    currentPosUpdate = int(file.read())  # read the number from file
                    driver.get( read_URL_machines_FILE("URL_machines.txt" , currentPosUpdate + 1) )

                error_and_back_to_internet()
                global updateMachine
                try:
                    updateMachine = driver.find_element(By.CSS_SELECTOR , "div.list-group-item:nth-child(1)")     # find the update button
                except:
                    updateMachine = driver.find_element(By.CSS_SELECTOR , "div.c-list-group-item:nth-child(1) > div:nth-child(1)")     # find the update button
                error_and_back_to_internet()
                updateMachine.click()       # press the "update" button
                
                
                machinesEachUpdate[currentPosUpdate] += 1
                with open("updateNumber.txt" , 'r') as file:
                    replace_line("MachinesEachUpdate.txt" , int( file.read() ) , machinesEachUpdate)
                
                totalUpdates += 1
                with open("totalUpdates.txt" , 'w') as fileTotal:
                    fileTotal.write(str(totalUpdates))   # write the number in the file
                    fileTotal.flush() 
                
                
                with open("totalUpdates.txt" , 'r') as fileTotal_R:
                    time_correction()
                    if( int(fileTotal_R.read()) == 1):
                        today = date.today()
                        str_date = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
                        send_email("Updates started" , "This email informs you that the updates for '" + str(str_date) + "' started at " + updatesStartedAt() + \
                                            "<br>Note:<br>If you want to insert or delete a machine<br>(URL-LINK) or update the current version of application from GitHub,<br>follow the steps below:<br><br> \
                                            * Insert a new machine in the list?<br>" + "&nbsp;" * 5 +  \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                        "     with subject: 'insert' or 'Insert'" + "<br>" + "&nbsp;" * 5 + \
                                                        "     and message: attach a txt file (insert.txt) that <br>" + "&nbsp;" * 5 +" contains the link-machine you want to add.<br><br> \
                                        * Delete an existing machine from the list?<br>" + "&nbsp;" * 5 + \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                        "     with subject: 'delete' or 'Delete'" + "<br>" + "&nbsp;" * 5 + \
                                                        "     and message: attach a txt file (delete.txt) that <br>" + "&nbsp;" * 5 +" contains the link-machine you want to delete.<br><br>" \
                                        "* Update the current version of program from<br>" + "&nbsp;" * 5 + "GitHub?<br>" + "&nbsp;" * 5 + \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                "     with subject: 'update' or 'Update'" + "<br>" + "&nbsp;" * 6 + \
                                                "     and message: attach a txt file (update.txt) that <br>" + "&nbsp;" * 5 +" contains the number of changes made in the<br>" + "&nbsp;" * 5 + "GitHub today.<br><br>" \
                                        "Remember to add the extension" + "&nbsp;" * 5 + "'.txt'" +"&nbsp;" * 5 + "at the end of file.<br>" \
                                        "Pay attention to the name of the file<br>(insert.txt / delete.txt / update.txt).<br>You'll receive a notification of your action, if everything goes well.<br><br>" + "&nbsp;" * 60\
                                            + "Written in Python" , ToMe)
                        send_email("Updates started" , "This email informs you that the updates for '" + str(str_date) + "' started at " + updatesStartedAt() + \
                                            "<br>Note:<br>If you want to insert or delete a machine<br>(URL-LINK) or update the current version of application from GitHub,<br>follow the steps below:<br><br> \
                                            * Insert a new machine in the list?<br>" + "&nbsp;" * 5 +  \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                        "     with subject: 'insert' or 'Insert'" + "<br>" + "&nbsp;" * 5 + \
                                                        "     and message: attach a txt file (insert.txt) that <br>" + "&nbsp;" * 5 +" contains the link-machine you want to add.<br><br> \
                                        * Delete an existing machine from the list?<br>" + "&nbsp;" * 5 + \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                        "     with subject: 'delete' or 'Delete'" + "<br>" + "&nbsp;" * 5 + \
                                                        "     and message: attach a txt file (delete.txt) that <br>" + "&nbsp;" * 5 +" contains the link-machine you want to delete.<br><br>" \
                                        "* Update the current version of program from<br>" + "&nbsp;" * 5 + "GitHub?<br>" + "&nbsp;" * 5 + \
                                                "Send an email to " + str(ToMe) + "<br>" + "&nbsp;" * 5 + \
                                                "     with subject: 'update' or 'Update'" + "<br>" + "&nbsp;" * 6 + \
                                                "     and message: attach a txt file (update.txt) that <br>" + "&nbsp;" * 5 +" contains the number of changes made in the<br>" + "&nbsp;" * 5 + "GitHub today.<br><br>" \
                                        "Remember to add the extension" + "&nbsp;" * 5 + "'.txt'" +"&nbsp;" * 5 + "at the end of file.<br>" \
                                        "Pay attention to the name of the file<br>(insert.txt / delete.txt / update.txt).<br>You'll receive a notification of your action, if everything goes well.<br><br>" + "&nbsp;" * 60\
                                            + "Written in Python" , ToOther)
                        print("Emails sent. Purpose: Updates started.")
                        now = datetime.datetime.now()
                        
                        print("Running... >  " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + hour__ + ":" + min__ + ":" + sec__ )
                    now = datetime.datetime.now()
                    print("Total updates till now, (" + hour__ + ":" + min__ + ":" + sec__ + "): " , end = "" , flush = True)
                    if( int (open("totalUpdates.txt").read() ) <= 9):
                        print("0" + open("totalUpdates.txt").read())
                    else:
                        print(open("totalUpdates.txt").read())

                 
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
                time_correction()
                send_email("The errors just solved in 'www.car.gr'" , "The errors in 'www.car.gr' solved." + "&nbsp;" * 7 + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
                send_email("The errors just solved in 'www.car.gr'" , "The errors in 'www.car.gr' solved." + "&nbsp;" * 7 + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + hour__ + ":" + min__ + ":" + sec__ + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
                write_error("run_after_error.txt" , 0)
                print("Emails sent... Purpose: Unrecognized errors solved.")
                print("Running normally again, due to 20 errors...  >  " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + hour__ + ":" + min__ + ":" + sec__ )
            
            
            if(readTotalUpdates() == totalUpdateOfTheDay ):
                print( str(totalUpdateOfTheDay) + " updates have been performed before 23:55:00 .Sleeping till 23:55:00 ...")
                sleep__ = computeTimeSleep(23 , 55 , 0)
                time.sleep(sleep__)
            

            elif (readTotalUpdates() < totalUpdateOfTheDay ):
                for i in range( 1 ,  int( open("delay.txt").read() )):   # sleeping... & checking for network disconnection
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
                
                if(os.path.exists(PATH_NAME + "geckodriver.log")):   # file path may not be the same
                    os.remove(PATH_NAME + "geckodriver.log")
                file = open("updateNumber.txt", "w")    # open the file
                file.write(str(0))   # write the number in the file
                file.flush() 
                file.close()

                fileTotal = open("totalUpdates.txt", "w")    # open the file
                fileTotal.write(str(0))   # write the number in the file
                fileTotal.flush()
                fileTotal.close()

                fileEach = open("MachinesEachUpdate.txt" , "w")
                for i in range(0 , read_NumberOfMachines("NumberOfMachines.txt")):
                    fileEach.write(str(0) + "\n")
                fileEach.close()


                changeDelayOnceWrite("change_delay_once.txt" , 1)
                writeNumOfErrors("let_20_errors_happen.txt" , 0)
                write_delay("delay.txt" , 5)
                write_error("run_after_error.txt" , 0)
                __internetStatusError__Write("internet_statusError.txt" , 0)

                errors__ = open("totalErrors.txt" , 'w')
                errors__.write( str(0) )
                errors__.flush()
                errors__.close()

                internet_err_DATE_file = open("internet_error_DATE.txt" , 'w')
                internet_err_DATE_file.write( str(0) )
                internet_err_DATE_file.flush()
                internet_err_DATE_file.close()

                fileGitHub = open("GitHubUpdatesNumber.txt" , 'w')
                fileGitHub.write( str(0) )
                fileGitHub.flush()
                fileGitHub.close()

                # executes only once per day...
                print("Sleeping till next day...")
                time.sleep(10*60)
                print("Waiting till 06:59:50 pm ...")
                time.sleep( computeTimeSleep(6 , 59 , 50) )  # sleep till tomorrow morning at 7pm                
                
                driver.quit()   # quit firefox
                os.execv(sys.executable, ["python3"] + sys.argv)    # run again from the top
                


except OSError:
    print("===============================================\nAn OS error occured. Trying again. Loading...\n===============================================\n")
    
    send_email("WARNING !!! 'carClicker' app stopped" , "WARNING !!! 'carClicker' app stopped running due to an OS exception. Trying to restart application...<br>You may need to manually fix the problem if this continues." + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
    send_email("WARNING !!! 'carClicker' app stopped" , "WARNING !!! 'carClicker' app stopped running due to an OS exception. Trying to restart application...<br>You may need to manually fix the problem if this continues." + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
    current_time = datetime.datetime.now().time()   # get current time
    if(not current_time < on_time and not current_time >= off_time):
        read_TXT_FILE_from_gmail()
    # close all files...
    open("change_delay_once.txt").close()
    open("delay.txt").close()
    open("internet_error_DATE.txt").close()
    open("internet_statusError.txt").close()
    open("let_20_errors_happen.txt").close()
    open("MachinesEachUpdate.txt").close()
    open("NumberOfMachines.txt").close()
    open("run_after_error.txt").close()
    open("totalErrors.txt").close()
    open("totalUpdates.txt").close()
    open("updateNumber.txt").close()
    open("URL_machines.txt").close()
    open("GitHubUpdatesNumber.txt").close()
    open("passwords.txt").close()


    write_error("run_after_error.txt" , 1)
    writeNumOfErrors("let_20_errors_happen.txt" , 0)
    __totalErrorsOfDay__W("totalErrors.txt")
    writeNumOfErrors("let_20_errors_happen.txt" , readNumOfErrors("let_20_errors_happen.txt") + 1)

    driver.quit()   # quit firefox
    os.execv(sys.executable, ["python3"] + sys.argv)    # run again from the top




except: # if anything is wrong
    print("===============================================\nAn error occured. Trying again. Loading...\n===============================================\n")
    __totalErrorsOfDay__W("totalErrors.txt")
    writeNumOfErrors("let_20_errors_happen.txt" , readNumOfErrors("let_20_errors_happen.txt") + 1)
    current_time = datetime.datetime.now().time()   # get current time
    if(not current_time < on_time and not current_time >= off_time):
        read_TXT_FILE_from_gmail()
    if( readNumOfErrors("let_20_errors_happen.txt") == 20):
        with open("updateNumber.txt") as file:
            today = date.today()
            str_date = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
            send_email("20 errors occured in 'www.car.gr'  " + str_date , "20 errors occured while the application was running.Trying to restart application...<br>You may need to manually fix the problem if this continues." + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToMe)
            send_email("20 errors occured in 'www.car.gr'  " + str_date , "20 errors occured while the application was running.Trying to restart application...<br>You may need to manually fix the problem if this continues." + "<br><br>" + "&nbsp;" * 60 + "Written in Python" , ToOther)
            print("Emails just sent... Purpose: Unrecognized error")
            write_error("run_after_error.txt" , 1)
            writeNumOfErrors("let_20_errors_happen.txt" , 0)
    driver.quit()   # quit firefox
    os.execv(sys.executable, ["python3"] + sys.argv)    # run again from the top
