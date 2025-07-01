/* Oscar (04/03/25) - A85189 - Copy last day dml for multi dml  */
DEFINE TEMP-TABLE c-list 
    FIELD zwkum    AS INTEGER INITIAL 0 
    FIELD grp      AS CHAR FORMAT "x(22)" COLUMN-LABEL "Group" 
    FIELD artnr    LIKE l-artikel.artnr 
    FIELD bezeich  AS CHAR FORMAT "x(38)" COLUMN-LABEL "Description" 
    FIELD qty      AS DECIMAL  FORMAT ">>,>>9.99" LABEL "Ordered Qty" 
    FIELD a-qty    AS DECIMAL  FORMAT "->>,>>9.99" LABEL "Add Qty" 
    FIELD price    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Unit Price"
    FIELD l-price  AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Last Purchase Price" /*Naufal*/
    FIELD unit     AS CHAR FORMAT "x(3)" LABEL "D-Unit" /*SIS 05/12/12 */
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
    FIELD remark   AS CHAR FORMAT "x(180)" LABEL "Remark"
    /*NAUFAL 150321 - add field for stock oh value*/
    FIELD soh      AS DECIMAL FORMAT ">,>>>,>>9.99" LABEL "Actual Qty"
    /*end*/ 
    FIELD dml-nr   AS CHARACTER
    FIELD qty2     AS DECIMAL FORMAT ">>,>>9.99" LABEL "Move Qty" .
    
DEFINE TEMP-TABLE supply-list
    FIELD lief-nr  AS INTEGER
    FIELD supplier AS CHAR
    FIELD telefon  LIKE l-lieferant.telefon           /*MT 01/07/12 */
    FIELD fax      LIKE l-lieferant.fax               /*MT 01/07/12 */
    FIELD namekontakt LIKE l-lieferant.namekontakt.   /*MT 01/07/12 */

DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER curr-dept      AS INT.
DEF INPUT  PARAMETER selected-date  AS DATE.
DEF INPUT  PARAMETER dml-no         AS CHARACTER.
DEF OUTPUT PARAMETER approve-flag   AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR c-list.
DEF OUTPUT PARAMETER TABLE FOR supply-list.

DEFINE BUFFER d-art       FOR dml-art. 
DEFINE BUFFER d-artdep    FOR dml-artdep.
DEFINE BUFFER breslin     FOR reslin-queasy.
DEFINE BUFFER buff-queasy FOR queasy.

DEFINE VARIABLE dml-counter AS INTEGER NO-UNDO.
DEFINE VARIABLE copy-mode   AS CHARACTER NO-UNDO.
DEFINE VARIABLE liefNo      AS INTEGER NO-UNDO.

IF dml-no EQ ? OR dml-no EQ " " THEN
    dml-no = "D" + STRING(curr-dept, "99") + SUBSTRING(STRING(YEAR((selected-date - 1)), "9999"), 3, 2)
           + STRING(MONTH((selected-date - 1)), "99") + STRING(DAY((selected-date - 1)), "99") + STRING(1, "999").

RUN copy-articles.

PROCEDURE copy-articles:
    DEFINE VARIABLE liefNo      AS INTEGER NO-UNDO.
  
    FOR EACH c-list: 
        DELETE c-list. 
    END. 
    
    FOR EACH supply-list:
        DELETE supply-list.
    END.
    
    IF curr-dept = 0 THEN 
    DO:
        FOR EACH dml-art WHERE dml-art.datum = (selected-date - 1) NO-LOCK,
            FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr NO-LOCK, 
            FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK: 
            
            RUN copy-from-dml-art.
        END. 
    END.
    ELSE 
    DO: 
        FIND FIRST reslin-queasy WHERE (NUM-ENTRIES(reslin-queasy.char3, ";") GE 2 AND ENTRY(2, reslin-queasy.char3, ";") EQ dml-no)
            AND reslin-queasy.date1 EQ (selected-date - 1)
            AND (NUM-ENTRIES(reslin-queasy.char1, ";") GE 2 AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept) NO-LOCK NO-ERROR.
        

        IF AVAILABLE reslin-queasy THEN
        DO:
            FIND FIRST l-artikel WHERE l-artikel.artnr = INT(ENTRY(1,reslin-queasy.char1,";")) NO-LOCK NO-ERROR.
            IF AVAILABLE l-artikel THEN
            DO:
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK NO-ERROR.
                IF AVAILABLE l-untergrup THEN 
                    copy-mode = "reslin-queasy".
            END.
        END.
        
        IF copy-mode EQ "" THEN
        DO:
            FIND FIRST dml-artdep WHERE ((NUM-ENTRIES(dml-artdep.chginit, ";") GE 2 AND ENTRY(2, dml-artdep.chginit, ";") EQ dml-no)
                OR (NUM-ENTRIES(dml-artdep.chginit, ";") GE 2 AND ENTRY(2, dml-artdep.chginit, ";") EQ "")
                OR (NUM-ENTRIES(dml-artdep.chginit, ";") EQ 1))
                AND dml-artdep.datum EQ (selected-date - 1)
                AND dml-artdep.departement EQ curr-dept NO-LOCK NO-ERROR.
            IF AVAILABLE dml-artdep THEN
            DO:
                copy-mode = "dml-artdep".
            END.
        END.

        IF copy-mode EQ "reslin-queasy" THEN
            RUN copy-from-reslin-queasy.
        ELSE IF copy-mode EQ "dml-artdep" THEN
            RUN copy-from-dml-artdep.
    END.

    approve-flag = NO.
END. 

PROCEDURE copy-from-dml-art:
    CREATE c-list. 
    ASSIGN 
        c-list.artnr      = l-artikel.artnr 
        c-list.grp        = l-untergrup.bezeich 
        c-list.zwkum      = l-untergrup.zwkum 
        c-list.bezeich    = l-artikel.bezeich 
        c-list.qty        = dml-art.anzahl 
        c-list.price      = dml-art.einzelpreis
        c-list.l-price    = l-artikel.ek-letzter /*Naufal*/
        c-list.unit       = l-artikel.traubensorte 
        c-list.content    = l-artikel.inhalt 
        c-list.deliver    = dml-art.geliefert 
        c-list.amount     = c-list.qty * c-list.price 
        c-list.qty1       = c-list.qty 
        c-list.price1     = c-list.price 
        c-list.id         = ENTRY(1, dml-art.userinit, ";") 
        c-list.cid        = REPLACE(ENTRY(1, dml-art.chginit, ";"), "!", "") 
        c-list.dept       = curr-dept.

    IF NUM-ENTRIES(dml-art.chginit, ";") GT 1 THEN
        c-list.dml-nr     = ENTRY(2, dml-art.chginit, ";").

    IF NUM-ENTRIES(dml-art.chginit, ";") GT 2 THEN
        c-list.qty2       = DECIMAL(ENTRY(3, dml-art.chginit, ";")).    

    /*NAUFAL 150321 - add validation for stock oh value*/
    FIND FIRST l-bestand WHERE l-bestand.artnr = dml-art.artnr 
        AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE l-bestand THEN
    DO:
        c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                   - l-bestand.anz-ausgang.
    END.
    /*end*/
    
    /*ITA 170518 --> add remark*//* 
    FIND FIRST queasy WHERE queasy.KEY = 202 
        AND queasy.number1 = 0 AND queasy.number2 = dml-art.artnr
        AND queasy.date1 = dml-art.datum
    */
    /* FIND FIRST queasy WHERE queasy.KEY = 202 
        AND queasy.number1 = 0
        AND queasy.number2 = dml-art.artnr
        AND queasy.number3 = 1
        AND queasy.date1 = dml-art.datum NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN 
    DO:
        ASSIGN c-list.remark = queasy.char1.
    END. */
    /*end*/

    /* CREATE queasy.
    ASSIGN 
        queasy.KEY = 202
        queasy.number1 = 0
        queasy.number2 = dml-art.artnr
        queasy.number3 = 1
        queasy.date1 = selected-date
        queasy.char1 = c-list.remark
    .
    
    CREATE d-art. 
    ASSIGN
        d-art.artnr       = dml-art.artnr 
        d-art.datum       = selected-date 
        d-art.userinit    = user-init
        d-art.anzahl      = dml-art.anzahl 
        d-art.einzelpreis = dml-art.einzelpreis
    .  */
END.

PROCEDURE copy-from-reslin-queasy:

    dml-counter = INTEGER(SUBSTRING(dml-no, 10, 3)).

    FOR EACH reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
        AND reslin-queasy.date1 EQ (selected-date - 1)
        AND (NUM-ENTRIES(reslin-queasy.char1, ";") GE 2 AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept)
        AND reslin-queasy.number2 EQ dml-counter NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = INT(ENTRY(1,reslin-queasy.char1,";")) NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK:

        CREATE c-list.
        ASSIGN
            c-list.zwkum    = l-untergrup.zwkum
            c-list.grp      = l-untergrup.bezeich
            c-list.artnr    = l-artikel.artnr
            c-list.bezeich  = l-artikel.bezeich
            c-list.qty      = reslin-queasy.deci2
            c-list.price    = reslin-queasy.deci1
            c-list.l-price  = l-artikel.ek-letzter
            c-list.unit     = l-artikel.traubensorte 
            c-list.content  = l-artikel.inhalt 
            c-list.amount   = c-list.qty * c-list.price
            c-list.deliver  = reslin-queasy.deci3
            c-list.dept     = curr-dept
            c-list.id       = ENTRY(1, reslin-queasy.char2, ";") 
            c-list.cid      = ENTRY(1, reslin-queasy.char3, ";")
            c-list.price1   = c-list.price
            c-list.qty1     = c-list.qty
        . 

        IF NUM-ENTRIES(reslin-queasy.char3, ";") GT 2 THEN
            c-list.qty2 = DECIMAL(ENTRY(3, reslin-queasy.char3, ";")).

        FIND FIRST l-bestand WHERE l-bestand.artnr = INT(ENTRY(1,reslin-queasy.char1,";"))
            AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE l-bestand THEN
        DO:
            c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                       - l-bestand.anz-ausgang.
        END.

        FIND FIRST queasy WHERE queasy.KEY = 202 
            AND queasy.number1 = INT(ENTRY(2,reslin-queasy.char1,";"))
            AND queasy.number2 = INT(ENTRY(1,reslin-queasy.char1,";"))
            AND queasy.number3 = dml-counter
            AND queasy.date1 = reslin-queasy.date1 NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN 
        DO:
            ASSIGN c-list.remark = queasy.char1.
        END.

        liefNo = 0.
        liefNo = INTEGER(ENTRY(2, reslin-queasy.char2, ";")) NO-ERROR.

        IF liefNo NE 0 THEN
        DO:
            FIND FIRST l-lieferant WHERE l-lieferant.lief-nr EQ liefNo NO-LOCK NO-ERROR.
            IF AVAILABLE l-lieferant THEN
                ASSIGN
                    c-list.supplier = l-lieferant.firma
                    c-list.lief-nr  = liefNo.
        END.
    END.
END.

PROCEDURE copy-from-dml-artdep:

    dml-counter = 1.

    FOR EACH dml-artdep WHERE dml-artdep.datum EQ (selected-date - 1)
        AND dml-artdep.departement EQ curr-dept NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = dml-artdep.artnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK:

        CREATE c-list.
        ASSIGN
            c-list.zwkum    = l-untergrup.zwkum
            c-list.grp      = l-untergrup.bezeich
            c-list.artnr    = l-artikel.artnr 
            c-list.bezeich  = l-artikel.bezeich
            c-list.qty      = dml-artdep.anzahl
            c-list.price    = dml-artdep.einzelpreis
            c-list.l-price  = l-artikel.ek-letzter
            c-list.unit     = l-artikel.traubensorte 
            c-list.content  = l-artikel.inhalt 
            c-list.amount   = c-list.qty * c-list.price
            c-list.deliver  = dml-artdep.geliefert
            c-list.dept     = curr-dept
            c-list.id       = ENTRY(1, dml-artdep.userinit, ";") 
            c-list.price1   = c-list.price
            c-list.qty1     = c-list.qty
        . 

        IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 1 THEN
            c-list.cid     = REPLACE(ENTRY(1, dml-artdep.chginit, ";"),"!","").
        ELSE
            c-list.cid    = REPLACE(dml-artdep.chginit,"!","").

        IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 2 THEN
            c-list.qty2 = DECIMAL(ENTRY(3, dml-artdep.chginit, ";")).

        FIND FIRST l-bestand WHERE l-bestand.artnr = dml-artdep.artnr
            AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE l-bestand THEN
        DO:
            c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                       - l-bestand.anz-ausgang.
        END.

        FIND FIRST queasy WHERE queasy.KEY = 202 
            AND queasy.number1 = dml-artdep.departement 
            AND queasy.number2 = dml-artdep.artnr
            AND queasy.number3 = dml-counter
            AND queasy.date1 = dml-artdep.datum NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN DO:
            ASSIGN c-list.remark = queasy.char1.
        END.

        liefNo = 0.
        liefNo = INTEGER(ENTRY(2, dml-artdep.userinit, ";")) NO-ERROR.

        IF liefNo NE 0 THEN
        DO:
            FIND FIRST l-lieferant WHERE l-lieferant.lief-nr EQ liefNo NO-LOCK NO-ERROR.
            IF AVAILABLE l-lieferant THEN
                ASSIGN
                    c-list.supplier = l-lieferant.firma
                    c-list.lief-nr  = liefNo.
        END.
    END.
END.

