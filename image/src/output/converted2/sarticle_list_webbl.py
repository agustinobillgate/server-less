#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, L_artikel, L_bestand

def sarticle_list_webbl(sorttype:int, last_art:string, last_art1:int, idflag:string):

    prepare_cache ([L_artikel, L_bestand])

    t_l_artikel_list = []
    counter:int = 0
    queasy = l_artikel = l_bestand = None

    t_l_artikel = bqueasy = tqueasy = None

    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"artnr":int, "bezeich":string, "masseinheit":string, "inhalt":Decimal, "traubensorte":string, "unit_price":Decimal, "lief_einheit":Decimal, "soh":Decimal})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, counter, queasy, l_artikel, l_bestand
        nonlocal sorttype, last_art, last_art1, idflag
        nonlocal bqueasy, tqueasy


        nonlocal t_l_artikel, bqueasy, tqueasy
        nonlocal t_l_artikel_list

        return {"t-l-artikel": t_l_artikel_list}

    def create_artikel():

        nonlocal t_l_artikel_list, counter, queasy, l_artikel, l_bestand
        nonlocal sorttype, last_art, last_art1, idflag
        nonlocal bqueasy, tqueasy


        nonlocal t_l_artikel, bqueasy, tqueasy
        nonlocal t_l_artikel_list


        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.masseinheit = l_artikel.masseinheit
        t_l_artikel.traubensorte = l_artikel.traubensorte
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.inhalt =  to_decimal(l_artikel.inhalt)


    def create_artikel1():

        nonlocal t_l_artikel_list, counter, queasy, l_artikel, l_bestand
        nonlocal sorttype, last_art, last_art1, idflag
        nonlocal bqueasy, tqueasy


        nonlocal t_l_artikel, bqueasy, tqueasy
        nonlocal t_l_artikel_list


        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.inhalt =  to_decimal(l_artikel.inhalt)
        t_l_artikel.masseinheit = l_artikel.masseinheit
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.traubensorte = l_artikel.traubensorte


    def create_artikel2():

        nonlocal t_l_artikel_list, counter, queasy, l_artikel, l_bestand
        nonlocal sorttype, last_art, last_art1, idflag
        nonlocal bqueasy, tqueasy


        nonlocal t_l_artikel, bqueasy, tqueasy
        nonlocal t_l_artikel_list


        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.masseinheit = l_artikel.masseinheit
        t_l_artikel.inhalt =  to_decimal(l_artikel.inhalt)
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.traubensorte = l_artikel.traubensorte

    def create_artikel3():

        nonlocal t_l_artikel_list, counter, queasy, l_artikel, l_bestand
        nonlocal sorttype, last_art, last_art1, idflag
        nonlocal bqueasy, tqueasy


        nonlocal t_l_artikel, bqueasy, tqueasy
        nonlocal t_l_artikel_list


        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.masseinheit = l_artikel.masseinheit
        t_l_artikel.inhalt =  to_decimal(l_artikel.inhalt)
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.traubensorte = l_artikel.traubensorte


        l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)]})

        if l_bestand:
            t_l_artikel.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)


    if sorttype == 1:

        if last_art1 != 0:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= last_art1)).order_by(L_artikel.artnr).all():

                if idflag.lower()  == ("quotation").lower() :
                    create_artikel1()

                elif idflag.lower()  == ("dml").lower() :
                    create_artikel2()

                elif idflag.lower()  == ("pr").lower() :
                    create_artikel3()
                else:
                    create_artikel()

        else:

            for l_artikel in db_session.query(L_artikel).order_by(L_artikel.artnr).all():

                if idflag.lower()  == ("quotation").lower() :
                    create_artikel1()

                elif idflag.lower()  == ("dml").lower() :
                    create_artikel2()

                elif idflag.lower()  == ("pr").lower() :
                    create_artikel3()
                else:
                    create_artikel()


    elif sorttype == 2:

        if substring(last_art, 0, 1) == ("*").lower() :

            for l_artikel in db_session.query(L_artikel).order_by(L_artikel.bezeich).all():

                if idflag.lower()  == ("quotation").lower() :
                    create_artikel1()

                elif idflag.lower()  == ("dml").lower() :
                    create_artikel2()

                elif idflag.lower()  == ("pr").lower() :
                    create_artikel3()
                else:
                    create_artikel()

        elif last_art.lower()  == ("ALL").lower() :

            for l_artikel in db_session.query(L_artikel).order_by(L_artikel.artnr).all():

                if idflag.lower()  == ("quotation").lower() :
                    create_artikel1()

                elif idflag.lower()  == ("dml").lower() :
                    create_artikel2()

                elif idflag.lower()  == ("pr").lower() :
                    create_artikel3()
                else:
                    create_artikel()
        else:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.bezeich >= ((last_art).lower()))).order_by(L_artikel.bezeich).all():

                if idflag.lower()  == ("quotation").lower() :
                    create_artikel1()

                elif idflag.lower()  == ("dml").lower() :
                    create_artikel2()

                elif idflag.lower()  == ("pr").lower() :
                    create_artikel3()
                else:
                    create_artikel()

    else:

        if last_art == "":

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr > last_art1)).order_by(L_artikel.artnr).all():

                if idflag.lower()  == ("quotation").lower() :
                    create_artikel1()

                elif idflag.lower()  == ("dml").lower() :
                    create_artikel2()

                elif idflag.lower()  == ("pr").lower() :
                    create_artikel3()
                else:
                    create_artikel()

        else:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.bezeich > (last_art).lower())).order_by(L_artikel.bezeich).all():

                if idflag.lower()  == ("quotation").lower() :
                    create_artikel1()

                elif idflag.lower()  == ("dml").lower() :
                    create_artikel2()

                elif idflag.lower()  == ("pr").lower() :
                    create_artikel3()
                else:
                    create_artikel()


    return generate_output()