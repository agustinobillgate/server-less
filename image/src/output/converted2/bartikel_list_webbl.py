#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Bk_rart, Bediener

def bartikel_list_webbl(from_cr:string, to_cr:string, curr_date:date):

    prepare_cache ([Bk_reser, Bk_rart, Bediener])

    from_i = 0
    to_i = 0
    output_list_list = []
    bk_reser = bk_rart = bediener = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"from_time":string, "to_time":string, "room":string, "rsv_no":int, "bezeich":string, "qty":int, "price":Decimal, "ba_status":string, "id":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_i, to_i, output_list_list, bk_reser, bk_rart, bediener
        nonlocal from_cr, to_cr, curr_date


        nonlocal output_list
        nonlocal output_list_list

        return {"from_i": from_i, "to_i": to_i, "output-list": output_list_list}

    def create_string():

        nonlocal from_i, to_i, output_list_list, bk_reser, bk_rart, bediener
        nonlocal from_cr, to_cr, curr_date


        nonlocal output_list
        nonlocal output_list_list

        status_chr:string = ""
        usrbuff = None
        Usrbuff =  create_buffer("Usrbuff",Bediener)

        if bk_rart.resstatus == 1:
            status_chr = "Fix"
        else:
            status_chr = "Tentative"

        usrbuff = get_cache (Bediener, {"nr": [(eq, bk_rart.setup_id)]})
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.from_time = to_string(bk_reser.von_zeit, "99:99")
        output_list.to_time = to_string(bk_reser.bis_zeit, "99:99")
        output_list.room = bk_rart.raum
        output_list.rsv_no = bk_rart.veran_nr
        output_list.bezeich = bk_rart.bezeich
        output_list.qty = bk_rart.anzahl
        output_list.price =  to_decimal(bk_rart.preis)
        output_list.ba_status = status_chr
        output_list.id = usrbuff.userinit

    output_list_list.clear()

    bk_rart_obj_list = {}
    bk_rart = Bk_rart()
    bk_reser = Bk_reser()
    for bk_rart.setup_id, bk_rart.raum, bk_rart.veran_nr, bk_rart.bezeich, bk_rart.anzahl, bk_rart.preis, bk_rart.resstatus, bk_rart._recid, bk_reser.von_zeit, bk_reser.bis_zeit, bk_reser.von_i, bk_reser.bis_i, bk_reser._recid in db_session.query(Bk_rart.setup_id, Bk_rart.raum, Bk_rart.veran_nr, Bk_rart.bezeich, Bk_rart.anzahl, Bk_rart.preis, Bk_rart.resstatus, Bk_rart._recid, Bk_reser.von_zeit, Bk_reser.bis_zeit, Bk_reser.von_i, Bk_reser.bis_i, Bk_reser._recid).join(Bk_reser,(Bk_reser.veran_nr == Bk_rart.veran_nr) & (Bk_reser.veran_resnr == Bk_rart.veran_resnr) & (Bk_reser.datum == curr_date) & (Bk_reser.resstatus <= 2)).filter(
             (Bk_rart.raum >= (from_cr).lower()) & (Bk_rart.raum <= (to_cr).lower()) & (Bk_rart.resstatus <= 2)).order_by(Bk_rart._recid).all():
        if bk_rart_obj_list.get(bk_rart._recid):
            continue
        else:
            bk_rart_obj_list[bk_rart._recid] = True


        from_i = bk_reser.von_i
        to_i = bk_reser.bis_i
        create_string()

    return generate_output()