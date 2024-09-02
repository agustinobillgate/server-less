from functions.additional_functions import *
import decimal
from models import Eg_property, Queasy

def sel_itemloc_create_categobjectbl(chrzinr:str, intlocation:int):
    categobjectlist_list = []
    cobjectlist_list = []
    categlist_list = []
    eg_property = queasy = None

    categobjectlist = cobjectlist = categlist = propertybuff = quesbuff = quesbuff1 = None

    categobjectlist_list, Categobjectlist = create_model("Categobjectlist", {"categ_nr":int, "categ_nm":str, "object_nr":int, "object_nm":str, "item_nr":int, "item_nm":str})
    cobjectlist_list, Cobjectlist = create_model("Cobjectlist", {"categ_nr":int, "object_nr":int, "object_nm":str})
    categlist_list, Categlist = create_model("Categlist", {"categ_nr":int, "categ_nm":str})

    Propertybuff = Eg_property
    Quesbuff = Queasy
    Quesbuff1 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal categobjectlist_list, cobjectlist_list, categlist_list, eg_property, queasy
        nonlocal propertybuff, quesbuff, quesbuff1


        nonlocal categobjectlist, cobjectlist, categlist, propertybuff, quesbuff, quesbuff1
        nonlocal categobjectlist_list, cobjectlist_list, categlist_list
        return {"CategObjectList": categobjectlist_list, "cObjectList": cobjectlist_list, "CategList": categlist_list}

    def create_categobject():

        nonlocal categobjectlist_list, cobjectlist_list, categlist_list, eg_property, queasy
        nonlocal propertybuff, quesbuff, quesbuff1


        nonlocal categobjectlist, cobjectlist, categlist, propertybuff, quesbuff, quesbuff1
        nonlocal categobjectlist_list, cobjectlist_list, categlist_list

        intcategob:int = 0
        intobjectnr:int = 0
        intcategex_nr:int = 0
        intobjectex_nr:int = 0
        Propertybuff = Eg_property
        Quesbuff = Queasy
        Quesbuff1 = Queasy

        if chrzinr == "":

            for propertybuff in db_session.query(Propertybuff).filter(
                    (Propertybuff.location == intlocation) &  (Propertybuff.activeflag)).all():

                quesbuff = db_session.query(Quesbuff).filter(
                        (Quesbuff.key == 133) &  (Quesbuff.number1 == propertybuff.maintask)).first()

                if quesbuff:

                    quesbuff1 = db_session.query(Quesbuff1).filter(
                            (Quesbuff1.key == 132) &  (Quesbuff1.number1 == quesbuff.number2)).first()

                    if quesbuff1:

                        if intcategex_nr == 0:
                            intcategex_nr = quesbuff1.number1
                            intcategob = quesbuff1.number1
                            categlist = Categlist()
                            categlist_list.append(categlist)

                            CategList.categ_nr = quesbuff1.number1
                            CategList.categ_nm = quesbuff1.char1


                        else:
                            intcategob = quesbuff1.number1

                            if intcategex_nr != quesbuff1.number1:
                                intcategex_nr = quesbuff1.number1

                                categlist = query(categlist_list, filters=(lambda categlist :categList.categ_nr == quesbuff1.number1), first=True)

                                if categList:
                                    pass
                                else:
                                    categlist = Categlist()
                                    categlist_list.append(categlist)

                                    CategList.categ_nr = quesbuff1.number1
                                    CategList.categ_nm = quesbuff1.char1


                            else:
                                pass
                    else:
                        pass

                    if intobjectex_nr == 0:
                        intobjectex_nr = quesbuff.number1
                        intobjectnr = quesbuff.number1
                        cobjectlist = Cobjectlist()
                        cobjectlist_list.append(cobjectlist)

                        cObjectList.categ_nr = intcategob
                        cObjectList.Object_nr = quesbuff.number1
                        cObjectList.Object_nm = quesbuff.char1


                    else:

                        if intobjectex_nr != quesbuff.number1:
                            intobjectex_nr = quesbuff.number1
                            intobjectnr = quesbuff.number1

                            cobjectlist = query(cobjectlist_list, filters=(lambda cobjectlist :cObjectList.Object_nr == quesbuff.number1), first=True)

                            if cObjectList:
                                pass
                            else:
                                cobjectlist = Cobjectlist()
                                cobjectlist_list.append(cobjectlist)

                                cObjectList.categ_nr = intcategob
                                cObjectList.Object_nr = quesbuff.number1
                                cObjectList.Object_nm = quesbuff.char1


                        else:
                            pass
                else:
                    pass
                categobjectlist = Categobjectlist()
                categobjectlist_list.append(categobjectlist)

                categobjectList.categ_nr = intcategob
                categobjectList.Object_nr = intobjectnr
                categobjectList.Item_nr = propertybuff.nr
                categobjectList.Item_nm = propertybuff.bezeich


        else:

            for propertybuff in db_session.query(Propertybuff).filter(
                    (propertyBuff.location == intlocation) &  (propertyBuff.zinr == chrzinr) &  (Propertybuff.activeflag)).all():

                quesbuff = db_session.query(Quesbuff).filter(
                        (Quesbuff.key == 133) &  (Quesbuff.number1 == propertybuff.maintask)).first()

                if quesbuff:

                    quesbuff1 = db_session.query(Quesbuff1).filter(
                            (Quesbuff1.key == 132) &  (Quesbuff1.number1 == quesbuff.number2)).first()

                    if quesbuff1:

                        if intcategex_nr == 0:
                            intcategex_nr = quesbuff1.number1
                            intcategob = quesbuff1.number1
                            categlist = Categlist()
                            categlist_list.append(categlist)

                            categList.categ_nr = quesbuff1.number1
                            categList.categ_nm = quesbuff1.char1


                        else:
                            intcategob = quesbuff1.number1

                            if intcategex_nr != quesbuff1.number1:
                                intcategex_nr = quesbuff1.number1

                                categlist = query(categlist_list, filters=(lambda categlist :categList.categ_nr == quesbuff1.number1), first=True)

                                if categList:
                                    pass
                                else:
                                    categlist = Categlist()
                                    categlist_list.append(categlist)

                                    categList.categ_nr = quesbuff1.number1
                                    categList.categ_nm = quesbuff1.char1


                            else:
                                pass
                    else:
                        pass

                    if intobjectex_nr == 0:
                        intobjectex_nr = quesbuff.number1
                        intobjectnr = quesbuff.number1
                        cobjectlist = Cobjectlist()
                        cobjectlist_list.append(cobjectlist)

                        cObjectList.categ_nr = intcategob
                        cObjectList.Object_nr = quesbuff.number1
                        cObjectList.Object_nm = quesbuff.char1


                    else:

                        if intobjectex_nr != quesbuff.number1:
                            intobjectex_nr = quesbuff.number1
                            intobjectnr = quesbuff.number1

                            cobjectlist = query(cobjectlist_list, filters=(lambda cobjectlist :cObjectList.Object_nr == quesbuff.number1), first=True)

                            if cObjectList:
                                pass
                            else:
                                cobjectlist = Cobjectlist()
                                cobjectlist_list.append(cobjectlist)

                                cObjectList.categ_nr = intcategob
                                cObjectList.Object_nr = quesbuff.number1
                                cObjectList.Object_nm = quesbuff.char1


                        else:
                            pass
                else:
                    pass
                categobjectlist = Categobjectlist()
                categobjectlist_list.append(categobjectlist)

                categobjectList.categ_nr = intcategob
                categobjectList.Object_nr = intobjectnr
                categobjectList.Item_nr = propertybuff.nr
                categobjectList.Item_nm = propertybuff.bezeich


    create_categobject()

    return generate_output()