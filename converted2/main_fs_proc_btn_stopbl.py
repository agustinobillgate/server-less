#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_func, B_storno

fsl_data, Fsl = create_model_like(Bk_func, {"deposit":Decimal, "limit_date":date, "deposit_payment":[Decimal,9], "payment_date":[date,9], "total_paid":Decimal, "payment_userinit":[string,9], "betriebsnr2":int, "cutoff":date, "raum":string, "grund":[string,18], "in_sales":string, "in_conv":string})

def main_fs_proc_btn_stopbl(fsl_data:[Fsl], resnr:int, resline:int, curr_gastnr:int, curr_amd:string, user_init:string):

    prepare_cache ([Bk_func])

    bstorno_data = []
    bk_func = b_storno = None

    fsl = bstorno = None

    bstorno_data, Bstorno = create_model_like(B_storno)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bstorno_data, bk_func, b_storno
        nonlocal resnr, resline, curr_gastnr, curr_amd, user_init


        nonlocal fsl, bstorno
        nonlocal bstorno_data

        return {"bstorno": bstorno_data}

    bstorno_data.clear()

    fsl = query(fsl_data, first=True)

    bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})
    pass
    bk_func.ape__getraenke[0] = fsl.ape__getraenke[0]
    bk_func.ape__getraenke[1] = fsl.ape__getraenke[1]
    bk_func.ape__getraenke[2] = fsl.ape__getraenke[2]
    bk_func.ape__getraenke[3] = fsl.ape__getraenke[3]
    bk_func.ape__getraenke[4] = fsl.ape__getraenke[4]
    bk_func.ape__getraenke[5] = fsl.ape__getraenke[5]
    bk_func.bemerkung = fsl.bemerkung
    bk_func.f_menu[0] = fsl.f_menu[0]
    bk_func.gema = fsl.gema
    bk_func.rpreis[6] = fsl.rpreis[6]
    bk_func.rpreis[7] = fsl.rpreis[7]
    bk_func.rpersonen[0] = fsl.rpersonen[0]
    bk_func.vkontrolliert = fsl.vkontrolliert
    bk_func.nadkarte[0] = fsl.nadkarte[0]
    bk_func.auf__datum = fsl.auf__datum
    bk_func.vgeschrieben = fsl.vgeschrieben
    bk_func.geschenk = fsl.geschenk


    pass

    b_storno = get_cache (B_storno, {"bankettnr": [(eq, resnr)],"breslinnr": [(eq, resline)]})

    if not b_storno:
        b_storno = B_storno()
        db_session.add(b_storno)

        b_storno.bankettnr = resnr
        b_storno.breslinnr = resline
        b_storno.gastnr = curr_gastnr
        b_storno.grund[0] = fsl.grund[0]
        b_storno.usercode = "1:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 1" + ";"
        b_storno.datum = get_current_date()


    else:

        if curr_amd == "1":

            if b_storno.grund[0] == "":
                b_storno.grund[0] = fsl.grund[0]
                b_storno.usercode = b_storno.usercode + "1:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 1" + ";"

            if b_storno.grund[0] != "":
                b_storno.grund[0] = fsl.grund[0]
                b_storno.usercode = b_storno.usercode + "1:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandment 1" + ";"
        elif curr_amd == "2":

            if b_storno.grund[1] == "":
                b_storno.grund[1] = fsl.grund[1]
                b_storno.usercode = b_storno.usercode + "2:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 2" + ";"

            elif b_storno.grund[1] != "":
                b_storno.grund[1] = fsl.grund[1]
                b_storno.usercode = b_storno.usercode + "2:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandment 2" + ";"
        elif curr_amd == "3":

            if b_storno.grund[2] == "":
                b_storno.grund[2] = fsl.grund[2]
                b_storno.usercode = b_storno.usercode + "3:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 3" + ";"

            elif b_storno.grund[2] != "":
                b_storno.grund[2] = fsl.grund[2]
                b_storno.usercode = b_storno.usercode + "3:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandment 3" + ";"
        elif curr_amd == "4":

            if b_storno.grund[3] == "":
                b_storno.grund[3] = fsl.grund[3]
                b_storno.usercode = b_storno.usercode + "4:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 4 " + ";"

            elif b_storno.grund[3] != "":
                b_storno.grund[3] = fsl.grund[3]
                b_storno.usercode = b_storno.usercode + "4:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandment 4" + ";"
        elif curr_amd == "5":

            if b_storno.grund[4] == "":
                b_storno.grund[4] = fsl.grund[4]
                b_storno.usercode = b_storno.usercode + "5:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 5" + ";"

            elif b_storno.grund[4] != "":
                b_storno.grund[4] = fsl.grund[4]
                b_storno.usercode = b_storno.usercode + "5:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandment 5" + ";"
        elif curr_amd == "6":

            if b_storno.grund[5] == "":
                b_storno.grund[5] = fsl.grund[5]
                b_storno.usercode = b_storno.usercode + "6:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 6" + ";"

            elif b_storno.grund[5] != "":
                b_storno.grund[5] = fsl.grund[5]
                b_storno.usercode = b_storno.usercode + "6:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandment 6" + ";"
        elif curr_amd == "7":

            if b_storno.grund[6] == "":
                b_storno.grund[6] = fsl.grund[6]
                b_storno.usercode = b_storno.usercode + "7:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 7" + ";"

            elif b_storno.grund[6] != "":
                b_storno.grund[6] = fsl.grund[6]
                b_storno.usercode = b_storno.usercode + "7:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandment 7" + ";". ";"
        elif curr_amd == "8":

            if b_storno.grund[7] == "":
                b_storno.grund[7] = fsl.grund[7]
                b_storno.usercode = b_storno.usercode + "8:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 8" + ";"

            elif b_storno.grund[7] != "":
                b_storno.grund[7] = fsl.grund[7]
                b_storno.usercode = b_storno.usercode + "8:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandment 8" + ";"
        elif curr_amd == "9":

            if b_storno.grund[8] == "":
                b_storno.grund[8] = fsl.grund[8]
                b_storno.usercode = b_storno.usercode + "9:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 9" + ";"

            elif b_storno.grund[8] != "":
                b_storno.grund[8] = fsl.grund[8]
                b_storno.usercode = b_storno.usercode + "9:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandment 9" + ";"
        elif curr_amd == "10":

            if b_storno.grund[9] == "":
                b_storno.grund[9] = fsl.grund[9]
                b_storno.usercode = b_storno.usercode + "10:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "New Amandment 10" + ";"

            elif b_storno.grund[9] != "":
                b_storno.grund[9] = fsl.grund[9]
                b_storno.usercode = b_storno.usercode + "10:" + user_init + ":" + to_string(get_current_date()) + ":" + to_string(get_current_time_in_seconds()) + ":" + "Change Amandement 10" + ";"

    for b_storno in db_session.query(B_storno).filter(
             (B_storno.bankettnr == resnr) & (B_storno.breslinnr == resline) & (B_storno.gastnr == curr_gastnr)).order_by(B_storno._recid).all():
        bstorno = Bstorno()
        bstorno_data.append(bstorno)

        buffer_copy(b_storno, bstorno)

    return generate_output()