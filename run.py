#to run jarivis
import multiprocessing
import subprocess


def startjarvis():
    #code for process 1
    print("process 1 is running")
    from main import start
    start()
 
#to run hotword   
def listenHotWord():
    #code for process 1
    print("process 2 is running")
    from assist.Engine.features import hotword
    hotword()
    
# Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startjarvis)
        p2 = multiprocessing.Process(target=listenHotWord)
        p1.start()
        subprocess.call([r'device.bat'])
        p2.start()
        p1.join()
        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")