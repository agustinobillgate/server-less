#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

release_table_list, Release_table = create_model("Release_table", {"dept":int, "tableno":int, "pax":int, "gname":string, "occupied":bool, "session_parameter":string, "gemail":string, "expired_session":bool, "dataqr":string, "date_time":datetime})

def pos_dashboard_release_tablebl(release_table_list:[Release_table], dynamic_qr:bool, asroom_service:bool):

    prepare_cache ([Queasy])

    error_msg = ""
    count_i:int = 0
    bill_no:int = 0
    dept_no:int = 0
    table_no:int = 0
    session_params:string = ""
    mess_str:string = ""
    mess_token:string = ""
    mess_keyword:string = ""
    mess_value:string = ""
    date_time:datetime = None
    queasy = None

    release_table = buff_orderbill = pickup_table = q_orderbill = q_searchbill = q_orderbill_line = q_search_orderbill_line = None

    Buff_orderbill = create_buffer("Buff_orderbill",Queasy)
    Pickup_table = create_buffer("Pickup_table",Queasy)
    Q_orderbill = create_buffer("Q_orderbill",Queasy)
    Q_searchbill = create_buffer("Q_searchbill",Queasy)
    Q_orderbill_line = create_buffer("Q_orderbill_line",Queasy)
    Q_search_orderbill_line = create_buffer("Q_search_orderbill_line",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_msg, count_i, bill_no, dept_no, table_no, session_params, mess_str, mess_token, mess_keyword, mess_value, date_time, queasy
        nonlocal dynamic_qr, asroom_service
        nonlocal buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line


        nonlocal release_table, buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line

        return {"error_msg": error_msg}

    def dynamic_release():

        nonlocal error_msg, count_i, bill_no, dept_no, table_no, session_params, mess_str, mess_token, mess_keyword, mess_value, date_time, queasy
        nonlocal dynamic_qr, asroom_service
        nonlocal buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line


        nonlocal release_table, buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line

        queasy = get_cache (Queasy, {"key": [(eq, 230)],"number1": [(eq, dept_no)],"number2": [(eq, table_no)],"char1": [(eq, session_params)]})

        if queasy:

            for q_searchbill in db_session.query(Q_searchbill).filter(
                     (Q_searchbill.key == 225) & (Q_searchbill.char1 == ("orderbill").lower()) & (Q_searchbill.number1 == dept_no) & (Q_searchbill.number2 == table_no) & (Q_searchbill.logi1) & (Q_searchbill.char3 == (session_params).lower()) & (num_entries(Q_searchbill.char2, "|") <= 7)).order_by(Q_searchbill._recid).all():

                if not q_searchbill.logi3:
                    error_msg = "Please make sure ALL Cancel Order is Posted."

                    return

            q_orderbill = db_session.query(Q_orderbill).filter(
                     (Q_orderbill.key == 225) & (Q_orderbill.char1 == ("orderbill").lower()) & (Q_orderbill.number1 == dept_no) & (Q_orderbill.number2 == table_no) & (Q_orderbill.logi1) & (Q_orderbill.logi3) & (Q_orderbill.char3 == (session_params).lower()) & (num_entries(Q_orderbill.char2, "|") <= 7)).first()

            if q_orderbill:

                for q_orderbill in db_session.query(Q_orderbill).filter(
                         (Q_orderbill.key == 225) & (Q_orderbill.char1 == ("orderbill").lower()) & (Q_orderbill.number1 == dept_no) & (Q_orderbill.number2 == table_no) & (Q_orderbill.logi1) & (Q_orderbill.logi3) & (Q_orderbill.char3 == (session_params).lower()) & (num_entries(Q_orderbill.char2, "|") <= 7)).order_by(Q_orderbill._recid).all():
                    q_orderbill.logi1 = False
                    q_orderbill.char3 = q_orderbill.char3 + "T" +\
                            replace_str(to_string(get_current_date()) , "/", "") +\
                            replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "") +\
                            ";" + "1-GLFT"

            pickup_table = db_session.query(Pickup_table).filter(
                     (Pickup_table.key == 225) & (Pickup_table.char1 == ("taken-table").lower()) & (Pickup_table.number1 == dept_no) & (Pickup_table.number2 == table_no) & (Pickup_table.logi1) & (Pickup_table.logi2) & (entry(0, Pickup_table.char3, "|") == (session_params).lower())).first()

            if pickup_table:
                pickup_table.char3 = entry(0, pickup_table.char3, "|", session_params + "T" +\
                        replace_str(to_string(get_current_date()) , "/", "") +\
                        replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "") +\
                        ";" + "1-GLFT")


            pass
            queasy.logi1 = True
            pass
            pass
            error_msg = "Table Released."


    def static_release():

        nonlocal error_msg, count_i, bill_no, dept_no, table_no, session_params, mess_str, mess_token, mess_keyword, mess_value, date_time, queasy
        nonlocal dynamic_qr, asroom_service
        nonlocal buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line


        nonlocal release_table, buff_orderbill, pickup_table, q_orderbill, q_searchbill, q_orderbill_line, q_search_orderbill_line

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 225) & (Queasy.char1 == ("orderbill").lower()) & (Queasy.number1 == dept_no) & (Queasy.number2 == table_no) & (Queasy.logi1) & (Queasy.logi3) & (Queasy.char3 == (session_params).lower()) & (num_entries(Queasy.char2, "|") <= 7)).first()

        if queasy:

            for q_searchbill in db_session.query(Q_searchbill).filter(
                     (Q_searchbill.key == 225) & (Q_searchbill.char1 == ("orderbill").lower()) & (Q_searchbill.number1 == dept_no) & (Q_searchbill.number2 == table_no) & (Q_searchbill.logi1) & (Q_searchbill.char3 == (session_params).lower()) & (num_entries(Q_searchbill.char2, "|") <= 7)).order_by(Q_searchbill._recid).all():

                if not q_searchbill.logi3:
                    error_msg = "Please make sure ALL Cancel Order is Posted."

                    return

            for q_orderbill in db_session.query(Q_orderbill).filter(
                     (Q_orderbill.key == 225) & (Q_orderbill.char1 == ("orderbill").lower()) & (Q_orderbill.number1 == dept_no) & (Q_orderbill.number2 == table_no) & (Q_orderbill.logi1) & (Q_orderbill.logi3) & (Q_orderbill.char3 == (session_params).lower()) & (num_entries(Q_orderbill.char2, "|") <= 7)).order_by(Q_orderbill._recid).all():

                for q_orderbill_line in db_session.query(Q_orderbill_line).filter(
                         (Q_orderbill_line.key == 225) & (Q_orderbill_line.char1 == ("orderbill-line").lower()) & (Q_orderbill_line.number1 == q_orderbill.number3) & (Q_orderbill_line.number2 == table_no) & (to_int(entry(0, Q_orderbill_line.char2, "|")) == dept_no) & (entry(3, Q_orderbill_line.char2, "|") == (session_params).lower()) & (Q_orderbill_line.logi2 == False) & (Q_orderbill_line.logi3 == False)).order_by(Q_orderbill_line._recid).all():
                    q_orderbill_line.char2 = entry(0, q_orderbill_line.char2, "|") + "|" +\
                            entry(1, q_orderbill_line.char2, "|") + "|" +\
                            entry(2, q_orderbill_line.char2, "|") + "|" +\
                            session_params + "T" + replace_str(to_string(get_current_date()) , "/", "") +\
                            replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "") +\
                            ";" + "1-GLFT"


                q_orderbill.logi1 = False
                q_orderbill.char3 = q_orderbill.char3 + "T" +\
                        replace_str(to_string(get_current_date()) , "/", "") +\
                        replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "") +\
                        ";" + "1-GLFT"


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