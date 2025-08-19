#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.repeat_glist_1blho import repeat_glist_1blho  # Oscar - skip because using HServer on Progress
from models import Htparam

input_list_data, Input_list = create_model("Input_list", {"pvilanguage":int, "from_date":date, "to_date":date, "ci_date":date, "create_inhouse":bool, "sorttype":int, "modetype":int, "min_stay":int})

def repeat_glist_centralized_webbl(input_list_data:[Input_list]):

    prepare_cache ([Htparam])

    g_list_data = []
    repeat_list_data = []
    cur_date_data = []
    pvilanguage:int = 0
    from_date:date = None
    to_date:date = None
    ci_date:date = None
    create_inhouse:bool = False
    sorttype:int = 0
    modetype:int = 0
    min_stay:int = 0
    vhost:string = ""
    vservice:string = ""
    hoappparam:string = ""
    lreturn:bool = False
    htparam = None

    input_list = g_list = repeat_list = cur_date = output_rlist2 = output_glist2 = None

    g_list_data, G_list = create_model("G_list", {"resnr":int, "gastnr":int, "name":string, "ankunft":date, "abreise":date, "zinr":string, "reslinnr":int, "zipreis":Decimal, "currency":string, "argt":string, "erwachs":int, "kind1":int, "gratis":int, "arrflag":bool, "resname":string, "lodging":Decimal})
    repeat_list_data, Repeat_list = create_model("Repeat_list", {"flag":int, "gastnr":int, "name":string, "nation":string, "birthdate":date, "email":string, "telefon":string, "vip":string, "city":string, "stay":int, "rmnite":int, "ankunft":date, "arrflag":bool, "zinr":string, "remark":string, "resname":string, "lodging":Decimal, "pax":int, "mobil_telefon":string})
    cur_date_data, Cur_date = create_model("Cur_date", {"curr_date":date})
    output_rlist2_data, Output_rlist2 = create_model_like(Repeat_list)
    output_glist2_data, Output_glist2 = create_model_like(G_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_list_data, repeat_list_data, cur_date_data, pvilanguage, from_date, to_date, ci_date, create_inhouse, sorttype, modetype, min_stay, vhost, vservice, hoappparam, lreturn, htparam


        nonlocal input_list, g_list, repeat_list, cur_date, output_rlist2, output_glist2
        nonlocal g_list_data, repeat_list_data, cur_date_data, output_rlist2_data, output_glist2_data

        return {"g-list": g_list_data, "repeat-list": repeat_list_data, "cur-date": cur_date_data}

    def disp_repeatlist():

        nonlocal g_list_data, repeat_list_data, cur_date_data, pvilanguage, from_date, to_date, ci_date, create_inhouse, sorttype, modetype, min_stay, vhost, vservice, hoappparam, lreturn, htparam


        nonlocal input_list, g_list, repeat_list, cur_date, output_rlist2, output_glist2
        nonlocal g_list_data, repeat_list_data, cur_date_data, output_rlist2_data, output_glist2_data

        tot_lodging:Decimal = to_decimal("0.0")
        tot_stay:int = 0
        tot_rmnight:int = 0
        tot_pax:int = 0

        if sorttype == 0:

            for output_rlist2 in query(output_rlist2_data, sort_by=[("stay",True),("name",False)]):

                if (output_rlist2.stay >= min_stay) or (output_rlist2.stay >= (min_stay - 1) and output_rlist2.arrFLag):
                    repeat_list = Repeat_list()
                    repeat_list_data.append(repeat_list)

                    repeat_list.flag = output_rlist2.flag
                    repeat_list.gastnr = output_rlist2.gastnr
                    repeat_list.name = output_rlist2.name
                    repeat_list.nation = output_rlist2.nation
                    repeat_list.birthdate = output_rlist2.birthdate
                    repeat_list.email = output_rlist2.email
                    repeat_list.telefon = output_rlist2.telefon
                    repeat_list.vip = output_rlist2.vip
                    repeat_list.city = output_rlist2.city
                    repeat_list.stay = output_rlist2.stay
                    repeat_list.rmnite = output_rlist2.rmnite
                    repeat_list.ankunft = output_rlist2.ankunft
                    repeat_list.arrflag = output_rlist2.arrFlag
                    repeat_list.zinr = output_rlist2.zinr
                    repeat_list.remark = output_rlist2.remark
                    repeat_list.resname = output_rlist2.resname
                    repeat_list.lodging =  to_decimal(output_rlist2.lodging)
                    repeat_list.pax = output_rlist2.pax
                    repeat_list.mobil_telefon = output_rlist2.mobil_telefon
                    tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_rlist2.lodging)
                    tot_stay = tot_stay + output_rlist2.stay
                    tot_rmnight = tot_rmnight + output_rlist2.rmnite
                    tot_pax = tot_pax + output_rlist2.pax


            repeat_list = Repeat_list()
            repeat_list_data.append(repeat_list)

            repeat_list.city = "T O T A L"
            repeat_list.stay = tot_stay
            repeat_list.lodging =  to_decimal(tot_lodging)
            repeat_list.rmnite = tot_rmnight
            repeat_list.zinr = " "
            repeat_list.pax = tot_pax


        else:
            if sorttype == 1:
                for output_rlist2 in query(output_rlist2_data, sort_by=[("stay",True),("name",False)]):
                    if output_rlist2.flag == sorttype and ((output_rlist2.stay >= min_stay) or (output_rlist2.stay >= (min_stay - 1) and output_rlist2.arrFLag)) and output_rlist2.ankunft >= from_date and output_rlist2.ankunft <= to_date:
                        repeat_list = Repeat_list()
                        repeat_list_data.append(repeat_list)

                        repeat_list.flag = output_rlist2.flag
                        repeat_list.gastnr = output_rlist2.gastnr
                        repeat_list.name = output_rlist2.name
                        repeat_list.nation = output_rlist2.nation
                        repeat_list.birthdate = output_rlist2.birthdate
                        repeat_list.email = output_rlist2.email
                        repeat_list.telefon = output_rlist2.telefon
                        repeat_list.vip = output_rlist2.vip
                        repeat_list.city = output_rlist2.city
                        repeat_list.stay = output_rlist2.stay
                        repeat_list.rmnite = output_rlist2.rmnite
                        repeat_list.ankunft = output_rlist2.ankunft
                        repeat_list.arrflag = output_rlist2.arrFlag
                        repeat_list.zinr = output_rlist2.zinr
                        repeat_list.remark = output_rlist2.remark
                        repeat_list.resname = output_rlist2.resname
                        repeat_list.lodging =  to_decimal(output_rlist2.lodging)
                        repeat_list.pax = output_rlist2.pax
                        repeat_list.mobil_telefon = output_rlist2.mobil_telefon
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_rlist2.lodging)
                        tot_pax = tot_pax + output_rlist2.pax


                repeat_list = Repeat_list()
                repeat_list_data.append(repeat_list)

                repeat_list.city = "T O T A L"
                repeat_list.stay = 999
                repeat_list.lodging =  to_decimal(tot_lodging)
                repeat_list.zinr = " "
                repeat_list.pax = tot_pax


            else:
                for output_rlist2 in query(output_rlist2_data, sort_by=[("stay",True),("name",False)]):
                    if output_rlist2.flag == sorttype and ((output_rlist2.stay >= min_stay) or (output_rlist2.stay >= (min_stay - 1) and output_rlist2.arrFLag)):
                        repeat_list = Repeat_list()
                        repeat_list_data.append(repeat_list)

                        repeat_list.flag = output_rlist2.flag
                        repeat_list.gastnr = output_rlist2.gastnr
                        repeat_list.name = output_rlist2.name
                        repeat_list.nation = output_rlist2.nation
                        repeat_list.birthdate = output_rlist2.birthdate
                        repeat_list.email = output_rlist2.email
                        repeat_list.telefon = output_rlist2.telefon
                        repeat_list.vip = output_rlist2.vip
                        repeat_list.city = output_rlist2.city
                        repeat_list.stay = output_rlist2.stay
                        repeat_list.rmnite = output_rlist2.rmnite
                        repeat_list.ankunft = output_rlist2.ankunft
                        repeat_list.arrflag = output_rlist2.arrFlag
                        repeat_list.zinr = output_rlist2.zinr
                        repeat_list.remark = output_rlist2.remark
                        repeat_list.resname = output_rlist2.resname
                        repeat_list.lodging =  to_decimal(output_rlist2.lodging)
                        repeat_list.pax = output_rlist2.pax
                        repeat_list.mobil_telefon = output_rlist2.mobil_telefon
                        tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_rlist2.lodging)
                        tot_pax = tot_pax + output_rlist2.pax


                repeat_list = Repeat_list()
                repeat_list_data.append(repeat_list)

                repeat_list.city = "T O T A L"
                repeat_list.stay = 999
                repeat_list.lodging =  to_decimal(tot_lodging)
                repeat_list.zinr = " "
                repeat_list.pax = tot_pax


    def disp_guesthistory():

        nonlocal g_list_data, repeat_list_data, cur_date_data, pvilanguage, from_date, to_date, ci_date, create_inhouse, sorttype, modetype, min_stay, vhost, vservice, hoappparam, lreturn, htparam


        nonlocal input_list, g_list, repeat_list, cur_date, output_rlist2, output_glist2
        nonlocal g_list_data, repeat_list_data, cur_date_data, output_rlist2_data, output_glist2_data

        for output_glist2 in query(output_glist2_data, filters=(lambda output_glist2: output_glist2.gastnr == sorttype), sort_by=[("ankunft",False)]):
            g_list = G_list()
            g_list_data.append(g_list)

            g_list.resnr = output_glist2.resnr
            g_list.gastnr = output_glist2.gastnr
            g_list.name = output_glist2.name
            g_list.ankunft = output_glist2.ankunft
            g_list.abreise = output_glist2.abreise
            g_list.zinr = output_glist2.zinr
            g_list.reslinnr = output_glist2.reslinnr
            g_list.zipreis =  to_decimal(output_glist2.zipreis)
            g_list.currency = output_glist2.currency
            g_list.argt = output_glist2.argt
            g_list.erwachs = output_glist2.erwachs
            g_list.kind1 = output_glist2.kind1
            g_list.gratis = output_glist2.gratis
            g_list.arrflag = output_glist2.arrFlag
            g_list.resname = output_glist2.resname
            g_list.lodging =  to_decimal(output_glist2.lodging)


    def repeat_glist_centralized(pvilanguage:string, from_date:date, to_date:date, ci_date:date, create_inhouse:bool):

        nonlocal g_list_data, repeat_list_data, cur_date_data, sorttype, modetype, min_stay, vhost, vservice, hoappparam, lreturn, htparam


        nonlocal input_list, g_list, repeat_list, cur_date, output_rlist2, output_glist2
        nonlocal g_list_data, repeat_list_data, cur_date_data, output_rlist2_data, output_glist2_data

        def generate_inner_output():
            return (output_glist2_data, output_rlist2_data, cur_date_data)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 1343)]})

        if htparam:

            if htparam.fchar != "" and htparam.fchar != None:

                if num_entries(htparam.fchar, ":") > 1:
                    vhost = entry(0, htparam.fchar, ":")
                    vservice = entry(1, htparam.fchar, ":")
                    hoappparam = " -H " + vhost + " -S " + vservice + " -DirectConnect -sessionModel Session-free"


        # lreturn = hServerHO:CONNECT (hoappparam, None, None, None) # Oscar - skip because using HServer on Progress
        lreturn = False

        if not lreturn:
            return generate_inner_output()
        
        local_storage.combo_flag = True
        # output_glist2_data, output_rlist2_data, cur_date_data = get_output(repeat_glist_1blho(pvilanguage, from_date, to_date, ci_date, create_inhouse)) # Oscar - skip because using HServer on Progress
        local_storage.combo_flag = False

        # lreturn = hServerHO:DISCONNECT() # Oscar - skip because using HServer on Progress

        return generate_inner_output()

    input_list = query(input_list_data, first=True)

    if not input_list:

        return generate_output()
    else:
        pvilanguage = input_list.pvilanguage
        from_date = input_list.from_date
        to_date = input_list.to_date
        ci_date = input_list.ci_date
        create_inhouse = input_list.create_inhouse
        sorttype = input_list.sorttype
        modetype = input_list.modetype
        min_stay = input_list.min_stay


    output_glist2_data, output_rlist2_data, cur_date_data = repeat_glist_centralized(pvilanguage, from_date, to_date, ci_date, create_inhouse)

    if modetype == 1:
        disp_repeatlist()

    elif modetype == 2:
        disp_guesthistory()

    return generate_output()