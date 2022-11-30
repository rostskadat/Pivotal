#!/usr/bin/env python
"""
Launch test of the LCS module.

SYNOPSIS:

test_pivotal.py --username username --password password --form-name "oraContact" --record-id "000000000000005C"
test_pivotal.py --username username --password password --asr-name "SolWeb" --method-name "ConsultaDetalleSiniestro" --parameters string,es-ES --parameters string,0010027100
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
    if args.form_name and args.record_id:
        response = lcs.get_form_data(args.username, args.password, args.form_name, args.record_id)
    elif args.asr_name and args.method_name:
        parameters = []
        for parameter in args.parameters:
            (type, value) = parameter[0].split(",")
            parameters.append((type, value))
        response = lcs.execute_asr(args.username, args.password, args.asr_name, args.method_name, parameters)
    else:
        logger.error()
    logger.info(response)

def parse_command_line():
    parser = ArgumentParser(prog='test_pivotal',
                            description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--username', help='The username to access the server', required=False, default=None)
    parser.add_argument(
        '--password', help='The password to access the server', required=False, default=None)
    parser.add_argument(
        '--form-name', help='The form to call in order to get a specific record', required=False, default=None)
    parser.add_argument(
        '--record-id', help='The record id to get', required=False, default=None)
    parser.add_argument(
        '--asr-name', help='The name of the script / asr to call', required=False, default=None)
    parser.add_argument(
        '--method-name', help='The method name to call', required=False, default=None)
    parser.add_argument(
        '--parameters', help='The parameter of the call', required=False, default=None, type=str, nargs='+', action='append')
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
