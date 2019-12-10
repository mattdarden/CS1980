from hypothesis_one import one_main
from hypothesis_two import two_main
import string

def main():
    file = 'classes.txt'            #setting the file path to the file with the classes and types of tests to run
    with open(file) as fp:
        line = fp.readline()        #reading the first line of the file
        while line:                 #while the line is still valid
            linelist = line.strip().split(' ')      #split the line up by the spaces and assign each as follows
            onedep = linelist[0]
            onenum = linelist[1]
            twodep = linelist[2]
            twonum = linelist[3]
            test = linelist[4]
            #informing that the following results are from this line in the file
            print('\nTest results for line:{} {} {} {} {}'.format(onedep, onenum, twodep, twonum, test))
            if test.upper() == 'GRADES':    # run the first hypothesis test if they want to compare the grades
                one_main(onedep.upper(), onenum, twodep.upper(), twonum)
            elif test.upper() == 'TIME':    # run the second hypothesis test if they want to compar the time between the classes
                two_main(onedep.upper(), onenum, twodep.upper(), twonum)
            else:
                print('Invalid Test')
            line = fp.readline()
        fp.close()

if __name__ == '__main__':
    main()
