#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/11/2025, with_for_update, skip, temp-table
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, Ap_journal, Queasy, Bediener

in_list_data, In_list = create_model("In_list", {"lscheinr":string})
s_list_data, S_list = create_model("S_list", {"datum":date, "lief_nr":int, "lager":int, "docu_nr":string, "lscheinnr":string, "userno":int, "zeit":int, "amount":Decimal, "storno":string, "loeschflag":int, "artnr":int, "inv_dept":bool, "user_init":string})

def check_incoming_ap_webbl(in_list_data:[In_list], s_list_data:[S_list]):

    prepare_cache ([Queasy, Bediener])

    out_list_data = []
    amount:Decimal = to_decimal("0.0")
    ct:int = 0
    l_kredit = ap_journal = queasy = bediener = None

    in_list = s_list = rcv_list = out_list = b_kredit = buff_kredit = b_journal = None

    rcv_list_data, Rcv_list = create_model("Rcv_list", {"datum":date, "lief_nr":int, "lager":int, "docu_nr":string, "lscheinnr":string, "userno":int, "zeit":int, "amount":Decimal, "storno":string, "loeschflag":int, "artnr":int, "inv_dept":bool, "user_init":string})
    out_list_data, Out_list = create_model("Out_list", {"msg_str":string})

    B_kredit = create_buffer("B_kredit",L_kredit)
    Buff_kredit = create_buffer("Buff_kredit",L_kredit)
    B_journal = create_buffer("B_journal",Ap_journal)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_list_data, amount, ct, l_kredit, ap_journal, queasy, bediener
        nonlocal b_kredit, buff_kredit, b_journal


        nonlocal in_list, s_list, rcv_list, out_list, b_kredit, buff_kredit, b_journal
        nonlocal rcv_list_data, out_list_data

        return {"out-list": out_list_data}


    in_list = query(in_list_data, first=True)

    if in_list:

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.lscheinnr == in_list.lscheinr)):
            amount =  to_decimal("0")

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, s_list.lscheinnr)],"number1": [(eq, s_list.artnr)]})

            if queasy:
                amount =  to_decimal(s_list.amount) + (to_decimal(s_list.amount) * to_decimal((queasy.deci1) / to_decimal(100)) )


            else:
                amount =  to_decimal(s_list.amount)
            amount = to_decimal(round(amount , 2))

            rcv_list = query(rcv_list_data, filters=(lambda rcv_list: rcv_list.docu_nr == s_list.docu_nr and rcv_list.lschein == s_list.lscheinnr), first=True)

            if not rcv_list:
                rcv_list = Rcv_list()
                rcv_list_data.append(rcv_list)

                rcv_list.datum = s_list.datum
                rcv_list.lief_nr = s_list.lief_nr
                rcv_list.docu_nr = s_list.docu_nr
                rcv_list.lschein = s_list.lscheinnr
                rcv_list.lager = s_list.lager
                rcv_list.zeit = s_list.zeit
                rcv_list.userno = s_list.userNo
                rcv_list.storno = s_list.storno
                rcv_list.loeschflag = s_list.loeschflag
                rcv_list.user_init = s_list.user_init
                rcv_list.amount =  to_decimal(amount)
                rcv_list.inv_dept = True


            else:
                rcv_list.amount =  to_decimal(rcv_list.amount) + to_decimal(amount)

        rcv_list = query(rcv_list_data, first=True)

        if rcv_list:

            b_kredit = db_session.query(B_kredit).filter(
                     (B_kredit.lscheinnr == rcv_list.lschein) & (B_kredit.lief_nr == rcv_list.lief_nr)).first()

            if not b_kredit:
                b_kredit = L_kredit()
                db_session.add(b_kredit)

                b_kredit.name = rcv_list.docu_nr
                b_kredit.lief_nr = rcv_list.lief_nr
                b_kredit.lscheinnr = rcv_list.lscheinnr
                b_kredit.rgdatum = rcv_list.datum
                b_kredit.datum = None
                b_kredit.ziel = 30
                b_kredit.saldo =  to_decimal(rcv_list.amount)
                b_kredit.netto =  to_decimal(rcv_list.amount)


                b_journal = Ap_journal()
                db_session.add(b_journal)

                b_journal.docu_nr = rcv_list.docu_nr
                b_journal.lscheinnr = rcv_list.lscheinnr
                b_journal.lief_nr = rcv_list.lief_nr
                b_journal.rgdatum = rcv_list.datum
                b_journal.zeit = rcv_list.zeit
                b_journal.saldo =  to_decimal(rcv_list.amount)
                b_journal.netto =  to_decimal(rcv_list.amount)

                bediener = get_cache (Bediener, {"userinit": [(eq, rcv_list.user_init)]})

                if bediener:
                    b_kredit.bediener_nr = bediener.nr
                    b_journal.userinit = bediener.userinit


            else:

                for l_kredit in db_session.query(L_kredit).filter(
                         (L_kredit.lscheinnr == s_list.lschein)).order_by(L_kredit._recid).all():

                    b_kredit = db_session.query(B_kredit).filter(
                             (B_kredit._recid == l_kredit._recid)).with_for_update().first()
                    db_session.delete(b_kredit)
                    pass

                for ap_journal in db_session.query(Ap_journal).filter(
                         (Ap_journal.lscheinnr == s_list.lschein)).order_by(Ap_journal._recid).all():

                    b_journal = db_session.query(B_journal).filter(
                             (B_journal._recid == ap_journal._recid)).with_for_update().first()
                    db_session.delete(b_journal)
                    pass
                b_kredit = L_kredit()
                db_session.add(b_kredit)

                b_kredit.name = rcv_list.docu_nr
                b_kredit.lief_nr = rcv_list.lief_nr
                b_kredit.lscheinnr = rcv_list.lscheinnr
                b_kredit.rgdatum = rcv_list.datum
                b_kredit.datum = None
                b_kredit.ziel = 30
                b_kredit.saldo =  to_decimal(rcv_list.amount)
                b_kredit.netto =  to_decimal(rcv_list.amount)
                b_kredit.bediener_nr = rcv_list.userNo


                b_journal = Ap_journal()
                db_session.add(b_journal)

                b_journal.docu_nr = rcv_list.docu_nr
                b_journal.lscheinnr = rcv_list.lscheinnr
                b_journal.lief_nr = rcv_list.lief_nr
                b_journal.rgdatum = rcv_list.datum
                b_journal.zeit = rcv_list.zeit
                b_journal.saldo =  to_decimal(rcv_list.amount)
                b_journal.netto =  to_decimal(rcv_list.amount)

                bediener = get_cache (Bediener, {"userinit": [(eq, rcv_list.user_init)]})

                if bediener:
                    b_kredit.bediener_nr = bediener.nr
                    b_journal.userinit = bediener.userinit

    return generate_output()