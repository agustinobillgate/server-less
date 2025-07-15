#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_artikel, Gl_acct, Mathis

def fa_upgrade_step_twobl(p_nr:int, amt:Decimal, user_init:string):

    prepare_cache ([Fa_artikel, Gl_acct, Mathis])

    debits = to_decimal("0.0")
    credits = to_decimal("0.0")
    avail_gl_acct = False
    avail_gl_acct1 = False
    name_mathis = ""
    curr_anz = 0
    remains = to_decimal("0.0")
    g_list_data = []
    s_list_data = []
    debit_betrag:Decimal = to_decimal("0.0")
    credit_betrag:Decimal = to_decimal("0.0")
    fa_artikel = gl_acct = mathis = None

    g_list = s_list = None

    g_list_data, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    s_list_data, S_list = create_model("S_list", {"fibukonto":string, "bezeich":string, "credit":Decimal, "debet":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, avail_gl_acct, avail_gl_acct1, name_mathis, curr_anz, remains, g_list_data, s_list_data, debit_betrag, credit_betrag, fa_artikel, gl_acct, mathis
        nonlocal p_nr, amt, user_init


        nonlocal g_list, s_list
        nonlocal g_list_data, s_list_data

        return {"debits": debits, "credits": credits, "avail_gl_acct": avail_gl_acct, "avail_gl_acct1": avail_gl_acct1, "name_mathis": name_mathis, "curr_anz": curr_anz, "remains": remains, "g-list": g_list_data, "s-list": s_list_data}

    def add_list(create_it:bool):

        nonlocal debits, credits, avail_gl_acct, avail_gl_acct1, name_mathis, curr_anz, remains, g_list_data, s_list_data, debit_betrag, credit_betrag, fa_artikel, gl_acct, mathis
        nonlocal p_nr, amt, user_init


        nonlocal g_list, s_list
        nonlocal g_list_data, s_list_data


        curr_anz = curr_anz + 1

        if create_it:
            g_list = G_list()
            g_list_data.append(g_list)

        g_list.nr = fa_artikel.nr
        g_list.fibukonto = gl_acct.fibukonto
        g_list.debit =  to_decimal(g_list.debit) + to_decimal(debit_betrag)
        g_list.credit =  to_decimal(g_list.credit) + to_decimal(credit_betrag)
        g_list.bemerk = mathis.asset + " - " + mathis.name
        g_list.userinit = user_init
        g_list.zeit = get_current_time_in_seconds()
        g_list.duplicate = False

        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto), first=True)

        if not s_list:
            s_list = S_list()
            s_list_data.append(s_list)

            s_list.fibukonto = gl_acct.fibukonto
            s_list.bezeich = gl_acct.bezeich


        s_list.credit =  to_decimal(s_list.credit) + to_decimal(credit_betrag)
        s_list.debet =  to_decimal(s_list.debet) + to_decimal(debit_betrag)
        credits =  to_decimal(credits) + to_decimal(credit_betrag)
        debits =  to_decimal(debits) + to_decimal(debit_betrag)
        remains =  to_decimal(debits) - to_decimal(credits)
        debit_betrag =  to_decimal("0")
        credit_betrag =  to_decimal("0")

    fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, p_nr)]})

    if fa_artikel:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})

        if gl_acct:
            avail_gl_acct1 = True
            debit_betrag =  to_decimal(amt)
            credit_betrag =  to_decimal("0")


            add_list(True)

        mathis = get_cache (Mathis, {"nr": [(eq, p_nr)]})

        if mathis:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_artikel.fibukonto)]})

            if gl_acct:
                avail_gl_acct = True
                credit_betrag =  to_decimal(amt)
                debit_betrag =  to_decimal("0")


                add_list(True)
            else:
                name_mathis = mathis.name

    return generate_output()