import argparse

###################################################################################################
# GLOBAL PARSER
parser = argparse.ArgumentParser(
    description="YoutubeDL-Subscribe: Download and organize your favorite media hassle-free."
)
parser.add_argument(
    "-c",
    "--config",
    metavar="CONFIGPATH",
    type=str,
    help="path to the config yaml, uses config.yaml if not provided",
    default="config.yaml",
)
###################################################################################################
# SUBSCRIPTION PARSER
subparsers = parser.add_subparsers(dest="subparser")
subscription_parser = subparsers.add_parser("sub")
subscription_parser.add_argument(
    "subscription_paths",
    metavar="SUBPATH",
    nargs="*",
    help="path to subscription files, uses config.yaml if not provided",
    default="config.yaml",
)
###################################################################################################
# DOWNLOAD PARSER
download_parser = subparsers.add_parser("dl")