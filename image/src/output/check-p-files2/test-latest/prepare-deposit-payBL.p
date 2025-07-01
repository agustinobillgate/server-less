DEF TEMP-TABLE t-reservation LIKE reservation.
DEF TEMP-TABLE artikel-list
    FIELD artnr       LIKE artikel.artnr
    FIELD departement LIKE artikel.departement
    FIELD bezeich     LIKE artikel.bezeich
    FIELD artart      LIKE artikel.artart
    FIELD payment     AS DECIMAL
    FIELD pay-exrate  AS INTEGER.


DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-resnr       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER depositgef      AS DECIMAL NO-UNDO.

DEF OUTPUT PARAMETER price-decimal  AS INTEGER.
DEF OUTPUT PARAMETER exchg-rate     AS DECIMAL.
DEF OUTPUT PARAMETER depoart        AS INTEGER.
DEF OUTPUT PARAMETER depobezeich    AS CHAR.
DEF OUTPUT PARAMETER ask-voucher    AS LOGICAL.
DEF OUTPUT PARAMETER deposit-exrate AS DECIMAL INIT 1.
DEF OUTPUT PARAMETER f-tittle       AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER balance        LIKE reservation.depositbez.
DEF OUTPUT PARAMETER paybez1        AS CHAR.
DEF OUTPUT PARAMETER paybez2        AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR artikel-list.
DEF OUTPUT PARAMETER TABLE FOR t-reservation.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "deposit-pay". 

DEFINE VARIABLE unallocated-subgrp  AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE sorttype            AS INTEGER.

RUN htpint.p(116, OUTPUT unallocated-subgrp).

FIND FIRST htparam WHERE htparam.paramnr = 491.
price-decimal = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK.
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR.
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit.

FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
  AND artikel.departement = 0 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Deposit article not yet defined (group 5, no 120.)",lvCAREA,"").
  RETURN. 
END. 
ELSE 
DO: 
  ASSIGN
    depoart = artikel.artnr
    depobezeich = artikel.bezeich 
    ask-voucher = artikel.resart
  . 
  IF artikel.pricetab THEN
  DO:
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
      NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung THEN 
        ASSIGN deposit-exrate = waehrung.ankauf / waehrung.einheit.
  END.
END.

FIND FIRST reservation WHERE reservation.resnr = inp-resnr NO-LOCK.
IF NOT AVAILABLE reservation THEN                     /* Rulita 181124 | Fixing for serverless */
DO:
  RETURN.
END.

ASSIGN balance = depositgef - reservation.depositbez 
  - reservation.depositbez2.

f-tittle = translateExtended ("Deposit Payment",lvCAREA,"") 
  + "  -  " + reservation.name 
  + " / " + translateExtended ("ResNo:",lvCAREA,"") 
  + " " + STRING(reservation.resnr).

sorttype = 1.
RUN display-artikel.

IF reservation.zahlkonto NE 0 THEN
DO:
    FIND FIRST artikel WHERE artikel.artnr = reservation.zahlkonto
        AND artikel.departement = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN paybez1 = artikel.bezeich.
END.
  
IF reservation.zahlkonto2 NE 0 THEN
DO:
    FIND FIRST artikel WHERE artikel.artnr = reservation.zahlkonto2
        AND artikel.departement = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN paybez2 = artikel.bezeich.
END.

CREATE t-reservation.
BUFFER-COPY reservation TO t-reservation.
ASSIGN t-reservation.depositgef = depositgef.

PROCEDURE display-artikel: 
  IF sorttype = 1 THEN
  FOR EACH artikel
      WHERE artikel.departement = 0 AND
      ((artikel.artart = 6 OR artikel.artart = 7)
      OR (artikel.artart = 2 AND (artikel.zwkum = unallocated-subgrp)))
      AND artikel.activeflag = YES
      NO-LOCK BY artikel.artnr:
      RUN assign-it.
  END.
  ELSE
  FOR EACH artikel
      WHERE artikel.departement = 0 AND
      ((artikel.artart = 6 OR artikel.artart = 7)
      OR (artikel.artart = 2 AND (artikel.zwkum = unallocated-subgrp)))
      AND artikel.activeflag = YES
      NO-LOCK BY artikel.bezeich:
      RUN assign-it.
  END.
  /*MT
  IF sorttype = 1 THEN
  FOR EACH artikel WHERE artikel.departement = 0
      AND (/* artart = 4 OR */ artikel.artart = 6 OR artikel.artart = 7) 
      AND artikel.activeflag NO-LOCK BY artikel.artnr:
      RUN assign-it.
  END.
  ELSE IF sorttype = 2 THEN 
  FOR EACH artikel WHERE artikel.departement = 0 
      AND (/* artart = 4 OR */ artikel.artart = 6 OR artikel.artart = 7) 
      AND artikel.activeflag NO-LOCK BY artikel.bezeich:
      RUN assign-it.
  END.
  */
END.

PROCEDURE assign-it:
    CREATE artikel-list.
    ASSIGN
      artikel-list.artnr       = artikel.artnr
      artikel-list.departement = artikel.departement
      artikel-list.bezeich     = artikel.bezeich
      artikel-list.artart      = artikel.artart
      artikel-list.payment     = - balance * deposit-exrate
      artikel-list.pay-exrate  = 1
    .
    IF artikel.pricetab THEN
    DO:
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
        NO-LOCK NO-ERROR.
      IF AVAILABLE waehrung THEN 
        ASSIGN artikel-list.pay-exrate = waehrung.ankauf / waehrung.einheit.
    END.
    /* artikel-list.payment = artikel-list.payment / pay-exrate. */   
    artikel-list.payment = artikel-list.payment / artikel-list.pay-exrate.                   /* Rulita 181124 | Fixing for serverless */
END.
