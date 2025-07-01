
DEFINE TEMP-TABLE m-list LIKE mathis.
DEFINE TEMP-TABLE fa-art LIKE fa-artikel.

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
    FIND FIRST counters WHERE counters.counter-no = 17 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
        create counters. 
        counters.counter-no = 17. 
    END. 
    IF counters.counter = 0 THEN counters.counter-bez = "Material / Fixed Asset". 
    counters.counter = counters.counter + 1. 
    
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
    
    FIND CURRENT mathis NO-LOCK. 
    FIND CURRENT counters NO-LOCK. 
    FIND CURRENT fa-artikel NO-LOCK. 
END.


PROCEDURE chg-mathis:
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
    FIND CURRENT fa-artikel NO-LOCK.

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
