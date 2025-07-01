DEFINE TEMP-TABLE depreciation-asset
    FIELD COA               LIKE fa-grup.fibukonto
    FIELD order-date        LIKE fa-ordheader.Order-Date
    FIELD order-number      LIKE fa-ordheader.Order-Nr 
    FIELD desc1             LIKE mathis.name
    FIELD qty               AS CHAR /* LIKE fa-order.order-qty */
    FIELD price             AS CHAR /* LIKE fa-order.order-price */
    FIELD amount            AS CHAR /* LIKE fa-order.order-amount */
    FIELD depn-value        AS CHAR /* LIKE fa-artikel.depn-wert */
    FIELD book-value        AS CHAR /* LIKE fa-artikel.book-wert */
    FIELD acc-depn          AS CHAR /* LIKE fa-artikel.anz-depn */
    FIELD date-rcv          LIKE fa-ordheader.close-date
    FIELD first-depn        LIKE fa-artikel.first-depn
    .


DEFINE TEMP-TABLE payload-list     
    FIELD depn-month  AS CHAR
    FIELD sorttype    AS INTEGER
    FIELD last-nr     AS INTEGER
    FIELD num-data    AS INTEGER
    FIELD mode        AS INTEGER
    .

DEFINE TEMP-TABLE output-list
    FIELD curr-nr           AS INTEGER
    .

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR depreciation-asset.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE tot-amount AS DECIMAL. 
DEFINE VARIABLE tot-depn-value AS DECIMAL. 
DEFINE VARIABLE tot-book-value AS DECIMAL. 
DEFINE VARIABLE tot-acc-depn AS INTEGER. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE qty AS INT.
DEFINE VARIABLE price AS DECIMAL.
DEFINE VARIABLE amount AS DECIMAL. 
DEFINE VARIABLE counter AS INTEGER INITIAL 0.
DEFINE VARIABLE counter-num-data AS INTEGER INITIAL 0.
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 

FIND FIRST payload-list.
CREATE output-list.


mm = INTEGER(SUBSTR(payload-list.depn-month,1,2)). 
yy = INTEGER(SUBSTR(payload-list.depn-month,3,4)). 
datum = DATE(mm, 1, yy).

mm = mm + 1. 

IF mm = 13 THEN
DO:
    mm = 1.
    yy = yy + 1.
END.
datum = DATE(mm, 1, yy) - 1.


counter-num-data = payload-list.num-data.
IF payload-list.mode EQ 1 THEN 
DO:
    IF payload-list.sorttype EQ 1 THEN
    DO:
        FOR EACH fa-artikel NO-LOCK,
            FIRST mathis WHERE mathis.nr EQ fa-artikel.nr NO-LOCK,
            FIRST queasy WHERE queasy.key EQ 348 AND queasy.date1 EQ datum 
                AND queasy.number1 EQ fa-artikel.nr NO-LOCK BY fa-artikel.nr:

            IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
            RUN create-list.
            counter = counter + 1. 
            output-list.curr-nr = mathis.nr.
        END.
    END.
    /* Api for pagination */
    ELSE
    DO:
        IF payload-list.last-nr NE ? AND payload-list.last-nr NE 0 THEN
        DO:
            FOR EACH fa-artikel WHERE fa-artikel.nr GT payload-list.last-nr NO-LOCK,
                FIRST mathis WHERE mathis.nr EQ fa-artikel.nr NO-LOCK,
                FIRST queasy WHERE queasy.key EQ 348 AND queasy.date1 EQ datum 
                    AND queasy.number1 EQ fa-artikel.nr NO-LOCK BY fa-artikel.nr:

                IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
                RUN create-list.
                counter = counter + 1. 
                output-list.curr-nr = mathis.nr.
            END.
        END.
    END.
END.
ELSE /* Query all depreciation list asset  */
DO:
    FOR EACH fa-artikel NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-artikel.nr NO-LOCK,
        FIRST queasy WHERE queasy.key EQ 348 AND queasy.date1 EQ datum 
            AND queasy.number1 EQ fa-artikel.nr NO-LOCK BY fa-artikel.nr: 
        RUN create-list.
    END.
END.

FIND FIRST depreciation-asset NO-ERROR.
IF AVAILABLE depreciation-asset THEN
DO:
    CREATE depreciation-asset.
    ASSIGN
        depreciation-asset.desc1        = "T O T A L"
        depreciation-asset.amount       = STRING(tot-amount, "->>,>>>,>>>,>>>,>>9.99")
        depreciation-asset.depn-value   = STRING(tot-depn-value, ">>,>>>,>>>,>>9.99")
        depreciation-asset.book-value   = STRING(tot-book-value, ">>,>>>,>>>,>>9.99")
        depreciation-asset.acc-depn     = STRING(tot-acc-depn, ">>9").
END.


PROCEDURE create-list:
    FIND FIRST fa-order WHERE fa-order.fa-nr = fa-artikel.nr NO-LOCK NO-ERROR.
    IF AVAILABLE fa-order THEN
    DO:
        FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr EQ fa-order.order-nr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-ordheader THEN
        DO:
            CREATE depreciation-asset.
            ASSIGN
            depreciation-asset.COA          = fa-artikel.fibukonto
            depreciation-asset.order-date   = fa-ordheader.Order-Date
            depreciation-asset.order-number = fa-ordheader.Order-Nr 
            depreciation-asset.desc1        = mathis.name
            depreciation-asset.qty          = STRING(fa-order.order-qty, "->,>>>,>>9") /* STRING(fa-order.order-qty, "->,>>>,>>9")  fa-order.order-qty */
            depreciation-asset.price        = STRING(fa-order.order-price, "->>,>>>,>>>,>>>,>>9.99") /*STRING(fa-order.order-price, "->>,>>>,>>>,>>>,>>9.99")*/
            depreciation-asset.amount       = STRING(fa-order.order-amount, "->>,>>>,>>>,>>>,>>9.99") /*STRING(fa-order.order-amount, "->>,>>>,>>>,>>>,>>9.99")*/
            depreciation-asset.depn-value   = STRING(queasy.deci1, ">>,>>>,>>>,>>9.99") /*ENTRY(1, queasy.char1, "|")*/
            depreciation-asset.book-value   = STRING(queasy.deci2, ">>,>>>,>>>,>>9.99") /*ENTRY(3, queasy.char1, "|")*/
            depreciation-asset.acc-depn     = STRING(queasy.number3, ">>9") /*ENTRY(2, queasy.char1, "|")*/
            /*
            depreciation-asset.depn-value   = STRING(fa-artikel.depn-wert, ">>,>>>,>>>,>>9.99")
            depreciation-asset.book-value   = STRING(fa-artikel.book-wert, ">>,>>>,>>>,>>9.99")
            depreciation-asset.acc-depn     = STRING(fa-artikel.anz-depn, ">>9")
            */
            depreciation-asset.date-rcv     = fa-ordheader.close-date
            depreciation-asset.first-depn   = fa-artikel.first-depn.
        
            tot-amount = tot-amount + fa-order.order-amount. /*fa-order.order-amount.*/
            tot-depn-value = tot-depn-value + queasy.deci1. /*fa-artikel.depn-wert.*/
            tot-book-value = tot-book-value + queasy.deci2. /*fa-artikel.book-wert.*/ 
            tot-acc-depn = tot-acc-depn +  queasy.number3. /*fa-artikel.anz-depn.*/
        END.
    END.
    ELSE
    DO:
        FIND FIRST fa-op WHERE fa-op.nr EQ fa-artikel.nr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-op THEN
        DO:
            CREATE depreciation-asset.
            ASSIGN
            depreciation-asset.COA          = fa-artikel.fibukonto
            /*depreciation-asset.order-date   = fa-ordheader.Order-Date */
            depreciation-asset.order-number = fa-op.docu-nr  /*fa-ordheader.Order-Nr*/
            depreciation-asset.desc1        = mathis.name
            depreciation-asset.qty          = STRING(fa-op.anzahl, "->,>>>,>>9") /* STRING(fa-order.order-qty, "->,>>>,>>9")  fa-order.order-qty */
            depreciation-asset.price        = STRING(fa-op.einzelpreis, "->>,>>>,>>>,>>>,>>9.99") /*STRING(fa-order.order-price, "->>,>>>,>>>,>>>,>>9.99")*/
            depreciation-asset.amount       = STRING(fa-op.warenwert, "->>,>>>,>>>,>>>,>>9.99") /*STRING(fa-order.order-amount, "->>,>>>,>>>,>>>,>>9.99")*/
            depreciation-asset.depn-value   = STRING(queasy.deci1, ">>,>>>,>>>,>>9.99") /*ENTRY(1, queasy.char1, "|")*/
            depreciation-asset.book-value   = STRING(queasy.deci2, ">>,>>>,>>>,>>9.99") /*ENTRY(3, queasy.char1, "|")*/
            depreciation-asset.acc-depn     = STRING(queasy.number3, ">>9") /*ENTRY(2, queasy.char1, "|")*/
            depreciation-asset.date-rcv     = fa-op.datum /*fa-ordheader.close-date */
            depreciation-asset.first-depn   = fa-artikel.first-depn.
        
            tot-amount = tot-amount + fa-op.warenwert. /*fa-order.order-amount.*/
            tot-depn-value = tot-depn-value + queasy.deci1. /*fa-artikel.depn-wert.*/
            tot-book-value = tot-book-value + queasy.deci2. /*fa-artikel.book-wert.*/ 
            tot-acc-depn = tot-acc-depn +  queasy.number3. /*fa-artikel.anz-depn.*/
        END.
        ELSE
        DO:
            CREATE depreciation-asset.
            ASSIGN
            depreciation-asset.COA          = fa-artikel.fibukonto
            /*depreciation-asset.order-date   = fa-ordheader.Order-Date 
            depreciation-asset.order-number = fa-op.docu-nr  /*fa-ordheader.Order-Nr*/*/
            depreciation-asset.desc1        = mathis.name
            /*
            depreciation-asset.qty          = STRING(fa-op.anzahl, "->,>>>,>>9") /* STRING(fa-order.order-qty, "->,>>>,>>9")  fa-order.order-qty */
            depreciation-asset.price        = STRING(fa-op.einzelpreis, "->>,>>>,>>>,>>>,>>9.99") /*STRING(fa-order.order-price, "->>,>>>,>>>,>>>,>>9.99")*/
            depreciation-asset.amount       = STRING(fa-op.warenwert, "->>,>>>,>>>,>>>,>>9.99") /*STRING(fa-order.order-amount, "->>,>>>,>>>,>>>,>>9.99")*/*/
            depreciation-asset.depn-value   = STRING(queasy.deci1, ">>,>>>,>>>,>>9.99") /*ENTRY(1, queasy.char1, "|")*/
            depreciation-asset.book-value   = STRING(queasy.deci2, ">>,>>>,>>>,>>9.99") /*ENTRY(3, queasy.char1, "|")*/
            depreciation-asset.acc-depn     = STRING(queasy.number3, ">>9") /*ENTRY(2, queasy.char1, "|")*/
            /*depreciation-asset.date-rcv     = fa-ordheader.close-date*/
            depreciation-asset.first-depn   = fa-artikel.first-depn.
            
            /*
            tot-amount = tot-amount + fa-op.warenwert. /*fa-order.order-amount.*/*/
            tot-depn-value = tot-depn-value + queasy.deci1. /*fa-artikel.depn-wert.*/
            tot-book-value = tot-book-value + queasy.deci2. /*fa-artikel.book-wert.*/ 
            tot-acc-depn = tot-acc-depn +  queasy.number3. /*fa-artikel.anz-depn.*/
        END.
    END.
END.
