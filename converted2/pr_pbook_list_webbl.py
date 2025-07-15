#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_pprice, Htparam, Bediener, L_artikel, L_order, L_lieferant

payload_list_data, Payload_list = create_model("Payload_list", {"pr":string, "mode":int, "s_artnr":int})

def pr_pbook_list_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Htparam, L_lieferant])

    output_list_data = []
    q1_list_data = []
    lart_list_data = []
    l_pprice = htparam = bediener = l_artikel = l_order = l_lieferant = None

    lart_list = payload_list = output_list = q1_list = None

    lart_list_data, Lart_list = create_model("Lart_list", {"artnr":int, "bezeich":string, "traubensorte":string, "lief_einheit":Decimal})
    output_list_data, Output_list = create_model("Output_list", {"long_digit":bool})
    q1_list_data, Q1_list = create_model_like(L_pprice, {"a_firma":string, "traubensorte":string, "lief_einheit":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, q1_list_data, lart_list_data, l_pprice, htparam, bediener, l_artikel, l_order, l_lieferant


        nonlocal lart_list, payload_list, output_list, q1_list
        nonlocal lart_list_data, output_list_data, q1_list_data

        return {"output-list": output_list_data, "q1-list": q1_list_data, "lart-list": lart_list_data}

    def create_lart_list():

        nonlocal output_list_data, q1_list_data, lart_list_data, l_pprice, htparam, bediener, l_artikel, l_order, l_lieferant


        nonlocal lart_list, payload_list, output_list, q1_list
        nonlocal lart_list_data, output_list_data, q1_list_data

        usr = None
        l_artikel = None
        Usr =  create_buffer("Usr",Bediener)
        L_art =  create_buffer("L_art",L_artikel)

        l_order_obj_list = {}
        for l_order, l_artikel in db_session.query(L_order, L_art).join(L_art,(L_art.artnr == L_order.artnr)).filter(
                 (L_order.docu_nr == payload_list.pr) & (L_order.loeschflag <= 1) & (L_order.pos > 0) & (L_order.lief_nr == 0)).order_by(L_art.bezeich).all():
            if l_order_obj_list.get(l_order._recid):
                continue
            else:
                l_order_obj_list[l_order._recid] = True


            lart_list = Lart_list()
            lart_list_data.append(lart_list)

            buffer_copy(l_artikel, lart_list)


    def create_query():

        nonlocal output_list_data, q1_list_data, lart_list_data, l_pprice, htparam, bediener, l_artikel, l_order, l_lieferant


        nonlocal lart_list, payload_list, output_list, q1_list
        nonlocal lart_list_data, output_list_data, q1_list_data

        l_pprice_obj_list = {}
        for l_pprice, l_artikel, l_lieferant in db_session.query(L_pprice, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                 (L_pprice.artnr == payload_list.s_artnr)).order_by(L_pprice._recid).all():
            if l_pprice_obj_list.get(l_pprice._recid):
                continue
            else:
                l_pprice_obj_list[l_pprice._recid] = True


            q1_list = Q1_list()
            q1_list_data.append(q1_list)

            buffer_copy(l_pprice, q1_list)
            q1_list.a_firma = l_lieferant.firma
            q1_list.traubensorte = l_artikel.traubensorte
            q1_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)

    payload_list = query(payload_list_data, first=True)
    output_list = Output_list()
    output_list_data.append(output_list)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    output_list.long_digit = htparam.flogical

    if payload_list.mode == 1:
        create_lart_list()
    else:

        if payload_list.s_artnr != None:
            create_query()

    return generate_output()