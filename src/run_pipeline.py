import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description='LeetCode Data & Visualization Pipeline'
    )
    parser.add_argument(
        '--run',
        action='store_true',
        help='Run full pipeline'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Number of problems to fetch'
    )
    args = parser.parse_args()

    if args.run:
        run_pipeline(problem_limit=args.limit)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
