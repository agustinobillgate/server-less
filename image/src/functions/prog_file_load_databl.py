from functions.additional_functions import *
import decimal
from models import Progfile

def prog_file_load_databl(main_nr:int):
    time_server = ""
    prog_list_list = []
    progfile = None

    prog_list = None

    prog_list_list, Prog_list = create_model("Prog_list", {"counter":int, "prog_grup":int, "prog_title":str, "prog_name":str, "prog_desc":str, "prog_active":bool, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal time_server, prog_list_list, progfile


        nonlocal prog_list
        nonlocal prog_list_list
        return {"time_server": time_server, "prog-list": prog_list_list}


    time_server = to_string(get_current_date(), "99/99/9999") + " " + to_string(get_current_time_in_seconds(), "HH:SS:MM")

    for progfile in db_session.query(Progfile).filter(
            (Progfile.catnr == main_nr)).all():
        prog_list = Prog_list()
        prog_list_list.append(prog_list)

        prog_list.counter = to_int(entry(0, progfile.bezeich, ";"))
        prog_list.prog_grup = to_int(entry(1, progfile.bezeich, ";"))
        prog_list.prog_title = entry(2, progfile.bezeich, ";")
        prog_list.prog_name = entry(3, progfile.bezeich, ";")
        prog_list.prog_desc = entry(4, progfile.bezeich, ";")
        prog_list.prog_active = logical(entry(5, progfile.bezeich, ";"))

    return generate_output()