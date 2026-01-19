with open('.env', 'rb') as f:
    content = f.read()
    if b'\x00' in content:
        print("Found NULL in .env")
    else:
        print("Clean .env")
