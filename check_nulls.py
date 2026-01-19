import os

def check_dir(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') or file.endswith('.ini'):
                f_path = os.path.join(root, file)
                try:
                    with open(f_path, 'rb') as f:
                        if b'\x00' in f.read():
                            print(f"NULL: {f_path}")
                except:
                    pass

check_dir('alembic')
if os.path.exists('alembic.ini'):
    with open('alembic.ini', 'rb') as f:
        if b'\x00' in f.read():
            print("NULL: alembic.ini")
