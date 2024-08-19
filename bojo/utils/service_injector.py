

from bojo.base_service import Service


def create_service(service_type: type[Service]):
    return service_type()