
DEF INPUT PARAMETER curr-dept       AS INT.
DEF INPUT PARAMETER cbuff-artnr     AS INT.
DEF INPUT PARAMETER cbuff-qty       AS DECIMAL.
DEF INPUT PARAMETER selected-date   AS DATE.
DEF INPUT PARAMETER user-init       AS CHAR.
DEF INPUT PARAMETER cbuff-price     AS DECIMAL.
DEF INPUT PARAMETER cbuff-lief-nr   AS INT.
DEF INPUT PARAMETER cbuff-approved  AS LOGICAL.
DEF INPUT PARAMETER cbuff-remark    AS CHAR.
DEF INPUT PARAMETER curr-select     AS CHAR.
DEF INPUT PARAMETER dml-no          AS CHAR.
DEF INPUT PARAMETER counter         AS INT.

DEFINE BUFFER breslin FOR reslin-queasy.
DEFINE BUFFER bdml-artdep FOR dml-artdep.

IF curr-dept = 0 THEN 
DO: 
    FIND FIRST dml-art WHERE dml-art.artnr = cbuff-artnr
        AND dml-art.datum = selected-date 
        AND ENTRY(2, dml-art.chginit, ";") EQ dml-no EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE dml-art THEN 
    DO: 
        CREATE dml-art. 
        ASSIGN
          dml-art.artnr    = cbuff-artnr
          dml-art.datum    = selected-date 
          dml-art.userinit = user-init
          dml-art.chginit  = user-init + ";" + dml-no.
    END.
    ASSIGN
        dml-art.anzahl                  = cbuff-qty
        dml-art.einzelpreis             = cbuff-price
        dml-art.userinit                = ENTRY(1, dml-art.userinit, ";").
    IF NUM-ENTRIES(dml-art.chginit, ";") GT 1 THEN
        ENTRY(1, dml-art.chginit, ";") = user-init.
    
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
        IF NUM-ENTRIES(dml-art.chginit, ";") GT 1 THEN
            ENTRY(1, dml-art.chginit, ";") = ENTRY(1, dml-art.chginit, ";") + "!".
        ELSE
            dml-art.chginit = dml-art.chginit + "!".
    
        FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = 0 
            AND queasy.date1 = dml-art.datum AND queasy.logi1 = YES 
            /*AND queasy.logi2 = NO*/
            AND queasy.number3 = 0 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY      = 254 
                queasy.number1  = 0 
                queasy.date1    = dml-art.datum 
                queasy.logi1    = YES 
                queasy.logi2    = NO
                queasy.number3  = 0.  
        END.
    END.
    FIND CURRENT dml-art NO-LOCK. 
END. 
ELSE 
DO: 
    IF curr-select EQ "new" THEN
    DO:
        IF counter GT 1 THEN
        DO:
            FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
                AND INT(ENTRY(1,reslin-queasy.char1,";")) EQ cbuff-artnr
                AND reslin-queasy.date1 EQ selected-date
                AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept 
                AND reslin-queasy.number2 EQ counter NO-LOCK NO-ERROR.
            IF NOT AVAILABLE reslin-queasy THEN
            DO:
                CREATE reslin-queasy.
                ASSIGN
                    reslin-queasy.KEY       = "DML"
                    reslin-queasy.char1     = STRING(cbuff-artnr) + ";" + STRING(curr-dept) + ";" + cbuff-remark
                    reslin-queasy.char2     = user-init
                    reslin-queasy.char3     = user-init + ";" + dml-no
                    reslin-queasy.deci2     = cbuff-qty
                    reslin-queasy.number2   = counter
                    reslin-queasy.deci1     = cbuff-price
                    reslin-queasy.date1     = selected-date.
                IF cbuff-lief-nr GT 0 THEN 
                    ASSIGN reslin-queasy.char2 = reslin-queasy.char2 + ";" + STRING(cbuff-lief-nr).
            
                IF cbuff-approved THEN
                DO:
                    IF NUM-ENTRIES(reslin-queasy.char3, ";") GT 1 THEN
                    DO:
                        REPLACE((ENTRY(1, reslin-queasy.char3, ";")), "", "!").
                        /*ENTRY(1, reslin-queasy.char3, ";") = ENTRY(1, reslin-queasy.char3, ";") + "!".*/
                    END.
                    ELSE
                    DO:
                        reslin-queasy.char3 = reslin-queasy.char3 + "!".
                    END.
                        
                    FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = INT(ENTRY(2, reslin-queasy.char1, ";"))
                          AND queasy.date1 = reslin-queasy.date1 AND queasy.logi1 = YES 
                          /*AND queasy.logi2 = NO*/
                          AND queasy.number3  = counter NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE queasy THEN DO:
                          CREATE queasy.
                          ASSIGN 
                              queasy.KEY      = 254 
                              queasy.number1  = INT(ENTRY(2, reslin-queasy.char1, ";"))
                              queasy.date1    = reslin-queasy.date1
                              queasy.logi1    = YES 
                              queasy.logi2    = NO
                              queasy.number3  = counter
                           .  
                    END.
                END.
            END.
        END.        
        ELSE DO:
            FIND FIRST dml-artdep WHERE dml-artdep.artnr EQ cbuff-artnr
                AND dml-artdep.datum EQ selected-date
                AND dml-artdep.departement EQ curr-dept EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE dml-artdep THEN
            DO:
                CREATE dml-artdep. 
                ASSIGN
                    dml-artdep.artnr       = cbuff-artnr 
                    dml-artdep.datum       = selected-date 
                    dml-artdep.departement = curr-dept 
                    dml-artdep.userinit    = user-init
                    dml-artdep.anzahl      = cbuff-qty
                    dml-artdep.einzelpreis = cbuff-price
                    dml-artdep.chginit     = user-init + ";" + dml-no.
            
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
                        queasy.number3  = counter
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
                    ASSIGN dml-artdep.userinit = dml-artdep.userinit + ";" + STRING(cbuff-lief-nr). 
                IF cbuff-approved THEN
                DO:
                    IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 1 THEN
                        ENTRY(1, dml-artdep.chginit, ";") = ENTRY(1, dml-artdep.chginit, ";") + "!".
                    ELSE
                        dml-artdep.chginit = dml-artdep.chginit + "!".
                    FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = dml-artdep.departement 
                          AND queasy.date1 = dml-artdep.datum AND queasy.logi1 = YES 
                          /*AND queasy.logi2 = NO*/
                          AND queasy.number3  = 0 NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE queasy THEN DO:
                          CREATE queasy.
                          ASSIGN 
                              queasy.KEY      = 254 
                              queasy.number1  = dml-artdep.departement
                              queasy.date1    = dml-artdep.datum 
                              queasy.logi1    = YES 
                              queasy.logi2    = NO
                              queasy.number3  = 0
                           .  
                    END.
                END.
                FIND CURRENT dml-artdep NO-LOCK.    
            END.
        END.
    END.
    ELSE DO:
        FIND FIRST breslin WHERE breslin.KEY EQ "DML"
            AND ENTRY(2, breslin.char3, ";") EQ dml-no NO-LOCK NO-ERROR.
        IF AVAILABLE breslin THEN
        DO:
            FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
                AND INT(ENTRY(1,reslin-queasy.char1,";")) EQ cbuff-artnr
                AND reslin-queasy.date1 EQ selected-date
                AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept
                AND ENTRY(2, reslin-queasy.char3, ";") EQ dml-no EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE reslin-queasy THEN
            DO:
                IF cbuff-qty GT 0 THEN
                DO:
                    ASSIGN
                        reslin-queasy.deci2                = cbuff-qty
                        reslin-queasy.deci1                = cbuff-price
                        reslin-queasy.char2                = ENTRY(1, reslin-queasy.char2, ";")
                        ENTRY(1, reslin-queasy.char3, ";") = user-init.
                    
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
                    
                    IF cbuff-lief-nr GT 0 THEN 
                        ASSIGN reslin-queasy.char2 = reslin-queasy.char2 + ";" + STRING(cbuff-lief-nr). 
                    IF cbuff-approved THEN DO: 
                        IF NUM-ENTRIES(reslin-queasy.char3, ";") GT 1 THEN
                        DO:
                            /*REPLACE((ENTRY(1, reslin-queasy.char3, ";")), "", "!").*/
                            ENTRY(1, reslin-queasy.char3, ";") = ENTRY(1, reslin-queasy.char3, ";") + "!".
                        END.
                        ELSE
                        DO:
                            reslin-queasy.char3 = reslin-queasy.char3 + "!".
                        END.
                    
                    
                        FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = INT(ENTRY(2,reslin-queasy.char1,";")) 
                              AND queasy.date1 = reslin-queasy.date1 AND queasy.logi1 = YES 
                              /*AND queasy.logi2 = NO*/
                              AND queasy.number3 = counter NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE queasy THEN DO:
                              CREATE queasy.
                              ASSIGN 
                                  queasy.KEY      = 254 
                                  queasy.number1  = INT(ENTRY(2,reslin-queasy.char1,";"))
                                  queasy.date1    = reslin-queasy.date1
                                  queasy.logi1    = YES 
                                  queasy.logi2    = NO
                                  queasy.number3  = reslin-queasy.number2
                               .  
                        END.
                    END.
                    FIND CURRENT reslin-queasy NO-LOCK.
                    RELEASE reslin-queasy.
                END.
                ELSE
                DO:
                    DELETE reslin-queasy.
                    RELEASE reslin-queasy.
                END.
            END.
            ELSE
            DO:
                CREATE reslin-queasy.
                ASSIGN
                    reslin-queasy.KEY       = "DML"
                    reslin-queasy.char1     = STRING(cbuff-artnr) + ";" + STRING(curr-dept) + ";" + cbuff-remark
                    reslin-queasy.char2     = user-init
                    reslin-queasy.char3     = user-init + ";" + dml-no
                    reslin-queasy.deci2     = cbuff-qty
                    reslin-queasy.number2   = counter
                    reslin-queasy.deci1     = cbuff-price
                    reslin-queasy.date1     = selected-date.
                IF cbuff-lief-nr GT 0 THEN 
                    ASSIGN reslin-queasy.char2 = reslin-queasy.char2 + ";" + STRING(cbuff-lief-nr).

                IF cbuff-approved THEN
                DO:
                    IF NUM-ENTRIES(reslin-queasy.char3, ";") GT 1 THEN
                    DO:
                        /*REPLACE((ENTRY(1, reslin-queasy.char3, ";")), "", "!").*/
                        ENTRY(1, reslin-queasy.char3, ";") = ENTRY(1, reslin-queasy.char3, ";") + "!".
                    END.
                    ELSE
                    DO:
                        reslin-queasy.char3 = reslin-queasy.char3 + "!".
                    END.
                        
                    FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = INT(ENTRY(2, reslin-queasy.char1, ";"))
                          AND queasy.date1 = reslin-queasy.date1 AND queasy.logi1 = YES 
                          /*AND queasy.logi2 = NO*/
                          AND queasy.number3 = counter NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE queasy THEN DO:
                          CREATE queasy.
                          ASSIGN 
                              queasy.KEY      = 254 
                              queasy.number1  = INT(ENTRY(2, reslin-queasy.char1, ";"))
                              queasy.date1    = reslin-queasy.date1
                              queasy.logi1    = YES 
                              queasy.logi2    = NO
                              queasy.number3  = counter
                           .  
                    END.
                END.
            END.
        END.            
        ELSE
        DO:
            FIND FIRST dml-artdep WHERE dml-artdep.artnr EQ cbuff-artnr
                AND dml-artdep.datum EQ selected-date
                AND dml-artdep.departement EQ curr-dept EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE dml-artdep THEN
            DO:
                IF cbuff-qty GT 0 THEN
                DO:
                    ASSIGN
                        dml-artdep.anzahl                 = cbuff-qty
                        dml-artdep.einzelpreis            = cbuff-price
                        dml-artdep.userinit               = ENTRY(1, dml-artdep.userinit, ";")
                        ENTRY(1, dml-artdep.chginit, ";") = user-init.
                    
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
                    
                    IF cbuff-lief-nr GT 0 THEN 
                        ASSIGN dml-artdep.userinit = dml-artdep.userinit + ";" + STRING(cbuff-lief-nr). 
                    IF cbuff-approved THEN DO: 
                        /*ENTRY(1, dml-artdep.chginit, ";") = ENTRY(1, dml-artdep.chginit, ";") + "!".*/
                        IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 1 THEN
                            ENTRY(1, dml-artdep.chginit, ";") = ENTRY(1, dml-artdep.chginit, ";") + "!".
                        ELSE
                            dml-artdep.chginit = dml-artdep.chginit + "!".
                    
                        FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = dml-artdep.departement 
                              AND queasy.date1 = dml-artdep.datum AND queasy.logi1 = YES 
                              /*AND queasy.logi2 = NO*/
                              AND queasy.number3 = 0 NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE queasy THEN DO:
                              CREATE queasy.
                              ASSIGN 
                                  queasy.KEY      = 254 
                                  queasy.number1  = dml-artdep.departement
                                  queasy.date1    = dml-artdep.datum 
                                  queasy.logi1    = YES 
                                  queasy.logi2    = NO
                                  queasy.number3  = 0
                               .  
                        END.
                    END.
                    FIND CURRENT dml-artdep NO-LOCK.
                    RELEASE dml-artdep.
                END.
                ELSE
                DO:
                    DELETE dml-artdep.
                    RELEASE dml-artdep.
                END.
            END.
            ELSE
            DO:
                CREATE dml-artdep.
                ASSIGN
                    dml-artdep.artnr        = cbuff-artnr
                    dml-artdep.datum        = selected-date
                    dml-artdep.departement  = curr-dept
                    dml-artdep.userinit     = user-init
                    dml-artdep.chginit      = user-init + ";" + dml-no
                    dml-artdep.anzahl       = cbuff-qty
                    dml-artdep.einzelpreis  = cbuff-price.

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
                    ASSIGN dml-artdep.userinit = dml-artdep.userinit + ";" + STRING(cbuff-lief-nr). 
                IF cbuff-approved THEN DO: 
                    /*ENTRY(1, dml-artdep.chginit, ";") = ENTRY(1, dml-artdep.chginit, ";") + "!".*/
                    IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 1 THEN
                        ENTRY(1, dml-artdep.chginit, ";") = ENTRY(1, dml-artdep.chginit, ";") + "!".
                    ELSE
                        dml-artdep.chginit = dml-artdep.chginit + "!".
            
                    FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = dml-artdep.departement 
                          AND queasy.date1 = dml-artdep.datum AND queasy.logi1 = YES 
                          /*AND queasy.logi2 = NO*/
                          AND queasy.number3 = 0 NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE queasy THEN DO:
                          CREATE queasy.
                          ASSIGN 
                              queasy.KEY      = 254 
                              queasy.number1  = dml-artdep.departement
                              queasy.date1    = dml-artdep.datum 
                              queasy.logi1    = YES 
                              queasy.logi2    = NO
                              queasy.number3  = 0
                           .  
                    END.
                END.
            END.
        END.
    END.
    /*FIND FIRST dml-artdep WHERE dml-artdep.artnr = cbuff-artnr 
        AND dml-artdep.datum = selected-date 
        AND dml-artdep.departement = curr-dept EXCLUSIVE-LOCK NO-ERROR. 
    
    IF NOT AVAILABLE dml-artdep THEN 
    DO: 
        CREATE dml-artdep. 
        ASSIGN
            dml-artdep.artnr       = cbuff-artnr 
            dml-artdep.datum       = selected-date 
            dml-artdep.departement = curr-dept 
            dml-artdep.userinit    = user-init. 
    END.
    ASSIGN
        dml-artdep.anzahl      = cbuff-qty
        dml-artdep.einzelpreis = cbuff-price 
        dml-artdep.userinit    = ENTRY(1, dml-artdep.userinit, ";")
        dml-artdep.chginit     = user-init. 
    
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
    ASSIGN dml-artdep.userinit = dml-artdep.userinit + ";" + STRING(cbuff-lief-nr). 
    IF cbuff-approved THEN DO: 
        dml-artdep.chginit = dml-artdep.chginit + "!".
    
        FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = dml-artdep.departement 
              AND queasy.date1 = dml-artdep.datum AND queasy.logi1 = YES 
              AND queasy.logi2 = NO NO-LOCK NO-ERROR.
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
    FIND CURRENT dml-artdep NO-LOCK. */
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
