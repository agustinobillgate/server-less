# using conversion tools version: 1.0.0.117

"""_yusufwijasena_ 10/10/2025

    TICKET ID: 79EBDE
    ISSUE:  - resnr & reslinnr is not known attribute
            - add type:ignore to model Datalist, avoid warning cannot assign attribute
            - fix  python indentation
            - operator not supported for types
            - matches, argument missing for parameter "pattern"
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Interface, Res_line, Reservation, Guest, Guestseg, Segment, History


def if_lgtv_v2bl():

    prepare_cache([Res_line, Guest, Guestseg, Segment, History])

    t_list_data = []
    gastnr_ind: int = 0
    gastnr_wi: int = 0
    # issue : 
    #     resnr & reslinnr is not known attribute
    # before :
    #     interface = res_line = reservation = guest = guestseg = segment = history = None
    
    interface = Interface()
    res_line = reservation = guest = guestseg = segment = history = None

    t_list = t_interface = bufflist = None

    t_list_data, T_list = create_model("T_list", {"resid": string, "irecid": int, "parameters": string, "firstname": string, "lastname": string, "salutation": string, "ci_date": date, "ci_time": int,
                                       "co_date": date, "co_time": int, "ci_status": string, "roomnr": string, "oldroomnr": string, "email_adr": string, "gastlang": string, "grpnr": int, "grpcode": string, "grpdesc": string, "vip": string})

    T_interface = create_buffer("T_interface", Interface)
    Bufflist = T_list
    bufflist_data = t_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, gastnr_ind, gastnr_wi, interface, res_line, reservation, guest, guestseg, segment, history
        nonlocal t_interface, bufflist

        nonlocal t_list, t_interface, bufflist
        nonlocal t_list_data

        return {"t-list": t_list_data}

    def update_tlist(create_flag: bool):

        nonlocal t_list_data, gastnr_ind, gastnr_wi, interface, res_line, reservation, guest, guestseg, segment, history
        nonlocal t_interface, bufflist

        nonlocal t_list, t_interface, bufflist
        nonlocal t_list_data

        res_line = get_cache(Res_line, {"resnr": [(eq, interface.resnr)], "reslinnr": [
                             (eq, interface.reslinnr)]})

        if res_line:

            reservation = get_cache(
                Reservation, {"resnr": [(eq, res_line.resnr)]})

            guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:

                if create_flag:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.firstname = guest.vorname1  # type: ignore
                    t_list.lastname = guest.name  # type: ignore
                    t_list.salutation = guest.anrede1  # type: ignore
                    t_list.ci_status = "true"  # type: ignore

                    t_list.parameters = interface.parameters  # type: ignore

                    if guest.nation1.lower() == ("USA").lower():
                        t_list.gastlang = "en_US"  # type: ignore

                    elif guest.nation1.lower() == ("NLD").lower():
                        t_list.gastlang = "nl_NL"  # type: ignore

                    elif guest.nation1.lower() == ("GBR").lower():
                        t_list.gastlang = "en_GB"  # type: ignore

                    elif guest.nation1.lower() == ("CAN").lower():
                        t_list.gastlang = "en_CA"  # type: ignore

                    elif guest.nation1.lower() == ("BGR").lower():
                        t_list.gastlang = "bg_BG"  # type: ignore

                    elif guest.nation1.lower() == ("DEU").lower():
                        t_list.gastlang = "de_DE"  # type: ignore

                    elif guest.nation1.lower() == ("ESP").lower():
                        t_list.gastlang = "es_ES"  # type: ignore

                    elif guest.nation1.lower() == ("FRA").lower():
                        t_list.gastlang = "fr_FR"  # type: ignore

                    elif guest.nation1.lower() == ("HRV").lower():
                        t_list.gastlang = "hr_HR"  # type: ignore

                    elif guest.nation1.lower() == ("HUN").lower():
                        t_list.gastlang = "hu_HU"  # type: ignore

                    elif guest.nation1.lower() == ("ITA").lower():
                        t_list.gastlang = "it_IT"  # type: ignore

                    elif guest.nation1.lower() == ("CHN").lower():
                        t_list.gastlang = "zh_CN"  # type: ignore

                    elif guest.nation1.lower() == ("PRT").lower():
                        t_list.gastlang = "pt_PT"  # type: ignore

                    elif guest.nation1.lower() == ("BRA").lower():
                        t_list.gastlang = "pt_BR"  # type: ignore

                    elif guest.nation1.lower() == ("GRC").lower():
                        t_list.gastlang = "el_GR"  # type: ignore

                    elif guest.nation1.lower() == ("RUS").lower():
                        t_list.gastlang = "ru_RU"  # type: ignore

                    elif guest.nation1.lower() == ("SWE").lower():
                        t_list.gastlang = "sv_SE"  # type: ignore

                    elif guest.nation1.lower() == ("ROM").lower():
                        t_list.gastlang = "ro_RO"  # type: ignore

                    elif guest.nation1.lower() == ("POL").lower():
                        t_list.gastlang = "pl_PL"  # type: ignore

                    elif guest.nation1.lower() == ("CZE").lower():
                        t_list.gastlang = "cs_CZ"  # type: ignore

                    elif guest.nation1.lower() == ("FIN").lower():
                        t_list.gastlang = "fi_FI"  # type: ignore

                    elif guest.nation1.lower() == ("NOR").lower():
                        t_list.gastlang = "no_NO"  # type: ignore

                    elif guest.nation1.lower() == ("DNK").lower():
                        t_list.gastlang = "da_DK"  # type: ignore

                    elif guest.nation1.lower() == ("HKG").lower():
                        t_list.gastlang = "zh_HK"  # type: ignore

                    elif guest.nation1.lower() == ("TWN").lower():
                        t_list.gastlang = "zh_TW"  # type: ignore

                    elif guest.nation1.lower() == ("SGP").lower():
                        t_list.gastlang = "zh_SG"  # type: ignore

                    elif guest.nation1.lower() == ("SVN").lower():
                        t_list.gastlang = "sl_SI"  # type: ignore

                    elif guest.nation1.lower() == ("CS").lower():
                        t_list.gastlang = "sr_RS"  # type: ignore

                    elif guest.nation1.lower() == ("TUR").lower():
                        t_list.gastlang = "tr_TR"  # type: ignore

                    elif guest.nation1.lower() == ("SVK").lower():
                        t_list.gastlang = "sk_SK"  # type: ignore

                    elif guest.nation1.lower() == ("ALB").lower():
                        t_list.gastlang = "al_AL"  # type: ignore

                    elif guest.nation1.lower() == ("BIH").lower():
                        t_list.gastlang = "bs_BA"  # type: ignore

                    elif guest.nation1.lower() == ("MKD").lower():
                        t_list.gastlang = "mk_MK"  # type: ignore

                    elif guest.nation1.lower() == ("UKR").lower():
                        t_list.gastlang = "uk_UA"  # type: ignore

                    elif guest.nation1.lower() == ("KAZ").lower():
                        t_list.gastlang = "kk_KZ"  # type: ignore

                    elif guest.nation1.lower() == ("EST").lower():
                        t_list.gastlang = "et_EE"  # type: ignore

                    elif guest.nation1.lower() == ("LVA").lower():
                        t_list.gastlang = "lv_LV"  # type: ignore

                    elif guest.nation1.lower() == ("LTU").lower():
                        t_list.gastlang = "lt_LT"  # type: ignore

                    elif guest.nation1.lower() == ("KOR").lower():
                        t_list.gastlang = "ko_KR"  # type: ignore

                    elif guest.nation1.lower() == ("JPN").lower():
                        t_list.gastlang = "ja_JP"  # type: ignore
                    else:
                        t_list.gastlang = ""  # type: ignore
                        t_list.ci_date = interface.intdate  # type: ignore
                        t_list.ci_time = interface.int_time  # type: ignore
                        t_list.co_date = res_line.abreise  # type: ignore
                        t_list.co_time = res_line.abreisezeit  # type: ignore
                        t_list.resid = to_string( interface.resnr) + to_string(interface.reslinnr) # type: ignore
                        t_list.irecid = interface._recid  # type: ignore
                        t_list.roomnr = interface.zinr  # type: ignore

                guestseg = get_cache(
                    Guestseg, {"gastnr": [(eq, guest.gastnr)]})

                if guestseg:

                    segment = get_cache(
                        Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

                    if segment:
                        t_list.grpnr = segment.segmentcode  # type: ignore
                        t_list.grpcode = segment.bezeich  # type: ignore
                        t_list.grpdesc = segment.bemerkung  # type: ignore

                        if segment.betriebsnr == 3:
                            t_list.vip = "vip"  # type: ignore

                        else:
                            t_list.vip = ""  # type: ignore

                    else:
                        t_list.grpnr = 1  # type: ignore
                        t_list.grpcode = ""  # type: ignore
                        t_list.grpdesc = ""  # type: ignore

                if matches(t_list.parameters, r"*Move in*"):  # type: ignore

                    # issue:
                    #     Operator ">=" not supported for types "str" and "int"
                    #     Operator ">=" not supported for types "None" and "str"
                    #     Operator ">=" not supported for types "None" and "int"
                    # before:
                    #     (substring(History.bemerk, 0, 8) >= to_string(res_line.   Eankunft)) & (substring(History.bemerk, 0, 8) <= to_string(res_line.abreise))

                    for history in db_session.query(History).filter(
                            (History.resnr == res_line.resnr) & (History.ankunft <= date_mdy(res_line.abreise)) & (History.abreise >= date_mdy(res_line.ankunft)) & (History.zi_wechsel) & (substring(History.bemerk, 0, 8) >= res_line.ankunft) & (substring(History.bemerk, 0, 8) <= res_line.abreise) & (matches(History.bemerk, "*: Moved To*"))).order_by(History.abreisezeit.desc()).all():
                        t_list.oldroomnr = history.zinr  # type: ignore
                        break

                    bufflist = query(bufflist_data, filters=(lambda bufflist: matches(
                        bufflist.parameters, r"*DataExchange*") and bufflist.roomnr == t_list.oldroomnr), first=True)  # type: ignore

                    if bufflist:
                        t_list_data.remove(t_list)

    # issue:
    #     Argument missing for parameter "pattern"
    # before:
    #     matches((Interface.parameters,"*Checkin*"))

    interface = db_session.query(Interface).filter(
        (Interface.key == 3) & (matches(Interface.parameters, "*Checkin*") | (matches(Interface.parameters, "*Checkout*")) | (matches(Interface.parameters, "*Move in*")) | (matches(Interface.parameters, "*Move out*")) | (matches(Interface.parameters, "*Change Guestname*")))).first()
    while None != interface:

        t_list = query(t_list_data, filters=(
            lambda t_list: t_list.roomnr == interface.zinr), first=True)

        if not t_list:
            update_tlist(True)

        elif t_list:

            if (interface.intdate == t_list.ci_date and interface.int_time > t_list.ci_time) or interface.intdate > t_list.ci_date:  # type: ignore

                t_interface = db_session.query(T_interface).filter(
                    (T_interface._recid == t_list.irecid)).first()  # type: ignore

                if t_interface:
                    db_session.delete(t_interface)
                    pass
                update_tlist(False)
            else:
                pass
                db_session.delete(interface)
                pass

        curr_recid = interface._recid

        # issue:
        #     Argument missing for parameter "pattern"
        # before:
        #     matches((Interface.parameters,"*Checkin*"))

        interface = db_session.query(Interface).filter(
            (Interface.key == 3) & (matches(Interface.parameters, "*Checkin*") | (matches(Interface.parameters, "*Checkout*")) | (matches(Interface.parameters, "*Move in*")) | (matches(Interface.parameters, "*Move out*")) | (matches(Interface.parameters, "*Change Guestname*"))) & (Interface._recid > curr_recid)).first()

    return generate_output()
