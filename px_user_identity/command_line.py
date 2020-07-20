from sys import stdout
import px_user_identity

def main():
    r = px_user_identity.main()
    stdout.flush()
    if type(r) == str:
        stdout.write(r)
    else:
        stdout.buffer.write(r)
    stdout.flush()

if __name__ == '__main__':
    main()