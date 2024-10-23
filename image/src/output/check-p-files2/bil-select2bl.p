
DEFINE BUFFER guest1 FOR guest.

DEFINE TEMP-TABLE b1-list
    FIELD rechnr    LIKE bill.rechnr
    FIELD name      LIKE guest1.name
    FIELD vorname1  LIKE guest1.vorname1
    FIELD anrede1   LIKE guest1.anrede1
    FIELD adresse1  LIKE guest1.adresse1
    FIELD saldo     LIKE bill.saldo
    FIELD groupname LIKE reservation.groupname
    FIELD resnr     LIKE bill.resnr
    FIELD printnr   LIKE bill.printnr
    FIELD zinr      LIKE res-line.zinr
    FIELD datum     LIKE bill.datum
    FIELD wohnort   LIKE guest1.wohnort
    FIELD plz       LIKE guest1.plz
    FIELD bemerk    LIKE guest1.bemerk
    FIELD rec-id    AS INTEGER.

DEFINE TEMP-TABLE b2-list
  FIELD gastnr AS INTEGER 
  FIELD rechnr LIKE bill.rechnr FORMAT ">>>>>>>9" 
  FIELD name AS CHAR FORMAT "x(36)" LABEL "Bill Receiver" 
  FIELD saldo LIKE bill.saldo FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD groupname LIKE reservation.groupname 
  FIELD resnr LIKE bill.resnr 
  FIELD printnr LIKE bill.printnr 
  FIELD zinr LIKE res-line.zinr
  FIELD datum LIKE bill.datum. 

DEFINE INPUT PARAMETER case-type    AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER resnr        AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER bil-flag     AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER master-flag  AS LOGICAL      NO-UNDO.
DEFINE INPUT PARAMETER sorttype     AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER gastname     AS CHARACTER    NO-UNDO.
DEFINE INPUT PARAMETER curr-gastnr  AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER bill-type    AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER ci-date      AS DATE         NO-UNDO.

DEFINE OUTPUT PARAMETER resname     AS CHAR         INIT "".
DEFINE OUTPUT PARAMETER address     AS CHAR         INIT "".
DEFINE OUTPUT PARAMETER city        AS CHAR         INIT "".
DEFINE OUTPUT PARAMETER comments    AS CHAR         INIT "".
DEFINE OUTPUT PARAMETER TABLE FOR b1-list.
DEFINE OUTPUT PARAMETER TABLE FOR b2-list.

IF case-type = 1 THEN
DO:
    IF bil-flag = 0 THEN RUN disp-bill-list0. 
    ELSE RUN disp-bill-list1. 
END.
ELSE IF case-type = 2 THEN
DO:
    RUN build-blist.
END.
 
/*************** PROCEDURE ***************/
PROCEDURE build-blist: 
DEFINE BUFFER rline FOR res-line.

  FOR EACH  bill WHERE bill.resnr GT 0 AND bill.reslinnr EQ 0
    AND bill.flag = bil-flag NO-LOCK BY bill.NAME:
    
    FIND FIRST res-line WHERE res-line.resnr =  bill.resnr 
      AND res-line.active-flag LE 1 NO-LOCK NO-ERROR. 
    
    IF NOT AVAILABLE res-line THEN 
    DO: 
      FIND FIRST rline WHERE rline.resnr =  bill.resnr 
        AND rline.resstatus = 8 NO-LOCK NO-ERROR.
      IF NOT AVAILABLE rline THEN
      FIND FIRST history WHERE history.resnr =  bill.resnr 
        AND history.reslinnr LT 999 
        AND history.zi-wechsel = NO NO-LOCK NO-ERROR.
      FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK. 
      FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK
          NO-ERROR. 
      
      CREATE b2-list. 
      ASSIGN
        b2-list.rechnr = bill.rechnr
        b2-list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
        b2-list.saldo = bill.saldo
        b2-list.resnr = bill.resnr
        b2-list.printnr = bill.printnr 
        b2-list.datum = bill.datum
        b2-list.gastnr = guest.gastnr
      . 
      IF AVAILABLE reservation THEN b2-list.groupname = reservation.groupname. 
      IF AVAILABLE rline THEN b2-list.zinr = rline.zinr.
      ELSE IF AVAILABLE history THEN b2-list.zinr = history.zinr.
    END. 
  END. 
END. 
 
PROCEDURE disp-bill-list0: 
DEFINE VARIABLE fr-name AS CHAR INITIAL " ". 
DEFINE VARIABLE to-name AS CHAR. 
  IF master-flag THEN RETURN.
  
  IF sorttype = 1 AND gastname NE "" THEN 
  DO: 
    IF curr-gastnr = 0 THEN 
    DO: 
      IF gastname = "*" THEN 
      DO: 
        to-name = "zz". 
        FOR EACH bill WHERE bill.zinr EQ "" 
          AND bill.flag = bil-flag 
          AND bill.name GE fr-name AND bill.name LE to-name 
          AND bill.resnr GT 0 AND bill.reslinnr = 0 
          AND bill.billtyp = bill-type NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK, 
          FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
          BY bill.rechnr descending:
            RUN assign-it.
        END.
      END. 
      ELSE 
      DO: 
        to-name = chr(asc(SUBSTR(gastname,1,1)) + 1). 
        FOR EACH bill WHERE bill.zinr EQ "" 
          AND bill.flag = bil-flag 
          AND bill.name GE gastname AND bill.name LE to-name 
          AND bill.resnr GT 0 AND bill.reslinnr = 0 
          AND bill.billtyp = bill-type NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK, 
          FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
          BY bill.rechnr descending:
            RUN assign-it.
        END.
      END. 
    END. 
    ELSE 
      FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
        AND bill.gastnr = curr-gastnr 
        AND bill.resnr GT 0 AND bill.reslinnr = 0 
        AND bill.billtyp = bill-type NO-LOCK USE-INDEX gastnr_index, 
        FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
        FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK, 
        FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
        BY bill.rechnr descending:
        RUN assign-it.
      END.
  END. 
  ELSE IF sorttype = 2 THEN 
  DO:
    FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
      AND bill.rechnr EQ resnr 
      AND bill.reslinnr = 0 AND bill.billtyp = bill-type NO-LOCK, 
      FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
      FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK, 
      FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.rechnr:
        RUN assign-it.
    END.
    FIND FIRST b1-list NO-ERROR.
    IF NOT AVAILABLE b1-list THEN 
    FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
      AND bill.rechnr GE resnr AND bill.rechnr LE (resnr + 1000) 
      AND bill.reslinnr = 0 AND bill.billtyp = bill-type NO-LOCK, 
      FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
      FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK, 
      FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.rechnr:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 3 THEN 
  DO: 
    IF curr-gastnr = 0 THEN 
    DO: 
      to-name = chr(asc(SUBSTR(gastname,1,1)) + 1). 
      IF gastname = "" THEN
      FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
        AND bill.name GE gastname AND bill.resnr GT 0 AND bill.reslinnr = 0 
        AND bill.billtyp = bill-type NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
        FIRST res-line WHERE res-line.resnr = bill.resnr 
          AND res-line.abreise = ci-date NO-LOCK, 
        FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
        BY bill.rechnr descending:
          RUN assign-it.
      END.
      ELSE
      FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
        AND bill.name GE gastname AND bill.name LE to-name 
        AND bill.resnr GT 0 AND bill.reslinnr = 0 
        AND bill.billtyp = bill-type NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
        FIRST res-line WHERE res-line.resnr = bill.resnr 
          AND res-line.abreise = ci-date NO-LOCK, 
        FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
        BY bill.rechnr descending:
          RUN assign-it.
      END.
    END. 
    ELSE 
      FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
        AND bill.gastnr = curr-gastnr 
        AND bill.resnr GT 0 AND bill.reslinnr = 0 
        AND bill.billtyp = bill-type NO-LOCK USE-INDEX gastnr_index, 
        FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
        FIRST res-line WHERE res-line.resnr = bill.resnr 
          AND res-line.abreise = ci-date NO-LOCK, 
        FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
        BY bill.rechnr descending:
        RUN assign-it.
      END.
  END. 
  IF AVAILABLE guest1 THEN 
  DO: 
    resname = guest1.name. 
    address = guest1.adresse1. 
    city = guest1.wohnort + " " + guest1.plz. 
    comments = guest1.bemerk. 
    FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK NO-ERROR. 
    IF AVAILABLE reservation AND reservation.bemerk NE "" THEN 
    comments = comments + chr(10) + reservation.bemerk. 
  END. 
END. 
 
PROCEDURE disp-bill-list1: 
DEFINE VARIABLE fr-name AS CHAR INITIAL " ". 
DEFINE VARIABLE to-name AS CHAR. 
  IF master-flag THEN RETURN. 
  IF sorttype = 1 AND gastname NE "" THEN 
  DO: 
    IF curr-gastnr = 0 THEN 
    DO: 
      IF gastname = "*" THEN to-name = "zz". 
      ELSE 
      DO: 
        fr-name = gastname. 
        to-name = chr(asc(SUBSTR(gastname,1,1)) + 1). 
      END. 
      FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
        AND bill.name GE fr-name AND bill.name LE to-name 
        AND bill.resnr GT 0 AND bill.reslinnr = 0 
        AND bill.billtyp = bill-type NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
        FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK, 
        FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
        BY bill.rechnr descending:
          RUN assign-it.
      END.
    END. 
    ELSE 
      FOR EACH bill WHERE bill.flag = bil-flag 
        AND bill.gastnr = curr-gastnr 
        AND bill.resnr GT 0 AND bill.billtyp = bill-type 
        NO-LOCK USE-INDEX gastnr_index, 
        FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
        FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK, 
        FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
        BY bill.rechnr descending:
        RUN assign-it.
      END.
  END. 
  ELSE IF sorttype = 2 AND resnr NE 0 THEN 
  DO: 
    FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
      AND bill.rechnr EQ resnr AND bill.reslinnr = 0 
      AND bill.billtyp = bill-type NO-LOCK, 
      FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
      FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK, 
      FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.rechnr:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 3 AND gastname NE "" THEN 
  DO: 
    IF curr-gastnr = 0 THEN 
    DO: 
      to-name = chr(asc(SUBSTR(gastname,1,1)) + 1). 
      FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
        AND bill.name GE gastname AND bill.name LE to-name 
        AND bill.resnr GT 0 AND bill.reslinnr = 0 
        AND bill.billtyp = bill-type NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
        FIRST res-line WHERE res-line.resnr = bill.resnr 
        AND res-line.abreise = ci-date NO-LOCK, 
        FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
        BY bill.rechnr descending:
          RUN assign-it.
      END.
    END. 
    ELSE 
      FOR EACH bill WHERE bill.zinr EQ "" AND bill.flag = bil-flag 
        AND bill.gastnr = curr-gastnr 
        AND bill.resnr GT 0 AND bill.reslinnr = 0 
        AND bill.billtyp = bill-type NO-LOCK USE-INDEX gastnr_index, 
        FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK, 
        FIRST res-line WHERE res-line.resnr = bill.resnr 
        AND res-line.abreise = ci-date NO-LOCK, 
        FIRST guest1 WHERE guest1.gastnr = bill.gastnr NO-LOCK BY bill.name 
        BY bill.rechnr descending:
        RUN assign-it.
      END.
  END. 
 
  IF AVAILABLE guest1 THEN 
  DO: 
    resname = guest1.name. 
    address = guest1.adresse1. 
    city = guest1.wohnort + " " + guest1.plz. 
    comments = guest1.bemerk. 
    FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK NO-ERROR. 
    IF AVAILABLE reservation AND reservation.bemerk NE "" THEN 
    comments = comments + chr(10) + reservation.bemerk.
  END. 
END. 

PROCEDURE assign-it:
    CREATE b1-list.
    ASSIGN
    b1-list.rechnr    = bill.rechnr
    b1-list.name      = guest1.name
    b1-list.vorname1  = guest1.vorname1
    b1-list.adresse1  = guest1.adresse1
    b1-list.anrede1   = guest1.anrede1
    b1-list.saldo     = bill.saldo
    b1-list.groupname = reservation.groupname
    b1-list.resnr     = bill.resnr
    b1-list.printnr   = bill.printnr
    b1-list.zinr      = res-line.zinr
    b1-list.datum     = bill.datum
    b1-list.wohnort   = guest1.wohnort
    b1-list.plz       = guest1.plz
    b1-list.bemerk    = guest1.bemerk
    b1-list.rec-id    = RECID(bill).
END.
