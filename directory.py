import os

startpath = input("Enter the path of the directory you want to inspect: ")
output_file = input("Enter the path for the output text file where the directory tree will be saved: ")
def print_directory_tree(startpath, output_file):
    with open(output_file, "w") as f:
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            f.write(f"{indent}{os.path.basename(root)}/\n")
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write(f"{subindent}{file}\n")

print_directory_tree(startpath, output_file)
