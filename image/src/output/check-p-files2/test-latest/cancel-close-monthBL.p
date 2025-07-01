
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date   AS DATE.

RUN close-month.

PROCEDURE close-month:
    DO TRANSACTION:
        FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum GE from-date 
            AND gl-jouhdr.datum LE to-date NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-jouhdr :
            FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK.
            ASSIGN gl-jouhdr.activeflag = 0 gl-jouhdr.BATCH = YES.
            IF gl-jouhdr.jtype = 0 THEN ASSIGN gl-jouhdr.BATCH = NO.
            FIND CURRENT gl-jouhdr NO-LOCK.

            FIND FIRST gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK
                NO-ERROR.
            DO WHILE AVAILABLE gl-journal:
                FIND CURRENT gl-journal EXCLUSIVE-LOCK.
                ASSIGN gl-journal.activeflag = 0.
                FIND CURRENT gl-journal NO-LOCK.

                FIND NEXT gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK
                    NO-ERROR.
            END.

            FIND NEXT gl-jouhdr WHERE gl-jouhdr.datum GE from-date 
                AND gl-jouhdr.datum LE to-date NO-LOCK NO-ERROR.
        END.
        
        FIND FIRST htparam WHERE paramnr = 597. /* Current Closing Period */
        htparam.fdate = to-date.
        FIND FIRST htparam WHERE paramnr = 558. /* Last Closing Period */
        htparam.fdate = from-date - 1.

    END.
END.
