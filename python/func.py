import sys
import ngender

if len(sys.argv)==3:
    if sys.argv[1]=="ng":
        dt=ngender.guess(sys.argv[2])
        if dt[0]=="male":
            g="男"
        else:
            g="女"
        text=sys.argv[2]+"的姓名猜测性别是："+g+"\n概率："+str(dt[1]*100)+"%"

with open(r"D:\Program Source\QQBOT\python\Temp\temp.txt","w+",encoding="UTF-8") as f:
    text=str(text)
    f.write(text)
    print(text)