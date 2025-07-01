/* Created by Gerald Fixed Asset Budget List F9131B*/ 
DEFINE TEMP-TABLE fa-budget                  
    FIELD name              AS CHAR
    FIELD asset             AS CHAR
    FIELD datum             AS DATE
    FIELD bezeich           AS CHAR
    FIELD fibukonto         AS CHAR
    FIELD price             AS DECIMAL
    FIELD price-str         AS CHAR
    FIELD anzahl            AS INTEGER
    FIELD anzahl-str        AS CHAR
    FIELD warenwert         AS DECIMAL
    FIELD warenwert-str     AS CHAR
    FIELD mtd-budget        AS DECIMAL
    FIELD mtd-budget-str    AS CHAR
    FIELD mtd-balance       AS DECIMAL
    FIELD mtd-balance-str   AS CHAR
    FIELD ytd-budget        AS DECIMAL
    FIELD ytd-budget-str    AS CHAR
    FIELD ytd-balance       AS DECIMAL
    FIELD ytd-balance-str   AS CHAR
    . 

DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE INPUT PARAMETER detailed  AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR fa-budget.

DEFINE VARIABLE i               AS INTEGER.
DEFINE VARIABLE c               AS CHAR.
DEFINE VARIABLE fibu            AS CHAR.
DEFINE VARIABLE beg-date        AS DATE.
DEFINE VARIABLE jan             AS INTEGER INITIAL 1.
DEFINE VARIABLE mm              AS INTEGER.
DEFINE VARIABLE mtd-budget      AS DECIMAL.
DEFINE VARIABLE mtd-balance     AS DECIMAL.
DEFINE VARIABLE ytd-budget      AS DECIMAL.
DEFINE VARIABLE ytd-balance     AS DECIMAL.
DEFINE VARIABLE t-anzahl        AS DECIMAL.
DEFINE VARIABLE t-warenwert     AS DECIMAL.

DEFINE VARIABLE t-mtd-balance   AS DECIMAL.
DEFINE VARIABLE t-ytd-balance   AS DECIMAL.
DEFINE VARIABLE tt-anzahl       AS DECIMAL.
DEFINE VARIABLE tt-warenwert    AS DECIMAL.
DEFINE VARIABLE tt-mtd-balance  AS DECIMAL.
DEFINE VARIABLE tt-ytd-balance  AS DECIMAL.

beg-date = DATE(1,1,YEAR(to-date)).
mm = MONTH(to-date).

IF detailed THEN
DO:
  FOR EACH fa-op WHERE fa-op.loeschflag LE 1
        AND fa-op.datum GE from-date AND fa-op.datum LE to-date NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag GT 0 no-lock,
        FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK BY fa-artikel.fibukonto BY fa-op.datum:

        IF fibu = "" THEN
        DO:
           mtd-budget    = 0.
           ytd-budget    = 0. 

           RUN convert-fibu(fa-artikel.fibukonto, OUTPUT c).

           mtd-budget = gl-acct.budget[MONTH(to-date)].

           DO i = jan TO mm: 
               ytd-budget = ytd-budget + gl-acct.budget[i]. 
           END.

           CREATE fa-budget.
           ASSIGN fa-budget.bezeich        = fa-grup.bezeich + " - " + c
                  fa-budget.fibukonto      = fa-artikel.fibukonto
                  fa-budget.mtd-budget-str = STRING(mtd-budget, "->>>,>>>,>>>,>>>,>>9.99")
                  fa-budget.ytd-budget-str = STRING(ytd-budget, "->>>,>>>,>>>,>>>,>>9.99").

           fibu          = fa-artikel.fibukonto.
           t-anzahl      = 0.
           t-warenwert   = 0.
           t-mtd-balance = 0.
           t-ytd-balance = 0.
        END.

        IF fibu NE fa-artikel.fibukonto THEN
        DO:
           
           RUN convert-fibu(fa-artikel.fibukonto, OUTPUT c).

           CREATE fa-budget.
           ASSIGN 
                  fa-budget.bezeich         = "T O T A L"
                  fa-budget.fibukonto       = fa-artikel.fibukonto
                  fa-budget.anzahl-str      = STRING(t-anzahl, "->>>,>>9")
                  fa-budget.warenwert-str   = STRING(t-warenwert, "->>>,>>>,>>>,>>>,>>9.99")
                  fa-budget.mtd-budget-str  = STRING(mtd-budget, "->>>,>>>,>>>,>>>,>>9.99")
                  fa-budget.mtd-balance-str = STRING(mtd-balance, "->>>,>>>,>>>,>>>,>>9.99")
                  fa-budget.ytd-budget-str  = STRING(ytd-budget, "->>>,>>>,>>>,>>>,>>9.99")
                  fa-budget.ytd-balance-str = STRING(ytd-balance, "->>>,>>>,>>>,>>>,>>9.99").

           mtd-budget    = 0.
           ytd-budget    = 0.

           mtd-budget = gl-acct.budget[MONTH(to-date)].

           DO i = jan TO mm:  
              ytd-budget = ytd-budget + gl-acct.budget[i]. 
           END.

           CREATE fa-budget.
           ASSIGN fa-budget.bezeich        = fa-grup.bezeich + " - " + c
                  fa-budget.fibukonto      = fa-artikel.fibukonto
                  fa-budget.mtd-budget-str = STRING(mtd-budget, "->>>,>>>,>>>,>>>,>>9.99")
                  fa-budget.ytd-budget-str = STRING(ytd-budget, "->>>,>>>,>>>,>>>,>>9.99").
                  
           fibu          = fa-artikel.fibukonto. 
           t-anzahl      = 0.
           t-warenwert   = 0.
           t-mtd-balance = 0.
           t-ytd-balance = 0.
        END.

        ASSIGN
          t-anzahl       = t-anzahl + fa-op.anzahl
          t-warenwert    = t-warenwert + fa-op.warenwert
          mtd-balance    = (mtd-budget - t-warenwert)
          ytd-balance    = (ytd-budget - t-warenwert)
          t-mtd-balance  = t-mtd-balance + mtd-balance
          t-ytd-balance  = t-ytd-balance + ytd-balance
          tt-anzahl      = tt-anzahl + fa-op.anzahl
          tt-warenwert   = tt-warenwert + fa-op.warenwert
          tt-mtd-balance = tt-mtd-balance + mtd-balance
          tt-ytd-balance = tt-ytd-balance + ytd-balance.
        
        CREATE fa-budget.
        ASSIGN fa-budget.bezeich         = mathis.NAME
               fa-budget.datum           = fa-op.datum
               fa-budget.fibukonto       = fa-artikel.fibukonto
               fa-budget.price-str       = STRING(fa-op.einzelpreis, "->>>,>>>,>>>,>>>,>>9.99")
               fa-budget.anzahl-str      = STRING(fa-op.anzahl, "->>>,>>9")
               fa-budget.warenwert-str   = STRING(fa-op.warenwert, "->>>,>>>,>>>,>>>,>>9.99")
               /*fa-budget.mtd-budget-str  = STRING(mtd-budget, "->>>,>>>,>>>,>>>,>>9.99")
               fa-budget.mtd-balance-str = STRING(mtd-balance, "->>>,>>>,>>>,>>>,>>9.99")
               fa-budget.ytd-budget-str  = STRING(ytd-budget, "->>>,>>>,>>>,>>>,>>9.99")
               fa-budget.ytd-balance-str = STRING(ytd-balance, "->>>,>>>,>>>,>>>,>>9.99")*/
               .
    END.

    CREATE fa-budget.
    ASSIGN 
           fa-budget.bezeich         = "T O T A L"
           fa-budget.anzahl-str      = STRING(t-anzahl, "->>>,>>9")
           fa-budget.warenwert-str   = STRING(t-warenwert, "->>>,>>>,>>>,>>>,>>9.99")
           fa-budget.mtd-budget-str  = STRING(mtd-budget, "->>>,>>>,>>>,>>>,>>9.99")
           fa-budget.mtd-balance-str = STRING(mtd-balance, "->>>,>>>,>>>,>>>,>>9.99")
           fa-budget.ytd-budget-str  = STRING(ytd-budget, "->>>,>>>,>>>,>>>,>>9.99")
           fa-budget.ytd-balance-str = STRING(ytd-balance, "->>>,>>>,>>>,>>>,>>9.99").
END.
ELSE 
DO:
    mtd-budget = 0.
    ytd-budget = 0.

    FOR EACH fa-budget:
        DELETE fa-budget.
    END.

    FOR EACH fa-op WHERE fa-op.loeschflag LE 1
        AND fa-op.datum GE beg-date AND fa-op.datum LE to-date NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-op.nr NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag GT 0 no-lock,
        FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK BY fa-artikel.fibukonto BY fa-op.datum:

        IF fibu NE fa-artikel.fibukonto THEN
        DO:
           mtd-budget    = 0.
           ytd-budget    = 0.  
           t-anzahl      = 0.
           t-warenwert   = 0.
           t-mtd-balance = 0.
           t-ytd-balance = 0. 
           
           RUN convert-fibu(fa-artikel.fibukonto, OUTPUT c).

           mtd-budget = gl-acct.budget[MONTH(to-date)].
           DO i = jan TO mm:  
              ytd-budget = ytd-budget + gl-acct.budget[i]. 
           END.

           IF fa-op.datum GE from-date AND fa-op.datum LE to-date THEN
           DO:
             CREATE fa-budget.
             ASSIGN fa-budget.bezeich         = fa-grup.bezeich + " - " + c
                    fa-budget.fibukonto       = fa-artikel.fibukonto
                    fa-budget.mtd-budget-str  = STRING(mtd-budget, "->>>,>>>,>>>,>>>,>>9.99")
                    fa-budget.ytd-budget-str  = STRING(ytd-budget, "->>>,>>>,>>>,>>>,>>9.99").
                    fibu = fa-artikel.fibukonto.
           END.
        END.

        IF fa-op.datum GE from-date AND fa-op.datum LE to-date THEN
        DO:
          t-anzahl    = t-anzahl + fa-op.anzahl.
          t-warenwert = t-warenwert + fa-op.warenwert.
          mtd-balance = (mtd-budget - t-warenwert).
        END.
        
        ASSIGN
          tt-warenwert              = tt-warenwert + fa-op.warenwert
          ytd-balance               = (ytd-budget - tt-warenwert)
          t-mtd-balance             = t-mtd-balance + mtd-balance
          t-ytd-balance             = t-ytd-balance + ytd-balance
          fa-budget.anzahl-str      = STRING(t-anzahl, "->>>,>>9")
          fa-budget.warenwert-str   = STRING(t-warenwert, "->>>,>>>,>>>,>>>,>>9.99")
          fa-budget.mtd-balance-str = STRING(mtd-balance, "->>>,>>>,>>>,>>>,>>9.99")
          fa-budget.ytd-balance-str = STRING(ytd-balance, "->>>,>>>,>>>,>>>,>>9.99").
    END.
    
END.

PROCEDURE convert-fibu: 
DEFINE INPUT  PARAMETER konto   AS CHAR. 
DEFINE OUTPUT PARAMETER s       AS CHAR INITIAL "". 
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
  ch = htparam.fchar. 
  j = 0. 
  DO i = 1 TO length(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 

