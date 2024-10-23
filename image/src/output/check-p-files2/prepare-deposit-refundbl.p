
DEF TEMP-TABLE t-reservation    LIKE reservation.
DEF TEMP-TABLE t-artikel        LIKE artikel
    FIELD pay-exrate AS DECIMAL INIT 1
    FIELD w-wabkurz  LIKE waehrung.wabkurz.

DEF INPUT  PARAMETER resnr          AS INT.
DEF OUTPUT PARAMETER deposit-exrate AS DECIMAL INITIAL 1.
DEF OUTPUT PARAMETER depobezeich    AS CHAR.
DEF OUTPUT PARAMETER depoart        AS INT INIT 0.
DEF OUTPUT PARAMETER flag-err       AS INT INIT 0.
DEF OUTPUT PARAMETER p-60           AS INT.
DEF OUTPUT PARAMETER p-152          AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-reservation.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.

RUN htpint.p(60, OUTPUT p-60).
RUN htpchar.p(152, OUTPUT p-152).
FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
AND artikel.departement = 0 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel THEN 
DO: 
    flag-err = 1.
    /*
  hide MESSAGE NO-PAUSE. 
  MESSAGE translateExtended ("Deposit article not yet defined (group 5, no 120).",lvCAREA,"") 
  VIEW-AS ALERT-BOX INFORMATION. 
    */
  RETURN. 
END. 
ELSE 
DO: 
  ASSIGN
    depoart = artikel.artnr
    depobezeich = artikel.bezeich.
  IF artikel.pricetab THEN
  DO:
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
      NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung THEN 
        ASSIGN deposit-exrate = waehrung.ankauf / waehrung.einheit.
  END.
END. 

FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK. 
CREATE t-reservation.
BUFFER-COPY reservation TO t-reservation.

FOR EACH artikel WHERE artikel.departement = 0 
    AND (artart = 6 OR artart = 7) 
    AND artikel.activeflag NO-LOCK:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.

    IF artikel.pricetab THEN
    DO:
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
          NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN 
          ASSIGN 
            t-artikel.pay-exrate = waehrung.ankauf / waehrung.einheit
            t-artikel.w-wabkurz  = waehrung.wabkurz.
        ELSE t-artikel.pay-exrate = 1.
    END.
END.

