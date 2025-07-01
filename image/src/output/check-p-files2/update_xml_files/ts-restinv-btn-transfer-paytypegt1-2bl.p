DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT PARAMETER rec-id  AS INT.
DEF INPUT PARAMETER do-it   AS LOGICAL.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER disc-art1 AS INT.
DEF INPUT PARAMETER disc-art2 AS INT.
DEF INPUT PARAMETER disc-art3 AS INT.
DEF INPUT PARAMETER kellner-kellner-nr AS INT.

DEF OUTPUT PARAMETER bill-date AS DATE.
DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.

IF do-it THEN
DO:
  FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
  vhp.h-bill.flag = 1. 
  FIND CURRENT vhp.h-bill NO-LOCK.
END. 
RUN fill-cover.
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
CREATE t-h-bill.
BUFFER-COPY h-bill TO t-h-bill.
ASSIGN t-h-bill.rec-id = RECID(h-bill).


PROCEDURE fill-cover: 
  DEF VAR f-pax  AS INTEGER INITIAL 0   NO-UNDO. 
  DEF VAR b-pax  AS INTEGER INITIAL 0   NO-UNDO.
  DEF VAR str     AS CHAR               NO-UNDO.
  DEF BUFFER h-art1 FOR vhp.h-artikel. 
  DEF BUFFER tbuff  FOR vhp.tisch.

  DO TRANSACTION: 
    
    FIND FIRST tbuff WHERE tbuff.tischnr = vhp.h-bill.tischnr 
        AND tbuff.departement = vhp.h-bill.departement NO-ERROR.
    IF AVAILABLE tbuff AND tbuff.roomcharge AND tbuff.kellner-nr NE 0 THEN
    DO:
        FIND CURRENT tbuff EXCLUSIVE-LOCK.
        ASSIGN tbuff.kellner-nr = 0.
        FIND CURRENT tbuff NO-LOCK.
    END.
    RUN release-TBplan.

    IF vhp.h-bill.resnr GT 0 THEN 
    RUN rest-addgastinfo.p(vhp.h-bill.departement, vhp.h-bill.rechnr,
      vhp.h-bill.resnr, vhp.h-bill.reslinnr, 0, transdate).

    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
    ASSIGN vhp.h-bill.kellner-nr = kellner-kellner-nr NO-ERROR.
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 739 NO-LOCK.
    IF vhp.htparam.flogical THEN 
    DO:
      flag = 1.
      /*MTRUN TS-voucherUI.p(OUTPUT str).
      IF str NE "" THEN ASSIGN vhp.h-bill.service[5] = DECIMAL(str).*/
    END.
    FIND CURRENT vhp.h-bill NO-LOCK.

    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
    /* vhp.bill DATE */ 
    bill-date = vhp.htparam.fdate. 
    IF transdate NE ? THEN bill-date = transdate. 
    ELSE 
    DO: 
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
      IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
    END. 
 
    FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = 0 
      AND vhp.h-umsatz.departement = curr-dept AND 
      vhp.h-umsatz.betriebsnr = curr-dept 
      AND vhp.h-umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE vhp.h-umsatz THEN 
    DO: 
      create vhp.h-umsatz. 
      vhp.h-umsatz.artnr = 0. 
      vhp.h-umsatz.departement = curr-dept. 
      vhp.h-umsatz.betriebsnr = curr-dept. 
      vhp.h-umsatz.datum = bill-date. 
    END. 
    vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl + vhp.h-bill.belegung. 
 
    IF vhp.h-bill.belegung NE 0 THEN 
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr 
        AND vhp.h-bill-line.departement = vhp.h-bill.departement 
        AND vhp.h-bill-line.artnr NE disc-art1 
        AND vhp.h-bill-line.artnr NE disc-art2 
        AND vhp.h-bill-line.artnr NE disc-art3 NO-LOCK, 
        FIRST h-art1 WHERE h-art1.artnr = vhp.h-bill-line.artnr 
        AND h-art1.departement = vhp.h-bill-line.departement 
        AND h-art1.artart = 0 NO-LOCK, 
        FIRST vhp.artikel WHERE vhp.artikel.artnr = h-art1.artnrfront 
        AND vhp.artikel.departement = h-art1.departement NO-LOCK: 
        IF vhp.artikel.umsatzart = 3 OR vhp.artikel.umsatzart = 5 THEN 
            f-pax = f-pax + h-bill-line.anzahl. 
        ELSE IF vhp.artikel.umsatzart = 6 THEN 
            b-pax = b-pax + h-bill-line.anzahl. 
    END. 
 
    IF vhp.h-bill.belegung > 0 THEN 
    DO: 
        IF f-pax > vhp.h-bill.belegung THEN f-pax = vhp.h-bill.belegung. 
        IF b-pax > vhp.h-bill.belegung THEN b-pax = vhp.h-bill.belegung. 
    END. 
    ELSE IF vhp.h-bill.belegung < 0 THEN 
    DO: 
        IF f-pax < vhp.h-bill.belegung THEN f-pax = vhp.h-bill.belegung. 
        IF b-pax < vhp.h-bill.belegung THEN b-pax = vhp.h-bill.belegung. 
    END. 
    vhp.h-umsatz.betrag = vhp.h-umsatz.betrag + f-pax. 
    vhp.h-umsatz.nettobetrag = vhp.h-umsatz.nettobetrag + b-pax. 
 
    FIND CURRENT vhp.h-umsatz NO-LOCK. 
    RELEASE vhp.h-umsatz. 
  END. 
END. 



PROCEDURE release-TBplan:
    FIND FIRST vhp.queasy WHERE vhp.queasy.KEY = 31 
      AND vhp.queasy.number1 = vhp.h-bill.departement
      AND vhp.queasy.number2 = vhp.h-bill.tischnr NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy THEN
    DO TRANSACTION:
      FIND CURRENT vhp.queasy EXCLUSIVE-LOCK.
      ASSIGN vhp.queasy.number3 = 0
             vhp.queasy.date1 = ?.
      FIND CURRENT vhp.queasy NO-LOCK.
      RELEASE vhp.queasy.
    END.
END.
