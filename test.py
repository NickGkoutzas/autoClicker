import os , sys , time
j = 1
os.system()
i = 1
if(j > 1):
    os.system("rm -r test.py." + str(j-1))
while(1):
    if(i == 20):
        os.system("wget 'https://github.com/NickGkoutzas/autoClicker/raw/main/test.py'")
        #os.execv(sys.executable, ["python3"] + sys.argv)
        os.system("python3 test.py." + str(j+1))
    else:
        print("Hello  -> " + str(i))
        time.sleep(1)
    i += 1