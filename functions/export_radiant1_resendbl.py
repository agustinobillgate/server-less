#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Interface

def export_radiant1_resendbl(resnr:int):

    prepare_cache ([Res_line, Interface])

    counter = 0
    new_status:string = ""
    res_line = interface = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal counter, new_status, res_line, interface
        nonlocal resnr

        return {"counter": counter}

    counter = 0

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

        if res_line.resstatus <= 5:
            new_status = "new"

        if res_line.resstatus == 6 or res_line.resstatus == 8:
            new_status = "modify"

        if res_line.resstatus == 9 or res_line.resstatus == 99 or res_line.resstatus == 10:
            new_status = "cancel"


        DO
        interface = Interface()
        db_session.add(interface)

        interface.key = 10
        interface.zinr = res_line.zinr
        interface.nebenstelle = ""
        interface.intfield = 0
        interface.decfield =  to_decimal("1")
        interface.int_time = get_current_time_in_seconds()
        interface.intdate = get_current_date()
        interface.parameters = new_status
        interface.resnr = res_line.resnr
        interface.reslinnr = res_line.reslinnr
        counter = counter + 1


        pass
        pass

    return generate_output()