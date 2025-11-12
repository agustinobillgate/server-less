#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 14-10-2025 
# Tiket ID : F50EA1 | New Compile program if 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Zimmer, Genstat, Zimkateg, Bill, Reservation, Segment, Sourccod, Guest, Nation, Arrangement, Artikel, Res_line

def vhpif_bi_tsi_get_room_revenuebl(resend_date:date):

    prepare_cache ([Htparam, Zimmer, Genstat, Zimkateg, Bill, Reservation, Segment, Guest, Nation, Arrangement, Artikel, Res_line])

    room_rev_data = []
    previous_date:date = None
    total_vacant_dirty:int = 0
    total_vacant_clean:int = 0
    total_vacant_clean_uncheck:int = 0
    total_vacant:int = 0
    curr_i:int = 0
    net_lodg:Decimal = to_decimal("0.0")
    fnet_lodg:Decimal = to_decimal("0.0")
    tot_breakfast:Decimal = to_decimal("0.0")
    tot_lunch:Decimal = to_decimal("0.0")
    tot_dinner:Decimal = to_decimal("0.0")
    tot_other:Decimal = to_decimal("0.0")
    tot_rmrev:Decimal = to_decimal("0.0")
    tot_vat:Decimal = to_decimal("0.0")
    tot_service:Decimal = to_decimal("0.0")
    bill_date:date = None
    serv1:int = 0
    vat1:int = 0
    vat2:int = 0
    fact1:int = 0
    do_it:bool = False
    i:int = 0
    str:string = ""
    htparam = zimmer = genstat = zimkateg = bill = reservation = segment = sourccod = guest = nation = arrangement = artikel = res_line = None

    room_rev = None

    room_rev_data, Room_rev = create_model("Room_rev", {"bill_number":int, "bill_date":date, "hotel_code":string, "room_type":string, "segment":string, "nationality":string, "room_sold":int, "room_night":int, "room_available":int, "room_pax":int, "room_price":Decimal, "total_room_price":Decimal, "room_number":string, "res_number":int, "ratecode":string, "checkin_date":date, "checkout_date":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_rev_data, previous_date, total_vacant_dirty, total_vacant_clean, total_vacant_clean_uncheck, total_vacant, curr_i, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, bill_date, serv1, vat1, vat2, fact1, do_it, i, str, htparam, zimmer, genstat, zimkateg, bill, reservation, segment, sourccod, guest, nation, arrangement, artikel, res_line
        nonlocal resend_date


        nonlocal room_rev
        nonlocal room_rev_data

        return {"room-rev": room_rev_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    bill_date = htparam.fdate
    total_vacant_dirty = 0
    total_vacant_clean = 0
    total_vacant_clean_uncheck = 0
    total_vacant = 0

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():

        if zimmer.zistatus == 2:
            total_vacant_dirty = total_vacant_dirty + 1

        elif zimmer.zistatus == 0:
            total_vacant_clean = total_vacant_clean + 1

        elif zimmer.zistatus == 1:
            total_vacant_clean_uncheck = total_vacant_clean_uncheck + 1
    total_vacant = total_vacant_clean + total_vacant_clean_uncheck + total_vacant_dirty
    resend_date = bill_date - timedelta(days=1)

    if resend_date < bill_date:

        genstat_obj_list = {}
        genstat = Genstat()
        zimmer = Zimmer()
        for genstat.resnr, genstat.res_int, genstat.gastnrmember, genstat.argt, genstat.datum, genstat.res_date, genstat.erwachs, genstat.kind1, genstat.gratis, genstat.logis, genstat.zinr, genstat.res_char, genstat._recid, zimmer.zikatnr, zimmer.zistatus, zimmer._recid in db_session.query(Genstat.resnr, Genstat.res_int, Genstat.gastnrmember, Genstat.argt, Genstat.datum, Genstat.res_date, Genstat.erwachs, Genstat.kind1, Genstat.gratis, Genstat.logis, Genstat.zinr, Genstat.res_char, Genstat._recid, Zimmer.zikatnr, Zimmer.zistatus, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Genstat.zinr)).filter(
                 (Genstat.zinr != "") & (Genstat.datum == resend_date) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.zinr, Genstat.resnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            bill = get_cache (Bill, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

            reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

            guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

            nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
            room_rev = Room_rev()
            room_rev_data.append(room_rev)

            room_rev.bill_number = bill.rechnr
            room_rev.bill_date = genstat.datum
            room_rev.hotel_code = ""
            room_rev.room_type = zimkateg.kurzbez
            room_rev.segment = segment.bezeich
            room_rev.nationality = nation.bezeich
            room_rev.room_sold = 1
            room_rev.room_night = (genstat.res_date[1] - genstat.res_date[0])

            if room_rev.room_night == 0:
                room_rev.room_night = 1
            room_rev.room_available = total_vacant
            room_rev.room_pax = genstat.erwachs + genstat.kind1 + genstat.gratis
            room_rev.room_price = to_decimal(round(genstat.logis , 0))
            room_rev.total_room_price =  to_decimal(room_rev.room_price) * to_decimal(room_rev.room_night)
            room_rev.room_number = genstat.zinr
            room_rev.res_number = genstat.resnr
            room_rev.checkin_date = genstat.res_date[0]
            room_rev.checkout_date = genstat.res_date[1]


            for i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                str = entry(i - 1, genstat.res_char[1], ";")

                if substring(str, 0, 6) == ("$CODE$").lower() :
                    room_rev.ratecode = substring(str, 6)
                    break
    else:

        for res_line in db_session.query(Res_line).filter(
                 ((Res_line.active_flag <= 1)) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (not_ (Res_line.ankunft > resend_date)) & (not_ (Res_line.abreise < resend_date))).order_by(Res_line.zinr, Res_line.resnr).all():
            do_it = True

            if res_line.abreise == resend_date:
                do_it = res_line.ankunft == resend_date

            if do_it:
                pass

                if res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

                bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
                serv1 = 0
                vat1 = 0
                vat2 = 0
                fact1 = 0


                serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, resend_date))
                room_rev = Room_rev()
                room_rev_data.append(room_rev)

                room_rev.bill_number = bill.rechnr
                room_rev.bill_date = bill.datum
                room_rev.hotel_code = ""
                room_rev.room_type = zimkateg.kurzbez
                room_rev.segment = segment.bezeich
                room_rev.nationality = nation.bezeich
                room_rev.room_sold = res_line.zimmeranz
                room_rev.room_night = (res_line.abreise - res_line.ankunft)

                if room_rev.room_night == 0:
                    room_rev.room_night = 1
                room_rev.room_available = total_vacant
                room_rev.room_pax = res_line.erwachs + res_line.kind1 + res_line.gratis
                room_rev.room_price = to_decimal(round(res_line.zipreis / (1 + vat1 + vat2 + serv1) , 0))
                room_rev.total_room_price =  to_decimal(room_rev.room_price) * to_decimal(room_rev.room_night)
                room_rev.room_number = res_line.zinr
                room_rev.res_number = res_line.resnr
                room_rev.checkin_date = res_line.ankunft
                room_rev.checkout_date = res_line.abreise


                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        room_rev.ratecode = substring(str, 6)
                        break

    return generate_output()