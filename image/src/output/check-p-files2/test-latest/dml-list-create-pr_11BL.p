DEFINE TEMP-TABLE c-list 
    FIELD zwkum    AS INTEGER INITIAL 0 
    FIELD grp      AS CHAR FORMAT "x(22)" COLUMN-LABEL "Group" 
    FIELD artnr    LIKE l-artikel.artnr 
    FIELD bezeich  AS CHAR FORMAT "x(38)" COLUMN-LABEL "Description" 
    FIELD qty      AS DECIMAL  FORMAT ">>,>>9.99" LABEL "Ordered Qty" 
    FIELD a-qty    AS DECIMAL  FORMAT "->>,>>9.99" LABEL "Add Qty" 
    FIELD price    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Unit Price"
    FIELD l-price  AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Last Purchase Price" /*Naufal*/
    FIELD unit     AS CHAR FORMAT "x(3)" LABEL "Unit" 
    FIELD content  AS DECIMAL FORMAT ">>,>>9.99" LABEL "Content" 
    FIELD amount   AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" LABEL "Amount" 
    FIELD deliver  AS DECIMAL FORMAT ">>,>>9.99" LABEL "Delivered" 
    FIELD dept     AS INTEGER FORMAT ">>" LABEL "Dept" 
    FIELD supplier AS CHAR FORMAT "x(32)" LABEL "Supplier"
    FIELD id       AS CHAR FORMAT "x(4)" LABEL "ID" 
    FIELD cid      AS CHAR FORMAT "x(4)" LABEL "CID" 
    FIELD price1   AS DECIMAL 
    FIELD qty1     AS DECIMAL
    FIELD lief-nr  AS INTEGER
    FIELD approved AS LOGICAL INIT NO
    FIELD remark   AS CHAR
    /*NAUFAL 120321 - Testing add field for stock oh value*/
    FIELD soh      AS DECIMAL FORMAT ">,>>>,>>9.99" LABEL "Actual Qty"
    /*end*/
    FIELD dml-nr   AS CHARACTER
    FIELD qty2     AS DECIMAL.

DEFINE TEMP-TABLE s-list 
    FIELD s-flag   AS CHAR FORMAT "x(1)" INITIAL "" COLUMN-LABEL "" 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD artnr    LIKE l-artikel.artnr 
    FIELD bezeich  AS CHAR FORMAT "x(32)" COLUMN-LABEL "Description" 
    FIELD qty      AS DECIMAL  FORMAT ">>,>>9.99" LABEL "Ordered Qty" 
    FIELD qty0     AS DECIMAL 
    FIELD price    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Unit Price"
    FIELD qty2     AS DECIMAL. 

DEFINE TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF INPUT PARAMETER TABLE FOR c-list.
DEF INPUT PARAMETER TABLE FOR s-list.

DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER dunit-price AS LOGICAL.
DEF INPUT PARAMETER selected-date AS DATE.
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.

DEFINE VARIABLE docu-nr AS CHAR NO-UNDO.
DEFINE VARIABLE t-qty   AS DECIMAL NO-UNDO.
DEFINE VARIABLE counter AS INTEGER NO-UNDO.

FIND FIRST s-list WHERE s-list.selected = YES NO-LOCK NO-ERROR.
FIND FIRST c-list WHERE c-list.artnr = s-list.artnr NO-LOCK NO-ERROR.
IF c-list.dml-nr NE "" THEN
DO:
    docu-nr = c-list.dml-nr.
    counter = INT(SUBSTRING(c-list.dml-nr, 11, 2)).
END.
ELSE
DO:
    docu-nr = "D" + STRING(c-list.dept, "99") + SUBSTR(STRING(YEAR(selected-date)),3,2) 
        + STRING(MONTH(selected-date), "99") + STRING(DAY(selected-date), "99") + "001".
    counter = 1.
END.

FIND FIRST bediener WHERE bediener.userinit = user-init.
FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id.
RUN create-pr.
FIND CURRENT l-orderhdr NO-LOCK.
CREATE t-l-orderhdr.
BUFFER-COPY l-orderhdr TO t-l-orderhdr.
ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).

PROCEDURE create-pr:
DEFINE VARIABLE pos AS INTEGER INITIAL 0. 
DEFINE buffer s1-list FOR s-list. 
DEFINE buffer c1-list FOR c-list. 
    DO TRANSACTION: 
        FIND CURRENT l-orderhdr EXCLUSIVE-LOCK. 
        ASSIGN 
            l-orderhdr.betriebsnr       = 10
            l-orderhdr.gedruckt         = ?
            l-orderhdr.lief-fax[2]      = " ; ; ; "
            l-orderhdr.lief-fax[1]      = bediener.username
            l-orderhdr.txtnr            = curr-dept 
        . 
        FIND CURRENT l-orderhdr NO-LOCK. 
        
        CREATE l-order. 
        ASSIGN 
            l-order.docu-nr = l-orderhdr.docu-nr 
            l-order.pos = 0 
            l-order.bestelldatum = l-orderhdr.bestelldatum 
            l-order.op-art = 1. 
        
        FOR EACH s1-list WHERE s1-list.selected = YES: 
            FIND FIRST l-artikel WHERE l-artikel.artnr = s1-list.artnr NO-LOCK. 
            pos = pos + 1. 
            CREATE l-order. 
            ASSIGN 
                l-order.docu-nr = l-orderhdr.docu-nr 
                l-order.artnr = l-artikel.artnr 
                l-order.pos = pos 
                l-order.bestelldatum = l-orderhdr.bestelldatum 
                l-order.op-art = 1 
                l-order.lief-fax[1] = bediener.username 
                l-order.lief-fax[3] = l-artikel.traubensort 
                l-order.anzahl = s1-list.qty 
                l-order.einzelpreis = s1-list.price 
                l-order.txtnr = 1 
                l-order.flag = dunit-price 
                l-order.warenwert = s1-list.qty * s1-list.price 
                l-order.quality = STRING(0, "99.99 ") + STRING(0, "99.99") 
                  + STRING(0, " 99.99") . 
            IF l-artikel.lief-einheit NE 0 THEN 
            DO: 
                l-order.warenwert = l-order.warenwert * l-artikel.lief-einheit. 
                IF dunit-price THEN l-order.einzelpreis = l-order.einzelpreis 
                  * l-artikel.lief-einheit. 
                l-order.txtnr = l-artikel.lief-einheit. 
            END. 
            FIND FIRST c1-list WHERE c1-list.artnr = s1-list.artnr.
            l-order.besteller       = c1-list.remark.
            IF s1-list.qty = s1-list.qty0 THEN DELETE c1-list. 
            ELSE c1-list.qty = s1-list.qty0 - s1-list.qty. 
            
            IF curr-dept = 0 THEN 
            DO: 
                FIND FIRST dml-art WHERE dml-art.artnr = s1-list.artnr 
                    AND dml-art.datum = selected-date EXCLUSIVE-LOCK NO-ERROR. 
                IF AVAILABLE dml-art THEN 
                DO: 
                    IF (s1-list.qty + s1-list.qty2) = s1-list.qty0 THEN DO:
                        /*FIND FIRST queasy WHERE queasy.KEY = 202
                            AND queasy.number1 = curr-dept
                            AND queasy.number2 = dml-art.artnr
                            AND queasy.date1   = dml-art.datum NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN DO:
                            FIND CURRENT queasy EXCLUSIVE-LOCK.
                            DELETE queasy.
                            RELEASE queasy.
                        END.                 
                        DELETE dml-art.  */
                        IF NUM-ENTRIES(dml-art.chginit,";") GT 2 THEN
                        DO:
                            IF s1-list.qty NE s1-list.qty0 THEN
                                s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                            ELSE
                                s1-list.qty2 = s1-list.qty.
                            ENTRY(3, dml-art.chginit, ";") = STRING(s1-list.qty2).
                        END.
                        ELSE
                        DO:
                            IF s1-list.qty NE s1-list.qty0 THEN
                                s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                            ELSE
                                s1-list.qty2 = s1-list.qty.
                            dml-art.chginit = dml-art.chginit + ";" + docu-nr + ";" + STRING(s1-list.qty2).
                        END.
                    END.
                    ELSE 
                    DO: 
                        IF NUM-ENTRIES(dml-art.chginit,";") GT 2 THEN
                        DO:
                            s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                            ENTRY(3, dml-art.chginit, ";") = STRING(s1-list.qty2).
                        END.
                        ELSE
                        DO:
                            s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                            dml-art.chginit = dml-art.chginit + ";" + docu-nr + ";" + STRING(s1-list.qty).
                        END.
                        FIND CURRENT dml-art NO-LOCK. 
                    END. 
                END. 
            END. 
            ELSE 
            DO: 
                IF counter GT 1 THEN
                DO:
                    FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
                        AND INT(ENTRY(1,reslin-queasy.char1,";")) EQ s1-list.artnr
                        AND reslin-queasy.date1 EQ selected-date
                        AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept 
                        AND reslin-queasy.number2 EQ counter EXCLUSIVE-LOCK NO-ERROR.
                    IF AVAILABLE reslin-queasy THEN
                    DO:
                        IF (s1-list.qty + s1-list.qty2) = s1-list.qty0 THEN DO:
                            IF NUM-ENTRIES(reslin-queasy.char3,";") GT 2 THEN
                            DO:
                                IF s1-list.qty NE s1-list.qty0 THEN
                                    s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                                ELSE
                                    s1-list.qty2 = s1-list.qty.
                                ENTRY(3, reslin-queasy.char3, ";") = STRING(s1-list.qty2).
                            END.
                            ELSE
                            DO:
                                IF s1-list.qty NE s1-list.qty0 THEN
                                    s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                                ELSE
                                    s1-list.qty2 = s1-list.qty.
                                reslin-queasy.char3 = reslin-queasy.char3 + ";" + STRING(s1-list.qty2).
                            END.
                        END.
                        ELSE 
                        DO:
                            IF NUM-ENTRIES(reslin-queasy.char3,";") GT 2 THEN
                            DO:
                                s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                                ENTRY(3, reslin-queasy.char3, ";") = STRING(s1-list.qty2).
                            END.
                            ELSE
                            DO:
                                s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                                reslin-queasy.char3 = reslin-queasy.char3 + ";" + STRING(s1-list.qty).
                            END.
                            FIND CURRENT reslin-queasy NO-LOCK. 
                        END.
                    END.
                END.
                ELSE
                DO:
                    FIND FIRST dml-artdep WHERE dml-artdep.artnr = s1-list.artnr 
                        AND dml-artdep.datum = selected-date 
                        AND dml-artdep.departement = curr-dept EXCLUSIVE-LOCK NO-ERROR. 
                    IF AVAILABLE dml-artdep THEN 
                    DO:           
                        IF (s1-list.qty + s1-list.qty2) = s1-list.qty0 THEN DO:
                            /*FIND FIRST queasy WHERE queasy.KEY = 202
                                AND queasy.number1 = dml-artdep.departement
                                AND queasy.number2 = dml-artdep.artnr
                                AND queasy.date1   = dml-artdep.datum NO-LOCK NO-ERROR.
                            IF AVAILABLE queasy THEN DO:
                                FIND CURRENT queasy EXCLUSIVE-LOCK.
                                DELETE queasy.
                                RELEASE queasy.
                            END.                 
                            DELETE dml-artdep. 
                            dml-artdep.chginit = dml-artdep.chginit + ";2;" + docu-nr.*/
                        
                            IF NUM-ENTRIES(dml-artdep.chginit,";") GT 2 THEN
                            DO:
                                IF s1-list.qty NE s1-list.qty0 THEN
                                    s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                                ELSE
                                    s1-list.qty2 = s1-list.qty.
                                ENTRY(3, dml-artdep.chginit, ";") = STRING(s1-list.qty2).
                            END.
                            ELSE
                            DO:
                                IF s1-list.qty NE s1-list.qty0 THEN
                                    s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                                ELSE
                                    s1-list.qty2 = s1-list.qty.
                                IF NUM-ENTRIES(dml-artdep.chginit,";") GT 1 THEN
                                    dml-artdep.chginit = dml-artdep.chginit + ";" + STRING(s1-list.qty2).
                                ELSE
                                    dml-artdep.chginit = dml-artdep.chginit + ";" + docu-nr + ";" + STRING(s1-list.qty2).
                            END.
                        END.
                        ELSE 
                        DO:
                            IF NUM-ENTRIES(dml-artdep.chginit,";") GT 2 THEN
                            DO:
                                s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                                ENTRY(3, dml-artdep.chginit, ";") = STRING(s1-list.qty2).
                            END.
                            ELSE
                            DO:
                                s1-list.qty2 = s1-list.qty2 + s1-list.qty.
                                IF NUM-ENTRIES(dml-artdep.chginit,";") GT 1 THEN
                                    dml-artdep.chginit = dml-artdep.chginit + ";" + STRING(s1-list.qty2).
                                ELSE
                                    dml-artdep.chginit = dml-artdep.chginit + ";" + docu-nr + ";" + STRING(s1-list.qty2).
                            END.
                            FIND CURRENT dml-artdep NO-LOCK. 
                        END. 
                    END.
                END. 
            END.
            /*FOR EACH dml-artdep WHERE dml-artdep.datum = selected-date 
                AND dml-artdep.departement = curr-dept:
            
                IF dml-artdep.chginit MATCHES "*!*" THEN
                    dml-artdep.chginit = REPLACE(dml-artdep.chginit,"!","").
            END.*/
        END. 
    END. 
END.
