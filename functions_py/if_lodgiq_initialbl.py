# using conversion tools version: 1.0.0.119
"""_yusufwijasena_13/11/2025

    Ticket ID: 62BADE
        _remark_:   - fix python indentation
                    - only convert to py
"""

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Interface, Genstat, Res_line


def if_lodgiq_initialbl():

    prepare_cache([Htparam, Genstat, Res_line])

    datum: date = None
    new_status = ""
    p_87: date = None
    fdate: date = None
    tdate: date = None
    res_initial = False
    htparam = interface = genstat = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum, new_status, p_87, fdate, tdate, res_initial, htparam, interface, genstat, res_line

        return {
            "res_initial": res_initial
        }

    def process_data_old(from_old: date, to_old: date):
        nonlocal datum, new_status, p_87, fdate, tdate, res_initial, htparam, interface, genstat, res_line

        for datum in date_range(from_old, to_old):
            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum >= datum) & 
                    (Genstat.datum <= datum) & 
                    (Genstat.resstatus != 11) & 
                    (Genstat.resstatus != 12) & 
                    (Genstat.resstatus != 13) & 
                    (Genstat.resnr != 0)).order_by(Genstat.resnr).all():
                interface = Interface()
                db_session.add(interface)

                interface.key = 10
                interface.zinr = genstat.zinr
                interface.nebenstelle = ""
                interface.intfield = 0
                interface.decfield = to_decimal("1")
                interface.int_time = get_current_time_in_seconds()
                interface.intdate = get_current_date()
                interface.parameters = "modify|init"
                interface.resnr = genstat.resnr
                interface.reslinnr = genstat.res_int[0]

    def process_forecast_data(from_fc: date, to_fc: date):
        nonlocal datum, new_status, p_87, fdate, tdate, res_initial, htparam, interface, genstat, res_line

        for datum in date_range(from_fc, to_fc):
            for res_line in db_session.query(Res_line).filter(
                    (Res_line.active_flag <= 1) & 
                    (Res_line.resstatus <= 13) & 
                    (Res_line.resstatus != 4) & 
                    (Res_line.resstatus != 11) & 
                    (Res_line.resstatus != 13) & 
                    (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & 
                    (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                if res_line.resstatus <= 5:
                    new_status = "new|init"

                elif res_line.resstatus == 6 or res_line.resstatus == 8:
                    new_status = "modify|init"

                elif res_line.resstatus == 9 or res_line.resstatus == 99 or res_line.resstatus == 10:
                    new_status = "cancel|init"

                interface = Interface()
                db_session.add(interface)

                interface.key = 10
                interface.zinr = res_line.zinr
                interface.nebenstelle = ""
                interface.intfield = 0
                interface.decfield = to_decimal("1")
                interface.int_time = get_current_time_in_seconds()
                interface.intdate = get_current_date()
                interface.parameters = new_status
                interface.resnr = res_line.resnr
                interface.reslinnr = res_line.reslinnr


    htparam = get_cache(Htparam, {"paramnr": [(eq, 87)]})
    p_87 = htparam.fdate

    for interface in db_session.query(Interface).filter(
            (Interface.key == 10) & 
            (matches((Interface.parameters, "*new|init*")) | (matches(Interface.parameters, "*modify|init*")) | (matches(Interface.parameters, "*cancel|init*")))).order_by(Interface._recid).with_for_update().all():
        db_session.delete(interface)
    fdate = p_87 - timedelta(days=365)
    tdate = p_87 + timedelta(days=365)

    if fdate < p_87 and tdate < p_87:
        process_data_old(fdate, tdate)
        res_initial = True

    elif fdate <= p_87 and tdate >= p_87:
        process_data_old(fdate, p_87 - 1)
        process_forecast_data(p_87, tdate)
        res_initial = True

    else:
        process_forecast_data(fdate, tdate)
        res_initial = True

    return generate_output()
