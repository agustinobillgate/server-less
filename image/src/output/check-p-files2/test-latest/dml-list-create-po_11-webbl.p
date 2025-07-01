DEFINE TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE s-list 
    FIELD s-flag   AS CHAR FORMAT "x(1)" INITIAL "" COLUMN-LABEL "" 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD artnr    LIKE l-artikel.artnr 
    FIELD bezeich  AS CHAR FORMAT "x(32)" COLUMN-LABEL "Description" 
    FIELD qty      AS DECIMAL FORMAT ">>,>>9.99" LABEL "Ordered Qty" 
    FIELD qty0     AS DECIMAL 
    FIELD price    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Unit Price"
    FIELD qty2     AS DECIMAL. 
 
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
    /*NAUFAL 150321 - add field for stock oh value*/
    FIELD soh      AS DECIMAL FORMAT ">,>>>,>>9.99" LABEL "Actual Qty" 
    /*end*/
    FIELD dml-nr   AS CHARACTER
    FIELD qty2     AS DECIMAL FORMAT ">>,>>9.99" LABEL "Move to PO Qty".

DEFINE INPUT PARAMETER TABLE FOR s-list.
DEFINE INPUT PARAMETER TABLE FOR c-list.
DEFINE INPUT PARAMETER l-orderhdr-recid AS INT.
DEFINE INPUT PARAMETER l-lieferant-recid AS INT.
DEFINE INPUT PARAMETER lief-nr AS INTEGER. 
DEFINE INPUT PARAMETER currdate AS DATE.
DEFINE INPUT PARAMETER selected-date AS DATE.
DEFINE INPUT PARAMETER bediener-username AS CHAR.
DEFINE INPUT PARAMETER crterm AS INT.
DEFINE INPUT PARAMETER local-nr AS INT.
DEFINE INPUT PARAMETER curr-dept AS INT.
DEFINE INPUT PARAMETER dunit-price AS LOGICAL.
DEFINE INPUT PARAMETER dml-hdr-remark AS CHARACTER. /* Oscar (25/02/25) - A36EF3 - save dml header remark */

DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.

DEFINE VARIABLE docu-nr AS CHAR NO-UNDO.
DEFINE VARIABLE t-qty   AS DECIMAL NO-UNDO.
DEFINE VARIABLE counter AS INTEGER NO-UNDO.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = l-orderhdr-recid.
FIND FIRST l-lieferant WHERE RECID(l-lieferant) = l-lieferant-recid.

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
    

/*RUN new-dml-number.*/
RUN create-po.

IF AVAILABLE l-orderhdr THEN /*Alder - Serverless - Issue 565*/
DO:
    FIND CURRENT l-orderhdr NO-LOCK.

    CREATE t-l-orderhdr.
    BUFFER-COPY l-orderhdr TO t-l-orderhdr.

    ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).

    RELEASE l-orderhdr.
END.


PROCEDURE create-po: 
    DEFINE VARIABLE pos AS INTEGER INITIAL 0. 
    DEFINE VARIABLE answer AS LOGICAL INITIAL YES. 
    DEFINE buffer s1-list FOR s-list. 
    DEFINE buffer c1-list FOR c-list. 

    DO TRANSACTION:
        IF AVAILABLE l-orderhdr THEN /*Alder - Serverless - Issue 565*/
        DO:
            FIND CURRENT l-orderhdr EXCLUSIVE-LOCK. 
            ASSIGN 
                l-orderhdr.lief-nr = lief-nr 
                l-orderhdr.bestelldatum = currdate 
                l-orderhdr.lieferdatum = selected-date 
                l-orderhdr.besteller = bediener-username 
                l-orderhdr.lief-fax[1] = l-lieferant.fax 
                l-orderhdr.lief-fax[3] = dml-hdr-remark /* Oscar (06/03/25) - A36EF3 - Save remark from dml to PO */
                l-orderhdr.angebot-lief[2] = crterm 
                l-orderhdr.angebot-lief[3] = local-nr 
                l-orderhdr.gedruckt = ? 
                l-orderhdr.txtnr = curr-dept. 
            FIND CURRENT l-orderhdr NO-LOCK.
            
            CREATE l-order. 
            ASSIGN 
                l-order.docu-nr       = l-orderhdr.docu-nr 
                l-order.pos           = 0 
                l-order.bestelldatum  = currdate 
                l-order.lief-nr       = lief-nr 
                l-order.lief-fax[1]   = docu-nr
                l-order.op-art        = 2
                l-order.lief-fax[3]   = "DML". 
            
            FOR EACH s1-list WHERE s1-list.selected = YES: 
                FIND FIRST l-artikel WHERE l-artikel.artnr = s1-list.artnr NO-LOCK. 
                pos = pos + 1. 
                create l-order. 
                ASSIGN 
                    l-order.docu-nr      = l-orderhdr.docu-nr 
                    l-order.artnr        = l-artikel.artnr 
                    l-order.pos          = pos 
                    l-order.bestelldatum = l-orderhdr.bestelldatum 
                    l-order.lief-nr      = lief-nr 
                    l-order.op-art       = 2 
                    l-order.lief-fax[1]  = bediener-username 
                    l-order.lief-fax[3]  = l-artikel.traubensorte 
                    l-order.anzahl       = s1-list.qty 
                    l-order.einzelpreis  = s1-list.price 
                    l-order.txtnr        = l-artikel.lief-einheit /* Oscar (05/06/2025) - 5B3BE7 - fix mess qty */
                    l-order.flag         = YES
                    l-order.warenwert    = s1-list.qty * s1-list.price /* Oscar (05/06/2025) - 5B3BE7 - fix amount for PO */
                    l-order.quality      = STRING(0, "99.99 ") + STRING(0, "99.99") + STRING(0, " 99.99"). 
                /* IF l-artikel.lief-einheit NE 0 THEN 
                DO: 
                    l-order.warenwert = l-order.warenwert * l-artikel.lief-einheit. 
                    IF dunit-price THEN l-order.einzelpreis = l-order.einzelpreis 
                        * l-artikel.lief-einheit. 
                    l-order.txtnr = l-artikel.lief-einheit. 
                END. */

                FIND FIRST c1-list WHERE c1-list.artnr = s1-list.artnr.
                l-order.besteller      = c1-list.remark.
                
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
                            /*dml-art.anzahl = s1-list.qty0 - s1-list.qty. 
                            dml-art.chginit = REPLACE(dml-art.chginit,"!","").*/
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
                                /*dml-artdep.anzahl = s1-list.qty0 - s1-list.qty. 
                                dml-artdep.chginit = REPLACE(dml-artdep.chginit,"!","").*/
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
                                /*dml-artdep.anzahl = s1-list.qty0 - s1-list.qty. 
                                dml-artdep.chginit = REPLACE(dml-artdep.chginit,"!","").*/
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
            /* RELEASE l-orderhdr. */
        END. /*IF AVAILABLE l-orderhdr*/
    END. 
END. 

/*PROCEDURE new-dml-number: 
DEFINE BUFFER l-orderhdr1 FOR l-orderhdr. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE i AS INTEGER INITIAL 1. 
  s = "D" + STRING(curr-dept, "99") + SUBSTR(STRING(year(currdate)),3,2) 
      + STRING(month(currdate), "99") + STRING(day(currdate), "99"). 

  FOR EACH l-order WHERE l-order.pos = 0 AND 
      l-order.bestelldatum  = currdate AND l-order.lief-fax[1] MATCHES "D*"
      AND l-order.lief-fax[3]   = "DML" NO-LOCK 
      BY l-order.lief-fax[1] DESCENDING:
        i = INTEGER(SUBSTR(l-order.lief-fax[1],10,3)). 
        i = i + 1. 
        docu-nr = s + STRING(i, "999").         
        RETURN. 
  END.
  docu-nr = s + STRING(i, "999"). 
END.*/

/*
PROCEDURE create-po:
DEFINE VARIABLE pos AS INTEGER INITIAL 0. 
DEFINE buffer s1-list FOR s-list. 
DEFINE buffer c1-list FOR c-list. 
  DO TRANSACTION: 
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK. 
    ASSIGN 
      l-orderhdr.lief-nr = lief-nr 
      l-orderhdr.bestelldatum = currdate 
      l-orderhdr.lieferdatum = selected-date 
      l-orderhdr.besteller = bediener-username 
      l-orderhdr.lief-fax[1] = l-lieferant.fax 
      l-orderhdr.angebot-lief[2] = crterm 
      l-orderhdr.angebot-lief[3] = local-nr 
      l-orderhdr.gedruckt = ? 
      l-orderhdr.txtnr = curr-dept 
    . 
    FIND CURRENT l-orderhdr NO-LOCK. 
 
    CREATE l-order. 
    ASSIGN 
      l-order.docu-nr = l-orderhdr.docu-nr 
      l-order.pos = 0 
      l-order.bestelldatum = currdate 
      l-order.lief-nr = lief-nr 
      l-order.op-art = 2. 
 
    FOR EACH s1-list WHERE s1-list.selected = YES: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = s1-list.artnr NO-LOCK. 
      pos = pos + 1. 
      create l-order. 
      ASSIGN 
        l-order.docu-nr = l-orderhdr.docu-nr 
        l-order.artnr = l-artikel.artnr 
        l-order.pos = pos 
        l-order.bestelldatum = l-orderhdr.bestelldatum 
        l-order.lief-nr = lief-nr 
        l-order.op-art = 2 
        l-order.lief-fax[1] = bediener-username 
        l-order.lief-fax[3] = l-artikel.traubensort 
        l-order.anzahl = s1-list.qty 
        l-order.einzelpreis = s1-list.price 
        l-order.txtnr = 1 
        l-order.flag = dunit-price 
        l-order.warenwert = s1-list.qty * s1-list.price 
        l-order.quality = STRING(0, "99.99 ") + STRING(0, "99.99") 
          + STRING(0, " 99.99") 
      . 
      IF l-artikel.lief-einheit NE 0 THEN 
      DO: 
        l-order.warenwert = l-order.warenwert * l-artikel.lief-einheit. 
        IF dunit-price THEN l-order.einzelpreis = l-order.einzelpreis 
          * l-artikel.lief-einheit. 
        l-order.txtnr = l-artikel.lief-einheit. 
      END.
      FIND FIRST c1-list WHERE c1-list.artnr = s1-list.artnr. 
      IF s1-list.qty = s1-list.qty0 THEN DELETE c1-list. 
      ELSE c1-list.qty = s1-list.qty0 - s1-list.qty. 
 
      IF curr-dept = 0 THEN 
      DO: 
        FIND FIRST dml-art WHERE dml-art.artnr = s1-list.artnr 
          AND dml-art.datum = selected-date EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE dml-art THEN 
        DO: 
          IF s1-list.qty = s1-list.qty0 THEN DELETE dml-art. 
          ELSE 
          DO: 
            dml-art.anzahl = s1-list.qty0 - s1-list.qty. 
            FIND CURRENT dml-art NO-LOCK. 
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
          IF s1-list.qty = s1-list.qty0 THEN DELETE dml-artdep. 
          ELSE 
          DO: 
            dml-artdep.anzahl = s1-list.qty0 - s1-list.qty. 
            FIND CURRENT dml-artdep NO-LOCK. 
          END. 
        END. 
      END. 
    END. 
  END. 
END. 
*/
