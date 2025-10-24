# using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix definition variabel
            - fix python indentation
            - add type ignore to avoid warning 
            - import session from sqlalchemy.orm
            - activate model Gl_jouhdr, Fa_op, L_op
            - moved Quesy() to global
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import session
from models import L_kredit, Gl_jouhdr, L_artikel, L_lieferant, L_op, Queasy, Fa_artikel, Fa_op, Gl_journal, L_ophdr, Gl_acct, Gl_department


def check_journal_webbl(from_date: date, to_date: date, ref_no: string, case_type: int, id_user: string):

    prepare_cache([Gl_jouhdr, L_op, Queasy, Fa_op, Gl_journal])

    tot_debit = to_decimal("0.0")
    tot_credit = to_decimal("0.0")
    flag_up = False
    flag_case = 0
    output_list_data = []
    curr_pay = to_decimal("0.0")
    d: date
    mon: int = 0
    art1: int = 0
    art2: int = 0
    fibu: string 
    credit = to_decimal("0.0")
    ct: int = 0
    tot_vat = to_decimal("0.0")
    do_it: bool = False
    l_kredit = l_artikel = l_lieferant = fa_artikel = gl_journal = l_ophdr = gl_acct = gl_department = None
    gl_jouhdr = Gl_jouhdr()
    fa_op = Fa_op()
    l_op = L_op()
    queasy = Queasy()

    output_list = l_ap = bgl_jouhdr = None

    output_list_data, Output_list = create_model(
        "Output_list", {
            "datum": date,
            "refno": string,
            "amount": Decimal,
            "gl_amount": Decimal,
            "diff": Decimal,
            "flag_diff": bool,
            "flag_diff_gl": bool,
            "flag_detail": bool,
            "gl_bezeich": string
        }
    )

    L_ap = create_buffer("L_ap", L_kredit)
    Bgl_jouhdr = create_buffer("Bgl_jouhdr", Gl_jouhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_debit, tot_credit, flag_up, flag_case, output_list_data, curr_pay, d, mon, art1, art2, fibu, credit, ct, tot_vat, do_it, gl_amount, l_kredit, gl_jouhdr, l_artikel, l_lieferant, l_op, queasy, fa_artikel, fa_op, gl_journal, l_ophdr, gl_acct, gl_department
        nonlocal from_date, to_date, ref_no, case_type, id_user
        nonlocal l_ap, bgl_jouhdr

        nonlocal output_list, l_ap, bgl_jouhdr
        nonlocal output_list_data

        return {
            "tot_debit": tot_debit, 
            "tot_credit": tot_credit, 
            "flag_up": flag_up, 
            "flag_case": flag_case, 
            "output-list": output_list_data
        }

    if case_type == 1:
        for d in date_range(from_date, to_date):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.datum = d  

            l_op_obj_list = {}
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel, (L_artikel.artnr == L_op.artnr)).join(L_lieferant, (L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.artnr >= 1000000) & (L_op.artnr <= 9999999) & (L_op.lief_nr > 0) & (L_op.datum == d) & (L_op.op_art <= 2) & (L_op.loeschflag <= 1)).order_by(L_lieferant.firma, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                queasy = get_cache(Queasy, {
                    "key": [(eq, 304)], 
                    "char1": [(eq, l_op.lscheinnr)], 
                    "number1": [(eq, l_op.artnr)]})

                if queasy:
                    tot_vat = to_decimal(l_op.warenwert + l_op.warenwert * queasy.deci1 / 100)

                else:
                    tot_vat = to_decimal(l_op.warenwert)

                    tot_vat = to_decimal(round(tot_vat, 2))  # type: ignore rounding hasil cast to_decimal
                    
                    output_list.amount = to_decimal(output_list.amount + tot_vat)  # type: ignore output list amount

                fa_op_obj_list = {}
                for fa_op, l_lieferant, fa_artikel in db_session.query(Fa_op, L_lieferant, Fa_artikel).join(L_lieferant, (L_lieferant.lief_nr == Fa_op.lief_nr)).join(Fa_artikel, (Fa_artikel.nr == Fa_op.nr)).filter(
                        (Fa_op.anzahl != 0) & (Fa_op.loeschflag < 2) & (Fa_op.opart == 1) & (Fa_op.datum == d)).order_by(Fa_op.lscheinnr).all():
                    if fa_op_obj_list.get(fa_op._recid):
                        continue
                    else:
                        fa_op_obj_list[fa_op._recid] = True

                        output_list = query(output_list_data, filters=(
                            lambda output_list: output_list.datum == fa_op.datum), first=True) 

                        if output_list:
                            output_list.amount = to_decimal(output_list.amount + fa_op.warenwert) 

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter((Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_jouhdr.jtyp == 6)).order_by(Gl_jouhdr._recid).all():
            gl_amount = None

            for gl_journal in db_session.query(Gl_journal).filter((Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                
                gl_amount = to_decimal(gl_amount + gl_journal.credit) 

            output_list = query(output_list_data, filters=(
                lambda output_list: output_list.datum == gl_jouhdr.datum), first=True)

            if output_list:
                
                output_list.gl_amount = to_decimal(gl_amount) 
                
                output_list.refno = gl_jouhdr.refno 

        
        for output_list in query(output_list_data): # type: ignore object output_list_data

            if output_list.amount > output_list.gl_amount:
                output_list.flag_diff_gl = True

            if output_list.amount < output_list.gl_amount:
                output_list.flag_diff = True
                
                output_list.diff = to_decimal(output_list.amount - output_list.gl_amount) 

            if int(str(output_list.diff)) != 0:  
                flag_up = True

    if case_type == 2:
        for d in date_range(from_date, to_date):
            do_it = True
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.datum = d 

            l_op_obj_list = {}
            for l_op, l_ophdr, gl_acct, gl_department, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, Gl_department, L_artikel).join(L_ophdr, (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.fibukonto != "")).join(Gl_acct, (Gl_acct.fibukonto == L_op.stornogrund)).join(Gl_department, (Gl_department.nr == Gl_acct.deptnr)).join(L_artikel, (L_artikel.artnr == L_op.artnr)).filter((L_op.datum == d) & (L_op.anzahl != 0) & (L_op.op_art == 3) & (L_op.loeschflag <= 1)).order_by(L_op.lscheinnr, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                tot_vat = to_decimal("0")

                tot_vat = to_decimal(l_op.warenwert)
                
                tot_vat = to_decimal(round(tot_vat, 2)) # type: ignore rounding hasil cast to_decimal
                
                output_list.amount = to_decimal(output_list.amount + tot_vat) # type: ignore output list amount

                queasy = get_cache(Queasy, {
                    "key": [(eq, 333)],
                    "char3": [(eq, "outgoing jurnal")],
                    "date1": [(eq, d)]
                }
                )

                if queasy:
                    credit = to_decimal("0")
                    gl_jouhdr = get_cache(
                        Gl_jouhdr, {
                            "refno": [(eq, queasy.char1)],
                            "datum": [(eq, queasy.date1)]})

                    if gl_jouhdr:
                        for gl_journal in db_session.query(Gl_journal).filter((Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                            
                            credit = to_decimal(credit + gl_journal.credit)
                            
                            output_list = query(output_list_data, filters=(
                                lambda output_list: output_list.datum == queasy.date1), first=True) 

                            if output_list:
                                
                                output_list.gl_amount = to_decimal(round(credit, 0)) # type: ignore rounding hadil cast to_decimal
                                output_list.refno = queasy.char1                                  
                                output_list.gl_bezeich = queasy.char2 

                    do_it = False
                else:
                    bgl_jouhdr = db_session.query(Bgl_jouhdr).filter((Bgl_jouhdr.datum == d) & (
                        matches(Bgl_jouhdr.refno, "OUT*")) & (Bgl_jouhdr.jnr != 0)).first()

                    if bgl_jouhdr:
                        credit = to_decimal("0")

                        for gl_journal in db_session.query(Gl_journal).filter((Gl_journal.jnr == bgl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                            
                            credit = to_decimal(credit + gl_journal.credit) 

                            output_list = query(output_list_data, filters=(
                                lambda output_list: output_list.datum == bgl_jouhdr.datum), first=True)   # type: ignore bgl_jauhdr.datum
                            if output_list:
                                
                                output_list.gl_amount = to_decimal(round(credit, 0)) # type: ignore rounding output cast to_decimal
                                output_list.refno = bgl_jouhdr.refno                                 
                                output_list.gl_bezeich = bgl_jouhdr.bezeich 

                    do_it = False

                if do_it:
                    for gl_jouhdr in db_session.query(Gl_jouhdr).filter((Gl_jouhdr.datum == d) & (Gl_jouhdr.jtyp == 3)).order_by(Gl_jouhdr._recid).all():
                        credit = to_decimal("0")

                        for gl_journal in db_session.query(Gl_journal).filter((Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                            credit = to_decimal(credit) + to_decimal(gl_journal.credit)

                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.datum = gl_jouhdr.datum
                        output_list.gl_amount = to_decimal(round(credit, 0))
                        output_list.refno = gl_jouhdr.refno
                        output_list.gl_bezeich = gl_jouhdr.bezeich
                        output_list.flag_detail = True

            
            for output_list in query(output_list_data): # type: ignore output list data
                output_list.amount = to_decimal(round(output_list.amount, 0))

                if output_list.amount > output_list.gl_amount:
                    output_list.flag_diff_gl = True

                if output_list.amount < output_list.gl_amount:
                    output_list.flag_diff = True

                
                output_list.diff = to_decimal(output_list.amount - output_list.gl_amount)   

                if int(str(output_list.diff)) != 0: 
                    flag_up = True

        if not flag_up:

            queasy = get_cache(Queasy, {
                "key": [(eq, 331)],
                "char1": [(eq, id_user)],
                "char2": [(eq, "inv-cek journal")]})

            if not queasy:
                queasy.key = 331
                queasy.char1 = id_user
                queasy.char2 = "Inv-Cek Journal"
                queasy.char3 = "yes"

                db_session.add(queasy)
                return generate_output()
