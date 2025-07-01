#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimkateg, Res_line, Genstat

def room_product_roomtype_webbl(to_date:date):

    prepare_cache ([Zimkateg, Res_line, Genstat])

    output_list_list = []
    fdate:date = None
    yy:int = 0
    curr_zikatnr:int = 0
    tot_m_anztage:int = 0
    tot_y_anztage:int = 0
    tot_m_logis:Decimal = to_decimal("0.0")
    tot_y_logis:Decimal = to_decimal("0.0")
    tot_m_erwachs:int = 0
    tot_y_erwachs:int = 0
    tot_m_kind:int = 0
    tot_y_kind:int = 0
    tot_m_avrg_logis:Decimal = to_decimal("0.0")
    tot_y_avrg_logis:Decimal = to_decimal("0.0")
    tot_m_room_resv:int = 0
    tot_y_room_resv:int = 0
    curr_m_resnr:int = 0
    curr_y_resnr:int = 0
    curr_m_reslinnr:int = 0
    curr_y_reslinnr:int = 0
    t_m_anztage:int = 0
    t_y_anztage:int = 0
    t_m_logis:Decimal = to_decimal("0.0")
    t_y_logis:Decimal = to_decimal("0.0")
    t_m_erwachs:int = 0
    t_y_erwachs:int = 0
    t_m_kind:int = 0
    t_y_kind:int = 0
    t_m_room_resv:int = 0
    t_y_room_resv:int = 0
    t_m_los:Decimal = to_decimal("0.0")
    t_y_los:Decimal = to_decimal("0.0")
    t_m_avrg_logis:Decimal = to_decimal("0.0")
    t_y_avrg_logis:Decimal = to_decimal("0.0")
    zimkateg = res_line = genstat = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"zikatnr":int, "kurzbez":string, "bezeichnung":string, "m_anztage":int, "y_anztage":int, "m_logis":Decimal, "y_logis":Decimal, "m_los":Decimal, "y_los":Decimal, "m_erwachs":int, "y_erwachs":int, "m_kind":int, "y_kind":int, "m_avrg_logis":Decimal, "y_avrg_logis":Decimal, "m_resv":int, "y_resv":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, fdate, yy, curr_zikatnr, tot_m_anztage, tot_y_anztage, tot_m_logis, tot_y_logis, tot_m_erwachs, tot_y_erwachs, tot_m_kind, tot_y_kind, tot_m_avrg_logis, tot_y_avrg_logis, tot_m_room_resv, tot_y_room_resv, curr_m_resnr, curr_y_resnr, curr_m_reslinnr, curr_y_reslinnr, t_m_anztage, t_y_anztage, t_m_logis, t_y_logis, t_m_erwachs, t_y_erwachs, t_m_kind, t_y_kind, t_m_room_resv, t_y_room_resv, t_m_los, t_y_los, t_m_avrg_logis, t_y_avrg_logis, zimkateg, res_line, genstat
        nonlocal to_date


        nonlocal output_list
        nonlocal output_list_list

        return {"output-list": output_list_list}


    yy = get_year(to_date)
    fdate = date_mdy(1, 1, yy)
    tot_m_anztage = 0
    tot_y_anztage = 0
    tot_m_logis =  to_decimal(0.0)
    tot_y_logis =  to_decimal(0.0)
    tot_m_erwachs = 0
    tot_y_erwachs = 0
    tot_m_kind = 0
    tot_y_kind = 0
    tot_m_room_resv = 0
    tot_y_room_resv = 0
    t_m_anztage = 0
    t_y_anztage = 0
    t_m_logis =  to_decimal("0")
    t_y_logis =  to_decimal("0")
    t_m_erwachs = 0
    t_y_erwachs = 0
    t_m_kind = 0
    t_y_kind = 0
    t_m_room_resv = 0
    t_y_room_resv = 0
    t_m_los =  to_decimal("0")
    t_y_los =  to_decimal("0")
    t_m_avrg_logis =  to_decimal("0")
    t_y_avrg_logis =  to_decimal("0")
    curr_m_resnr = -1
    curr_y_resnr = -1
    curr_zikatnr = -1

    genstat_obj_list = {}
    genstat = Genstat()
    zimkateg = Zimkateg()
    res_line = Res_line()
    for genstat.logis, genstat.erwachs, genstat.gratis, genstat.kind1, genstat.kind2, genstat.resnr, genstat.res_int, genstat.datum, genstat._recid, zimkateg.zikatnr, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, res_line.reslinnr, res_line._recid in db_session.query(Genstat.logis, Genstat.erwachs, Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat.resnr, Genstat.res_int, Genstat.datum, Genstat._recid, Zimkateg.zikatnr, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Res_line.reslinnr, Res_line._recid).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)])).filter(
             (Genstat.datum >= fdate) & (Genstat.datum <= to_date) & (Genstat.zikatnr != 0)).order_by(Zimkateg.zikatnr, Genstat.resnr, Genstat.res_int[inc_value(0)]).all():
        if genstat_obj_list.get(genstat._recid):
            continue
        else:
            genstat_obj_list[genstat._recid] = True

        if curr_zikatnr != zimkateg.zikatnr and output_list:
            output_list.m_anztage = tot_m_anztage
            output_list.y_anztage = tot_y_anztage
            output_list.m_logis =  to_decimal(tot_m_logis)
            output_list.y_logis =  to_decimal(tot_y_logis)
            output_list.m_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
            output_list.y_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
            output_list.m_erwachs = tot_m_erwachs
            output_list.y_erwachs = tot_y_erwachs
            output_list.m_kind = tot_m_kind
            output_list.y_kind = tot_y_kind
            output_list.m_resv = tot_m_room_resv
            output_list.y_resv = tot_y_room_resv


            t_m_anztage = t_m_anztage + tot_m_anztage
            t_y_anztage = t_y_anztage + tot_y_anztage
            t_m_logis =  to_decimal(t_m_logis) + to_decimal(tot_m_logis)
            t_y_logis =  to_decimal(t_y_logis) + to_decimal(tot_y_logis)
            t_m_erwachs = t_m_erwachs + tot_m_erwachs
            t_y_erwachs = t_y_erwachs + tot_y_erwachs
            t_m_kind = t_m_kind + tot_m_kind
            t_y_kind = t_y_kind + tot_y_kind
            t_m_room_resv = t_m_room_resv + tot_m_room_resv
            t_y_room_resv = t_y_room_resv + tot_y_room_resv
            t_m_los =  to_decimal(t_m_los) + to_decimal((tot_m_anztage) / to_decimal(tot_m_room_resv))
            t_y_los =  to_decimal(t_y_los) + to_decimal((tot_y_anztage) / to_decimal(tot_y_room_resv))

            if tot_m_logis == 0.0:
                output_list.m_avrg_logis =  to_decimal(0.0)
                t_m_avrg_logis =  to_decimal(t_m_avrg_logis) + to_decimal(0.0)


            else:
                output_list.m_avrg_logis =  to_decimal(tot_m_logis) / to_decimal(tot_m_anztage)
                t_m_avrg_logis =  to_decimal(t_m_avrg_logis) + to_decimal((tot_m_logis) / to_decimal(tot_m_anztage) )

            if tot_y_logis == 0.0:
                output_list.y_avrg_logis =  to_decimal(0.0)
                t_y_avrg_logis =  to_decimal(t_y_avrg_logis) + to_decimal(0.0)


            else:
                output_list.y_avrg_logis =  to_decimal(tot_y_logis) / to_decimal(tot_y_anztage)
                t_y_avrg_logis =  to_decimal(t_y_avrg_logis) + to_decimal((tot_y_logis) / to_decimal(tot_y_anztage) )


            tot_m_anztage = 0
            tot_y_anztage = 0
            tot_m_logis =  to_decimal(0.0)
            tot_y_logis =  to_decimal(0.0)
            tot_m_erwachs = 0
            tot_y_erwachs = 0
            tot_m_kind = 0
            tot_y_kind = 0
            tot_m_room_resv = 0
            tot_y_room_resv = 0

        output_list = query(output_list_list, filters=(lambda output_list: output_list.zikatnr == zimkateg.zikatnr and output_list.kurzbez == zimkateg.kurzbez), first=True)

        if not output_list:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.zikatnr = zimkateg.zikatnr
            output_list.kurzbez = zimkateg.kurzbez
            output_list.bezeichnung = zimkateg.bezeichnung


            curr_zikatnr = zimkateg.zikatnr
            curr_m_resnr = -1
            curr_y_resnr = -1

        if get_month(genstat.datum) == get_month(to_date):
            tot_m_anztage = tot_m_anztage + 1
            tot_m_logis =  to_decimal(tot_m_logis) + to_decimal(genstat.logis)
            tot_m_erwachs = tot_m_erwachs + to_int(genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2)
            tot_m_kind = tot_m_kind + to_int(genstat.kind1 + genstat.kind2)

            if curr_m_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
                tot_m_room_resv = tot_m_room_resv + 1
                curr_m_reslinnr = res_line.reslinnr
                curr_m_resnr = genstat.resnr
        tot_y_anztage = tot_y_anztage + 1
        tot_y_logis =  to_decimal(tot_y_logis) + to_decimal(genstat.logis)
        tot_y_erwachs = tot_y_erwachs + to_int(genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2)
        tot_y_kind = tot_y_kind + to_int(genstat.kind1 + genstat.kind2)

        if curr_y_resnr != genstat.resnr or curr_m_reslinnr != genstat.res_int[0]:
            tot_y_room_resv = tot_y_room_resv + 1
            curr_y_reslinnr = res_line.reslinnr
            curr_y_resnr = genstat.resnr

    output_list = query(output_list_list, last=True)

    if output_list:
        output_list.m_anztage = tot_m_anztage
        output_list.y_anztage = tot_y_anztage
        output_list.m_logis =  to_decimal(tot_m_logis)
        output_list.y_logis =  to_decimal(tot_y_logis)
        output_list.m_los =  to_decimal(tot_m_anztage) / to_decimal(tot_m_room_resv)
        output_list.y_los =  to_decimal(tot_y_anztage) / to_decimal(tot_y_room_resv)
        output_list.m_erwachs = tot_m_erwachs
        output_list.y_erwachs = tot_y_erwachs
        output_list.m_kind = tot_m_kind
        output_list.y_kind = tot_y_kind
        output_list.m_resv = tot_m_room_resv
        output_list.y_resv = tot_y_room_resv


        t_m_anztage = t_m_anztage + tot_m_anztage
        t_y_anztage = t_y_anztage + tot_y_anztage
        t_m_logis =  to_decimal(t_m_logis) + to_decimal(tot_m_logis)
        t_y_logis =  to_decimal(t_y_logis) + to_decimal(tot_y_logis)
        t_m_erwachs = t_m_erwachs + tot_m_erwachs
        t_y_erwachs = t_y_erwachs + tot_y_erwachs
        t_m_kind = t_m_kind + tot_m_kind
        t_y_kind = t_y_kind + tot_y_kind
        t_m_room_resv = t_m_room_resv + tot_m_room_resv
        t_y_room_resv = t_y_room_resv + tot_y_room_resv
        t_m_los =  to_decimal(t_m_los) + to_decimal((tot_m_anztage) / to_decimal(tot_m_room_resv))
        t_y_los =  to_decimal(t_y_los) + to_decimal((tot_y_anztage) / to_decimal(tot_y_room_resv))

        if tot_m_logis == 0.0:
            output_list.m_avrg_logis =  to_decimal(0.0)
            t_m_avrg_logis =  to_decimal(t_m_avrg_logis) + to_decimal(0.0)


        else:
            output_list.m_avrg_logis =  to_decimal(tot_m_logis) / to_decimal(tot_m_anztage)
            t_m_avrg_logis =  to_decimal(t_m_avrg_logis) + to_decimal((tot_m_logis) / to_decimal(tot_m_anztage) )

        if tot_y_logis == 0.0:
            output_list.y_avrg_logis =  to_decimal(0.0)
            t_y_avrg_logis =  to_decimal(t_y_avrg_logis) + to_decimal(0.0)


        else:
            output_list.y_avrg_logis =  to_decimal(tot_y_logis) / to_decimal(tot_y_anztage)
            t_y_avrg_logis =  to_decimal(t_y_avrg_logis) + to_decimal((tot_y_logis) / to_decimal(tot_y_anztage) )


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.zikatnr = 0
        output_list.kurzbez = ""
        output_list.bezeichnung = "T O T A L"
        output_list.m_anztage = t_m_anztage
        output_list.y_anztage = t_y_anztage
        output_list.m_logis =  to_decimal(t_m_logis)
        output_list.y_logis =  to_decimal(t_y_logis)
        output_list.m_los =  to_decimal(t_m_anztage) / to_decimal(t_m_room_resv)
        output_list.y_los =  to_decimal(t_y_anztage) / to_decimal(t_y_room_resv)
        output_list.m_erwachs = t_m_erwachs
        output_list.y_erwachs = t_y_erwachs
        output_list.m_kind = t_m_kind
        output_list.y_kind = t_y_kind
        output_list.m_avrg_logis =  to_decimal(t_m_avrg_logis)
        output_list.y_avrg_logis =  to_decimal(t_y_avrg_logis)
        output_list.m_resv = t_m_room_resv
        output_list.y_resv = t_y_room_resv

    return generate_output()