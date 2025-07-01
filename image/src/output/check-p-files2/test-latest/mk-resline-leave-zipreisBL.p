
DEF TEMP-TABLE t-list
    FIELD datum AS DATE
    FIELD avail-katpreis AS LOGICAL.

DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER r-arrangement  AS CHAR.
DEF INPUT  PARAMETER r-betriebsnr   AS INT.
DEF INPUT  PARAMETER local-nr       AS INT.
DEF INPUT  PARAMETER price-decimal  AS INT.
DEF INPUT  PARAMETER rmcat          AS INT.
DEF OUTPUT PARAMETER wrong-price    AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER exrate1        AS DECIMAL INITIAL 1 NO-UNDO.
DEF OUTPUT PARAMETER exrate2        AS DECIMAL INITIAL 1 NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE datum      AS DATE. 
DEFINE VARIABLE tol-value  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE wd-array            AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE BUFFER   htp1       FOR htparam. 

FIND FIRST arrangement WHERE arrangement.arrangement = r-arrangement NO-LOCK NO-ERROR. 
IF NOT AVAILABLE arrangement THEN 
DO: 
    wrong-price = YES.
    RETURN NO-APPLY. 
END. 

FIND FIRST htp1  WHERE htp1.paramnr = 145 NO-LOCK. 
IF r-betriebsnr = local-nr AND (price-decimal = 0) THEN 
    tol-value = htp1.finteger * 10. 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exrate1 = waehrung.ankauf / waehrung.einheit. 

FIND FIRST waehrung WHERE waehrung.waehrungsnr = r-betriebsnr NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exrate2 = waehrung.ankauf / waehrung.einheit. 


DO datum = from-date TO to-date: 
 
    /*MT
    rack-rate = 0.
    */
    FIND FIRST katpreis WHERE katpreis.zikatnr = rmcat 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE datum 
      AND katpreis.endperiode GE datum 
      AND katpreis.betriebsnr = wd-array[WEEKDAY(datum)] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE katpreis THEN 
    FIND FIRST katpreis WHERE katpreis.zikatnr = rmcat 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE datum 
      AND katpreis.endperiode GE datum 
      AND katpreis.betriebsnr =  0 NO-LOCK NO-ERROR.

    CREATE t-list.
    ASSIGN
        t-list.datum = datum
        t-list.avail-katpreis = AVAILABLE katpreis.
 
    /*MT
    IF AVAILABLE katpreis THEN rack-rate = get-rackrate(reslin-list.erwachs, 
       reslin-list.kind1, reslin-list.kind2). 
 
    rack-rate = rack-rate * exrate1 / exrate2. 
    IF TRUNCATE(rack-rate,0) NE rack-rate THEN 
       rack-rate = ROUND(rack-rate + 0.5, 0). 
 
    IF rack-rate * (1 - max-disc) GT (reslin-list.zipreis + tol-value) THEN 
    DO: 
      MESSAGE translateExtended ("Over discounted rate)",lvCAREA,"") 
        + " " + translateExtended ("for date =",lvCAREA,"") + " " + STRING(datum) 
        VIEW-AS ALERT-BOX INFORMATION. 
      ASSIGN reslin-list.zipreis = price.
      DISP reslin-list.zipreis WITH FRAME frame1.
      APPLY "entry" TO reslin-list.zipreis. 
      wrong-price = YES. 
      RETURN. 
    END. 
    */
END. 
