#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.rm_drecap2bl import rm_drecap2bl

def rm_drecap3bl(language_code:int, opening_date:date, from_date:date, to_date:date, fdate:date, tdate:date, segmtype_exist:bool, checked_mi_mtd:bool, checked_mi_ftd:bool, checked_mi_exchu:bool, checked_mi_exccomp:bool, long_digit:bool):
    dos_list_list = []

    output_list = dos_list = None

    output_list_list, Output_list = create_model("Output_list", {"segno":int, "flag":string, "str":string, "yroom":string, "proz3":string, "ypax":string, "yrate":string, "yrev":string, "zero_flag":bool})
    dos_list_list, Dos_list = create_model("Dos_list", {"segno":int, "flag":string, "guestsegment":string, "room":int, "proz_rm":Decimal, "mtd":int, "proz_mtd":Decimal, "ytd":int, "proz_ytd":Decimal, "pax":int, "mtd_pax":int, "ytd_pax":int, "avrg_rate":Decimal, "mtd_avrgrate":Decimal, "ytd_avrgrate":Decimal, "room_rev":Decimal, "mtd_rev":Decimal, "ytd_rev":Decimal, "zero_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dos_list_list
        nonlocal language_code, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, checked_mi_mtd, checked_mi_ftd, checked_mi_exchu, checked_mi_exccomp, long_digit


        nonlocal output_list, dos_list
        nonlocal output_list_list, dos_list_list

        return {"dos-list": dos_list_list}

    output_list_list = get_output(rm_drecap2bl(language_code, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, checked_mi_mtd, checked_mi_ftd, checked_mi_exchu, checked_mi_exccomp, long_digit))

    for output_list in query(output_list_list):
        dos_list = Dos_list()
        dos_list_list.append(dos_list)

        dos_list.segno = to_int(substring(output_list.str, 0, 3))
        dos_list.flag = output_list.flag
        dos_list.guestsegment = substring(output_list.str, 3, 16)
        dos_list.room = to_int(substring(output_list.str, 19, 3))
        dos_list.proz_rm = to_decimal(substring(output_list.str, 22, 7))
        dos_list.mtd = to_int(substring(output_list.str, 29, 6))
        dos_list.proz_mtd = to_decimal(substring(output_list.str, 35, 7))
        dos_list.ytd = to_int(output_list.yroom)
        dos_list.proz_ytd =  to_decimal(to_decimal(output_list.proz3) )
        dos_list.pax = to_int(substring(output_list.str, 42, 3))
        dos_list.mtd_pax = to_int(substring(output_list.str, 45, 6))
        dos_list.ytd_pax = to_int(output_list.ypax)
        dos_list.avrg_rate = to_decimal(substring(output_list.str, 51, 13))
        dos_list.mtd_avrgrate = to_decimal(substring(output_list.str, 64, 13))
        dos_list.ytd_avrgrate =  to_decimal(to_decimal(output_list.yrate) )
        dos_list.room_rev = to_decimal(substring(output_list.str, 77, 14))
        dos_list.mtd_rev = to_decimal(substring(output_list.str, 91, 19))
        dos_list.ytd_rev =  to_decimal(to_decimal(output_list.yrev) )
        dos_list.zero_flag = output_list.zero_flag

    return generate_output()