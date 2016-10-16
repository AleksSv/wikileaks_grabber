import os
import sys, getopt
from threading import *

from urllib.request import urlopen

def main(argv):

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

    print("Grabbing emails from " + str(start) + " to " + str(end))

    directory = "podesta"
    urls = []


    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(start, end + 1):

        urls.append(["https://wikileaks.org/podesta-emails//get/" + str(i),str(i) + ".eml"])

        # u = urlopen("https://wikileaks.org/podesta-emails//get/" + str(i))
        # filename =
        # localFile = open(directory + "/" + filename, 'wb')
        # localFile.write(u.read())
        # localFile.close()



    class worker(Thread):
        def __init__(self, link, filename):
            Thread.__init__(self)
            self.link = link
            self.filename = filename
            self.start()
        def run(self):
            u = urlopen(self.link)
            localFile = open(directory + "/" + self.filename, 'wb')
            localFile.write(u.read())
            localFile.close()
            print("Downloaded " + self.filename)

    for url in urls:
        worker(url[0],url[1])


if __name__ == "__main__":
   main(sys.argv[1:])