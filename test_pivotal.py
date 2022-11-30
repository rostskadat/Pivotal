#!/usr/bin/env python
"""
Launch test of the LCS module
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import lcs
import logging
import sys

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def launch_test(args):
    """_summary_

    Args:
        args (_type_): _description_
    """
    # response = lcs.get_form_data(args.username, args.password, 'oraContact', '000000000000005C')
    parameters = [('string', 'es-ES'), ('string', '0010027100')]
    response = lcs.execute_asr("username", "password", 'SolWeb', 'ConsultaDetalleSiniestro', parameters)
    logger.info(response)
    return

def parse_command_line():
    parser = ArgumentParser(prog='test_pivotal',
                            description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--username', help='The username to access the server', required=False, default=None)
    parser.add_argument(
        '--password', help='The password to access the server', required=False, default=None)
    parser.set_defaults(func=launch_test)
    return parser.parse_args()


def main():
    args = parse_command_line()
    try:
        if args.debug:
            logger.setLevel(logging.DEBUG)
        return args.func(args)
    except Exception as e:
        logging.error(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
