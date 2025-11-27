#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.pj_inhouse4_btn_go_4_cldbl import pj_inhouse4_btn_go_4_cldbl
from models import Queasy, Zimkateg, Paramtext

def pj_inhouse4_webbl(sorttype:int, from_date:date, to_date:date, froom:string, troom:string, exc_depart:bool, incl_gcomment:bool, incl_rsvcomment:bool, disp_accompany:bool, idflag:string):

    prepare_cache ([Queasy, Zimkateg, Paramtext])

    curr_date:date = None
    curr_gastnr:int = 0
    str:string = ""
    htl_no:string = ""
    tdate:string = ""
    crdate:string = ""
    cgdate:string = ""
    counter:int = 0
    company:string = ""
    tot_payrm:int = 0
    tot_rm:int = 0
    tot_a:int = 0
    tot_c:int = 0
    tot_co:int = 0
    tot_avail:int = 0
    inactive:int = 0
    tot_keycard:int = 0
    bemerk:string = ""
    bemerk1:string = ""
    bezeich:string = ""
    curr_time:int = 0
    queasy = zimkateg = paramtext = None

    inhouse_guest_list = output_list = s_list = zikat_list = t_buff_queasy = bqueasy = tqueasy = bufflist = None

    inhouse_guest_list_data, Inhouse_guest_list = create_model("Inhouse_guest_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})
    output_list_data, Output_list = create_model("Output_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})
    s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})
    t_buff_queasy_data, T_buff_queasy = create_model_like(Queasy)

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)
    Bufflist = Output_list
    bufflist_data = output_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, curr_gastnr, str, htl_no, tdate, crdate, cgdate, counter, company, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, bemerk, bemerk1, bezeich, curr_time, queasy, zimkateg, paramtext
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany, idflag
        nonlocal bqueasy, tqueasy, bufflist


        nonlocal inhouse_guest_list, output_list, s_list, zikat_list, t_buff_queasy, bqueasy, tqueasy, bufflist
        nonlocal inhouse_guest_list_data, output_list_data, s_list_data, zikat_list_data, t_buff_queasy_data

        return {}

    def decode_string(in_str:string):

        nonlocal curr_date, curr_gastnr, str, htl_no, tdate, crdate, cgdate, counter, company, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, bemerk, bemerk1, bezeich, curr_time, queasy, zimkateg, paramtext
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany, idflag
        nonlocal bqueasy, tqueasy, bufflist


        nonlocal inhouse_guest_list, output_list, s_list, zikat_list, t_buff_queasy, bqueasy, tqueasy, bufflist
        nonlocal inhouse_guest_list_data, output_list_data, s_list_data, zikat_list_data, t_buff_queasy_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def add_html(pcstring:string):

        nonlocal curr_date, curr_gastnr, str, htl_no, tdate, crdate, cgdate, counter, company, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, bemerk, bemerk1, bezeich, curr_time, queasy, zimkateg, paramtext
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany, idflag
        nonlocal bqueasy, tqueasy, bufflist


        nonlocal inhouse_guest_list, output_list, s_list, zikat_list, t_buff_queasy, bqueasy, tqueasy, bufflist
        nonlocal inhouse_guest_list_data, output_list_data, s_list_data, zikat_list_data, t_buff_queasy_data

        pccleaned = ""
        ihtmltagbegins:int = 0
        ihtmltagends:int = 0
        lhtmltagactive:bool = False
        i:int = 0

        def generate_inner_output():
            return (pccleaned)

        for i in range(1,length(pcstring)  + 1) :

            if lhtmltagactive == False and substring(pcstring, i - 1, 1) == ">":
                ihtmltagbegins = i
                lhtmltagactive = True

            if lhtmltagactive and substring(pcstring, i - 1, 1) == "<":
                ihtmltagends = i
                lhtmltagactive = True
                pcstring = replace_substring(pcstring, i - 1, 1, " " + replace_substring(pcstring, i - 1, 1))
        pccleaned = pcstring

        return generate_inner_output()


    def clean_html(pcstring:string):

        nonlocal curr_date, curr_gastnr, str, htl_no, tdate, crdate, cgdate, counter, company, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, bemerk, bemerk1, bezeich, curr_time, queasy, zimkateg, paramtext
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany, idflag
        nonlocal bqueasy, tqueasy, bufflist


        nonlocal inhouse_guest_list, output_list, s_list, zikat_list, t_buff_queasy, bqueasy, tqueasy, bufflist
        nonlocal inhouse_guest_list_data, output_list_data, s_list_data, zikat_list_data, t_buff_queasy_data

        pccleaned = ""
        ihtmltagbegins:int = 0
        ihtmltagends:int = 0
        lhtmltagactive:bool = False
        i:int = 0

        def generate_inner_output():
            return (pccleaned)

        for i in range(1,length(pcstring)  + 1) :

            if lhtmltagactive == False and substring(pcstring, i - 1, 1) == "<":
                ihtmltagbegins = i
                lhtmltagactive = True

            if lhtmltagactive and substring(pcstring, i - 1, 1) == ">":
                ihtmltagends = i
                lhtmltagactive = True
                pcstring = replace_substring(pcstring, ihtmltagbegins - 1, ihtmltagends - ihtmltagbegins + 1, fill("|", ihtmltagends - ihtmltagbegins))
        pccleaned = replace_str(pcstring, "|", "")

        return generate_inner_output()

    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "Inhouse List"
    queasy.number1 = 1
    queasy.number2 = to_int(idflag)


    pass
    curr_time = get_current_time_in_seconds()


    curr_date = get_output(htpdate(87))

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.kurzbez).all():
        zikat_list = Zikat_list()
        zikat_list_data.append(zikat_list)

        zikat_list.zikatnr = zimkateg.zikatnr
        zikat_list.kurzbez = zimkateg.kurzbez
        zikat_list.bezeich = zimkateg.bezeichnung

    for zikat_list in query(zikat_list_data):
        zikat_list.selected = True

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)
    tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, output_list_data, s_list_data, t_buff_queasy_data = get_output(pj_inhouse4_btn_go_4_cldbl(1, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, "PJ-inhouse2", disp_accompany, zikat_list_data))

    if sorttype == 1 or sorttype == 3:

        if sorttype == 1:

            for output_list in query(output_list_data, sort_by=[("nr",False)]):
                counter = counter + 1
                output_list.nr = counter


                inhouse_guest_list = Inhouse_guest_list()
                inhouse_guest_list_data.append(inhouse_guest_list)

                buffer_copy(output_list, inhouse_guest_list)
        else:

            for output_list in query(output_list_data, sort_by=[("etage",False),("rmno",False)]):
                counter = counter + 1
                output_list.nr = counter


                inhouse_guest_list = Inhouse_guest_list()
                inhouse_guest_list_data.append(inhouse_guest_list)

                buffer_copy(output_list, inhouse_guest_list)
    else:

        for output_list in query(output_list_data, sort_by=[("company",False)]):

            if company != output_list.company:
                company = output_list.company
                inhouse_guest_list = Inhouse_guest_list()
                inhouse_guest_list_data.append(inhouse_guest_list)

                inhouse_guest_list.rmcat = output_list.company

                for bufflist in query(bufflist_data, filters=(lambda bufflist: bufflist.company.lower()  == (company).lower())):
                    counter = counter + 1
                    inhouse_guest_list = Inhouse_guest_list()
                    inhouse_guest_list_data.append(inhouse_guest_list)

                    buffer_copy(bufflist, inhouse_guest_list)
                    inhouse_guest_list.nr = counter
                inhouse_guest_list = Inhouse_guest_list()
                inhouse_guest_list_data.append(inhouse_guest_list)


    inhouse_guest_list = query(inhouse_guest_list_data, first=True)
    while None != inhouse_guest_list:

        if inhouse_guest_list.bezeich == None:
            bezeich = ""
        else:
            bezeich = inhouse_guest_list.bezeich

        if inhouse_guest_list.bemerk == None:
            bemerk = ""
        else:
            bemerk = inhouse_guest_list.bemerk

        if inhouse_guest_list.bemerk1 == None:
            bemerk1 = ""
        else:
            bemerk1 = inhouse_guest_list.bemerk1
        bezeich = replace_str(bezeich, chr_unicode(10) , "")
        bezeich = replace_str(bezeich, chr_unicode(13) , "")
        bemerk = replace_str(bemerk, chr_unicode(10) , "")
        bemerk = replace_str(bemerk, chr_unicode(13) , "")
        bemerk = replace_str(bemerk, "|", "")
        counter = counter + 1


        bezeich = add_html(bezeich)
        bezeich = clean_html(bezeich)
        bemerk = add_html(bemerk)
        bemerk = clean_html(bemerk)
        bemerk1 = add_html(bemerk1)
        bemerk1 = clean_html(bemerk1)
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 280
        queasy.char1 = "Inhouse List"
        queasy.number2 = to_int(idflag)
        queasy.char3 = to_string(bezeich) + "|" +\
                to_string(bemerk) + "|" +\
                to_string(bemerk1)
        queasy.char2 = to_string(inhouse_guest_list.flag) + "|" +\
                to_string(inhouse_guest_list.karteityp) + "|" +\
                to_string(inhouse_guest_list.nr) + "|" +\
                inhouse_guest_list.vip + "|" +\
                to_string(inhouse_guest_list.resnr) + "|" +\
                inhouse_guest_list.firstname + "|" +\
                inhouse_guest_list.lastname + "|" +\
                inhouse_guest_list.birthdate + "|" +\
                inhouse_guest_list.groupname + "|" +\
                inhouse_guest_list.rmno + "|" +\
                to_string(inhouse_guest_list.qty) + "|" +\
                to_string(inhouse_guest_list.arrive) + "|" +\
                to_string(inhouse_guest_list.depart) + "|" +\
                inhouse_guest_list.rmcat + "|" +\
                inhouse_guest_list.ratecode + "|" +\
                to_string(inhouse_guest_list.zipreis) + "|" +\
                inhouse_guest_list.kurzbez + "|" +\
                to_string(inhouse_guest_list.a) + "|" +\
                to_string(inhouse_guest_list.c) + "|" +\
                to_string(inhouse_guest_list.co) + "|" +\
                inhouse_guest_list.pax + "|" +\
                inhouse_guest_list.nat + "|" +\
                inhouse_guest_list.nation + "|" +\
                inhouse_guest_list.argt + "|" +\
                inhouse_guest_list.company + "|" +\
                inhouse_guest_list.flight + "|" +\
                inhouse_guest_list.etd + "|" +\
                to_string(inhouse_guest_list.paym) + "|" +\
                inhouse_guest_list.segm + "|" +\
                inhouse_guest_list.telefon + "|" +\
                inhouse_guest_list.mobil_tel + "|" +\
                to_string(inhouse_guest_list.created) + "|" +\
                inhouse_guest_list.createID + "|" +\
                inhouse_guest_list.ci_time + "|" +\
                inhouse_guest_list.curr + "|" +\
                to_string(inhouse_guest_list.inhousedate) + "|" +\
                inhouse_guest_list.sob + "|" +\
                to_string(inhouse_guest_list.gastnr) + "|" +\
                to_string(inhouse_guest_list.lodging) + "|" +\
                to_string(inhouse_guest_list.breakfast) + "|" +\
                to_string(inhouse_guest_list.lunch) + "|" +\
                to_string(inhouse_guest_list.dinner) + "|" +\
                to_string(inhouse_guest_list.otherev) + "|" +\
                to_string(inhouse_guest_list.rechnr) + "|" +\
                inhouse_guest_list.memberno + "|" +\
                inhouse_guest_list.membertype + "|" +\
                inhouse_guest_list.email + "|" +\
                inhouse_guest_list.localreg + "|" +\
                inhouse_guest_list.c_zipreis + "|" +\
                inhouse_guest_list.c_lodging + "|" +\
                inhouse_guest_list.c_breakfast + "|" +\
                inhouse_guest_list.c_lunch + "|" +\
                inhouse_guest_list.c_dinner + "|" +\
                inhouse_guest_list.c_otherev + "|" +\
                inhouse_guest_list.c_a + "|" +\
                inhouse_guest_list.c_c + "|" +\
                inhouse_guest_list.c_co + "|" +\
                inhouse_guest_list.c_rechnr + "|" +\
                inhouse_guest_list.c_resnr + "|" +\
                inhouse_guest_list.night + "|" +\
                inhouse_guest_list.city + "|" +\
                inhouse_guest_list.keycard + "|" +\
                inhouse_guest_list.co_time + "|" +\
                inhouse_guest_list.pay_art + "|" +\
                to_string(inhouse_guest_list.etage) + "|" +\
                inhouse_guest_list.zinr_bez + "|" +\
                to_string(inhouse_guest_list.flag_guest)
        queasy.number1 = counter

        inhouse_guest_list = query(inhouse_guest_list_data, next=True)

    # bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "inhouse list")],"number2": [(eq, to_int(idflag))]})
    bqueasy = db_session.query(Bqueasy).filter(
        (Bqueasy.key == 285) & 
        (Bqueasy.char1 == "Inhouse List") & 
        (Bqueasy.number2 == to_int(idflag))).with_for_update().first()

    if bqueasy:
        pass
        bqueasy.number1 = 0
        db_session.refresh(bqueasy,with_for_update=True)

        pass
        pass

    return generate_output()
