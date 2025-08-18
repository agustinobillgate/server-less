#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 18/8/2025
# update compare " " -> " ".strip()
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line

def mobile_reportbl(case_type:int, from_date:date, to_date:date):

    prepare_cache ([Res_line])

    rlist_data = []
    loopi:int = 0
    str1:string = ""
    tot_cimb:int = 0
    tot_cifda:int = 0
    tot_scanmb:int = 0
    tot_scanfda:int = 0
    tot_signmb:int = 0
    tot_signfda:int = 0
    tot_rcmb:int = 0
    tot_rcfda:int = 0
    res_line = None

    rlist = None

    rlist_data, Rlist = create_model("Rlist", {"gastnr":int, "gname":string, "arrive":date, "depart":date, "ci_mobile":string, "ci_fda":string, "scan_mobile":string, "scan_fda":string, "sign_mobile":string, "sign_fda":string, "rc_mobile":string, "rc_fda":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rlist_data, loopi, str1, tot_cimb, tot_cifda, tot_scanmb, tot_scanfda, tot_signmb, tot_signfda, tot_rcmb, tot_rcfda, res_line
        nonlocal case_type, from_date, to_date


        nonlocal rlist
        nonlocal rlist_data

        return {"rlist": rlist_data}


    tot_cimb = 0
    tot_cifda = 0
    tot_scanmb = 0
    tot_scanfda = 0
    tot_signmb = 0
    tot_signfda = 0
    tot_rcmb = 0
    tot_rcfda = 0

    if case_type == 1:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date) & (Res_line.resstatus != 99) & (Res_line.resstatus != 9) & (Res_line.resstatus != 8)).order_by(Res_line._recid).all():
            rlist = Rlist()
            rlist_data.append(rlist)

            rlist.gastnr = res_line.gastnr
            rlist.gname = res_line.name
            rlist.arrive = res_line.ankunft
            rlist.depart = res_line.abreise


            for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str1 = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                if matches(str1,r"*mobile-ci*"):
                    rlist.ci_mobile = "*"
                    tot_cimb = tot_cimb + 1

                if matches(str1,r"*mobile-scan*"):
                    rlist.scan_mobile = "*"
                    tot_scanmb = tot_scanmb + 1

                if matches(str1,r"*mobile-sign-bill*"):
                    rlist.sign_mobile = "*"
                    tot_signmb = tot_signmb + 1

                if matches(str1,r"*mobile-sign-rc*"):
                    rlist.rc_mobile = "*"
                    tot_rcmb = tot_rcmb + 1

            # Rd, 18/8/2025
            # if rlist.ci_mobile == " ":
            if rlist.ci_mobile.strip() == "":
                rlist.ci_fda = "*"
                tot_cifda = tot_cifda + 1

            # Rd, 18/8/2025
            # if rlist.scan_mobile == " ":
            if rlist.scan_mobile.strip() == "":
                rlist.scan_fda = "*"
                tot_scanfda = tot_scanfda + 1

            # Rd, 18/8/2025
            # if rlist.sign_mobile == " ":
            if rlist.sign_mobile.strip() == "":
                rlist.sign_fda = "*"
                tot_signfda = tot_signfda + 1

            # Rd, 18/8/2025
            # if rlist.rc_mobile == " ":
            if rlist.rc_mobile.strip() == "":
                rlist.rc_fda = "*"
                tot_rcfda = tot_rcfda + 1


    elif case_type == 2:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.abreise >= from_date) & (Res_line.abreise <= to_date) & (Res_line.resstatus != 99) & (Res_line.resstatus != 9)).order_by(Res_line._recid).all():
            rlist = Rlist()
            rlist_data.append(rlist)

            rlist.gastnr = res_line.gastnr
            rlist.gname = res_line.name
            rlist.arrive = res_line.ankunft
            rlist.depart = res_line.abreise


            for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str1 = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                if matches(str1,r"*mobile-ci*"):
                    rlist.ci_mobile = "res_line.zimmer_wunsch"  #"*"

                    tot_cimb = tot_cimb + 1

                if matches(str1,r"*mobile-scan*"):
                    rlist.scan_mobile = "*"
                    tot_scanmb = tot_scanmb + 1

                if matches(str1,r"*mobile-sign-bill*"):
                    rlist.sign_mobile = "*"
                    tot_signmb = tot_signmb + 1

                if matches(str1,r"*mobile-sign-rc*"):
                    rlist.rc_mobile = "*"
                    tot_rcmb = tot_rcmb + 1

            # if rlist.ci_mobile == " ":
            #     rlist.ci_fda = "*"
            #     tot_cifda = tot_cifda + 1

            # if rlist.scan_mobile == " ":
            #     rlist.scan_fda = "*"
            #     tot_scanfda = tot_scanfda + 1

            # if rlist.sign_mobile == " ":
            #     rlist.sign_fda = "*"
            #     tot_signfda = tot_signfda + 1

            # if rlist.rc_mobile == " ":
            #     rlist.rc_fda = "*"
            #     tot_rcfda = tot_rcfda + 1
            # Rd, 18/8/2025
            # if rlist.ci_mobile == " ":
            if rlist.ci_mobile.strip() == "":
                rlist.ci_fda = "*"
                tot_cifda = tot_cifda + 1

            # Rd, 18/8/2025
            # if rlist.scan_mobile == " ":
            if rlist.scan_mobile.strip() == "":
                rlist.scan_fda = "*"
                tot_scanfda = tot_scanfda + 1

            # Rd, 18/8/2025
            # if rlist.sign_mobile == " ":
            if rlist.sign_mobile.strip() == "":
                rlist.sign_fda = "*"
                tot_signfda = tot_signfda + 1

            # Rd, 18/8/2025
            # if rlist.rc_mobile == " ":
            if rlist.rc_mobile.strip() == "":
                rlist.rc_fda = "*"
                tot_rcfda = tot_rcfda + 1


    elif case_type == 3:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.abreise >= from_date) & (Res_line.abreise <= to_date) & (Res_line.resstatus == 10)).order_by(Res_line._recid).all():
            rlist = Rlist()
            rlist_data.append(rlist)

            rlist.gastnr = res_line.gastnr
            rlist.gname = res_line.name
            rlist.arrive = res_line.ankunft
            rlist.depart = res_line.abreise


            for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str1 = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                if matches(str1,r"*mobile-ci*"):
                    rlist.ci_mobile = "*"
                    tot_cimb = tot_cimb + 1

                if matches(str1,r"*mobile-scan*"):
                    rlist.scan_mobile = "*"
                    tot_scanmb = tot_scanmb + 1

                if matches(str1,r"*mobile-sign-bill*"):
                    rlist.sign_mobile = "*"
                    tot_signmb = tot_signmb + 1

                if matches(str1,r"*mobile-sign-rc*"):
                    rlist.rc_mobile = "*"
                    tot_rcmb = tot_rcmb + 1

            # if rlist.ci_mobile == " ":
            #     rlist.ci_fda = "*"
            #     tot_cifda = tot_cifda + 1

            # if rlist.scan_mobile == " ":
            #     rlist.scan_fda = "*"
            #     tot_scanfda = tot_scanfda + 1

            # if rlist.sign_mobile == " ":
            #     rlist.sign_fda = "*"
            #     tot_signfda = tot_signfda + 1

            # if rlist.rc_mobile == " ":
            #     rlist.rc_fda = "*"
            #     tot_rcfda = tot_rcfda + 1
            # Rd, 18/8/2025
            # if rlist.ci_mobile == " ":
            if rlist.ci_mobile.strip() == "":
                rlist.ci_fda = "*"
                tot_cifda = tot_cifda + 1

            # Rd, 18/8/2025
            # if rlist.scan_mobile == " ":
            if rlist.scan_mobile.strip() == "":
                rlist.scan_fda = "*"
                tot_scanfda = tot_scanfda + 1

            # Rd, 18/8/2025
            # if rlist.sign_mobile == " ":
            if rlist.sign_mobile.strip() == "":
                rlist.sign_fda = "*"
                tot_signfda = tot_signfda + 1

            # Rd, 18/8/2025
            # if rlist.rc_mobile == " ":
            if rlist.rc_mobile.strip() == "":
                rlist.rc_fda = "*"
                tot_rcfda = tot_rcfda + 1


    rlist = Rlist()
    rlist_data.append(rlist)

    rlist.gastnr = 99999999
    rlist.gname = "T O T A L"
    rlist.ci_mobile = to_string(tot_cimb, ">>>>9")
    rlist.scan_mobile = to_string(tot_scanmb, ">>>>9")
    rlist.sign_mobile = to_string(tot_signmb, ">>>>9")
    rlist.rc_mobile = to_string(tot_rcmb, ">>>>9")
    rlist.ci_fda = to_string(tot_cifda, ">>>>9")
    rlist.scan_fda = to_string(tot_scanfda, ">>>>9")
    rlist.sign_fda = to_string(tot_signfda, ">>>>9")
    rlist.rc_fda = to_string(tot_rcfda, ">>>>9")

    return generate_output()