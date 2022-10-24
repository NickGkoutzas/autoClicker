import os , sys , time
j = 2
i = 1

while(1):
    if(i == 20):
        os.system("wget 'https://github.com/NickGkoutzas/autoClicker/raw/main/test.py'")
        #os.execv(sys.executable, ["python3"] + sys.argv)
        #if(j > 1):
         #   os.system("rm -r test.py." + str(j-1))
        os.system("python3 test.py." + str(j))
    else:
        print("Hello  -> " + str(i))
        time.sleep(1)
    i += 1