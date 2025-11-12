# using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_ 10/10/2025

    TICKET ID: 79EBDE
    ISSUE:  - Fix variabel = None
            - Fix python indentation
            - add type:ignore to model Datalist, avoid warning cannot assign attribute
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import (
    Nitehist,
    Guest,
    Htparam,
    Nightaudit,
    Zimmer,
    Zimkateg,
    Res_line,
    Guest_pr,
)


def create_table_revinatebl():

    prepare_cache(
        [Nitehist, Guest, Htparam, Nightaudit,
            Zimmer, Zimkateg, Res_line, Guest_pr]
    )

    nite_status: int  # output parameter
    nite_date: date  # ouput parameter
    data_list_data = []  # output parameter
    ci_date: date
    reihenfolge: int
    cidate: string
    codate: string
    loop_i: int
    str_rsv: string
    progname: string = "nt-revinatesurvey.p"
    nitehist = guest = htparam = nightaudit = zimmer = zimkateg = res_line = (
        guest_pr
    ) = None

    data_list = buff_nite = gmember = None

    data_list_data, Data_list = create_model(
        "Data_list",
        {
            "guest_title": string,
            "first_name": string,
            "last_name": string,
            "email": string,
            "nation": string,
            "ci_date": string,
            "co_date": string,
            "rmno": string,
            "rmtype": string,
            "rcode": string,
        },
    )

    Buff_nite = create_buffer("Buff_nite", Nitehist)
    Gmember = create_buffer("Gmember", Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal nite_status, nite_date, data_list_data, ci_date, reihenfolge, cidate, codate, loop_i, str_rsv, progname, nitehist, guest, htparam, nightaudit, zimmer, zimkateg, res_line, guest_pr
        nonlocal buff_nite, gmember

        nonlocal data_list, buff_nite, gmember
        nonlocal data_list_data

        return {
            "nite_status": nite_status,
            "nite_date": nite_date,
            "data-list": data_list_data,
        }

    def find_inhouse_guests():
        nonlocal nite_status, nite_date, data_list_data, ci_date, reihenfolge, cidate, codate, loop_i, str_rsv, progname, nitehist, guest, htparam, nightaudit, zimmer, zimkateg, res_line, guest_pr
        nonlocal buff_nite, gmember

        nonlocal data_list, buff_nite, gmember
        nonlocal data_list_data

        res_line_obj_list = {}
        res_line = Res_line()
        gmember = Guest()
        for (
            res_line.zinr,
            res_line.ankunft,
            res_line.abreise,
            res_line.zimmer_wunsch,
            res_line.gastnr,
            res_line._recid,
            gmember.anrede1,
            gmember.vorname1,
            gmember.name,
            gmember.email_adr,
            gmember.nation1,
            gmember._recid,
        ) in (
            db_session.query(
            Res_line.zinr,
            Res_line.ankunft,
            Res_line.abreise,
            Res_line.zimmer_wunsch,
            Res_line.gastnr,
            Res_line._recid,
            Gmember.anrede1,
            Gmember.vorname1,
            Gmember.name,
            Gmember.email_adr,
            Gmember.nation1,
            Gmember._recid,
            ).join(Gmember, (Gmember.gastnr == Res_line.gastnrmember)).filter(
            (Res_line.ankunft == ci_date)
            & (Res_line.resstatus == 6)
            & (Res_line.zipreis != 0)
            ).order_by(Res_line.ankunft, Res_line.name, Res_line.zinr).all()
        ):
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

                data_list = Data_list()
                data_list_data.append(data_list)

                data_list.guest_title = gmember.anrede1  
                data_list.first_name = gmember.vorname1  
                data_list.last_name = gmember.name  
                data_list.email = gmember.email_adr  
                data_list.nation = gmember.nation1  
                data_list.rmno = res_line.zinr  
                data_list.ci_date = str(to_string(get_month(res_line.ankunft), "99")) + "/"  + str(to_string(get_day(res_line.ankunft), "99")) + "/" + str(to_string(get_year(res_line.ankunft), "9999"))
                data_list.co_date = str(to_string(get_month(res_line.abreise), "99")) + "/"  + str(to_string(get_day(res_line.abreise), "99")) + "/" + str(to_string(get_year(res_line.abreise), "9999"))

                zimmer = get_cache(Zimmer, {
                    "zinr": [(eq, data_list.rmno)]}) 

                if zimmer:
                    zimkateg = get_cache(
                    Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                    if zimkateg:
                        data_list.rmtype = zimkateg.kurzbez 
                        for loop_i in range(1, int(str(num_entries(res_line.zimmer_wunsch, ";"))) - 1 + 1): 
                            str_rsv = str(entry(loop_i - 1, res_line.zimmer_wunsch, ";")) 

                    if str(substring(str_rsv, 0, 6)) == ("$code$"): 
                        data_list.rcode = substring(str_rsv, 6) 

                if str(data_list.rcode) == "": 

                    guest_pr = get_cache(Guest_pr, {
                        "gastnr": [(eq, res_line.gastnr)]})

                    if guest_pr:
                        data_list.rcode = guest_pr.code 
                    nite_status = 2
                    nite_date = ci_date
                    data_list.guest_title = replace_str( 
                        data_list.guest_title, chr_unicode(44), chr_unicode(46) 
                    )
                    data_list.first_name = replace_str( 
                        data_list.first_name, chr_unicode(44), chr_unicode(46) 
                    )
                    data_list.last_name = replace_str( 
                        data_list.last_name, chr_unicode(44), chr_unicode(46) 
                    )
                    data_list.email = replace_str( 
                        data_list.email, chr_unicode(44), chr_unicode(46) 
                    )

    htparam = get_cache(Htparam, {
        "paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    nightaudit = get_cache(Nightaudit, {
        "programm": [(eq, progname)]})

    if not nightaudit:
        return generate_output()
    
    reihenfolge = nightaudit.reihenfolge
    nite_status = 0

    nitehist = get_cache(
        Nitehist, {
            "reihenfolge": [(eq, reihenfolge)], 
            "line": [(eq, "send|0")]}
    )

    if nitehist:
        nite_status = 1
        nite_date = nitehist.datum

        for buff_nite in (
            db_session.query(Buff_nite)
            .filter(
                (Buff_nite.reihenfolge == reihenfolge)
                & (Buff_nite.datum == nite_date)
                & (entry(0, Buff_nite.line, "|") != ("SEND").lower())
            )
            .order_by(Buff_nite._recid)
            .all()
        ):
            data_list = Data_list()
            data_list_data.append(data_list)

            data_list.guest_title = entry(0, buff_nite.line, "|") 
            data_list.first_name = entry(1, buff_nite.line, "|") 
            data_list.last_name = entry(2, buff_nite.line, "|") 
            data_list.email = entry(4, buff_nite.line, "|") 
            data_list.nation = entry(5, buff_nite.line, "|") 
            data_list.ci_date = entry(6, buff_nite.line, "|") 
            data_list.co_date = entry(7, buff_nite.line, "|") 
            data_list.rmno = entry(8, buff_nite.line, "|") 
            data_list.rcode = entry(14, buff_nite.line, "|") 

            zimmer = get_cache(Zimmer, {
                "zinr": [(eq, data_list.rmno)]}) 

            if zimmer:

                zimkateg = get_cache(
                    Zimkateg, {
                        "zikatnr": [(eq, zimmer.zikatnr)]})

                if zimkateg:
                    data_list.rmtype = zimkateg.kurzbez 

    elif not nitehist:
        nite_status = 0

    if nite_status == 0:
        find_inhouse_guests()

    return generate_output()
