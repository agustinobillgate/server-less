DEFINE WORKFILE ledger 
  FIELD artnr           AS INTEGER 
  FIELD bezeich         AS CHARACTER FORMAT "x(24)" INITIAL "?????" 
  FIELD debt0           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt1           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt2           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt3           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0. 


DEFINE WORKFILE age-list 
  FIELD artnr           AS INTEGER 
  FIELD rechnr          AS INTEGER 
  FIELD counter         AS INTEGER 
  FIELD gastnr          AS INTEGER 
  FIELD creditlimit     AS DECIMAL 
  FIELD rgdatum         AS DATE 
  FIELD gastname        AS CHARACTER FORMAT "x(34)" 
  FIELD saldo           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt0           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt1           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt2           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt3           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0
  FIELD fcurr           AS CHAR. 

DEFINE TEMP-TABLE output-list 
  FIELD curr         AS CHAR    FORMAT "x(4)"
  FIELD gastnr       AS INTEGER
  FIELD age1         AS CHAR    FORMAT "x(17)" 
  FIELD age2         AS CHAR    FORMAT "x(17)" 
  FIELD age3         AS CHAR    FORMAT "x(17)" 
  FIELD age4         AS CHAR    FORMAT "x(17)" 
  FIELD creditlimit  AS DECIMAL FORMAT ">>>,>>>,>>>,>>>" 
  FIELD STR          AS CHAR. 


DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER from-art AS INT.
DEF INPUT PARAMETER to-art AS INT.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER from-name AS CHAR.
DEF INPUT PARAMETER to-name AS CHAR.
DEF INPUT PARAMETER disptype AS INT.
DEF OUTPUT PARAMETER outlist AS CHAR FORMAT "x(170)".
DEF OUTPUT PARAMETER TABLE FOR output-list.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "ar-age".

DEFINE VARIABLE default-fcurr AS CHAR FORMAT "x(4)" NO-UNDO.
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK.
default-fcurr = htparam.fchar.

DEFINE VARIABLE day1 AS INTEGER INITIAL 30. 
DEFINE VARIABLE day2 AS INTEGER INITIAL 30. 
DEFINE VARIABLE day3 AS INTEGER INITIAL 30.
FIND FIRST htparam WHERE paramnr = 330 NO-LOCK. 
IF finteger NE 0 THEN day1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 331 NO-LOCK. 
IF finteger NE 0 THEN day2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 332 NO-LOCK. 
IF finteger NE 0 THEN day3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
day2 = day2 + day1. 
day3 = day3 + day2. 

DEFINE VARIABLE price-decimal AS INTEGER. 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 


IF SUBSTR(to-name,1,2) = "zz" THEN RUN age-listA.
ELSE RUN age-list.


PROCEDURE age-list:
DEFINE VARIABLE curr-art AS INTEGER. 
DEFINE VARIABLE billdate AS DATE. 
DEFINE VARIABLE ct AS INTEGER FORMAT ">>>9". 
DEFINE VARIABLE t-debet      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-credit     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-comm       AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-adjust     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-saldo      AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt0      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt1      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt2      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt3      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE tmp-saldo    AS DECIMAL FORMAT "->>>>>>>>>>9" INITIAL 0. 
DEFINE VARIABLE curr-name    AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE curr-gastnr  AS INTEGER. 
DEFINE VARIABLE creditlimit  AS DECIMAL. 
DEFINE VARIABLE gastname     AS CHARACTER FORMAT "x(34)". 
DEFINE VARIABLE debt0        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt1        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt2        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt3        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-debt     AS DECIMAL FORMAT "->>>,>>>,>>9". 
DEFINE VARIABLE ar-saldo     AS DECIMAL.
DEFINE VARIABLE fcurr        AS INTEGER.
DEFINE VARIABLE curr-fcurr   AS CHAR .
DEFINE VARIABLE balance     AS DECIMAL FORMAT "->>,>>>,>>>,>>9".

DEFINE BUFFER debt FOR debitor. 

  FOR EACH ledger: 
    DELETE ledger. 
  END. 
  FOR EACH age-list: 
    DELETE age-list. 
  END. 
  FOR EACH output-list: 
    DELETE output-list. 
  END. 

  FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
    AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
    AND artikel.departement = 0
    NO-LOCK BY (STRING(artikel.artart) + STRING(artikel.artnr,"9999")): 
    CREATE ledger. 
    ledger.artnr = artikel.artnr. 
    ledger.bezeich = STRING(artikel.artnr) + "  -  " + artikel.bezeich. 
  END. 
 
/**** unpaid / partial paid A/R records *****/ 
  curr-art = 0. 
  FOR EACH debitor WHERE debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.rgdatum LE to-date AND debitor.opart EQ 0 NO-LOCK 
    USE-INDEX artdat_ix BY debitor.artnr: 
    IF debitor.name GE from-name AND debitor.name LE to-name THEN 
    DO: 
      IF curr-art NE debitor.artnr THEN 
      DO: 
        curr-art = debitor.artnr. 
        FIND FIRST artikel WHERE artikel.artnr = curr-art 
          AND artikel.departement = 0  NO-LOCK NO-ERROR. 
      END. 
 
      IF disptype = 0 THEN
        ar-saldo = debitor.saldo. 
      ELSE 
          ASSIGN 
              ar-saldo = debitor.vesrdep.
      IF debitor.counter NE 0 THEN 
      DO: 
        IF disptype = 0 THEN
        FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
          AND debt.counter = debitor.counter AND debt.opart = 1 
          AND debt.zahlkonto NE 0 
          AND debt.rgdatum LE to-date NO-LOCK USE-INDEX deb-rechnr_ix: 
            ar-saldo = ar-saldo + debt.saldo. 
        END. 
        ELSE
        FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
          AND debt.counter = debitor.counter AND debt.opart = 1 
          AND debt.zahlkonto NE 0 AND debt.betrieb-gastmem = debitor.betrieb-gastmem
          AND debt.rgdatum LE to-date NO-LOCK USE-INDEX deb-rechnr_ix: 
          ar-saldo = ar-saldo + debt.vesrdep.
        END. 
      END. 
      FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
      CREATE age-list. 
      age-list.artnr = debitor.artnr. 
      age-list.rechnr = debitor.rechnr. 
      age-list.rgdatum = debitor.rgdatum. 
      age-list.counter = debitor.counter. 
      age-list.gastnr = debitor.gastnr. 
      age-list.creditlimit = guest.kreditlimit. 
      age-list.tot-debt = ar-saldo. 
      IF betrieb-gastmem = 0 THEN
          age-list.fcurr = default-fcurr.
      ELSE
      DO:
          FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem NO-LOCK NO-ERROR.
          IF AVAILABLE waehrung THEN
              age-list.fcurr = waehrung.wabkurz.
      END.
      IF artikel.artart = 2 THEN 
      DO: 
        age-list.gastname = guest.name + ", " 
         + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
           age-list.creditlimit = guest.kreditlimit. 
      END. 
      ELSE 
      DO: 
        age-list.creditlimit = 0. 
        FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
        IF debitor.gastnr = htparam.finteger THEN 
          age-list.gastname = "F&B " + artikel.bezeich. 
        ELSE age-list.gastname = "F/O " + artikel.bezeich. 
      END. 
 
      IF to-date - age-list.rgdatum GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day1 
        THEN age-list.debt1 = age-list.debt1 + ar-saldo. 
      ELSE age-list.debt0 = age-list.debt0 + ar-saldo. 
    END. 
  END. 
  
  /**** Full paid A/R records *****/ 
  curr-art = 0. 
  FOR EACH debitor WHERE debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.rgdatum LE to-date AND debitor.opart EQ 2 
    AND debitor.zahlkonto = 0 NO-LOCK USE-INDEX artdat_ix BY debitor.artnr: 
    FIND FIRST debt WHERE debt.rechnr = debitor.rechnr 
      AND debt.counter = debitor.counter AND debt.opart = 2 
      AND debt.zahlkonto NE 0 AND debt.rgdatum GT to-date 
      NO-LOCK USE-INDEX deb-rechnr_ix NO-ERROR. 
    IF AVAILABLE debt AND debitor.name GE from-name AND debitor.name LE to-name 
    THEN DO: 
      IF curr-art NE debitor.artnr THEN 
      DO: 
        curr-art = debitor.artnr. 
        FIND FIRST artikel WHERE artikel.artnr = curr-art 
          AND artikel.departement = 0  NO-LOCK NO-ERROR. 
      END. 
 
      IF disptype = 0 THEN
        ar-saldo = debitor.saldo. 
      ELSE 
          ASSIGN 
              ar-saldo = debitor.vesrdep.
      IF disptype = 0 THEN
      FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
        AND debt.counter = debitor.counter AND debt.opart = 2 
        AND debt.zahlkonto NE 0 AND debt.rgdatum LE to-date 
        NO-LOCK USE-INDEX deb-rechnr_ix: 
        ar-saldo = ar-saldo + debt.saldo. 
      END. 
      ELSE
      FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
        AND debt.counter = debitor.counter AND debt.opart = 2 
        AND debt.zahlkonto NE 0 AND debt.rgdatum LE to-date 
        AND debt.betrieb-gastmem = debitor.betrieb-gastmem 
        NO-LOCK USE-INDEX deb-rechnr_ix: 
        ar-saldo = ar-saldo + debt.vesrdep. 
      END. 
      
      FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
      CREATE age-list. 
      age-list.artnr = debitor.artnr. 
      age-list.rechnr = debitor.rechnr.
      age-list.rgdatum = debitor.rgdatum. 
      age-list.counter = debitor.counter. 
      age-list.gastnr = debitor.gastnr. 
      age-list.creditlimit = guest.kreditlimit. 
      age-list.tot-debt = ar-saldo. 
      
      IF debitor.betrieb-gastmem = 0 THEN
          age-list.fcurr = default-fcurr.
      ELSE
      DO:
          FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
              NO-LOCK NO-ERROR.
          IF AVAILABLE waehrung THEN
              age-list.fcurr = waehrung.wabkurz.
      END.
      IF artikel.artart = 2 THEN 
      DO: 
        age-list.gastname = guest.name + ", " 
         + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
           age-list.creditlimit = guest.kreditlimit. 
      END. 
      ELSE 
      DO: 
        age-list.creditlimit = 0. 
        FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
        IF debitor.gastnr = htparam.finteger THEN 
          age-list.gastname = "F&B " + artikel.bezeich. 
        ELSE age-list.gastname = "F/O " + artikel.bezeich. 
      END. 
 
      IF to-date - age-list.rgdatum GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day1 
        THEN age-list.debt1 = age-list.debt1 + ar-saldo. 
      ELSE age-list.debt0 = age-list.debt0 + ar-saldo. 
    END. 
  END. 
  
  FOR EACH ledger BY ledger.artnr: 
    FIND FIRST artikel WHERE artikel.artnr = ledger.artnr
        AND artikel.departement = 0 NO-LOCK.
    outlist = "    " + CAPS(ledger.bezeich). 
    RUN fill-in-list(0, ""). 
    outlist = "". 
    RUN fill-in-list(0, ""). 
    ct = 0. 
    curr-gastnr = 0. 
    creditlimit = 0. 
    curr-fcurr = "".
    FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
      AND age-list.tot-debt NE 0 BY age-list.gastname: 
      ledger.tot-debt = ledger.tot-debt + age-list.tot-debt. 
      ledger.debt0 = ledger.debt0 + age-list.debt0. 
      ledger.debt1 = ledger.debt1 + age-list.debt1. 
      ledger.debt2 = ledger.debt2 + age-list.debt2. 
      ledger.debt3 = ledger.debt3 + age-list.debt3. 
      t-saldo  = t-saldo + age-list.tot-debt. 
      t-debt0  = t-debt0 + age-list.debt0. 
      t-debt1  = t-debt1 + age-list.debt1. 
      t-debt2  = t-debt2 + age-list.debt2. 
      t-debt3  = t-debt3 + age-list.debt3. 
      IF curr-gastnr = 0 THEN 
      DO: 
        gastname = age-list.gastname. 
        creditlimit = age-list.creditlimit. 
        tot-debt = age-list.tot-debt. 
        debt0 = age-list.debt0. 
        debt1 = age-list.debt1. 
        debt2 = age-list.debt2. 
        debt3 = age-list.debt3. 
        ct = ct + 1. 
      END. 
      ELSE IF curr-name NE age-list.gastname THEN 
      DO: 
        IF price-decimal = 0 THEN 
        DO: 
          IF NOT long-digit THEN 
          outlist = "  " + STRING(ct,">>>9") + "  " 
             + STRING(gastname, "x(34)") + "  " 
             + STRING(tot-debt, "->>>,>>>,>>9.99") +  "  " 
             + STRING(debt0, "->>>,>>>,>>9.99") + "  " 
             + STRING(debt1, "->>>,>>>,>>9.99") + "  " 
             + STRING(debt2, "->>>,>>>,>>9.99") + "  " 
             + STRING(debt3, "->>>,>>>,>>9.99") + "  "
             . 
          ELSE outlist = "  " + STRING(ct,">>>9") + "  " 
             + STRING(gastname, "x(34)") + "  " 
             + STRING(tot-debt, "->>>>,>>>,>>>,>>9") 
             + STRING(debt0, "->>>>,>>>,>>>,>>9") 
             + STRING(debt1, "->>>>,>>>,>>>,>>9") 
             + STRING(debt2, "->>>>,>>>,>>>,>>9") 
             + STRING(debt3, "->>>>,>>>,>>>,>>9")
             . 
        END. 
        ELSE outlist = "  " + STRING(ct,">>>9") + "  " 
           + STRING(gastname, "x(34)") + "  " 
           + STRING(tot-debt, "->>>,>>>,>>9.99") +  "  " 
           + STRING(debt0, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt1, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt2, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt3, "->>>,>>>,>>9.99") + "  "
           .

        IF artikel.artart = 2 THEN RUN fill-in-list(age-list.gastnr, age-list.fcurr). 
        ELSE RUN fill-in-list(0, "").

        ASSIGN
          output-list.creditlimit   = creditlimit
          creditlimit               = age-list.creditlimit 
          gastname                  = age-list.gastname
          tot-debt                  = age-list.tot-debt 
          debt0                     = age-list.debt0
          debt1                     = age-list.debt1 
          debt2                     = age-list.debt2 
          debt3                     = age-list.debt3 
          ct                        = ct + 1
        . 
      END. 
      ELSE 
      ASSIGN  
        tot-debt = tot-debt + age-list.tot-debt 
        debt0    = debt0 + age-list.debt0
        debt1    = debt1 + age-list.debt1 
        debt2    = debt2 + age-list.debt2 
        debt3    = debt3 + age-list.debt3
      . 
      curr-gastnr = age-list.gastnr. 
      curr-name = age-list.gastname. 
      curr-fcurr = age-list.fcurr.
      DELETE age-list. 
    END.

    IF ct GT 0 THEN 
    DO: 
      IF price-decimal = 0 THEN 
      DO: 
         IF NOT long-digit THEN 
         outlist = "  " + STRING(ct,">>>9") + "  " 
           + STRING(gastname, "x(34)") + "  " 
           + STRING(tot-debt, "->>>,>>>,>>9.99") +  "  " 
           + STRING(debt0, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt1, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt2, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt3, "->>>,>>>,>>9.99") + "  ". 
         ELSE outlist = "  " + STRING(ct,">>>9") + "  " 
           + STRING(gastname, "x(34)") + "  " 
           + STRING(tot-debt, "->>>>,>>>,>>>,>>9") 
           + STRING(debt0, "->>>>,>>>,>>>,>>9") 
           + STRING(debt1, "->>>>,>>>,>>>,>>9") 
           + STRING(debt2, "->>>>,>>>,>>>,>>9") 
           + STRING(debt3, "->>>>,>>>,>>>,>>9"). 
      END. 
      ELSE outlist = "  " + STRING(ct,">>>9") + "  " 
           + STRING(gastname, "x(34)") + "  " 
           + STRING(tot-debt, "->>>,>>>,>>9.99") +  "  " 
           + STRING(debt0, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt1, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt2, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt3, "->>>,>>>,>>9.99") + "  ". 

      IF artikel.artart = 2 THEN RUN fill-in-list(curr-gastnr, curr-fcurr). 
      ELSE RUN fill-in-list(0, "").

      output-list.creditlimit = creditlimit. 
    END. 
 
    tmp-saldo = ledger.tot-debt. 
    IF tmp-saldo = 0 THEN tmp-saldo = 1. 
    outlist = FILL("-",170). 
    RUN fill-in-list(0, "----"). 
    IF price-decimal = 0 THEN 
    DO: 
      IF NOT long-digit THEN 
      outlist = "                             T o t a l      " 
        + STRING(ledger.tot-debt, "->>>,>>>,>>9.99") +  "  " 
        + STRING(ledger.debt0, "->>>,>>>,>>9.99") + "  " 
        + STRING(ledger.debt1, "->>>,>>>,>>9.99") + "  " 
        + STRING(ledger.debt2, "->>>,>>>,>>9.99") + "  " 
        + STRING(ledger.debt3, "->>>,>>>,>>9.99"). 
      ELSE outlist = "                             T o t a l      " 
        + STRING(ledger.tot-debt, "->>>>,>>>,>>>,>>9") 
        + STRING(ledger.debt0, "->>>>,>>>,>>>,>>9") 
        + STRING(ledger.debt1, "->>>>,>>>,>>>,>>9") 
        + STRING(ledger.debt2, "->>>>,>>>,>>>,>>9") 
        + STRING(ledger.debt3, "->>>>,>>>,>>>,>>9"). 
    END. 
    ELSE outlist = "                             T o t a l      " 
      + STRING(ledger.tot-debt, "->>>,>>>,>>9.99") +  "  " 
      + STRING(ledger.debt0, "->>>,>>>,>>9.99") + "  " 
      + STRING(ledger.debt1, "->>>,>>>,>>9.99") + "  " 
      + STRING(ledger.debt2, "->>>,>>>,>>9.99") + "  " 
      + STRING(ledger.debt3, "->>>,>>>,>>9.99"). 
    RUN fill-in-list(0, ""). 
    IF NOT long-digit THEN 
    outlist = STRING (translateExtended ("        Statistic Percentage (%):",lvCAREA,""), "x(34)") 
      + "               " 
      + STRING((ledger.tot-debt / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt0 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt1 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt2 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt3 / tmp-saldo * 100), "->>,>>9.99"). 
    ELSE outlist = STRING (translateExtended ("        Statistic Percentage (%):",lvCAREA,""), "x(34)") 
      + "                 " 
      + STRING((ledger.tot-debt / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt0 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt1 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt2 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt3 / tmp-saldo * 100), "->>,>>9.99"). 
    RUN fill-in-list(0, ""). 
    outlist = "". 
    RUN fill-in-list(0, ""). 
  END. 
 
  outlist = 
  "-----------------------------------------------------------------------------------------------------------------------------------------------------------". 
  RUN fill-in-list(0, "----"). 
  IF price-decimal = 0 THEN 
  DO: 
    IF NOT long-digit THEN 
    outlist = STRING (translateExtended ("           T O T A L  A/R:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->>>,>>>,>>9.99") + "  " 
      + STRING(t-debt0, "->>>,>>>,>>9.99") + "  " 
      + STRING(t-debt1, "->>>,>>>,>>9.99") + "  " 
      + STRING(t-debt2, "->>>,>>>,>>9.99") + "  " 
      + STRING(t-debt3, "->>>,>>>,>>9.99"). 
    ELSE outlist = STRING (translateExtended ("           T O T A L  A/R:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->>>>,>>>,>>>,>>9") 
      + STRING(t-debt0, "->>>>,>>>,>>>,>>9") 
      + STRING(t-debt1, "->>>>,>>>,>>>,>>9") 
      + STRING(t-debt2, "->>>>,>>>,>>>,>>9") 
      + STRING(t-debt3, "->>>>,>>>,>>>,>>9"). 
  END. 
  ELSE outlist = STRING (translateExtended ("           T O T A L  A/R:",lvCAREA,""), "x(26)") 
    + "                  " 
    + STRING(t-saldo, "->>>,>>>,>>9.99") + "  " 
    + STRING(t-debt0, "->>>,>>>,>>9.99") + "  " 
    + STRING(t-debt1, "->>>,>>>,>>9.99") + "  " 
    + STRING(t-debt2, "->>>,>>>,>>9.99") + "  " 
    + STRING(t-debt3, "->>>,>>>,>>9.99"). 
  RUN fill-in-list(0, ""). 
  outlist = "". 
  RUN fill-in-list(0, ""). 
  IF NOT long-digit THEN 
  outlist = STRING (translateExtended ("        Statistic Percentage (%):",lvCAREA,""), "x(34)") 
    + "                " 
    + "100.00" 
    + "       " 
    + STRING((t-debt0 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt1 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt2 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt3 / t-saldo * 100), "->>,>>9.99"). 
  ELSE outlist = STRING (translateExtended ("        Statistic Percentage (%):",lvCAREA,""), "x(34)") 
    + "                  " 
    + "100.00" 
    + "       " 
    + STRING((t-debt0 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt1 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt2 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt3 / t-saldo * 100), "->>,>>9.99"). 
  RUN fill-in-list(0, ""). 
  outlist = "". 
  RUN fill-in-list(0, ""). 
END.

PROCEDURE age-listA: 
DEFINE VARIABLE curr-art AS INTEGER. 
DEFINE VARIABLE billdate AS DATE. 
DEFINE VARIABLE ct AS INTEGER FORMAT ">>>9". 
DEFINE VARIABLE t-debet      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-credit     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-comm       AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-adjust     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-saldo      AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt0      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt1      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt2      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt3      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE tmp-saldo    AS DECIMAL FORMAT "->>>>>>>>>>9" INITIAL 0. 
DEFINE VARIABLE curr-name    AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE curr-gastnr  AS INTEGER. 
DEFINE VARIABLE creditlimit  AS DECIMAL. 
DEFINE VARIABLE gastname     AS CHARACTER FORMAT "x(34)". 
DEFINE VARIABLE debt0        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt1        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt2        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt3        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-debt     AS DECIMAL FORMAT "->>>,>>>,>>9". 
DEFINE VARIABLE fcurr        AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-fcurr   AS CHAR NO-UNDO.
DEFINE VARIABLE balance     AS DECIMAL FORMAT "->>,>>>,>>>,>>9".
 
DEFINE BUFFER debt FOR debitor. 
DEFINE VARIABLE ar-saldo AS DECIMAL. 

  FOR EACH ledger: 
    DELETE ledger. 
  END. 
  FOR EACH age-list: 
    DELETE age-list. 
  END. 
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
 
  FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
      AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
      AND artikel.departement = 0
      NO-LOCK BY (STRING(artikel.artart) + STRING(artikel.artnr,"9999")): 
    CREATE ledger. 
    ledger.artnr = artikel.artnr. 
    ledger.bezeich = STRING(artikel.artnr) + "  -  " + artikel.bezeich. 
  END. 
 
/**** unpaid / partial paid A/R records *****/ 
  curr-art = 0. 
  FOR EACH debitor WHERE debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.rgdatum LE to-date AND debitor.opart EQ 0 NO-LOCK 
    USE-INDEX artdat_ix BY debitor.artnr: 
    IF debitor.name GE from-name THEN 
    DO: 
      IF curr-art NE debitor.artnr THEN 
      DO: 
        curr-art = debitor.artnr. 
        FIND FIRST artikel WHERE artikel.artnr = curr-art 
          AND artikel.departement = 0  NO-LOCK NO-ERROR. 
      END. 
 
      IF disptype = 1 THEN
          ASSIGN
          ar-saldo = debitor.vesrdep.
      ELSE ar-saldo = debitor.saldo. 
      IF debitor.counter NE 0 THEN 
      DO: 
        IF disptype = 0 THEN
        FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
          AND debt.counter = debitor.counter AND debt.opart = 1 
          AND debt.zahlkonto NE 0 
          AND debt.rgdatum LE to-date NO-LOCK USE-INDEX deb-rechnr_ix: 
            IF disptype = 0 THEN
                ar-saldo = ar-saldo + debt.saldo. 
            ELSE ar-saldo = ar-saldo  + debt.vesrdep.
        END. 
        ELSE
        FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
          AND debt.counter = debitor.counter AND debt.opart = 1 
          AND debt.zahlkonto NE 0 AND debt.betrieb-gastmem = debitor.betrieb-gastmem
          AND debt.rgdatum LE to-date NO-LOCK USE-INDEX deb-rechnr_ix: 
            ar-saldo = ar-saldo  + debt.vesrdep.
        END. 
      END. 
      FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
      CREATE age-list. 
      age-list.artnr = debitor.artnr. 
      age-list.rechnr = debitor.rechnr. 
      age-list.rgdatum = debitor.rgdatum. 
      age-list.counter = debitor.counter. 
      age-list.gastnr = debitor.gastnr. 
      age-list.creditlimit = guest.kreditlimit. 
      age-list.tot-debt = ar-saldo. 
      IF debitor.betrieb-gastmem = 0 THEN
          age-list.fcurr = default-fcurr.
      ELSE
      DO:
          FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem NO-LOCK NO-ERROR.
          IF AVAILABLE waehrung THEN
              age-list.fcurr = waehrung.wabkurz.
      END.
      IF artikel.artart = 2 THEN 
      DO: 
        age-list.gastname = guest.name + ", " 
         + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
           age-list.creditlimit = guest.kreditlimit. 
      END. 
      ELSE 
      DO: 
        age-list.creditlimit = 0. 
        FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
        IF debitor.gastnr = htparam.finteger THEN 
          age-list.gastname = "F&B " + artikel.bezeich. 
        ELSE age-list.gastname = "F/O " + artikel.bezeich. 
      END. 
 
      IF to-date - age-list.rgdatum GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day1 
        THEN age-list.debt1 = age-list.debt1 + ar-saldo. 
      ELSE age-list.debt0 = age-list.debt0 + ar-saldo. 
    END. 
  END. 
 
/**** Full paid A/R records *****/ 
  curr-art = 0. 
  FOR EACH debitor WHERE debitor.artnr GE from-art AND debitor.artnr LE to-art 
    AND debitor.rgdatum LE to-date AND debitor.opart EQ 2 
    AND debitor.zahlkonto = 0 NO-LOCK USE-INDEX artdat_ix BY debitor.artnr: 
    FIND FIRST debt WHERE debt.rechnr = debitor.rechnr 
      AND debt.counter = debitor.counter AND debt.opart = 2 
      AND debt.zahlkonto NE 0 AND debt.rgdatum GT to-date 
      NO-LOCK USE-INDEX deb-rechnr_ix NO-ERROR. 
    IF AVAILABLE debt AND debitor.name GE from-name THEN
    DO: 
      IF curr-art NE debitor.artnr THEN 
      DO: 
        curr-art = debitor.artnr. 
        FIND FIRST artikel WHERE artikel.artnr = curr-art 
          AND artikel.departement = 0  NO-LOCK NO-ERROR. 
      END. 
      IF disptype = 0 THEN
        ar-saldo = debitor.saldo. 
      ELSE ASSIGN ar-saldo = debitor.vesrdep.
      IF disptype = 0 THEN
      FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
        AND debt.counter = debitor.counter AND debt.opart = 2 
        AND debt.zahlkonto NE 0 AND debt.rgdatum LE to-date 
        NO-LOCK USE-INDEX deb-rechnr_ix: 
            ar-saldo = ar-saldo + debt.saldo. 
      END. 
      ELSE
      FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
        AND debt.counter = debitor.counter AND debt.opart = 2 
        AND debt.zahlkonto NE 0 AND debt.rgdatum LE to-date 
        AND debt.betrieb-gastmem = debitor.betrieb-gastmem 
          NO-LOCK USE-INDEX deb-rechnr_ix: 
        ar-saldo = ar-saldo + debt.vesrdep.
      END. 
      FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
      CREATE age-list. 
      age-list.artnr = debitor.artnr. 
      age-list.rechnr = debitor.rechnr. 
      age-list.rgdatum = debitor.rgdatum. 
      age-list.counter = debitor.counter. 
      age-list.gastnr = debitor.gastnr. 
      age-list.creditlimit = guest.kreditlimit. 
      age-list.tot-debt = ar-saldo. 
      IF debitor.betrieb-gastmem = 0 THEN
          age-list.fcurr = default-fcurr.
      ELSE
      DO:
          FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
              NO-LOCK NO-ERROR.
          IF AVAILABLE waehrung THEN
              age-list.fcurr = waehrung.wabkurz.
      END.
      IF artikel.artart = 2 THEN 
      DO: 
        age-list.gastname = guest.name + ", " 
         + guest.vorname1 + guest.anredefirma + " " + guest.anrede1. 
           age-list.creditlimit = guest.kreditlimit. 
      END. 
      ELSE 
      DO: 
        age-list.creditlimit = 0. 
        FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
        IF debitor.gastnr = htparam.finteger THEN 
          age-list.gastname = "F&B " + artikel.bezeich. 
        ELSE age-list.gastname = "F/O " + artikel.bezeich. 
      END. 
 
      IF to-date - age-list.rgdatum GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF to-date - age-list.rgdatum GT day1 
        THEN age-list.debt1 = age-list.debt1 + ar-saldo. 
      ELSE age-list.debt0 = age-list.debt0 + ar-saldo. 
    END. 
  END. 
 
  
  FOR EACH ledger BY ledger.artnr: 
    outlist = "   " + CAPS(ledger.bezeich). 
    RUN fill-in-list(0, ""). 
    outlist = "". 
    RUN fill-in-list(0, ""). 
    ct = 0. 
    curr-gastnr = 0. 
    creditlimit = 0. 
    FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
      AND age-list.tot-debt NE 0 BY age-list.gastname: 
      ledger.tot-debt = ledger.tot-debt + age-list.tot-debt. 
      ledger.debt0 = ledger.debt0 + age-list.debt0. 
      ledger.debt1 = ledger.debt1 + age-list.debt1. 
      ledger.debt2 = ledger.debt2 + age-list.debt2. 
      ledger.debt3 = ledger.debt3 + age-list.debt3. 
      t-saldo  = t-saldo + age-list.tot-debt. 
      t-debt0  = t-debt0 + age-list.debt0. 
      t-debt1  = t-debt1 + age-list.debt1. 
      t-debt2  = t-debt2 + age-list.debt2. 
      t-debt3  = t-debt3 + age-list.debt3. 
      IF curr-gastnr = 0 THEN 
      DO: 
        gastname = age-list.gastname. 
        creditlimit = age-list.creditlimit. 
        tot-debt = age-list.tot-debt. 
        debt0 = age-list.debt0. 
        debt1 = age-list.debt1. 
        debt2 = age-list.debt2. 
        debt3 = age-list.debt3. 
        ct = ct + 1. 
      END. 
      ELSE IF curr-name NE age-list.gastname THEN 
      DO: 
        IF price-decimal = 0 THEN 
        DO: 
          IF NOT long-digit THEN 
          outlist = "  " + STRING(ct,">>>9") + "  " 
             + STRING(gastname, "x(34)") + "  " 
             + STRING(tot-debt, "->>>,>>>,>>9.99") +  "  " 
             + STRING(debt0, "->>>,>>>,>>9.99") + "  " 
             + STRING(debt1, "->>>,>>>,>>9.99") + "  " 
             + STRING(debt2, "->>>,>>>,>>9.99") + "  " 
             + STRING(debt3, "->>>,>>>,>>9.99") + "  "
             .
          ELSE outlist = "  " + STRING(ct,">>>9") + "  " 
             + STRING(gastname, "x(34)") + "  " 
             + STRING(tot-debt, "->>>>,>>>,>>>,>>9") 
             + STRING(debt0, "->>>>,>>>,>>>,>>9") 
             + STRING(debt1, "->>>>,>>>,>>>,>>9") 
             + STRING(debt2, "->>>>,>>>,>>>,>>9") 
             + STRING(debt3, "->>>>,>>>,>>>,>>9")
             .
        END. 
        ELSE outlist = "  " + STRING(ct,">>>9") + "  " 
           + STRING(gastname, "x(34)") + "  " 
           + STRING(tot-debt, "->>>,>>>,>>9.99") +  "  " 
           + STRING(debt0, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt1, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt2, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt3, "->>>,>>>,>>9.99") + "  "
           .
        RUN fill-in-list(age-list.gastnr, age-list.fcurr). 
        output-list.creditlimit = creditlimit.
        /*naufal*/
        IF output-list.creditlimit NE 0 THEN
            balance = output-list.creditlimit - tot-debt.
        ELSE 
            balance = 0.
        DISP
            output-list.creditlimit
            tot-debt
            balance.
        MESSAGE "1"
            VIEW-AS ALERT-BOX INFO BUTTONS OK.
        /*end naufal*/
        creditlimit = age-list.creditlimit. 
        gastname = age-list.gastname. 
        tot-debt = age-list.tot-debt. 
        debt0 = age-list.debt0. 
        debt1 = age-list.debt1. 
        debt2 = age-list.debt2. 
        debt3 = age-list.debt3. 
        ct = ct + 1. 
      END. 
      ELSE 
      DO: 
        tot-debt = tot-debt + age-list.tot-debt. 
        debt0 = debt0 + age-list.debt0. 
        debt1 = debt1 + age-list.debt1. 
        debt2 = debt2 + age-list.debt2. 
        debt3 = debt3 + age-list.debt3. 
      END. 
      curr-gastnr = age-list.gastnr. 
      curr-name = age-list.gastname. 
      curr-fcurr = age-list.fcurr.
      DELETE age-list. 
    END. 
    IF ct GT 0 THEN 
    DO: 
      IF price-decimal = 0 THEN 
      DO: 
         IF NOT long-digit THEN 
         outlist = "  " + STRING(ct,">>>9") + "  " 
           + STRING(gastname, "x(34)") + "  " 
           + STRING(tot-debt, "->>>,>>>,>>9.99") +  "  " 
           + STRING(debt0, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt1, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt2, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt3, "->>>,>>>,>>9.99") + "  ". 
         ELSE outlist = "  " + STRING(ct,">>>9") + "  " 
           + STRING(gastname, "x(34)") + "  " 
           + STRING(tot-debt, "->>>>,>>>,>>>,>>9") 
           + STRING(debt0, "->>>>,>>>,>>>,>>9") 
           + STRING(debt1, "->>>>,>>>,>>>,>>9") 
           + STRING(debt2, "->>>>,>>>,>>>,>>9") 
           + STRING(debt3, "->>>>,>>>,>>>,>>9"). 
      END. 
      ELSE outlist = "  " + STRING(ct,">>>9") + "  " 
           + STRING(gastname, "x(34)") + "  " 
           + STRING(tot-debt, "->>>,>>>,>>9.99") +  "  " 
           + STRING(debt0, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt1, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt2, "->>>,>>>,>>9.99") + "  " 
           + STRING(debt3, "->>>,>>>,>>9.99") + "  ". 
      RUN fill-in-list(curr-gastnr, curr-fcurr). 
      output-list.creditlimit = creditlimit.
      /*naufal*/
        IF output-list.creditlimit NE 0 THEN
            balance = output-list.creditlimit - tot-debt.
        ELSE 
            balance = 0.
        DISP
            output-list.creditlimit
            tot-debt
            balance.
        MESSAGE "2"
            VIEW-AS ALERT-BOX INFO BUTTONS OK.
        /*end naufal*/
    END. 
 
    tmp-saldo = ledger.tot-debt. 
    IF tmp-saldo = 0 THEN tmp-saldo = 1. 
    outlist = 
    "-----------------------------------------------------------------------------------------------------------------------------------------------------------". 
    RUN fill-in-list(0, "----"). 
    IF price-decimal = 0 THEN 
    DO: 
      IF NOT long-digit THEN 
      outlist = "                             T o t a l      " 
        + STRING(ledger.tot-debt, "->>>,>>>,>>9.99") +  "  " 
        + STRING(ledger.debt0, "->>>,>>>,>>9.99") + "  " 
        + STRING(ledger.debt1, "->>>,>>>,>>9.99") + "  " 
        + STRING(ledger.debt2, "->>>,>>>,>>9.99") + "  " 
        + STRING(ledger.debt3, "->>>,>>>,>>9.99"). 
      ELSE outlist = "                             T o t a l      " 
        + STRING(ledger.tot-debt, "->>>>,>>>,>>>,>>9") 
        + STRING(ledger.debt0, "->>>>,>>>,>>>,>>9") 
        + STRING(ledger.debt1, "->>>>,>>>,>>>,>>9") 
        + STRING(ledger.debt2, "->>>>,>>>,>>>,>>9") 
        + STRING(ledger.debt3, "->>>>,>>>,>>>,>>9"). 
    END. 
    ELSE outlist = "                             T o t a l      " 
      + STRING(ledger.tot-debt, "->>>,>>>,>>9.99") +  "  " 
      + STRING(ledger.debt0, "->>>,>>>,>>9.99") + "  " 
      + STRING(ledger.debt1, "->>>,>>>,>>9.99") + "  " 
      + STRING(ledger.debt2, "->>>,>>>,>>9.99") + "  " 
      + STRING(ledger.debt3, "->>>,>>>,>>9.99"). 
    RUN fill-in-list(0, ""). 
    IF NOT long-digit THEN 
    outlist = STRING (translateExtended ("        Statistic Percentage (%):",lvCAREA,""), "x(34)") 
      + "               " 
      + STRING((ledger.tot-debt / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt0 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt1 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt2 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt3 / tmp-saldo * 100), "->>,>>9.99"). 
    ELSE outlist = STRING (translateExtended ("        Statistic Percentage (%):",lvCAREA,""), "x(34)") 
      + "                 " 
      + STRING((ledger.tot-debt / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt0 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt1 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt2 / tmp-saldo * 100), "->>,>>9.99") 
      + "       " 
      + STRING((ledger.debt3 / tmp-saldo * 100), "->>,>>9.99"). 
    RUN fill-in-list(0, ""). 
    outlist = "". 
    RUN fill-in-list(0, ""). 
  END. 
 
  outlist = 
  "-----------------------------------------------------------------------------------------------------------------------------------------------------------". 
  RUN fill-in-list(0, "----"). 
  IF price-decimal = 0 THEN 
  DO: 
    IF NOT long-digit THEN 
    outlist = STRING (translateExtended ("           T O T A L  A/R:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->>>,>>>,>>9.99") + "  " 
      + STRING(t-debt0, "->>>,>>>,>>9.99") + "  " 
      + STRING(t-debt1, "->>>,>>>,>>9.99") + "  " 
      + STRING(t-debt2, "->>>,>>>,>>9.99") + "  " 
      + STRING(t-debt3, "->>>,>>>,>>9.99"). 
    ELSE outlist = STRING (translateExtended ("           T O T A L  A/R:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->>>>,>>>,>>>,>>9") 
      + STRING(t-debt0, "->>>>,>>>,>>>,>>9") 
      + STRING(t-debt1, "->>>>,>>>,>>>,>>9") 
      + STRING(t-debt2, "->>>>,>>>,>>>,>>9") 
      + STRING(t-debt3, "->>>>,>>>,>>>,>>9"). 
  END. 
  ELSE outlist = STRING (translateExtended ("           T O T A L  A/R:",lvCAREA,""), "x(26)") 
    + "                  " 
    + STRING(t-saldo, "->>>,>>>,>>9.99") + "  " 
    + STRING(t-debt0, "->>>,>>>,>>9.99") + "  " 
    + STRING(t-debt1, "->>>,>>>,>>9.99") + "  " 
    + STRING(t-debt2, "->>>,>>>,>>9.99") + "  " 
    + STRING(t-debt3, "->>>,>>>,>>9.99"). 
  RUN fill-in-list(0, ""). 
  outlist = "". 
  RUN fill-in-list(0, ""). 
  IF NOT long-digit THEN 
  outlist = STRING (translateExtended ("        Statistic Percentage (%):",lvCAREA,""), "x(34)") 
    + "                   " 
    + "100.00" 
    + "       " 
    + STRING((t-debt0 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt1 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt2 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt3 / t-saldo * 100), "->>,>>9.99"). 
  ELSE outlist = STRING (translateExtended ("        Statistic Percentage (%):",lvCAREA,""), "x(34)") 
    + "                  " 
    + "100.00" 
    + "       " 
    + STRING((t-debt0 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt1 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt2 / t-saldo * 100), "->>,>>9.99") 
    + "       " 
    + STRING((t-debt3 / t-saldo * 100), "->>,>>9.99"). 
  RUN fill-in-list(0, ""). 
  outlist = "". 
  RUN fill-in-list(0, ""). 
END. 



PROCEDURE fill-in-list:
DEF INPUT PARAMETER inp-gastnr AS INTEGER NO-UNDO.
DEF INPUT PARAMETER currency AS CHAR NO-UNDO.


  CREATE output-list. 
  output-list.str = outlist. 
  ASSIGN output-list.gastnr = inp-gastnr.

  IF NOT long-digit THEN 
  DO: 
    output-list.age1 = SUBSTRING(STR,60, 17). 
    output-list.age2 = SUBSTRING(STR,77, 17). 
    output-list.age3 = SUBSTRING(STR,94, 17). 
    output-list.age4 = SUBSTRING(STR,111, 17). 
    output-list.curr = currency.
  END. 
  ELSE 
  DO: 
    output-list.age1 = SUBSTRING(STR,62, 17). 
    output-list.age2 = SUBSTRING(STR,79, 17). 
    output-list.age3 = SUBSTRING(STR,96, 17). 
    output-list.age4 = SUBSTRING(STR,113, 17). 
    output-list.curr = currency.
  END. 
END. 


