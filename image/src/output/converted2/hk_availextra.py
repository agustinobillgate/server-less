#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.hk_availextrabl import hk_availextrabl
from functions.read_artikelbl import read_artikelbl
from models import Paramtext, Htparam, Artikel, Printer, Printcod

def hk_availextra(fdate:date, tdate:date, artnr:int, sorttype:int, language_code:int):
    msgstr = ""
    disp_table_list = []
    cdate:date = None
    paramtext = htparam = artikel = printer = printcod = None

    t_paramtext = t_htparam = t_artikel = t_printer = t_printcod = tmp_extra = disp_table = temp_art = None

    t_paramtext_list, T_paramtext = create_model_like(Paramtext)
    t_htparam_list, T_htparam = create_model_like(Htparam)
    t_artikel_list, T_artikel = create_model_like(Artikel)
    t_printer_list, T_printer = create_model_like(Printer)
    t_printcod_list, T_printcod = create_model_like(Printcod)
    tmp_extra_list, Tmp_extra = create_model("Tmp_extra", {"reihe":int, "typ_pos":string, "pos_from":string, "cdate":date, "room":string, "qty":int, "rsvno":int})
    disp_table_list, Disp_table = create_model("Disp_table", {"reihe":int, "str_typ":string, "str1":string, "str2":string, "str3":string, "str5":string, "str6":string})
    temp_art_list, Temp_art = create_model("Temp_art", {"art_nr":int, "art_nm":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msgstr, disp_table_list, cdate, paramtext, htparam, artikel, printer, printcod
        nonlocal fdate, tdate, artnr, sorttype, language_code


        nonlocal t_paramtext, t_htparam, t_artikel, t_printer, t_printcod, tmp_extra, disp_table, temp_art
        nonlocal t_paramtext_list, t_htparam_list, t_artikel_list, t_printer_list, t_printcod_list, tmp_extra_list, disp_table_list, temp_art_list

        return {"msgstr": msgstr, "disp-table": disp_table_list}

    def disp_detail():

        nonlocal msgstr, disp_table_list, cdate, paramtext, htparam, artikel, printer, printcod
        nonlocal fdate, tdate, artnr, sorttype, language_code


        nonlocal t_paramtext, t_htparam, t_artikel, t_printer, t_printcod, tmp_extra, disp_table, temp_art
        nonlocal t_paramtext_list, t_htparam_list, t_artikel_list, t_printer_list, t_printcod_list, tmp_extra_list, disp_table_list, temp_art_list

        tot_used:int = 0
        ndate:date = None
        art_qty:int = 0
        art_qty1:int = 0
        up_str3:int = 0
        fart:string = ""
        flabel:string = ""
        str1:string = ""
        ndate = fdate
        t_artikel_list = get_output(read_artikelbl(artnr, 0, ""))

        t_artikel = query(t_artikel_list, first=True)

        if t_artikel:
            art_qty = t_artikel.anzahl
        art_qty1 = art_qty
        while ndate <= tdate :

            tmp_extra = query(tmp_extra_list, filters=(lambda tmp_extra: tmp_extra.cdate == ndate), first=True)

            if tmp_extra:

                for tmp_extra in query(tmp_extra_list, filters=(lambda tmp_extra: tmp_extra.cdate == ndate), sort_by=[("reihe",False),("room",False)]):
                    tot_used = tot_used + tmp_extra.qty

                    disp_table = query(disp_table_list, filters=(lambda disp_table: disp_table.str1 == to_string(ndate , "99/99/9999") and disp_table.str2 == tmp_extra.room), first=True)

                    if disp_table:
                        up_str3 = int (disp_table.str3) + tmp_extra.qty
                        disp_table.str1 = to_string(ndate , "99/99/9999")
                        disp_table.str2 = tmp_extra.room
                        disp_table.str3 = to_string(up_str3)
                        disp_table.str5 = to_string(art_qty - up_str3)
                        disp_table.str6 = to_string(tmp_extra.rsvno)


                    else:
                        art_qty1 = art_qty1 - tmp_extra.qty
                        disp_table = Disp_table()
                        disp_table_list.append(disp_table)

                        disp_table.reihe = tmp_extra.reihe
                        disp_table.str1 = to_string(ndate , "99/99/9999")
                        disp_table.str2 = tmp_extra.room
                        disp_table.str3 = to_string(tmp_extra.qty)
                        disp_table.str5 = to_string(art_qty1)
                        disp_table.str6 = to_string(tmp_extra.rsvno)


                disp_table = Disp_table()
                disp_table_list.append(disp_table)

                disp_table.str1 = ""
                disp_table.str2 = "Total"
                disp_table.str3 = to_string(tot_used)
                disp_table.str5 = to_string(art_qty - tot_used)


                disp_table = Disp_table()
                disp_table_list.append(disp_table)

                disp_table.str1 = ""
                disp_table.str2 = ""
                disp_table.str3 = ""
                disp_table.str5 = ""
                disp_table.str6 = ""


            else:
                disp_table = Disp_table()
                disp_table_list.append(disp_table)

                disp_table.str1 = to_string(ndate , "99/99/9999")
                disp_table.str2 = ""
                disp_table.str3 = ""
                disp_table.str5 = to_string(art_qty)


                disp_table = Disp_table()
                disp_table_list.append(disp_table)

                disp_table.str1 = ""
                disp_table.str2 = "Total"
                disp_table.str3 = to_string(tot_used)
                disp_table.str5 = to_string(art_qty)


                disp_table = Disp_table()
                disp_table_list.append(disp_table)

                disp_table.str1 = ""
                disp_table.str2 = ""
                disp_table.str3 = ""
                disp_table.str5 = ""
                disp_table.str6 = ""


            art_qty1 = art_qty
            up_str3 = 0
            tot_used = 0
            ndate = ndate + timedelta(days=1)


    def disp_summary():

        nonlocal msgstr, disp_table_list, cdate, paramtext, htparam, artikel, printer, printcod
        nonlocal fdate, tdate, artnr, sorttype, language_code


        nonlocal t_paramtext, t_htparam, t_artikel, t_printer, t_printcod, tmp_extra, disp_table, temp_art
        nonlocal t_paramtext_list, t_htparam_list, t_artikel_list, t_printer_list, t_printcod_list, tmp_extra_list, disp_table_list, temp_art_list

        tot_used:int = 0
        ndate:date = None
        art_qty:int = 0
        fart:string = ""
        flabel:string = ""
        str1:string = ""
        ndate = fdate
        t_artikel_list = get_output(read_artikelbl(artnr, 0, ""))

        t_artikel = query(t_artikel_list, first=True)

        if t_artikel:
            art_qty = t_artikel.anzahl
        while ndate <= tdate :

            for tmp_extra in query(tmp_extra_list, filters=(lambda tmp_extra: tmp_extra.cdate == ndate and tmp_extra.qty != 0)):
                tot_used = tot_used + tmp_extra.qty
            disp_table = Disp_table()
            disp_table_list.append(disp_table)

            disp_table.str1 = to_string(ndate , "99/99/99")
            disp_table.str2 = ""
            disp_table.str3 = to_string(tot_used)
            disp_table.str5 = to_string(art_qty - tot_used)
            disp_table.str6 = ""


            tot_used = 0
            ndate = ndate + timedelta(days=1)

    if fdate > tdate:
        msgstr = "From Date can not be greater than To Date"

        return generate_output()
    else:

        if artnr == 0:
            msgstr = "Article For not yet define."

            return generate_output()
        else:
            tmp_extra_list = get_output(hk_availextrabl(language_code, artnr, fdate, tdate))

            if sorttype == 1:
                disp_detail()
            else:
                disp_summary()

    return generate_output()