import time
i = 1
thing = True
while True:
    if i >= 100:
        thing = False
    elif i <= 0:
        thing = True

    if thing: i+= 1
    else: i-= 1
    print(f"\r\033[38;2;{int(float(i/100)*255)};0;{255-int(float(i/100)*255)}m" + "THIS GITHUB REPOSITORY WAS SPONSORED BY TOAST" + "\033[0m", end="")
    time.sleep(0.1)