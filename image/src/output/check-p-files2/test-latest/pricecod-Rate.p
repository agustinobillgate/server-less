/* calculate room rate based on the new conract rate setup for a certain date */

DEFINE INPUT PARAMETER resnr        AS INTEGER.
DEFINE INPUT PARAMETER reslinnr     AS INTEGER.
DEFINE INPUT PARAMETER prcode       AS CHAR.
DEFINE INPUT PARAMETER datum        AS DATE.
DEFINE INPUT PARAMETER ankunft      AS DATE.
DEFINE INPUT PARAMETER abreise      AS DATE.
DEFINE INPUT PARAMETER marknr       AS INTEGER.
DEFINE INPUT PARAMETER argtNo       AS INTEGER.
DEFINE INPUT PARAMETER rmcatNo      AS INTEGER.
DEFINE INPUT PARAMETER adult        AS INTEGER.
DEFINE INPUT PARAMETER child1       AS INTEGER.
DEFINE INPUT PARAMETER child2       AS INTEGER.
DEFINE INPUT PARAMETER reserve-dec  AS DECIMAL.
DEFINE INPUT PARAMETER wahrNo       AS INTEGER.
DEFINE OUTPUT PARAMETER rmRate      AS DECIMAL INITIAL 0.
DEFINE OUTPUT PARAMETER rate-found  AS LOGICAL INITIAL NO.
/*
DEFINE VARIABLE resnr        AS INTEGER.
DEFINE VARIABLE reslinnr     AS INTEGER.
DEFINE VARIABLE prcode       AS CHAR INITIAL "ALL1".
DEFINE VARIABLE datum        AS DATE INITIAL "02/20/06".
DEFINE VARIABLE ankunft      AS DATE INITIAL "02/20/06".
DEFINE VARIABLE abreise      AS DATE INITIAL "02/22/06".
DEFINE VARIABLE marknr       AS INTEGER INITIAL 4.
DEFINE VARIABLE argtNo       AS INTEGER INITIAL 8.
DEFINE VARIABLE rmcatNo      AS INTEGER INITIAL 1.
DEFINE VARIABLE adult        AS INTEGER INITIAL 3.
DEFINE VARIABLE child1       AS INTEGER.
DEFINE VARIABLE child2       AS INTEGER.
DEFINE VARIABLE reserve-dec  AS DECIMAL.
DEFINE VARIABLE wahrNo       AS INTEGER.
DEFINE VARIABLE rmRate       AS DECIMAL INITIAL 0.
*/

DEFINE VARIABLE exrate1             AS DECIMAL INITIAL 1    NO-UNDO.
DEFINE VARIABLE ex2                 AS DECIMAL INITIAL 1    NO-UNDO.
DEFINE VARIABLE do-it               AS LOGICAL              NO-UNDO.
DEFINE VARIABLE add-it              AS LOGICAL              NO-UNDO.
DEFINE VARIABLE EBdisc-found        AS LOGICAL              NO-UNDO.
DEFINE VARIABLE KBdisc-found        AS LOGICAL              NO-UNDO.
DEFINE VARIABLE argt-defined        AS LOGICAL              NO-UNDO.
DEFINE VARIABLE qty                 AS INTEGER              NO-UNDO.
DEFINE VARIABLE niteNo              AS INTEGER              NO-UNDO.
DEFINE VARIABLE ci-date             AS DATE                 NO-UNDO.
DEFINE VARIABLE fdatum              AS DATE                 NO-UNDO.
DEFINE VARIABLE tdatum              AS DATE                 NO-UNDO.
DEFINE VARIABLE n                   AS INTEGER              NO-UNDO.
DEFINE VARIABLE ct                  AS CHAR                 NO-UNDO.
DEFINE VARIABLE RmOcc               AS DECIMAL INITIAL -1   NO-UNDO.

/******************* TEMP TABLE **************************************/

DEFINE TEMP-TABLE early-discount
    FIELD disc-rate AS DECIMAL FORMAT " >>"   LABEL "Disc%"
    FIELD min-days  AS INTEGER FORMAT ">>>"   LABEL "Min to C/I(days)"
    FIELD min-stay  AS INTEGER FORMAT ">>>"   LABEL "Min Stays"
    FIELD max-occ   AS INTEGER FORMAT " >>"   LABEL "Upto Occ".

DEFINE TEMP-TABLE kickback-discount
    FIELD disc-rate AS DECIMAL FORMAT " >>"   LABEL "Disc%"
    FIELD max-days  AS INTEGER FORMAT ">>>"   LABEL "Max to C/I(days)"
    FIELD min-stay  AS INTEGER FORMAT ">>>"   LABEL "Min Stays"
    FIELD max-occ   AS INTEGER FORMAT " >>"   LABEL "Upto Occ".

DEFINE TEMP-TABLE stay-pay
    FIELD f-date    AS DATE                      LABEL "FromDate"
    FIELD t-date    AS DATE                      LABEL "ToDate"
    FIELD stay      AS INTEGER FORMAT "     >>>" LABEL "Stay(Nights)"
    FIELD pay       AS INTEGER FORMAT "     >>>" LABEL "Pay(Nights)".

DEF BUFFER kbuff FOR kickback-discount.
DEF BUFFER ebuff FOR early-discount.

/***********************************************************************/

FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN 
DO:    
  rmRate = res-line.zipreis.
  IF SUBSTR(prcode,1,1) = "!" THEN prcode = SUBSTR(prcode,2).
  ELSE
  DO:
    ct = res-line.zimmer-wunsch.
    IF ct MATCHES("*$CODE$*") THEN
    DO:
      ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
      prcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
    END.
  END.
END.

/* check if rate is fixed for the whole stay */
FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
  = marknr NO-LOCK NO-ERROR. 
IF AVAILABLE queasy AND queasy.logi3 THEN datum = ankunft. 

FIND FIRST pricecod WHERE pricecod.code = prcode 
  AND pricecod.marknr = marknr AND pricecod.argtnr = argtNo
  AND pricecod.zikatnr = rmcatNo
  AND pricecod.startperiode LE datum AND pricecod.endperiode GE datum
  NO-LOCK NO-ERROR. 

IF NOT AVAILABLE pricecod THEN RETURN.

rate-found = YES.
rmRate = pricecod.perspreis[adult] + pricecod.kindpreis[1] * child1 
  + pricecod.kindpreis[2] * child2.

/** additional charges IF argt-line price NOT included IN basic room rate **/ 
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.
FIND FIRST arrangement WHERE arrangement.argtnr = argtNo NO-LOCK.
FIND FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr NO-LOCK 
   NO-ERROR. 
IF AVAILABLE waehrung THEN exrate1 = waehrung.ankauf / waehrung.einheit. 
IF reserve-dec NE 0 THEN ex2 = ex2 / reserve-dec. 
ELSE 
DO: 
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = wahrNo NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN ex2 = (waehrung.ankauf / waehrung.einheit). 
END. 
        
FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
   AND NOT argt-line.kind1 AND NOT argt-line.kind2: 
   add-it = NO. 
   IF argt-line.vt-percnt = 0 THEN 
   DO: 
     IF argt-line.betriebsnr = 0 THEN qty = adult. 
     ELSE qty = argt-line.betriebsnr. 
  END. 
  ELSE IF argt-line.vt-percnt = 1 THEN qty = child1. 
  ELSE IF argt-line.vt-percnt = 2 THEN qty = child2. 
 
  IF qty GT 0 THEN 
  DO: 
    IF argt-line.fakt-modus = 1 THEN add-it = YES. 
    ELSE IF argt-line.fakt-modus = 2 THEN 
    DO: 
      IF ankunft GE ci-date THEN add-it = YES. 
    END.
    ELSE IF argt-line.fakt-modus = 3 THEN 
    DO: 
      IF (ankunft + 1) GE ci-date THEN add-it = YES. 
    END. 
    ELSE IF argt-line.fakt-modus = 4 AND DAY(datum) = 1 THEN add-it = YES. 
    ELSE IF argt-line.fakt-modus = 5 AND DAY(datum + 1) = 1 THEN add-it = YES. 
    ELSE IF argt-line.fakt-modus = 6 THEN 
    DO: 
      IF (ankunft + (argt-line.intervall - 1)) GE ci-date THEN add-it = YES.  
    END.
  
    IF add-it THEN 
    DO: 
      argt-defined = NO. 
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
        AND reslin-queasy.char1 = "" AND reslin-queasy.char1 = "" 
        AND reslin-queasy.number1 = argt-line.departement 
        AND reslin-queasy.number2 = argt-line.argtnr 
        AND reslin-queasy.resnr = resnr AND reslin-queasy.reslinnr = reslinnr 
        AND reslin-queasy.number3 = argt-line.argt-artnr 
        AND reslin-queasy.date1 LE datum
        AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        argt-defined = YES. 
        IF argt-line.vt-percnt = 0 THEN 
          rmRate = rmRate + reslin-queasy.deci1 * qty. 
        ELSE IF argt-line.vt-percnt = 1 THEN 
          rmRate = rmRate + reslin-queasy.deci2 * qty. 
        ELSE IF argt-line.vt-percnt = 2 THEN 
          rmRate = rmRate + reslin-queasy.deci3 * qty. 
      END. 
            
      IF NOT argt-defined THEN 
      DO: 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
          AND reslin-queasy.char1 = prcode AND reslin-queasy.number1 = marknr 
          AND reslin-queasy.number2 = argtnO AND reslin-queasy.reslinnr = rmcatNo 
          AND reslin-queasy.number3 = argt-line.argt-artnr 
          AND reslin-queasy.resnr = argt-line.departement 
          AND reslin-queasy.date1 LE datum
          AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO: 
          IF argt-line.vt-percnt = 0 THEN 
            rmRate = rmRate + reslin-queasy.deci1 * qty. 
          ELSE IF argt-line.vt-percnt = 1 THEN 
            rmRate = rmRate + reslin-queasy.deci2 * qty. 
          ELSE IF argt-line.vt-percnt = 2 THEN 
            rmRate = rmRate + reslin-queasy.deci3 * qty. 
        END. 
        ELSE rmRate = rmRate + (argt-line.betrag * qty) * exrate1 / ex2. 
      END. /* not argt-defined   */ 
    END.   /* if do it           */
  END.     /* if qty NE 0        */
END.       /* for each argt-line */
