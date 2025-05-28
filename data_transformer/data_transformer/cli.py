import sys
import argparse

parser = argparse.ArgumentParser()
parser.parse_args()

def main():
    print("Arguments passed:", sys.argv)

if __name__ == "__main__":
    main()