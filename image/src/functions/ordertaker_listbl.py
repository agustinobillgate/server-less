from functions.additional_functions import *
import decimal
from datetime import date
from functions.rest_odtakerlist_btn_gobl import rest_odtakerlist_btn_gobl
from models import Htparam

def ordertaker_listbl(usr_nr:int, from_date:date, to_date:date):
    odtaker_list_list = []
    long_digit:bool = False
    htparam = None

    output_list = odtaker_list = None

    output_list_list, Output_list = create_model("Output_list", {"datum":date, "tischnr":int, "rechnr":int, "artnr":int, "bezeich":str, "dept":int, "anzahl":int, "betrag":decimal, "zeit":int, "kellnr1":int, "kellnr2":int})
    odtaker_list_list, Odtaker_list = create_model("Odtaker_list", {"datum":date, "tableno":str, "billno":int, "artno":int, "bezeich":str, "qty":int, "amount":decimal, "departement":str, "zeit":str, "id":str, "tb":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal odtaker_list_list, long_digit, htparam


        nonlocal output_list, odtaker_list
        nonlocal output_list_list, odtaker_list_list
        return {"odtaker-list": odtaker_list_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    output_list_list = get_output(rest_odtakerlist_btn_gobl(from_date, to_date, usr_nr, long_digit))
    odtaker_list_list.clear()

    for output_list in query(output_list_list):
        odtaker_list = Odtaker_list()
        odtaker_list_list.append(odtaker_list)

        odtaker_list.datum = output_list.datum
        odtaker_list.tableno = to_string(output_list.tischnr, ">>>9")
        odtaker_list.billno = output_list.rechnr
        odtaker_list.artno = output_list.artnr
        odtaker_list.bezeich = output_list.bezeich
        odtaker_list.qty = output_list.anzahl
        odtaker_list.amount = output_list.betrag
        odtaker_list.departement = to_string(output_list.dept, ">>>9")
        odtaker_list.zeit = to_string(output_list.zeit, "HH:MM")
        odtaker_list.id = to_string(output_list.kellnr1, ">9")
        odtaker_list.tb = to_string(output_list.kellnr2, ">9")

    return generate_output()