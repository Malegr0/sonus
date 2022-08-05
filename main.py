import argparse


def evaluate_args():
    parser = argparse.ArgumentParser()
    # add arguments here
    parser.add_argument("-t", action="store_true", help="test")

    args = parser.parse_args()
    if args.t:
        print("test")


if __name__ == '__main__':
    evaluate_args()
