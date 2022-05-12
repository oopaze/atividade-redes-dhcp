from app import OUTPUT_SUCCESS_TEMPLATE, RESERVAS_FILEPATH
from app.handles.DHCPHandler import DHCPHandler

from app.handles.FileHandler import FileHandler
from app.handles.ReservaCreator import ReservaCreator
from app.handles.CSVHandle import CSVHandle


def add_reserva():
    reservas_handler = ReservaCreator()
    dhcp_handler = DHCPHandler()

    reserva = reservas_handler.generate_reserva()

    reservas = dhcp_handler.get_reservas_from_dhcp_conf()
    reservas.append(reserva)

    reservas_as_str = CSVHandle.list_to_csv(reservas)

    FileHandler.create_file(RESERVAS_FILEPATH, reservas_as_str)

    hosts = dhcp_handler.generate_hosts_from_reservas()
    dhcp_handler.create_dhcp_conf_file(hosts)

    return OUTPUT_SUCCESS_TEMPLATE.format(content="Reserva Adicionada com sucesso")
