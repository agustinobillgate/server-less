from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Interface, Queasy, Res_line

def mn_del_interfacebl(case_type:int):
    ci_date:date = None
    htparam = interface = queasy = res_line = None

    interf = qsy = None

    Interf = Interface
    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, htparam, interface, queasy, res_line
        nonlocal interf, qsy


        nonlocal interf, qsy
        return {}

    def del_interface():

        nonlocal ci_date, htparam, interface, queasy, res_line
        nonlocal interf, qsy


        nonlocal interf, qsy


        Interf = Interface
        Qsy = Queasy

        interface = db_session.query(Interface).filter(
                (Interface.key >= 0) &  (Interface.intdate <= (ci_date - 2)) &  (Interface.int_time >= 0)).first()
        while None != interface:

            interf = db_session.query(Interf).filter(
                        (Interf._recid == interface._recid)).first()
            db_session.delete(interf)

            interface = db_session.query(Interface).filter(
                    (Interface.key >= 0) &  (Interface.intdate <= (ci_date - 2)) &  (Interface.int_time >= 0)).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 35) &  (Queasy.date1 <= (ci_date - 2))).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 35) &  (Queasy.date1 <= (ci_date - 2))).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 30) &  (Queasy.betriebsnr == 1) &  (Queasy.date1 <= (ci_date - 2))).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 30) &  (Queasy.betriebsnr == 1) &  (Queasy.date1 <= (ci_date - 2))).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 30) &  (Queasy.betriebsnr == 2) &  (Queasy.date1 <= (ci_date - 2))).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 30) &  (Queasy.betriebsnr == 2) &  (Queasy.date1 <= (ci_date - 2))).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 37) &  (Queasy.betriebsnr == 1) &  (Queasy.date1 <= (ci_date - 2))).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 37) &  (Queasy.betriebsnr == 1) &  (Queasy.date1 <= (ci_date - 2))).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 37) &  (Queasy.betriebsnr == 2) &  (Queasy.date1 <= (ci_date - 2))).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 37) &  (Queasy.betriebsnr == 2) &  (Queasy.date1 <= (ci_date - 2))).first()

    def crm_checkout():

        nonlocal ci_date, htparam, interface, queasy, res_line
        nonlocal interf, qsy


        nonlocal interf, qsy

        bill_date:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resstatus == 8) &  (Res_line.abreise == bill_date) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.erwachs > 0)).all():
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
            interface.parameters = "CRM check_out"

            interface = db_session.query(Interface).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if case_type == 1:
        del_interface()
    else:
        crm_checkout()

    return generate_output()