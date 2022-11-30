from jinja2 import FileSystemLoader, Environment
from os.path import dirname
import requests
import xml.etree.ElementTree as ET

SERVICE_URL = "http://SES000A204221/Pivotal/Services/PivotalServices.aspx"
LCS_SERVER = "SES000A204221"
SYSTEM_NAME = "Mapfre"

def render_template(template_name, args):
    env = Environment(loader=FileSystemLoader(dirname(__file__)))
    template = env.get_template(template_name)
    return template.render(args)

def send_command(username, password, xml_command):
    url = "{SERVICE_URL}?server={LCS_SERVER}".format(**globals())
    headers = {
        'useraAgent': 'Mozilla/4.0',
        'content-type': 'text/xml; charset=utf-8',
        'content-length': str(len(xml_command))
    }
    return requests.post(url, data=xml_command, headers=headers, auth=(username, password))

def parse_response (name:str, response:str):
    xml = ET.fromstring(response)
    for element in xml.iter():
        for child in element:
            print (child.tag, child.text)
    return {
        "name": name,
        "fields": xml
    }

def get_form_data(username, password, form_name: str, record_id: str):
    args = {
        'system_name': SYSTEM_NAME,
        'form_name': form_name,
        'record_id': record_id
    }
    xml_command = render_template('get_form_data.jinja2.xml', args)
    response = send_command(username, password, xml_command)
    return parse_response(form_name, response.text)

def execute_asr(username, password, asr_name: str, method_name: str):
    args = {
        'system_name': SYSTEM_NAME,
        'asr_name': asr_name,
        'method_name': method_name,
        'parameters': []
    }
    xml_command = render_template('execute_asr.jinja2.xml', args)
    response = send_command(username, password, xml_command)
    return parse_response(asr_name, response.text)

def execute_script(username, password, form_name: str, method_name: str):
    args = {
        'system_name': SYSTEM_NAME,
        'form_name': form_name,
        'method_name': method_name,
        'parameters': []
    }
    xml_command = render_template('execute_script.jinja2.xml', args)
    response = send_command(username, password, xml_command)
    return parse_response(form_name, response.text)
