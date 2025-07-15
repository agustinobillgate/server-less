#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_accthis, Gl_acct

coa_list_data, Coa_list = create_model("Coa_list", {"old_fibu":string, "new_fibu":string, "bezeich":string, "coastat":int, "old_main":int, "new_main":int, "bezeichm":string, "old_dept":int, "new_dept":int, "bezeichd":string, "catno":int, "acct":int, "old_acct":int}, {"coastat": -1})

def mapping_coa_3bl(coa_list_data:[Coa_list]):
    i:int = 0
    gl_accthis = gl_acct = None

    coa_list = temp_gl_accthis = acct_list = None

    temp_gl_accthis_data, Temp_gl_accthis = create_model_like(Gl_accthis)
    acct_list_data, Acct_list = create_model_like(Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, gl_accthis, gl_acct


        nonlocal coa_list, temp_gl_accthis, acct_list
        nonlocal temp_gl_accthis_data, acct_list_data

        return {}

    def update_gl2():

        nonlocal i, gl_accthis, gl_acct


        nonlocal coa_list, temp_gl_accthis, acct_list
        nonlocal temp_gl_accthis_data, acct_list_data


        temp_gl_accthis_data.clear()

        gl_accthis = db_session.query(Gl_accthis).first()
        while None != gl_accthis:

            coa_list = query(coa_list_data, filters=(lambda coa_list: coa_list.old_fibu == gl_accthis.fibukonto), first=True)

            if coa_list:
                temp_gl_accthis = Temp_gl_accthis()
                temp_gl_accthis_data.append(temp_gl_accthis)

                buffer_copy(gl_accthis, temp_gl_accthis)
                pass
                db_session.delete(gl_accthis)
                pass

            curr_recid = gl_accthis._recid
            gl_accthis = db_session.query(Gl_accthis).filter(Gl_accthis._recid > curr_recid).first()

        coa_list = query(coa_list_data, first=True)
        while None != coa_list:

            temp_gl_accthis = query(temp_gl_accthis_data, filters=(lambda temp_gl_accthis: temp_gl_accthis.fibukonto == coa_list.old_fibu), first=True)
            while None != temp_gl_accthis:

                gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, coa_list.new_fibu)],"year": [(eq, temp_gl_accthis.year)]})

                if gl_accthis:
                    for i in range(1,12 + 1) :
                        gl_accthis.actual[i - 1] = gl_accthis.actual[i - 1] + temp_gl_accthis.actual[i - 1]
                        gl_accthis.last_yr[i - 1] = gl_accthis.last_yr[i - 1] + temp_gl_accthis.last_yr[i - 1]
                        gl_accthis.budget[i - 1] = gl_accthis.budget[i - 1] + temp_gl_accthis.budget[i - 1]
                        gl_accthis.ly_budget[i - 1] = gl_accthis.ly_budget[i - 1] + temp_gl_accthis.ly_budget[i - 1]
                        gl_accthis.debit[i - 1] = gl_accthis.debit[i - 1] + temp_gl_accthis.debit[i - 1]
                        gl_accthis.credit[i - 1] = gl_accthis.credit[i - 1] + temp_gl_accthis.credit[i - 1]


                else:
                    gl_accthis = Gl_accthis()
                    db_session.add(gl_accthis)

                    buffer_copy(temp_gl_accthis, gl_accthis,except_fields=["fibukonto"])
                    gl_accthis.fibukonto = coa_list.new_fibu
                    gl_accthis.bezeich = coa_list.bezeich
                    gl_accthis.main_nr = coa_list.new_main
                    gl_accthis.deptnr = coa_list.new_dept
                    gl_accthis.fs_type = coa_list.catno
                    gl_accthis.acc_type = coa_list.acct

                temp_gl_accthis = query(temp_gl_accthis_data, filters=(lambda temp_gl_accthis: temp_gl_accthis.fibukonto == coa_list.old_fibu), next=True)

            coa_list = query(coa_list_data, next=True)

    update_gl2()

    return generate_output()