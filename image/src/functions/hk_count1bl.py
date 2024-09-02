from functions.additional_functions import *
import decimal
from functions.expiredid_countbl import expiredid_countbl
from datetime import date
from models import Htparam, Zimmer, Res_line, Reservation, Segment, Zimkateg, Waehrung

def hk_count1bl(aswaittime:int, price_decimal:int):
    arrived1 = 0
    arrived2 = 0
    arriving1 = 0
    arriving2 = 0
    tot_arrive1 = 0
    tot_arrive2 = 0
    avrg_rate1 = 0
    avrg_rate2 = 0
    rm_rate = 0
    departed1 = 0
    departed2 = 0
    departing1 = 0
    departing2 = 0
    tot_depart1 = 0
    tot_depart2 = 0
    vclean = 0
    vuncheck = 0
    oclean = 0
    odirty = 0
    vdirty = 0
    atoday = 0
    oroom1 = 0
    oroom2 = 0
    oooroom1 = 0
    oooroom2 = 0
    comproom1 = 0
    comproom2 = 0
    houseroom1 = 0
    houseroom2 = 0
    iroom1 = 0
    iroom2 = 0
    eocc1 = 0
    eocc2 = 0
    tot_zimmer = 0
    expired_id = 0
    user_wig = False
    uhr:int = -100
    uhr_str:str = ""
    pvlstopped:bool = FALSE
    curr_time:int = 0
    min_unit:int = 0
    occ_rm1:int = 0
    occ_rm2:int = 0
    htparam = zimmer = res_line = reservation = segment = zimkateg = waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal arrived1, arrived2, arriving1, arriving2, tot_arrive1, tot_arrive2, avrg_rate1, avrg_rate2, rm_rate, departed1, departed2, departing1, departing2, tot_depart1, tot_depart2, vclean, vuncheck, oclean, odirty, vdirty, atoday, oroom1, oroom2, oooroom1, oooroom2, comproom1, comproom2, houseroom1, houseroom2, iroom1, iroom2, eocc1, eocc2, tot_zimmer, expired_id, user_wig, uhr, uhr_str, pvlstopped, curr_time, min_unit, occ_rm1, occ_rm2, htparam, zimmer, res_line, reservation, segment, zimkateg, waehrung


        return {"arrived1": arrived1, "arrived2": arrived2, "arriving1": arriving1, "arriving2": arriving2, "tot_arrive1": tot_arrive1, "tot_arrive2": tot_arrive2, "avrg_rate1": avrg_rate1, "avrg_rate2": avrg_rate2, "rm_rate": rm_rate, "departed1": departed1, "departed2": departed2, "departing1": departing1, "departing2": departing2, "tot_depart1": tot_depart1, "tot_depart2": tot_depart2, "vclean": vclean, "vuncheck": vuncheck, "oclean": oclean, "odirty": odirty, "vdirty": vdirty, "atoday": atoday, "oroom1": oroom1, "oroom2": oroom2, "oooroom1": oooroom1, "oooroom2": oooroom2, "comproom1": comproom1, "comproom2": comproom2, "houseroom1": houseroom1, "houseroom2": houseroom2, "iroom1": iroom1, "iroom2": iroom2, "eocc1": eocc1, "eocc2": eocc2, "tot_zimmer": tot_zimmer, "expired_id": expired_id, "user_wig": user_wig}

    def init_var():

        nonlocal arrived1, arrived2, arriving1, arriving2, tot_arrive1, tot_arrive2, avrg_rate1, avrg_rate2, rm_rate, departed1, departed2, departing1, departing2, tot_depart1, tot_depart2, vclean, vuncheck, oclean, odirty, vdirty, atoday, oroom1, oroom2, oooroom1, oooroom2, comproom1, comproom2, houseroom1, houseroom2, iroom1, iroom2, eocc1, eocc2, tot_zimmer, expired_id, user_wig, uhr, uhr_str, pvlstopped, curr_time, min_unit, occ_rm1, occ_rm2, htparam, zimmer, res_line, reservation, segment, zimkateg, waehrung

        ci_date:date = None
        rm_active:bool = False
        departed1 = 0
        departed2 = 0
        departing1 = 0
        departing2 = 0
        arrived1 = 0
        arrived2 = 0
        arriving1 = 0
        arriving2 = 0
        vclean = 0
        vuncheck = 0
        oclean = 0
        vdirty = 0
        odirty = 0
        atoday = 0
        oroom1 = 0
        oroom2 = 0
        oooroom1 = 0
        oooroom2 = 0
        iroom1 = 0
        iroom2 = 0
        eocc1 = 0
        eocc2 = 0
        houseroom1 = 0
        houseroom2 = 0
        comproom1 = 0
        comproom2 = 0
        tot_zimmer = 0
        occ_rm1 = 0
        occ_rm2 = 0
        rm_rate = 0
        avrg_rate1 = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise == ci_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if res_line.resstatus == 6:
                departing1 = departing1 + 1


            departing2 = departing2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

        res_line_obj_list = []
        for res_line, zimmer, reservation in db_session.query(Res_line, Zimmer, Reservation).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == reservation.segmentcode)).first()

            if ((res_line.abreise > ci_date) or (res_line.ankunft == ci_date and res_line.abreise == ci_date and res_line.zipreis > 0)):

                if res_line.resstatus == 6 and zimmer.sleeping:
                    occ_rm2 = occ_rm2 + 1
                    oroom1 = oroom1 + 1
                    eocc1 = eocc1 + 1
                    oroom2 = oroom2 + res_line.erwachs + res_line.gratis +\
                            res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]
                    eocc2 = eocc2 + res_line.erwachs + res_line.gratis +\
                            res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

                    if res_line.zipreis > 0:
                        occ_rm1 = occ_rm1 + 1
                cal_local_rmrate()

            if res_line.ankunft == ci_date:

                if res_line.resstatus == 6:
                    arrived1 = arrived1 + 1
                arrived2 = arrived2 + (res_line.erwachs + res_line.gratis) + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

            if segment:

                if segment.betriebsnr == 2:

                    if res_line.resstatus == 6:
                        houseroom1 = houseroom1 + 1


                    houseroom2 = houseroom2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

                elif segment.betriebsnr == 1 or res_line.gratis > 0:

                    if res_line.resstatus == 6:
                        comproom1 = comproom1 + 1


                    comproom2 = comproom2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

            if not zimmer.sleeping:
                iroom2 = iroom2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                (Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise == ci_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if not res_line.zimmerfix:
                departed1 = departed1 + 1
            departed2 = departed2 + res_line.erwachs + res_line.gratis +\
                    res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]


        tot_depart1 = departed1 + departing1
        tot_depart2 = departed2 + departing2

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  (Res_line.ankunft == ci_date) &  (Res_line.l_zuordnung[2] == 0)).all():

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()
            rm_active = True

            if (zimmer and not zimmer.sleeping):
                rm_active = False

            if (res_line.resstatus == 1 or res_line.resstatus == 2 or res_line.resstatus == 5):
                arriving1 = arriving1 + res_line.zimmeranz

                if rm_active:
                    eocc1 = eocc1 + res_line.zimmeranz
                    occ_rm2 = occ_rm2 + res_line.zimmeranz

                    if res_line.zipreis > 0:
                        occ_rm1 = occ_rm1 + res_line.zimmeranz

            if (res_line.resstatus == 1 or res_line.resstatus == 2 or res_line.resstatus == 5 or res_line.resstatus == 11):
                arriving2 = arriving2 + res_line.zimmeranz * (res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3])

                if rm_active:
                    eocc2 = eocc2 + res_line.zimmeranz * (res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3])
                    cal_local_rmrate()
        avrg_rate1 = rm_rate / occ_rm1
        avrg_rate2 = rm_rate / occ_rm2


        tot_arrive1 = arrived1 + arriving1
        tot_arrive2 = arrived2 + arriving2

        zimmer_obj_list = []
        for zimmer, zimkateg in db_session.query(Zimmer, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).all():
            if zimmer._recid in zimmer_obj_list:
                continue
            else:
                zimmer_obj_list.append(zimmer._recid)

            if zimkateg.verfuegbarkeit:

                if (zimmer.zistatus == 0 or zimmer.zistatus == 1 or zimmer.zistatus == 5):

                    if zimmer.zistatus == 0:
                        vclean = vclean + 1

                    elif zimmer.zistatus == 1:
                        vuncheck = vuncheck + 1

                    elif zimmer.zistatus == 5:
                        oclean = oclean + 1

                elif (zimmer.zistatus == 2 or zimmer.zistatus == 3 or zimmer.zistatus == 4):

                    if zimmer.zistatus == 2:
                        vdirty = vdirty + 1

                    elif zimmer.zistatus == 4:
                        odirty = odirty + 1

                    elif zimmer.zistatus == 3:
                        atoday = atoday + 1

                elif zimmer.zistatus == 6:
                    oooroom1 = oooroom1 + 1

                if not zimmer.sleeping:
                    iroom1 = iroom1 + 1

                if zimmer.sleeping:
                    tot_zimmer = tot_zimmer + 1

    def cal_local_rmrate():

        nonlocal arrived1, arrived2, arriving1, arriving2, tot_arrive1, tot_arrive2, avrg_rate1, avrg_rate2, rm_rate, departed1, departed2, departing1, departing2, tot_depart1, tot_depart2, vclean, vuncheck, oclean, odirty, vdirty, atoday, oroom1, oroom2, oooroom1, oooroom2, comproom1, comproom2, houseroom1, houseroom2, iroom1, iroom2, eocc1, eocc2, tot_zimmer, expired_id, user_wig, uhr, uhr_str, pvlstopped, curr_time, min_unit, occ_rm1, occ_rm2, htparam, zimmer, res_line, reservation, segment, zimkateg, waehrung

        frate:decimal = 1
        rate:decimal = 0

        if res_line.zipreis == 0:

            return

        if res_line.reserve_dec != 0:
            frate = res_line.reserve_dec
        else:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                frate = waehrung.ankauf / waehrung.einheit
        rm_rate = rm_rate + round(res_line.zipreis * frate, price_decimal) * res_line.zimmeranz

    init_var()
    expired_id, user_wig = get_output(expiredid_countbl(aswaittime))

    return generate_output()