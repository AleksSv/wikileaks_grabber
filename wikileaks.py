import os
import sys, getopt
from urllib.request import urlopen

def main(argv):

    start = 1
    end = 10

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["start=", "end="])
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

    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(start, end + 1):

        u = urlopen("https://wikileaks.org/podesta-emails//get/" + str(i))
        filename = str(i) + ".eml"
        localFile = open(directory + "/" + filename, 'wb')
        localFile.write(u.read())
        localFile.close()

        print("Downloaded " + filename)

if __name__ == "__main__":
   main(sys.argv[1:])