import os

def generate_file_tree(dir_path, file, indent_level=0):
    try:
        entries = sorted(os.listdir(dir_path))
    except OSError as e:
        file.write(f"Access denied: {dir_path}\n")
        return
    for entry in entries:
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            file.write('    ' * indent_level + f"+ {entry}/\n")
            generate_file_tree(full_path, file, indent_level + 1)
        else:
            file.write('    ' * indent_level + f"- {entry}\n")
root_directory = input("Enter the directory path to generate the file tree: ")
output_file_path = input("Enter the output file path: ")
with open(output_file_path, 'w') as file:
    file.write(f"File Tree of {root_directory}:\n")
    generate_file_tree(root_directory, file)

print(f"Directory tree has been written to {output_file_path}")
