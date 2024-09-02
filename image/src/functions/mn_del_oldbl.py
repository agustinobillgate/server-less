from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, H_compli, Queasy, Kontline, Res_line

def mn_del_oldbl(case_type:int):
    i = 0
    ci_date:date = None
    htparam = h_compli = queasy = kontline = res_line = None

    qbuff = kline = None

    Qbuff = Queasy
    Kline = Kontline

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, h_compli, queasy, kontline, res_line
        nonlocal qbuff, kline


        nonlocal qbuff, kline
        return {"i": i}

    def del_old_hcompli():

        nonlocal i, ci_date, htparam, h_compli, queasy, kontline, res_line
        nonlocal qbuff, kline


        nonlocal qbuff, kline

        anz:int = 0
        curr_date:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1083)).first()
        anz = htparam.finteger

        if anz <= 60:
            anz = 180
        curr_date = ci_date - anz

        h_compli = db_session.query(H_compli).filter(
                (H_compli.datum <= curr_date)).first()
        while None != h_compli:
            i = i + 1

            h_compli = db_session.query(H_compli).first()
            db_session.delete(h_compli)


            h_compli = db_session.query(H_compli).filter(
                    (H_compli.datum <= curr_date)).first()

    def del_old_workorder():

        nonlocal i, ci_date, htparam, h_compli, queasy, kontline, res_line
        nonlocal qbuff, kline


        nonlocal qbuff, kline


        Qbuff = Queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 28) &  (Queasy.number1 == 2) &  (Queasy.date1 < (ci_date - 60))).first()
        while None != queasy:

            qbuff = db_session.query(Qbuff).filter(
                        (Qbuff._recid == queasy._recid)).first()
            db_session.delete(qbuff)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 28) &  (Queasy.number1 == 2) &  (Queasy.date1 < (ci_date - 60))).first()

    def del_old_global_allotment():

        nonlocal i, ci_date, htparam, h_compli, queasy, kontline, res_line
        nonlocal qbuff, kline


        nonlocal qbuff, kline


        Kline = Kontline

        kontline = db_session.query(Kontline).filter(
                (Kontline.abreise < (ci_date - 1))).first()
        while None != kontline:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 147) &  (Queasy.number1 == kontline.gastnr) &  (Queasy.char1 == kontline.kontcode)).first()

            if queasy:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.active_flag == 1) &  (Res_line.kontignr == kontline.kontignr)).first()

                if not res_line:

                    kline = db_session.query(Kline).filter(
                            (Kline._recid == kontline._recid)).first()
                    db_session.delete(kline)


            kontline = db_session.query(Kontline).filter(
                    (Kontline.abreise < (ci_date - 1))).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if case_type == 1:
        del_old_hcompli()

    elif case_type == 2:
        del_old_workorder()

    elif case_type == 3:
        del_old_global_allotment()

    return generate_output()