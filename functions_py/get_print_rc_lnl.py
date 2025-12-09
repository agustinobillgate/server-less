#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.get_print_rc_lnlbl import get_print_rc_lnlbl

def get_print_rc_lnl(resno:int, reslinno:int):
    variable_list_data = []

    print_rc_list = variable_list = None

    print_rc_list_data, Print_rc_list = create_model("Print_rc_list", {"gastno":string, "cr_usr":string, "last_name":string, "first_name":string, "guest_title":string, "room":string, "room_no":string, "room_price":string, "arrival":string, "departure":string, "eta_flight":string, "eta_time":string, "etd_flight":string, "etd_time":string, "no_guest":string, "purpose_stay":string, "guest_address1":string, "guest_address2":string, "guest_address3":string, "guest_country":string, "guest_zip":string, "guest_city":string, "guest_nation":string, "guest_id":string, "guest_email":string, "birth_date":string, "company_name":string, "rsv_addr1":string, "rsv_addr2":string, "rsv_addr3":string, "rsv_country":string, "rsv_city":string, "rsv_zip":string, "ccard":string, "mobile_no":string, "bill_instruct":string, "birth_place":string, "expired_id":string, "resnr":string, "province":string, "phone":string, "telefax":string, "occupation":string, "child1":string, "child2":string, "main_comment":string, "member_comment":string, "depositgef":string, "depositbez":string, "segment":string})
    variable_list_data, Variable_list = create_model("Variable_list", {"varkey":string, "varvalue":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal variable_list_data
        nonlocal resno, reslinno


        nonlocal print_rc_list, variable_list
        nonlocal print_rc_list_data, variable_list_data

        return {"variable-list": variable_list_data}

    print_rc_list_data = get_output(get_print_rc_lnlbl(resno, reslinno))

    print_rc_list = query(print_rc_list_data, first=True)

    if print_rc_list:
        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$GASTNO"
        variable_list.varvalue = print_rc_list.gastno


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$CR-USR"
        variable_list.varvalue = print_rc_list.cr_usr


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$FIRSTNAME"
        variable_list.varvalue = print_rc_list.first_name


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$TITLE1"
        variable_list.varvalue = print_rc_list.guest_title


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ROOM"
        variable_list.varvalue = print_rc_list.room


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ROOM-NO"
        variable_list.varvalue = print_rc_list.room_no


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ROOM-PRICE"
        variable_list.varvalue = print_rc_list.room_price


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ARRIVAL"
        variable_list.varvalue = print_rc_list.arrival


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ETAFL"
        variable_list.varvalue = print_rc_list.eta_flight


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ETATIME"
        variable_list.varvalue = print_rc_list.eta_time


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$DEPARTURE"
        variable_list.varvalue = print_rc_list.departure


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$DEPARTURE0"
        variable_list.varvalue = substring(print_rc_list.departure, 0, 10)


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ETDFL"
        variable_list.varvalue = print_rc_list.etd_flight


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ETDTIME"
        variable_list.varvalue = print_rc_list.etd_time


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ACC"
        variable_list.varvalue = print_rc_list.no_guest


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ADDRESS1"
        variable_list.varvalue = print_rc_list.guest_address1


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ADDRESS2"
        variable_list.varvalue = print_rc_list.guest_address2


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ADDRESS1"
        variable_list.varvalue = print_rc_list.guest_address3


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$RESIDENT"
        variable_list.varvalue = print_rc_list.guest_city


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ZIP"
        variable_list.varvalue = print_rc_list.guest_zip


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$COUNTRY"
        variable_list.varvalue = print_rc_list.guest_country


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$GCOMPANY"
        variable_list.varvalue = print_rc_list.company_name


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$RSV-ADDR1"
        variable_list.varvalue = print_rc_list.rsv_addr1


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$RSV-ADDR2"
        variable_list.varvalue = print_rc_list.rsv_addr2


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$RSV-ADDR3"
        variable_list.varvalue = print_rc_list.rsv_addr3


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$RSV-CITY"
        variable_list.varvalue = print_rc_list.rsv_city


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$RSV-ZIP"
        variable_list.varvalue = print_rc_list.rsv_zip


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$RSV-COUNTRY"
        variable_list.varvalue = print_rc_list.rsv_country


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$CCARD"
        variable_list.varvalue = print_rc_list.ccard


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$BIRTHPLACE"
        variable_list.varvalue = print_rc_list.birth_place


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$BIRTDATE"
        variable_list.varvalue = print_rc_list.birth_date


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ID-No"
        variable_list.varvalue = print_rc_list.guest_id


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$ID-EXPIRED"
        variable_list.varvalue = print_rc_list.expired_id


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$NATION1"
        variable_list.varvalue = print_rc_list.guest_nation


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$PURPOSE"
        variable_list.varvalue = print_rc_list.purpose_stay


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$BL-INSTRUCT"
        variable_list.varvalue = print_rc_list.bill_instruct


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$EMAIL"
        variable_list.varvalue = print_rc_list.guest_email


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$resno"
        variable_list.varvalue = print_rc_list.resnr


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$PROVINCE"
        variable_list.varvalue = print_rc_list.province


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$PHONE"
        variable_list.varvalue = print_rc_list.phone


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$OCCUPATION"
        variable_list.varvalue = print_rc_list.occupation


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$CHILD1"
        variable_list.varvalue = print_rc_list.child1


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$CHILD2"
        variable_list.varvalue = print_rc_list.child2


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$MAIN-COMMENT"
        variable_list.varvalue = print_rc_list.main_comment


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$MEMBER-COMMENT"
        variable_list.varvalue = print_rc_list.member_comment


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$DEPOSITGEF"
        variable_list.varvalue = print_rc_list.depositgef


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$DEPOSITBEZ"
        variable_list.varvalue = print_rc_list.depositbez


        variable_list = Variable_list()
        variable_list_data.append(variable_list)

        variable_list.varkey = "$SEGMENT"
        variable_list.varvalue = print_rc_list.segment

        if num_entries(print_rc_list.last_name, "-") > 1:
            variable_list = Variable_list()
            variable_list_data.append(variable_list)

            variable_list.varkey = "$Name1"
            variable_list.varvalue = entry(0, print_rc_list.last_name, "-")


            variable_list = Variable_list()
            variable_list_data.append(variable_list)

            variable_list.varkey = "$MC-TYPE"
            variable_list.varvalue = entry(1, print_rc_list.last_name, "-")


        else:
            variable_list = Variable_list()
            variable_list_data.append(variable_list)

            variable_list.varkey = "$Name1"
            variable_list.varvalue = print_rc_list.last_name

        if num_entries(print_rc_list.telefax, ";") > 1:
            variable_list = Variable_list()
            variable_list_data.append(variable_list)

            variable_list.varkey = "$TELEFAX"
            variable_list.varvalue = entry(0, print_rc_list.telefax, ";")


            variable_list = Variable_list()
            variable_list_data.append(variable_list)

            variable_list.varkey = "$CARD-NUM"
            variable_list.varvalue = entry(1, print_rc_list.telefax, ";")


        else:
            variable_list = Variable_list()
            variable_list_data.append(variable_list)

            variable_list.varkey = "$TELEFAX"
            variable_list.varvalue = print_rc_list.telefax

        if num_entries(print_rc_list.mobile_no, ";") > 1:
            variable_list = Variable_list()
            variable_list_data.append(variable_list)

            variable_list.varkey = "$MOBILE"
            variable_list.varvalue = entry(0, print_rc_list.mobile_no, ";")


            variable_list = Variable_list()
            variable_list_data.append(variable_list)

            variable_list.varkey = "$SOURCE"
            variable_list.varvalue = entry(1, print_rc_list.mobile_no, ";")


        else:
            variable_list = Variable_list()
            variable_list_data.append(variable_list)

            variable_list.varkey = "$MOBILE"
            variable_list.varvalue = print_rc_list.mobile_no

    return generate_output()