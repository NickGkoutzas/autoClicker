import os , time , sys
i = 1
while(1):
    if(i == 20):
        time.sleep(300)
        os.system("wget 'https://github.com/NickGkoutzas/autoClicker/raw/main/test.py'")
        
        os.system("python3 test.py.2")
    else:
        print("helloooooo " + str(i))
        time.sleep(1)
        i += 1
    