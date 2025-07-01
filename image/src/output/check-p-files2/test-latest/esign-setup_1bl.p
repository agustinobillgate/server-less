DEFINE TEMP-TABLE esign-list NO-UNDO
    FIELD sign-nr       AS INT FORMAT ">>>" LABEL "No"
    FIELD sign-name     AS CHARACTER FORMAT "x(35)" LABEL "Name"
    FIELD sign-img      AS BLOB 
    FIELD sign-use-for  AS CHARACTER FORMAT "x(20)" LABEL "Use For"
    FIELD sign-position AS CHARACTER FORMAT "x(23)" LABEL "Position"
    FIELD sign-userinit AS CHARACTER FORMAT "x(15)" LABEL "Username"
    FIELD sign-id       AS INTEGER FORMAT "->>>>>>>>>>"
    FIELD sign-select   AS LOGICAL
    FIELD sign-pass     AS CHAR
    FIELD sign-pr       AS LOGICAL  LABEL "PR Approval"
    FIELD sign-po       AS LOGICAL  LABEL "PO Approval"
    .

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR esign-list.

IF case-type EQ 0 THEN /*load*/
DO :
    FOR EACH guestbook WHERE guestbook.gastnr GE -271150
        AND guestbook.gastnr LE -271080 NO-LOCK BY guestbook.reserve-int[1]:
        CREATE esign-list.
        ASSIGN 
            esign-list.sign-nr       = INT(ENTRY(1,guestbook.infostr,"|"))
            esign-list.sign-name     = ENTRY(2,guestbook.infostr,"|")
            esign-list.sign-img      = guestbook.imagefile
            esign-list.sign-use-for  = ENTRY(3,guestbook.infostr,"|")
            esign-list.sign-position = ENTRY(4,guestbook.infostr,"|")
            esign-list.sign-userinit = guestbook.userinit
            esign-list.sign-id       = guestbook.gastnr
            esign-list.sign-pass     = guestbook.reserve-char[1]
            esign-list.sign-pr       = guestbook.reserve-logic[1]
            esign-list.sign-po       = guestbook.reserve-logic[2]
            .
    END.
    FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
    CREATE res-history. 
    ASSIGN 
        res-history.nr    = bediener.nr 
        res-history.datum = TODAY 
        res-history.zeit  = TIME 
        res-history.aenderung = "VIEWING DATA E-Signature"
        res-history.action = "E-Signature Setup"
    . 
    FIND CURRENT bediener NO-LOCK.
    FIND CURRENT res-history NO-LOCK. 
    RELEASE res-history. 
    RELEASE bediener.
END.
ELSE IF case-type EQ 1 THEN  /*add or modify*/
DO:
    FOR EACH esign-list:
        FIND FIRST guestbook WHERE guestbook.gastnr EQ esign-list.sign-id NO-LOCK NO-ERROR.
        IF AVAILABLE guestbook THEN
        DO:
            FIND CURRENT guestbook EXCLUSIVE-LOCK.
            ASSIGN 
                guestbook.infostr = STRING(esign-list.sign-nr) + "|" + 
                                    esign-list.sign-name + "|" + 
                                    esign-list.sign-use-for + "|" + 
                                    esign-list.sign-position
                guestbook.imagefile = esign-list.sign-img
                guestbook.userinit  = esign-list.sign-userinit
                guestbook.reserve-char[1]   = esign-list.sign-pass
                guestbook.reserve-logic[1]  = esign-list.sign-pr
                guestbook.reserve-logic[2]  = esign-list.sign-po
                .

            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            CREATE res-history. 
            ASSIGN 
                res-history.nr    = bediener.nr 
                res-history.datum = TODAY 
                res-history.zeit  = TIME 
                res-history.aenderung = "MODIFY E-Sign: ID Name " + esign-list.sign-name
                res-history.action = "E-Signature Setup"
            . 
            FIND CURRENT guestbook NO-LOCK.
            FIND CURRENT bediener NO-LOCK.
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
            RELEASE guestbook.
            RELEASE bediener.
        END.
        ELSE 
        DO:
            DEFINE BUFFER gbook FOR guestbook.
            DEFINE VARIABLE booknr AS INT FORMAT "->>>>>>>".


            FIND FIRST gbook WHERE gbook.gastnr GE -271150 AND gbook.gastnr LE -271080 NO-LOCK NO-ERROR.
            IF AVAILABLE gbook THEN
            DO:
                FOR EACH guestbook WHERE guestbook.gastnr GE -271150 AND guestbook.gastnr LE -271080 NO-LOCK BY guestbook.gastnr:
                    booknr = guestbook.gastnr - 1.
                    LEAVE.
                END.
            END.
            ELSE booknr =  - 271080.
            RELEASE gbook.

            CREATE guestbook.
            ASSIGN 
                guestbook.gastnr = booknr
                guestbook.reserve-int[1] = esign-list.sign-nr
                guestbook.infostr = STRING(esign-list.sign-nr) + "|" + 
                                    esign-list.sign-name + "|" + 
                                    esign-list.sign-use-for + "|" + 
                                    esign-list.sign-position
                guestbook.imagefile = esign-list.sign-img
                guestbook.userinit  = esign-list.sign-userinit
                guestbook.reserve-char[1]   = esign-list.sign-pass
                guestbook.reserve-logic[1]  = esign-list.sign-pr
                guestbook.reserve-logic[2]  = esign-list.sign-po
                esign-list.sign-id = booknr
                .

            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            CREATE res-history. 
            ASSIGN 
                res-history.nr    = bediener.nr 
                res-history.datum = TODAY 
                res-history.zeit  = TIME 
                res-history.aenderung = "ADD E-Sign: ID Name " + esign-list.sign-name
                res-history.action = "E-Signature Setup"
            . 
            FIND CURRENT guestbook NO-LOCK.
            FIND CURRENT bediener NO-LOCK.
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
            RELEASE guestbook.
            RELEASE bediener.
        END.
    END.
END.
ELSE IF case-type EQ 2 THEN /*delete*/
DO:
    FIND FIRST esign-list WHERE esign-list.sign-select EQ YES NO-LOCK NO-ERROR.
    IF AVAILABLE esign-list THEN
    DO:
        FIND FIRST guestbook WHERE guestbook.gastnr EQ esign-list.sign-id NO-LOCK NO-ERROR.
        IF AVAILABLE guestbook THEN
        DO:
            FIND CURRENT guestbook EXCLUSIVE-LOCK.
            DELETE guestbook.
    
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            CREATE res-history. 
            ASSIGN 
                res-history.nr    = bediener.nr 
                res-history.datum = TODAY 
                res-history.zeit  = TIME 
                res-history.aenderung = "DELETE E-Sign: ID Name " + esign-list.sign-name
                res-history.action = "E-Signature Setup"
            . 
            FIND CURRENT bediener NO-LOCK.
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
            RELEASE guestbook.
            RELEASE bediener.
        END.        
    END.
END.

