#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_func, Bk_reser, Bk_rart, Bk_veran
from sqlalchemy.orm import flag_modified

fsl_data, Fsl = create_model_like(Bk_func, {"deposit":Decimal, "limit_date":date, "deposit_payment":[Decimal,9], "payment_date":[date,9], "total_paid":Decimal, "payment_userinit":[string,9], "betriebsnr2":int, "cutoff":date, "raum":string, "grund":[string,18], "in_sales":string, "in_conv":string})

def main_fs_mi_allbl(fsl_data:[Fsl], resnr:int, resline:int, q3_list_veran_nr:int, 
                     q3_list_veran_seite:int, rsvsort:int, user_init:string):

    prepare_cache ([Bk_func, Bk_reser, Bk_rart, Bk_veran])

    total_depo = to_decimal("0.0")
    bk_func = bk_reser = bk_rart = bk_veran = None

    fsl = bkfunc = bkreser = None

    Bkfunc = create_buffer("Bkfunc",Bk_func)
    Bkreser = create_buffer("Bkreser",Bk_reser)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal total_depo, bk_func, bk_reser, bk_rart, bk_veran
        nonlocal resnr, resline, q3_list_veran_nr, q3_list_veran_seite, rsvsort, user_init
        nonlocal bkfunc, bkreser
        nonlocal fsl, bkfunc, bkreser

        return {"total_depo": total_depo}

    def assign_changes():

        nonlocal total_depo, bk_func, bk_reser, bk_rart, bk_veran
        nonlocal resnr, resline, q3_list_veran_nr, q3_list_veran_seite, rsvsort, user_init
        nonlocal bkfunc, bkreser


        nonlocal fsl, bkfunc, bkreser

        bk_f = None
        Bk_f =  create_buffer("Bk_f",Bk_func)
        total_depo =  to_decimal("0")
        pass

        bk_f_obj_list = {}
        bk_f = Bk_func()
        bkreser = Bk_reser()
        for bk_f.geschenk, bk_f.vkontrolliert, bk_f.personen, bk_f.veran_nr, bk_f._recid, bk_f.rpreis, bk_f.rpersonen, bk_f.ape__getraenke, bk_f.bemerkung, bk_f.kartentext, bk_f.sonstiges, bkreser.limitdate, bkreser._recid in db_session.query(Bk_f.geschenk, Bk_f.vkontrolliert, Bk_f.personen, Bk_f.veran_nr, Bk_f._recid, Bk_f.rpreis, Bk_f.rpersonen, Bk_f.ape__getraenke, Bk_f.bemerkung, Bk_f.kartentext, Bk_f.sonstiges, Bkreser.limitdate, Bkreser._recid).join(Bkreser,(Bkreser.veran_nr == q3_list_veran_nr) & (Bkreser.veran_resnr == q3_list_veran_seite) & (Bkreser.resstatus == rsvsort)).filter(
                 (Bk_f.veran_nr == q3_list_veran_nr)).order_by(Bk_f._recid).all():
            if bk_f_obj_list.get(bk_f._recid):
                continue
            else:
                bk_f_obj_list[bk_f._recid] = True


            total_depo =  to_decimal(total_depo) + to_decimal(bk_f.rpreis[0] + (bk_f.rpersonen[0]) * to_decimal(bk_f.rpreis[6]))
            bk_func.vkontrolliert = user_init
            bk_func.geschenk = to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "hh:mm:ss")
        pass

        for bk_rart in db_session.query(Bk_rart).filter(
                 (Bk_rart.veran_nr == q3_list_veran_nr)).order_by(Bk_rart._recid).all():
            total_depo =  to_decimal(total_depo) + to_decimal(bk_rart.preis)
        fsl.geschenk = bk_func.geschenk
        fsl.vkontrolliert = bk_func.vkontrolliert
        fsl.personen = bk_func.personen

        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bk_func.veran_nr)]})

        if bk_veran:
            bk_veran.segmentcode = fsl.segmentcode
            bk_veran.payment_userinit[8] = fsl.in_sales
            bk_veran.payment_userinit[8] = bk_veran.payment_userinit[8] + chr_unicode(2) + fsl.in_conv

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)]})

        if bk_reser:
            bk_reser.limitdate = fsl.cutoff


    fsl = query(fsl_data, first=True)

    # bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})
    bk_func = db_session.query(Bk_func).filter(
             (Bk_func.veran_nr == resnr) & (Bk_func.veran_seite == resline)).with_for_update().first()

    for bkfunc in db_session.query(Bkfunc).filter(
             (Bkfunc.veran_nr == fsl.veran_nr) & (Bkfunc.veran_seite != fsl.veran_seite)).order_by(Bkfunc._recid).all():
        bkfunc.ape__getraenke[6] = fsl.ape__getraenke[6]
        bkfunc.ape__getraenke[7] = fsl.ape__getraenke[7]
        bkfunc.bemerkung = fsl.bemerkung
        bkfunc.rpreis[6] = fsl.rpreis[6]
        bkfunc.rpreis[7] = fsl.rpreis[7]
        bkfunc.rpersonen[0] = fsl.rpersonen[0]
        bkfunc.kartentext[0] = fsl.kartentext[0]
        bkfunc.kartentext[1] = fsl.kartentext[1]
        bkfunc.kartentext[2] = fsl.kartentext[2]
        bkfunc.kartentext[3] = fsl.kartentext[3]
        bkfunc.kartentext[4] = fsl.kartentext[4]
        bkfunc.kartentext[5] = fsl.kartentext[5]
        bkfunc.kartentext[6] = fsl.kartentext[6]
        bkfunc.kartentext[7] = fsl.kartentext[7]
        bkfunc.sonstiges[0] = fsl.sonstiges[0]
        bkfunc.sonstiges[1] = fsl.sonstiges[1]
        bkfunc.sonstiges[2] = fsl.sonstiges[2]
        bkfunc.sonstiges[3] = fsl.sonstiges[3]
    assign_changes()
    flag_modified(bk_func, "ape__getraenke")
    flag_modified(bk_func, "rpreis")
    flag_modified(bk_func, "rpersonen")
    flag_modified(bk_func, "kartentext")
    flag_modified(bk_func, "sonstiges")

    return generate_output()