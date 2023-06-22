import os

def find_files(directory, extension):
    result = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                result.append(os.path.join(root, file))
    return result

# Example usage
directory = '/mnt/data/Media/Movies/'
extension = '.old'
files = find_files(directory, extension)
for file in files:
    print(file)
