import gvm
from gvm.protocols.latest import Gmp
from lxml import etree
import base64
import io


class Scan:

    def __init__(self, username, password):
        self.gmp = self.establish_connection(username, password)

    def establish_connection(self, username, password):
        connection = gvm.connections.TLSConnection(hostname="localhost", port=9390)
        gmp = Gmp(connection=connection)
        gmp.authenticate(username=username, password=password)

        return gmp

    def print_version(self):
        print(self.gmp.get_version())

    def create_task(self, name, target_id):
        response = self.gmp.create_task(name=name, config_id='daba56c8-73ec-11df-a475-002264764cea',
                                        target_id=target_id, scanner_id='08b69003-5fc2-4037-a479-93b440211c73')
        root = etree.fromstring(response)
        task_id = root.attrib.get("id")
        return task_id

    def create_target(self, name, hosts_list):
        response = self.gmp.create_target(name=name, hosts=hosts_list,
                                          port_list_id="33d0cd82-57c6-11e1-8ed1-406186ea4fc5")
        root = etree.fromstring(response)
        target_id = root.attrib.get("id")
        return target_id

    def get_task_id(self, task_name):
        response = self.gmp.get_tasks(filter_string=task_name)

        root = etree.fromstring(response)
        task_element = root.find('.//task')
        task_id = task_element.get('id')

        return task_id

    def start_task(self, task_id):
        task_response = self.gmp.start_task(task_id)
        return task_response

    def find_report_id_from_task_response(self, task_response):
        root = etree.fromstring(task_response)
        report_id = root.find('report_id').text
        return report_id

    def is_task_finished(self, report_id):
        report = self.gmp.get_report(report_id)
        first_index = report.index('<scan_run_status>')
        last_index = report.index('</scan_run_status>')
        status = report[first_index + len('<scan_run_status>'): last_index]
        print("Status of task: " + status)
        if status == "Done":
            return True
        else:
            return False

    def save_report_to_pdf(self, report_id, report_file_name):
        report = self.gmp.get_report(report_id, report_format_id='c402cc3e-b531-11e1-9163-406186ea4fc5')

        start_index = report.index('</report_format>')
        last_index = report.index('</report>')

        encoded_report_pdf = report[start_index + len('</report_format>'): last_index]

        decoded_bytes = base64.b64decode(encoded_report_pdf)

        with open(report_file_name, 'wb') as f:
            f.write(decoded_bytes)
