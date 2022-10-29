def save(data: str, file: str, mode='w', log=False):
    log and print(f'Saving data to {file}...')
    with open(file, mode) as f:
        f.write(data)
    log and print('  Saved successfully!')
