#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix definition variabel
            - fix python indentation
            - add type ignore to avoid warning 
            - activate model L_op & Fa_op
            - fix ap-journal.userinit EQ bediener.userinit to ap_journal.userinit = bediener.userinit       
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, Ap_journal, L_op, Queasy, L_lieferant, Fa_artikel, Fa_op, Bediener

output_list_data, Output_list = create_model(
    "Output_list", {
        "datum":date, 
        "rcv_amount":Decimal, 
        "ap_amount":Decimal, 
        "diff":Decimal, 
        "flag_diff_rcv":bool, 
        "flag_diff_ap":bool
        }
    )

def check_receiving_update_webbl(from_date:date, to_date:date, ref_no:string, id_user:string, output_list_data:[Output_list]):

    prepare_cache ([L_op, Queasy, Fa_op, Bediener])

    flag_up = False
    amt:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    t_amount:Decimal = to_decimal("0.0")
    ct:int = 0
    l_kredit = ap_journal = l_op = queasy = l_lieferant = fa_artikel = fa_op = bediener = None

    output_list = s_list = b_kredit = bl_kredit = buff_lkredit = buff_apjournal = None

    s_list_data, S_list = create_model(
        "S_list", {
            "datum":date, 
            "lief_nr":int, 
            "lager":int, 
            "docu_nr":string, 
            "lschein":string, 
            "userno":int, 
            "zeit":int, 
            "amount":Decimal, 
            "storno":string, 
            "loeschflag":int, 
            "artnr":int, 
            "inv_dept":bool
            }
        )

    B_kredit = create_buffer("B_kredit",L_kredit)
    Bl_kredit = create_buffer("Bl_kredit",L_kredit)
    Buff_lkredit = create_buffer("Buff_lkredit",L_kredit)
    Buff_apjournal = create_buffer("Buff_apjournal",Ap_journal)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_up, amt, amount, t_amount, ct, l_kredit, ap_journal, l_op, queasy, l_lieferant, fa_artikel, fa_op, bediener
        nonlocal from_date, to_date, ref_no, id_user
        nonlocal b_kredit, bl_kredit, buff_lkredit, buff_apjournal
        nonlocal output_list, s_list, b_kredit, bl_kredit, buff_lkredit, buff_apjournal
        nonlocal s_list_data

        return {
            "flag_up": flag_up
        }


    for l_op in db_session.query(L_op).filter(
             (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.op_art == 1) & (L_op.loeschflag <= 2)).order_by(L_op._recid).all():
        amount =  to_decimal("0")

        queasy = get_cache (Queasy, {
            "key": [(eq, 304)],
            "char1": [(eq, l_op.lscheinnr)],
            "number1": [(eq, l_op.artnr)]
            })

        if queasy:
            amount =  to_decimal(l_op.warenwert + l_op.warenwert * queasy.deci1 / 100)  

        else:
            amount =  to_decimal(l_op.warenwert)
        
        amount = to_decimal(round(amount , 2))  # type: ignore rounding hasil to_decimal

        s_list = query(s_list_data, filters=(lambda s_list: s_list.docu_nr == l_op.docu_nr and s_list.lschein == l_op.lscheinnr and s_list.loeschflag == l_op.loeschflag), first=True)

        if not s_list:
            s_list = S_list()
            s_list_data.append(s_list)

            s_list.datum = l_op.datum
            s_list.lief_nr = l_op.lief_nr
            s_list.docu_nr = l_op.docu_nr
            s_list.lschein = l_op.lscheinnr
            s_list.lager = l_op.lager_nr
            s_list.zeit = l_op.zeit
            s_list.userno = l_op.fuellflag
            s_list.storno = l_op.stornogrund
            s_list.loeschflag = l_op.loeschflag
            s_list.amount =  to_decimal(amount)
            s_list.inv_dept = True


        else:
            s_list.amount =  to_decimal(s_list.amount) + to_decimal(amount)

    fa_op_obj_list = {}
    for fa_op, l_lieferant, fa_artikel in db_session.query(Fa_op, L_lieferant, Fa_artikel).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).filter(
             (Fa_op.anzahl != 0) & (Fa_op.loeschflag < 2) & (Fa_op.opart == 1) & (Fa_op.datum >= from_date) & (Fa_op.datum <= to_date)).order_by(Fa_op.lscheinnr).all():
        if fa_op_obj_list.get(fa_op._recid):
            continue
        else:
            fa_op_obj_list[fa_op._recid] = True

        s_list = query(s_list_data, filters=(lambda s_list: s_list.docu_nr == fa_op.docu_nr and s_list.lschein == fa_op.lscheinnr), first=True)

        if not s_list:
            s_list = S_list()
            s_list_data.append(s_list)

            s_list.datum = fa_op.datum
            s_list.lief_nr = fa_op.lief_nr
            s_list.docu_nr = fa_op.docu_nr
            s_list.lschein = fa_op.lscheinnr
            s_list.zeit = fa_op.zeit
            s_list.userno = 00
            s_list.amount =  to_decimal(fa_op.warenwert)
            s_list.inv_dept = False


        else:
            s_list.amount =  to_decimal(s_list.amount) + to_decimal(fa_op.warenwert)

    for output_list in query(output_list_data, filters=(lambda output_list: output_list.datum >= from_date and output_list.datum <= to_date)):

        if output_list.flag_diff_ap or output_list.flag_diff_rcv:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.datum == output_list.datum), sort_by=[("loeschflag",True)]):

                if s_list.loeschflag == 2:

                    l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, s_list.lschein)]})

                    if l_kredit:

                        buff_lkredit = db_session.query(Buff_lkredit).filter(
                                 (Buff_lkredit._recid == l_kredit._recid)).with_for_update().first()
                        
                        db_session.delete(buff_lkredit)

                        ap_journal = get_cache (Ap_journal, {"lscheinnr": [(eq, s_list.lschein)],"lief_nr": [(eq, s_list.lief_nr)]})

                        if ap_journal:

                            buff_apjournal = db_session.query(Buff_apjournal).filter(
                                     (Buff_apjournal._recid == ap_journal._recid)).with_for_update().first()
                            
                            db_session.delete(buff_apjournal)
                            

                elif s_list.loeschflag == 0:

                    l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, s_list.lschein)],"lief_nr": [(eq, s_list.lief_nr)]})

                    if not l_kredit:
                        l_kredit = L_kredit()
                        db_session.add(l_kredit)

                        l_kredit.name = s_list.docu_nr
                        l_kredit.lief_nr = s_list.lief_nr
                        l_kredit.lscheinnr = s_list.lschein
                        l_kredit.rgdatum = s_list.datum
                        l_kredit.datum = None
                        l_kredit.ziel = 30
                        l_kredit.saldo =  to_decimal(s_list.amount)
                        l_kredit.netto =  to_decimal(s_list.amount)
                        l_kredit.bediener_nr = s_list.userNo

                        bediener = get_cache (Bediener, {"nr": [(eq, s_list.userno)]})
                        ap_journal = Ap_journal()
                        db_session.add(ap_journal)

                        ap_journal.docu_nr = s_list.docu_nr
                        ap_journal.lscheinnr = s_list.lschein
                        ap_journal.lief_nr = s_list.lief_nr
                        ap_journal.rgdatum = s_list.datum
                        ap_journal.zeit = s_list.zeit
                        ap_journal.saldo =  to_decimal(s_list.amount)
                        ap_journal.netto =  to_decimal(s_list.amount)

                        if bediener:
                            ap_journal.userinit = bediener.userinit
                    else:

                        for l_kredit in db_session.query(L_kredit).filter(
                                 (L_kredit.lscheinnr == s_list.lschein)).order_by(L_kredit._recid).all():

                            buff_lkredit = db_session.query(Buff_lkredit).filter(
                                     (Buff_lkredit._recid == l_kredit._recid)).with_for_update().first()
                            
                            db_session.delete(buff_lkredit)
                            
                        for ap_journal in db_session.query(Ap_journal).filter(
                                 (Ap_journal.lscheinnr == s_list.lschein)).order_by(Ap_journal._recid).all():

                            buff_apjournal = db_session.query(Buff_apjournal).filter(
                                     (Buff_apjournal._recid == ap_journal._recid)).with_for_update().first()
                            
                            db_session.delete(buff_apjournal)
                            
                        l_kredit = L_kredit()
                        db_session.add(l_kredit)

                        l_kredit.name = s_list.docu_nr
                        l_kredit.lief_nr = s_list.lief_nr
                        l_kredit.lscheinnr = s_list.lschein
                        l_kredit.rgdatum = s_list.datum
                        l_kredit.datum = None
                        l_kredit.ziel = 30
                        l_kredit.saldo =  to_decimal(s_list.amount)
                        l_kredit.netto =  to_decimal(s_list.amount)
                        l_kredit.bediener_nr = s_list.userNo

                        bediener = get_cache (Bediener, {"nr": [(eq, s_list.userno)]})
                        ap_journal = Ap_journal()
                        db_session.add(ap_journal)

                        ap_journal.docu_nr = s_list.docu_nr
                        ap_journal.lscheinnr = s_list.lschein
                        ap_journal.lief_nr = s_list.lief_nr
                        ap_journal.rgdatum = s_list.datum
                        ap_journal.zeit = s_list.zeit
                        ap_journal.saldo =  to_decimal(s_list.amount)
                        ap_journal.netto =  to_decimal(s_list.amount)

                        if bediener:
                            ap_journal.userinit = bediener.userinit
        flag_up = True

    return generate_output()