from functions.additional_functions import *
import decimal
from models import Gl_journal, Gl_jourhis, Gl_accthis, Gl_acct

coa_list_list, Coa_list = create_model("Coa_list", {"old_fibu":str, "new_fibu":str, "bezeich":str, "coastat":int, "old_main":int, "new_main":int, "bezeichm":str, "old_dept":int, "new_dept":int, "bezeichd":str, "catno":int, "acct":int, "old_acct":int}, {"coastat": -1})

def mapping_coa_2bl(coa_list_list:[Coa_list]):
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
        temp_gl_journal_list.clear()

        gl_journal = db_session.query(Gl_journal).first()
        while None != gl_journal:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == gl_journal.fibukonto), first=True)

            if coa_list:
                temp_gl_journal = Temp_gl_journal()
                temp_gl_journal_list.append(temp_gl_journal)

                buffer_copy(gl_journal, temp_gl_journal)
                db_session.delete(gl_journal)
                pass

            curr_recid = gl_journal._recid
            gl_journal = db_session.query(Gl_journal).filter(Gl_journal._recid > curr_recid).first()


        temp_gl_journal = query(temp_gl_journal_list, first=True)
        while None != temp_gl_journal:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == temp_gl_journal.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                temp_gl_journal.fibukonto = coa_list.new_fibu


                gl_journal = Gl_journal()
                db_session.add(gl_journal)

                buffer_copy(temp_gl_journal, gl_journal)

            temp_gl_journal = query(temp_gl_journal_list, next=True)
        temp_gl_jourhis_list.clear()

        gl_jourhis = db_session.query(Gl_jourhis).first()
        while None != gl_jourhis:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == gl_jourhis.fibukonto), first=True)

            if coa_list:
                temp_gl_jourhis = Temp_gl_jourhis()
                temp_gl_jourhis_list.append(temp_gl_jourhis)

                buffer_copy(gl_jourhis, temp_gl_jourhis)
                db_session.delete(gl_jourhis)
                pass

            curr_recid = gl_jourhis._recid
            gl_jourhis = db_session.query(Gl_jourhis).filter(Gl_jourhis._recid > curr_recid).first()


        temp_gl_jourhis = query(temp_gl_jourhis_list, first=True)
        while None != temp_gl_jourhis:

            coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.old_fibu == temp_gl_jourhis.fibukonto and coa_list.new_fibu != None), first=True)

            if coa_list:
                temp_gl_jourhis.fibukonto = coa_list.new_fibu


                gl_jourhis = Gl_jourhis()
                db_session.add(gl_jourhis)

                buffer_copy(temp_gl_jourhis, gl_jourhis)

            temp_gl_jourhis = query(temp_gl_jourhis_list, next=True)

    update_gl()

    return generate_output()