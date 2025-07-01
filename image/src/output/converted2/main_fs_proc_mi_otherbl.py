#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_func, Bk_reser, Bk_rart

fsl_list, Fsl = create_model_like(Bk_func, {"deposit":Decimal, "limit_date":date, "deposit_payment":[Decimal,9], "payment_date":[date,9], "total_paid":Decimal, "payment_userinit":[string,9], "betriebsnr2":int, "cutoff":date, "raum":string, "grund":[string,18], "in_sales":string, "in_conv":string})

def main_fs_proc_mi_otherbl(fsl_list:[Fsl], oresnr:int, oresline:int, rsvsort:int, user_init:string):

    prepare_cache ([Bk_func, Bk_rart])

    total_depo = to_decimal("0.0")
    bk_func = bk_reser = bk_rart = None

    fsl = bkfunc = bkreser = None

    Bkfunc = create_buffer("Bkfunc",Bk_func)
    Bkreser = create_buffer("Bkreser",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal total_depo, bk_func, bk_reser, bk_rart
        nonlocal oresnr, oresline, rsvsort, user_init
        nonlocal bkfunc, bkreser


        nonlocal fsl, bkfunc, bkreser

        return {"total_depo": total_depo}

    fsl = query(fsl_list, first=True)

    bkfunc = get_cache (Bk_func, {"veran_nr": [(eq, oresnr)],"veran_seite": [(eq, oresline)]})

    if bkfunc:
        pass
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
        bkfunc.f_menu[0] = fsl.f_menu[0]
        bkfunc.gema = fsl.gema
        bkfunc.weine[0] = fsl.weine[0]
        bkfunc.weine[1] = fsl.weine[1]
        bkfunc.weine[2] = fsl.weine[2]
        bkfunc.weine[3] = fsl.weine[3]
        bkfunc.weine[4] = fsl.weine[4]
        bkfunc.weine[5] = fsl.weine[5]
        bkfunc.menue[0] = fsl.menue[0]
        bkfunc.menue[1] = fsl.menue[1]
        bkfunc.menue[2] = fsl.menue[2]
        bkfunc.menue[3] = fsl.menue[3]
        bkfunc.menue[4] = fsl.menue[4]
        bkfunc.menue[5] = fsl.menue[5]
        bkfunc.vkontrolliert = user_init
        bkfunc.geschenk = to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "hh:mm:ss")
        pass

        bkfunc_obj_list = {}
        for bkfunc, bkreser in db_session.query(Bkfunc, Bkreser).join(Bkreser,(Bkreser.veran_nr == oresnr) & (Bkreser.veran_resnr == Bkfunc.veran_seite) & (Bkreser.resstatus == rsvsort)).filter(
                 (Bkfunc.veran_nr == oresnr)).order_by(Bkfunc._recid).all():
            if bkfunc_obj_list.get(bkfunc._recid):
                continue
            else:
                bkfunc_obj_list[bkfunc._recid] = True


            total_depo =  to_decimal(total_depo) + to_decimal(bkfunc.rpreis[0] + (bkfunc.rpersonen[0]) * to_decimal(bkfunc.rpreis[6]))

        bk_rart_obj_list = {}
        for bk_rart, bkreser in db_session.query(Bk_rart, Bkreser).join(Bkreser,(Bkreser.veran_nr == oresnr) & (Bkreser.veran_resnr == Bk_rart.veran_seite) & (Bkreser.resstatus == rsvsort)).filter(
                 (Bk_rart.veran_nr == oresnr)).order_by(Bk_rart._recid).all():
            if bk_rart_obj_list.get(bk_rart._recid):
                continue
            else:
                bk_rart_obj_list[bk_rart._recid] = True


            total_depo =  to_decimal(total_depo) + to_decimal(bk_rart.preis)

    return generate_output()