#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Zimkateg, Htparam, Zimmer, Genstat, Zkstat

def calculate_occupied_roomsbl(datum:date, rmtype:string, global_occ:bool):

    prepare_cache ([Res_line, Zimkateg, Htparam, Zimmer, Genstat, Zkstat])

    occ_rooms = 0
    use_it:bool = False
    ci_date:date = None
    tot_occ_rooms:int = 0
    rmcat_rooms:int = 0
    total_rooms:int = 0
    occ_rooms_1:int = 0
    i_method:int = 0
    d_occupancy:Decimal = to_decimal("0.0")
    calc_rm:bool = False
    res_line = zimkateg = htparam = zimmer = genstat = zkstat = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal occ_rooms, use_it, ci_date, tot_occ_rooms, rmcat_rooms, total_rooms, occ_rooms_1, i_method, d_occupancy, calc_rm, res_line, zimkateg, htparam, zimmer, genstat, zkstat
        nonlocal datum, rmtype, global_occ

        return {"occ_rooms": occ_rooms}

    def cal_method0():

        nonlocal occ_rooms, use_it, ci_date, tot_occ_rooms, rmcat_rooms, total_rooms, occ_rooms_1, i_method, d_occupancy, calc_rm, res_line, zimkateg, htparam, zimmer, genstat, zkstat
        nonlocal datum, rmtype, global_occ

        if zimkateg.typ != 0:
            cal_method0a()

            return

        if datum >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.zikatnr == zimkateg.zikatnr) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)).order_by(Res_line._recid).all():
                use_it = True

                if res_line.ankunft == res_line.abreise:
                    use_it = (res_line.zipreis > 0)

                if res_line.abreise > res_line.ankunft and res_line.abreise == datum:
                    use_it = False

                if use_it and res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                    if zimmer and not zimmer.sleeping:
                        use_it = False

                if use_it:
                    occ_rooms = occ_rooms + res_line.zimmeranz
        else:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == datum) & (Genstat.zinr != "") & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zikatnr == zimkateg.zikatnr)).order_by(Genstat._recid).all():
                occ_rooms = occ_rooms + 1


    def cal_method0a():

        nonlocal occ_rooms, use_it, ci_date, tot_occ_rooms, rmcat_rooms, total_rooms, occ_rooms_1, i_method, d_occupancy, calc_rm, res_line, zimkateg, htparam, zimmer, genstat, zkstat
        nonlocal datum, rmtype, global_occ

        zkbuff = None
        Zkbuff =  create_buffer("Zkbuff",Zimkateg)

        if datum >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)).order_by(Res_line._recid).all():

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
                use_it = (zkbuff.typ == zimkateg.typ)

                if use_it:

                    if res_line.ankunft == res_line.abreise:
                        use_it = (res_line.zipreis > 0)

                    if res_line.abreise > res_line.ankunft and res_line.abreise == datum:
                        use_it = False

                if use_it and res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                    if zimmer and not zimmer.sleeping:
                        use_it = False

                if use_it:
                    occ_rooms = occ_rooms + res_line.zimmeranz
        else:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == datum) & (Genstat.zinr != "") & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                if zkbuff.typ == zimkateg.typ:
                    occ_rooms = occ_rooms + 1


    def cal_method1():

        nonlocal occ_rooms, use_it, ci_date, tot_occ_rooms, rmcat_rooms, total_rooms, occ_rooms_1, i_method, d_occupancy, calc_rm, res_line, zimkateg, htparam, zimmer, genstat, zkstat
        nonlocal datum, rmtype, global_occ

        zkbuff = None
        Zkbuff =  create_buffer("Zkbuff",Zimkateg)

        if zimkateg and zimkateg.typ != 0:
            cal_method1a()

            return

        if datum >= ci_date:

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.sleeping)).order_by(Zimmer._recid).all():

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
                total_rooms = total_rooms + 1

                if zkbuff.kurzbez == rmtype:
                    rmcat_rooms = rmcat_rooms + 1

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)).order_by(Res_line._recid).all():
                use_it = True

                if res_line.ankunft == res_line.abreise:
                    use_it = (res_line.zipreis > 0)

                if res_line.abreise > res_line.ankunft and res_line.abreise == datum:
                    use_it = False

                if use_it and res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                    if zimmer and not zimmer.sleeping:
                        use_it = False

                if use_it:
                    tot_occ_rooms = tot_occ_rooms + res_line.zimmeranz

            if global_occ:
                occ_rooms_1 = tot_occ_rooms
            else:
                occ_rooms_1 = round(tot_occ_rooms * rmcat_rooms / total_rooms, 0)
        else:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
                total_rooms = total_rooms + zkstat.anz100

                if zimkateg and zkstat.zikatnr == zimkateg.zikatnr:
                    rmcat_rooms = rmcat_rooms + zkstat.anz100

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == datum) & (Genstat.zinr != "") & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                tot_occ_rooms = tot_occ_rooms + 1

            if global_occ:
                occ_rooms_1 = tot_occ_rooms
            else:
                occ_rooms_1 = round(tot_occ_rooms * rmcat_rooms / total_rooms, 0)


    def cal_method1a():

        nonlocal occ_rooms, use_it, ci_date, tot_occ_rooms, rmcat_rooms, total_rooms, occ_rooms_1, i_method, d_occupancy, calc_rm, res_line, zimkateg, htparam, zimmer, genstat, zkstat
        nonlocal datum, rmtype, global_occ

        zkbuff = None
        Zkbuff =  create_buffer("Zkbuff",Zimkateg)

        if datum >= ci_date:

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.sleeping)).order_by(Zimmer._recid).all():

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
                total_rooms = total_rooms + 1

                if zkbuff.typ == zimkateg.typ:
                    rmcat_rooms = rmcat_rooms + 1

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)).order_by(Res_line._recid).all():
                use_it = True

                if res_line.ankunft == res_line.abreise:
                    use_it = (res_line.zipreis > 0)

                if res_line.abreise > res_line.ankunft and res_line.abreise == datum:
                    use_it = False

                if use_it and res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                    if zimmer and not zimmer.sleeping:
                        use_it = False

                if use_it:
                    tot_occ_rooms = tot_occ_rooms + res_line.zimmeranz

            if global_occ:
                occ_rooms_1 = tot_occ_rooms
            else:
                occ_rooms_1 = round(tot_occ_rooms * rmcat_rooms / total_rooms, 0)
        else:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
                total_rooms = total_rooms + zkstat.anz100

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zkstat.zikatnr)]})

                if zkbuff.typ == zimkateg.typ:
                    rmcat_rooms = rmcat_rooms + zkstat.anz100

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == datum) & (Genstat.zinr != "") & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                tot_occ_rooms = tot_occ_rooms + 1

            if global_occ:
                occ_rooms_1 = tot_occ_rooms
            else:
                occ_rooms_1 = round(tot_occ_rooms * rmcat_rooms / total_rooms, 0)


    def cal_method2():

        nonlocal occ_rooms, use_it, ci_date, tot_occ_rooms, rmcat_rooms, total_rooms, occ_rooms_1, i_method, d_occupancy, calc_rm, res_line, zimkateg, htparam, zimmer, genstat, zkstat
        nonlocal datum, rmtype, global_occ

        zkbuff = None
        Zkbuff =  create_buffer("Zkbuff",Zimkateg)

        if zimkateg and zimkateg.typ != 0:
            cal_method2a()

            return

        if datum >= ci_date:

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.sleeping)).order_by(Zimmer._recid).all():

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
                total_rooms = total_rooms + 1

                if zkbuff.typ == zimkateg.typ:
                    rmcat_rooms = rmcat_rooms + 1

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)).order_by(Res_line._recid).all():
                use_it = True

                if res_line.ankunft == res_line.abreise:
                    use_it = (res_line.zipreis > 0)

                if res_line.abreise > res_line.ankunft and res_line.abreise == datum:
                    use_it = False

                if use_it and res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                    if zimmer:

                        if not zimmer.sleeping:
                            use_it = False
                        else:

                            zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                            if zkbuff.typ == zimkateg.typ:
                                use_it = True
                            else:
                                use_it = False

                if use_it:
                    tot_occ_rooms = tot_occ_rooms + res_line.zimmeranz
            occ_rooms_1 = tot_occ_rooms


        else:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
                total_rooms = total_rooms + zkstat.anz100

                if zkbuff.typ == zimkateg.typ:
                    rmcat_rooms = rmcat_rooms + zkstat.anz100

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == datum) & (Genstat.zinr != "") & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

                if zimmer:

                    if not zimmer.sleeping:
                        use_it = False
                    else:

                        zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                        if zkbuff.typ == zimkateg.typ:
                            use_it = True
                        else:
                            use_it = False

                if use_it:
                    tot_occ_rooms = tot_occ_rooms + 1


            occ_rooms_1 = tot_occ_rooms


    def cal_method2a():

        nonlocal occ_rooms, use_it, ci_date, tot_occ_rooms, rmcat_rooms, total_rooms, occ_rooms_1, i_method, d_occupancy, calc_rm, res_line, zimkateg, htparam, zimmer, genstat, zkstat
        nonlocal datum, rmtype, global_occ

        zkbuff = None
        Zkbuff =  create_buffer("Zkbuff",Zimkateg)

        if datum >= ci_date:

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.sleeping)).order_by(Zimmer._recid).all():

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
                total_rooms = total_rooms + 1

                if zkbuff.typ == zimkateg.typ:
                    rmcat_rooms = rmcat_rooms + 1

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)).order_by(Res_line.zinr).all():
                use_it = True

                if res_line.ankunft == res_line.abreise:
                    use_it = (res_line.zipreis > 0)

                if res_line.abreise > res_line.ankunft and res_line.abreise == datum:
                    use_it = False

                if use_it and res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                    if zimmer:

                        if not zimmer.sleeping:
                            use_it = False
                        else:

                            zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                            if zkbuff.typ == zimkateg.typ:
                                use_it = True
                            else:
                                use_it = False

                if use_it:
                    tot_occ_rooms = tot_occ_rooms + res_line.zimmeranz
            occ_rooms_1 = tot_occ_rooms


        else:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
                total_rooms = total_rooms + zkstat.anz100

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zkstat.zikatnr)]})

                if zkbuff.typ == zimkateg.typ:
                    rmcat_rooms = rmcat_rooms + zkstat.anz100

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum == datum) & (Genstat.zinr != "") & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

                if zimmer:

                    if not zimmer.sleeping:
                        use_it = False
                    else:

                        zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                        if zkbuff.typ == zimkateg.typ:
                            use_it = True
                        else:
                            use_it = False

                if use_it:
                    tot_occ_rooms = tot_occ_rooms + 1


            occ_rooms_1 = tot_occ_rooms

    res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(le, 6),(ne, 3),(ne, 4)],"ankunft": [(gt, datum)],"abreise": [(le, datum)]})

    if not res_line:

        return generate_output()
    ci_date = get_output(htpdate(87))

    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 439)]})

    if htparam.feldtyp == 1 and htparam.finteger <= 2:
        i_method = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 459)]})

    if htparam:
        calc_rm = htparam.flogical

    if calc_rm == False:

        if i_method == 0:
            cal_method0()

        elif i_method == 1:
            cal_method1()
            occ_rooms = occ_rooms_1

        elif i_method == 2:
            cal_method0()
            cal_method1()

            if occ_rooms_1 > occ_rooms:
                occ_rooms = occ_rooms_1

    elif calc_rm :
        cal_method2()
        occ_rooms = occ_rooms_1

    return generate_output()