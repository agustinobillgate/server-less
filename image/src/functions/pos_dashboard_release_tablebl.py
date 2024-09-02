from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def pos_dashboard_release_tablebl(release_table:[Release_table], dynamic_qr:bool, asroom_service:bool):
    error_msg = ""
    count_i:int = 0
    bill_no:int = 0
    dept_no:int = 0
    table_no:int = 0
    session_params:str = ""
    mess_str:str = ""
    mess_token:str = ""
    mess_keyword:str = ""
    mess_value:str = ""
    date_time: = None
    queasy = None

    release_table = buff_orderbill = pickup_table = q_orderbill = q_searchbill = q_orderbill_line = q_search_orderbill_line = None

    release_table_list, Release_table = create_model("Release_table", {"dept":int, "tableno":int, "pax":int, "gname":str, "occupied":bool, "session_parameter":str, "gemail":str, "expired_session":bool, "dataqr":str, "date_time":})

    Buff_orderbill = Queasy
    Pickup_table = Queasy
    Q_orderbill = Queasy
    Q_searchbill = Queasy
    Q_orderbill_line = Queasy
    Q_search_orderbill_line = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_msg, count_i, bill_no, dept_no, table_no, session_params, mess_str, mess_token, mess_keyword, mess_value, date_time, queasy
        nonlocal buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line


        nonlocal release_table, buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line
        nonlocal release_table_list
        return {"error_msg": error_msg}

    def dynamic_release():

        nonlocal error_msg, count_i, bill_no, dept_no, table_no, session_params, mess_str, mess_token, mess_keyword, mess_value, date_time, queasy
        nonlocal buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line


        nonlocal release_table, buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line
        nonlocal release_table_list

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 230) &  (Queasy.number1 == dept_no) &  (Queasy.number2 == table_no) &  (func.lower(Queasy.char1) == (session_params).lower())).first()

        if queasy:

            for q_searchbill in db_session.query(Q_searchbill).filter(
                    (Q_searchbill.key == 225) &  (func.lower(Q_searchbill.char1) == "orderbill") &  (Q_searchbill.number1 == dept_no) &  (Q_searchbill.number2 == table_no) &  (Q_searchbill.logi1) &  (func.lower(Q_searchbill.char3) == (session_params).lower()) &  (num_entries(Q_searchbill.char2, "|Q_searchbill.") <= 7)).all():

                if not q_searchbill.logi3:
                    error_msg = "Please make sure ALL Cancel Order is Posted."

                    return

            q_orderbill = db_session.query(Q_orderbill).filter(
                    (Q_orderbill.key == 225) &  (func.lower(Q_orderbill.char1) == "orderbill") &  (Q_orderbill.number1 == dept_no) &  (Q_orderbill.number2 == table_no) &  (Q_orderbill.logi1) &  (Q_orderbill.logi3) &  (func.lower(Q_orderbill.char3) == (session_params).lower()) &  (num_entries(Q_orderbill.char2, "|Q_orderbill.") <= 7)).first()

            if q_orderbill:

                for q_orderbill in db_session.query(Q_orderbill).filter(
                        (Q_orderbill.key == 225) &  (func.lower(Q_orderbill.char1) == "orderbill") &  (Q_orderbill.number1 == dept_no) &  (Q_orderbill.number2 == table_no) &  (Q_orderbill.logi1) &  (Q_orderbill.logi3) &  (func.lower(Q_orderbill.char3) == (session_params).lower()) &  (num_entries(Q_orderbill.char2, "|Q_orderbill.") <= 7)).all():
                    q_orderbill.logi1 = False
                    q_orderbill.char3 = q_orderbill.char3 + "T" +\
                            replace_str(to_string(get_current_date()) , "/", "") +\
                            replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "") +\
                            ";" + "1_GLFT"

            pickup_table = db_session.query(Pickup_table).filter(
                    (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.number1 == dept_no) &  (Pickup_table.number2 == table_no) &  (Pickup_table.logi1) &  (Pickup_table.logi2) &  (entry(0, Pickup_table.char3, "|Pickup_table.") == (session_params).lower())).first()

            if pickup_table:
                pickup_table.char3 = entry(0, pickup_table.char3, "|", session_params + "T" +\
                        replace_str(to_string(get_current_date()) , "/", "") +\
                        replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "") +\
                        ";" + "1_GLFT")

            queasy = db_session.query(Queasy).first()
            queasy.logi1 = True

            queasy = db_session.query(Queasy).first()

            error_msg = "Table Released."

    def static_release():

        nonlocal error_msg, count_i, bill_no, dept_no, table_no, session_params, mess_str, mess_token, mess_keyword, mess_value, date_time, queasy
        nonlocal buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line


        nonlocal release_table, buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line
        nonlocal release_table_list

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.number1 == dept_no) &  (Queasy.number2 == table_no) &  (Queasy.logi1) &  (Queasy.logi3) &  (func.lower(Queasy.char3) == (session_params).lower()) &  (num_entries(Queasy.char2, "|Queasy.") <= 7)).first()

        if queasy:

            for q_searchbill in db_session.query(Q_searchbill).filter(
                    (Q_searchbill.key == 225) &  (func.lower(Q_searchbill.char1) == "orderbill") &  (Q_searchbill.number1 == dept_no) &  (Q_searchbill.number2 == table_no) &  (Q_searchbill.logi1) &  (func.lower(Q_searchbill.char3) == (session_params).lower()) &  (num_entries(Q_searchbill.char2, "|Q_searchbill.") <= 7)).all():

                if not q_searchbill.logi3:
                    error_msg = "Please make sure ALL Cancel Order is Posted."

                    return

            for q_orderbill in db_session.query(Q_orderbill).filter(
                    (Q_orderbill.key == 225) &  (func.lower(Q_orderbill.char1) == "orderbill") &  (Q_orderbill.number1 == dept_no) &  (Q_orderbill.number2 == table_no) &  (Q_orderbill.logi1) &  (Q_orderbill.logi3) &  (func.lower(Q_orderbill.char3) == (session_params).lower()) &  (num_entries(Q_orderbill.char2, "|Q_orderbill.") <= 7)).all():

                for q_orderbill_line in db_session.query(Q_orderbill_line).filter(
                        (Q_orderbill_line.key == 225) &  (func.lower(Q_orderbill_line.char1) == "orderbill_line") &  (Q_orderbill_line.number1 == q_orderbill.number3) &  (Q_orderbill_line.number2 == table_no) &  (to_int(entry(0, Q_orderbill_line.char2, "|Q_orderbill_line.Q_orderbill_line.")) == dept_no) &  (entry(3, Q_orderbill_line.char2, "|Q_orderbill_line.") == (session_params).lower()) &  (Q_orderbill_line.logi2 == False) &  (Q_orderbill_line.logi3 == False)).all():
                    q_orderbill_line.char2 = entry(0, q_orderbill_line.char2, "|") + "|" +\
                            entry(1, q_orderbill_line.char2, "|") + "|" +\
                            entry(2, q_orderbill_line.char2, "|") + "|" +\
                            session_params + "T" + replace_str(to_string(get_current_date()) , "/", "") +\
                            replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "") +\
                            ";" + "1_GLFT"


                q_orderbill.logi1 = False
                q_orderbill.char3 = q_orderbill.char3 + "T" +\
                        replace_str(to_string(get_current_date()) , "/", "") +\
                        replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "") +\
                        ";" + "1_GLFT"


            error_msg = "Table Released."
        else:
            error_msg = "Please make sure Cancel Order is Posted."

            return

    release_table = query(release_table_list, first=True)

    if not release_table:

        return generate_output()
    dept_no = release_table.dept
    table_no = release_table.tableno
    session_params = release_table.session_parameter
    date_time = release_table.date_time

    if dynamic_qr:
        dynamic_release()
    else:
        static_release()

    return generate_output()