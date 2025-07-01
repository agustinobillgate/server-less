
DEFINE INPUT PARAMETER rec-id AS INTEGER.
DEFINE INPUT PARAMETER maintask-nr AS INTEGER.
DEFINE INPUT PARAMETER sub-code AS CHARACTER.
DEFINE INPUT PARAMETER maintask-nr2 AS INTEGER.
DEFINE INPUT PARAMETER sub-code2 AS CHARACTER.
DEFINE INPUT PARAMETER bezeich AS CHARACTER.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

/*
DEFINE VARIABLE rec-id AS INTEGER INIT 958974.
DEFINE VARIABLE maintask-nr AS INTEGER INIT 1.
DEFINE VARIABLE sub-code AS CHARACTER INIT "08001001".
DEFINE VARIABLE maintask-nr2 AS INTEGER INIT 1.
DEFINE VARIABLE sub-code2 AS CHARACTER INIT "08001004".
DEFINE VARIABLE bezeich AS CHARACTER INIT "TV Banyak Semut dan Blank".
*/

DEFINE BUFFER buf-eg-request FOR eg-request.
/*
FIND FIRST eg-request WHERE eg-request.maintask = maintask-nr
    AND eg-request.sub-task = sub-code NO-LOCK NO-ERROR.
IF NOT AVAILABLE eg-request THEN success-flag = NO.
ELSE
DO:
    /*Delete Selected Merge Problem*/
    FIND FIRST eg-subtask WHERE RECID(eg-subtask) = rec-id NO-LOCK NO-ERROR. 
    IF AVAILABLE eg-subtask THEN
    DO:
        FIND CURRENT eg-subtask EXCLUSIVE-LOCK.  
        DELETE eg-subtask.  
        RELEASE eg-subtask.
        success-flag = YES.
    END.
END.
*/
/*Replace problem at Work Order with problem merge*/
FIND FIRST eg-subtask WHERE RECID(eg-subtask) = rec-id NO-LOCK NO-ERROR. 
IF NOT AVAILABLE eg-subtask THEN success-flag = NO.
ELSE
DO:
    FOR EACH eg-request NO-LOCK: 
        FIND FIRST buf-eg-request WHERE buf-eg-request.reqnr = eg-request.reqnr
            AND buf-eg-request.maintask = maintask-nr
            AND buf-eg-request.sub-task = sub-code NO-LOCK NO-ERROR.
        IF AVAILABLE buf-eg-request THEN
        DO:
            FIND CURRENT buf-eg-request EXCLUSIVE-LOCK.
            ASSIGN
                buf-eg-request.maintask = maintask-nr2
                buf-eg-request.sub-task = sub-code2
                buf-eg-request.subtask-bezeich = bezeich 
            .
            FIND CURRENT buf-eg-request NO-LOCK.
            RELEASE buf-eg-request.
            success-flag = YES.
        END.        
    END.

    /*Delete Selected Merge Problem*/
    FIND CURRENT eg-subtask EXCLUSIVE-LOCK.  
    DELETE eg-subtask.  
    RELEASE eg-subtask.
    success-flag = YES.
END.

