DEFINE TEMP-TABLE t-list 
  FIELD nr          AS INTEGER
  FIELD f-bezeich   AS CHAR FORMAT "x(20)" 
  FIELD t-bezeich   AS CHAR FORMAT "x(30)" 
  FIELD artnr       AS CHAR FORMAT "x(7)"
  FIELD bezeich     AS CHAR FORMAT "x(36)" 
  FIELD qty         AS DECIMAL FORMAT "->>,>>9.999" 
  FIELD price       AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" 
  FIELD val         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD mess-unit   AS CHARACTER    
  FIELD deliv-unit  AS CHARACTER
  .

DEFINE INPUT PARAMETER sorttype  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER from-date AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER to-date   AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER main-grp  AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.

RUN create-list.

PROCEDURE create-list:
    DEF BUFFER tbuff FOR t-list.
    DEF VAR close-mat AS DATE NO-UNDO.
    DEF VAR close-fb  AS DATE NO-UNDO.
    DEF VAR close-date AS DATE NO-UNDO.
    DEF VAR tot-amt   AS DECIMAL NO-UNDO INITIAL 0.
    DEF VAR tot-qty   AS INTEGER NO-UNDO INITIAL 0.
    DEF VAR i         AS INTEGER NO-UNDO.

    FIND FIRST htparam WHERE paramnr = 221 NO-LOCK.
    close-mat = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */
    FIND FIRST htparam WHERE paramnr = 224 NO-LOCK.
    close-fb = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */

    IF close-mat GT close-fb THEN close-date = close-mat.
    ELSE close-date = close-fb.

    FOR EACH t-list:
        DELETE t-list.
    END.

    IF sorttype NE 3 THEN
    DO:
        IF to-date LE close-date THEN
            FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND 
                l-ophis.datum LE to-date AND l-ophis.op-art = 3 AND 
                SUBSTR(l-ophis.lscheinnr,1,3) = "INV" NO-LOCK,
                FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
                AND l-artikel.endkum = main-grp 
                NO-LOCK BY l-artikel.bezeich BY l-ophis.datum BY
                l-ophis.lscheinnr:
                CREATE t-list.
                ASSIGN 
                    t-list.artnr    = STRING(l-ophis.artnr, "9999999")
                    t-list.bezeich  = l-artikel.bezeich
                    t-list.qty      = l-ophis.anzahl
                    t-list.val      = l-ophis.warenwert
                    tot-amt         = tot-amt + l-ophis.warenwert
                    tot-qty         = tot-qty + l-ophis.anzahl.

                /*FDL June 28, 2024 => Ticket ECF03B*/
                t-list.mess-unit    = l-artikel.masseinheit.
                t-list.deliv-unit   = l-artikel.traubensort.

                IF t-list.qty GT 0 AND t-list.val GT 0 THEN
                    t-list.price   = t-list.val / t-list.qty.
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-ophis.fibukonto
                    NO-LOCK NO-ERROR.
                IF AVAILABLE gl-acct THEN
                    t-list.t-bezeich = gl-acct.bezeich.
                FIND FIRST l-lager WHERE l-lager.lager-nr = l-ophis.lager-nr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE l-lager THEN
                    t-list.f-bezeich = l-lager.bezeich.
            END.
        ELSE
            FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date
                AND l-op.op-art = 3 AND l-op.loeschflag LE 1 AND
                SUBSTR(l-op.lscheinnr,1,3) = "INV" NO-LOCK,
                FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr
                AND l-artikel.endkum = main-grp  
                NO-LOCK BY l-artikel.bezeich BY l-op.datum BY 
                l-op.lscheinnr:
    
                CREATE t-list.
                ASSIGN 
                    t-list.artnr    = STRING(l-op.artnr, "9999999")
                    t-list.bezeich  = l-artikel.bezeich
                    t-list.qty      = l-op.anzahl
                    t-list.val      = l-op.warenwert
                    tot-amt         = tot-amt + l-op.warenwert
                    tot-qty         = tot-qty + l-ophis.anzahl.

                /*FDL June 28, 2024 => Ticket ECF03B*/
                t-list.mess-unit    = l-artikel.masseinheit.
                t-list.deliv-unit   = l-artikel.traubensort.

                IF t-list.qty GT 0 AND t-list.val GT 0 THEN
                    t-list.price   = t-list.val / t-list.qty.
                
                FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE l-lager THEN
                    t-list.f-bezeich = l-lager.bezeich.
            END.
    END.
    ELSE
    DO:
        IF to-date LE close-date THEN
            FOR EACH l-ophis WHERE l-ophis.datum GE from-date AND 
                l-ophis.datum LE to-date AND l-ophis.op-art = 3 AND 
                SUBSTR(l-ophis.lscheinnr,1,3) = "INV" NO-LOCK,
                FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
                AND l-artikel.endkum GE 3
                NO-LOCK BY l-artikel.bezeich BY l-ophis.datum BY
                l-ophis.lscheinnr:
                CREATE t-list.
                ASSIGN 
                    t-list.artnr    = STRING(l-ophis.artnr, "9999999")
                    t-list.bezeich  = l-artikel.bezeich
                    t-list.qty      = l-ophis.anzahl
                    t-list.val      = l-ophis.warenwert
                    tot-amt         = tot-amt + l-ophis.warenwert
                    tot-qty         = tot-qty + l-ophis.anzahl.

                /*FDL June 28, 2024 => Ticket ECF03B*/
                t-list.mess-unit    = l-artikel.masseinheit.
                t-list.deliv-unit   = l-artikel.traubensort.

                IF t-list.qty GT 0 AND t-list.val GT 0 THEN
                    t-list.price   = t-list.val / t-list.qty.
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-ophis.fibukonto
                    NO-LOCK NO-ERROR.
                IF AVAILABLE gl-acct THEN
                    t-list.t-bezeich = gl-acct.bezeich.
                FIND FIRST l-lager WHERE l-lager.lager-nr = l-ophis.lager-nr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE l-lager THEN
                    t-list.f-bezeich = l-lager.bezeich.
            END.
        ELSE
            FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date
                AND l-op.op-art = 3 AND l-op.loeschflag LE 1 AND
                SUBSTR(l-op.lscheinnr,1,3) = "INV" NO-LOCK,
                FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr
                AND l-artikel.endkum GE 3
                NO-LOCK BY l-artikel.bezeich BY l-op.datum BY 
                l-op.lscheinnr:
    
                CREATE t-list.
                ASSIGN 
                    t-list.artnr    = STRING(l-op.artnr, "9999999")
                    t-list.bezeich  = l-artikel.bezeich
                    t-list.qty      = l-op.anzahl
                    t-list.val      = l-op.warenwert
                    tot-amt         = tot-amt + l-op.warenwert
                    tot-qty         = tot-qty + l-ophis.anzahl.

                /*FDL June 28, 2024 => Ticket ECF03B*/
                t-list.mess-unit    = l-artikel.masseinheit.
                t-list.deliv-unit   = l-artikel.traubensort.

                IF t-list.qty GT 0 AND t-list.val GT 0 THEN
                    t-list.price   = t-list.val / t-list.qty.
                
                FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE l-lager THEN
                    t-list.f-bezeich = l-lager.bezeich.
            END.
    END.
    
    i = 1.
    FOR EACH tbuff NO-LOCK BY tbuff.f-bezeich:
        ASSIGN tbuff.nr = i.
        i = i + 1.
    END.

    CREATE t-list.
    ASSIGN 
        t-list.bezeich = "T O T A L"
        t-list.qty = tot-qty
        t-list.val = tot-amt
        t-list.nr  = i.

END.
