#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit, L_lieferant, Gl_jouhdr, Bediener, Res_history

t_l_kredit_list, T_l_kredit = create_model_like(L_kredit)

def ap_edit_btn_ok_1bl(t_l_kredit_list:[T_l_kredit], recid_ap:int, orig_liefnr:int, lief_nr:int, firma:string, user_init:string):

    prepare_cache ([L_kredit, Gl_jouhdr, Bediener, Res_history])

    l_kredit = l_lieferant = gl_jouhdr = bediener = res_history = None

    t_l_kredit = supplier = subuff = None

    Supplier = create_buffer("Supplier",L_lieferant)
    Subuff = create_buffer("Subuff",L_lieferant)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit, l_lieferant, gl_jouhdr, bediener, res_history
        nonlocal recid_ap, orig_liefnr, lief_nr, firma, user_init
        nonlocal supplier, subuff


        nonlocal t_l_kredit, supplier, subuff

        return {}

    l_kredit = get_cache (L_kredit, {"_recid": [(eq, recid_ap)]})

    if l_kredit:

        subuff = db_session.query(Subuff).filter(
                 (Subuff.lief_nr == l_kredit.lief_nr)).first()

        if subuff:

            supplier = db_session.query(Supplier).filter(
                     (Supplier.lief_nr == lief_nr)).first()

            if supplier:

                t_l_kredit = query(t_l_kredit_list, first=True)

                if t_l_kredit:
                    pass
                    l_kredit.lief_nr = t_l_kredit.lief_nr
                    l_kredit.rabatt =  to_decimal(t_l_kredit.rabatt)
                    l_kredit.rabattbetrag =  to_decimal(t_l_kredit.rabattbetrag)
                    l_kredit.ziel = t_l_kredit.ziel
                    l_kredit.netto =  to_decimal(t_l_kredit.netto)
                    l_kredit.bediener_nr = t_l_kredit.bediener_nr
                    l_kredit.bemerk = t_l_kredit.bemerk

                    if orig_liefnr != lief_nr:

                        gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, l_kredit.name)]})

                        if gl_jouhdr:
                            pass
                            gl_jouhdr.bezeich = firma


                            pass
                            pass

                    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                    if bediener:
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = bediener.nr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.aenderung = "P/O " + l_kredit.name +\
                                "; DeliveryNote " + l_kredit.lscheinnr +\
                                "; Change Supplier " + subuff.firma +\
                                " -> " + supplier.firma


                        res_history.action = "A/P"
                        pass
                        pass

    return generate_output()