import sys
import yaml


def smudge_or_clean(do_smudge):
    try:
        with open('secret.yaml') as secret_yaml:
            secret = yaml.safe_load(secret_yaml)
    except FileNotFoundError:
        secret = {}
    for line in sys.stdin:
        line = line.rstrip()
        key = line.split('=', 1)[0].strip() if '=' in line else None
        print(' = '.join((key, secret[key] if do_smudge else '')).rstrip()
              if key in secret else line)


if __name__ == '__main__':
    smudge_or_clean(dict(smudge=True, clean=False)[sys.argv[1]])