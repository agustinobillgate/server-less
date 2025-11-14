DEFINE INPUT PARAMETER rcode     AS CHAR.
DEFINE INPUT PARAMETER curr-task AS CHAR.

DEFINE BUFFER qsy FOR queasy.
DEFINE VARIABLE cat-flag AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE zikat-nr AS INTEGER NO-UNDO.
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.

IF curr-task = "avail" THEN
DO:
    IF rcode NE "" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 171 AND (queasy.logi1 OR queasy.logi3) 
            AND queasy.char1 = rcode NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE queasy:
            DO TRANSACTION:
                FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
                IF AVAILABLE qsy THEN DO:
                    ASSIGN
                        qsy.logi1 = NO
                        qsy.logi3 = NO.
                    FIND CURRENT qsy NO-LOCK.
                    RELEASE qsy.
                END.
            END.
            FIND NEXT queasy WHERE queasy.KEY = 171 AND (queasy.logi1 OR queasy.logi3)
                AND queasy.char1 = rcode NO-LOCK NO-ERROR.
        END.                            
    END.
    ELSE IF rcode = "" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 171 AND (queasy.logi1 OR queasy.logi3) NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE queasy:
            DO TRANSACTION:
                FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
                IF AVAILABLE qsy THEN DO:
                    ASSIGN
                        qsy.logi1 = NO
                        qsy.logi3 = NO.
                    FIND CURRENT qsy NO-LOCK.
                    RELEASE qsy.
                END.
            END.
            FIND NEXT queasy WHERE queasy.KEY = 171 AND (queasy.logi1 OR queasy.logi3) NO-LOCK NO-ERROR.
        END. 
    END.
    
    /* FIND FIRST queasy WHERE queasy.KEY = 175 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND CURRENT queasy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            DELETE queasy.
            RELEASE queasy.
            FIND NEXT queasy WHERE queasy.KEY = 175 NO-LOCK NO-ERROR.
        END.
    END. */ /*do not delete needed for debug*/
	FIND FIRST queasy WHERE queasy.KEY = 175 AND (queasy.logi1 OR queasy.logi3)  NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                qsy.logi1 = NO.
                qsy.logi3 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.  
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 175 AND (queasy.logi1 OR queasy.logi3) NO-LOCK NO-ERROR.
    END.
END.
ELSE IF curr-task = "availAll" THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY = 171 AND (queasy.logi1 OR queasy.logi3) NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                ASSIGN
                    qsy.logi1 = NO
                    qsy.logi3 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 171 AND (queasy.logi1 OR queasy.logi3) NO-LOCK NO-ERROR.
    END. 

    /* FIND FIRST queasy WHERE queasy.KEY = 175 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND CURRENT queasy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            DELETE queasy.
            RELEASE queasy.
            FIND NEXT queasy WHERE queasy.KEY = 175 NO-LOCK NO-ERROR.
        END.
    END. */ /*do not delete needed for debug*/
	FIND FIRST queasy WHERE queasy.KEY = 175 AND (queasy.logi1 OR queasy.logi3)  NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                qsy.logi1 = NO.
                qsy.logi3 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.  
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 175 AND (queasy.logi1 OR queasy.logi3) NO-LOCK NO-ERROR.
    END.
END.
ELSE IF curr-task = "availbyrmtype" THEN /* tambahan untuk mengirim avail per roomtype  17Sep2025 */
DO:
    FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN cat-flag = YES.

    IF cat-flag THEN /* by room category */
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 152 
            AND queasy.char1 = rcode NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN zikat-nr = queasy.number1.
    END.  
    ELSE /* by room type */
    DO:
        FIND FIRST zimkateg WHERE zimkateg.kurzbez = rcode NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN zikat-nr = zimkateg.zikatnr.
    END.

    FIND FIRST queasy WHERE queasy.KEY = 171 AND (queasy.logi1 OR queasy.logi3)
		AND queasy.number1 = zikat-nr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                ASSIGN
                    qsy.logi1 = NO
                    qsy.logi3 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.  
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 171 AND (queasy.logi1 OR queasy.logi3)
            AND queasy.number1 = zikat-nr NO-LOCK NO-ERROR.
    END.

    /* FIND FIRST queasy WHERE queasy.KEY = 175 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND CURRENT queasy EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            DELETE queasy.
            RELEASE queasy.
            FIND NEXT queasy WHERE queasy.KEY = 175 NO-LOCK NO-ERROR.
        END.
    END. */ /*do not delete needed for debug*/
	FIND FIRST queasy WHERE queasy.KEY = 175 AND (queasy.logi1 OR queasy.logi3) 
		AND queasy.number1 = zikat-nr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                qsy.logi1 = NO.
                qsy.logi3 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.  
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 175 AND (queasy.logi1 OR queasy.logi3) 
		AND queasy.number1 = zikat-nr NO-LOCK NO-ERROR.
    END.
END.
ELSE IF curr-task = "rate" THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY = 170 AND (queasy.logi1 OR queasy.logi3)
        AND queasy.char1 = rcode NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                ASSIGN
                    qsy.logi1 = NO
                    qsy.logi3 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.  
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 170 AND (queasy.logi1 OR queasy.logi3)
            AND queasy.char1 = rcode NO-LOCK NO-ERROR.
    END.
END. 
ELSE IF curr-task = "rateAll" THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY = 170 AND (queasy.logi1 OR queasy.logi3)  NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                qsy.logi1 = NO.
                qsy.logi3 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.  
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 170 AND (queasy.logi1 OR queasy.logi3) NO-LOCK NO-ERROR.
    END.
END.

/* tambahan untuk mengirim rates per roomtype CRG 15Nov2018 */
ELSE IF curr-task = "ratebyrmtype" THEN
DO:
    DEF VAR rcode1 AS CHAR.
    DEF VAR rm-typ AS CHAR.
    
    rcode1 = ENTRY(1, rcode, ";").
    rm-typ = ENTRY(2, rcode, ";").

    FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN cat-flag = YES.

    IF cat-flag THEN /* by room category */
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 152 
            AND queasy.char1 = rm-typ NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN zikat-nr = queasy.number1.
    END.  
    ELSE /* by room type */
    DO:
        FIND FIRST zimkateg WHERE zimkateg.kurzbez = rm-typ NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN zikat-nr = zimkateg.zikatnr.
    END.

    FIND FIRST queasy WHERE queasy.KEY = 170 AND (queasy.logi1 OR queasy.logi3)
        AND queasy.char1 = rcode1 AND queasy.number1 = zikat-nr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                ASSIGN
                    qsy.logi1 = NO
                    qsy.logi3 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.  
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 170 AND (queasy.logi1 OR queasy.logi3)
            AND queasy.char1 = rcode1 AND queasy.number1 = zikat-nr NO-LOCK NO-ERROR.
    END.
END.
ELSE IF curr-task = "restriction" THEN /*NC -travelclick*/
DO:
    FIND FIRST queasy WHERE queasy.KEY = 175 AND (queasy.logi1 OR queasy.logi3)  NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                qsy.logi1 = NO.
                qsy.logi3 = NO.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.  
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 175 AND (queasy.logi1 OR queasy.logi3) NO-LOCK NO-ERROR.
    END.
END.
ELSE IF curr-task = "push-all-restriction" THEN /*NC -travelclick*/
DO:
    FIND FIRST queasy WHERE queasy.KEY = 175 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        DO TRANSACTION:
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE qsy THEN DO:
                qsy.logi3 = YES.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.  
            END.
        END.
        FIND NEXT queasy WHERE queasy.KEY = 175 NO-LOCK NO-ERROR.
    END.
END.