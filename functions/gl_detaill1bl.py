#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Gl_journal, Gl_jourhis, Gl_jhdrhis

def gl_detaill1bl(fibu:string, from_date:date, to_date:date):

    prepare_cache ([Gl_jouhdr, Gl_journal, Gl_jourhis, Gl_jhdrhis])

    b1_list_data = []
    t_gl_acct_data = []
    t_from_date:date = None
    t_to_date:date = None
    from_datehis:date = None
    to_datehis:date = None
    t_date:date = None
    tmp_lastday:date = None
    gl_acct = gl_jouhdr = gl_journal = gl_jourhis = gl_jhdrhis = None

    b1_list = t_gl_acct = None

    b1_list_data, B1_list = create_model("B1_list", {"jnr":int, "datum":date, "refno":string, "bezeich":string, "debit":Decimal, "credit":Decimal, "userinit":string, "bemerk":string, "jtype":int, "fibukonto":string})
    t_gl_acct_data, T_gl_acct = create_model_like(Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_data, t_gl_acct_data, t_from_date, t_to_date, from_datehis, to_datehis, t_date, tmp_lastday, gl_acct, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis
        nonlocal fibu, from_date, to_date


        nonlocal b1_list, t_gl_acct
        nonlocal b1_list_data, t_gl_acct_data

        return {"b1-list": b1_list_data, "t-gl-acct": t_gl_acct_data}

    def lastday(d:date):

        nonlocal b1_list_data, t_gl_acct_data, t_from_date, t_to_date, from_datehis, to_datehis, t_date, tmp_lastday, gl_acct, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis
        nonlocal fibu, from_date, to_date


        nonlocal b1_list, t_gl_acct
        nonlocal b1_list_data, t_gl_acct_data

        tmp_date:date = None
        tot_date:date = None
        tmp_date = add_interval(date_mdy(get_month(d) , 1, get_year(d)) , 1, "month")
        tot_date = tmp_date - timedelta(days=1)
        return tot_date


    def disp_it():

        nonlocal b1_list_data, t_gl_acct_data, t_from_date, t_to_date, from_datehis, to_datehis, t_date, tmp_lastday, gl_acct, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis
        nonlocal fibu, from_date, to_date


        nonlocal b1_list, t_gl_acct
        nonlocal b1_list_data, t_gl_acct_data

        gl_jouhdr = Gl_jouhdr()
        gl_journal = Gl_journal()
        for gl_jouhdr.jnr, gl_jouhdr.datum, gl_jouhdr.refno, gl_jouhdr.bezeich, gl_jouhdr.jtype, gl_jouhdr._recid, gl_journal.debit, gl_journal.credit, gl_journal.userinit, gl_journal.bemerk, gl_journal.fibukonto, gl_journal._recid in db_session.query(Gl_jouhdr.jnr, Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich, Gl_jouhdr.jtype, Gl_jouhdr._recid, Gl_journal.debit, Gl_journal.credit, Gl_journal.userinit, Gl_journal.bemerk, Gl_journal.fibukonto, Gl_journal._recid).join(Gl_journal,(Gl_journal.jnr == Gl_jouhdr.jnr) & (Gl_journal.fibukonto == (fibu).lower())).filter(
                 (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum).all():
            b1_list = B1_list()
            b1_list_data.append(b1_list)

            b1_list.jnr = gl_jouhdr.jnr
            b1_list.datum = gl_jouhdr.datum
            b1_list.refno = gl_jouhdr.refno
            b1_list.bezeich = gl_jouhdr.bezeich
            b1_list.debit =  to_decimal(gl_journal.debit)
            b1_list.credit =  to_decimal(gl_journal.credit)
            b1_list.userinit = gl_journal.userinit
            b1_list.bemerk = gl_journal.bemerk
            b1_list.jtype = gl_jouhdr.jtype
            b1_list.fibukonto = gl_journal.fibukonto


    def disp_it_his():

        nonlocal b1_list_data, t_gl_acct_data, t_from_date, t_to_date, from_datehis, to_datehis, t_date, tmp_lastday, gl_acct, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis
        nonlocal fibu, from_date, to_date


        nonlocal b1_list, t_gl_acct
        nonlocal b1_list_data, t_gl_acct_data

        gl_jhdrhis = Gl_jhdrhis()
        gl_jourhis = Gl_jourhis()
        for gl_jhdrhis.jnr, gl_jhdrhis.datum, gl_jhdrhis.refno, gl_jhdrhis.bezeich, gl_jhdrhis.jtype, gl_jhdrhis._recid, gl_jourhis.debit, gl_jourhis.credit, gl_jourhis.userinit, gl_jourhis.bemerk, gl_jourhis.fibukonto, gl_jourhis._recid in db_session.query(Gl_jhdrhis.jnr, Gl_jhdrhis.datum, Gl_jhdrhis.refno, Gl_jhdrhis.bezeich, Gl_jhdrhis.jtype, Gl_jhdrhis._recid, Gl_jourhis.debit, Gl_jourhis.credit, Gl_jourhis.userinit, Gl_jourhis.bemerk, Gl_jourhis.fibukonto, Gl_jourhis._recid).join(Gl_jourhis,(Gl_jourhis.jnr == Gl_jhdrhis.jnr) & (Gl_jourhis.fibukonto == (fibu).lower())).filter(
                 (Gl_jhdrhis.datum >= from_datehis) & (Gl_jhdrhis.datum <= to_datehis)).order_by(Gl_jhdrhis.datum).all():
            b1_list = B1_list()
            b1_list_data.append(b1_list)

            b1_list.jnr = gl_jhdrhis.jnr
            b1_list.datum = gl_jhdrhis.datum
            b1_list.refno = gl_jhdrhis.refno
            b1_list.bezeich = gl_jhdrhis.bezeich
            b1_list.debit =  to_decimal(gl_jourhis.debit)
            b1_list.credit =  to_decimal(gl_jourhis.credit)
            b1_list.userinit = gl_jourhis.userinit
            b1_list.bemerk = gl_jourhis.bemerk
            b1_list.jtype = gl_jhdrhis.jtype
            b1_list.fibukonto = gl_jourhis.fibukonto

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})
    t_gl_acct = T_gl_acct()
    t_gl_acct_data.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)
    t_from_date = from_date
    t_to_date = to_date
    from_date = None
    t_date = None


    tmp_lastday = lastday (t_from_date)

    gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, tmp_lastday)]})

    if gl_jouhdr:
        from_date = t_from_date
        to_date = t_to_date


        disp_it()
    else:

        gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, t_to_date)]})

        if gl_jouhdr:
            for t_date in date_range(t_from_date,t_to_date) :

                gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, t_date)]})

                if gl_jouhdr:
                    from_datehis = t_from_date
                    to_datehis = t_date - timedelta(days=1)


                    disp_it_his()
                    from_date = t_date
                    to_date = t_to_date


                    disp_it()
                    break
        else:
            from_datehis = t_from_date
            to_datehis = t_to_date


            disp_it_his()

    return generate_output()