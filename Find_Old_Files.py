import os
import sys

def main(directory, extension):
    global conflicts
    global counter
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    old_file = os.path.join(root, file)
                    new_file = os.path.join(root, file.replace(extension, ''))
                    print(old_file)
                    print(new_file)
                    if os.path.exists(new_file):
                        conflicts += 1
                        print('CONFLICT')
                    print('\n')
                    counter += 1
                    #os.rename(old_file, new_file)
        print(counter)
        print(conflicts)
    except:
        sys.exit(1)

if __name__ == "__main__":
    counter = 0
    conflicts = 0
    directory = '/mnt/data/Media/Shows/'
    extension = '.old'
    main(directory, extension)
