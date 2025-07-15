from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Telephone

def phone_listbl(case_type:int, name1:str, dept1:str, phone_nr:str, pn:str, mobil_nr:str, lvcoldmobilnr:str):
    t_phone_list_list = []
    telephone = None

    t_phone_list = None
    t_phone_list_list, T_phone_list = create_model("T_phone_list", {"dept":str, "name":str, "telephone":str, "ext":str, "mobil_telefon":str, "fax":str, "adresse1":str, "wohnort":str, "prefix":str, "land":str, "vorname":str, "telex":str, "adresse2":str, "rec_id":int})
    # name1 = name1.strip()
    # dept1 = dept1.strip()
    # phone_nr = phone_nr.strip()
    # mobil_nr = mobil_nr.strip()
    # lvcoldmobilnr = lvcoldmobilnr.strip()
    # pn = pn.strip()

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_phone_list_list, telephone


        nonlocal t_phone_list
        nonlocal t_phone_list_list
        return {"t-phone-list": t_phone_list_list}

    def assign_it():

        nonlocal t_phone_list_list, telephone
        nonlocal t_phone_list
        nonlocal t_phone_list_list

        t_phone_list = T_phone_list()
        t_phone_list_list.append(t_phone_list)

        t_phone_list.dept = telephone.dept
        t_phone_list.name = telephone.name
        t_phone_list.telephone = telephone
        t_phone_list.ext = telephone.ext
        t_phone_list.mobil_telefon = telephone.mobil_telefon
        t_phone_list.fax = telephone.fax
        t_phone_list.adresse1 = telephone.adresse1
        t_phone_list.wohnort = telephone.wohnort
        t_phone_list.prefix = telephone.prefix
        t_phone_list.land = telephone.land
        t_phone_list.vorname = telephone.vorname
        t_phone_list.telex = telephone.telex
        t_phone_list.adresse2 = telephone.adresse2
        t_phone_list.rec_id = telephone._recid

    if case_type == 1:

        if dept1 == "":

            if substring(name1, 0, 1) == "*":

                for telephone in db_session.query(Telephone).filter(
                        (Telephone.name.op("~")(name1))).all():
                    assign_it()
            else:

                for telephone in db_session.query(Telephone).filter(
                        (func.lower(Telephone.name) >= (name1).lower())).all():
                    assign_it()
        else:

            if substring(name1, 0, 1) == "*":

                for telephone in db_session.query(Telephone).filter(
                        (func.lower(Telephone.dept) >= (dept1).lower()) &  (Telephone.name.op("~")(name1))).all():
                    assign_it()
            else:

                for telephone in db_session.query(Telephone).filter(
                        (func.lower(Telephone.dept) >= (dept1).lower()) &  (func.lower(Telephone.name) >= (name1).lower())).all():
                    assign_it()

    elif case_type == 2:

        if phone_nr.lower()  == "" and phone_nr.lower()  != (pn).lower() :

            for telephone in db_session.query(Telephone).filter(
                    (func.lower(Telephone.dept) >= (dept1).lower()) &  (func.lower(Telephone.name) >= (name1).lower())).all():
                assign_it()
        else:

            if phone_nr.lower()  != "" and phone_nr.lower()  != (pn).lower() :

                if substring(phone_nr, 0, 1) == "*":

                    for telephone in db_session.query(Telephone).filter(
                            (Telephone.Telephone.op("~")(phone_nr)) &  (func.lower(Telephone.dept) >= (dept1).lower()) &  (func.lower(Telephone.name) >= (name1).lower())).all():
                        assign_it()

                else:

                    for telephone in db_session.query(Telephone).filter(
                            (func.lower(Telephone) >= (phone_nr).lower()) &  (func.lower(Telephone.dept) >= (dept1).lower()) &  (func.lower(Telephone.name) >= (name1).lower())).all():
                        assign_it()


    elif case_type == 3:

        if mobil_nr == "" and mobil_nr != lvcoldmobilnr:

            for telephone in db_session.query(Telephone).filter(
                    (func.lower(Telephone.dept) >= (dept1).lower()) &  (func.lower(Telephone.name) >= (name1).lower())).all():
                assign_it()
        else:

            if mobil_nr != "" and mobil_nr != lvcoldmobilnr:

                if substring(mobil_nr, 0, 1) == "*":

                    for telephone in db_session.query(Telephone).filter(
                            (func.lower(Telephone.dept) >= (dept1).lower()) &  (func.lower(Telephone.name) >= (name1).lower()) &  (Telephone.mobil_telefon.op("~")(mobil_nr + ".*"))).all():
                        assign_it()

                else:

                    for telephone in db_session.query(Telephone).filter(
                            (func.lower(Telephone.dept) >= (dept1).lower()) &  (func.lower(Telephone.name) >= (name1).lower()) &  (func.lower(Telephone.mobil_telefon) >= (mobil_nr).lower())).all():
                        assign_it()

    local_storage.debugging = "phonelist_done"
    return generate_output()