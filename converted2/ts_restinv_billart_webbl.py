#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import H_artikel, Bediener, Wgrpdep, Paramtext

t_request_list_data, T_request_list = create_model("T_request_list", {"billart":int, "curr_dept":int, "user_init":string})

def ts_restinv_billart_webbl(t_request_list_data:[T_request_list]):

    prepare_cache ([Paramtext])

    price = to_decimal("0.0")
    error_message = ""
    t_h_artikel_data = []
    perm:List[int] = create_empty_list(120,0)
    loopn:int = 0
    h_artikel = bediener = wgrpdep = paramtext = None

    t_request_list = t_h_artikel = tp_bediener = None

    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    tp_bediener_data, Tp_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price, error_message, t_h_artikel_data, perm, loopn, h_artikel, bediener, wgrpdep, paramtext


        nonlocal t_request_list, t_h_artikel, tp_bediener
        nonlocal t_h_artikel_data, tp_bediener_data

        return {"price": price, "error_message": error_message, "t-h-artikel": t_h_artikel_data}

    def get_price():

        nonlocal price, error_message, t_h_artikel_data, perm, loopn, h_artikel, bediener, wgrpdep, paramtext


        nonlocal t_request_list, t_h_artikel, tp_bediener
        nonlocal t_h_artikel_data, tp_bediener_data

        i:int = 0
        n:int = 0
        j:int = 0
        tolerance:int = 0
        curr_min:int = 0
        price =  to_decimal(h_artikel.epreis1)

        if h_artikel.epreis2 == 0:

            return

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, (10000 + t_request_list.curr_dept))]})

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


    t_request_list = query(t_request_list_data, first=True)

    bediener = get_cache (Bediener, {"userinit": [(eq, t_request_list.user_init)]})

    if bediener:
        tp_bediener = Tp_bediener()
        tp_bediener_data.append(tp_bediener)

        buffer_copy(bediener, tp_bediener)

    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel.artnr == t_request_list.billart) & (H_artikel.departement == t_request_list.curr_dept) & (H_artikel.activeflag) & (H_artikel.artart == 0)).first()

    if h_artikel:
        t_h_artikel = T_h_artikel()
        t_h_artikel_data.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = h_artikel._recid


        get_price()

        tp_bediener = query(tp_bediener_data, first=True)
        for loopn in range(1,length(tp_bediener.permissions)  + 1) :
            perm[loopn - 1] = to_int(substring(tp_bediener.permissions, loopn - 1, 1))

        wgrpdep = db_session.query(Wgrpdep).filter(
                 (Wgrpdep.zknr == t_h_artikel.zwkum) & (Wgrpdep.departement == t_h_artikel.departement) & (matches(Wgrpdep.bezeich,"*DISCOUNT*"))).first()

        if wgrpdep:

            if perm[78] < 2:
                error_message = "Sorry, No Access Right. Access Code = 79,2"

                return generate_output()

    return generate_output()