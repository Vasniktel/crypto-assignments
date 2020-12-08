from Crypto.Random import get_random_bytes


if __name__ == '__main__':
  with open('kek.txt', 'wb') as f:
    f.write(get_random_bytes(32))
