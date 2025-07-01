#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Guest, Genstat

def rm_productbyratebl(to_date:date):

    prepare_cache ([Queasy, Guest, Genstat])

    tlist_list = []
    s:string = ""
    curr_code:string = ""
    do_it:bool = False
    counter:int = 0
    tot_rmrev:Decimal = to_decimal("0.0")
    tot_arr:Decimal = to_decimal("0.0")
    tot_rmsold:Decimal = to_decimal("0.0")
    tot_fbrev:Decimal = to_decimal("0.0")
    tot_proz:Decimal = to_decimal("0.0")
    tot_mrmrev:Decimal = to_decimal("0.0")
    tot_marr:Decimal = to_decimal("0.0")
    tot_mrmsold:Decimal = to_decimal("0.0")
    tot_mfbrev:Decimal = to_decimal("0.0")
    tot_mproz:Decimal = to_decimal("0.0")
    tot_yrmrev:Decimal = to_decimal("0.0")
    tot_yarr:Decimal = to_decimal("0.0")
    tot_yrmsold:Decimal = to_decimal("0.0")
    tot_yfbrev:Decimal = to_decimal("0.0")
    tot_yproz:Decimal = to_decimal("0.0")
    fdate:date = None
    queasy = guest = genstat = None

    tlist = tmp_room = bqueasy = None

    tlist_list, Tlist = create_model("Tlist", {"nr":int, "ratecode":string, "bezeich":string, "rm_rev":Decimal, "arr":Decimal, "rm_sold":Decimal, "fbrev":Decimal, "proz":Decimal, "mrm_rev":Decimal, "marr":Decimal, "mrm_sold":Decimal, "mfbrev":Decimal, "mproz":Decimal, "yrm_rev":Decimal, "yarr":Decimal, "yrm_sold":Decimal, "yfbrev":Decimal, "yproz":Decimal})
    tmp_room_list, Tmp_room = create_model("Tmp_room", {"gastnr":int, "zinr":string, "flag":int})

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tlist_list, s, curr_code, do_it, counter, tot_rmrev, tot_arr, tot_rmsold, tot_fbrev, tot_proz, tot_mrmrev, tot_marr, tot_mrmsold, tot_mfbrev, tot_mproz, tot_yrmrev, tot_yarr, tot_yrmsold, tot_yfbrev, tot_yproz, fdate, queasy, guest, genstat
        nonlocal to_date
        nonlocal bqueasy


        nonlocal tlist, tmp_room, bqueasy
        nonlocal tlist_list, tmp_room_list

        return {"tlist": tlist_list}

    fdate = date_mdy(1, 1, get_year(to_date))


    tot_rmrev =  to_decimal("0")
    tot_arr =  to_decimal("0")
    tot_rmsold =  to_decimal("0")
    tot_fbrev =  to_decimal("0")
    tot_proz =  to_decimal("0")
    tot_mrmrev =  to_decimal("0")
    tot_marr =  to_decimal("0")
    tot_mrmsold =  to_decimal("0")
    tot_mfbrev =  to_decimal("0")
    tot_mproz =  to_decimal("0")
    tot_yrmrev =  to_decimal("0")
    tot_yarr =  to_decimal("0")
    tot_yrmsold =  to_decimal("0")
    tot_yfbrev =  to_decimal("0")
    tot_yproz =  to_decimal("0")

    genstat_obj_list = {}
    genstat = Genstat()
    guest = Guest()
    for genstat.logis, genstat.gastnr, genstat.zinr, genstat.res_deci, genstat.datum, genstat._recid, guest.gastnr, guest._recid in db_session.query(Genstat.logis, Genstat.gastnr, Genstat.zinr, Genstat.res_deci, Genstat.datum, Genstat._recid, Guest.gastnr, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
             (Genstat.datum >= fdate) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr).all():
        if genstat_obj_list.get(genstat._recid):
            continue
        else:
            genstat_obj_list[genstat._recid] = True


        do_it = True

        queasy = get_cache (Queasy, {"key": [(eq, 212)],"number3": [(eq, guest.gastnr)]})

        if queasy:

            bqueasy = get_cache (Queasy, {"key": [(eq, 211)],"number1": [(eq, queasy.number1)]})

            if bqueasy:
                curr_code = bqueasy.char1


            else:
                curr_code = "UNKNOWN"
        else:
            curr_code = "UNKNOWN"

        if do_it :

            tlist = query(tlist_list, filters=(lambda tlist: tlist.ratecode.lower()  == (curr_code).lower()), first=True)

            if not tlist:
                tlist = Tlist()
                tlist_list.append(tlist)

                tlist.ratecode = curr_code
                tlist.bezeich = curr_code

            if genstat.datum == to_date:
                tlist.rm_rev =  to_decimal(tlist.rm_rev) + to_decimal(genstat.logis)
                tot_rmrev =  to_decimal(tot_rmrev) + to_decimal(genstat.logis)

                tmp_room = query(tmp_room_list, filters=(lambda tmp_room: tmp_room.gastnr == genstat.gastnr and tmp_room.zinr == genstat.zinr and tmp_room.flag == 1), first=True)

                if not tmp_room:
                    tlist.rm_sold =  to_decimal(tlist.rm_sold) + to_decimal("1")
                    tot_rmsold =  to_decimal(tot_rmsold) + to_decimal("1")


                    tmp_room = Tmp_room()
                    tmp_room_list.append(tmp_room)

                    tmp_room.gastnr = genstat.gastnr
                    tmp_room.zinr = genstat.zinr
                    tmp_room.flag = 1


                tlist.fbrev =  to_decimal(tlist.fbrev) + to_decimal((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) )
                tot_fbrev =  to_decimal(tot_fbrev) + to_decimal((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) )

            if get_month(genstat.datum) == get_month(to_date):
                tlist.mrm_rev =  to_decimal(tlist.mrm_rev) + to_decimal(genstat.logis)
                tlist.mrm_sold =  to_decimal(tlist.mrm_sold) + to_decimal("1")
                tlist.mfbrev =  to_decimal(tlist.mfbrev) + to_decimal((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) )
                tot_mrmrev =  to_decimal(tot_mrmrev) + to_decimal(genstat.logis)
                tot_mrmsold =  to_decimal(tot_mrmsold) + to_decimal("1")
                tot_mfbrev =  to_decimal(tot_mfbrev) + to_decimal((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) )


            tlist.yrm_rev =  to_decimal(tlist.yrm_rev) + to_decimal(genstat.logis)
            tlist.yrm_sold =  to_decimal(tlist.yrm_sold) + to_decimal("1")
            tlist.yfbrev =  to_decimal(tlist.yfbrev) + to_decimal((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) )
            tot_yrmrev =  to_decimal(tot_yrmrev) + to_decimal(genstat.logis)
            tot_yrmsold =  to_decimal(tot_yrmsold) + to_decimal("1")
            tot_yfbrev =  to_decimal(tot_yfbrev) + to_decimal((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) )

    for tlist in query(tlist_list):
        tlist.arr =  to_decimal(tlist.rm_rev) / to_decimal(tlist.rm_sold)
        tlist.marr =  to_decimal(tlist.mrm_rev) / to_decimal(tlist.mrm_sold)
        tlist.yarr =  to_decimal(tlist.yrm_rev) / to_decimal(tlist.yrm_sold)

        if tlist.arr == None:
            tlist.arr =  to_decimal("0")

        if tlist.marr == None:
            tlist.marr =  to_decimal("0")

        if tlist.yarr == None:
            tlist.yarr =  to_decimal("0")
        tot_arr =  to_decimal(tot_arr) + to_decimal(tlist.arr)
        tot_marr =  to_decimal(tot_marr) + to_decimal(tlist.marr)
        tot_yarr =  to_decimal(tot_yarr) + to_decimal(tlist.yarr)
        tlist.proz = ( to_decimal(tlist.rm_rev) / to_decimal(tot_rmrev)) * to_decimal("100")
        tlist.mproz = ( to_decimal(tlist.mrm_rev) / to_decimal(tot_mrmrev)) * to_decimal("100")
        tlist.yproz = ( to_decimal(tlist.yrm_rev) / to_decimal(tot_yrmrev)) * to_decimal("100")

        if tlist.proz == None:
            tlist.proz =  to_decimal("0")

        if tlist.mproz == None:
            tlist.mproz =  to_decimal("0")

        if tlist.yproz == None:
            tlist.yproz =  to_decimal("0")
        tot_proz =  to_decimal(tot_proz) + to_decimal(tlist.proz)
        tot_mproz =  to_decimal(tot_mproz) + to_decimal(tlist.mproz)
        tot_yproz =  to_decimal(tot_yproz) + to_decimal(tlist.yproz)

    for tlist in query(tlist_list, sort_by=[("bezeich",False)]):
        counter = counter + 1
        tlist.nr = counter


    tlist = Tlist()
    tlist_list.append(tlist)

    counter = counter + 1
    tlist.nr = counter
    tlist.bezeich = "T O T A L"
    tlist.rm_rev =  to_decimal(tot_rmrev)
    tlist.arr =  to_decimal(tot_arr)
    tlist.rm_sold =  to_decimal(tot_rmsold)
    tlist.fbrev =  to_decimal(tot_fbrev)
    tlist.proz =  to_decimal(tot_proz)
    tlist.mrm_rev =  to_decimal(tot_mrmrev)
    tlist.marr =  to_decimal(tot_marr)
    tlist.mrm_sold =  to_decimal(tot_mrmsold)
    tlist.mfbrev =  to_decimal(tot_mfbrev)
    tlist.mproz =  to_decimal(tot_mproz)
    tlist.yrm_rev =  to_decimal(tot_yrmrev)
    tlist.yarr =  to_decimal(tot_yarr)
    tlist.yrm_sold =  to_decimal(tot_yrmsold)
    tlist.yfbrev =  to_decimal(tot_yfbrev)
    tlist.yproz =  to_decimal(tot_yproz)

    return generate_output()