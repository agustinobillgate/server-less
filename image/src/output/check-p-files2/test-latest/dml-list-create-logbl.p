DEFINE TEMP-TABLE c-list 
    FIELD zwkum    AS INTEGER INITIAL 0 
    FIELD grp      AS CHAR    FORMAT "x(22)" COLUMN-LABEL "Group" 
    FIELD artnr    LIKE l-artikel.artnr 
    FIELD bezeich  AS CHAR    FORMAT "x(38)" COLUMN-LABEL "Description" 
    FIELD qty      AS DECIMAL FORMAT ">>,>>9.99" LABEL "Ordered Qty" 
    FIELD a-qty    AS DECIMAL FORMAT "->>,>>9.99" LABEL "Add Qty" 
    FIELD price    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Unit Price"
    FIELD l-price  AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Last Purchase Price" /*Naufal*/
    FIELD unit     AS CHAR    FORMAT "x(3)" LABEL "D-Unit" /*SIS 05/12/12 */
    FIELD content  AS DECIMAL FORMAT ">>,>>9.99" LABEL "Content" 
    FIELD amount   AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" LABEL "Amount" 
    FIELD deliver  AS DECIMAL FORMAT ">>,>>9.99" LABEL "Delivered" 
    FIELD dept     AS INTEGER FORMAT ">>" LABEL "Dept" 
    FIELD supplier AS CHAR    FORMAT "x(32)" LABEL "Supplier"
    FIELD id       AS CHAR    FORMAT "x(4)" LABEL "ID" 
    FIELD cid      AS CHAR    FORMAT "x(4)" LABEL "CID" 
    FIELD price1   AS DECIMAL 
    FIELD qty1     AS DECIMAL
    FIELD lief-nr  AS INTEGER
    FIELD approved AS LOGICAL INIT NO
    FIELD remark   AS CHAR    FORMAT "x(180)" LABEL "Remark"
    /*NAUFAL 120321 - Testing add field for stock oh value*/
    FIELD soh      AS DECIMAL FORMAT ">,>>>,>>9.99" LABEL "Actual Qty"
    FIELD dml-nr   AS CHARACTER
    FIELD qty2     AS DECIMAL.

DEFINE INPUT PARAMETER curr-flag    AS CHARACTER   NO-UNDO.
DEFINE INPUT PARAMETER bediener-nr  AS INTEGER     NO-UNDO.
DEFINE INPUT PARAMETER curr-dept    AS INTEGER     NO-UNDO.
DEFINE INPUT PARAMETER curr-date    AS DATE        NO-UNDO.
DEFINE INPUT PARAMETER prev-qty     AS INTEGER     NO-UNDO.
DEFINE INPUT PARAMETER prev-amt     AS INTEGER     NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR c-list.

DEFINE VARIABLE curr-qty AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-amt AS INTEGER NO-UNDO.
DEFINE VARIABLE t-qty    AS INTEGER NO-UNDO.
DEFINE VARIABLE t-amt    AS INTEGER NO-UNDO.

IF curr-flag EQ "new" THEN
DO:
    DO TRANSACTION:
        CREATE res-history. 
        ASSIGN 
            res-history.nr = bediener-nr 
            res-history.datum = TODAY 
            res-history.zeit = TIME 
            res-history.aenderung = "Add DML[" + STRING(curr-date) + "] Department[" + STRING(curr-dept) + "]".
            res-history.action = "DML".
        FIND CURRENT res-history NO-LOCK. 
        RELEASE res-history. 
    END.
END.
ELSE IF curr-flag EQ "chg" THEN
DO:
    /* Malik Serverless 567 Comment - Change query methode 
    /*MNaufal 130123 - add validation to get qty and amt value for logfile*/
    FIND FIRST c-list WHERE c-list.qty NE 0 OR c-list.a-qty NE 0 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE c-list:
        ASSIGN
            t-qty = c-list.qty + c-list.a-qty
            t-amt = t-qty * c-list.price
            curr-qty = curr-qty + t-qty
            curr-amt = curr-amt + t-amt.
        FIND NEXT c-list WHERE c-list.qty NE 0 OR c-list.a-qty NE 0 NO-LOCK NO-ERROR.
    END. */
    /* Malik Serverless 567 New query methode */
    FOR EACH c-list WHERE c-list.qty NE 0 OR c-list.a-qty NE 0:
        ASSIGN
            t-qty = c-list.qty + c-list.a-qty
            t-amt = t-qty * c-list.price
            curr-qty = curr-qty + t-qty
            curr-amt = curr-amt + t-amt.
    END.
    
    DO TRANSACTION:
        CREATE res-history. 
        ASSIGN 
            res-history.nr = bediener-nr 
            res-history.datum = TODAY 
            res-history.zeit = TIME 
            res-history.aenderung = "Modify DML[" + STRING(curr-date) + "] Dept[" + STRING(curr-dept) + "] | Total Price From: " + STRING(prev-amt)
                                  + " To Total Price: " + STRING(curr-amt) + " | Total Qty From: " + STRING(prev-qty) + " To Total Qty: " + STRING(curr-qty).
            res-history.action = "DML".
        FIND CURRENT res-history NO-LOCK. 
        RELEASE res-history.
    END.
END.
