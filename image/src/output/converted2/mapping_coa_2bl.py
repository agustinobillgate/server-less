#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_journal, Gl_jourhis, Gl_accthis, Gl_acct

coa_list_list, Coa_list = create_model("Coa_list", {"old_fibu":string, "new_fibu":string, "bezeich":string, "coastat":int, "old_main":int, "new_main":int, "bezeichm":string, "old_dept":int, "new_dept":int, "bezeichd":string, "catno":int, "acct":int, "old_acct":int}, {"coastat": -1})

def mapping_coa_2bl(coa_list_list:[Coa_list]):

    prepare_cache ([Gl_journal, Gl_jourhis])

    gl_journal = gl_jourhis = gl_accthis = gl_acct = None

    coa_list = temp_gl_journal = temp_gl_jourhis = None

    temp_gl_journal_list, Temp_gl_journal = create_model_like(Gl_journal)
    temp_gl_jourhis_list, Temp_gl_jourhis = create_model_like(Gl_jourhis)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_journal, gl_jourhis, gl_accthis, gl_acct


        nonlocal coa_list, temp_gl_journal, temp_gl_jourhis
        nonlocal temp_gl_journal_list, temp_gl_jourhis_list

        return {}

    def update_gl():

        nonlocal gl_journal, gl_jourhis, gl_accthis, gl_acct


        nonlocal coa_list, temp_gl_journal, temp_gl_jourhis
        nonlocal temp_gl_journal_list, temp_gl_jourhis_list

        gljourbuff2 = None
        jouhisbuff2 = None
        acchisbuff2 = None
        acctbuff = None
        acctbuff2 = None
        i:int = 0
        Gljourbuff2 =  create_buffer("Gljourbuff2",Gl_journal)
        Jouhisbuff2 =  create_buffer("Jouhisbuff2",Gl_jourhis)
        Acchisbuff2 =  create_buffer("Acchisbuff2",Gl_accthis)
        Acctbuff =  create_buffer("Acctbuff",Gl_acct)
        Acctbuff2 =  create_buffer("Acctbuff2",Gl_acct)

        gl_journal = db_session.query(Gl_journal).first()
        while None != gl_journal:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == gl_journal.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:

                gljourbuff2 = get_cache (Gl_journal, {"_recid": [(eq, gl_journal._recid)]})
                gljourbuff2.fibukonto = coa_list.new_fibu


                pass
                pass

            curr_recid = gl_journal._recid
            gl_journal = db_session.query(Gl_journal).filter(Gl_journal._recid > curr_recid).first()

        gl_jourhis = db_session.query(Gl_jourhis).first()
        while None != gl_jourhis:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == gl_jourhis.fibukonto), first=True)

            if coa_list:

                jouhisbuff2 = get_cache (Gl_jourhis, {"_recid": [(eq, gl_jourhis._recid)]})
                jouhisbuff2.fibukonto = coa_list.new_fibu


                pass
                pass

            curr_recid = gl_jourhis._recid
            gl_jourhis = db_session.query(Gl_jourhis).filter(Gl_jourhis._recid > curr_recid).first()

    update_gl()

    return generate_output()