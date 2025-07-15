from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Zimkateg, Arrangement, Ratecode, Waehrung

def find_dyna_ratecode(datum:date, rmtype:str, adult:int, child:int, rmrate:decimal, dynacode:str, argtno:int):
    statcode = ""
    markno = 0
    curr = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    w_day:int = 0
    tokcounter:int = 0
    iftask:str = ""
    mestoken:str = ""
    mesvalue:str = ""
    mapcode:str = ""
    dyna_flag:bool = False
    queasy = zimkateg = arrangement = ratecode = waehrung = None

    dynarate_list = None

    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rcode":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal statcode, markno, curr, wd_array, w_day, tokcounter, iftask, mestoken, mesvalue, mapcode, dyna_flag, queasy, zimkateg, arrangement, ratecode, waehrung
        nonlocal datum, rmtype, adult, child, rmrate, dynacode, argtno


        nonlocal dynarate_list
        nonlocal dynarate_list_list

        return {"statcode": statcode, "argtno": argtno, "markno": markno, "curr": curr}

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 2) & (Queasy.char1 == dynacode)).first()

    if not queasy:

        return generate_output()

    if queasy.logi2:
        dyna_flag = True
    else:
        statcode = dynacode

    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.kurzbez == rmtype)).first()

    arrangement = db_session.query(Arrangement).filter(
             (Arrangement.argtnr == argtno)).first()

    if dyna_flag:

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == dynacode)).order_by(Ratecode._recid).all():

            if re.match(r".*RT" + rmtype + r".*",ratecode.char1[4], re.IGNORECASE):
                dynarate_list = Dynarate_list()
                dynarate_list_list.append(dynarate_list)

                iftask = ratecode.char1[4]


                for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                    if mestoken == "CN":
                        dynarate_list.counter = to_int(mesvalue)
                    elif mestoken == "RC":
                        dynarate_list.rcode = mesvalue
                    elif mestoken == "WD":
                        dynarate_list.w_day = to_int(mesvalue)
        w_day = wd_array[get_weekday(datum) - 1]

        for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.dynarate_list.w_day == w_day or dynarate_list.w_day == 0), sort_by=[("w_day",True)]):
            mapcode = dynarate_list.rcode

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 145) & (Queasy.char1 == dynacode) & (func.lower(Queasy.char2) == (mapcode).lower()) & (Queasy.number1 == zimkateg.zikatnr) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == datum)).first()

            if queasy:
                mapcode = queasy.char3

            if arrangement:

                ratecode = db_session.query(Ratecode).filter(
                         (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0)).first()

                if ratecode:
                    statcode = mapcode
                    argtno = ratecode.argtnr
                    markno = ratecode.marknr

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 18) & (Queasy.number1 == markno)).first()

                    if queasy:

                        waehrung = db_session.query(Waehrung).filter(
                                 (Waehrung.wabkurz == queasy.char3)).first()

                        if waehrung:
                            curr = waehrung.waehrungsnr

                    return generate_output()
            else:

                ratecode = db_session.query(Ratecode).filter(
                         (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.zipreis == rmrate)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day)).first()

                if not ratecode:

                    ratecode = db_session.query(Ratecode).filter(
                             (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0)).first()

                if ratecode:
                    statcode = mapcode
                    argtno = ratecode.argtnr
                    markno = ratecode.marknr

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 18) & (Queasy.number1 == markno)).first()

                    if queasy:

                        waehrung = db_session.query(Waehrung).filter(
                                 (Waehrung.wabkurz == queasy.char3)).first()

                        if waehrung:
                            curr = waehrung.waehrungsnr

                    return generate_output()
    else:
        w_day = wd_array[get_weekday(datum) - 1]

        if arrangement:

            ratecode = db_session.query(Ratecode).filter(
                     (Ratecode.code == statcode) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.argtnr == arrangement.argtnr) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0)).first()

            if ratecode:
                argtno = ratecode.argtnr
                markno = ratecode.marknr

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 18) & (Queasy.number1 == markno)).first()

                if queasy:

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung.wabkurz == queasy.char3)).first()

                    if waehrung:
                        curr = waehrung.waehrungsnr

                return generate_output()
        else:

            ratecode = db_session.query(Ratecode).filter(
                     (Ratecode.code == statcode) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == statcode) & (Ratecode.zikatnr == zimkateg.zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0)).first()

            if ratecode:
                argtno = ratecode.argtnr
                markno = ratecode.marknr

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 18) & (Queasy.number1 == markno)).first()

                if queasy:

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung.wabkurz == queasy.char3)).first()

                    if waehrung:
                        curr = waehrung.waehrungsnr

                return generate_output()

    return generate_output()