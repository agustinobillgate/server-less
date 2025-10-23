#using conversion tools version: 1.0.0.117
"""_yusufwijaena_22/10/2025

    TicketID: 6526C2
        _remark_:   - fix python indentation
                    - fix var declaration
                    - fix spacing on long string
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Queasy, Res_history

input_list_data, Input_list = create_model(
    "Input_list", {
        "case_type":int, 
        "bediener_nr":int
        }
    )
t_artikel_data, T_artikel = create_model_like(Artikel, {
    "rec_id":int, 
    "minibar":bool
    })

def write_artikel_1_webbl(input_list_data:[Input_list], t_artikel_data:[T_artikel]):

    prepare_cache ([Artikel, Queasy, Res_history])

    success_flag = False
    case_type:int = 0
    bediener_nr:int = 0
    artikel = queasy = res_history = None

    t_artikel = input_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, case_type, bediener_nr, artikel, queasy, res_history
        nonlocal t_artikel, input_list

        return {
            "success_flag": success_flag
            }


    t_artikel = query(t_artikel_data, first=True)

    if not t_artikel:
        return generate_output()

    input_list = query(input_list_data, first=True)

    if not input_list:
        return generate_output()
    else:
        case_type = input_list.case_type
        bediener_nr = input_list.bediener_nr

    if case_type == 1:
        artikel = Artikel()

        buffer_copy(t_artikel, artikel)
        
        db_session.add(artikel)
        
        queasy = Queasy()

        queasy.key = 266
        queasy.number1 = t_artikel.departement
        queasy.number2 = t_artikel.artnr
        queasy.logi1 = t_artikel.minibar

        db_session.add(queasy)

        success_flag = True
    elif case_type == 2:
        artikel = get_cache (Artikel, {"_recid": [(eq, t_artikel.rec_id)]})

        if artikel:
            res_history = Res_history()

            res_history.nr = bediener_nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Modify ArtNo : " + to_string(t_artikel.artnr) + " => "
            res_history.action = "Artikel F/O"
            
            db_session.add(res_history)

            if t_artikel.bezeich != artikel.bezeich:
                res_history.aenderung = res_history.aenderung + " Description " + artikel.bezeich + " to : " + t_artikel.bezeich + " , "

            if t_artikel.zwkum != artikel.zwkum:
                res_history.aenderung = res_history.aenderung + " SubGroup " + to_string(artikel.zwkum) + " to : " + to_string(t_artikel.zwkum) + " , "

            if t_artikel.endkum != artikel.endkum:
                res_history.aenderung = res_history.aenderung + " Maingroup " + to_string(artikel.endkum) + " to : " + to_string(t_artikel.endkum) + " , "

            if t_artikel.epreis != artikel.epreis:
                res_history.aenderung = res_history.aenderung + " Unit Price " + to_string(artikel.epreis) + " to : " + to_string(t_artikel.epreis) + " , "

            if t_artikel.artart != artikel.artart:
                res_history.aenderung = res_history.aenderung + "  Art Type " + to_string(artikel.artart) + " to : " + to_string(t_artikel.artart) + " , "

            if t_artikel.mwst_code != artikel.mwst_code:
                res_history.aenderung = res_history.aenderung + " VAT " + to_string(artikel.mwst_code) + " to : " + to_string(t_artikel.mwst_code) + " , "

            if t_artikel.service_code != artikel.service_code:
                res_history.aenderung = res_history.aenderung + " Service Code " + to_string(artikel.service_code) + " to : " + to_string(t_artikel.service_code) + " , "

            if t_artikel.activeflag != artikel.activeflag:
                res_history.aenderung = res_history.aenderung + " Active Flag " + to_string(artikel.activeflag) + " to : " + to_string(t_artikel.activeflag) + " , "

            if t_artikel.fibukonto != artikel.fibukonto:
                res_history.aenderung = res_history.aenderung + " Chart of Account " + to_string(artikel.fibukonto) + " to : " + to_string(t_artikel.fibukonto) + " , "
            buffer_copy(t_artikel, artikel)

            queasy = get_cache (Queasy, {
                "key": [(eq, 266)],
                "number1": [(eq, t_artikel.departement)],
                "number2": [(eq, t_artikel.artnr)]})

            if not queasy:
                queasy = Queasy()

                queasy.key = 266
                queasy.number1 = t_artikel.departement
                queasy.number2 = t_artikel.artnr
                queasy.logi1 = t_artikel.minibar

                db_session.add(queasy)

            else:
                queasy.logi1 = t_artikel.minibar

            success_flag = True

    return generate_output()