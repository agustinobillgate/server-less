#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Gl_journal, Gl_acct, Gl_jourhis, Gl_jhdrhis

def netsuite_loadjournaldetailbl(from_date:date, to_date:date):

    prepare_cache ([Gl_jouhdr, Gl_journal, Gl_acct, Gl_jourhis, Gl_jhdrhis])

    gldetail_list_data = []
    t_from_date:date = None
    t_to_date:date = None
    from_datehis:date = None
    to_datehis:date = None
    t_date:date = None
    bemerkgl:string = ""
    gl_jouhdr = gl_journal = gl_acct = gl_jourhis = gl_jhdrhis = None

    gldetail_list = None

    gldetail_list_data, Gldetail_list = create_model("Gldetail_list", {"jnr":int, "datum":date, "refno":string, "bezeich":string, "debit":Decimal, "credit":Decimal, "userinit":string, "bemerk":string, "jtype":int, "fibukonto":string, "mappingcoa":string, "coadept":int, "dept_id":int, "class_id":int, "entity_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gldetail_list_data, t_from_date, t_to_date, from_datehis, to_datehis, t_date, bemerkgl, gl_jouhdr, gl_journal, gl_acct, gl_jourhis, gl_jhdrhis
        nonlocal from_date, to_date


        nonlocal gldetail_list
        nonlocal gldetail_list_data

        return {"gldetail-list": gldetail_list_data}

    def lastday(d:date):

        nonlocal gldetail_list_data, t_from_date, t_to_date, from_datehis, to_datehis, t_date, bemerkgl, gl_jouhdr, gl_journal, gl_acct, gl_jourhis, gl_jhdrhis
        nonlocal from_date, to_date


        nonlocal gldetail_list
        nonlocal gldetail_list_data


        return add_interval(date_mdy(get_month(d) , 1, get_year(d)) , 1, "month") - 1


    def disp_it():

        nonlocal gldetail_list_data, t_from_date, t_to_date, from_datehis, to_datehis, t_date, bemerkgl, gl_jouhdr, gl_journal, gl_acct, gl_jourhis, gl_jhdrhis
        nonlocal from_date, to_date


        nonlocal gldetail_list
        nonlocal gldetail_list_data

        gl_jouhdr = Gl_jouhdr()
        gl_journal = Gl_journal()
        for gl_jouhdr.jnr, gl_jouhdr.datum, gl_jouhdr.refno, gl_jouhdr.bezeich, gl_jouhdr.jtype, gl_jouhdr._recid, gl_journal.bemerk, gl_journal.debit, gl_journal.credit, gl_journal.userinit, gl_journal.fibukonto, gl_journal._recid in db_session.query(Gl_jouhdr.jnr, Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich, Gl_jouhdr.jtype, Gl_jouhdr._recid, Gl_journal.bemerk, Gl_journal.debit, Gl_journal.credit, Gl_journal.userinit, Gl_journal.fibukonto, Gl_journal._recid).join(Gl_journal,(Gl_journal.jnr == Gl_jouhdr.jnr) & (Gl_journal.fibukonto == fibu)).filter(
                 (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum).all():

            if num_entries(gl_journal.bemerk, ";") >= 2:
                bemerkgl = entry(0, gl_journal.bemerk, ";")
            else:
                bemerkgl = gl_journal.bemerk
            gldetail_list = Gldetail_list()
            gldetail_list_data.append(gldetail_list)

            gldetail_list.jnr = gl_jouhdr.jnr
            gldetail_list.datum = gl_jouhdr.datum
            gldetail_list.refno = gl_jouhdr.refno
            gldetail_list.bezeich = gl_jouhdr.bezeich
            gldetail_list.debit =  to_decimal(gl_journal.debit)
            gldetail_list.credit =  to_decimal(gl_journal.credit)
            gldetail_list.userinit = gl_journal.userinit
            gldetail_list.bemerk = gl_jouhdr.refno + "|" + bemerkgl
            gldetail_list.jtype = gl_jouhdr.jtype
            gldetail_list.fibukonto = gl_journal.fibukonto

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, gl_journal.fibukonto)]})

            if gl_acct:
                gldetail_list.coadept = gl_acct.deptnr

                if num_entries(gl_acct.userinit, ";") >= 2:
                    gldetail_list.mappingcoa = entry(1, gl_acct.userinit, ";")
                else:
                    gldetail_list.mappingcoa = ""

                if num_entries(gl_acct.bemerk, "|") >= 2:
                    gldetail_list.dept_id = to_int(entry(0, gl_acct.bemerk, "|"))
                    gldetail_list.class_id = to_int(entry(1, gl_acct.bemerk, "|"))
                    gldetail_list.entity_id = to_int(replace_str(entry(2, gl_acct.bemerk, "|") , ";", ""))


    def disp_it_his():

        nonlocal gldetail_list_data, t_from_date, t_to_date, from_datehis, to_datehis, t_date, bemerkgl, gl_jouhdr, gl_journal, gl_acct, gl_jourhis, gl_jhdrhis
        nonlocal from_date, to_date


        nonlocal gldetail_list
        nonlocal gldetail_list_data

        gl_jhdrhis = Gl_jhdrhis()
        gl_jourhis = Gl_jourhis()
        for gl_jhdrhis.jnr, gl_jhdrhis.datum, gl_jhdrhis.refno, gl_jhdrhis.bezeich, gl_jhdrhis.jtype, gl_jhdrhis._recid, gl_jourhis.debit, gl_jourhis.credit, gl_jourhis.userinit, gl_jourhis.fibukonto, gl_jourhis._recid in db_session.query(Gl_jhdrhis.jnr, Gl_jhdrhis.datum, Gl_jhdrhis.refno, Gl_jhdrhis.bezeich, Gl_jhdrhis.jtype, Gl_jhdrhis._recid, Gl_jourhis.debit, Gl_jourhis.credit, Gl_jourhis.userinit, Gl_jourhis.fibukonto, Gl_jourhis._recid).join(Gl_jourhis,(Gl_jourhis.jnr == Gl_jhdrhis.jnr) & (Gl_jourhis.fibukonto == fibu)).filter(
                 (Gl_jhdrhis.datum >= from_datehis) & (Gl_jhdrhis.datum <= to_datehis)).order_by(Gl_jhdrhis.datum).all():

            if num_entries(gl_journal.bemerk, ";") >= 2:
                bemerkgl = entry(0, gl_journal.bemerk, ";")
            else:
                bemerkgl = gl_journal.bemerk
            gldetail_list = Gldetail_list()
            gldetail_list_data.append(gldetail_list)

            gldetail_list.jnr = gl_jhdrhis.jnr
            gldetail_list.datum = gl_jhdrhis.datum
            gldetail_list.refno = gl_jhdrhis.refno
            gldetail_list.bezeich = gl_jhdrhis.bezeich
            gldetail_list.debit =  to_decimal(gl_jourhis.debit)
            gldetail_list.credit =  to_decimal(gl_jourhis.credit)
            gldetail_list.userinit = gl_jourhis.userinit
            gldetail_list.bemerk = gl_jhdrhis.bezeich + "|" + bemerkgl
            gldetail_list.jtype = gl_jhdrhis.jtype
            gldetail_list.fibukonto = gl_jourhis.fibukonto

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, gl_jourhis.fibukonto)]})

            if gl_acct:
                gldetail_list.coadept = gl_acct.deptnr

                if num_entries(gl_acct.userinit, ";") >= 2:
                    gldetail_list.mappingcoa = entry(1, gl_acct.userinit, ";")
                else:
                    gldetail_list.mappingcoa = ""

                if num_entries(gl_acct.bemerk, "|") >= 2:
                    gldetail_list.dept_id = to_int(entry(0, gl_acct.bemerk, "|"))
                    gldetail_list.class_id = to_int(entry(1, gl_acct.bemerk, "|"))
                    gldetail_list.entity_id = to_int(replace_str(entry(2, gl_acct.bemerk, "|") , ";", ""))

    t_from_date = from_date
    t_to_date = to_date
    from_date = None
    t_date = None

    gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, lastday (t_from_date))]})

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

    for gldetail_list in query(gldetail_list_data):
        gldetail_list.bemerk = replace_str(gldetail_list.bemerk, "&", "")
        gldetail_list.bemerk = replace_str(gldetail_list.bemerk, "/", "-")

    return generate_output()