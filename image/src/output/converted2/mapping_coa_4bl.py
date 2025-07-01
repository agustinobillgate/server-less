#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_accthis, Gl_jourhis, Gl_journal

coa_list_list, Coa_list = create_model("Coa_list", {"old_fibu":string, "new_fibu":string, "bezeich":string, "coastat":int, "old_main":int, "new_main":int, "bezeichm":string, "old_dept":int, "new_dept":int, "bezeichd":string, "catno":int, "acct":int, "old_acct":int}, {"coastat": -1})

def mapping_coa_4bl(coa_list_list:[Coa_list]):
    i:int = 0
    gl_acct = gl_accthis = gl_jourhis = gl_journal = None

    coa_list = acct_list = None

    acct_list_list, Acct_list = create_model_like(Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, gl_acct, gl_accthis, gl_jourhis, gl_journal


        nonlocal coa_list, acct_list
        nonlocal acct_list_list

        return {}

    def update_gl3():

        nonlocal i, gl_acct, gl_accthis, gl_jourhis, gl_journal


        nonlocal coa_list, acct_list
        nonlocal acct_list_list

        for acct_list in query(acct_list_list):
            acct_list_list.remove(acct_list)

        gl_acct = db_session.query(Gl_acct).first()
        while None != gl_acct:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == gl_acct.fibukonto), first=True)

            if coa_list:
                acct_list = Acct_list()
                acct_list_list.append(acct_list)

                buffer_copy(gl_acct, acct_list)
                pass
                db_session.delete(gl_acct)
                pass

            curr_recid = gl_acct._recid
            gl_acct = db_session.query(Gl_acct).filter(Gl_acct._recid > curr_recid).first()

        coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu != None), first=True)
        while None != coa_list:

            acct_list = query(acct_list_list, filters=(lambda acct_list: acct_list.fibukonto == coa_list.old_fibu), first=True)
            while None != acct_list:

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, coa_list.new_fibu)]})

                if gl_acct:
                    for i in range(1,12 + 1) :
                        gl_acct.actual[i - 1] = gl_acct.actual[i - 1] + acct_list.actual[i - 1]
                        gl_acct.last_yr[i - 1] = gl_acct.last_yr[i - 1] + acct_list.last_yr[i - 1]
                        gl_acct.budget[i - 1] = gl_acct.budget[i - 1] + acct_list.budget[i - 1]
                        gl_acct.ly_budget[i - 1] = gl_acct.ly_budget[i - 1] + acct_list.ly_budget[i - 1]
                        gl_acct.debit[i - 1] = gl_acct.debit[i - 1] + acct_list.debit[i - 1]
                        gl_acct.credit[i - 1] = gl_acct.credit[i - 1] + acct_list.credit[i - 1]


                else:
                    gl_acct = Gl_acct()
                    db_session.add(gl_acct)

                    buffer_copy(acct_list, gl_acct,except_fields=["fibukonto"])
                    gl_acct.fibukonto = coa_list.new_fibu
                    gl_acct.bezeich = coa_list.bezeich
                    gl_acct.main_nr = coa_list.new_main
                    gl_acct.deptnr = coa_list.new_dept
                    gl_acct.fs_type = coa_list.catno
                    gl_acct.acc_type = coa_list.acct

                acct_list = query(acct_list_list, filters=(lambda acct_list: acct_list.fibukonto == coa_list.old_fibu), next=True)

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu != None), next=True)

        for coa_list in query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == None and coa_list.new_fibu != "")):
            gl_acct = Gl_acct()
            db_session.add(gl_acct)

            gl_acct.fibukonto = coa_list.new_fibu
            gl_acct.bezeich = coa_list.bezeich
            gl_acct.main_nr = coa_list.new_main
            gl_acct.deptnr = coa_list.new_dept
            gl_acct.fs_type = coa_list.catno
            gl_acct.acc_type = coa_list.acct


    def delete_gl():

        nonlocal i, gl_acct, gl_accthis, gl_jourhis, gl_journal


        nonlocal coa_list, acct_list
        nonlocal acct_list_list

        for coa_list in query(coa_list_list, filters=(lambda coa_list: coa_list.coaStat == -1)):

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, coa_list.old_fibu)]})

            if gl_acct:
                db_session.delete(gl_acct)
                pass

            gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, coa_list.old_fibu)]})

            if gl_accthis:
                db_session.delete(gl_accthis)
                pass

            gl_jourhis = get_cache (Gl_jourhis, {"fibukonto": [(eq, coa_list.old_fibu)]})

            if gl_jourhis:
                db_session.delete(gl_jourhis)
                pass

            gl_journal = get_cache (Gl_journal, {"fibukonto": [(eq, coa_list.old_fibu)]})

            if gl_journal:
                db_session.delete(gl_journal)
                pass


    update_gl3()
    delete_gl()

    return generate_output()