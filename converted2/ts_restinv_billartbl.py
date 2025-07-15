#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Paramtext

def ts_restinv_billartbl(billart:int, curr_dept:int):

    prepare_cache ([Paramtext])

    price = to_decimal("0.0")
    t_h_artikel_data = []
    h_artikel = paramtext = None

    t_h_artikel = None

    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price, t_h_artikel_data, h_artikel, paramtext
        nonlocal billart, curr_dept


        nonlocal t_h_artikel
        nonlocal t_h_artikel_data

        return {"price": price, "t-h-artikel": t_h_artikel_data}

    def get_price():

        nonlocal price, t_h_artikel_data, h_artikel, paramtext
        nonlocal billart, curr_dept


        nonlocal t_h_artikel
        nonlocal t_h_artikel_data

        i:int = 0
        n:int = 0
        j:int = 0
        tolerance:int = 0
        curr_min:int = 0
        price =  to_decimal(h_artikel.epreis1)

        if h_artikel.epreis2 == 0:

            return

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, (10000 + curr_dept))]})

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


    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel.artnr == billart) & (H_artikel.departement == curr_dept) & (H_artikel.activeflag) & (H_artikel.artart == 0)).first()

    if h_artikel:
        t_h_artikel = T_h_artikel()
        t_h_artikel_data.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = h_artikel._recid


        get_price()

    return generate_output()