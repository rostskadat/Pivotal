#!/usr/bin/env python
"""
Launch test of the LCS module.

SYNOPSIS:

test_pivotal.py --username username --password password --command "get_user_id" 
test_pivotal.py --username username --password password --command "get_form_data" --form-name "oraContact" --record-id "000000000000005C"
test_pivotal.py --username username --password password --command "execute_asr" --asr-name "SolWeb" --method-name "ConsultaDetalleSiniestro" --parameters "string,es-ES" --parameters "string,0010027100"
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from lcs import get_form_data, get_user_id, execute_asr, execute_script
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
    context = { }
    parameters = []
    for parameter in args.parameters:
        (type, value) = parameter[0].split(",")
        parameters.append((type, value))
    context['parameters'] = parameters
    if args.command == "get_user_id":
        response = get_user_id(args.username, args.password, context)
    elif args.command == "get_form_data" and args.form_name and args.record_id:
        context['form_name'] = args.form_name
        context['record_id'] = args.record_id
        response = get_form_data(args.username, args.password, context)
    elif args.command == "execute_asr" and args.asr_name and args.method_name:
        context['asr_name'] = args.asr_name
        context['method_name'] = args.method_name
        response = execute_asr(args.username, args.password, context)
    elif args.command == "execute_script" and args.asr_name and args.method_name:
        context['form_name'] = args.form_name
        context['method_name'] = args.method_name
        response = execute_script(args.username, args.password, context)
    else:
        logger.error("Invalid call.")
        return
    logger.info (response)
    return response


def parse_command_line():
    parser = ArgumentParser(prog='test_pivotal',
                            description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '--debug', action="store_true", help='Run the program in debug', required=False, default=False)
    parser.add_argument(
        '--username', help='The username to access the server', required=False, default=None)
    parser.add_argument(
        '--password', help='The password to access the server', required=False, default=None)
    parser.add_argument('--command', help="Select one command to execute", required=True, default="get_user_id", choices=['execute_asr', 'execute_script', 'get_form_data', 'get_user_id'], )
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
