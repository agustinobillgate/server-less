#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pi

def print_gcpi_chg_statbl(docu_nr:string, flag:int):

    prepare_cache ([Gc_pi])

    gc_pi = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pi
        nonlocal docu_nr, flag

        return {}


    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})

    if gc_pi:
        pass

        if flag == 1:
            gc_pi.printed1 = True

        elif flag == 2:
            gc_pi.printed1a = True


        pass
        pass

    return generate_output()