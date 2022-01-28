import threading as Threading
class testClass():
    def test(self, a):
        at = Threading.Thread(target=self.threadTest, args=(a,))
        at.start()
        at.join()
        
        print(a)
        pass
    
    def threadTest(self, a):
        _a = a;
        while(_a < 100):
            _a+=1
        print(_a) 
        
    

tc = testClass()
a = 1
tc.test(a)