#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser, Bk_func, Bk_rart, Bk_veran

def main_fs_assign_changesbl(resnr:int, resline:int, rsvsort:int, user_init:string, fsl_segmentcode:int, fsl_in_sales:string, fsl_in_conv:string, fsl_cutoff:date):

    prepare_cache ([Bk_reser, Bk_func, Bk_rart, Bk_veran])

    fsl_geschenk = ""
    fsl_vkontrolliert = ""
    fsl_personen = 0
    total_depo = to_decimal("0.0")
    bk_reser = bk_func = bk_rart = bk_veran = None

    bkreser = None

    Bkreser = create_buffer("Bkreser",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fsl_geschenk, fsl_vkontrolliert, fsl_personen, total_depo, bk_reser, bk_func, bk_rart, bk_veran
        nonlocal resnr, resline, rsvsort, user_init, fsl_segmentcode, fsl_in_sales, fsl_in_conv, fsl_cutoff
        nonlocal bkreser


        nonlocal bkreser

        return {"fsl_geschenk": fsl_geschenk, "fsl_vkontrolliert": fsl_vkontrolliert, "fsl_personen": fsl_personen, "total_depo": total_depo}

    def assign_changes():

        nonlocal fsl_geschenk, fsl_vkontrolliert, fsl_personen, total_depo, bk_reser, bk_func, bk_rart, bk_veran
        nonlocal resnr, resline, rsvsort, user_init, fsl_segmentcode, fsl_in_sales, fsl_in_conv, fsl_cutoff
        nonlocal bkreser


        nonlocal bkreser

        bk_f = None
        Bk_f =  create_buffer("Bk_f",Bk_func)
        total_depo =  to_decimal("0")

        bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})

        if bk_func:
            pass

            bk_f_obj_list = {}
            bk_f = Bk_func()
            bkreser = Bk_reser()
            for bk_f.veran_nr, bk_f.veran_seite, bk_f.geschenk, bk_f.vkontrolliert, bk_f.personen, bk_f._recid, bk_f.rpreis, bk_f.rpersonen, bkreser.limitdate, bkreser._recid in db_session.query(Bk_f.veran_nr, Bk_f.veran_seite, Bk_f.geschenk, Bk_f.vkontrolliert, Bk_f.personen, Bk_f._recid, Bk_f.rpreis, Bk_f.rpersonen, Bkreser.limitdate, Bkreser._recid).join(Bkreser,(Bkreser.veran_nr == bk_func.veran_nr) & (Bkreser.veran_resnr == bk_func.veran_seite) & (Bkreser.resstatus == rsvsort)).filter(
                     (Bk_f.veran_nr == bk_func.veran_nr)).order_by(Bk_f._recid).all():
                if bk_f_obj_list.get(bk_f._recid):
                    continue
                else:
                    bk_f_obj_list[bk_f._recid] = True


                total_depo =  to_decimal(total_depo) + to_decimal(bk_f.rpreis[0] + (bk_f.rpersonen[0]) * to_decimal(bk_f.rpreis[6]))
                bk_func.vkontrolliert = user_init
                bk_func.geschenk = to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "hh:mm:ss")
            pass

            for bk_rart in db_session.query(Bk_rart).filter(
                     (Bk_rart.veran_nr == bk_func.veran_nr)).order_by(Bk_rart._recid).all():
                total_depo =  to_decimal(total_depo) + to_decimal(bk_rart.preis)
            fsl_geschenk = bk_func.geschenk
            fsl_vkontrolliert = bk_func.vkontrolliert
            fsl_personen = bk_func.personen

            bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bk_func.veran_nr)]})

            if bk_veran:
                bk_veran.segmentcode = fsl_segmentcode
                bk_veran.payment_userinit[8] = fsl_in_sales
                bk_veran.payment_userinit[8] = bk_veran.payment_userinit[8] + chr_unicode(2) + fsl_in_conv

            bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)]})

            if bk_reser:
                bk_reser.limitdate = fsl_cutoff


    assign_changes()

    return generate_output()