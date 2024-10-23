DEF TEMP-TABLE akt-line1 LIKE akt-line.

DEFINE INPUT PARAMETER case-type    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER file-mode    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER base64file   AS LONGCHAR NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR akt-line1.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER result-message AS CHAR.

DEF VAR curr-counter AS INT. 

FIND FIRST akt-line1 NO-ERROR.
IF NOT AVAILABLE akt-line1 THEN RETURN NO-APPLY.
curr-counter = akt-line1.linenr.

IF base64file EQ ? THEN
DO:
    base64file = "".
END.

CASE case-type:
    WHEN 1 THEN
    DO: 
        CREATE akt-line.
        BUFFER-COPY akt-line1 TO akt-line.
        success-flag = YES.
        FIND CURRENT akt-line NO-LOCK.

        IF success-flag THEN
        DO:
            IF base64file NE "" AND user-init NE "" THEN
            DO:
                RUN upload-imagesetupbl.p(file-mode, base64file, user-init, curr-counter, OUTPUT result-message).
            END.                
        END.        
    END.
    WHEN 2 THEN
    DO: 
        FIND FIRST akt-line WHERE akt-line.linenr = akt-line1.linenr EXCLUSIVE-LOCK.
        IF AVAILABLE akt-line THEN
        DO: 
            BUFFER-COPY akt-line1 TO akt-line.
            success-flag = YES.
        END.
        FIND CURRENT akt-line NO-LOCK.

        IF success-flag THEN
        DO:
            IF akt-line1.flag EQ 2 THEN
            DO:
                RUN delete-imagesetupbl.p(file-mode, curr-counter, OUTPUT result-message, OUTPUT base64file).
            END.
            ELSE
            DO:
                IF base64file NE "" AND user-init NE "" THEN
                DO:
                    RUN upload-imagesetupbl.p(file-mode, base64file, user-init, curr-counter, OUTPUT result-message).
                END.                    
            END. 
        END.               
    END.
END CASE.
