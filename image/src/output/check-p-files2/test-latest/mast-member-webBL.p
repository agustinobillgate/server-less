DEF TEMP-TABLE b-list 
    FIELD resnr AS INTEGER 
    FIELD reslinnr AS INTEGER 
    FIELD rechnr AS INTEGER
    FIELD saldo AS DECIMAL 
    FIELD parent-nr AS INTEGER INITIAL 0 
. 
DEF TEMP-TABLE b1-list
    FIELD resnr       AS INTEGER
    FIELD reslinnr    AS INTEGER
    FIELD zinr        AS CHAR
    FIELD name        AS CHAR
    FIELD erwachs     AS INTEGER
    FIELD rechnr      AS INTEGER
    FIELD saldo       AS DECIMAL 
    FIELD resstatus   AS INTEGER
    FIELD ankunft     AS DATE
    FIELD abreise     AS DATE
    FIELD gname       AS CHAR
    FIELD gratis      AS INTEGER
    FIELD kind1       AS INTEGER
    FIELD kind2       AS INTEGER
    FIELD arrangement AS CHAR 
    FIELD zipreis     AS DECIMAL 
    FIELD wabkurz     AS CHAR
    FIELD bill-name   AS CHAR
    .

DEFINE INPUT PARAMETER resno            AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER billno    AS INTEGER.
DEFINE OUTPUT PARAMETER tot-adult       AS INTEGER.
DEFINE OUTPUT PARAMETER tot-room        AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR b1-list.

DEF BUFFER mbill FOR bill.

    /* can be guest or master bill */
FIND FIRST bill WHERE bill.rechnr = billno NO-LOCK.

IF bill.reslinnr = 0 THEN
   FIND FIRST mbill WHERE mbill.rechnr = billno NO-LOCK. 
ELSE
DO:
  FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.reslinnr = bill.parent-nr NO-LOCK.
  IF res-line.l-zuordnung[5] NE 0 THEN
  FIND FIRST mbill WHERE mbill.resnr = res-line.l-zuordnung[5]
    AND mbill.reslinnr = 0 NO-LOCK NO-ERROR.
  ELSE
  FIND FIRST mbill WHERE mbill.resnr = res-line.resnr 
    AND mbill.reslinnr = 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE mbill THEN RETURN.
END.

ASSIGN billno = mbill.rechnr.

FOR EACH res-line WHERE res-line.resnr = resno 
  AND res-line.resstatus NE 9 
  AND res-line.resstatus NE 10 
  AND res-line.resstatus NE 99 /*dody 17/10/16 add status NE 99*/
  AND res-line.l-zuordnung[3] = 0 NO-LOCK: 

  IF res-line.resstatus NE 12 
     AND res-line.resstatus NE 99 THEN 
      tot-adult = tot-adult + res-line.erwachs.
  IF res-line.resstatus NE 12 AND res-line.resstatus NE 13 
     AND res-line.resstatus NE 99
     AND NOT res-line.zimmerfix THEN 
      tot-room = tot-room + res-line.zimmeranz.
  
  FIND FIRST bill WHERE bill.resnr = res-line.resnr 
    AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
  CREATE b-list. 
  ASSIGN 
    b-list.resnr = res-line.resnr 
    b-list.reslinnr = res-line.reslinnr 
  . 
  IF AVAILABLE bill THEN 
  ASSIGN 
    b-list.rechnr = bill.rechnr 
    b-list.saldo = bill.saldo 
    b-list.parent-nr = bill.parent-nr 
  . 
END. 
 
FOR EACH res-line WHERE res-line.l-zuordnung[5] = resNo
  AND res-line.resstatus NE 12 AND res-line.active-flag LE 1 
  AND res-line.resnr NE resNo NO-LOCK: 
  FIND FIRST bill WHERE bill.resnr = res-line.resnr 
    AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
  CREATE b-list. 
  ASSIGN 
    b-list.resnr = res-line.resnr 
    b-list.reslinnr = res-line.reslinnr 
  . 
  IF AVAILABLE bill THEN 
  ASSIGN 
    b-list.rechnr = bill.rechnr 
    b-list.saldo = bill.saldo 
    b-list.parent-nr = bill.parent-nr 
  . 
END.


FOR EACH res-line WHERE (res-line.resnr = resno 
  AND res-line.resstatus NE 9 
  AND res-line.resstatus NE 10 
  AND res-line.l-zuordnung[3] = 0) OR (res-line.l-zuordnung[5] = resNo 
  AND res-line.resstatus NE 12 
  AND res-line.resstatus NE 99 /*dody 17/10/16 add status NE 99*/
  AND res-line.active-flag LE 1 
  AND res-line.resnr NE resNo) NO-LOCK, 
  FIRST b-list WHERE b-list.resnr = res-line.resnr 
  AND b-list.reslinnr = res-line.reslinnr NO-LOCK 
  BY res-line.zinr BY b-list.parent-nr BY res-line.name:


    CREATE b1-list.
    ASSIGN
        b1-list.zinr        = res-line.zinr
        /*b1-list.name        = res-line.name*/
        b1-list.erwachs     = res-line.erwachs
        b1-list.rechnr      = b-list.rechnr
        b1-list.saldo       = b-list.saldo
        b1-list.resstatus   = res-line.resstatus
        b1-list.ankunft     = res-line.ankunft
        b1-list.abreise     = res-line.abreise
        b1-list.resnr       = res-line.resnr
        b1-list.reslinnr    = res-line.reslinnr
        b1-list.erwachs     = res-line.erwachs
        b1-list.gratis      = res-line.gratis
        b1-list.kind1       = res-line.kind1
        b1-list.kind2       = res-line.kind2
        b1-list.arrangement = res-line.arrangement
        b1-list.zipreis     = res-line.zipreis
        
        .
    IF res-line.resstatus NE 12 THEN b1-list.gname = res-line.NAME.

    FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN b1-list.wabkurz = waehrung.wabkurz.
      ELSE b1-list.wabkurz = "    ".

    FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
      ASSIGN b1-list.bill-name = guest.name + ", " + guest.vorname1 
            + guest.anredefirma + " " + guest.anrede1. 
    END.

    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
      ASSIGN b1-list.NAME = guest.name + ", " + guest.vorname1 
            + guest.anredefirma + " " + guest.anrede1. 
    END.
END.
