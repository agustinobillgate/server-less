DEFINE WORKFILE ledger 
    FIELD artnr         AS INTEGER 
    FIELD bezeich       AS CHARACTER FORMAT "x(24)" INITIAL "?????" 
    FIELD debt0         AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt1         AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt2         AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt3         AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD tot-debt      AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0. 

DEFINE WORKFILE age-list 
    FIELD artnr         AS INTEGER 
    FIELD rechnr        AS INTEGER 
    FIELD counter       AS INTEGER 
    FIELD gastnr        AS INTEGER 
    FIELD creditlimit   AS DECIMAL 
    FIELD rgdatum       AS DATE 
    FIELD gastname      AS CHARACTER FORMAT "x(34)" 
    FIELD saldo         AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0 
    FIELD debt0         AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0 
    FIELD debt1         AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0 
    FIELD debt2         AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0 
    FIELD debt3         AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0 
    FIELD tot-debt      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0
    FIELD fcurr         AS CHAR. 

DEFINE TEMP-TABLE arage-list
    FIELD curr              AS CHARACTER
    FIELD gastnr            AS INTEGER
    FIELD number-str        AS CHARACTER
    FIELD customer-name     AS CHARACTER
    FIELD outstanding       AS CHARACTER
    FIELD age1              AS CHARACTER
    FIELD age2              AS CHARACTER
    FIELD age3              AS CHARACTER
    FIELD age4              AS CHARACTER
    FIELD creditlimit       AS DECIMAL
    FIELD balance           AS DECIMAL
    FIELD creditlimit-str   AS CHARACTER
    FIELD balance-str       AS CHARACTER
    .

DEF INPUT PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER from-art AS INT.
DEF INPUT PARAMETER to-art AS INT.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER from-name AS CHAR.
DEF INPUT PARAMETER to-name AS CHAR.
DEF INPUT PARAMETER disptype AS INT.
DEF INPUT PARAMETER cvt-flag AS LOGICAL.
DEF INPUT PARAMETER dollar-rate AS DECIMAL.
DEF OUTPUT PARAMETER outlist AS CHAR FORMAT "x(200)".
DEF OUTPUT PARAMETER TABLE FOR arage-list.

/* Rd, #753, 27Mar25, date variable */
DEFINE VARIABLE tmpdays AS INTEGER NO-UNDO.

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
DEFINE VARIABLE curr-fcurr   AS CHAR.

DEFINE BUFFER debt FOR debitor. 

  FOR EACH ledger: 
    DELETE ledger. 
  END. 
  FOR EACH age-list: 
    DELETE age-list. 
  END. 
  FOR EACH arage-list: 
    DELETE arage-list. 
  END. 

  FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
    AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
    AND artikel.departement = 0
    /*AND artikel.activeflag         william add activeflag F8F550*/
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
      ELSE DO:
        IF NOT cvt-flag THEN ar-saldo = debitor.vesrdep.
        ELSE ar-saldo = debitor.saldo / dollar-rate. 
      END. 
              
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
          IF NOT cvt-flag THEN ar-saldo = ar-saldo + debitor.vesrdep.
          ELSE ar-saldo = ar-saldo + (debitor.saldo / dollar-rate).  
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
      
      /* Rd, #753, 27Mar25, date variable */
      tmpdays = to-date - age-list.rgdatum.
      IF tmpdays GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF tmpdays GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF tmpdays GT day1 
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
      ELSE DO:
          IF NOT cvt-flag THEN ar-saldo = debitor.vesrdep.
          ELSE ar-saldo = debitor.saldo / dollar-rate. 
      END.
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
        IF NOT cvt-flag THEN ar-saldo = ar-saldo + debt.vesrdep.
        ELSE ar-saldo = ar-saldo + (debt.saldo / dollar-rate). 
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
 
      /* Rd, #753, 27Mar25, date variable */
      tmpdays = to-date - age-list.rgdatum.
      IF tmpdays GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF tmpdays GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF tmpdays GT day1 
        THEN age-list.debt1 = age-list.debt1 + ar-saldo. 
      ELSE age-list.debt0 = age-list.debt0 + ar-saldo. 
    END. 
  END. 
  
  FOR EACH ledger BY ledger.artnr: 
    FIND FIRST artikel WHERE artikel.artnr = ledger.artnr
        AND artikel.departement = 0 NO-LOCK.

    FIND FIRST age-list WHERE age-list.artnr = ledger.artnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE age-list THEN NEXT. /*william add validation to not show ledger with empty aging F8F550*/

    CREATE arage-list.
    arage-list.number-str = STRING(ledger.artnr) + " -".
    arage-list.customer-name = CAPS(ENTRY(2,ledger.bezeich,"-")). 
    CREATE arage-list.

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
          DO:
              CREATE arage-list.
              ASSIGN
                  arage-list.number-str     = STRING(ct,">>>9")
                  arage-list.customer-name  = gastname
                  arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>9.99")
                  arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>9.99")
                  arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>9.99")
                  arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>9.99")
                  arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>9.99")                  
                  .

              IF artikel.artart EQ 2 THEN
              DO:
                  ASSIGN
                      arage-list.curr   = age-list.fcurr
                      arage-list.gastnr = age-list.gastnr
                      .
              END.
          END.
          ELSE
          DO:
              CREATE arage-list.
              ASSIGN
                  arage-list.number-str     = STRING(ct,">>>9")
                  arage-list.customer-name  = gastname
                  arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>>,>>9.99")
                  arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>>,>>9.99")
                  arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>>,>>9.99")
                  arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>>,>>9.99")
                  arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>>,>>9.99")
                  .      

              IF artikel.artart EQ 2 THEN
              DO:
                  ASSIGN
                      arage-list.curr   = age-list.fcurr
                      arage-list.gastnr = age-list.gastnr
                      .
              END.
          END.          
        END. 
        ELSE
        DO:
            CREATE arage-list.
            ASSIGN
                arage-list.number-str     = STRING(ct,">>>9")
                arage-list.customer-name  = gastname
                arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>>,>>9.99")
                .  
            IF artikel.artart EQ 2 THEN
            DO:
                ASSIGN
                    arage-list.curr     = age-list.fcurr
                    arage-list.gastnr   = age-list.gastnr
                    .
            END.
        END.            

        ASSIGN            
            creditlimit = age-list.creditlimit 
            gastname    = age-list.gastname
            tot-debt    = age-list.tot-debt 
            debt0       = age-list.debt0
            debt1       = age-list.debt1 
            debt2       = age-list.debt2 
            debt3       = age-list.debt3 
            ct          = ct + 1
        .
        arage-list.creditlimit = creditlimit.        
        /*naufal*/
        IF arage-list.creditlimit NE 0 THEN
            arage-list.balance = arage-list.creditlimit - tot-debt.
        ELSE 
            arage-list.balance = 0.
        /*end naufal*/

        arage-list.creditlimit-str = STRING(arage-list.creditlimit, "->>,>>>,>>>,>>>,>>9.99").
        arage-list.balance-str = STRING(arage-list.balance, "->>,>>>,>>>,>>>,>>9.99").
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
        DO:
            CREATE arage-list.
            ASSIGN
                arage-list.number-str     = STRING(ct,">>>9")
                arage-list.customer-name  = gastname
                arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>9.99")
                arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>9.99")
                arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>9.99")
                arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>9.99")
                arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>9.99")                  
                .   

            IF artikel.artart EQ 2 THEN
            DO:
                ASSIGN
                    arage-list.curr     = curr-fcurr
                    arage-list.gastnr   = curr-gastnr
                    .
            END.
        END.
        ELSE
        DO:
            CREATE arage-list.
            ASSIGN
                arage-list.number-str     = STRING(ct,">>>9")
                arage-list.customer-name  = gastname
                arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.curr           = age-list.fcurr
                arage-list.gastnr         = age-list.gastnr
                .  

            IF artikel.artart EQ 2 THEN
            DO:
                ASSIGN
                    arage-list.curr     = curr-fcurr
                    arage-list.gastnr   = curr-gastnr
                    .
            END.
        END.        
      END. 
      ELSE
      DO:
          CREATE arage-list.
          ASSIGN
              arage-list.number-str     = STRING(ct,">>>9")
              arage-list.customer-name  = gastname
              arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>>,>>9.99")              
              .  

          IF artikel.artart EQ 2 THEN
          DO:
              ASSIGN
                  arage-list.curr   = curr-fcurr
                  arage-list.gastnr = curr-gastnr
                  .
          END.
      END.                

      arage-list.creditlimit = creditlimit.
      /*naufal*/
      IF arage-list.creditlimit NE 0 THEN
          arage-list.balance = arage-list.creditlimit - tot-debt.
      ELSE 
          arage-list.balance = 0.
      /*end naufal*/

      arage-list.creditlimit-str = STRING(arage-list.creditlimit, "->>,>>>,>>>,>>>,>>9.99").
      arage-list.balance-str = STRING(arage-list.balance, "->>,>>>,>>>,>>>,>>9.99").
    END. 
 
    tmp-saldo = ledger.tot-debt. 
    IF tmp-saldo = 0 THEN tmp-saldo = 1. 
    
    IF price-decimal = 0 THEN 
    DO: 
      IF NOT long-digit THEN 
      DO:
          CREATE arage-list.
          ASSIGN
              arage-list.customer-name  = "T o t a l"
              arage-list.outstanding    = STRING(ledger.tot-debt, "->>,>>>,>>>,>>9.99")
              arage-list.age1           = STRING(ledger.debt0, "->>,>>>,>>>,>>9.99")
              arage-list.age2           = STRING(ledger.debt1, "->>,>>>,>>>,>>9.99")
              arage-list.age3           = STRING(ledger.debt2, "->>,>>>,>>>,>>9.99")
              arage-list.age4           = STRING(ledger.debt3, "->>,>>>,>>>,>>9.99")              
              . 
      END.
      ELSE
      DO:
          CREATE arage-list.
          ASSIGN
              arage-list.customer-name  = "T o t a l"
              arage-list.outstanding    = STRING(ledger.tot-debt, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age1           = STRING(ledger.debt0, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age2           = STRING(ledger.debt1, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age3           = STRING(ledger.debt2, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age4           = STRING(ledger.debt3, "->>,>>>,>>>,>>>,>>9.99")              
              . 
      END.      
    END. 
    ELSE
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "T o t a l"
            arage-list.outstanding    = STRING(ledger.tot-debt, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age1           = STRING(ledger.debt0, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age2           = STRING(ledger.debt1, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age3           = STRING(ledger.debt2, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age4           = STRING(ledger.debt3, "->>,>>>,>>>,>>>,>>9.99")              
            . 
    END.         
    
    IF NOT long-digit THEN 
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "Statistic Percentage (%):"
            arage-list.outstanding    = STRING((ledger.tot-debt / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age1           = STRING((ledger.debt0 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age2           = STRING((ledger.debt1 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age3           = STRING((ledger.debt2 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age4           = STRING((ledger.debt3 / tmp-saldo * 100), "->>,>>9.99")              
            . 
    END.
    ELSE
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "Statistic Percentage (%):"
            arage-list.outstanding    = STRING((ledger.tot-debt / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age1           = STRING((ledger.debt0 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age2           = STRING((ledger.debt1 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age3           = STRING((ledger.debt2 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age4           = STRING((ledger.debt3 / tmp-saldo * 100), "->>,>>9.99")              
            . 
    END.
    CREATE arage-list.   
  END. 
 
  CREATE arage-list. 
  IF price-decimal = 0 THEN 
  DO: 
    IF NOT long-digit THEN 
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "T O T A L  A/R:"
            arage-list.outstanding    = STRING(t-saldo, "->>,>>>,>>>,>>9.99")
            arage-list.age1           = STRING(t-debt0, "->>,>>>,>>>,>>9.99")
            arage-list.age2           = STRING(t-debt1, "->>,>>>,>>>,>>9.99")
            arage-list.age3           = STRING(t-debt2, "->>,>>>,>>>,>>9.99")
            arage-list.age4           = STRING(t-debt3, "->>,>>>,>>>,>>9.99")              
            . 
    END.
    ELSE
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "T O T A L  A/R:"
            arage-list.outstanding    = STRING(t-saldo, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age1           = STRING(t-debt0, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age2           = STRING(t-debt1, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age3           = STRING(t-debt2, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age4           = STRING(t-debt3, "->>,>>>,>>>,>>>,>>9.99")              
            . 
    END.    
  END. 
  ELSE
  DO:
      CREATE arage-list.
      ASSIGN
          arage-list.customer-name  = "T O T A L  A/R:"
          arage-list.outstanding    = STRING(t-saldo, "->>,>>>,>>>,>>>,>>9.99")
          arage-list.age1           = STRING(t-debt0, "->>,>>>,>>>,>>>,>>9.99")
          arage-list.age2           = STRING(t-debt1, "->>,>>>,>>>,>>>,>>9.99")
          arage-list.age3           = STRING(t-debt2, "->>,>>>,>>>,>>>,>>9.99")
          arage-list.age4           = STRING(t-debt3, "->>,>>>,>>>,>>>,>>9.99")              
          . 
  END.      
  CREATE arage-list.
  
  IF NOT long-digit THEN 
  DO:
      CREATE arage-list.
      ASSIGN
          arage-list.customer-name  = "Statistic Percentage (%):"
          arage-list.outstanding    = "100.00"
          arage-list.age1           = STRING((t-debt0 / t-saldo * 100), "->>,>>9.99") 
          arage-list.age2           = STRING((t-debt1 / t-saldo * 100), "->>,>>9.99")
          arage-list.age3           = STRING((t-debt2 / t-saldo * 100), "->>,>>9.99")
          arage-list.age4           = STRING((t-debt3 / t-saldo * 100), "->>,>>9.99")             
          . 
  END.  
  ELSE
  DO:
      CREATE arage-list.
      ASSIGN
          arage-list.customer-name  = "Statistic Percentage (%):"
          arage-list.outstanding    = "100.00"
          arage-list.age1           = STRING((t-debt0 / t-saldo * 100), "->>,>>9.99") 
          arage-list.age2           = STRING((t-debt1 / t-saldo * 100), "->>,>>9.99")
          arage-list.age3           = STRING((t-debt2 / t-saldo * 100), "->>,>>9.99")
          arage-list.age4           = STRING((t-debt3 / t-saldo * 100), "->>,>>9.99")             
          .
  END.
  CREATE arage-list.
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
  FOR EACH arage-list: 
    DELETE arage-list. 
  END. 
 
  FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
      AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
      AND artikel.departement = 0
      /*AND artikel.activeflag    william add activeflag F8F550*/
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
        
      IF disptype = 1 THEN DO : 
        IF NOT cvt-flag THEN ar-saldo = debitor.vesrdep.
        ELSE ASSIGN ar-saldo = debitor.saldo / dollar-rate.  
      END.
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
            ELSE DO:
                IF NOT cvt-flag THEN ar-saldo = ar-saldo +  debt.vesrdep.
                ELSE ar-saldo = ar-saldo + (debt.saldo / dollar-rate). 
            END.
        END. 
        ELSE
        FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
          AND debt.counter = debitor.counter AND debt.opart = 1 
          AND debt.zahlkonto NE 0 AND debt.betrieb-gastmem = debitor.betrieb-gastmem
          AND debt.rgdatum LE to-date NO-LOCK USE-INDEX deb-rechnr_ix: 
            IF NOT cvt-flag THEN ar-saldo = ar-saldo +  debt.vesrdep.
            ELSE ar-saldo = ar-saldo + (debt.saldo / dollar-rate). 
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
 
      /* Rd, #753, 27Mar25, date variable */
      tmpdays = to-date - age-list.rgdatum.
      IF tmpdays GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF tmpdays GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF tmpdays GT day1 
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
      ELSE DO:
        IF NOT cvt-flag THEN ar-saldo = debitor.vesrdep.
        ELSE ar-saldo = debitor.saldo / dollar-rate. 
      END.
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
        IF NOT cvt-flag THEN ar-saldo = ar-saldo +  debt.vesrdep.
        ELSE ar-saldo = ar-saldo + (debt.saldo / dollar-rate). 
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
 
      /* Rd, #753, 27Mar25, date variable */
      tmpdays = to-date - age-list.rgdatum.
      IF tmpdays GT day3 
        THEN age-list.debt3 = age-list.debt3 + ar-saldo. 
      ELSE IF tmpdays GT day2 
        THEN age-list.debt2 = age-list.debt2 + ar-saldo. 
      ELSE IF tmpdays GT day1 
        THEN age-list.debt1 = age-list.debt1 + ar-saldo. 
      ELSE age-list.debt0 = age-list.debt0 + ar-saldo. 
    END. 
  END. 
 
  
  FOR EACH ledger BY ledger.artnr: 
    FIND FIRST age-list WHERE age-list.artnr = ledger.artnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE age-list THEN NEXT. /*william add validation to not show ledger with empty aging F8F550*/

    CREATE arage-list.
    arage-list.number-str = STRING(ledger.artnr) + " -".
    arage-list.customer-name = CAPS(ENTRY(2,ledger.bezeich,"-")).  
    CREATE arage-list.

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
          DO:
              CREATE arage-list.
              ASSIGN
                  arage-list.number-str     = STRING(ct,">>>9")
                  arage-list.customer-name  = gastname
                  arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>9.99")
                  arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>9.99")
                  arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>9.99")
                  arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>9.99")
                  arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>9.99")   
                  arage-list.curr           = age-list.fcurr
                  arage-list.gastnr         = age-list.gastnr
                  .
          END.
          ELSE
          DO:
              CREATE arage-list.
              ASSIGN
                  arage-list.number-str     = STRING(ct,">>>9")
                  arage-list.customer-name  = gastname
                  arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>>,>>9.99")
                  arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>>,>>9.99")
                  arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>>,>>9.99")
                  arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>>,>>9.99")
                  arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>>,>>9.99")
                  arage-list.curr           = age-list.fcurr
                  arage-list.gastnr         = age-list.gastnr
                  .
          END.          
        END. 
        ELSE
        DO:
            CREATE arage-list.
            ASSIGN
                arage-list.number-str     = STRING(ct,">>>9")
                arage-list.customer-name  = gastname
                arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.curr           = age-list.fcurr
                arage-list.gastnr         = age-list.gastnr
                  .
        END.
            
        arage-list.creditlimit = creditlimit.
        /*naufal*/
        IF arage-list.creditlimit NE 0 THEN
            arage-list.balance = arage-list.creditlimit - tot-debt.
        ELSE 
            arage-list.balance = 0.
        /*end naufal*/

        arage-list.creditlimit-str = STRING(arage-list.creditlimit, "->>,>>>,>>>,>>>,>>9.99").
        arage-list.balance-str = STRING(arage-list.balance, "->>,>>>,>>>,>>>,>>9.99").

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
        DO:
            CREATE arage-list.
            ASSIGN
                arage-list.number-str     = STRING(ct,">>>9")
                arage-list.customer-name  = gastname
                arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>9.99")
                arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>9.99")
                arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>9.99")
                arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>9.99")
                arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>9.99")   
                arage-list.curr           = curr-fcurr
                arage-list.gastnr         = curr-gastnr
                .
        END.
        ELSE
        DO:
            CREATE arage-list.
            ASSIGN
                arage-list.number-str     = STRING(ct,">>>9")
                arage-list.customer-name  = gastname
                arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>>,>>9.99")
                arage-list.curr           = curr-fcurr 
                arage-list.gastnr         = curr-gastnr
                .
        END.         
      END. 
      ELSE
      DO:
          CREATE arage-list.
          ASSIGN
              arage-list.number-str     = STRING(ct,">>>9")
              arage-list.customer-name  = gastname
              arage-list.outstanding    = STRING(tot-debt, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age1           = STRING(debt0, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age2           = STRING(debt1, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age3           = STRING(debt2, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age4           = STRING(debt3, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.curr           = curr-fcurr 
              arage-list.gastnr         = curr-gastnr
              .
      END.
                
      arage-list.creditlimit = creditlimit.
      /*naufal*/
        IF arage-list.creditlimit NE 0 THEN
            arage-list.balance = arage-list.creditlimit - tot-debt.
        ELSE 
            arage-list.balance = 0.
      /*end naufal*/
       
      arage-list.creditlimit-str = STRING(arage-list.creditlimit, "->>,>>>,>>>,>>>,>>9.99").
      arage-list.balance-str = STRING(arage-list.balance, "->>,>>>,>>>,>>>,>>9.99").
    END. 
 
    tmp-saldo = ledger.tot-debt. 
    IF tmp-saldo = 0 THEN tmp-saldo = 1. 
     
    IF price-decimal = 0 THEN 
    DO: 
      IF NOT long-digit THEN 
      DO:
          CREATE arage-list.
          ASSIGN
              arage-list.customer-name  = "T o t a l"
              arage-list.outstanding    = STRING(ledger.tot-debt, "->>,>>>,>>>,>>9.99")
              arage-list.age1           = STRING(ledger.debt0, "->>,>>>,>>>,>>9.99")
              arage-list.age2           = STRING(ledger.debt1, "->>,>>>,>>>,>>9.99")
              arage-list.age3           = STRING(ledger.debt2, "->>,>>>,>>>,>>9.99")
              arage-list.age4           = STRING(ledger.debt3, "->>,>>>,>>>,>>9.99")              
              . 
      END.
      ELSE
      DO:
          CREATE arage-list.
          ASSIGN
              arage-list.customer-name  = "T o t a l"
              arage-list.outstanding    = STRING(ledger.tot-debt, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age1           = STRING(ledger.debt0, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age2           = STRING(ledger.debt1, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age3           = STRING(ledger.debt2, "->>,>>>,>>>,>>>,>>9.99")
              arage-list.age4           = STRING(ledger.debt3, "->>,>>>,>>>,>>>,>>9.99")              
              . 
      END. 
    END. 
    ELSE
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "T o t a l"
            arage-list.outstanding    = STRING(ledger.tot-debt, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age1           = STRING(ledger.debt0, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age2           = STRING(ledger.debt1, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age3           = STRING(ledger.debt2, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age4           = STRING(ledger.debt3, "->>,>>>,>>>,>>>,>>9.99")              
            . 
    END.
            
    IF NOT long-digit THEN 
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "Statistic Percentage (%):"
            arage-list.outstanding    = STRING((ledger.tot-debt / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age1           = STRING((ledger.debt0 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age2           = STRING((ledger.debt1 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age3           = STRING((ledger.debt2 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age4           = STRING((ledger.debt3 / tmp-saldo * 100), "->>,>>9.99")              
            . 
    END.
    ELSE
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "Statistic Percentage (%):"
            arage-list.outstanding    = STRING((ledger.tot-debt / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age1           = STRING((ledger.debt0 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age2           = STRING((ledger.debt1 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age3           = STRING((ledger.debt2 / tmp-saldo * 100), "->>,>>9.99")
            arage-list.age4           = STRING((ledger.debt3 / tmp-saldo * 100), "->>,>>9.99")              
            . 
    END.
    CREATE arage-list.
  END. 
 
  CREATE arage-list.
  IF price-decimal = 0 THEN 
  DO: 
    IF NOT long-digit THEN 
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "T O T A L  A/R:"
            arage-list.outstanding    = STRING(t-saldo, "->>,>>>,>>>,>>9.99")
            arage-list.age1           = STRING(t-debt0, "->>,>>>,>>>,>>9.99")
            arage-list.age2           = STRING(t-debt1, "->>,>>>,>>>,>>9.99")
            arage-list.age3           = STRING(t-debt2, "->>,>>>,>>>,>>9.99")
            arage-list.age4           = STRING(t-debt3, "->>,>>>,>>>,>>9.99")              
            . 
    END.
    ELSE
    DO:
        CREATE arage-list.
        ASSIGN
            arage-list.customer-name  = "T O T A L  A/R:"
            arage-list.outstanding    = STRING(t-saldo, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age1           = STRING(t-debt0, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age2           = STRING(t-debt1, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age3           = STRING(t-debt2, "->>,>>>,>>>,>>>,>>9.99")
            arage-list.age4           = STRING(t-debt3, "->>,>>>,>>>,>>>,>>9.99")              
            . 
    END.
  END. 
  ELSE
  DO:
      CREATE arage-list.
      ASSIGN
          arage-list.customer-name  = "T O T A L  A/R:"
          arage-list.outstanding    = STRING(t-saldo, "->>,>>>,>>>,>>>,>>9.99")
          arage-list.age1           = STRING(t-debt0, "->>,>>>,>>>,>>>,>>9.99")
          arage-list.age2           = STRING(t-debt1, "->>,>>>,>>>,>>>,>>9.99")
          arage-list.age3           = STRING(t-debt2, "->>,>>>,>>>,>>>,>>9.99")
          arage-list.age4           = STRING(t-debt3, "->>,>>>,>>>,>>>,>>9.99")              
          . 
  END.
  CREATE arage-list.     
  
  IF NOT long-digit THEN 
  DO:
      CREATE arage-list.
      ASSIGN
          arage-list.customer-name  = "Statistic Percentage (%):"
          arage-list.outstanding    = "100.00"
          arage-list.age1           = STRING((t-debt0 / t-saldo * 100), "->>,>>9.99") 
          arage-list.age2           = STRING((t-debt1 / t-saldo * 100), "->>,>>9.99")
          arage-list.age3           = STRING((t-debt2 / t-saldo * 100), "->>,>>9.99")
          arage-list.age4           = STRING((t-debt3 / t-saldo * 100), "->>,>>9.99")             
          . 
  END.  
  ELSE
  DO:
      CREATE arage-list.
      ASSIGN
          arage-list.customer-name  = "Statistic Percentage (%):"
          arage-list.outstanding    = "100.00"
          arage-list.age1           = STRING((t-debt0 / t-saldo * 100), "->>,>>9.99") 
          arage-list.age2           = STRING((t-debt1 / t-saldo * 100), "->>,>>9.99")
          arage-list.age3           = STRING((t-debt2 / t-saldo * 100), "->>,>>9.99")
          arage-list.age4           = STRING((t-debt3 / t-saldo * 100), "->>,>>9.99")             
          .
  END.
  CREATE arage-list.
END. 



