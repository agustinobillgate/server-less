from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def pos_dashboard_taken_tablebl(case_type:int, sessionid:str, table_nr:int, guest_name:str, pax:int, dept:int, pathqr:str, date_time:, dynamic_flag:bool):
    success_taken = False
    pick_table_list = []
    mess_str:str = ""
    i_str:int = 0
    mess_token:str = ""
    mess_keyword:str = ""
    mess_value:str = ""
    tpax:int = 0
    gname:str = ""
    table_no:int = 0
    dtime: = None
    queasy = None

    pick_table = posted_item = session_table = None

    pick_table_list, Pick_table = create_model("Pick_table", {"dept":int, "tableno":int, "pax":int, "gname":str, "occupied":bool, "session_parameter":str, "gemail":str, "active_session":bool, "dataqr":str, "date_time":})

    Posted_item = Queasy
    Session_table = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_taken, pick_table_list, mess_str, i_str, mess_token, mess_keyword, mess_value, tpax, gname, table_no, dtime, queasy
        nonlocal posted_item, session_table


        nonlocal pick_table, posted_item, session_table
        nonlocal pick_table_list
        return {"success_taken": success_taken, "pick-table": pick_table_list}

    def create_table():

        nonlocal success_taken, pick_table_list, mess_str, i_str, mess_token, mess_keyword, mess_value, tpax, gname, table_no, dtime, queasy
        nonlocal posted_item, session_table


        nonlocal pick_table, posted_item, session_table
        nonlocal pick_table_list

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (func.lower(Queasy.char1) == "taken_table") &  (entry(0, Queasy.char3, "|Queasy.") == sessionid) &  (Queasy.logi1)).first()

        if queasy:
            success_taken = False
        else:
            success_taken = True
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 225
            queasy.number2 = table_nr
            queasy.number1 = dept
            queasy.char1 = "taken_table"
            queasy.char2 = "TB == " + to_string(table_nr) +\
                    "|NM == " + guest_name +\
                    "|PX == " + to_string(pax) +\
                    "|TM == " + to_string(date_time)
            queasy.char3 = sessionid + "|" + pathqr
            queasy.logi1 = True
            queasy.logi2 = dynamic_flag


            pass

    if case_type == 1:
        create_table()

    return generate_output()