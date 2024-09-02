from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Guest, Htparam, Genstat, Zimkateg, Waehrung, Reservation

def rm_upgradebl(datum:date, to_date:date):
    str_list_list = []
    new_contrate:bool = False
    curr_date:date = None
    ci_date:date = None
    from_date:date = None
    ct:str = ""
    curr_i:int = 0
    origzikatnr:int = 0
    origrmtype:str = ""
    res_line = guest = htparam = genstat = zimkateg = waehrung = reservation = None

    str_list = gbuff = None

    str_list_list, Str_list = create_model_like(Res_line, {"gname":str, "company":str, "rmtype":str, "currency":str, "cat":str, "id":str})

    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, new_contrate, curr_date, ci_date, from_date, ct, curr_i, origzikatnr, origrmtype, res_line, guest, htparam, genstat, zimkateg, waehrung, reservation
        nonlocal gbuff


        nonlocal str_list, gbuff
        nonlocal str_list_list
        return {"str-list": str_list_list}

    def upgrade1():

        nonlocal str_list_list, new_contrate, curr_date, ci_date, from_date, ct, curr_i, origzikatnr, origrmtype, res_line, guest, htparam, genstat, zimkateg, waehrung, reservation
        nonlocal gbuff


        nonlocal str_list, gbuff
        nonlocal str_list_list

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum < ci_date) &  (Genstat.datum >= datum) &  (Genstat.datum <= to_date) &  (Genstat.zinr != "") &  (Genstat.res_char[1].op("~")(".*RmUpgrade.*"))).all():
            origzikatnr = 0
            for curr_i in range(1,num_entries(res_char[1], ";") - 1 + 1) :
                ct = entry(curr_i - 1, res_char[1], ";")

                if substring(ct, 0, 9) == "RmUpgrade":
                    origzikatnr = to_int(substring(ct, 9))

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == origzikatnr)).first()

                    if zimkateg:
                        origrmtype = zimkateg.kurzbez

            str_list = query(str_list_list, filters=(lambda str_list :str_list.resnr == genstat.resnr and str_list.reslinnr == genstat.res_int[0] and str_list.zikatnr == genstat.zikatnr and str_list.rmType == origrmtype), first=True)

            if not str_list:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == genstat.gastnrmember)).first()

                gbuff = db_session.query(Gbuff).filter(
                        (Gbuff.gastnr == genstat.gastnr)).first()

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == genstat.zikatnr)).first()

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                if origrmtype != zimkateg.kurzbez:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.resnr = genstat.resnr
                    str_list.reslinnr = genstat.res_int[0]
                    str_list.zinr = genstat.zinr
                    str_list.zikatnr = genstat.zikatnr
                    str_list.rmType = origrmtype
                    str_list.arrangement = genstat.argt
                    str_list.gname = guest.name + ", " + guest.vorname1
                    str_list.company = gbuff.name + ", " + gbuff.anredefirma
                    str_list.ankunft = genstat.res_date[0]
                    str_list.abreise = genstat.res_date[1]
                    str_list.zipreis = genstat.zipreis
                    str_list.cat = zimkateg.kurzbez
                    str_list.changed = res_line.changed

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == genstat.wahrungsn)).first()

                    if waehrung:
                        str_list.currency = waehrung.wabkurz

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.gastnr == genstat.gastnr)).first()

                    if reservation:
                        str_list.id = reservation.useridanlage
                        str_list.changed_id = reservation.useridmutat

    def upgrade2():

        nonlocal str_list_list, new_contrate, curr_date, ci_date, from_date, ct, curr_i, origzikatnr, origrmtype, res_line, guest, htparam, genstat, zimkateg, waehrung, reservation
        nonlocal gbuff


        nonlocal str_list, gbuff
        nonlocal str_list_list

        for res_line in db_session.query(Res_line).filter(
                (not Res_line.ankunft > to_date) &  (not Res_line.abreise <= from_date) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[0] >= 0)).all():
            origzikatnr = res_line.l_zuordnung[0]

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == origzikatnr)).first()

            if zimkateg:
                origrmtype = zimkateg.kurzbez

            str_list = query(str_list_list, filters=(lambda str_list :str_list.resnr == res_line.resnr and str_list.reslinnr == res_line.reslinnr and str_list.zikatnr == res_line.zikatnr and str_list.rmType == origrmtype), first=True)

            if not str_list:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()

                gbuff = db_session.query(Gbuff).filter(
                        (Gbuff.gastnr == res_line.gastnr)).first()

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()

                reservation = db_session.query(Reservation).filter(
                        (Reservation.gastnr == res_line.gastnr)).first()

                if origrmtype != zimkateg.kurzbez:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.resnr = res_line.resnr
                    str_list.reslinnr = res_line.reslinnr
                    str_list.zinr = res_line.zinr
                    str_list.zikatnr = res_line.zikatnr
                    str_list.rmType = origrmtype
                    str_list.arrangement = res_line.arrangement
                    str_list.gname = guest.name + ", " + guest.vorname1
                    str_list.company = gbuff.name + ", " + gbuff.anredefirma
                    str_list.ankunft = res_line.ankunft
                    str_list.abreise = res_line.abreise
                    str_list.zipreis = res_line.zipreis
                    str_list.cat = zimkateg.kurzbez
                    str_list.changed = res_line.changed

                    if reservation:
                        str_list.id = reservation.useridanlage
                        str_list.changed_id = reservation.useridmutat

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == res_line.betriebsnr)).first()

                    if waehrung:
                        str_list.currency = waehrung.wabkurz


    str_list_list.clear()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    curr_date = ci_date

    if datum <= to_date:
        upgrade1()

    elif datum >= to_date:
        upgrade2()

    return generate_output()