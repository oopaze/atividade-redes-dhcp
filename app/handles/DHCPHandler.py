from os import environ as env
from typing import List

from app.handles.FileHandler import FileHandler
from app.handles.ParserHandle import AddressContract, ParserAddress
from app.utils.get_today_date import get_today_date

HOST_TEMPLATE = """
host {name} {{
    hardware ethernet    {mac};
    fixed-address        {ip};
}}
"""


class DHCPHandler:
    DHCP_FILEPATH = env.get("DHCP_FILEPATH", "fixtures/dhcpd.conf")
    RESERVAS_FILEPATH = env.get("RESERVAS_FILEPATH", "fixtures/RESERVAS.txt")

    def get_dhcp_conf(self, as_str: bool = True):
        file_handler = FileHandler(self.DHCP_FILEPATH)
        return file_handler.get_content(as_str=as_str)

    def get_reservas_conf(self):
        file_handler = ParserAddress(self.RESERVAS_FILEPATH)
        reservas = file_handler.parser()
        return reservas

    def get_hosts_from_reservas(self):
        content = ""

        for reserva in self.get_reservas_conf():
            content += self.tranform_reserva_into_host(reserva)

        return content

    def get_hosts_from_conf(self):
        content = self.get_dhcp_conf(as_str=False)
        formated_hosts = []

        for idx, line in enumerate(content):
            if line.strip().startswith("host"):
                host = content[idx : idx + 3]
                formated_hosts.append(self.format_host(host))

        return formated_hosts

    def format_host(self, host: List[str]) -> AddressContract:
        computer_name = host[0].split(" ")[1]
        mac_address = host[1].split("    ")[2].replace(";\n", "")
        ip_address = host[2].split("        ")[1].replace(";\n", "")

        return {
            "computer_name": computer_name,
            "mac_address": mac_address,
            "ip_address": ip_address,
        }

    def tranform_reserva_into_host(self, reserva: AddressContract):
        return HOST_TEMPLATE.format(
            name=reserva["computer_name"],
            mac=reserva["mac_address"],
            ip=reserva["ip_address"],
        )

    def create_dhcp_conf_file(self, content: str):
        requied_dhcp_handler = FileHandler('fixtures/required_dhcp.conf')
        required_dhcp_conf = requied_dhcp_handler.get_content(as_str=True)

        content = required_dhcp_conf + content

        moment = get_today_date()
        FileHandler.create_file(f"fixtures/dhcp.conf/dhcp-{moment}.conf", content)

    def create_backup_file(self):
        moment = get_today_date()
        content = self.get_dhcp_conf()
        filename = f"backup-{moment}.conf"

        FileHandler.create_file(
            filepath=f"fixtures/backups/{filename}", content=content
        )
