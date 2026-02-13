import os
import shutil


def move_helper(current_from, current_to):
    if not os.path.isdir(current_to):
        os.mkdir(current_to)
    for item in os.listdir(current_from):
        full_from = os.path.join(current_from, item)
        full_to = os.path.join(current_to, item)
        if os.path.isfile(full_from):
            shutil.copy(full_from, full_to)
        else:
            #print(f"moving into directory '{full_from}'")
            move_helper(full_from, full_to)

def move_from_static_to_public():
    current_dir = os.path.dirname(__file__)
    static_dir = os.path.join(current_dir, "../static")
    public_dir = os.path.join(current_dir, "../public")
    for item in os.listdir(public_dir):
        full_path = os.path.join(public_dir, item)
        if os.path.basename(public_dir) != "public":
            raise Exception("fatal: Trying to delete from inaccessible folder")
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)
    move_helper(static_dir, public_dir)



