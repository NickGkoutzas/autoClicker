def changeDelayOnceWrite(file_name , number): # in the beginning 'number' must be '1'... -> 'change_delay_once.txt'
    once = open(file_name , 'w')
    once.write( str(number) )
    once.flush()
    once.close()

def writeNumOfErrors(file_name , number):
    write_err = open(file_name , 'w')
    write_err.write( str(number) )
    write_err.flush()
    write_err.close()

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

def read_NumberOfMachines(file_name):
    numOfMach = open(file_name , 'r')
    numberOfMachines__ = numOfMach.read()
    numOfMach.close()
    return int(numberOfMachines__)

def __internetStatusError__Write(file_name , status): # '1' if an error occured , else '0' -> normal
    delay = open(file_name , 'w')
    delay.write( str(status) )
    delay.flush()
    delay.close()

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

GitHub_updates_number = open("GitHubUpdatesNumber.txt" , 'w')
GitHub_updates_number.write( str(0) )
GitHub_updates_number.flush()
GitHub_updates_number.close()

internet_err_DATE_file = open("internet_error_DATE.txt" , 'w')
internet_err_DATE_file.write( str(0) )
internet_err_DATE_file.flush()
internet_err_DATE_file.close()