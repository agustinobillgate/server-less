from functions.additional_functions import *
import decimal
from datetime import date
from functions.hk_rmboy_rmlist_1bl import hk_rmboy_rmlist_1bl

def auto_room_maidlistbl(loc_combo:str, stat1:str, stat2:str, stat3:str, stat4:str, fr_floor:int, to_floor:int, pax:int):
    rmlist_list = []
    credit:int = 0
    resbemerk:str = ""
    count_i:int = 0

    rmlist = temp_loc = None

    rmlist_list, Rmlist = create_model("Rmlist", {"flag":int, "code":str, "zinr":str, "credit":int, "floor":int, "gname":str, "pic":str, "bemerk":str, "rstat":str, "ankunft":date, "abreise":date, "kbezeich":str, "nation":str, "paxnr":int})
    temp_loc_list, Temp_loc = create_model("Temp_loc", {"t_loc":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmlist_list, credit, resbemerk, count_i
        nonlocal loc_combo, stat1, stat2, stat3, stat4, fr_floor, to_floor, pax


        nonlocal rmlist, temp_loc
        nonlocal rmlist_list, temp_loc_list
        return {"rmlist": rmlist_list}

    def create_rmlist():

        nonlocal rmlist_list, credit, resbemerk, count_i
        nonlocal loc_combo, stat1, stat2, stat3, stat4, fr_floor, to_floor, pax


        nonlocal rmlist, temp_loc
        nonlocal rmlist_list, temp_loc_list


        credit, rmlist_list = get_output(hk_rmboy_rmlist_1bl(loc_combo, stat1, stat2, stat3, stat4, fr_floor, to_floor))


    def create_browse():

        nonlocal rmlist_list, credit, resbemerk, count_i
        nonlocal loc_combo, stat1, stat2, stat3, stat4, fr_floor, to_floor, pax


        nonlocal rmlist, temp_loc
        nonlocal rmlist_list, temp_loc_list

        each_credit:decimal = to_decimal("0.0")
        n:int = 1
        pnt:decimal = to_decimal("0.0")
        pers_str:str = ""

        if to_decimal(pax) != 0 and to_decimal(pax) != None:
            each_credit =  to_decimal(to_decimal(credit)) / to_decimal(to_decimal(pax))
        pers_str = "Person"

        for rmlist in query(rmlist_list, filters=(lambda rmlist: rmlist.zinr != ''), sort_by=[("floor",False),("zinr",False)]):
            pnt =  to_decimal(pnt) + to_decimal(rmlist.credit)

            if (pnt > each_credit) and (n < pax):
                n = n + 1
                pnt =  to_decimal("0")
            rmlist.pic = pers_str + " " + to_string(n, ">>9")
            rmlist.paxnr = n


            resbemerk = rmlist.bemerk
            resbemerk = replace_str(resbemerk, chr(10) , "")
            resbemerk = replace_str(resbemerk, chr(13) , "")
            resbemerk = replace_str(resbemerk, "~n", "")
            resbemerk = replace_str(resbemerk, "\\n", "")
            resbemerk = replace_str(resbemerk, "~r", "")
            resbemerk = replace_str(resbemerk, "~r~n", "")
            resbemerk = replace_str(resbemerk, "&nbsp;", " ")
            resbemerk = replace_str(resbemerk, "</p>", "</p></p>")
            resbemerk = replace_str(resbemerk, "</p>", chr(13))
            resbemerk = replace_str(resbemerk, "<BR>", chr(13))
            resbemerk = replace_str(resbemerk, chr(10) + chr(13) , "")

            if len(resbemerk) < 3:
                resbemerk = replace_str(resbemerk, chr(32) , "")

            if len(resbemerk) < 3:
                resbemerk = ""

            if len(resbemerk) == None:
                resbemerk = ""
            for count_i in range(0,31 + 1) :

                if re.match(chr(count_i),resbemerk, re.IGNORECASE):
                    resbemerk = replace_str(resbemerk, chr(count_i) , "")
            for count_i in range(127,255 + 1) :

                if re.match(chr(count_i),resbemerk, re.IGNORECASE):
                    resbemerk = replace_str(resbemerk, chr(count_i) , "")
            rmlist.bemerk = resbemerk


    create_rmlist()
    create_browse()

    return generate_output()