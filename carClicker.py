# Nick Gkoutzas , Feb 2022


from selenium import webdriver
from datetime import datetime , time , date
import time , datetime , os , sys , smtplib , linecache , socket , imaplib , email , traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.firefox.options import Options




# Fill the information !!!
#====================================
FROM_EMAIL = "email"                    
FROM_PWD = "password"             
ToMe = "email"
ToOther = "other_email"
site_username = "username"
site_password = "password"
PATH_NAME = "path_name"
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
    link = __file.read().strip("\n")
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






def read_URL_machines_FILE(file__ , which_line):
    URL_machine = linecache.getline(file__ , which_line).strip("\n")
    return str(URL_machine)





def delete_from_URL_MACHINES_FILE(file__ , URL):
    for i in range( read_NumberOfMachines("NumberOfMachines.txt") ):
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
finished_earlier = True





def email_sendToOther(SUBJECT , message):
    global FROM_EMAIL , FROM_PWD , ToOther
    FROM = FROM_EMAIL
    TO = ToOther

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


def email_sendToMe(SUBJECT , message):
    global FROM_EMAIL , FROM_PWD , ToMe
    FROM = FROM_EMAIL
    TO = ToMe

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




def read_TXT_FILE_from_gmail():
    global ToOther

    found_insert_or_delete_word = 0
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    mail.select('inbox')

    data = mail.search(None, 'ALL')
    mail_ids = data[1]
    id_list = mail_ids[0].split()   
    latest_email_id = int(id_list[-1])
    check_last_N_emails = 5
    for e in range(latest_email_id , latest_email_id - check_last_N_emails , -1):
        data = mail.fetch(str(e), '(RFC822)' )
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1],'utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']

        for part in msg.walk():
            filename__ = part.get_filename()
            if filename__:
                open(PATH_NAME + str(filename__) , "wb").write(part.get_payload(decode=True))
                
        if(email_subject == "delete"):
            found_insert_or_delete_word = 1
            exists = 0
            for s in range(read_NumberOfMachines("NumberOfMachines.txt") ):
                if(linecache.getline("URL_machines.txt" , s).strip("\n") == read_file_from_email(filename__) ):
                    delete_line("MachinesEachUpdate.txt" , s - 1, machinesEachUpdate)
                    delete_from_URL_MACHINES_FILE("URL_machines.txt" , read_file_from_email(filename__) )
                    exists = 1
                    break
            
            now = datetime.datetime.now()

            if(exists == 0):    # the url that sent me ,does not exist in my list
                #email_sendToOther("Problem: Machine can not be deleted in 'www.car.gr'" , read_file_from_email(filename__) +  " does not exist in the list .<br>Time: " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
                email_sendToMe("Problem: Machine can not be deleted in 'www.car.gr'" , read_file_from_email(filename__) +  " does not exist in the list .<br>Time: " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
                

            else:
                #email_sendToOther("List updated in 'www.car.gr': A machine deleted " , read_file_from_email(filename__) +  " deleted succesfully.<br>List of all machines updated at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)  + "<br>You may not be able to see the machine on the site, because the administrator has removed it.")
                email_sendToMe("List updated in 'www.car.gr': A machine deleted " , read_file_from_email(filename__) +  " deleted succesfully.<br>List of all machines updated at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "<br>You may not be able to see the machine on the site, because the administrator has removed it.")
                    
                write_EDIT__file_NumberOfMachines("NumberOfMachines.txt" , read_NumberOfMachines("NumberOfMachines.txt") - 1 )
            return

        elif(email_subject == "insert"):
            found_insert_or_delete_word = 1
            for s in range(read_NumberOfMachines("NumberOfMachines.txt") ):
                if(linecache.getline("URL_machines.txt" , s).strip("\n") == read_file_from_email(filename__) ):
                    now = datetime.datetime.now()
                    #email_sendToOther("Warning in 'www.car.gr': A machine already exists " , read_file_from_email(filename__) +  " already exists in the list.<br>Time: " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
                    email_sendToMe("Warning in 'www.car.gr': A machine already exists " , read_file_from_email(filename__) +  " already exists in the list.<br>Time: " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
                    return
            write_EDIT__file_NumberOfMachines("NumberOfMachines.txt" , read_NumberOfMachines("NumberOfMachines.txt") + 1 )
            with open("URL_machines.txt", "a") as __file__:
                __file__.write(read_file_from_email(filename__)+"\n")

            with open("MachinesEachUpdate.txt", "a") as __file:
                __file.write(str(0)+"\n")

            now = datetime.datetime.now()
            #email_sendToOther("List updated in 'www.car.gr': A machine inserted " , read_file_from_email(filename__) +  " inserted succesfully.<br>List of all machines updated at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
            email_sendToMe("List updated in 'www.car.gr': A machine inserted " , read_file_from_email(filename__) +  " inserted succesfully.<br>List of all machines updated at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
            return


        else:
            if(e == check_last_N_emails and found_insert_or_delete_word == 0 and email_from == ToOther):
                now = datetime.datetime.now()
                #email_sendToOther("Problem in 'www.car.gr': Specify what you want to do: 'delete' or 'insert'" , "Subject of email does not contain nor the word 'delete' neither 'insert' word ,but '" + str(email_subject) + "' given instead.Please, try again...<br>Time: " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
                email_sendToMe("Problem in 'www.car.gr': Specify what you want to do: 'delete' or 'insert'" , "Subject of email does not contain nor the word 'delete' neither 'insert' word ,but '" + str(email_subject) + "' given instead.Please, try again...<br>Time: " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
                


read_TXT_FILE_from_gmail()



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




def readTotalUpdates():
    read_update = open("totalUpdates.txt" , 'r')
    return int( read_update.read() )




def error_and_back_to_internet():
    if( not check_internet_connection() ):
        print("Disconnected from the network...")
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
                print("Connected again...")
                write_delay("delay.txt" , computeDelay(23 , 55 , 0) )
                __internetStatusError__Write("internet_statusError.txt" , 0)
                now = datetime.datetime.now()
                email_sendToOther("[SOLVED] Internet connection error" , "There was a problem connecting<br>to the network at " + str( open("internet_error_DATE.txt").read() ) + "<br><br>Possible problems:<br>1) Ethernet cable disconnected<br>2) Bad Wi-Fi connection<br>3) Power outage<br>" + "<br>The problem solved at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
                email_sendToMe("[SOLVED] Internet connection error" , "There was a problem connecting<br>to the network at " + str( open("internet_error_DATE.txt").read() ) + "<br><br>Possible problems:<br>1) Ethernet cable disconnected<br>2) Bad Wi-Fi connection<br>3) Power outage<br>" + "<br>The problem solved at " +  str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
                print("Sent email due to network disconnection... > " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))




# Go to this link
# https://www.youtube.com/redirect?v=YPiHBtddefI&redir_token=QUFFLUhqa3phOTlrSjk3RWpRNThXSHJBUDNobzRpNXlFZ3xBQ3Jtc0ttbzhFSXhmai1Mb19ORG9NYzVGa2lwcVNyWG9TYnkxWDZPd1RiQ2JPX05LTlRPQVpTeVMwN0tQWFN6SlZwWThCZFBWcmhFQTZfSlkwVzZ5NXVYaWNVRjVzYTdpT015bXY5UnVqTWFXcmpvQURIVHRBNA%3D%3D&event=video_description&q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps%3Fpli%3D1
# to enable 'less secure apps' 



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

    cookies = driver.find_element_by_css_selector(".css-ofc9r3")      # accept cookies
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

                file = open("wait.txt", "w")    # open the file
                file.write(str(1))   # write the number in the file
                file.flush()

                read_TXT_FILE_from_gmail() # check if the admin of the site sent an email...

                with open("updateNumber.txt") as file:
                    currentPosUpdate = int(file.read())  # read the number from file
                    machine = driver.get( read_URL_machines_FILE("URL_machines.txt" , currentPosUpdate + 1) )

                
                error_and_back_to_internet()
                updateMachine = driver.find_element_by_css_selector("div.list-group-item:nth-child(1)")     # find the update button
                error_and_back_to_internet()
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
                        email_sendToOther("Updates started" , "This email informs you that the updates for '" + str(str_date) + "' started at " + updatesStartedAt() )
                        email_sendToMe("Updates started" , "This email informs you that the updates for '" + str(str_date) + "' started at " + updatesStartedAt() )
                        print("Emails sent... Purpose: Start of the new day.")
                        now = datetime.datetime.now()
                        print("Running... >  " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
                    print("Total updates till now: " + open("totalUpdates.txt").read())
                    
                currentPosUpdate += 1       # increase current position of machine update
                file = open("updateNumber.txt", "w")    # open the file
                file.write(str(currentPosUpdate))   # write the number in the file
                file.flush()    
                

            if(currentPosUpdate == read_NumberOfMachines("NumberOfMachines.txt")):  # if update of all machines finished
                currentPosUpdate = 0                    # start again
                file = open("updateNumber.txt", "w")    # open the file
                file.write(str(currentPosUpdate))   # write the number in the file
                file.flush() 

            if( read_error("run_after_error.txt") == 1 ):
                now = datetime.datetime.now()
                email_sendToOther("The errors just solved in 'www.car.gr'" , "The errors in 'www.car.gr' solved." + "&nbsp;" * 7 + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
                email_sendToMe("The errors just solved in 'www.car.gr'" , "The errors in 'www.car.gr' solved." + "&nbsp;" * 7 + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
                write_error("run_after_error.txt" , 0)
                print("Emails sent... Purpose: Errors solved.")
                print("Running normally again, due to an 5 errors...  >  " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "  ,  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) )
            
            
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
            if( int( open("wait.txt" , 'r').read() ) == 1):
                file = open("wait.txt", "w")    # open the file
                file.write(str(0))   # write the number in the file
                file.flush()

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
                    email_sendToOther("'www.car.gr' Update ~ " + str_date , open("totalUpdates.txt").read() + " updates were performed successfully.<br>Total errors during the day: " + str(__totalErrorsOfDay__R("totalErrors.txt")) + "<br>" + all_machines_updates_number)
                    email_sendToMe("'www.car.gr' Update ~ " + str_date , open("totalUpdates.txt").read() + " updates were performed successfully.<br>Total errors during the day: " + str(__totalErrorsOfDay__R("totalErrors.txt")) + "<br>" + all_machines_updates_number)
                    print("Emails just sent... Purpose: Success")
                
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
                writeNumOfErrors("let_5_errors_happen.txt" , 0)
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

                #write_select_edit("select_edit" , 0)


                # executes only once per day...
                print("Sleeping till next day...")
                time.sleep(10*60)
                print("Waiting till 06:59:50 pm ...")
                time.sleep( computeTimeSleep(6 , 59 , 50) )  # sleep till tomorrow morning at 7pm                
                
                driver.quit()   # quit firefox
                os.execv(sys.executable, ["python3"] + sys.argv)    # run again from the top
            



except: # if anything is wrong
    print("AN ERROR OCCURED. Trying again. Loading...")
    read_TXT_FILE_from_gmail() # check if the admin of the site sent an email...
                
    if( int( open("delay.txt").read() ) >= 10 ):
        write_delay("delay.txt" , int( open("delay.txt").read() ) - 5 )
    __totalErrorsOfDay__W("totalErrors.txt")
    writeNumOfErrors("let_5_errors_happen.txt" , readNumOfErrors("let_5_errors_happen.txt") + 1)

    
    if( readNumOfErrors("let_5_errors_happen.txt") == 5):
        with open("updateNumber.txt") as file:
            today = date.today()
            str_date = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
            email_sendToOther("5 errors occured in 'www.car.gr'  " + str_date , "5 errors occured while the application was running.Trying to restart application...<br>Note: If this e-mail reappears, check the raspberry pi, otherwise the problem will have already been solved.")
            email_sendToMe("5 errors occured in 'www.car.gr'  " + str_date , "5 errors occured while the application was running.Trying to restart application...<br>Note: If this e-mail reappears, check the raspberry pi, otherwise the problem will have already been solved.")
            print("Emails just sent... Purpose: Error")
            write_error("run_after_error.txt" , 1)
            writeNumOfErrors("let_5_errors_happen.txt" , 0)
    driver.quit()   # quit firefox
    os.execv(sys.executable, ["python3"] + sys.argv)    # run again from the top
