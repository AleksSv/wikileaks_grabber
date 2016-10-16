import os
import sys, getopt
from queue import Queue
from threading import *

from urllib.request import urlopen

def main(argv):

    num_worker_threads = 4

    start = 1
    end = 10

    try:
        opts, args = getopt.getopt(argv, "hi:s:e:", ["start=", "end="])
    except getopt.GetoptError:
        print('wikileaks.py -s <start_index> -e <end_index>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('wikileaks.py -s <start_index> -e <end_index>')
            sys.exit()
        elif opt in ("-s", "--start"):
            start = int(arg)
        elif opt in ("-e", "--end"):
            end = int(arg)

    ow_input = input("Do you want to overwrite emails? y/n")
    ow = False
    if(ow_input == "y"):
        print("Overwriting Emails")
        ow = True
    else:
        print("Downloading new files only")


    print("Grabbing emails from " + str(start) + " to " + str(end))

    directory = "podesta"


    if not os.path.exists(directory):
        os.makedirs(directory)

    q = Queue()

    for i in range(start, end + 1):
        q.put(["https://wikileaks.org/podesta-emails//get/" + str(i),str(i) + ".eml"])

    class worker(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.start()
        def run(self):
            while True:
                item = q.get()
                self.download(item[0],item[1])
                q.task_done()

        def download(self,link,filename):
            if(os.path.isfile(directory + "/" + filename)):
                if(ow):
                    print("Overwriting " + filename)
                else:
                    print("Ignoring " + filename + " because it already exists")
                    return

            u = urlopen(link)
            localFile = open(directory + "/" + filename, 'wb')
            localFile.write(u.read())
            localFile.close()
            print("Downloaded " + filename)


    for i in range(num_worker_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    q.join()

if __name__ == "__main__":
   main(sys.argv[1:])