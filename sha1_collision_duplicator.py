import pymd5
import sys

"""
This program is based on Google finding 2 files that have the same SHA1 hash and different contents.
What it does is take input from the user and 2 files that have the same SHA1 hash('good.pdf' and 'bad.pdf' in this case, but that can be edited in the code).
It then creates 2 new files that have equivalent SHA1 hashes, but differing contents, including the user's input in the files as well.
"""

def main():
    #exit if wrong incorrect of args
    if(len(sys.argv) < 3):
        print("correct usage: python2.7 sha1Crack.py new_file_1 new_file_2")
        sys.exit(0)

    print("Get ready to create 2 files that have different contents, but the same SHA1 hashes.")
    print("We will use the 'good.pdf' and 'bad.pdf' files I provided to do this. So make sure that they are in the same folder where you're running this from.")
    user_input = raw_input("\nType what you want to add to our prexisting files: ")

    quit_or_continue = raw_input("\nCAUTION, file " + sys.argv[1] + " and " + sys.argv[2] + " will be created, or overwritten if they exist. \nType 'c' to continue, any other character to quit, then press ENTER: ")

    if(quit_or_continue != 'c'):
        sys.exit(0)

    #check to see if read files are ok
    try:
        #work with the files that have the same SHA1, but different content
        with open("good.pdf", 'r') as old_first_sha1_file, open("bad.pdf", 'r') as old_second_sha1_file:
            #store those files' contents
            first_sha1_contents_to_write = old_first_sha1_file.read()
            second_sha1_contents_to_write = old_second_sha1_file.read()
    except IOError:
        print("\nCouldn't open files for reading!\nExiting")
        sys.exit(1)

    #merkle-damgard block chain padding. calculate padding based on lengths of original files. in this case, len(first_sha1_contents_to_write) == len(second_sha1_contents_to_write)
    pad = pymd5.padding(len(first_sha1_contents_to_write)*8)

    #append the padding and the user_input to get a SHA1 collision
    first_sha1_contents_to_write += pad + user_input
    second_sha1_contents_to_write += pad + user_input

    #check to see if write files are ok
    try:
        #work with the files that we want to write to
        with open(sys.argv[1], 'w') as new_first_sha1_file, open(sys.argv[2], 'w') as new_second_sha1_file:
            #write to the files 
            new_first_sha1_file.write(user_input)
            new_second_sha1_file.write(user_input)
    except IOError:
        print("\nCouldn't open files for writing!\nExiting")
        sys.exit(1)

    print("\n\nCongratulations, you now have 2 files, " + sys.argv[1] + " and " + sys.argv[2] + " , that have different contents, but the same SHA1 hash!\n") 

    print("\nNow compare the SHA1 hashes of each file with: openssl dgst -sha1 " + sys.argv[1] + " " + sys.argv[2])
    print("Compare the difference in the contents of the files with: diff " + sys.argv[1] + " " + sys.argv[2])

if __name__ == "__main__":
    main()
