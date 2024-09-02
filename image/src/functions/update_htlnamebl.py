from functions.additional_functions import *
import decimal
from models import Paramtext

def update_htlnamebl(htl_name:str, htl_adr1:str, htl_adr2:str, htl_adr3:str, htl_tel:str, htl_fax:str, htl_email:str):
    paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal paramtext


        return {}

    def update_it():

        nonlocal paramtext

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 200)).first()
        paramtext.ptexte = htl_name

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 201)).first()
        paramtext.ptexte = htl_adr1

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 202)).first()
        paramtext.ptexte = htl_adr2

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 203)).first()
        paramtext.ptexte = htl_adr3

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 204)).first()
        paramtext.ptexte = htl_tel

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 205)).first()
        paramtext.ptexte = htl_fax

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 206)).first()
        paramtext.ptexte = htl_email

    update_it()

    return generate_output()