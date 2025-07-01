
DEF INPUT PARAMETER answer2            AS LOGICAL.
DEF INPUT PARAMETER t-resnr            AS INT.
DEF INPUT PARAMETER t-reslinnr         AS INT.
DEF INPUT PARAMETER c-status           AS CHAR.
DEF INPUT PARAMETER r-status           AS INT.
DEF INPUT PARAMETER recid-rl           AS INT.
DEF INPUT PARAMETER bk-reser-resstatus AS INT.
DEF INPUT PARAMETER user-init          AS CHAR.

DEFINE BUFFER bf FOR bk-func. 
DEFINE BUFFER rl FOR bk-reser.

DEFINE VARIABLE new-status AS CHAR.
DEFINE VARIABLE old-status AS CHAR.

IF bk-reser-resstatus EQ 1 THEN
    old-status = "Fix Reservation".
ELSE IF bk-reser-resstatus EQ 2 THEN
    old-status = "Tentative".

IF r-status EQ 1 THEN
    new-status = "Fix Reservation".
ELSE IF r-status EQ 2 THEN
    new-status = "Tentative".

FIND FIRST rl WHERE RECID(rl) = recid-rl NO-LOCK NO-ERROR.
IF answer2 THEN
DO:
    FOR EACH bf WHERE bf.veran-nr = t-resnr:
        IF AVAILABLE bf AND c-status NE "" THEN
        DO:
            /*FIND CURRENT bf EXCLUSIVE-LOCK. */
            bf.c-resstatus[1] = c-status. 
            bf.r-resstatus[1] = r-status. 
            bf.resstatus = r-status. 
            /*FIND CURRENT bf NO-LOCK.*/  
            FIND CURRENT rl EXCLUSIVE-LOCK. 
            rl.resstatus = r-status. 
            FIND CURRENT rl NO-LOCK. 
            RUN check-oth-rl-sts.p(bf.veran-nr,bf.veran-seite,bf.resstatus). 
            /*MT
            IF curr-view = "daily" THEN RUN create-dlist. 
            ELSE RUN create-wlist.
            */
            IF bk-reser-resstatus NE r-status THEN
            DO:
                FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
                CREATE res-history. 
                ASSIGN 
                    res-history.nr = bediener.nr 
                    res-history.datum = TODAY 
                    res-history.zeit = TIME 
                    res-history.aenderung = "Status Changes From " + old-status + " To " + new-status
                    res-history.action = "Banquet"
                . 
                FIND CURRENT res-history NO-LOCK. 
                RELEASE res-history.
            END.
        END.
    END.
END.
ELSE
DO:
    FIND FIRST bf WHERE bf.veran-nr = t-resnr AND 
    bf.veran-seite = t-reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE bf AND c-status NE "" THEN 
    DO: 
        FIND CURRENT bf EXCLUSIVE-LOCK. 
        bf.c-resstatus[1] = c-status. 
        bf.r-resstatus[1] = r-status. 
        bf.resstatus = r-status. 
        FIND CURRENT bf NO-LOCK. 
        FIND CURRENT rl EXCLUSIVE-LOCK. 
        rl.resstatus = r-status. 
        FIND CURRENT rl NO-LOCK. 
        RUN check-oth-rl-sts.p(bf.veran-nr,bf.veran-seite,bf.resstatus).
        /*MT
        IF curr-view = "daily" THEN RUN create-dlist. 
        ELSE RUN create-wlist.
        */
        IF bk-reser-resstatus NE r-status THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
            CREATE res-history. 
            ASSIGN 
                res-history.nr = bediener.nr 
                res-history.datum = TODAY 
                res-history.zeit = TIME 
                res-history.aenderung = "Status Changes From " + old-status + " To " + new-status
                res-history.action = "Banquet"
            . 
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history.
        END.
    END. 
END.

