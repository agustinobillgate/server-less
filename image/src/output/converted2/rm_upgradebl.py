#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Guest, Htparam, Genstat, Zimkateg, Waehrung, Reservation

def rm_upgradebl(datum:date, to_date:date):

    prepare_cache ([Res_line, Guest, Htparam, Genstat, Zimkateg, Waehrung, Reservation])

    str_list_list = []
    new_contrate:bool = False
    curr_date:date = None
    ci_date:date = None
    from_date:date = None
    ct:string = ""
    curr_i:int = 0
    origzikatnr:int = 0
    origrmtype:string = ""
    res_line = guest = htparam = genstat = zimkateg = waehrung = reservation = None

    str_list = gbuff = None

    str_list_list, Str_list = create_model_like(Res_line, {"gname":string, "company":string, "rmtype":string, "currency":string, "cat":string, "id":string})

    Gbuff = create_buffer("Gbuff",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, new_contrate, curr_date, ci_date, from_date, ct, curr_i, origzikatnr, origrmtype, res_line, guest, htparam, genstat, zimkateg, waehrung, reservation
        nonlocal datum, to_date
        nonlocal gbuff


        nonlocal str_list, gbuff
        nonlocal str_list_list

        return {"str-list": str_list_list}

    def upgrade1():

        nonlocal str_list_list, new_contrate, curr_date, ci_date, from_date, ct, curr_i, origzikatnr, origrmtype, res_line, guest, htparam, genstat, zimkateg, waehrung, reservation
        nonlocal datum, to_date
        nonlocal gbuff


        nonlocal str_list, gbuff
        nonlocal str_list_list

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum < ci_date) & (Genstat.datum >= datum) & (Genstat.datum <= to_date) & (Genstat.zinr != "") & (matches(Genstat.res_char[inc_value(1)],("*RmUpgrade*")))).order_by(Genstat._recid).all():
            origzikatnr = 0
            for curr_i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                ct = entry(curr_i - 1, genstat.res_char[1], ";")

                if substring(ct, 0, 9) == ("RmUpgrade").lower() :
                    origzikatnr = to_int(substring(ct, 9))

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, origzikatnr)]})

                    if zimkateg:
                        origrmtype = zimkateg.kurzbez

            str_list = query(str_list_list, filters=(lambda str_list: str_list.resnr == genstat.resnr and str_list.reslinnr == genstat.res_int[0] and str_list.zikatnr == genstat.zikatnr and str_list.rmtype == origrmtype), first=True)

            if not str_list:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                gbuff = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                if origrmtype != zimkateg.kurzbez:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.resnr = genstat.resnr
                    str_list.reslinnr = genstat.res_int[0]
                    str_list.zinr = genstat.zinr
                    str_list.zikatnr = genstat.zikatnr
                    str_list.rmtype = origrmtype
                    str_list.arrangement = genstat.argt
                    str_list.gname = guest.name + ", " + guest.vorname1
                    str_list.company = gbuff.name + ", " + gbuff.anredefirma
                    str_list.ankunft = genstat.res_date[0]
                    str_list.abreise = genstat.res_date[1]
                    str_list.zipreis =  to_decimal(genstat.zipreis)
                    str_list.cat = zimkateg.kurzbez
                    str_list.changed = res_line.changed

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, genstat.wahrungsnr)]})

                    if waehrung:
                        str_list.currency = waehrung.wabkurz

                    reservation = get_cache (Reservation, {"gastnr": [(eq, genstat.gastnr)]})

                    if reservation:
                        str_list.id = reservation.useridanlage
                        str_list.changed_id = reservation.useridmutat


    def upgrade2():

        nonlocal str_list_list, new_contrate, curr_date, ci_date, from_date, ct, curr_i, origzikatnr, origrmtype, res_line, guest, htparam, genstat, zimkateg, waehrung, reservation
        nonlocal datum, to_date
        nonlocal gbuff


        nonlocal str_list, gbuff
        nonlocal str_list_list

        for res_line in db_session.query(Res_line).filter(
                 not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= from_date) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(0)] >= 0)).order_by(Res_line._recid).all():
            origzikatnr = res_line.l_zuordnung[0]

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, origzikatnr)]})

            if zimkateg:
                origrmtype = zimkateg.kurzbez

            str_list = query(str_list_list, filters=(lambda str_list: str_list.resnr == res_line.resnr and str_list.reslinnr == res_line.reslinnr and str_list.zikatnr == res_line.zikatnr and str_list.rmtype == origrmtype), first=True)

            if not str_list:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                reservation = get_cache (Reservation, {"gastnr": [(eq, res_line.gastnr)]})

                if origrmtype != zimkateg.kurzbez:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.resnr = res_line.resnr
                    str_list.reslinnr = res_line.reslinnr
                    str_list.zinr = res_line.zinr
                    str_list.zikatnr = res_line.zikatnr
                    str_list.rmtype = origrmtype
                    str_list.arrangement = res_line.arrangement
                    str_list.gname = guest.name + ", " + guest.vorname1
                    str_list.company = gbuff.name + ", " + gbuff.anredefirma
                    str_list.ankunft = res_line.ankunft
                    str_list.abreise = res_line.abreise
                    str_list.zipreis =  to_decimal(res_line.zipreis)
                    str_list.cat = zimkateg.kurzbez
                    str_list.changed = res_line.changed

                    if reservation:
                        str_list.id = reservation.useridanlage
                        str_list.changed_id = reservation.useridmutat

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if waehrung:
                        str_list.currency = waehrung.wabkurz

    str_list_list.clear()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    curr_date = ci_date

    if datum <= to_date:
        upgrade1()

    elif datum >= to_date:
        upgrade2()

    return generate_output()