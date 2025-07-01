
DEFINE TEMP-TABLE m-list LIKE mathis.
/* DEFINE TEMP-TABLE fa-art LIKE fa-artikel. */
DEFINE TEMP-TABLE fa-art 
    LIKE fa-artikel 
    FIELD start-date AS DATE.

DEFINE INPUT PARAMETER flag             AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER mathis-nr        AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER spec             AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER locate           AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER picture-file     AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER upgrade-part     AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER fibukonto        AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER credit-fibu      AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER debit-fibu       AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER user-init        AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER curr-location    AS CHAR     NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR m-list.
DEFINE INPUT PARAMETER TABLE FOR fa-art.
DEFINE OUTPUT PARAMETER curr-mathisnr   AS INTEGER NO-UNDO.

DEFINE VARIABLE created AS LOGICAL NO-UNDO.

FIND FIRST m-list NO-ERROR.
FIND FIRST fa-art NO-ERROR.

IF flag = 1 THEN RUN new-mathis.
ELSE IF flag = 2 THEN RUN chg-mathis.

PROCEDURE new-mathis:
    DEFINE VARIABLE avail-counter AS LOGICAL INITIAL NO.
    DEFINE VARIABLE last-counter AS INTEGER.

    FIND FIRST counters WHERE counters.counter-no = 17 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
        create counters. 
        counters.counter-no = 17. 
    END. 
    IF counters.counter = 0 THEN counters.counter-bez = "Material / Fixed Asset". 
    /* counters.counter = counters.counter + 1. */

    last-counter = counters.counter + 1.
    DO WHILE avail-counter EQ NO:
        FIND FIRST mathis WHERE mathis.nr EQ last-counter NO-LOCK NO-ERROR.
        IF AVAILABLE mathis THEN
        DO:
            last-counter = last-counter + 1.
        END.
        ELSE
        DO:
            avail-counter = YES.
        END.
    END.
    counters.counter = last-counter.        

    create mathis. 
    ASSIGN mathis.nr        = counters.counter
           mathis.datum     = m-list.datum
           mathis.name      = m-list.NAME
           mathis.supplier  = m-list.supplier
           mathis.model     = m-list.model
           mathis.mark      = m-list.mark
           mathis.asset     = m-list.asset
           mathis.price     = m-list.price 
           mathis.spec      = spec
           mathis.location  = locate
           mathis.remark    = m-list.remark
           mathis.fname     = picture-file
           curr-mathisnr    = mathis.nr.
    
    IF upgrade-part THEN
    mathis.flag = 2.
    ELSE mathis.flag = 1.
    
    create fa-artikel. 
    ASSIGN 
        fa-artikel.nr           = counters.counter
        fa-artikel.lief-nr      = fa-art.lief-nr 
        fa-artikel.gnr          = fa-art.gnr
        fa-artikel.subgrp       = fa-art.subgrp 
        fa-artikel.katnr        = fa-art.katnr
        fa-artikel.fibukonto    = fibukonto 
        fa-artikel.credit-fibu  = credit-fibu 
        fa-artikel.debit-fibu   = debit-fibu 
        fa-artikel.anzahl       = fa-art.anzahl 
        fa-artikel.anz100       = fa-art.anzahl 
        fa-artikel.warenwert    = fa-art.warenwert 
        fa-artikel.depn-wert    = fa-art.depn-wert 
        fa-artikel.book-wert    = fa-art.book-wert 
        fa-artikel.anz-depn     = fa-art.anz-depn 
        fa-artikel.next-depn    = fa-art.next-depn 
        fa-artikel.first-depn   = fa-art.first-depn 
        fa-artikel.last-depn    = fa-art.last-depn
        fa-artikel.id           = user-init 
        created = YES. 
    
    CREATE queasy.
    ASSIGN
        queasy.key     = 314
        queasy.number1 = counters.counter
        queasy.date1   = fa-art.start-date.      
    FIND CURRENT mathis NO-LOCK. 
    FIND CURRENT counters NO-LOCK. 
    FIND CURRENT fa-artikel NO-LOCK. 
    FIND CURRENT queasy NO-LOCK.
END.


PROCEDURE chg-mathis:
    DEFINE VARIABLE next-date AS DATE. 
    DEFINE VARIABLE next-mon AS INTEGER. 
    DEFINE VARIABLE next-yr AS INTEGER.
    
    FIND FIRST mathis WHERE mathis.nr = mathis-nr EXCLUSIVE-LOCK. 
    ASSIGN
          mathis.datum      = m-list.datum
          mathis.name       = m-list.NAME 
          mathis.supplier   = m-list.supplier 
          mathis.model      = m-list.model 
          mathis.mark       = m-list.mark 
          mathis.spec       = spec 
          mathis.asset      = m-list.asset 
          mathis.location   = locate 
          mathis.price      = m-list.price 
          mathis.remark     = m-list.remark 
          mathis.fname      = picture-file.
    
    IF upgrade-part THEN mathis.flag = 2.
    ELSE mathis.flag = 1.
    FIND CURRENT mathis NO-LOCK.

    FIND FIRST fa-artikel WHERE fa-artikel.nr = mathis-nr EXCLUSIVE-LOCK. 
    ASSIGN
        fa-artikel.lief-nr      = fa-art.lief-nr
        fa-artikel.gnr          = fa-art.gnr 
        fa-artikel.subgrp       = fa-art.subgrp 
        fa-artikel.katnr        = fa-art.katnr 
        fa-artikel.fibukonto    = fibukonto 
        fa-artikel.credit-fibu  = credit-fibu 
        fa-artikel.debit-fibu   = debit-fibu 
        fa-artikel.anzahl       = fa-art.anzahl 
        fa-artikel.anz100       = fa-art.anzahl 
        fa-artikel.warenwert    = fa-art.warenwert 
        fa-artikel.depn-wert    = fa-art.depn-wert 
        fa-artikel.book-wert    = fa-art.book-wert 
        fa-artikel.anz-depn     = fa-art.anz-depn 
        fa-artikel.next-depn    = fa-art.next-depn 
        fa-artikel.first-depn   = fa-art.first-depn 
        fa-artikel.last-depn    = fa-art.last-depn 
        fa-artikel.cid          = user-init 
        fa-artikel.changed      = TODAY. 
    /* FIND CURRENT fa-artikel NO-LOCK. */
    
    /*
    FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = mathis-nr  EXCLUSIVE-LOCK.
    ASSIGN
        queasy.date1   = fa-art.start-date. 
    FIND CURRENT queasy NO-LOCK.  */
    /*
    FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = mathis-nr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
            queasy.date1   = fa-art.start-date.
        /*    
        IF fa-artikel.next-depn NE ? THEN
        DO:
            next-mon = month(queasy.date1) + 1. 
            next-yr = year(queasy.date1). 
            IF next-mon = 13 THEN 
            DO: 
                next-mon = 1. 
                next-yr = next-yr + 1. 
            END. 
            next-date = DATE(next-mon, 1, next-yr) - 1.
            ASSIGN
                fa-artikel.next-depn = next-date.
        END. */   
    END. */

    /*
    FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = mathis-nr  EXCLUSIVE-LOCK.
    ASSIGN
        queasy.date1   = fa-art.start-date. 
    IF fa-artikel.next-depn NE ? AND fa-artikel.first-depn EQ ? THEN
    DO:
        next-mon = month(queasy.date1) + 1. 
        next-yr = year(queasy.date1). 
        IF next-mon = 13 THEN 
        DO: 
            next-mon = 1. 
            next-yr = next-yr + 1. 
        END. 
        next-date = DATE(next-mon, 1, next-yr) - 1.
        ASSIGN
            fa-artikel.next-depn = next-date.
    END.    
    FIND CURRENT queasy NO-LOCK. */
    FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = mathis-nr NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        queasy.date1   = fa-art.start-date.
        IF fa-artikel.next-depn NE ?  AND fa-artikel.first-depn EQ ? THEN
        DO:
            next-mon = month(queasy.date1) + 1. 
            next-yr = year(queasy.date1). 
            IF next-mon = 13 THEN 
            DO: 
                next-mon = 1. 
                next-yr = next-yr + 1. 
            END. 
            next-date = DATE(next-mon, 1, next-yr) - 1.
            ASSIGN
                fa-artikel.next-depn = next-date.
        END.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.key     = 314
            queasy.number1 = mathis-nr
            queasy.date1   = fa-art.start-date.  
    END.
    FIND CURRENT fa-artikel NO-LOCK. 
    
    /* FIND CURRENT fa-artikel NO-LOCK. */

    IF curr-location NE mathis.location THEN 
    DO: 
        create mhis-line.
        ASSIGN
            mhis-line.nr        = mathis-nr 
            mhis-line.datum     = TODAY 
            mhis-line.remark    = "Change Location      From: " + curr-location 
            + "   To: " + mathis.location. 
    FIND CURRENT mhis-line NO-LOCK. 
    END.
END.
