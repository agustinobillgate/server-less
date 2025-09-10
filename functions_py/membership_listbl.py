#using conversion tools version: 1.0.0.117

# -------------------------------------------
# Rulita, 09-09-2025 Scenario 144, 145, 149 
# issue, added stip variable member_number
# -------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mc_guest, Guest, Mc_types, Bediener

def membership_listbl(member_number:string, member_type:int):

    prepare_cache ([Mc_guest, Guest, Mc_types, Bediener])

    # Rulita
    member_number = member_number.strip()
    result_str = ""
    member_list_data = []
    salesname:string = ""
    mc_guest = guest = mc_types = bediener = None

    member_list = non_member = None

    member_list_data, Member_list = create_model("Member_list", {"guest_number":int, "member_number":string, "member_type":string, "member_from_date":date, "member_to_date":date, "member_sales_id":string, "member_sales_name":string, "member_actiflag":bool, "guest_title":string, "first_name":string, "last_name":string, "country":string, "address":string, "city":string, "phone":string, "mobile_phone":string, "email":string, "sex":string, "idcard_number":string, "birthday":date, "bemerk":string, "member_name":string})
    non_member_data, Non_member = create_model("Non_member", {"activeflag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_str, member_list_data, salesname, mc_guest, guest, mc_types, bediener
        nonlocal member_number, member_type


        nonlocal member_list, non_member
        nonlocal member_list_data, non_member_data

        return {"result_str": result_str, "member-list": member_list_data}

    def create_list():

        nonlocal result_str, member_list_data, salesname, mc_guest, guest, mc_types, bediener
        nonlocal member_number, member_type


        nonlocal member_list, non_member
        nonlocal member_list_data, non_member_data


        member_list = Member_list()
        member_list_data.append(member_list)

        member_list.guest_number = guest.gastnr
        member_list.member_number = mc_guest.cardnum
        member_list.member_type = mc_types.bezeich
        member_list.member_from_date = mc_guest.fdate
        member_list.member_to_date = mc_guest.tdate
        member_list.member_sales_id = mc_guest.sales_id
        member_list.member_sales_name = salesname
        member_list.member_actiflag = mc_guest.activeflag
        member_list.first_name = guest.vorname1
        member_list.last_name = guest.name
        member_list.guest_title = guest.anrede1
        member_list.country = guest.land
        member_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
        member_list.city = guest.wohnort
        member_list.phone = guest.telefon
        member_list.mobile_phone = guest.mobil_telefon
        member_list.email = guest.email_adr
        member_list.sex = guest.geschlecht
        member_list.idcard_number = guest.ausweis_nr1
        member_list.birthday = guest.geburtdatum1
        member_list.bemerk = replace_str(member_list.address, chr_unicode(10) , "")
        member_list.member_name = replace_str(guest.vorname1 + " " + guest.name, chr_unicode(10) , "")

        if mc_types:
            member_list.member_type = mc_types.bezeich

    if member_type == 0:

        if member_number == "":

            for mc_guest in db_session.query(Mc_guest).order_by(Mc_guest._recid).all():

                guest = get_cache (Guest, {"gastnr": [(eq, mc_guest.gastnr)]})

                mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})
                salesname = ""

                if mc_guest.sales_id != "":

                    bediener = get_cache (Bediener, {"flag": [(eq, 0)],"userinit": [(eq, mc_guest.sales_id)]})

                    if bediener:
                        salesname = bediener.username
                    else:
                        salesname = ""

                if guest:
                    create_list()
        else:

            mc_guest = get_cache (Mc_guest, {"cardnum": [(eq, member_number)]})

            if mc_guest:

                guest = get_cache (Guest, {"gastnr": [(eq, mc_guest.gastnr)]})

                mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})
                salesname = ""

                if mc_guest.sales_id != "":

                    bediener = get_cache (Bediener, {"flag": [(eq, 0)],"userinit": [(eq, mc_guest.sales_id)]})

                    if bediener:
                        salesname = bediener.username
                    else:
                        salesname = ""
                create_list()
    else:

        if member_number == "":

            for mc_guest in db_session.query(Mc_guest).filter(
                     (Mc_guest.nr == member_type)).order_by(Mc_guest._recid).all():

                guest = get_cache (Guest, {"gastnr": [(eq, mc_guest.gastnr)]})

                mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})
                salesname = ""

                if mc_guest.sales_id != "":

                    bediener = get_cache (Bediener, {"flag": [(eq, 0)],"userinit": [(eq, mc_guest.sales_id)]})

                    if bediener:
                        salesname = bediener.username
                    else:
                        salesname = ""
                create_list()
        else:

            mc_guest = get_cache (Mc_guest, {"nr": [(eq, member_type)],"cardnum": [(eq, member_number)]})

            if mc_guest:

                guest = get_cache (Guest, {"gastnr": [(eq, mc_guest.gastnr)]})

                mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})
                salesname = ""

                if mc_guest.sales_id != "":

                    bediener = get_cache (Bediener, {"flag": [(eq, 0)],"userinit": [(eq, mc_guest.sales_id)]})

                    if bediener:
                        salesname = bediener.username
                    else:
                        salesname = ""
                create_list()

    return generate_output()