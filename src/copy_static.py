import os
import shutil

def copy(source_dir, dest_dir):
    # First clear the destination directory once at the very start, outside of recursion
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    # List contents of the source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)  # Full path of item in source
        dest_path = os.path.join(dest_dir, item)      # Corresponding path in destination

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        elif os.path.isdir(source_path):
            # Create the directory in the destination path
            os.mkdir(dest_path)
            # Recursively copy contents
            copy(source_path, dest_path)

# Example usage


