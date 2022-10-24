import os , time , sys
j = 1
i = 1
while(1):
    if(i == 20):
        os.system("wget 'https://github.com/NickGkoutzas/autoClicker/raw/main/test.py' && mv test.py.1 test.py")
        time.sleep(2)
        
        os.execv(sys.executable, ["python3"] + sys.argv)
        #os.system("python3 test.py.2")
    else:
        print("helloooooo " + str(i))
        time.sleep(1)
    i += 1
    