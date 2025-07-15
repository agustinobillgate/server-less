#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from functions.calculate_occupied_roomsbl import calculate_occupied_roomsbl
from models import Queasy, Paramtext, Pricecod, Zimkateg, Zimmer, Prmarket, Ratecode

def res_zimkateg1bl(datum:date, origcode:string, prcode:string, curr_marknr:int):

    prepare_cache ([Queasy, Paramtext, Pricecod, Prmarket, Ratecode])

    s_list_data = []
    new_contrate:bool = False
    csetup_array:List[string] = create_empty_list(99,"")
    isetup_array:List[int] = create_empty_list(99,0)
    anz_setup:int = 0
    ci_date:date = None
    global_occ:bool = False
    i_param439:int = 0
    queasy = paramtext = pricecod = zimkateg = zimmer = prmarket = ratecode = None

    s_list = dynarate_list = dybuff = None

    s_list_data, S_list = create_model("S_list", {"zikatnr":int, "kurzbez":string, "bezeichnung":string, "reihenfolge":int, "flag":int, "marknr":int, "market":string, "contcode":string, "kurzbez1":string, "setup":string, "nr":int})
    dynarate_list_data, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rmtype":string, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":string, "dynacode":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_data, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal datum, origcode, prcode, curr_marknr


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_data, dynarate_list_data

        return {"prcode": prcode, "s-list": s_list_data}

    def get_bedsetup():

        nonlocal s_list_data, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal datum, origcode, prcode, curr_marknr


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_data, dynarate_list_data

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext.txtnr).all():

            if paramtext.notes != "":
                anz_setup = anz_setup + 1
                csetup_array[anz_setup - 1] = substring(notes, 0, 1)
                isetup_array[anz_setup - 1] = paramtext.txtnr - 9200


    def create_list():

        nonlocal s_list_data, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal datum, origcode, prcode, curr_marknr


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_data, dynarate_list_data

        i:int = 0

        for pricecod in db_session.query(Pricecod).filter(
                 (Pricecod.code == (prcode).lower())).order_by(Pricecod._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, pricecod.zikatnr)]})

            if zimkateg:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.marknr == pricecod.marknr and s_list.zikatnr == zimkateg.zikatnr and s_list.contcode.lower()  == (prcode).lower()), first=True)

                if not s_list:

                    if anz_setup > 0:

                        zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, 0)]})

                        if zimmer:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.contcode = prcode
                            s_list.zikatnr = zimkateg.zikatnr
                            s_list.kurzbez = zimkateg.kurzbez
                            s_list.kurzbez1 = zimkateg.kurzbez
                            s_list.bezeichnung = zimkateg.bezeichnung
                            s_list.marknr = pricecod.marknr

                            prmarket = get_cache (Prmarket, {"nr": [(eq, pricecod.marknr)]})

                            if prmarket:
                                s_list.market = prmarket.bezeich
                        for i in range(1,anz_setup + 1) :

                            paramtext = get_cache (Paramtext, {"txtnr": [(eq, (isetup_array[i - 1] + 9200))]})

                            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, isetup_array[i - 1])]})

                            if zimmer:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.contcode = prcode
                                s_list.zikatnr = zimkateg.zikatnr
                                s_list.kurzbez = zimkateg.kurzbez
                                s_list.kurzbez1 = zimkateg.kurzbez +\
                                        substring(paramtext.notes, 0, 1)
                                s_list.bezeichnung = zimkateg.bezeichnung
                                s_list.marknr = pricecod.marknr
                                s_list.setup = paramtext.ptexte
                                s_list.nr = i

                                prmarket = get_cache (Prmarket, {"nr": [(eq, pricecod.marknr)]})

                                if prmarket:
                                    s_list.market = prmarket.bezeich
                    else:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.contcode = prcode
                        s_list.zikatnr = zimkateg.zikatnr
                        s_list.kurzbez = zimkateg.kurzbez
                        s_list.kurzbez1 = zimkateg.kurzbez
                        s_list.bezeichnung = zimkateg.bezeichnung
                        s_list.marknr = pricecod.marknr

                        prmarket = get_cache (Prmarket, {"nr": [(eq, pricecod.marknr)]})

                        if prmarket:
                            s_list.market = prmarket.bezeich

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

            s_list = query(s_list_data, filters=(lambda s_list: s_list.zikatnr == zimkateg.zikatnr), first=True)

            if not s_list:

                if anz_setup > 0:

                    zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, 0)]})

                    if zimmer:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.zikatnr = zimkateg.zikatnr
                        s_list.kurzbez = zimkateg.kurzbez
                        s_list.kurzbez1 = zimkateg.kurzbez
                        s_list.bezeichnung = zimkateg.bezeichnung
                        s_list.flag = 1


                    for i in range(1,anz_setup + 1) :

                        paramtext = get_cache (Paramtext, {"txtnr": [(eq, (isetup_array[i - 1] + 9200))]})

                        zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, isetup_array[i - 1])]})

                        if zimmer:
                            s_list = S_list()
                            s_list_data.append(s_list)

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
                    s_list_data.append(s_list)

                    s_list.zikatnr = zimkateg.zikatnr
                    s_list.kurzbez = zimkateg.kurzbez
                    s_list.kurzbez1 = zimkateg.kurzbez
                    s_list.bezeichnung = zimkateg.bezeichnung
                    s_list.flag = 1

        if curr_marknr != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.marknr == curr_marknr)):
                s_list.reihenfolge = curr_marknr

    def new_create_list():

        nonlocal s_list_data, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal datum, origcode, prcode, curr_marknr


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_data, dynarate_list_data

        i:int = 0

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == (prcode).lower())).order_by(Ratecode._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, ratecode.zikatnr)]})

            if zimkateg:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.marknr == ratecode.marknr and s_list.zikatnr == zimkateg.zikatnr and s_list.contcode.lower()  == (prcode).lower()), first=True)

                if not s_list:

                    if anz_setup > 0:

                        zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, 0)]})

                        if zimmer:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            buffer_copy(zimkateg, s_list)
                            s_list.contcode = prcode
                            s_list.kurzbez1 = zimkateg.kurzbez
                            s_list.marknr = ratecode.marknr

                            prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                            if prmarket:
                                s_list.market = prmarket.bezeich
                        for i in range(1,anz_setup + 1) :

                            paramtext = get_cache (Paramtext, {"txtnr": [(eq, (isetup_array[i - 1] + 9200))]})

                            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, isetup_array[i - 1])]})

                            if zimmer:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                buffer_copy(zimkateg, s_list)
                                s_list.contcode = prcode
                                s_list.kurzbez1 = zimkateg.kurzbez +\
                                        substring(paramtext.notes, 0, 1)
                                s_list.marknr = ratecode.marknr
                                s_list.setup = paramtext.ptexte
                                s_list.nr = i

                                prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                                if prmarket:
                                    s_list.market = prmarket.bezeich
                    else:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        buffer_copy(zimkateg, s_list)
                        s_list.contcode = prcode
                        s_list.kurzbez1 = zimkateg.kurzbez
                        s_list.marknr = ratecode.marknr

                        prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                        if prmarket:
                            s_list.market = prmarket.bezeich

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

            s_list = query(s_list_data, filters=(lambda s_list: s_list.zikatnr == zimkateg.zikatnr), first=True)

            if not s_list:

                if anz_setup > 0:

                    zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, 0)]})

                    if zimmer:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        buffer_copy(zimkateg, s_list)
                        s_list.kurzbez1 = zimkateg.kurzbez
                        s_list.flag = 1


                    for i in range(1,anz_setup + 1) :

                        paramtext = get_cache (Paramtext, {"txtnr": [(eq, (isetup_array[i - 1] + 9200))]})

                        zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, isetup_array[i - 1])]})

                        if zimmer:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            buffer_copy(zimkateg, s_list)
                            s_list.kurzbez1 = zimkateg.kurzbez +\
                                    substring(paramtext.notes, 0, 1)
                            s_list.setup = paramtext.ptexte
                            s_list.nr = i
                            s_list.flag = 1


                else:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    buffer_copy(zimkateg, s_list)
                    s_list.kurzbez1 = zimkateg.kurzbez
                    s_list.flag = 1

        if curr_marknr != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.marknr == curr_marknr)):
                s_list.reihenfolge = curr_marknr

    def create_dynarate_list():

        nonlocal s_list_data, new_contrate, csetup_array, isetup_array, anz_setup, ci_date, global_occ, i_param439, queasy, paramtext, pricecod, zimkateg, zimmer, prmarket, ratecode
        nonlocal datum, origcode, prcode, curr_marknr


        nonlocal s_list, dynarate_list, dybuff
        nonlocal s_list_data, dynarate_list_data

        i:int = 0
        tokcounter:int = 0
        iftask:string = ""
        mestoken:string = ""
        mesvalue:string = ""
        mapcode:string = ""
        occ_rooms:int = 0
        use_it:bool = False
        Dybuff = Dynarate_list
        dybuff_data = dynarate_list_data

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == (prcode).lower())).order_by(Ratecode._recid).all():
            dynarate_list = Dynarate_list()
            dynarate_list_data.append(dynarate_list)

            iftask = ratecode.char1[4]
            for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                if mestoken == "CN":
                    dynarate_list.counter = to_int(mesvalue)
                elif mestoken == "RT":
                    dynarate_list.rmtype = mesvalue
                elif mestoken == "WD":
                    dynarate_list.w_day = to_int(mesvalue)
                elif mestoken == "FR":
                    dynarate_list.fr_room = to_int(mesvalue)
                elif mestoken == "TR":
                    dynarate_list.to_room = to_int(mesvalue)
                elif mestoken == "D1":
                    dynarate_list.days1 = to_int(mesvalue)
                elif mestoken == "D2":
                    dynarate_list.days2 = to_int(mesvalue)
                elif mestoken == "RC":
                    dynarate_list.rcode = mesvalue

        dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  == ("*").lower()), first=True)
        global_occ = None != dynarate_list and i_param439 == 1

        if global_occ:

            for dynarate_list in query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  != ("*").lower())):
                dynarate_list_data.remove(dynarate_list)

        else:

            for dynarate_list in query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  == ("*").lower())):
                dynarate_list_data.remove(dynarate_list)


        for dynarate_list in query(dynarate_list_data):
            occ_rooms = get_output(calculate_occupied_roomsbl(datum, dynarate_list.rmType, global_occ))
            use_it = True

            if dynarate_list.days1 != 0 and (datum - ci_date) <= dynarate_list.days1:
                use_it = False

            if use_it and dynarate_list.days2 != 0 and (datum - ci_date) >= dynarate_list.days2:
                use_it = False

            if use_it:
                use_it = (dynarate_list.fr_room <= occ_rooms) and (dynarate_list.to_room >= occ_rooms)

            if not use_it:
                dynarate_list_data.remove(dynarate_list)

            elif (dynarate_list.days1 != 0) or (dynarate_list.days2 != 0):

                for dybuff in query(dybuff_data, filters=(lambda dybuff: dybuff.days1 == 0 and dybuff.days2 == 0 and (dybuff.rmtype == dynarate_list.rmtype) and (dybuff.fr_room <= occ_rooms) and (dybuff.to_room >= occ_rooms))):
                    dybuff_data.remove(dybuff)


        if global_occ:

            for dynarate_list in query(dynarate_list_data):

                for ratecode in db_session.query(Ratecode).filter(
                         (Ratecode.code == dynarate_list.rcode) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum)).order_by(Ratecode._recid).all():

                    if curr_marknr == 0:
                        use_it = True
                    else:
                        use_it = (ratecode.marknr == curr_marknr)

                    if use_it:

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, ratecode.zikatnr)]})
                        mapcode = ratecode.code

                        queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, origcode)],"char2": [(eq, mapcode)],"number1": [(eq, 0)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, datum)]})

                        if queasy:
                            mapcode = queasy.char3

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.marknr == ratecode.marknr and s_list.zikatnr == zimkateg.zikatnr and s_list.contcode.lower()  == (mapcode).lower()), first=True)

                        if not s_list:

                            if anz_setup > 0:

                                zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, 0)]})

                                if zimmer:
                                    s_list = S_list()
                                    s_list_data.append(s_list)

                                    buffer_copy(zimkateg, s_list)
                                    s_list.contcode = mapcode
                                    s_list.kurzbez1 = zimkateg.kurzbez
                                    s_list.marknr = ratecode.marknr

                                    prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                                    if prmarket:
                                        s_list.market = prmarket.bezeich
                                for i in range(1,anz_setup + 1) :

                                    paramtext = get_cache (Paramtext, {"txtnr": [(eq, (isetup_array[i - 1] + 9200))]})

                                    zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, isetup_array[i - 1])]})

                                    if zimmer:
                                        s_list = S_list()
                                        s_list_data.append(s_list)

                                        buffer_copy(zimkateg, s_list)
                                        s_list.contcode = mapcode
                                        s_list.kurzbez1 = zimkateg.kurzbez +\
                                                substring(paramtext.notes, 0, 1)
                                        s_list.marknr = ratecode.marknr
                                        s_list.setup = paramtext.ptexte
                                        s_list.nr = i

                                        prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                                        if prmarket:
                                            s_list.market = prmarket.bezeich
                            else:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                buffer_copy(zimkateg, s_list)
                                s_list.contcode = mapcode
                                s_list.kurzbez1 = zimkateg.kurzbez
                                s_list.marknr = ratecode.marknr

                                prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                                if prmarket:
                                    s_list.market = prmarket.bezeich

        else:

            for dynarate_list in query(dynarate_list_data):

                ratecode = get_cache (Ratecode, {"code": [(eq, dynarate_list.rcode)]})

                zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, dynarate_list.rmtype)]})

                if zimkateg:
                    mapcode = ratecode.code

                    queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, origcode)],"char2": [(eq, mapcode)],"number1": [(eq, zimkateg.zikatnr)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, datum)]})

                    if queasy:
                        mapcode = queasy.char3

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.marknr == ratecode.marknr and s_list.zikatnr == zimkateg.zikatnr and s_list.contcode.lower()  == (mapcode).lower()), first=True)

                    if not s_list:

                        if anz_setup > 0:

                            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, 0)]})

                            if zimmer:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                buffer_copy(zimkateg, s_list)
                                s_list.contcode = mapcode
                                s_list.kurzbez1 = zimkateg.kurzbez
                                s_list.marknr = ratecode.marknr

                                prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                                if prmarket:
                                    s_list.market = prmarket.bezeich
                            for i in range(1,anz_setup + 1) :

                                paramtext = get_cache (Paramtext, {"txtnr": [(eq, (isetup_array[i - 1] + 9200))]})

                                zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, isetup_array[i - 1])]})

                                if zimmer:
                                    s_list = S_list()
                                    s_list_data.append(s_list)

                                    buffer_copy(zimkateg, s_list)
                                    s_list.contcode = mapcode
                                    s_list.kurzbez1 = zimkateg.kurzbez +\
                                            substring(paramtext.notes, 0, 1)
                                    s_list.marknr = ratecode.marknr
                                    s_list.setup = paramtext.ptexte
                                    s_list.nr = i

                                    prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                                    if prmarket:
                                        s_list.market = prmarket.bezeich
                        else:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            buffer_copy(zimkateg, s_list)
                            s_list.contcode = mapcode
                            s_list.kurzbez1 = zimkateg.kurzbez
                            s_list.marknr = ratecode.marknr

                            prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                            if prmarket:
                                s_list.market = prmarket.bezeich


        if curr_marknr != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.marknr == curr_marknr)):
                s_list.reihenfolge = curr_marknr


    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, origcode)]})

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

    return generate_output()