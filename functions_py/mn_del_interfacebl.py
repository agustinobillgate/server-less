#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
# timedelta
#------------------------------------------

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from models import Htparam, Interface, Queasy, Res_line

def mn_del_interfacebl(case_type:int):

    prepare_cache ([Htparam, Res_line])

    ci_date:date = None
    htparam = interface = queasy = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, htparam, interface, queasy, res_line
        nonlocal case_type

        return {}

    def del_interface():

        nonlocal ci_date, htparam, interface, queasy, res_line
        nonlocal case_type

        interf = None
        qsy = None
        Interf =  create_buffer("Interf",Interface)
        Qsy =  create_buffer("Qsy",Queasy)

        # interface = get_cache (Interface, {"key": [(ge, 0)],"intdate": [(le, (ci_date - 2))],"int_time": [(ge, 0)]})
        interface = db_session.query(Interface).filter(
                 (Interface.key >= 0) & (Interface.intdate <= (ci_date - timedelta(days=2))) & (Interface.int_time >= 0)).order_by(Interface._recid).first()
        while None != interface:

            interf = db_session.query(Interf).filter(
                         (Interf._recid == interface._recid)).with_for_update().first()
            db_session.delete(interf)
            pass

            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                     (Interface.key >= 0) & (Interface.intdate <= (ci_date - timedelta(days=2))) & (Interface.int_time >= 0) & (Interface._recid > curr_recid)).first()

        # queasy = get_cache (Queasy, {"key": [(eq, 35)],"date1": [(le, (ci_date - 2))]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 35) & (Queasy.date1 <= (ci_date - timedelta(days=2)))).order_by(Queasy._recid).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                         (Qsy._recid == queasy._recid)).with_for_update().first()
            db_session.delete(qsy)
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 35) & (Queasy.date1 <= (ci_date - timedelta(days=2))) & (Queasy._recid > curr_recid)).first()

        # queasy = get_cache (Queasy, {"key": [(eq, 30)],"betriebsnr": [(eq, 1)],"date1": [(le, (ci_date - 2))]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 30) & (Queasy.betriebsnr == 1) & (Queasy.date1 <= (ci_date - timedelta(days=2)))).order_by(Queasy._recid).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                         (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 30) & (Queasy.betriebsnr == 1) & (Queasy.date1 <= (ci_date - timedelta(days=2))) & (Queasy._recid > curr_recid)).first()

        # queasy = get_cache (Queasy, {"key": [(eq, 30)],"betriebsnr": [(eq, 2)],"date1": [(le, (ci_date - 2))]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 30) & (Queasy.betriebsnr == 2) & (Queasy.date1 <= (ci_date - timedelta(days=2)))).order_by(Queasy._recid).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                         (Qsy._recid == queasy._recid)).with_for_update().first()
            db_session.delete(qsy)
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 30) & (Queasy.betriebsnr == 2) & (Queasy.date1 <= (ci_date - timedelta(days=2))) & (Queasy._recid > curr_recid)).first()

        # queasy = get_cache (Queasy, {"key": [(eq, 37)],"betriebsnr": [(eq, 1)],"date1": [(le, (ci_date - 2))]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 37) & (Queasy.betriebsnr == 1) & (Queasy.date1 <= (ci_date - timedelta(days=2)))).order_by(Queasy._recid).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                         (Qsy._recid == queasy._recid)).with_for_update().first()
            db_session.delete(qsy)
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 37) & (Queasy.betriebsnr == 1) & (Queasy.date1 <= (ci_date - timedelta(days=2))) & (Queasy._recid > curr_recid)).first()

        # queasy = get_cache (Queasy, {"key": [(eq, 37)],"betriebsnr": [(eq, 2)],"date1": [(le, (ci_date - 2))]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 37) & (Queasy.betriebsnr == 2) & (Queasy.date1 <= (ci_date - timedelta(days=2)))).order_by(Queasy._recid).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                         (Qsy._recid == queasy._recid)).with_for_update().first()
            db_session.delete(qsy)
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 37) & (Queasy.betriebsnr == 2) & (Queasy.date1 <= (ci_date - timedelta(days=2))) & (Queasy._recid > curr_recid)).first()


    def crm_checkout():

        nonlocal ci_date, htparam, interface, queasy, res_line
        nonlocal case_type

        bill_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 8) & (Res_line.abreise == bill_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.erwachs > 0)).order_by(Res_line._recid).all():
            interface = Interface()
            db_session.add(interface)

            interface.key = 5
            interface.zinr = res_line.zinr
            interface.nebenstelle = res_line.zinr
            interface.resnr = res_line.resnr
            interface.reslinnr = res_line.reslinnr
            interface.intfield = 0
            interface.int_time = get_current_time_in_seconds()
            interface.intdate = get_current_date()
            interface.parameters = "CRM check-out"


            pass
            pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if case_type == 1:
        del_interface()
    else:
        crm_checkout()

    return generate_output()