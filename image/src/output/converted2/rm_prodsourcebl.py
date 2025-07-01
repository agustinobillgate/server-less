#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Sourccod, Guest, Genstat

def rm_prodsourcebl(source_name:string, ytd_flag:bool, incl_comp:bool, fr_date:date, to_date:date):

    prepare_cache ([Sourccod, Guest, Genstat])

    flag = 0
    output_list_list = []
    tot_dlodge:Decimal = to_decimal("0.0")
    tot_mlodge:Decimal = to_decimal("0.0")
    tot_ylodge:Decimal = to_decimal("0.0")
    tot_dnite:int = 0
    tot_mnite:int = 0
    tot_ynite:int = 0
    tot_drate:Decimal = to_decimal("0.0")
    tot_mrate:Decimal = to_decimal("0.0")
    tot_yrate:Decimal = to_decimal("0.0")
    tot1_dlodge:Decimal = to_decimal("0.0")
    tot1_mlodge:Decimal = to_decimal("0.0")
    tot1_ylodge:Decimal = to_decimal("0.0")
    tot1_dnite:int = 0
    tot1_mnite:int = 0
    tot1_ynite:int = 0
    tot1_drate:Decimal = to_decimal("0.0")
    tot1_mrate:Decimal = to_decimal("0.0")
    tot1_yrate:Decimal = to_decimal("0.0")
    sourccod = guest = genstat = None

    output_list = t_list = None

    output_list_list, Output_list = create_model("Output_list", {"gname":string, "flag":bool, "name":string, "dlodge":Decimal, "mlodge":Decimal, "ylodge":Decimal, "dnite":int, "mnite":int, "ynite":int, "drate":Decimal, "mrate":Decimal, "yrate":Decimal})
    t_list_list, T_list = create_model("T_list", {"natnr":int, "nat":string, "counts":int, "tot_nat":int, "flag":bool, "gastnr":int, "name":string, "gname":string, "dlodge":Decimal, "mlodge":Decimal, "ylodge":Decimal, "dnite":int, "mnite":int, "ynite":int, "drate":Decimal, "mrate":Decimal, "yrate":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, output_list_list, tot_dlodge, tot_mlodge, tot_ylodge, tot_dnite, tot_mnite, tot_ynite, tot_drate, tot_mrate, tot_yrate, tot1_dlodge, tot1_mlodge, tot1_ylodge, tot1_dnite, tot1_mnite, tot1_ynite, tot1_drate, tot1_mrate, tot1_yrate, sourccod, guest, genstat
        nonlocal source_name, ytd_flag, incl_comp, fr_date, to_date


        nonlocal output_list, t_list
        nonlocal output_list_list, t_list_list

        return {"flag": flag, "output-list": output_list_list}

    def create_list1():

        nonlocal flag, output_list_list, tot_dlodge, tot_mlodge, tot_ylodge, tot_dnite, tot_mnite, tot_ynite, tot_drate, tot_mrate, tot_yrate, tot1_dlodge, tot1_mlodge, tot1_ylodge, tot1_dnite, tot1_mnite, tot1_ynite, tot1_drate, tot1_mrate, tot1_yrate, sourccod, guest, genstat
        nonlocal source_name, ytd_flag, incl_comp, fr_date, to_date


        nonlocal output_list, t_list
        nonlocal output_list_list, t_list_list

        b:int = 0
        curr_nat:int = 0
        do_it:bool = True
        gbuff = None
        Gbuff =  create_buffer("Gbuff",Guest)

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= fr_date) & (Genstat.datum <= to_date) & (Genstat.source == sourccod.source_code) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            do_it = True

            if not incl_comp:

                if (genstat.erwachs + genstat.kind1) > 0:
                    do_it = True
                else:
                    do_it = False

            if do_it:

                t_list = query(t_list_list, filters=(lambda t_list: t_list.gastnr == genstat.gastnr and t_list.natnr == genstat.source), first=True)

                if not t_list:

                    guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                    if guest:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                        if gbuff:
                            t_list = T_list()
                            t_list_list.append(t_list)

                            t_list.gastnr = genstat.gastnr
                            t_list.name = guest.name + ", " + guest.vorname1 + ", " +\
                                    guest.anrede1 + guest.anredefirma
                            t_list.gname = gbuff.name + ", " + gbuff.vorname1 + ", " +\
                                    gbuff.anrede1 + gbuff.anredefirma
                            t_list.nat = sourccod.bezeich
                            t_list.natnr = genstat.source

                if t_list:

                    if genstat.datum == to_date:
                        t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(genstat.logis)


                        t_list.dnite = t_list.dnite + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        t_list.mlodge =  to_decimal(t_list.mlodge) + to_decimal(genstat.logis)


                        t_list.mnite = t_list.mnite + 1


                    t_list.ylodge =  to_decimal(t_list.ylodge) + to_decimal(genstat.logis)


                    t_list.ynite = t_list.ynite + 1

        for t_list in query(t_list_list):

            if t_list.dnite != 0:
                t_list.drate =  to_decimal(t_list.dlodge) / to_decimal(t_list.dnite)

            if t_list.mnite != 0:
                t_list.mrate =  to_decimal(t_list.mlodge) / to_decimal(t_list.mnite)

            if t_list.ynite != 0:
                t_list.yrate =  to_decimal(t_list.ylodge) / to_decimal(t_list.ynite)


        count_sub()
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.name = "--------------------------------------------------------------"
        output_list.gname = "------------------------>"


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.name = "Total"
        output_list.dlodge =  to_decimal(tot_dlodge)
        output_list.mlodge =  to_decimal(tot_mlodge)
        output_list.ylodge =  to_decimal(tot_ylodge)
        output_list.dnite = tot_dnite
        output_list.mnite = tot_mnite
        output_list.ynite = tot_ynite
        output_list.drate =  to_decimal(tot_drate)
        output_list.mrate =  to_decimal(tot_mrate)
        output_list.yrate =  to_decimal(tot_yrate)


    def create_list2():

        nonlocal flag, output_list_list, tot_dlodge, tot_mlodge, tot_ylodge, tot_dnite, tot_mnite, tot_ynite, tot_drate, tot_mrate, tot_yrate, tot1_dlodge, tot1_mlodge, tot1_ylodge, tot1_dnite, tot1_mnite, tot1_ynite, tot1_drate, tot1_mrate, tot1_yrate, sourccod, guest, genstat
        nonlocal source_name, ytd_flag, incl_comp, fr_date, to_date


        nonlocal output_list, t_list
        nonlocal output_list_list, t_list_list

        b:int = 0
        curr_nat:int = 0
        do_it:bool = True
        gbuff = None
        Gbuff =  create_buffer("Gbuff",Guest)

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= fr_date) & (Genstat.datum <= to_date) & (Genstat.source == sourccod.source_code) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
            do_it = True

            if not incl_comp:

                if (genstat.erwachs + genstat.kind1) > 0:
                    do_it = True
                else:
                    do_it = False

            if do_it:

                t_list = query(t_list_list, filters=(lambda t_list: t_list.gastnr == genstat.gastnr and t_list.natnr == genstat.source), first=True)

                if not t_list:

                    guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                    if guest:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                        if gbuff:
                            t_list = T_list()
                            t_list_list.append(t_list)

                            t_list.gastnr = genstat.gastnr
                            t_list.name = guest.name + ", " + guest.vorname1 + ", " +\
                                    guest.anrede1 + guest.anredefirma
                            t_list.gname = gbuff.name + ", " + gbuff.vorname1 + ", " +\
                                    gbuff.anrede1 + gbuff.anredefirma
                            t_list.nat = sourccod.bezeich
                            t_list.natnr = genstat.source

                if t_list:

                    if genstat.datum == to_date:
                        t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(genstat.logis)


                        t_list.dnite = t_list.dnite + 1


                    t_list.mlodge =  to_decimal(t_list.mlodge) + to_decimal(genstat.logis)


                    t_list.mnite = t_list.mnite + 1


                    t_list.ylodge =  to_decimal(t_list.ylodge) + to_decimal(genstat.logis)


                    t_list.ynite = t_list.ynite + 1

        for t_list in query(t_list_list):

            if t_list.dnite != 0:
                t_list.drate =  to_decimal(t_list.dlodge) / to_decimal(t_list.dnite)

            if t_list.mnite != 0:
                t_list.mrate =  to_decimal(t_list.mlodge) / to_decimal(t_list.mnite)

            if t_list.ynite != 0:
                t_list.yrate =  to_decimal(t_list.ylodge) / to_decimal(t_list.ynite)


        count_sub()
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.name = "--------------------------------------------------------------"
        output_list.gname = "------------------------>"


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.name = "Total"
        output_list.dlodge =  to_decimal(tot_dlodge)
        output_list.mlodge =  to_decimal(tot_mlodge)
        output_list.ylodge =  to_decimal(tot_ylodge)
        output_list.dnite = tot_dnite
        output_list.mnite = tot_mnite
        output_list.ynite = tot_ynite
        output_list.drate =  to_decimal(tot_drate)
        output_list.mrate =  to_decimal(tot_mrate)
        output_list.yrate =  to_decimal(tot_yrate)


    def count_sub():

        nonlocal flag, output_list_list, tot_dlodge, tot_mlodge, tot_ylodge, tot_dnite, tot_mnite, tot_ynite, tot_drate, tot_mrate, tot_yrate, tot1_dlodge, tot1_mlodge, tot1_ylodge, tot1_dnite, tot1_mnite, tot1_ynite, tot1_drate, tot1_mrate, tot1_yrate, sourccod, guest, genstat
        nonlocal source_name, ytd_flag, incl_comp, fr_date, to_date


        nonlocal output_list, t_list
        nonlocal output_list_list, t_list_list

        curr_nat:int = 0

        for t_list in query(t_list_list, sort_by=[("natnr",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.gname = t_list.gname
            output_list.name = t_list.name
            output_list.dlodge =  to_decimal(t_list.dlodge)
            output_list.mlodge =  to_decimal(t_list.mlodge)
            output_list.ylodge =  to_decimal(t_list.ylodge)
            output_list.dnite = t_list.dnite
            output_list.mnite = t_list.mnite
            output_list.ynite = t_list.ynite
            output_list.drate =  to_decimal(t_list.drate)
            output_list.mrate =  to_decimal(t_list.mrate)
            output_list.yrate =  to_decimal(t_list.yrate)


            tot_dlodge =  to_decimal(tot_dlodge) + to_decimal(t_list.dlodge)
            tot_dnite = tot_dnite + t_list.dnite
            tot_mlodge =  to_decimal(tot_mlodge) + to_decimal(t_list.mlodge)
            tot_ylodge =  to_decimal(tot_ylodge) + to_decimal(t_list.ylodge)
            tot_mnite = tot_mnite + t_list.mnite
            tot_ynite = tot_ynite + t_list.ynite
            tot_drate =  to_decimal(tot_drate) + to_decimal(t_list.drate)
            tot_mrate =  to_decimal(tot_mrate) + to_decimal(t_list.mrate)
            tot_yrate =  to_decimal(tot_yrate) + to_decimal(t_list.yrate)

        if tot_dnite != 0:
            tot_drate =  to_decimal(tot_dlodge) / to_decimal(tot_dnite)

        if tot_mnite != 0:
            tot_mrate =  to_decimal(tot_mlodge) / to_decimal(tot_mnite)

        if tot_ynite != 0:
            tot_yrate =  to_decimal(tot_ylodge) / to_decimal(tot_ynite)

    sourccod = get_cache (Sourccod, {"bezeich": [(eq, source_name)]})

    if not sourccod:

        sourccod = db_session.query(Sourccod).filter(
                 (substring(Sourccod.bezeich, 0, length((source_name).lower() )) == (source_name).lower())).first()

    if not sourccod:
        flag = 1

        return generate_output()

    if ytd_flag:
        create_list1()
    else:
        create_list2()

    return generate_output()