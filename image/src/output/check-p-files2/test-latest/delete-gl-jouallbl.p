/* Created by Michael @ 24/09/2018 for Harris Riverview Bali request - ticket no B213E6 */
DEFINE INPUT PARAMETER refno    AS CHAR FORMAT "x(16)".
/* change from integer to charactr by damen 16/02/23 3BB36A */
DEFINE INPUT PARAMETER idnr     AS CHARACTER.
DEFINE OUTPUT PARAMETER flag    AS LOGICAL.
DEFINE OUTPUT PARAMETER msg     AS CHARACTER.

DEFINE VARIABLE fb-close AS DATE NO-UNDO.
DEFINE VARIABLE mat-close AS DATE NO-UNDO.
DEFINE VARIABLE gl-close AS DATE NO-UNDO.
DEFINE VARIABLE tdate AS CHARACTER NO-UNDO.
DEFINE VARIABLE iday AS INTEGER NO-UNDO.
DEFINE VARIABLE imon AS INTEGER NO-UNDO.
DEFINE VARIABLE iyear AS INTEGER NO-UNDO.

DEF TEMP-TABLE t-lop
    FIELD lscheinnr AS CHARACTER FORMAT "x(24)".

FIND FIRST htparam WHERE htparam.paramnr EQ 221 NO-LOCK NO-ERROR.
ASSIGN fb-close = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr EQ 224 NO-LOCK NO-ERROR.
ASSIGN mat-close = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr EQ 597 NO-LOCK NO-ERROR.
ASSIGN gl-close = htparam.fdate.

FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno EQ refno NO-LOCK NO-ERROR.
IF AVAILABLE gl-jouhdr THEN
DO:
    /* Modify by Michael @ 13/02/2019 for adding validation can not delete if journal has been closed - ticket no 5C7394 */
    IF gl-jouhdr.activeflag EQ 0 THEN
    DO:
        IF gl-jouhdr.jtype EQ 3 OR gl-jouhdr.jtype EQ 6 THEN
        DO:
            IF gl-jouhdr.datum GE DATE(MONTH(fb-close), 1, YEAR(fb-close)) OR gl-jouhdr.datum GE DATE(MONTH(mat-close), 1, YEAR(mat-close)) THEN
            DO:
                FOR EACH gl-journal WHERE gl-journal.jnr EQ gl-jouhdr.jnr:
                    DELETE gl-journal.
                END.
                FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK.
                DELETE gl-jouhdr.
                ASSIGN flag = YES.
            END.
            ELSE
            DO:
                ASSIGN flag = NO.
                msg = "GL has been closed. Can not delete journal".
                RETURN NO-APPLY.
            END.
        END.
        ELSE
        DO:
            IF gl-jouhdr.datum GE DATE(MONTH(gl-close), 1, YEAR(gl-close)) THEN
            DO:
                FOR EACH gl-journal WHERE gl-journal.jnr EQ gl-jouhdr.jnr:
                    DELETE gl-journal.
                END.
                FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK.
                DELETE gl-jouhdr.
                ASSIGN flag = YES.
            END.
            ELSE
            DO:
                ASSIGN flag = NO.
                msg = "GL has been closed. Can not delete journal".
                RETURN NO-APPLY.
            END.
        END.
    END.
    ELSE
    DO:
        ASSIGN flag = NO
        msg = "Closed journal can not be deleted".
        RETURN NO-APPLY.
    END.
    /* End of modify */
END.
/* change from bediener.nr to userinit by damen 16/02/23 3BB36A */
FIND FIRST bediener WHERE bediener.userinit EQ idnr NO-LOCK NO-ERROR.

/* Malik Serverless */
IF AVAILABLE bediener THEN
DO:
    CREATE res-history. 
    ASSIGN 
        /* change from idnr to bediener.nr by damen 16/02/23 3BB36A */
        res-history.nr = bediener.nr 
        res-history.resnr = 0 
        res-history.reslinnr = 0 
        res-history.datum = TODAY 
        res-history.zeit = TIME 
        res-history.aenderung = "Journal Transaction & Detail Delete - Reference no " + refno + " by " + bediener.username
        res-history.betriebsnr = bediener.nr
        res-history.action = "JournalTransactionDelete". 
    RELEASE res-history.
END.
/* END Malik */

