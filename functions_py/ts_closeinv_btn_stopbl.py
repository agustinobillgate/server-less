#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd 3/8/2025
# if not availble -> return
# Rd, 01/12/2025, with_for_update added
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill_line, H_bill, H_umsatz, Queasy

t_p_list_data, T_p_list = create_model("T_p_list", {"rechnr":int, "dept":int, "billno":int, "printed_line":int, "b_recid":int, "last_amount":Decimal, "last_famount":Decimal})

def ts_closeinv_btn_stopbl(t_p_list_data:[T_p_list], rec_id:int, pax:int, belegung:int):

    prepare_cache ([H_bill_line, H_bill, H_umsatz])

    h_bill_line = h_bill = h_umsatz = queasy = None

    t_p_list = hbline = None

    Hbline = create_buffer("Hbline",H_bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill_line, h_bill, h_umsatz, queasy
        nonlocal rec_id, pax, belegung
        nonlocal hbline


        nonlocal t_p_list, hbline

        return {"t-p-list": t_p_list_data}

    def del_queasy():

        nonlocal h_bill_line, h_bill, h_umsatz, queasy
        nonlocal rec_id, pax, belegung
        nonlocal hbline


        nonlocal t_p_list, hbline

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 4) & (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) & 
                 (Queasy.number2 >= 0) & (Queasy.deci2 >= 0)).order_by(Queasy._recid).with_for_update().all():
            db_session.delete(queasy)
        pass

        for t_p_list in query(t_p_list_data, filters=(lambda t_p_list: t_p_list.rechnr == h_bill.rechnr and t_p_list.dept == h_bill.departement)):
            t_p_list_data.remove(t_p_list)


    # h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    h_bill = db_session.query(H_bill).filter(
                 (H_bill._recid == rec_id)).with_for_update().first()
    # Rd 3/8/2025
    # if not avail return
    if h_bill is None:
        return generate_output()
    
    if pax != belegung:

        hbline = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)]})

        if hbline:

            # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, 0)],"departement": [(eq, h_bill.departement)],"betriebsnr": [(eq, h_bill.departement)],"datum": [(eq, hbline.bill_datum)]})
            h_umsatz = db_session.query(H_umsatz).filter(
                 (H_umsatz.artnr == 0) & (H_umsatz.departement == h_bill.departement) &
                 (H_umsatz.betriebsnr == h_bill.departement) &
                 (H_umsatz.datum == hbline.bill_datum)).with_for_update().first()
            if h_umsatz:
                h_umsatz.anzahl = h_umsatz.anzahl - h_bill.belegung + pax


                pass
        pass

        if h_bill:
            h_bill.belegung = pax
            pass
    del_queasy()

    return generate_output()