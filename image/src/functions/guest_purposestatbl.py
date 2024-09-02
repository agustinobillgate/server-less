from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import Guest, Genstat, Res_line, Queasy

def guest_purposestatbl(f_date:date, t_date:date, pur_stay:str, mi_ch:str):
    gmember_list = []
    s:str = ""
    num:int = 0
    number:int = 0
    pur_nr:int = 0
    p_nr:int = 0
    guest = genstat = res_line = queasy = None

    gmember = None

    gmember_list, Gmember = create_model("Gmember", {"nr":int, "name":str, "adresse1":str, "email_adr":str, "ankunft":date, "abreise":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gmember_list, s, num, number, pur_nr, p_nr, guest, genstat, res_line, queasy


        nonlocal gmember
        nonlocal gmember_list
        return {"gmember": gmember_list}

    def disp_arlist():

        nonlocal gmember_list, s, num, number, pur_nr, p_nr, guest, genstat, res_line, queasy


        nonlocal gmember
        nonlocal gmember_list

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                (Genstat.datum >= f_date) &  (Genstat.datum <= t_date) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            res_line = db_session.query(Res_line).filter(
                    (Res_line.gastnrmember == genstat.gastnrmember)).first()

            if res_line:
                p_nr = 0
                for num in range(1,num_entries(genstat.res_char[1], ";")  + 1) :
                    s = entry(num - 1, genstat.res_char[1], ";")

                    if re.match("SEGM__PUR.*",s):
                        p_nr = to_int(substring(s,0 + get_index(s, "SEGM__PUR") + 8))

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 143) &  (func.lower(Queasy.char3) == (pur_stay).lower())).first()

                if queasy:
                    pur_nr = queasy.number1

                if pur_stay.lower()  == "UNKNOWN":
                    pur_nr = 0

                if pur_nr == p_nr:
                    gmember = Gmember()
                    gmember_list.append(gmember)

                    gmember.name = guest.name + guest.anrede1
                    gmember.adresse1 = guest.adresse1
                    gmember.email_adr = guest.email_adr
                    gmember.ankunft = res_line.ankunft
                    gmember.abreise = res_line.abreise


    disp_arlist()

    return generate_output()