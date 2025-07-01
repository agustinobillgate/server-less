
DEF INPUT PARAMETER curr-dept       AS INT.
DEF INPUT PARAMETER cbuff-artnr     AS INT.
DEF INPUT PARAMETER cbuff-qty       AS DECIMAL.
DEF INPUT PARAMETER selected-date   AS DATE.
DEF INPUT PARAMETER user-init       AS CHAR.
DEF INPUT PARAMETER cbuff-price     AS DECIMAL.
DEF INPUT PARAMETER cbuff-lief-nr   AS INT.
DEF INPUT PARAMETER cbuff-approved  AS LOGICAL.
DEF INPUT PARAMETER cbuff-remark    AS CHAR.


IF curr-dept = 0 THEN 
DO: 
  FIND FIRST dml-art WHERE dml-art.artnr = cbuff-artnr
    AND dml-art.datum = selected-date EXCLUSIVE-LOCK NO-ERROR. 

  IF NOT AVAILABLE dml-art THEN 
  DO: 
    CREATE dml-art. 
    ASSIGN
      dml-art.artnr    = cbuff-artnr
      dml-art.datum    = selected-date 
      dml-art.userinit = user-init
    .
  END.
  ASSIGN
    dml-art.anzahl      = cbuff-qty
    dml-art.einzelpreis = cbuff-price
    dml-art.userinit    = ENTRY(1, dml-art.userinit, ";")
    dml-art.chginit     = user-init.

  /*ITA 170518 --> add remark*/
    FIND FIRST queasy WHERE queasy.KEY = 202 
        AND queasy.number1 = 0
        AND queasy.number2 = cbuff-artnr
        AND queasy.date1 = selected-date NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 202
            queasy.number1  = 0
            queasy.number2  = cbuff-artnr
            queasy.date1    = selected-date
            queasy.char1    = cbuff-remark.
    END.
    ELSE DO: 
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN queasy.char1 = cbuff-remark.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
  /*end*/

  IF cbuff-lief-nr GT 0 THEN 
  ASSIGN dml-art.userinit = dml-art.userinit 
          + ";" + STRING(cbuff-lief-nr). 
  IF cbuff-approved THEN DO: 
      dml-art.chginit = dml-art.chginit + "!".

      FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = 0 
            AND queasy.date1 = dml-art.datum AND queasy.logi1 = YES 
            /*AND queasy.logi2 = NO*/ NO-LOCK NO-ERROR.
      IF NOT AVAILABLE queasy THEN DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY      = 254 
                queasy.number1  = 0 
                queasy.date1    = dml-art.datum 
                queasy.logi1    = YES 
                queasy.logi2    = NO
             .  
      END.
  END.
  FIND CURRENT dml-art NO-LOCK. 
END. 
ELSE 
DO: 
  FIND FIRST dml-artdep WHERE dml-artdep.artnr = cbuff-artnr 
    AND dml-artdep.datum = selected-date 
    AND dml-artdep.departement = curr-dept EXCLUSIVE-LOCK NO-ERROR. 

  IF NOT AVAILABLE dml-artdep THEN 
  DO: 
    CREATE dml-artdep. 
    ASSIGN
      dml-artdep.artnr       = cbuff-artnr 
      dml-artdep.datum       = selected-date 
      dml-artdep.departement = curr-dept 
      dml-artdep.userinit    = user-init
    . 
  END.
  ASSIGN
    dml-artdep.anzahl      = cbuff-qty
    dml-artdep.einzelpreis = cbuff-price 
    dml-artdep.userinit    = ENTRY(1, dml-artdep.userinit, ";")
    dml-artdep.chginit     = user-init
  . 

  /*ITA 170518 --> add remark*/
    FIND FIRST queasy WHERE queasy.KEY = 202 
        AND queasy.number1 = curr-dept
        AND queasy.number2 = cbuff-artnr
        AND queasy.date1 = selected-date NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY      = 202
            queasy.number1  = curr-dept
            queasy.number2  = cbuff-artnr
            queasy.date1    = selected-date
            queasy.char1    = cbuff-remark.
    END.
    ELSE DO: 
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN queasy.char1 = cbuff-remark.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
  /*end*/

  IF cbuff-lief-nr GT 0 THEN 
  ASSIGN dml-artdep.userinit = dml-artdep.userinit 
         + ";" + STRING(cbuff-lief-nr). 
  IF cbuff-approved THEN DO: 
      dml-artdep.chginit = dml-artdep.chginit + "!".

      FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = dml-artdep.departement 
            AND queasy.date1 = dml-artdep.datum AND queasy.logi1 = YES 
            /*AND queasy.logi2 = NO*/ NO-LOCK NO-ERROR.
      IF NOT AVAILABLE queasy THEN DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY      = 254 
                queasy.number1  = dml-artdep.departement
                queasy.date1    = dml-artdep.datum 
                queasy.logi1    = YES 
                queasy.logi2    = NO
             .  
      END.
  END.
  FIND CURRENT dml-artdep NO-LOCK. 
END. 

/*
IF curr-dept = 0 THEN 
DO: 
  FIND FIRST dml-art WHERE dml-art.artnr = cbuff-artnr 
    AND dml-art.datum = selected-date EXCLUSIVE-LOCK NO-ERROR. 

  IF NOT AVAILABLE dml-art THEN 
  DO: 
    CREATE dml-art. 
    ASSIGN
      dml-art.artnr    = cbuff-artnr 
      dml-art.datum    = selected-date 
      dml-art.userinit = user-init
    .
  END.
  ASSIGN
    dml-art.anzahl      = cbuff-qty
    dml-art.einzelpreis = cbuff-price
    dml-art.userinit    = ENTRY(1, dml-art.userinit, ";")
    dml-art.chginit     = user-init
  . 
  IF cbuff-lief-nr GT 0 THEN 
  ASSIGN dml-art.userinit = dml-art.userinit 
          + ";" + STRING(cbuff-lief-nr). 
  IF cbuff-approved THEN dml-art.chginit = dml-art.chginit + "!".
  FIND CURRENT dml-art NO-LOCK. 
END. 
ELSE 
DO: 
  FIND FIRST dml-artdep WHERE dml-artdep.artnr = cbuff-artnr 
    AND dml-artdep.datum = selected-date 
    AND dml-artdep.departement = curr-dept EXCLUSIVE-LOCK NO-ERROR. 

  IF NOT AVAILABLE dml-artdep THEN 
  DO: 
    CREATE dml-artdep. 
    ASSIGN
      dml-artdep.artnr       = cbuff-artnr 
      dml-artdep.datum       = selected-date 
      dml-artdep.departement = curr-dept 
      dml-artdep.userinit    = user-init
    . 
  END.
  ASSIGN
    dml-artdep.anzahl      = cbuff-qty
    dml-artdep.einzelpreis = cbuff-price 
    dml-artdep.userinit    = ENTRY(1, dml-artdep.userinit, ";")
    dml-artdep.chginit     = user-init
  . 
  IF cbuff-lief-nr GT 0 THEN 
  ASSIGN dml-artdep.userinit = dml-artdep.userinit 
         + ";" + STRING(cbuff-lief-nr). 
  IF cbuff-approved THEN dml-artdep.chginit = dml-artdep.chginit + "!".
  FIND CURRENT dml-artdep NO-LOCK. 
END.
*/
