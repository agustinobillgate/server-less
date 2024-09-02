from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from sqlalchemy import func
from functions.calculate_occupied_roomsbl import calculate_occupied_roomsbl
from models import Queasy, Paramtext, Pricecod, Zimkateg, Zimmer, Prmarket, Ratecode

def res_zimkateg1bl(datum:date, origcode:str, prcode:str, curr_marknr:int):
    s_list_list = []
    new_contrate:bool = False
    csetup_array:str = ""
    isetup_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    anz_setup:int = 0
    ci_date:date = None
    global_occ:bool = False
    i_param439:int = 0
    queasy = paramtext = pricecod = zimkateg = zimmer = prmarket = ratecode = None

    s_list = dynarate_list = dybuff = None

    s_list_list, S_list = create_model("S_list", {"zikatnr":int, "kurzbez":str, "bezeichnung":str, "reihenfolge":int, "flag":int, "marknr":int, "market":str, "contcode":str, "kurzbez1":str, "setup":str, "nr":int})
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rmtype":str, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":str, "dynacode":str})

    Dybuff = Dynarate_list
    dybuff_list = dynarate_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal dybuff


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_list, dynarate_list_list
        return {"s-list": s_list_list}

    def get_bedsetup():

        nonlocal s_list_list, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal dybuff


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_list, dynarate_list_list

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():

            if paramtext.notes != "":
                anz_setup = anz_setup + 1
                csetup_array[anz_setup - 1] = substring(notes, 0, 1)
                isetup_array[anz_setup - 1] = paramtext.txtnr - 9200

    def create_list():

        nonlocal s_list_list, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal dybuff


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_list, dynarate_list_list

        i:int = 0

        for pricecod in db_session.query(Pricecod).filter(
                (func.lower(Pricecod.code) == (prcode).lower())).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == pricecod.zikatnr)).first()

            if zimkateg:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.marknr == pricecod.marknr and s_list.zikatnr == zimkateg.zikatnr and s_list.contcode.lower()  == (prcode).lower()), first=True)

                if not s_list:

                    if anz_setup > 0:

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == 0)).first()

                        if zimmer:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.contcode = prcode
                            s_list.zikatnr = zimkateg.zikatnr
                            s_list.kurzbez = zimkateg.kurzbez
                            s_list.kurzbez1 = zimkateg.kurzbez
                            s_list.bezeichnung = zimkateg.bezeichnung
                            s_list.marknr = pricecod.marknr

                            prmarket = db_session.query(Prmarket).filter(
                                    (Prmarket.nr == pricecod.marknr)).first()

                            if prmarket:
                                s_list.market = prmarket.bezeich
                        for i in range(1,anz_setup + 1) :

                            paramtext = db_session.query(Paramtext).filter(
                                    (Paramtext.txtnr == (isetup_array[i - 1] + 9200))).first()

                            zimmer = db_session.query(Zimmer).filter(
                                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == isetup_array[i - 1])).first()

                            if zimmer:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.contcode = prcode
                                s_list.zikatnr = zimkateg.zikatnr
                                s_list.kurzbez = zimkateg.kurzbez
                                s_list.kurzbez1 = zimkateg.kurzbez +\
                                        substring(paramtext.notes, 0, 1)
                                s_list.bezeichnung = zimkateg.bezeichnung
                                s_list.marknr = pricecod.marknr
                                s_list.setup = paramtext.ptexte
                                s_list.nr = i

                                prmarket = db_session.query(Prmarket).filter(
                                        (Prmarket.nr == pricecod.marknr)).first()

                                if prmarket:
                                    s_list.market = prmarket.bezeich
                    else:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.contcode = prcode
                        s_list.zikatnr = zimkateg.zikatnr
                        s_list.kurzbez = zimkateg.kurzbez
                        s_list.kurzbez1 = zimkateg.kurzbez
                        s_list.bezeichnung = zimkateg.bezeichnung
                        s_list.marknr = pricecod.marknr

                        prmarket = db_session.query(Prmarket).filter(
                                (Prmarket.nr == pricecod.marknr)).first()

                        if prmarket:
                            s_list.market = prmarket.bezeich

        for zimkateg in db_session.query(Zimkateg).all():

            s_list = query(s_list_list, filters=(lambda s_list :s_list.zikatnr == zimkateg.zikatnr), first=True)

            if not s_list:

                if anz_setup > 0:

                    zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == 0)).first()

                    if zimmer:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.zikatnr = zimkateg.zikatnr
                        s_list.kurzbez = zimkateg.kurzbez
                        s_list.kurzbez1 = zimkateg.kurzbez
                        s_list.bezeichnung = zimkateg.bezeichnung
                        s_list.flag = 1


                    for i in range(1,anz_setup + 1) :

                        paramtext = db_session.query(Paramtext).filter(
                                (Paramtext.txtnr == (isetup_array[i - 1] + 9200))).first()

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == isetup_array[i - 1])).first()

                        if zimmer:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.zikatnr = zimkateg.zikatnr
                            s_list.kurzbez = zimkateg.kurzbez
                            s_list.kurzbez1 = zimkateg.kurzbez +\
                                    substring(paramtext.notes, 0, 1)
                            s_list.bezeichnung = zimkateg.bezeichnung
                            s_list.setup = paramtext.ptexte
                            s_list.nr = i
                            s_list.flag = 1


                else:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.zikatnr = zimkateg.zikatnr
                    s_list.kurzbez = zimkateg.kurzbez
                    s_list.kurzbez1 = zimkateg.kurzbez
                    s_list.bezeichnung = zimkateg.bezeichnung
                    s_list.flag = 1

        if curr_marknr != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.marknr == curr_marknr)):
                s_list.reihenfolge = curr_marknr


    def new_create_list():

        nonlocal s_list_list, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal dybuff


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_list, dynarate_list_list

        i:int = 0

        for ratecode in db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower())).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == ratecode.zikatnr)).first()

            if zimkateg:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.marknr == ratecode.marknr and s_list.zikatnr == zimkateg.zikatnr and s_list.contcode.lower()  == (prcode).lower()), first=True)

                if not s_list:

                    if anz_setup > 0:

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == 0)).first()

                        if zimmer:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            buffer_copy(zimkateg, s_list)
                            s_list.contcode = prcode
                            s_list.kurzbez1 = zimkateg.kurzbez
                            s_list.marknr = ratecode.marknr

                            prmarket = db_session.query(Prmarket).filter(
                                    (Prmarket.nr == ratecode.marknr)).first()

                            if prmarket:
                                s_list.market = prmarket.bezeich
                        for i in range(1,anz_setup + 1) :

                            paramtext = db_session.query(Paramtext).filter(
                                    (Paramtext.txtnr == (isetup_array[i - 1] + 9200))).first()

                            zimmer = db_session.query(Zimmer).filter(
                                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == isetup_array[i - 1])).first()

                            if zimmer:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                buffer_copy(zimkateg, s_list)
                                s_list.contcode = prcode
                                s_list.kurzbez1 = zimkateg.kurzbez +\
                                        substring(paramtext.notes, 0, 1)
                                s_list.marknr = ratecode.marknr
                                s_list.setup = paramtext.ptexte
                                s_list.nr = i

                                prmarket = db_session.query(Prmarket).filter(
                                        (Prmarket.nr == ratecode.marknr)).first()

                                if prmarket:
                                    s_list.market = prmarket.bezeich
                    else:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        buffer_copy(zimkateg, s_list)
                        s_list.contcode = prcode
                        s_list.kurzbez1 = zimkateg.kurzbez
                        s_list.marknr = ratecode.marknr

                        prmarket = db_session.query(Prmarket).filter(
                                (Prmarket.nr == ratecode.marknr)).first()

                        if prmarket:
                            s_list.market = prmarket.bezeich

        for zimkateg in db_session.query(Zimkateg).all():

            s_list = query(s_list_list, filters=(lambda s_list :s_list.zikatnr == zimkateg.zikatnr), first=True)

            if not s_list:

                if anz_setup > 0:

                    zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == 0)).first()

                    if zimmer:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        buffer_copy(zimkateg, s_list)
                        s_list.kurzbez1 = zimkateg.kurzbez
                        s_list.flag = 1


                    for i in range(1,anz_setup + 1) :

                        paramtext = db_session.query(Paramtext).filter(
                                (Paramtext.txtnr == (isetup_array[i - 1] + 9200))).first()

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == isetup_array[i - 1])).first()

                        if zimmer:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            buffer_copy(zimkateg, s_list)
                            s_list.kurzbez1 = zimkateg.kurzbez +\
                                    substring(paramtext.notes, 0, 1)
                            s_list.setup = paramtext.ptexte
                            s_list.nr = i
                            s_list.flag = 1


                else:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    buffer_copy(zimkateg, s_list)
                    s_list.kurzbez1 = zimkateg.kurzbez
                    s_list.flag = 1

        if curr_marknr != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.marknr == curr_marknr)):
                s_list.reihenfolge = curr_marknr


    def create_dynarate_list():

        nonlocal s_list_list, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal dybuff


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_list, dynarate_list_list

        i:int = 0
        tokcounter:int = 0
        iftask:str = ""
        mestoken:str = ""
        mesvalue:str = ""
        mapcode:str = ""
        occ_rooms:int = 0
        use_it:bool = False
        Dybuff = Dynarate_list

        for ratecode in db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower())).all():
            dynarate_list = Dynarate_list()
            dynarate_list_list.append(dynarate_list)

            iftask = ratecode.char1[4]
            for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                if mestoken == "CN":
                    dynarate_list.counter = to_int(mesvalue)
                elif mestoken == "RT":
                    dynaRate_list.rmType = mesvalue
                elif mestoken == "WD":
                    dynarate_list.w_day = to_int(mesvalue)
                elif mestoken == "FR":
                    dynaRate_list.fr_room = to_int(mesvalue)
                elif mestoken == "TR":
                    dynaRate_list.to_room = to_int(mesvalue)
                elif mestoken == "D1":
                    dynaRate_list.days1 = to_int(mesvalue)
                elif mestoken == "D2":
                    dynaRate_list.days2 = to_int(mesvalue)
                elif mestoken == "RC":
                    dynaRate_list.rCode = mesvalue


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (Queasy.char1 == origcode)).first()

    if not queasy:

        return generate_output()
    i_param439 = get_output(htpint(439))
    ci_date = get_output(htpdate(87))
    new_contrate = get_output(htplogic(550))
    get_bedsetup()

    if new_contrate:

        if queasy.logi2:
            prcode = origcode
            create_dynarate_list()
        else:
            new_create_list()
    else:
        create_list()

    dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list :dynarate_list.rmtype.lower()  == "*"), first=True)
    global_occ = None != dynarate_list and i_param439 == 1

    if global_occ:

        for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list :dynarate_list.rmtype.lower()  != "*")):
            dynarate_list_list.remove(dynarate_list)

    else:

        for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list :dynarate_list.rmtype.lower()  == "*")):
            dynarate_list_list.remove(dynarate_list)


    for dynarate_list in query(dynarate_list_list):
        occ_rooms = get_output(calculate_occupied_roomsbl(datum, dynaRate_list.rmType, global_occ))
        use_it = True

        if dynaRate_list.days1 != 0 and (datum - ci_date) <= dynaRate_list.days1:
            use_it = False

        if use_it and dynaRate_list.days2 != 0 and (datum - ci_date) >= dynaRate_list.days2:
            use_it = False

        if use_it:
            use_it = (dynaRate_list.fr_room <= occ_rooms) and (dynaRate_list.to_room >= occ_rooms)

        if not use_it:
            dynarate_list_list.remove(dynarate_list)

        elif (dynaRate_list.days1 != 0) or (dynaRate_list.days2 != 0):

            for dybuff in query(dybuff_list, filters=(lambda dybuff :dybuff.days1 == 0 and dybuff.days2 == 0 and (dybuff.rmtype == dynaRate_list.rmtype) and (dybuff.fr_room <= occ_rooms) and (dybuff.to_room >= occ_rooms))):
                dybuff_list.remove(dybuff)


    if global_occ:

        for dynarate_list in query(dynarate_list_list):

            for ratecode in db_session.query(Ratecode).filter(
                    (Ratecode.CODE == dynaRate_list.rcode) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum)).all():

                if curr_marknr == 0:
                    use_it = True
                else:
                    use_it = (ratecode.marknr == curr_marknr)

                if use_it:

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == ratecode.zikatnr)).first()
                    mapcode = ratecode.CODE

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 145) &  (Queasy.char1 == origcode) &  (func.lower(Queasy.char2) == (mapcode).lower()) &  (Queasy.number1 == 0) &  (Queasy.deci1 == dynarate_list.w_day) &  (Queasy.deci2 == dynarate_list.counter) &  (Queasy.date1 == datum)).first()

                    if queasy:
                        mapcode = queasy.char3

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.marknr == ratecode.marknr and s_list.zikatnr == zimkateg.zikatnr and s_list.contcode.lower()  == (mapcode).lower()), first=True)

                    if not s_list:

                        if anz_setup > 0:

                            zimmer = db_session.query(Zimmer).filter(
                                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == 0)).first()

                            if zimmer:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                buffer_copy(zimkateg, s_list)
                                s_list.contcode = mapcode
                                s_list.kurzbez1 = zimkateg.kurzbez
                                s_list.marknr = ratecode.marknr

                                prmarket = db_session.query(Prmarket).filter(
                                        (Prmarket.nr == ratecode.marknr)).first()

                                if prmarket:
                                    s_list.market = prmarket.bezeich
                            for i in range(1,anz_setup + 1) :

                                paramtext = db_session.query(Paramtext).filter(
                                        (Paramtext.txtnr == (isetup_array[i - 1] + 9200))).first()

                                zimmer = db_session.query(Zimmer).filter(
                                        (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == isetup_array[i - 1])).first()

                                if zimmer:
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    buffer_copy(zimkateg, s_list)
                                    s_list.contcode = mapcode
                                    s_list.kurzbez1 = zimkateg.kurzbez +\
                                            substring(paramtext.notes, 0, 1)
                                    s_list.marknr = ratecode.marknr
                                    s_list.setup = paramtext.ptexte
                                    s_list.nr = i

                                    prmarket = db_session.query(Prmarket).filter(
                                            (Prmarket.nr == ratecode.marknr)).first()

                                    if prmarket:
                                        s_list.market = prmarket.bezeich
                        else:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            buffer_copy(zimkateg, s_list)
                            s_list.contcode = mapcode
                            s_list.kurzbez1 = zimkateg.kurzbez
                            s_list.marknr = ratecode.marknr

                            prmarket = db_session.query(Prmarket).filter(
                                    (Prmarket.nr == ratecode.marknr)).first()

                            if prmarket:
                                s_list.market = prmarket.bezeich

    else:

        for dynarate_list in query(dynarate_list_list):

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.CODE == dynaRate_list.rcode)).first()

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.kurzbez == dynaRate_list.rmtype)).first()

            if zimkateg:
                mapcode = ratecode.CODE

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 145) &  (Queasy.char1 == origcode) &  (func.lower(Queasy.char2) == (mapcode).lower()) &  (Queasy.number1 == zimkateg.zikatnr) &  (Queasy.deci1 == dynarate_list.w_day) &  (Queasy.deci2 == dynarate_list.counter) &  (Queasy.date1 == datum)).first()

                if queasy:
                    mapcode = queasy.char3

                s_list = query(s_list_list, filters=(lambda s_list :s_list.marknr == ratecode.marknr and s_list.zikatnr == zimkateg.zikatnr and s_list.contcode.lower()  == (mapcode).lower()), first=True)

                if not s_list:

                    if anz_setup > 0:

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == 0)).first()

                        if zimmer:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            buffer_copy(zimkateg, s_list)
                            s_list.contcode = mapcode
                            s_list.kurzbez1 = zimkateg.kurzbez
                            s_list.marknr = ratecode.marknr

                            prmarket = db_session.query(Prmarket).filter(
                                    (Prmarket.nr == ratecode.marknr)).first()

                            if prmarket:
                                s_list.market = prmarket.bezeich
                        for i in range(1,anz_setup + 1) :

                            paramtext = db_session.query(Paramtext).filter(
                                    (Paramtext.txtnr == (isetup_array[i - 1] + 9200))).first()

                            zimmer = db_session.query(Zimmer).filter(
                                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == isetup_array[i - 1])).first()

                            if zimmer:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                buffer_copy(zimkateg, s_list)
                                s_list.contcode = mapcode
                                s_list.kurzbez1 = zimkateg.kurzbez +\
                                        substring(paramtext.notes, 0, 1)
                                s_list.marknr = ratecode.marknr
                                s_list.setup = paramtext.ptexte
                                s_list.nr = i

                                prmarket = db_session.query(Prmarket).filter(
                                        (Prmarket.nr == ratecode.marknr)).first()

                                if prmarket:
                                    s_list.market = prmarket.bezeich
                    else:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        buffer_copy(zimkateg, s_list)
                        s_list.contcode = mapcode
                        s_list.kurzbez1 = zimkateg.kurzbez
                        s_list.marknr = ratecode.marknr

                        prmarket = db_session.query(Prmarket).filter(
                                (Prmarket.nr == ratecode.marknr)).first()

                        if prmarket:
                            s_list.market = prmarket.bezeich


    if curr_marknr != 0:

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.marknr == curr_marknr)):
            s_list.reihenfolge = curr_marknr


    return generate_output()