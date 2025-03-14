import multiprocessing
import subprocess


def startjarvis():
    # Code for process 1
    print("Process 1 is running")
    from main import start
    start()


def listenHotWord():
    # Code for process 2
    print("Process 2 is running")
    try:
        from assist.Engine.features import hotword
        print("Running hotword detection...")
        hotword()
    except Exception as e:
        print(f"Error in hotword detection: {e}")


# Start both processes
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=startjarvis)
    p2 = multiprocessing.Process(target=listenHotWord)
    
    # Start both processes
    p1.start()
    p2.start()
    
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()
     
    print("System stopped")
