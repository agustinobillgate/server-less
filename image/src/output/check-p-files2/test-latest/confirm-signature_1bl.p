DEFINE INPUT PARAMETER app-id       AS CHAR.
DEFINE INPUT PARAMETER app-no       AS INT.
DEFINE INPUT PARAMETER docu-nr      AS CHAR.
DEFINE INPUT PARAMETER user-init    AS CHAR.
DEFINE INPUT PARAMETER sign-id      AS INT.
/*NAUFAL - add flag for bug esign not deleted after uncheck*/
DEFINE INPUT PARAMETER confirmsign-flag AS LOGICAL.
DEFINE INPUT PARAMETER flag-type    AS CHAR.

IF confirmsign-flag EQ YES THEN
DO TRANSACTION:
    IF flag-type EQ "PR" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 227 AND queasy.char1 EQ docu-nr AND queasy.number1 EQ app-no EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY = 227
                queasy.char1 = docu-nr 
                queasy.char2 = user-init
                queasy.char3 = app-id
                queasy.number1 = app-no
                queasy.number2 = sign-id.
        
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            CREATE res-history. 
            ASSIGN 
              res-history.nr    = bediener.nr 
              res-history.datum = TODAY 
              res-history.zeit  = TIME 
              res-history.aenderung = "Using E-Signature For PR: " + docu-nr + "|Approve No: " + STRING(app-no) + "|" + app-id
              res-history.action = "E-Signature"
            . 
            FIND CURRENT bediener NO-LOCK.
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
        END.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN 
                queasy.char2 = user-init
                queasy.char3 = app-id
                queasy.number1 = app-no
                queasy.number2 = sign-id
                .
        
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            CREATE res-history. 
            ASSIGN 
              res-history.nr    = bediener.nr 
              res-history.datum = TODAY 
              res-history.zeit  = TIME 
              res-history.aenderung =  "Change E-Signature For PR: " + docu-nr + "|Approve No: " + STRING(app-no) + "|" + app-id
              res-history.action = "E-Signature"
            . 
            FIND CURRENT bediener NO-LOCK.
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
        END.
    END.
    IF flag-type EQ "PO" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ docu-nr AND queasy.number1 EQ app-no EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY = 245
                queasy.char1 = docu-nr 
                queasy.char2 = user-init
                queasy.char3 = app-id
                queasy.number1 = app-no
                queasy.number2 = sign-id.
        
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            CREATE res-history. 
            ASSIGN 
              res-history.nr    = bediener.nr 
              res-history.datum = TODAY 
              res-history.zeit  = TIME 
              res-history.aenderung = "Using E-Signature For PO: " + docu-nr + "|Approve No: " + STRING(app-no) + "|" + app-id
              res-history.action = "E-Signature"
            . 
            FIND CURRENT bediener NO-LOCK.
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
        END.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN 
                queasy.char2 = user-init
                queasy.char3 = app-id
                queasy.number1 = app-no
                queasy.number2 = sign-id
                .
        
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            CREATE res-history. 
            ASSIGN 
              res-history.nr    = bediener.nr 
              res-history.datum = TODAY 
              res-history.zeit  = TIME 
              res-history.aenderung =  "Change E-Signature For PO: " + docu-nr + "|Approve No: " + STRING(app-no) + "|" + app-id
              res-history.action = "E-Signature"
            . 
            FIND CURRENT bediener NO-LOCK.
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
        END.
    END.
END.
ELSE IF confirmsign-flag EQ NO THEN
DO TRANSACTION:
    IF flag-type EQ "PR" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 227 AND queasy.char1 EQ docu-nr AND queasy.number1 EQ app-no EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.       
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
                CREATE res-history. 
                ASSIGN 
                  res-history.nr    = bediener.nr 
                  res-history.datum = TODAY 
                  res-history.zeit  = TIME 
                  res-history.aenderung =  "Cancel E-Signature For PR: " + docu-nr + "|Approve No: " + STRING(app-no) + "|" + app-id
                  res-history.action = "E-Signature"
                . 
            FIND CURRENT bediener NO-LOCK.
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history.
        END.
    END.
    IF flag-type EQ "PO" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ docu-nr AND queasy.number1 EQ app-no EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.       
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
                CREATE res-history. 
                ASSIGN 
                  res-history.nr    = bediener.nr 
                  res-history.datum = TODAY 
                  res-history.zeit  = TIME 
                  res-history.aenderung =  "Cancel E-Signature For PO: " + docu-nr + "|Approve No: " + STRING(app-no) + "|" + app-id
                  res-history.action = "E-Signature"
                . 
            FIND CURRENT bediener NO-LOCK.
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history.
        END.
    END.
END.
