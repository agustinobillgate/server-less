from functions.additional_functions import *
import decimal

def vhpwork_connect():

    db_session = local_storage.db_session

    def generate_output():

        return {}

    CURRENT_WINDOW:LOAD_MOUSE_POINTER ("wait")

    if not CONNECTED ("vhp2"):
        CONNECT -db c:\vhp_db\work\vhp -1 -ld vhp2

        if not CONNECTED ("vhp2"):
            CONNECT -db \vhp_db\work\vhp -1 -ld vhp2
    CURRENT_WINDOW:LOAD_MOUSE_POINTER ("arrow")

    return generate_output()