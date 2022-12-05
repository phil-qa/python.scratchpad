def pretty_sumab(func):
    def inner(a,b):
        print(f"{a} + {b} is ")
        return func(a,b)
    return inner


@pretty_sumab
def sumab(a,b):
    summed = a + b
    print(summed)

sumab(3,5)

import time                                                                                                               
                                                                                                                          
def measure_time(func):                                                                                                   
                                                                                                                          
  def wrapper(*arg):                                                                                                      
      t = time.time()                                                                                                     
      res = func(*arg)                                                                                                    
      print("Function took " + str(time.time()-t) + " seconds to run")                                                    
      return res                                                                                                          
                                                                                                                          
  return wrapper                                                                                                          
                                                                                                                          
@measure_time                                                                                                             
def myFunction(n):                                                                                                        
  time.sleep(n)   

myFunction(3)