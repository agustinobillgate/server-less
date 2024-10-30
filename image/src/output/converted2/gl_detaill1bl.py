from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_acct, Gl_jouhdr, Gl_journal, Gl_jourhis, Gl_jhdrhis

def gl_detaill1bl(fibu:str, from_date:date, to_date:date):
    b1_list_list = []
    t_gl_acct_list = []
    t_from_date:date = None
    t_to_date:date = None
    from_datehis:date = None
    to_datehis:date = None
    t_date:date = None
    gl_acct = gl_jouhdr = gl_journal = gl_jourhis = gl_jhdrhis = None

    b1_list = t_gl_acct = None

    b1_list_list, B1_list = create_model("B1_list", {"jnr":int, "datum":date, "refno":str, "bezeich":str, "debit":decimal, "credit":decimal, "userinit":str, "bemerk":str, "jtype":int, "fibukonto":str})
    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, t_gl_acct_list, t_from_date, t_to_date, from_datehis, to_datehis, t_date, gl_acct, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis
        nonlocal fibu, from_date, to_date


        nonlocal b1_list, t_gl_acct
        nonlocal b1_list_list, t_gl_acct_list

        return {"b1-list": b1_list_list, "t-gl-acct": t_gl_acct_list}

    def lastDay(d:date):

        nonlocal b1_list_list, t_gl_acct_list, t_from_date, t_to_date, from_datehis, to_datehis, t_date, gl_acct, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis
        nonlocal fibu, from_date, to_date


        nonlocal b1_list, t_gl_acct
        nonlocal b1_list_list, t_gl_acct_list


        return add_interval(date_mdy(get_month(d) , 1, get_year(d)) , 1, "month") - 1


    def disp_it():

        nonlocal b1_list_list, t_gl_acct_list, t_from_date, t_to_date, from_datehis, to_datehis, t_date, gl_acct, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis
        nonlocal fibu, from_date, to_date


        nonlocal b1_list, t_gl_acct
        nonlocal b1_list_list, t_gl_acct_list

        for gl_jouhdr, gl_journal in db_session.query(Gl_jouhdr, Gl_journal).join(Gl_journal,(Gl_journal.jnr == Gl_jouhdr.jnr) & (func.lower(Gl_journal.fibukonto) == (fibu).lower())).filter(
                 (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum).all():
            b1_list = B1_list()
            b1_list_list.append(b1_list)

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

        nonlocal b1_list_list, t_gl_acct_list, t_from_date, t_to_date, from_datehis, to_datehis, t_date, gl_acct, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis
        nonlocal fibu, from_date, to_date


        nonlocal b1_list, t_gl_acct
        nonlocal b1_list_list, t_gl_acct_list

        for gl_jhdrhis, gl_jourhis in db_session.query(Gl_jhdrhis, Gl_jourhis).join(Gl_jourhis,(Gl_jourhis.jnr == Gl_jhdrhis.jnr) & (func.lower(Gl_jourhis.fibukonto) == (fibu).lower())).filter(
                 (Gl_jhdrhis.datum >= from_datehis) & (Gl_jhdrhis.datum <= to_datehis)).order_by(Gl_jhdrhis.datum).all():
            b1_list = B1_list()
            b1_list_list.append(b1_list)

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

    gl_acct = db_session.query(Gl_acct).filter(
             (func.lower(Gl_acct.fibukonto) == (fibu).lower())).first()
    t_gl_acct = T_gl_acct()
    t_gl_acct_list.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)
    t_from_date = from_date
    t_to_date = to_date
    from_date = None
    t_date = None

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.datum <= lastDay (t_from_date))).first()

    if gl_jouhdr:
        from_date = t_from_date
        to_date = t_to_date


        disp_it()
    else:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum <= t_to_date)).first()

        if gl_jouhdr:
            for t_date in date_range(t_from_date,t_to_date) :

                gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.datum <= t_date)).first()

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