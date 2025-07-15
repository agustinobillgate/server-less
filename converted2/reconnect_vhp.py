from functions.additional_functions import *
import decimal

def reconnect_vhp():

    db_session = local_storage.db_session

    def generate_output():

        return {}

    CONNECT -pf VALUE ("-db vhp -N tcp -S 2600/tcp -H toshiba")

    return generate_output()