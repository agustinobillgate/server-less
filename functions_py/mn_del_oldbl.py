#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
# timedelta
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from models import Htparam, H_compli, Queasy, Kontline, Res_line, L_quote, Guestbook

def mn_del_oldbl(case_type:int):

    prepare_cache ([Htparam])

    i = 0
    ci_date:date = None
    htparam = h_compli = queasy = kontline = res_line = l_quote = guestbook = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, h_compli, queasy, kontline, res_line, l_quote, guestbook
        nonlocal case_type

        return {"i": i}

    def del_old_hcompli():

        nonlocal i, ci_date, htparam, h_compli, queasy, kontline, res_line, l_quote, guestbook
        nonlocal case_type

        anz:int = 0
        curr_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1083)]})
        anz = htparam.finteger

        if anz <= 60:
            anz = 180
        curr_date = ci_date - timedelta(days=anz)

        # h_compli = get_cache (H_compli, {"datum": [(le, curr_date)]})
        # while None != h_compli:
        #     i = i + 1
        #     pass
        #     db_session.delete(h_compli)

        #     curr_recid = h_compli._recid
        #     h_compli = db_session.query(H_compli).filter(
        #              (H_compli.datum <= curr_date) & (H_compli._recid > curr_recid)).first()

        for h_compli in db_session.query(H_compli).filter(H_compli.datum <= curr_date).with_for_update().all():   
            i = i + 1
            db_session.delete(h_compli)


    def del_old_workorder():

        nonlocal i, ci_date, htparam, h_compli, queasy, kontline, res_line, l_quote, guestbook
        nonlocal case_type

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)

        # queasy = db_session.query(Queasy).filter(
        #          (Queasy.key == 28) & (Queasy.number1 == 2) & (Queasy.date1 < (ci_date - timedelta(days=60)))).order_by(Queasy._recid).first()
        # while None != queasy:

        #     qbuff = db_session.query(Qbuff).filter(
        #                  (Qbuff._recid == queasy._recid)).first()
        #     db_session.delete(qbuff)
        #     pass

        #     curr_recid = queasy._recid
        #     queasy = db_session.query(Queasy).filter(
        #              (Queasy.key == 28) & (Queasy.number1 == 2) & (Queasy.date1 < (ci_date - timedelta(days=60))) & (Queasy._recid > curr_recid)).first()

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 28) & (Queasy.number1 == 2) & (Queasy.date1 < (ci_date - timedelta(days=60)))).all():

            qbuff = db_session.query(Qbuff).filter(
                         (Qbuff._recid == queasy._recid)).with_for_update().first()
            
            db_session.delete(qbuff)
            i = i + 1


    def del_old_global_allotment():

        nonlocal i, ci_date, htparam, h_compli, queasy, kontline, res_line, l_quote, guestbook
        nonlocal case_type

        kline = None
        Kline =  create_buffer("Kline",Kontline)

        kontline = get_cache (Kontline, {"abreise": [(lt, ci_date - timedelta(days=1))]})
        while None != kontline:

            queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, kontline.gastnr)],"char1": [(eq, kontline.kontcode)]})

            if queasy:

                res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"kontignr": [(eq, kontline.kontignr)]})

                if not res_line:

                    kline = db_session.query(Kline).filter(
                             (Kline._recid == kontline._recid)).with_for_update().first()
                    
                    db_session.delete(kline)

            curr_recid = kontline._recid
            kontline = db_session.query(Kontline).filter(
                     (Kontline.abreise < (ci_date - timedelta(days=1))) & (Kontline._recid > curr_recid)).first()


    def del_old_quote_attach():

        nonlocal i, ci_date, htparam, h_compli, queasy, kontline, res_line, l_quote, guestbook
        nonlocal case_type

        anz:int = 0
        curr_date:date = None
        attach_num:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1083)]})

        if htparam and htparam.finteger != 0:
            anz = htparam.finteger

        if anz == 0:
            anz = 365
        curr_date = ci_date - timedelta(days=anz)

        l_quote = get_cache (L_quote, {"to_date": [(lt, curr_date)]})
        while None != l_quote:
            attach_num = to_int("-18" + to_string(l_quote._recid))

            guestbook = db_session.query(Guestbook).filter(
                         (Guestbook.gastnr == attach_num) & (Guestbook.reserve_int[0] == to_int(l_quote._recid))).first()

            if guestbook:
                db_session.refresh(guestbook, with_for_update=True)
                db_session.delete(guestbook)
                db_session.flush()

            curr_recid = l_quote._recid
            l_quote = db_session.query(L_quote).filter(
                     (L_quote.to_date < curr_date) & (L_quote._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if case_type == 1:
        del_old_hcompli()

    elif case_type == 2:
        del_old_workorder()

    elif case_type == 3:
        del_old_global_allotment()

    elif case_type == 4:
        del_old_quote_attach()

    return generate_output()