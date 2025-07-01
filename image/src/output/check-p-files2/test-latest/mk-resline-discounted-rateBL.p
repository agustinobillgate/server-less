DEF TEMP-TABLE t-katpreis       LIKE katpreis.

DEF INPUT  PARAMETER res-mode       AS CHAR.
DEF INPUT  PARAMETER r-arrangement  AS CHAR.
DEF INPUT  PARAMETER r-betriebsnr   AS INT.
DEF INPUT  PARAMETER r-ankunft      AS DATE.
DEF INPUT  PARAMETER r-zikatnr      AS INT.
DEF INPUT  PARAMETER r-erwachs      AS INT.
DEF INPUT  PARAMETER r-kind1        AS INT.
DEF INPUT  PARAMETER r-kind2        AS INT.
DEF INPUT  PARAMETER ci-date        AS DATE.
DEF OUTPUT PARAMETER exrate1        AS DECIMAL INITIAL 1  NO-UNDO.
DEF OUTPUT PARAMETER exrate2        AS DECIMAL INITIAL 1  NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-katpreis.

DEF VAR datum     AS DATE               NO-UNDO.
DEFINE VARIABLE wd-array            AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

FIND FIRST arrangement WHERE arrangement.arrangement = r-arrangement 
      NO-LOCK NO-ERROR. 
IF NOT AVAILABLE arrangement THEN RETURN. 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar 
    NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exrate1 = waehrung.ankauf / waehrung.einheit. 
 
FIND FIRST waehrung WHERE waehrung.waehrungsnr = r-betriebsnr
    NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exrate2 = waehrung.ankauf / waehrung.einheit. 
 
datum = r-ankunft.
IF res-mode = "inhouse" THEN datum = ci-date. 
FIND FIRST katpreis WHERE katpreis.zikatnr = r-zikatnr 
    AND katpreis.argtnr = arrangement.argtnr 
    AND katpreis.startperiode LE datum 
    AND katpreis.endperiode GE datum 
    AND katpreis.betriebsnr = wd-array[WEEKDAY(datum)] NO-LOCK NO-ERROR. 
IF NOT AVAILABLE katpreis THEN 
FIND FIRST katpreis WHERE katpreis.zikatnr = r-zikatnr 
    AND katpreis.argtnr = arrangement.argtnr 
    AND katpreis.startperiode LE datum 
    AND katpreis.endperiode GE datum 
    AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE katpreis THEN RETURN. 
ELSE
DO:
    CREATE t-katpreis.
    BUFFER-COPY katpreis TO t-katpreis.
END.

