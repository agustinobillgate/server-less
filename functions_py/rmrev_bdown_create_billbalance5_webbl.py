#------------------------------------------
# Rd, 20/8/2025
#
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.rmrev_bdown_create_billbalance5_cldbl import rmrev_bdown_create_billbalance5_cldbl
from models import Argt_line, Waehrung, Queasy

input_list_data, Input_list = create_model("Input_list", {"exc_taxserv":bool, "pvILanguage":int, "new_contrate":bool, "foreign_rate":bool, "price_decimal":int, "fdate":date, "tdate":date, "srttype":int, "id_flag":string})

def rmrev_bdown_create_billbalance5_webbl(input_list_data:[Input_list]):

    prepare_cache ([Queasy])

    cl_list_data = []
    currency_list_data = []
    sum_list_data = []
    s_list_data = []
    argt_list_data = []
    done_flag = False
    exchg_rate:Decimal = 1
    frate:Decimal = to_decimal("0.0")
    post_it:bool = False
    total_rev:Decimal = to_decimal("0.0")
    argt_line = waehrung = queasy = None

    sum_list = currency_list = cl_list = s_list = argt_list = t_argt_line = input_list = waehrung1 = cc_list = bqueasy = None

    sum_list_data, Sum_list = create_model("Sum_list", {"bezeich":string, "pax":int, "adult":int, "ch1":int, "ch2":int, "comch":int, "com":int, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "fixcost":Decimal, "t_rev":Decimal})
    currency_list_data, Currency_list = create_model("Currency_list", {"code":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"zipreis":Decimal, "localrate":Decimal, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "fixcost":Decimal, "t_rev":Decimal, "c_zipreis":string, "c_localrate":string, "c_lodging":string, "c_bfast":string, "c_lunch":string, "c_dinner":string, "c_misc":string, "c_fixcost":string, "ct_rev":string, "res_recid":int, "sleeping":bool, "row_disp":int, "flag":string, "zinr":string, "rstatus":int, "argt":string, "currency":string, "ratecode":string, "pax":int, "com":int, "ankunft":date, "abreise":date, "rechnr":int, "name":string, "ex_rate":string, "fix_rate":string, "adult":int, "ch1":int, "ch2":int, "comch":int, "age1":int, "age2":string, "rmtype":string, "resnr":int, "resname":string, "segm_desc":string, "nation":string}, {"sleeping": True})
    s_list_data, S_list = create_model("S_list", {"artnr":int, "dept":int, "bezeich":string, "curr":string, "anzahl":int, "betrag":Decimal, "l_betrag":Decimal, "f_betrag":Decimal})
    argt_list_data, Argt_list = create_model("Argt_list", {"argtnr":int, "argtcode":string, "bezeich":string, "room":int, "pax":int, "qty":int, "bfast":Decimal})
    t_argt_line_data, T_argt_line = create_model_like(Argt_line)

    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Cc_list = Cl_list
    cc_list_data = cl_list_data

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_data, currency_list_data, sum_list_data, s_list_data, argt_list_data, done_flag, exchg_rate, frate, post_it, total_rev, argt_line, waehrung, queasy
        nonlocal waehrung1, cc_list, bqueasy


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, input_list, waehrung1, cc_list, bqueasy
        nonlocal sum_list_data, currency_list_data, cl_list_data, s_list_data, argt_list_data, t_argt_line_data

        return {"cl-list": cl_list_data, "currency-list": currency_list_data, "sum-list": sum_list_data, "s-list": s_list_data, "argt-list": argt_list_data, "done_flag": done_flag}

    input_list = query(input_list_data, first=True)

    if not input_list:
        return generate_output()
        
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "RRB Period"
    queasy.number1 = 1
    queasy.char2 = input_list.id_flag


    pass
    cl_list_data, currency_list_data, sum_list_data, s_list_data, argt_list_data = get_output(rmrev_bdown_create_billbalance5_cldbl(input_list.exc_taxserv, input_list.pvILanguage, input_list.new_contrate, input_list.foreign_rate, input_list.price_decimal, input_list.fdate, input_list.tdate, input_list.srttype, input_list.id_flag))

    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "rrb period")],"char2": [(eq, input_list.id_flag)]})

    if bqueasy:
        done_flag = True
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()