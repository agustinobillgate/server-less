DEFINE TEMP-TABLE depo-list
    FIELD group-str     AS CHAR FORMAT "x(1)"
    FIELD resnr         LIKE reservation.resnr COLUMN-LABEL "ResNr" FORMAT ">>>>>>9"
    FIELD reserve-name  LIKE reservation.NAME 
    FIELD grpname       LIKE reservation.groupname
    FIELD guestname     LIKE res-line.NAME
    FIELD ankunft       LIKE res-line.ankunft
    FIELD depositgef    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
    FIELD limitdate     LIKE reservation.limitdate COLUMN-LABEL "Due Date"
    FIELD bal           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" COLUMN-LABEL "Balance"
    FIELD depo1         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" COLUMN-LABEL ""
    FIELD depositbez    LIKE reservation.depositbez
    FIELD datum1        LIKE reservation.zahldatum
    FIELD depo2         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" COLUMN-LABEL ""
    FIELD depositbez2   LIKE reservation.depositbez2
    FIELD datum2        LIKE reservation.zahldatum2
    FIELD status-rsv    AS CHAR
    FIELD departure     LIKE res-line.abreise. /*bernatd 30E6C5*/


DEFINE INPUT  PARAMETER fdate AS DATE.
DEFINE INPUT  PARAMETER tdate AS DATE.
DEFINE INPUT  PARAMETER sorttype AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR depo-list.


DEFINE VARIABLE depo-foreign LIKE artikel.pricetab.
DEFINE VARIABLE depo-curr LIKE artikel.betriebsnr.
DEFINE VARIABLE bill-date AS DATE.
DEFINE VARIABLE exchg-rate AS DECIMAL NO-UNDO.
DEFINE VARIABLE found-it AS LOGICAL INITIAL YES NO-UNDO.


FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK.
FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
    AND artikel.departement = 0 NO-LOCK.
depo-foreign = artikel.pricetab.
depo-curr  = artikel.betriebsnr.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.
bill-date = htparam.fdate.

DEFINE VARIABLE grpstr      AS CHAR FORMAT "x(1)" EXTENT 2 
  INITIAL [" ", "G"] LABEL "   ". 

FOR EACH depo-list:
    DELETE depo-list.
END.

/* start bernatd 30E6C5*/
IF sorttype = 1 THEN
DO:
  IF depo-foreign THEN 
  RUN create-depolist-arr1.
  ELSE  
  RUN create-depolist-arr2.
END.
IF sorttype = 2 THEN
DO:
  IF depo-foreign THEN 
  RUN create-depolist1.
  ELSE 
  RUN create-depolist2.
END.
IF sorttype = 3 THEN
DO:
  IF depo-foreign THEN
  RUN create-depolist-dep1.
  ELSE 
  RUN create-depolist-dep2.
END.
/* end bernatd 30E6C5*/


PROCEDURE create-depolist1: 
  FOR EACH reservation WHERE reservation.depositgef NE 0
    AND ((reservation.zahldatum GE fdate AND reservation.zahldatum LE tdate) OR  
      (reservation.zahldatum2 GE fdate AND reservation.zahldatum2 LE tdate) OR
      (reservation.limitdate GE fdate AND reservation.limitdate LE tdate)),
    FIRST res-line WHERE res-line.resnr = reservation.resnr AND res-line.resstatus LE 8 AND (res-line.abreise GE fdate AND res-line.abreise LE tdate) NO-LOCK BY res-line.abreise:
    CREATE depo-list.
    ASSIGN
      depo-list.group-str     = grpstr[INTEGER(reservation.grpflag) + 1]
      depo-list.resnr         = reservation.resnr
      depo-list.reserve-name  = reservation.NAME
      depo-list.grpname       = reservation.groupname
      depo-list.guestname     = res-line.NAME
      depo-list.ankunft       = res-line.ankunft
      depo-list.depositgef    = reservation.depositgef
      depo-list.limitdate     = reservation.limitdate
      depo-list.datum1        = reservation.zahldatum
      depo-list.datum2        = reservation.zahldatum2
      depo-list.departure     = res-line.abreise.
    IF res-line.resstatus = 6  THEN depo-list.status-rsv = "Checked-In".
    ELSE IF res-line.resstatus = 8 THEN depo-list.status-rsv = "Checked-Out".
    ELSE depo-list.status-rsv = "Reservation".
    IF depo-list.datum1 LT bill-date AND depo-list.datum1 NE ? THEN
    DO:
      FIND FIRST exrate WHERE exrate.artnr = depo-curr AND exrate.datum 
        = depo-list.datum1 NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN exchg-rate = exrate.betrag.
      ELSE found-it = NO.
    END.
    ELSE IF (depo-list.datum1 GE bill-date AND depo-list.datum1 NE ?) OR
      NOT found-it THEN
    DO:
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = depo-curr NO-LOCK NO-ERROR.
      IF AVAILABLE waehrung THEN
        exchg-rate = waehrung.ankauf / waehrung.einheit.
    END.
    IF exchg-rate = 0 THEN exchg-rate = 1.
    depo-list.depo1 = reservation.depositbez * exchg-rate.
    found-it = YES.

    IF depo-list.datum2 LT bill-date AND depo-list.datum2 NE ? THEN
    DO:
      FIND FIRST exrate WHERE exrate.artnr = depo-curr 
        AND exrate.datum = depo-list.datum2 NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN exchg-rate = exrate.betrag.
      ELSE found-it = NO.
   END.
   ELSE IF (depo-list.datum2 GE bill-date AND depo-list.datum2 NE ?) OR
     NOT found-it THEN
   DO:
     FIND FIRST waehrung WHERE waehrung.waehrungsnr = depo-curr NO-LOCK NO-ERROR.
     IF AVAILABLE waehrung THEN
       exchg-rate = waehrung.ankauf / waehrung.einheit.
   END.
   IF exchg-rate = 0 THEN exchg-rate = 1.
   depo-list.depo2 = reservation.depositbez2 * exchg-rate.
   depo-list.bal   = depo-list.depositgef - depo-list.depo1 - depo-list.depo2.
  END.
END.

PROCEDURE create-depolist2:
  FOR EACH reservation WHERE reservation.depositgef NE 0
    AND ((reservation.zahldatum GE fdate AND reservation.zahldatum LE tdate) OR  
      (reservation.zahldatum2 GE fdate AND reservation.zahldatum2 LE tdate) OR
      (reservation.limitdate GE fdate AND reservation.limitdate LE tdate)),
    FIRST res-line WHERE res-line.resnr = reservation.resnr AND res-line.resstatus LE 8 AND (res-line.abreise GE fdate AND res-line.abreise LE tdate) NO-LOCK BY res-line.abreise:
    CREATE depo-list.
    ASSIGN
      depo-list.group-str     = grpstr[INTEGER(reservation.grpflag) + 1]
      depo-list.resnr         = reservation.resnr
      depo-list.reserve-name  = reservation.NAME
      depo-list.grpname       = reservation.groupname
      depo-list.guestname     = res-line.NAME
      depo-list.ankunft       = res-line.ankunft
      depo-list.depositgef    = reservation.depositgef
      depo-list.bal           = reservation.depositgef - reservation.depositbez - reservation.depositbez2
      depo-list.limitdate     = reservation.limitdate
      depo-list.datum1        = reservation.zahldatum
      depo-list.datum2        = reservation.zahldatum2
      depo-list.depo1         = reservation.depositbez
      depo-list.depo2         = reservation.depositbez2
      depo-list.departure     = res-line.abreise.
    IF res-line.resstatus = 6  THEN depo-list.status-rsv = "Checked-In".
    ELSE IF res-line.resstatus = 8 THEN depo-list.status-rsv = "Checked-Out".
    ELSE depo-list.status-rsv = "Reservation".    
  END.                                                  
END.

PROCEDURE create-depolist-arr1: 
  FOR EACH reservation WHERE reservation.depositgef NE 0
    AND ((reservation.zahldatum GE fdate AND reservation.zahldatum LE tdate) OR  
      (reservation.zahldatum2 GE fdate AND reservation.zahldatum2 LE tdate) OR
      (reservation.limitdate GE fdate AND reservation.limitdate LE tdate)),
    FIRST res-line WHERE res-line.resnr = reservation.resnr AND res-line.resstatus LE 8 AND (res-line.ankunft GE fdate AND res-line.ankunft LE tdate) NO-LOCK BY res-line.ankunft:
    CREATE depo-list.
    ASSIGN
      depo-list.group-str     = grpstr[INTEGER(reservation.grpflag) + 1]
      depo-list.resnr         = reservation.resnr
      depo-list.reserve-name  = reservation.NAME
      depo-list.grpname       = reservation.groupname
      depo-list.guestname     = res-line.NAME
      depo-list.ankunft       = res-line.ankunft
      depo-list.depositgef    = reservation.depositgef
      depo-list.limitdate     = reservation.limitdate
      depo-list.datum1        = reservation.zahldatum
      depo-list.datum2        = reservation.zahldatum2
      depo-list.departure     = res-line.abreise.
    IF res-line.resstatus = 6  THEN depo-list.status-rsv = "Checked-In".
    ELSE IF res-line.resstatus = 8 THEN depo-list.status-rsv = "Checked-Out".
    ELSE depo-list.status-rsv = "Reservation".
    IF depo-list.datum1 LT bill-date AND depo-list.datum1 NE ? THEN
    DO:
      FIND FIRST exrate WHERE exrate.artnr = depo-curr AND exrate.datum 
        = depo-list.datum1 NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN exchg-rate = exrate.betrag.
      ELSE found-it = NO.
    END.
    ELSE IF (depo-list.datum1 GE bill-date AND depo-list.datum1 NE ?) OR
      NOT found-it THEN
    DO:
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = depo-curr NO-LOCK NO-ERROR.
      IF AVAILABLE waehrung THEN
        exchg-rate = waehrung.ankauf / waehrung.einheit.
    END.
    IF exchg-rate = 0 THEN exchg-rate = 1.
    depo-list.depo1 = reservation.depositbez * exchg-rate.
    found-it = YES.

    IF depo-list.datum2 LT bill-date AND depo-list.datum2 NE ? THEN
    DO:
      FIND FIRST exrate WHERE exrate.artnr = depo-curr 
        AND exrate.datum = depo-list.datum2 NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN exchg-rate = exrate.betrag.
      ELSE found-it = NO.
   END.
   ELSE IF (depo-list.datum2 GE bill-date AND depo-list.datum2 NE ?) OR
     NOT found-it THEN
   DO:
     FIND FIRST waehrung WHERE waehrung.waehrungsnr = depo-curr NO-LOCK NO-ERROR.
     IF AVAILABLE waehrung THEN
       exchg-rate = waehrung.ankauf / waehrung.einheit.
   END.
   IF exchg-rate = 0 THEN exchg-rate = 1.
   depo-list.depo2 = reservation.depositbez2 * exchg-rate.
   depo-list.bal   = depo-list.depositgef - depo-list.depo1 - depo-list.depo2.
  END.
END.

PROCEDURE create-depolist-arr2:
  FOR EACH reservation WHERE reservation.depositgef NE 0
    AND ((reservation.zahldatum GE fdate AND reservation.zahldatum LE tdate) OR  
      (reservation.zahldatum2 GE fdate AND reservation.zahldatum2 LE tdate) OR
      (reservation.limitdate GE fdate AND reservation.limitdate LE tdate)),
    FIRST res-line WHERE res-line.resnr = reservation.resnr AND res-line.resstatus LE 8 AND (res-line.ankunft GE fdate AND res-line.ankunft LE tdate) NO-LOCK BY res-line.ankunft:
    CREATE depo-list.
    ASSIGN
      depo-list.group-str     = grpstr[INTEGER(reservation.grpflag) + 1]
      depo-list.resnr         = reservation.resnr
      depo-list.reserve-name  = reservation.NAME
      depo-list.grpname       = reservation.groupname
      depo-list.guestname     = res-line.NAME
      depo-list.ankunft       = res-line.ankunft
      depo-list.depositgef    = reservation.depositgef
      depo-list.bal           = reservation.depositgef - reservation.depositbez - reservation.depositbez2
      depo-list.limitdate     = reservation.limitdate
      depo-list.datum1        = reservation.zahldatum
      depo-list.datum2        = reservation.zahldatum2
      depo-list.depo1         = reservation.depositbez
      depo-list.depo2         = reservation.depositbez2
      depo-list.departure     = res-line.abreise.
    IF res-line.resstatus = 6  THEN depo-list.status-rsv = "Checked-In".
    ELSE IF res-line.resstatus = 8 THEN depo-list.status-rsv = "Checked-Out".
    ELSE depo-list.status-rsv = "Reservation".  
  END.                                                  
END.


PROCEDURE create-depolist-dep1: 
  FOR EACH reservation WHERE reservation.depositgef NE 0
    AND ((reservation.zahldatum GE fdate AND reservation.zahldatum LE tdate) OR  
      (reservation.zahldatum2 GE fdate AND reservation.zahldatum2 LE tdate) OR
      (reservation.limitdate GE fdate AND reservation.limitdate LE tdate)),
    FIRST res-line WHERE res-line.resnr = reservation.resnr AND res-line.resstatus LE 8 NO-LOCK BY reservation.zahldatum:
    CREATE depo-list.
    ASSIGN
      depo-list.group-str     = grpstr[INTEGER(reservation.grpflag) + 1]
      depo-list.resnr         = reservation.resnr
      depo-list.reserve-name  = reservation.NAME
      depo-list.grpname       = reservation.groupname
      depo-list.guestname     = res-line.NAME
      depo-list.ankunft       = res-line.ankunft
      depo-list.depositgef    = reservation.depositgef
      depo-list.limitdate     = reservation.limitdate
      depo-list.datum1        = reservation.zahldatum
      depo-list.datum2        = reservation.zahldatum2
      depo-list.departure     = res-line.abreise.
    IF res-line.resstatus = 6  THEN depo-list.status-rsv = "Checked-In".
    ELSE IF res-line.resstatus = 8 THEN depo-list.status-rsv = "Checked-Out".
    ELSE depo-list.status-rsv = "Reservation".
    IF depo-list.datum1 LT bill-date AND depo-list.datum1 NE ? THEN
    DO:
      FIND FIRST exrate WHERE exrate.artnr = depo-curr AND exrate.datum 
        = depo-list.datum1 NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN exchg-rate = exrate.betrag.
      ELSE found-it = NO.
    END.
    ELSE IF (depo-list.datum1 GE bill-date AND depo-list.datum1 NE ?) OR
      NOT found-it THEN
    DO:
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = depo-curr NO-LOCK NO-ERROR.
      IF AVAILABLE waehrung THEN
        exchg-rate = waehrung.ankauf / waehrung.einheit.
    END.
    IF exchg-rate = 0 THEN exchg-rate = 1.
    depo-list.depo1 = reservation.depositbez * exchg-rate.
    found-it = YES.

    IF depo-list.datum2 LT bill-date AND depo-list.datum2 NE ? THEN
    DO:
      FIND FIRST exrate WHERE exrate.artnr = depo-curr 
        AND exrate.datum = depo-list.datum2 NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN exchg-rate = exrate.betrag.
      ELSE found-it = NO.
   END.
   ELSE IF (depo-list.datum2 GE bill-date AND depo-list.datum2 NE ?) OR
     NOT found-it THEN
   DO:
     FIND FIRST waehrung WHERE waehrung.waehrungsnr = depo-curr NO-LOCK NO-ERROR.
     IF AVAILABLE waehrung THEN
       exchg-rate = waehrung.ankauf / waehrung.einheit.
   END.
   IF exchg-rate = 0 THEN exchg-rate = 1.
   depo-list.depo2 = reservation.depositbez2 * exchg-rate.
   depo-list.bal   = depo-list.depositgef - depo-list.depo1 - depo-list.depo2.
  END.
END.

PROCEDURE create-depolist-dep2:
  FOR EACH reservation WHERE reservation.depositgef NE 0
    AND ((reservation.zahldatum GE fdate AND reservation.zahldatum LE tdate) OR  
      (reservation.zahldatum2 GE fdate AND reservation.zahldatum2 LE tdate) OR
      (reservation.limitdate GE fdate AND reservation.limitdate LE tdate)),
    FIRST res-line WHERE res-line.resnr = reservation.resnr AND res-line.resstatus LE 8 NO-LOCK BY reservation.zahldatum:

    CREATE depo-list.
    ASSIGN
      depo-list.group-str     = grpstr[INTEGER(reservation.grpflag) + 1]
      depo-list.resnr         = reservation.resnr
      depo-list.reserve-name  = reservation.NAME
      depo-list.grpname       = reservation.groupname
      depo-list.guestname     = res-line.NAME
      depo-list.ankunft       = res-line.ankunft
      depo-list.depositgef    = reservation.depositgef
      depo-list.bal           = reservation.depositgef - reservation.depositbez - reservation.depositbez2
      depo-list.limitdate     = reservation.limitdate
      depo-list.datum1        = reservation.zahldatum
      depo-list.datum2        = reservation.zahldatum2
      depo-list.depo1         = reservation.depositbez
      depo-list.depo2         = reservation.depositbez2
      depo-list.departure     = res-line.abreise.
    IF res-line.resstatus = 6  THEN depo-list.status-rsv = "Checked-In".
    ELSE IF res-line.resstatus = 8 THEN depo-list.status-rsv = "Checked-Out".
    ELSE depo-list.status-rsv = "Reservation".    
  END.                                                  
END.


