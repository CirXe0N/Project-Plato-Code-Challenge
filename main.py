import argparse
import asyncio
from pathlib import Path

from crawler.crawlers import Crawler


def main():
    parser = argparse.ArgumentParser(
        description='Project Plato Crawler',
        epilog='Enjoy the program! :)',
    )
    parser.add_argument(
        '-u',
        '--url',
        type=str,
        required=True,
        dest='url',
        help='the initial URL to start crawling from'
    )
    parser.add_argument(
        '-p',
        '--path',
        type=str,
        dest='path',
        default='./out',
        help='the path to the output file'
    )
    parser.add_argument(
        '-n',
        '--num_workers',
        type=int,
        dest='num_workers',
        default=5,
        help='the amount of workers'
    )

    args = parser.parse_args()

    c = Crawler(
        initial_url=args.url,
        num_workers=args.num_workers,
        out_path=Path(args.path)
    )
    asyncio.run(c.run())


if __name__ == "__main__":
    main()

