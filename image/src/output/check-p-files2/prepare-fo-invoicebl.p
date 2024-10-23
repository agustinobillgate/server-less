

DEF TEMP-TABLE t-artikel
    FIELD artnr         LIKE artikel.artnr
    FIELD bezeich       LIKE artikel.bezeich
    FIELD epreis        LIKE artikel.epreis
    FIELD departement   LIKE artikel.departement
    FIELD artart        LIKE artikel.artart
    FIELD activeflag    LIKE artikel.activeflag
    FIELD artgrp        LIKE artikel.artgrp
    FIELD bezaendern    LIKE artikel.bezaendern
    FIELD autosaldo     LIKE artikel.autosaldo
    FIELD pricetab      LIKE artikel.pricetab
    FIELD betriebsnr    LIKE artikel.betriebsnr
    FIELD resart        LIKE artikel.resart
    FIELD zwkum         LIKE artikel.zwkum.

DEF TEMP-TABLE t-foinv
    FIELD vipnr1            AS INT
    FIELD vipnr2            AS INT
    FIELD vipnr3            AS INT
    FIELD vipnr4            AS INT
    FIELD vipnr5            AS INT
    FIELD vipnr6            AS INT
    FIELD vipnr7            AS INT
    FIELD vipnr8            AS INT
    FIELD vipnr9            AS INT
    FIELD ext-char          AS CHAR
    FIELD price-decimal     AS INT
    FIELD double-currency   AS LOGICAL
    FIELD change-date       AS LOGICAL
    FIELD foreign-rate      AS LOGICAL
    FIELD exchg-rate        AS DECIMAL INIT 1
    FIELD curr-local        AS CHAR
    FIELD curr-foreign      AS CHAR
    FIELD lvAnzVat          AS INT
    FIELD b-title           AS CHAR
    FIELD artikel-str       AS CHAR
    FIELD p-219             AS LOGICAL
    FIELD p-199             AS LOGICAL
    FIELD p-145             AS INT
    FIELD p-242             AS INT

    FIELD p-60              AS INT
    FIELD p-251             AS LOGICAL
    FIELD p-2313            AS INT
    FIELD p-1116            AS INT
    FIELD p-685             AS INT
    FIELD avail-brief685    AS LOGICAL INIT NO
    
    FIELD p-173             AS CHAR
    FIELD p-2314            AS INT
    FIELD p-83              AS LOGICAL
    
    FIELD p-497             AS INT
    FIELD p-120             AS INT
    FIELD avail-brief497    AS LOGICAL INIT NO

    FIELD p-1086            AS DECIMAL.

DEFINE INPUT  PARAMETER bil-flag       AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-artikel.
DEFINE OUTPUT PARAMETER TABLE FOR t-foinv.

DEFINE VARIABLE vat-artlist     AS INTEGER EXTENT 4 INITIAL [0,0,0,0].
DEFINE VARIABLE lvInt1          AS INTEGER INITIAL 0 NO-UNDO.

/* SY 04 June 2016 */
DEF VARIABLE curr-parent AS INTEGER NO-UNDO INIT 0.
DEF BUFFER bbuff FOR bill.

CREATE t-foinv.
FIND FIRST htparam WHERE htparam.paramnr = 1086 NO-LOCK. 
p-1086 = htparam.fdecimal.

FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
p-120 = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 2314 NO-LOCK. 
p-2314 = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 83 NO-LOCK. 
p-83 = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 60 NO-LOCK. 
t-foinv.p-60 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr = 251 NO-LOCK. 
t-foinv.p-251 = htparam.flogical.
FIND FIRST htparam WHERE htparam.paramnr = 2313 NO-LOCK. 
t-foinv.p-2313 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr = 1116 NO-LOCK. 
t-foinv.p-1116 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr = 685 NO-LOCK. 
t-foinv.p-685 = htparam.finteger.
FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR.
IF AVAILABLE brief THEN avail-brief685 = YES.

FIND FIRST htparam WHERE htparam.paramnr = 497 NO-LOCK. 
t-foinv.p-497 = htparam.finteger.
FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR.
IF AVAILABLE brief THEN avail-brief497 = YES.

FIND FIRST htparam WHERE htparam.paramnr = 173 NO-LOCK. 
t-foinv.p-173 = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 219 NO-LOCK. 
t-foinv.p-219 = htparam.flogical.
FIND FIRST htparam WHERE htparam.paramnr = 199 NO-LOCK. 
t-foinv.p-199 = htparam.flogical.
FIND FIRST htparam WHERE htparam.paramnr = 145 NO-LOCK. 
t-foinv.p-145 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr = 242 NO-LOCK. 
t-foinv.p-242 = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 700 NO-LOCK. 
IF htparam.finteger NE 0 THEN t-foinv.vipnr1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE htparam.paramnr = 701 NO-LOCK. 
IF htparam.finteger NE 0 THEN t-foinv.vipnr2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE htparam.paramnr = 702 NO-LOCK. 
IF htparam.finteger NE 0 THEN t-foinv.vipnr3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE htparam.paramnr = 703 NO-LOCK. 
IF htparam.finteger NE 0 THEN t-foinv.vipnr4 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE htparam.paramnr = 704 NO-LOCK. 
IF htparam.finteger NE 0 THEN t-foinv.vipnr5 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE htparam.paramnr = 705 NO-LOCK. 
IF htparam.finteger NE 0 THEN t-foinv.vipnr6 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE htparam.paramnr = 706 NO-LOCK. 
IF htparam.finteger NE 0 THEN t-foinv.vipnr7 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE htparam.paramnr = 707 NO-LOCK. 
IF htparam.finteger NE 0 THEN t-foinv.vipnr8 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE htparam.paramnr = 708 NO-LOCK. 
IF htparam.finteger NE 0 THEN t-foinv.vipnr9 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

/* SY 23 Oct 2015 */
FIND FIRST htparam WHERE htparam.paramnr = 148 no-lock.  /* Extended CHAR FOR GCF Prog */ 
t-foinv.ext-char = htparam.fchar.
FIND FIRST htparam WHERE htparam.paramnr = 453 NO-LOCK.
IF htparam.feldtyp = 5 AND htparam.fchar NE "" THEN
    ASSIGN t-foinv.ext-char = t-foinv.ext-char + ";" + htparam.fchar.
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
t-foinv.price-decimal = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 240 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN t-foinv.double-currency = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 219 NO-LOCK.
t-foinv.change-date = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
t-foinv.foreign-rate = htparam.flogical.  
IF t-foinv.foreign-rate OR t-foinv.double-currency THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN t-foinv.exchg-rate = waehrung.ankauf / waehrung.einheit. 
END. 
 
FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
t-foinv.curr-local = htparam.fchar. 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
t-foinv.curr-foreign = htparam.fchar. 

ASSIGN t-foinv.lvAnzVat = 0.
FIND FIRST htparam WHERE htparam.paramnr = 132 NO-LOCK.
IF htparam.fchar NE "" THEN
DO lvInt1 = 1 TO NUM-ENTRIES(htparam.fchar, ";"):
  IF INTEGER(ENTRY(lvInt1, htparam.fchar, ";")) NE 0 THEN
  DO:
    t-foinv.lvAnzVat = t-foinv.lvAnzVat + 1.
    vat-artlist[lvAnzVat] = INTEGER(ENTRY(lvInt1, htparam.fchar, ";")).
  END.
END.

FIND FIRST hoteldpt WHERE hoteldpt.num = 0 NO-LOCK. 
IF bil-flag = 0 THEN 
DO: 
  t-foinv.b-title = hoteldpt.depart + " BILLS". 
END. 
ELSE IF bil-flag = 1 THEN 
DO: 
  t-foinv.b-title = hoteldpt.depart + " CLOSED BILLS". 
END. 
 
t-foinv.artikel-str = "F/O Articles".


/* SY 04 June 2016 */
FOR EACH artikel NO-LOCK WHERE artikel.activeflag = YES:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
/*    
    ASSIGN
        t-artikel.artnr         = artikel.artnr
        t-artikel.bezeich       = artikel.bezeich
        t-artikel.epreis        = artikel.epreis
        t-artikel.departement   = artikel.departement
        t-artikel.artart        = artikel.artart
        t-artikel.activeflag    = artikel.activeflag
        t-artikel.artgrp        = artikel.artgrp
        t-artikel.bezaendern    = artikel.bezaendern
        t-artikel.autosaldo     = artikel.autosaldo
        t-artikel.pricetab      = artikel.pricetab
        t-artikel.betriebsnr    = artikel.betriebsnr
        t-artikel.resart        = artikel.resart
        t-artikel.zwkum         = artikel.zwkum.
*/
END.

/* SY 07 June 2016 */
/* Purpose: As prevention of guest bill(s) with wrong RmNo */
IF bil-flag NE 0 THEN RETURN.
FOR EACH bill WHERE bill.resnr GT 0 AND bill.reslinnr GT 0
    AND bill.flag = 0 NO-LOCK BY bill.resnr:
    FIND FIRST res-line WHERE res-line.resnr = bill.resnr
      AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line AND res-line.zinr NE bill.zinr 
        AND res-line.active-flag = 1 THEN
    DO:
        FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
            EXCLUSIVE-LOCK.
        ASSIGN bbuff.zinr = res-line.zinr.
        FIND CURRENT bbuff NO-LOCK.
        RELEASE bbuff.
    END.
END.


