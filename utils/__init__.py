def save(data: str, file: str, mode='w'):
    with open(file, mode) as f:
        f.write(data)
