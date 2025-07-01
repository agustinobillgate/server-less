#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Zimmer, Res_line, Guest

def hk_rmboy_rmlistbl(loc_combo:string, stat1:string, stat2:string, stat3:string, stat4:string):

    prepare_cache ([Zimmer, Res_line, Guest])

    credit = 0
    rmlist_list = []
    ci_date:date = None
    stat_list:List[string] = create_empty_list(4,"")
    zimmer = res_line = guest = None

    rmlist = None

    rmlist_list, Rmlist = create_model("Rmlist", {"flag":int, "code":string, "zinr":string, "credit":int, "floor":int, "gname":string, "pic":string, "bemerk":string, "rstat":string, "ankunft":date, "abreise":date, "kbezeich":string, "nation":string, "paxnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal credit, rmlist_list, ci_date, stat_list, zimmer, res_line, guest
        nonlocal loc_combo, stat1, stat2, stat3, stat4


        nonlocal rmlist
        nonlocal rmlist_list

        return {"credit": credit, "rmlist": rmlist_list}

    def create_rmlist():

        nonlocal credit, rmlist_list, ci_date, stat_list, zimmer, res_line, guest
        nonlocal loc_combo, stat1, stat2, stat3, stat4


        nonlocal rmlist
        nonlocal rmlist_list

        last_code:string = "1"
        do_it:bool = False
        room = None
        Room =  create_buffer("Room",Zimmer)
        rmlist_list.clear()
        credit = 0

        for room in db_session.query(Room).filter(
                 (Room.zistatus >= 2) & (Room.zistatus <= 4)).order_by(Room._recid).all():

            if loc_combo.lower()  == ("ALL").lower() :
                do_it = True
            else:
                do_it = room.code == loc_combo

            if do_it:
                rmlist = Rmlist()
                rmlist_list.append(rmlist)

                rmlist.code = room.code
                rmlist.zinr = room.zinr
                rmlist.credit = room.reihenfolge
                rmlist.floor = room.etage
                rmlist.rstat = stat_list[room.zistatus - 1]
                rmlist.kbezeich = room.kbezeich

                if rmlist.credit == 0:
                    rmlist.credit = 1

                if room.zistatus == 3 or room.zistatus == 4:

                    res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, room.zinr)]})

                    if res_line:
                        rmlist.bemerk = res_line.bemerk
                        rmlist.ankunft = res_line.ankunft
                        rmlist.abreise = res_line.abreise

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if guest:
                            rmlist.gname = guest.name + ", " + guest.vorname1 +\
                                    " " + guest.anrede1
                            rmlist.nation = guest.nation1

                if room.reihenfolge == 0:
                    credit = credit + 1
                else:
                    credit = credit + room.reihenfolge

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 6) & (Res_line.abreise == ci_date)).order_by(Res_line.zinr).all():

            room = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if loc_combo.lower()  == ("ALL").lower() :
                do_it = True
            else:
                do_it = room.code == loc_combo

            if do_it:

                rmlist = query(rmlist_list, filters=(lambda rmlist: rmlist.zinr == res_line.zinr), first=True)

                if not rmlist:
                    rmlist = Rmlist()
                    rmlist_list.append(rmlist)

                    rmlist.code = room.code
                    rmlist.zinr = room.zinr
                    rmlist.credit = room.reihenfolge
                    rmlist.floor = room.etage
                    rmlist.rstat = stat_list[2]
                    rmlist.kbezeich = room.kbezeich

                    if rmlist.credit == 0:
                        rmlist.credit = 1
                    rmlist.bemerk = res_line.bemerk
                    rmlist.ankunft = res_line.ankunft
                    rmlist.abreise = res_line.abreise

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if guest:
                        rmlist.gname = guest.name + ", " + guest.vorname1 +\
                                " " + guest.anrede1
                        rmlist.nation = guest.nation1

                    if room.reihenfolge == 0:
                        credit = credit + 1
                    else:
                        credit = credit + room.reihenfolge

    stat_list[0] = stat1
    stat_list[1] = stat2
    stat_list[2] = stat3
    stat_list[3] = stat4


    ci_date = get_output(htpdate(87))
    create_rmlist()

    return generate_output()