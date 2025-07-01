DEFINE TEMP-TABLE op-list LIKE l-op 
  FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
  FIELD anzahl0  AS DECIMAL
  FIELD fibu     AS CHAR
  FIELD fibu10   AS CHAR
  FIELD s-recid  AS INTEGER
  FIELD einheit  AS CHAR FORMAT "x(3)".

/* Oscar (14/03/25) - 3E510E - change payload format and add new field sr-remark */
DEFINE TEMP-TABLE payload-list
  FIELD s-recid      AS INTEGER
  FIELD user-init    AS CHARACTER
  FIELD t-lschein    AS CHARACTER
  FIELD release-flag AS LOGICAL
  FIELD transfered   AS LOGICAL
  FIELD show-price   AS LOGICAL
  FIELD sr-remark     AS CHARACTER
.

/* Oscar (14/03/25) - 3E510E - change response format */
DEFINE TEMP-TABLE response-list
  FIELD s-recid  AS INTEGER
  FIELD changed  AS LOGICAL
  FIELD approved AS LOGICAL
  FIELD flag     AS INTEGER
.

DEF INPUT  PARAMETER TABLE FOR payload-list.
DEF INPUT  PARAMETER TABLE FOR op-list.
DEF OUTPUT PARAMETER TABLE FOR response-list.

DEFINE VARIABLE s-recid      AS INT.
DEFINE VARIABLE user-init    AS CHAR.
DEFINE VARIABLE t-lschein    AS CHAR.
DEFINE VARIABLE release-flag AS LOGICAL.
DEFINE VARIABLE transfered   AS LOGICAL.
DEFINE VARIABLE show-price   AS LOGICAL.
DEFINE VARIABLE sr-remark    AS CHARACTER.
DEFINE VARIABLE changed      AS LOGICAL.
DEFINE VARIABLE approved     AS LOGICAL.
DEFINE VARIABLE flag         AS INT INIT 0.

DEFINE VARIABLE transfer-date AS DATE.

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        s-recid      = payload-list.s-recid     
        user-init    = payload-list.user-init   
        t-lschein    = payload-list.t-lschein   
        release-flag = payload-list.release-flag
        transfered   = payload-list.transfered  
        show-price   = payload-list.show-price  
        sr-remark    = payload-list.sr-remark
    .

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    IF NOT transfered AND show-price THEN
    DO:
        FIND FIRST op-list NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE op-list:
            FIND FIRST gl-acct WHERE gl-acct.fibukonto = op-list.fibu
                NO-LOCK NO-ERROR.
            IF NOT AVAILABLE gl-acct THEN
            DO:
                flag = 1.
                RETURN NO-APPLY.
            END.

            /*geral 7E68C2*/
            IF AVAILABLE gl-acct THEN
            DO:
                FIND FIRST parameters WHERE progname = "CostCenter" 
                    AND section = "Alloc" AND varname GT "" 
                    AND parameters.vstring = gl-acct.fibukonto NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE parameters THEN
                DO:
                    flag = 2.
                    RETURN NO-APPLY.    
                END.
            END.

            IF s-recid = 0 THEN s-recid = RECID(op-list).
            ELSE
            DO:     
                IF RECID(op-list) = s-recid THEN LEAVE.
                ELSE s-recid = RECID(op-list).
            END.
            FIND NEXT op-list NO-LOCK NO-ERROR.
        END.
    END.
    ELSE IF NOT transfered AND NOT show-price THEN
    DO:
        FIND FIRST op-list NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE op-list:
            FIND FIRST gl-acct WHERE gl-acct.fibukonto = op-list.fibu
                NO-LOCK NO-ERROR.
            IF NOT AVAILABLE gl-acct THEN
            DO:
                flag = 1.
                RETURN NO-APPLY.
            END.
            /*geral 7E68C2*/
            IF AVAILABLE gl-acct THEN
            DO:
                FIND FIRST parameters WHERE progname = "CostCenter" 
                    AND section = "Alloc" AND varname GT "" 
                    AND parameters.vstring = gl-acct.fibukonto NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE parameters THEN
                DO:
                    flag = 2.
                    RETURN NO-APPLY.    
                END.
            END.

            IF s-recid = 0 THEN s-recid = RECID(op-list).
            ELSE
            DO:     
                IF RECID(op-list) = s-recid THEN LEAVE.
                ELSE s-recid = RECID(op-list).
            END.
            FIND NEXT op-list NO-LOCK NO-ERROR.
        END.
    END.

    FOR EACH op-list WHERE op-list.anzahl NE op-list.anzahl0
        OR op-list.fibu NE op-list.fibu10 :
        /* Rulita 140225 | Fixing serverless issue git 599 */
        FIND FIRST l-op WHERE RECID(l-op) = op-list.s-recid NO-LOCK NO-ERROR.
        IF AVAILABLE l-op THEN
        DO:
            FIND CURRENT l-op EXCLUSIVE-LOCK.
            ASSIGN
                l-op.anzahl      = op-list.anzahl
                l-op.stornogrund = op-list.fibu
                l-op.warenwert   = op-list.warenwert /*IT 150513*/
                changed          = YES
            .
            IF AVAILABLE bediener THEN l-op.fuellflag = bediener.nr.

            FIND CURRENT l-op NO-LOCK.
            RELEASE l-op.
        END.
        /* End Rulita */
    END.

    FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr EQ t-lschein NO-LOCK NO-ERROR.
    IF AVAILABLE l-ophdr THEN
    DO:
        transfer-date = l-ophdr.datum.
    END.

    /* Oscar (14/03/25) - 3E510E - save field sr-remark */
    FIND FIRST queasy WHERE queasy.KEY EQ 343 
        AND queasy.char1 EQ t-lschein NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        queasy.char2 = sr-remark.

        FIND CURRENT queasy NO-LOCK.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 343
            queasy.char1 = t-lschein
            queasy.char2 = sr-remark
            queasy.date1 = transfer-date
        .
    END.

    IF release-flag THEN
    DO:
        FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "REQ"
            AND l-ophdr.lscheinnr = t-lschein
            AND l-ophdr.docu-nr = t-lschein EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE l-ophdr THEN
        DO:
            IF AVAILABLE bediener THEN l-ophdr.betriebsnr = bediener.nr.

            FIND CURRENT l-ophdr NO-LOCK.
            RELEASE l-ophdr.
            approved = YES.
        END.
    END.

    CREATE response-list.
    ASSIGN
        response-list.s-recid  = s-recid 
        response-list.changed  = changed 
        response-list.approved = approved
        response-list.flag     = flag    
    .
END.


