#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Interface

def i_intevent_1(var1, var2, var3, var4, var5, var6, var7, var8):

    prepare_cache ([Interface])

    interface = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal interface
        nonlocal var1, var2, var3, var4, var5, var6, var7, var8

        return {}

    interface = Interface()
    db_session.add(interface)

    interface.key = var1
    interface.zinr = var3
    interface.nebenstelle = var5
    interface.intfield = var6
    interface.decfield =  to_decimal(var2)
    interface.int_time = get_current_time_in_seconds()
    interface.intdate = get_current_date()
    interface.parameters = var4
    interface.resnr = var7
    interface.reslinnr = var8


    pass
    pass

    return generate_output()