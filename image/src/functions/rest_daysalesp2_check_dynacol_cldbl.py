from functions.additional_functions import *
import decimal
from models import Htparam

def rest_daysalesp2_check_dynacol_cldbl(buf_art:[Buf_art], art_str:str, htl_dept_dptnr:int):
    anzahl = 0
    artnr_list = 0
    bezeich = ""
    show_option = False
    i:int = 0
    qty:int = 0
    counter:int = 0
    artnr_data:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    disc_art1:int = -1
    disc_art2:int = -1
    disc_art3:int = -1
    htparam = None

    buf_art = t_artnr = None

    buf_art_list, Buf_art = create_model("Buf_art", {"artnr":int, "bezeich":str, "departement":int})
    t_artnr_list, T_artnr = create_model("T_artnr", {"nr":int, "artnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl, artnr_list, bezeich, show_option, i, qty, counter, artnr_data, disc_art1, disc_art2, disc_art3, htparam


        nonlocal buf_art, t_artnr
        nonlocal buf_art_list, t_artnr_list
        return {"anzahl": anzahl, "artnr_list": artnr_list, "bezeich": bezeich, "show_option": show_option}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 556)).first()

    if htparam.finteger > 0:
        disc_art3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()

    if htparam.finteger > 0:
        disc_art1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 596)).first()

    if htparam.finteger > 0:
        disc_art2 = htparam.finteger
    t_artnr_list.clear()
    for i in range(1,num_entries(art_str, ",")  + 1) :

        if i > 21:
            pass
        else:
            artnr_data[i - 1] = to_int(entry(i - 1, art_str, ","))

            if artnr_data[i - 1] == disc_art2 or artnr_data[i - 1] == disc_art3:
                show_option = True

            if artnr_data[i - 1] != 0:
                qty = qty + 1
    for i in range(1,qty + 1) :

        buf_art = query(buf_art_list, filters=(lambda buf_art :buf_art.artnr == artnr_data[i - 1] and buf_art.departement == htl_dept_dptnr), first=True)

        if buf_art:
            counter = counter + 1
            t_artnr = T_artnr()
            t_artnr_list.append(t_artnr)

            t_artnr.nr = counter
            t_artnr.artnr = buf_art.artnr
    anzahl = counter

    for t_artnr in query(t_artnr_list):
        artnr_list[t_artnr.nr - 1] = t_artnr.artnr
    for i in range(1,anzahl + 1) :

        buf_art = query(buf_art_list, filters=(lambda buf_art :buf_art.artnr == artnr_list[i - 1] and buf_art.departement == htl_dept_dptnr), first=True)

        if buf_art:
            bezeich[i - 1] = buf_art.bezeich

    return generate_output()