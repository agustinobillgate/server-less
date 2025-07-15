from functions.additional_functions import *
import decimal

def vhpcommerce_connect():

    db_session = local_storage.db_session

    def generate_output():

        return {}

    CURRENT_WINDOW:LOAD_MOUSE_POINTER ("wait")

    if not CONNECTED ("vhp1"):
        CONNECT -db c:\vhp_db\commerce\vhp -1 -ld vhp1

        if not CONNECTED ("vhp1"):
            CONNECT -db \vhp_db\commerce\vhp -1 -ld vhp1
    CURRENT_WINDOW:LOAD_MOUSE_POINTER ("arrow")

    return generate_output()