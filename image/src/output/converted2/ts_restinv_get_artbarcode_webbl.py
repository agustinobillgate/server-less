#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Queasy, Paramtext

def ts_restinv_get_artbarcode_webbl(barcode:string, table_no:int, dept_no:int):

    prepare_cache ([Queasy, Paramtext])

    mess_info = ""
    price = to_decimal("0.0")
    t_h_artikel_list = []
    billart:int = 0
    h_artikel = queasy = paramtext = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_info, price, t_h_artikel_list, billart, h_artikel, queasy, paramtext
        nonlocal barcode, table_no, dept_no


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        return {"mess_info": mess_info, "price": price, "t-h-artikel": t_h_artikel_list}

    def get_price():

        nonlocal mess_info, price, t_h_artikel_list, billart, h_artikel, queasy, paramtext
        nonlocal barcode, table_no, dept_no


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        i:int = 0
        n:int = 0
        j:int = 0
        tolerance:int = 0
        curr_min:int = 0
        price =  to_decimal(h_artikel.epreis1)

        if h_artikel.epreis2 == 0:

            return

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, (10000 + dept_no))]})

        if paramtext:
            tolerance = paramtext.sprachcode
            curr_min = to_int(substring(to_string(get_current_time_in_seconds(), "HH:MM:SS") , 3, 2))
            i = round((get_current_time_in_seconds() / 3600 - 0.5) , 0)

            if i <= 0:
                i = 24
            n = to_int(substring(paramtext.ptexte, i - 1, 1))

            if n == 2:
                price =  to_decimal(h_artikel.epreis2)

            elif tolerance > 0:

                if i == 1:
                    j = 24
                else:
                    j = i - 1

                if to_int(substring(paramtext.ptexte, j - 1, 1)) == 2 and curr_min <= tolerance:
                    price =  to_decimal(h_artikel.epreis2)


    if table_no == 0:
        mess_info = "Select a table first."

        return generate_output()

    if barcode == None:
        barcode = ""

    queasy = get_cache (Queasy, {"key": [(eq, 200)],"char1": [(eq, barcode)]})

    if queasy:

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, queasy.number2)],"departement": [(eq, queasy.number1)],"artart": [(eq, 0)]})

        if h_artikel:

            if h_artikel.activeflag:
                billart = h_artikel.artnr
            else:
                mess_info = "Article is no longer active. Choose another barcode."

                return generate_output()
            t_h_artikel = T_h_artikel()
            t_h_artikel_list.append(t_h_artikel)

            buffer_copy(h_artikel, t_h_artikel)
            t_h_artikel.rec_id = h_artikel._recid


            get_price()

    return generate_output()