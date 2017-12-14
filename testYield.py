# coding=utf-8
# 關於yield的測試

def yield_test(n):  
    for i in range(n):  
        print("Before Yield is {}".format(i))
        yield call(i)   #yield就像是return返回一個值(yield 右邊的值)，並且記住這個返回的位置，下次iter就從這個位置後(下一行)開始
        print("i=",i)       
    print("do something.")      
    print("end.")  
  
def call(i):  
    return i*2  
 
for i in yield_test(5):  
    print(i,",")
