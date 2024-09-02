from functions.additional_functions import *
import decimal
from models import Progfile

def prog_file_btn_savebl(case_type:int, main_nr:int, counter:int, grupno:int, titleno:str, rname:str, bezeich:str, active_flag:bool):
    count_no:int = 0
    progfile = None

    prog_list = None

    prog_list_list, Prog_list = create_model("Prog_list", {"counter":int, "prog_grup":int, "prog_title":str, "prog_name":str, "prog_desc":str, "prog_active":bool, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal count_no, progfile


        nonlocal prog_list
        nonlocal prog_list_list
        return {}

    if case_type == 1:

        for progfile in db_session.query(Progfile).filter(
                (Progfile.catnr == main_nr) &  (Progfile.bezeich.op("~")(".*;.*"))).all():
            count_no = to_int(entry(0, progfile.bezeich, ";"))


            break
        count_no = count_no + 1


        progfile = Progfile()
        db_session.add(progfile)

        progfile.catnr = main_nr
        progfile.bezeich = to_string(count_no) + ";" +\
                to_string(grupno) + ";" +\
                titleno + ";" +\
                rname + ";" +\
                bezeich + ";" +\
                to_string(active_flag)


    elif case_type == 2:

        progfile = db_session.query(Progfile).filter(
                (Progfile.catnr == main_nr) &  (Progfile.bezeich.op("~")(".*;.*")) &  (to_int(entry(0, Progfile.bezeich, ";")) == counter)).first()

        if progfile:

            progfile = db_session.query(Progfile).first()
            progfile.bezeich = to_string(counter) + ";" +\
                    to_string(grupno) + ";" +\
                    titleno + ";" +\
                    rname + ";" +\
                    bezeich + ";" +\
                    to_string(active_flag)

            progfile = db_session.query(Progfile).first()

    elif case_type == 3:

        progfile = db_session.query(Progfile).filter(
                (Progfile.catnr == main_nr) &  (Progfile.bezeich.op("~")(".*;.*")) &  (to_int(entry(0, Progfile.bezeich, ";")) == counter)).first()

        if progfile:

            progfile = db_session.query(Progfile).first()
            db_session.delete(progfile)


    return generate_output()