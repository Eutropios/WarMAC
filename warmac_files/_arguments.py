"""
File that contains function to add command line functionality
"""
import argparse

def create_parser() -> argparse.ArgumentParser:
    """_summary_

    :return: ArgumentParser with appropriate documentation and functionality
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test',
                        default=0.1,
                        type=float,
                        help='test')
    # Many more arguments
    return parser
