DEFINE TEMP-TABLE subtask LIKE eg-subtask.

DEF INPUT PARAMETER TABLE FOR subtask.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER subBuff FOR eg-subtask.
FIND FIRST subtask.
IF case-type = 1 THEN
DO:
    CREATE eg-subtask.

    ASSIGN 
    subtask.create-DATE     = TODAY
    subtask.create-TIME     = TIME
    subtask.create-by       = user-init
    subtask.sourceForm      = "0". 

    BUFFER-COPY subtask TO eg-subtask.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST subBuff WHERE subBuff.main-nr = subtask.main-nr AND subBuff.bezeich = subtask.bezeich 
        AND subbuff.sub-code NE subtask.sub-code NO-LOCK NO-ERROR.
    IF AVAILABLE subBuff THEN
    DO:
        fl-code = 1.
        /*MTHIDE MESSAGE NO-PAUSE.
        MESSAGE translateextended ("Description for selected Object already exists, choose other one.", lvcarea, "") 
            VIEW-AS ALERT-BOX INFORMATION.*/
    END.
    ELSE
    DO:
        FIND FIRST eg-subtask WHERE eg-subtask.dept-nr = subtask.dept-nr AND eg-subtask.main-nr = subtask.main-nr 
            AND eg-subtask.sub-code = subtask.sub-code NO-LOCK NO-ERROR.
        IF AVAILABLE eg-subtask THEN
        DO:
            IF eg-subtask.othersflag NE subtask.othersflag THEN
            DO:
                IF subtask.othersflag = YES THEN
                DO:
                    FIND FIRST eg-subtask WHERE eg-subtask.dept-nr = subtask.dept-nr AND eg-subtask.main-nr = subtask.main-nr 
                    AND eg-subtask.sub-code NE subtask.sub-code AND eg-subtask.othersflag = YES NO-LOCK NO-ERROR.
                    IF AVAILABLE eg-subtask THEN
                    DO:
                        fl-code = 2.
                        /*MTHIDE MESSAGE NO-PAUSE.
                        MESSAGE translateextended ("There is already Object Task with User defineable description.", lvcarea, "") 
                            VIEW-AS ALERT-BOX INFORMATION.*/
                    END.
                    ELSE
                    DO:
                        FIND FIRST eg-subtask WHERE RECID(eg-subtask) = rec-id.
                        FIND CURRENT eg-subtask EXCLUSIVE-LOCK NO-ERROR.
                        BUFFER-COPY subtask TO eg-subtask.
                        FIND CURRENT eg-subtask NO-LOCK.
                        RELEASE eg-subtask.
                        fl-code = 3.

                        /*MT
                        RUN mk-readonly(YES).
                        OPEN QUERY q1 FOR EACH eg-subtask /*WHERE eg-subtask.reserve-int = ""*/ NO-LOCK, FIRST maintask WHERE 
                                maintask.main-nr = eg-subtask.main-nr NO-LOCK, FIRST sduration
                                WHERE sduration.Duration-nr = eg-subtask.dur-nr NO-LOCK, FIRST department
                                WHERE department.dept-nr = eg-subtask.dept-nr NO-LOCK 
                                BY eg-subtask.sub-code.
                        
                        curr-select = "".
                        ENABLE btn-addart btn-renart btn-delart btn-exit WITH FRAME frame1.
                        APPLY "entry" TO b1.
                        */
                    END.
                END.
                ELSE
                DO:
                    FIND FIRST eg-subtask WHERE RECID(eg-subtask) = rec-id.
                    FIND CURRENT eg-subtask EXCLUSIVE-LOCK NO-ERROR.
                    BUFFER-COPY subtask TO eg-subtask.
                    FIND CURRENT eg-subtask NO-LOCK.
                    RELEASE eg-subtask.
                    fl-code = 3.

                    /*MT
                    RUN mk-readonly(YES).
                    OPEN QUERY q1 FOR EACH eg-subtask /*WHERE eg-subtask.reserve-int = ""*/ NO-LOCK, FIRST maintask WHERE 
                            maintask.main-nr = eg-subtask.main-nr NO-LOCK, FIRST sduration
                            WHERE sduration.Duration-nr = eg-subtask.dur-nr NO-LOCK, FIRST department
                            WHERE department.dept-nr = eg-subtask.dept-nr NO-LOCK 
                            BY eg-subtask.sub-code.
                    curr-select = "".
                    ENABLE btn-addart btn-renart btn-delart btn-exit WITH FRAME frame1.
                    APPLY "entry" TO b1.
                    */
                END.
            END.
            ELSE
            DO:
                FIND FIRST eg-subtask WHERE RECID(eg-subtask) = rec-id.
                FIND CURRENT eg-subtask EXCLUSIVE-LOCK NO-ERROR.
                BUFFER-COPY subtask TO eg-subtask.
                FIND CURRENT eg-subtask NO-LOCK.
                RELEASE eg-subtask.
                fl-code = 3.

                /*MT
                RUN mk-readonly(YES).
                OPEN QUERY q1 FOR EACH eg-subtask /*WHERE eg-subtask.reserve-int = ""*/ NO-LOCK, FIRST maintask WHERE 
                    maintask.main-nr = eg-subtask.main-nr NO-LOCK, FIRST sduration
                    WHERE sduration.Duration-nr = eg-subtask.dur-nr NO-LOCK, FIRST department
                    WHERE department.dept-nr = eg-subtask.dept-nr NO-LOCK 
                    BY eg-subtask.sub-code.
                curr-select = "".
                ENABLE btn-addart btn-renart btn-delart btn-exit WITH FRAME frame1.
                APPLY "entry" TO b1.
                */
            END.
        END.
    END.
END.
