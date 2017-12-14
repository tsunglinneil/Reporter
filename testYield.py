# coding=utf-8
# 關於yield的測試

def yield_test(n):  
    for i in range(n):  
        print("Before Yield is {}".format(i))
        yield call(i)   #
        print("i=",i)       
    print("do something.")      
    print("end.")  
  
def call(i):  
    return i*2  
 
for i in yield_test(5):  
    print(i,",")
