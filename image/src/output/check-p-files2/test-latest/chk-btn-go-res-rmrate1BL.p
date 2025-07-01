DEF TEMP-TABLE t-reslin-queasy
    FIELD date1   LIKE reslin-queasy.date1
    FIELD date2   LIKE reslin-queasy.date2
    FIELD deci1   LIKE reslin-queasy.deci1
    FIELD char1   LIKE reslin-queasy.char1
    FIELD number3 LIKE reslin-queasy.number3
    FIELD char2   LIKE reslin-queasy.char2
    FIELD char3   LIKE reslin-queasy.char3
    FIELD recid-reslin AS INT.

DEFINE TEMP-TABLE p-list 
  FIELD betrag  LIKE res-line.zipreis COLUMN-LABEL "Room Rate" 
  FIELD date1   AS DATE LABEL "From" 
  FIELD date2   AS DATE LABEL "To" 
  FIELD argt    AS CHAR FORMAT "x(8) " LABEL "ArgCode" 
  FIELD pax     AS INTEGER FORMAT ">>"  LABEL "Adult" INIT 0
  FIELD rcode   AS CHAR FORMAT "x(8)"  LABEL "RateCode"
.


DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER curr-select    AS CHAR.
DEF INPUT  PARAMETER max-rate       AS DECIMAL.
DEF INPUT  PARAMETER fact1          AS DECIMAL.
DEF INPUT  PARAMETER inp-wahrnr     AS INTEGER.
DEF INPUT  PARAMETER inp-zikatnr    AS INTEGER. 
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER resnr          AS INTEGER. 
DEF INPUT  PARAMETER reslinnr       AS INTEGER.
DEF INPUT  PARAMETER recid-reslin   AS INT.
DEF INPUT  PARAMETER contcode       AS CHAR.
DEF INPUT  PARAMETER TABLE FOR p-list.

DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER error-found1   AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER error-code     AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-reslin-queasy.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "chk-btn-go-res-rmrate".

DEF VAR error-found AS LOGICAL.
DEF BUFFER bRQ FOR reslin-queasy.
DEF BUFFER waehrung1 FOR waehrung.

DEF VAR exrate2    AS DECIMAL INITIAL 1. 
DEFINE VARIABLE wd-array AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 


FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 

FOR EACH p-list NO-LOCK:

    FIND FIRST arrangement WHERE arrangement.arrangement = p-list.argt 
        NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE arrangement THEN 
    DO: 
        msg-str = msg-str + CHR(2)
                + translateExtended ("Arrangement Code incorrect.",lvCAREA,"").
        error-code = 1.
        RETURN NO-APPLY.
    END.

    IF curr-select = "add" THEN DO:
        RUN check-rate(OUTPUT error-found).
        IF error-found THEN 
        DO:
             error-found1 = error-found.
             RETURN NO-APPLY. 
        END.
    END.
END.

FOR EACH p-list NO-LOCK:
    IF curr-select = "add" THEN DO:
         CREATE reslin-queasy.
         ASSIGN
          reslin-queasy.key         = "arrangement"
          reslin-queasy.resnr       = resnr
          reslin-queasy.reslinnr    = reslinnr 
          reslin-queasy.date1       = p-list.date1 
          reslin-queasy.date2       = p-list.date2 
          reslin-queasy.deci1       = p-list.betrag 
          reslin-queasy.char1       = p-list.argt
          reslin-queasy.char2       = p-list.rcode
          reslin-queasy.char3       = user-init
          reslin-queasy.number3     = p-list.pax
        .
        FIND CURRENT reslin-queasy NO-LOCK.
        CREATE t-reslin-queasy.
        BUFFER-COPY reslin-queasy TO t-reslin-queasy.
        ASSIGN t-reslin-queasy.recid-reslin  = RECID(reslin-queasy).

        FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr
            AND res-line.reslinnr = reslin-queasy.reslinnr NO-LOCK NO-ERROR.
        RUN res-changes-add.

    END.
    ELSE IF curr-select = "chg" THEN DO:

        FIND FIRST reslin-queasy WHERE RECID(reslin-queasy) = recid-reslin NO-LOCK NO-ERROR.
        FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr
            AND res-line.reslinnr = reslin-queasy.reslinnr
            NO-LOCK NO-ERROR.
        RUN res-changes-chg.
        
        FIND CURRENT reslin-queasy EXCLUSIVE-LOCK.
        ASSIGN
          reslin-queasy.key         = "arrangement"
          reslin-queasy.resnr       = resnr
          reslin-queasy.reslinnr    = reslinnr 
          reslin-queasy.date1       = p-list.date1 
          reslin-queasy.date2       = p-list.date2 
          reslin-queasy.deci1       = p-list.betrag 
          reslin-queasy.char1       = p-list.argt
          reslin-queasy.char2       = p-list.rcode
          reslin-queasy.char3       = user-init
          reslin-queasy.number3     = p-list.pax
        .
        FIND CURRENT reslin-queasy NO-LOCK.
        CREATE t-reslin-queasy.
        BUFFER-COPY reslin-queasy TO t-reslin-queasy.
        ASSIGN t-reslin-queasy.recid-reslin  = recid-reslin.
    END.
END.


FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs AS INTEGER, 
     INPUT kind1 AS INTEGER, 
     INPUT kind2 AS INTEGER). 
  DEF VAR rate AS DECIMAL INITIAL 0. 
  IF erwachs GE 1 AND erwachs LE 4 THEN 
      rate = rate + katpreis.perspreis[erwachs]. 
  rate = rate + kind1 * katpreis.kindpreis[1] + kind2 * katpreis.kindpreis[2]. 
  RETURN rate. 
END FUNCTION. 


PROCEDURE check-rate: 
DEF OUTPUT PARAMETER error-found AS LOGICAL INITIAL NO. 
DEF VARIABLE i AS INTEGER. 
DEF VARIABLE n AS INTEGER. 
DEF VARIABLE val AS DECIMAL. 
DEF VARIABLE max-disc AS DECIMAL INITIAL 0. 
DEF VARIABLE tol-value AS DECIMAL INITIAL 0. 
DEF VARIABLE rack-rate AS DECIMAL. 
DEF VARIABLE datum AS DATE. 

 
DEF VAR exrate1    AS DECIMAL INITIAL 1. 
 
  /*IF bediener.char1 = "" THEN RETURN. */

  IF max-rate NE 0 AND p-list.betrag * fact1 GT max-rate THEN
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("Room Rate incorrect / too large! Check currency.", lvCAREA, "":U).
    error-found = YES. 
    RETURN. 
  END.

  FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr
      NO-LOCK NO-ERROR.
  IF AVAILABLE guest-pr THEN 
  DO:
    FIND FIRST ratecode WHERE ratecode.CODE = guest-pr.CODE
        NO-LOCK NO-ERROR.
    IF AVAILABLE ratecode THEN RETURN.
    FIND FIRST pricecod WHERE pricecod.CODE = guest-pr.CODE
        NO-LOCK NO-ERROR.
    IF AVAILABLE pricecod THEN RETURN.
  END.
  
  n = NUM-ENTRIES(bediener.char1, ";"). 
  DO i = 1 TO n: 
    val = INTEGER(ENTRY(i, bediener.char1, ";")) / 100. 
      IF max-disc LT val THEN max-disc = val. 
  END. 
  max-disc = max-disc / 100. 
  IF max-disc = 0 THEN RETURN. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exrate1 = waehrung.ankauf / waehrung.einheit. 
 
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = inp-wahrnr NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exrate2 = waehrung.ankauf / waehrung.einheit. 
 
  DO datum = p-list.date1 TO p-list.date2: 
    rack-rate = 0. 
    FIND FIRST katpreis WHERE katpreis.zikatnr = inp-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE datum 
      AND katpreis.endperiode GE datum 
      AND katpreis.betriebsnr = wd-array[WEEKDAY(datum)] NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE katpreis THEN 
    FIND FIRST katpreis WHERE katpreis.zikatnr = inp-zikatnr 
      AND katpreis.argtnr = arrangement.argtnr 
      AND katpreis.startperiode LE datum 
      AND katpreis.endperiode GE datum 
      AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE katpreis THEN rack-rate = get-rackrate(res-line.erwachs, 
       res-line.kind1, res-line.kind2). 
 
    rack-rate = rack-rate * exrate1 / exrate2. 
    IF TRUNCATE(rack-rate,0) NE rack-rate THEN 
       rack-rate = ROUND(rack-rate + 0.5, 0). 
 
    IF rack-rate * (1 - max-disc) GT p-list.betrag THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Over discounted rate)",lvCAREA,"")
              + " " + translateExtended ("for date =",lvCAREA,"")
              + " " + STRING(datum).
      error-found = YES. 
      RETURN. 
    END. 
  END.
END. 

PROCEDURE check-currency: 
  FIND FIRST reslin-queasy WHERE key = "arrangement" 
    AND reslin-queasy.resnr = resnr 
    AND reslin-queasy.reslinnr = reslinnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE reslin-queasy THEN 
  DO: 
    IF NOT AVAILABLE guest-pr THEN RETURN. 
    FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 = contcode 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy AND queasy.number1 NE 0 THEN 
    DO: 
      FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = queasy.number1 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung1 AND waehrung1.waehrungsnr 
        NE res-line.betriebsnr THEN 
      DO: 
        FIND CURRENT res-line EXCLUSIVE-LOCK. 
        res-line.betriebsnr = waehrung1.waehrungsnr. 
        FIND CURRENT res-line NO-LOCK. 
        msg-str = msg-str + CHR(2) + "&W"
                + translateExtended ("No AdHoc Rates found; set back the currency code",lvCAREA,"")
                + CHR(10)
                + translateExtended ("to",lvCAREA,"") + " " + waehrung1.bezeich + " " + translateExtended ("as defined in the contract rates.",lvCAREA,"").
      END. 
    END. 
  END. 
END. 

PROCEDURE res-changes-add:
DEF VAR cid   AS CHAR NO-UNDO INIT "".
DEF VAR cdate AS CHAR NO-UNDO FORMAT "x(8)" INIT "        ". 
DEF BUFFER rqy FOR reslin-queasy.

    IF NOT AVAILABLE res-line THEN RETURN.
    IF res-line.active-flag = 2 THEN RETURN. /* res-mode = "NEW" */
    
    IF res-line.changed NE ? THEN
    ASSIGN
        cid   = res-line.changed-id 
        cdate = STRING(res-line.changed)
    .
    CREATE rqy.
    ASSIGN
      rqy.key         = "ResChanges"
      rqy.resnr       = res-line.resnr
      rqy.reslinnr    = res-line.reslinnr
      rqy.date2       = TODAY
      rqy.number2     = TIME 
    . 
    rqy.char3 = STRING(res-line.ankunft) + ";" 
            + STRING(res-line.ankunft) + ";" 
            + STRING(res-line.abreise) + ";" 
            + STRING(res-line.abreise) + ";" 
            + STRING(res-line.zimmeranz) + ";" 
            + STRING(res-line.zimmeranz) + ";" 
            + STRING(res-line.erwachs) + ";" 
            + STRING(res-line.erwachs) + ";" 
            + STRING(res-line.kind1) + ";" 
            + STRING(res-line.kind1) + ";" 
            + STRING(res-line.gratis) + ";" 
            + STRING(res-line.gratis) + ";" 
            + STRING(res-line.zikatnr) + ";" 
            + STRING(res-line.zikatnr) + ";" 
            + STRING(res-line.zinr) + ";" 
            + STRING(res-line.zinr) + ";"
            + STRING(res-line.arrangement) + ";" 
            + STRING(res-line.arrangement) + ";"
            + STRING(res-line.zipreis) + ";" 
            + STRING(res-line.zipreis) + ";"
            + STRING(cid) + ";" 
            + STRING(user-init) + ";" 
            + STRING(cdate, "x(8)") + ";" 
            + STRING(TODAY) + ";" 
            + STRING("ADD Fixrate:") + ";" 
            + STRING(reslin-queasy.date1) 
            + "-" + STRING(reslin-queasy.deci1) + ";"
            + STRING("YES", "x(3)") + ";" 
            + STRING("YES", "x(3)") + ";" 
    .
    FIND CURRENT rqy NO-LOCK.
    RELEASE rqy. 

END.

PROCEDURE res-changes-chg:
DEF VAR cid   AS CHAR NO-UNDO INIT "".
DEF VAR cdate AS CHAR NO-UNDO FORMAT "x(8)" INIT "        ". 
DEF BUFFER rqy FOR reslin-queasy.

    IF NOT AVAILABLE res-line THEN RETURN.
    IF res-line.active-flag = 2 THEN RETURN. /* res-mode = "NEW" */
    
    IF res-line.changed NE ? THEN
    ASSIGN
        cid   = res-line.changed-id 
        cdate = STRING(res-line.changed)
    .

    CREATE rqy.
    ASSIGN
      rqy.key         = "ResChanges"
      rqy.resnr       = res-line.resnr
      rqy.reslinnr    = res-line.reslinnr
      rqy.date2       = TODAY
      rqy.number2     = TIME 
    .  
    rqy.char3 = STRING(res-line.ankunft) + ";" 
            + STRING(res-line.ankunft) + ";" 
            + STRING(res-line.abreise) + ";" 
            + STRING(res-line.abreise) + ";" 
            + STRING(res-line.zimmeranz) + ";" 
            + STRING(res-line.zimmeranz) + ";" 
            + STRING(res-line.erwachs) + ";" 
            + STRING(res-line.erwachs) + ";" 
            + STRING(res-line.kind1) + ";" 
            + STRING(res-line.kind1) + ";" 
            + STRING(res-line.gratis) + ";" 
            + STRING(res-line.gratis) + ";" 
            + STRING(res-line.zikatnr) + ";" 
            + STRING(res-line.zikatnr) + ";" 
            + STRING(res-line.zinr) + ";" 
            + STRING(res-line.zinr) + ";"
            + STRING(res-line.arrangement) + ";" 
            + STRING(res-line.arrangement) + ";"
            + STRING(res-line.zipreis) + ";" 
            + STRING(res-line.zipreis) + ";"
            + STRING(cid) + ";" 
            + STRING(user-init) + ";" 
            + STRING(cdate, "x(8)") + ";" 
            + STRING(TODAY) + ";" 
            + STRING("CHG Fixrate FR:") + ";" 
            + STRING(reslin-queasy.date1) 
            + "-" + STRING(reslin-queasy.deci1) + ";"
            + STRING("YES", "x(3)") + ";" 
            + STRING("YES", "x(3)") + ";" 
    .
    FIND CURRENT rqy NO-LOCK.
    RELEASE rqy. 

    CREATE rqy.
    ASSIGN
      rqy.key         = "ResChanges"
      rqy.resnr       = res-line.resnr
      rqy.reslinnr    = res-line.reslinnr
      rqy.date2       = TODAY
      rqy.number2     = TIME 
    .  
    rqy.char3 = STRING(res-line.ankunft) + ";" 
            + STRING(res-line.ankunft) + ";" 
            + STRING(res-line.abreise) + ";" 
            + STRING(res-line.abreise) + ";" 
            + STRING(res-line.zimmeranz) + ";" 
            + STRING(res-line.zimmeranz) + ";" 
            + STRING(res-line.erwachs) + ";" 
            + STRING(res-line.erwachs) + ";" 
            + STRING(res-line.kind1) + ";" 
            + STRING(res-line.kind1) + ";" 
            + STRING(res-line.gratis) + ";" 
            + STRING(res-line.gratis) + ";" 
            + STRING(res-line.zikatnr) + ";" 
            + STRING(res-line.zikatnr) + ";" 
            + STRING(res-line.zinr) + ";" 
            + STRING(res-line.zinr) + ";"
            + STRING(res-line.arrangement) + ";" 
            + STRING(res-line.arrangement) + ";"
            + STRING(res-line.zipreis) + ";" 
            + STRING(res-line.zipreis) + ";"
            + STRING(cid) + ";" 
            + STRING(user-init) + ";" 
            + STRING(cdate, "x(8)") + ";" 
            + STRING(TODAY) + ";" 
            + STRING("CHG Fixrate TO:") + ";" 
            + STRING(p-list.date1) 
            + "-" + STRING(p-list.betrag) + ";"
            + STRING("YES", "x(3)") + ";" 
            + STRING("YES", "x(3)") + ";" 
    .
    FIND CURRENT rqy NO-LOCK.
    RELEASE rqy. 

END.

