DEFINE TEMP-TABLE supply-list
    FIELD lief-nr  AS INTEGER
    FIELD supplier AS CHAR
    FIELD telefon  LIKE l-lieferant.telefon           /*MT 01/07/12 */
    FIELD fax      LIKE l-lieferant.fax               /*MT 01/07/12 */
    FIELD namekontakt LIKE l-lieferant.namekontakt.   /*MT 01/07/12 */

DEFINE TEMP-TABLE c-list 
    FIELD zwkum    AS INTEGER INITIAL 0 
    FIELD grp      AS CHAR    FORMAT "x(22)" COLUMN-LABEL "Group" 
    FIELD artnr    LIKE l-artikel.artnr 
    FIELD bezeich  AS CHAR    FORMAT "x(38)" COLUMN-LABEL "Description" 
    FIELD qty      AS DECIMAL FORMAT ">>,>>9.99" LABEL "Ordered Qty" 
    FIELD a-qty    AS DECIMAL FORMAT "->>,>>9.99" LABEL "Add Qty" 
    FIELD price    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Unit Price"
    FIELD l-price  AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Last Purchase Price" /*Naufal*/
    FIELD unit     AS CHAR FORMAT "x(3)" LABEL "Unit" 
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
    FIELD remark   AS CHAR
    /*NAUFAL 120321 - Testing add field for stock oh value*/
    FIELD soh      AS DECIMAL FORMAT ">,>>>,>>9.99" LABEL "Actual Qty"
    /*end*/
    FIELD dml-nr   AS CHARACTER
    FIELD qty2     AS DECIMAL
    FIELD app-id   AS CHARACTER
.

DEFINE TEMP-TABLE dml-list
    FIELD counter   AS INTEGER
    FIELD dept      AS CHARACTER
    FIELD id        AS CHARACTER
    FIELD approved  AS LOGICAL INIT NO.

/* Oscar (11/04/25) - 4BF019 - change input method */
DEFINE TEMP-TABLE payload-list
    FIELD curr-dept     AS INT
    FIELD selected-date AS CHARACTER
    FIELD dml-no        AS CHARACTER.

/* Oscar (11/04/25) - 4BF019 - change output method */
DEFINE TEMP-TABLE response-list
    FIELD dml-hdr-remark AS CHARACTER
    FIELD dml-grand-total AS DECIMAL. /* Oscar (11/04/25) - 4BF019 - count grand total */
    
DEFINE INPUT PARAMETER TABLE FOR payload-list. /* Oscar (11/04/25) - 4BF019 - change input method */
DEFINE OUTPUT PARAMETER TABLE FOR supply-list.
DEFINE OUTPUT PARAMETER TABLE FOR c-list.
DEFINE OUTPUT PARAMETER TABLE FOR response-list. /* Oscar (11/04/25) - 4BF019 - change output method */

DEFINE VARIABLE curr-dept       AS INT.
DEFINE VARIABLE selected-date   AS DATE.
DEFINE VARIABLE dml-no          AS CHARACTER.
DEFINE VARIABLE dml-hdr-remark  AS CHARACTER. /* Oscar (25/02/25) - A36EF3 - show dml header remark */
DEFINE VARIABLE dml-grand-total AS DECIMAL INIT 0.

DEFINE VARIABLE dml-counter   AS INTEGER NO-UNDO.
DEFINE VARIABLE fill-dml-nr   AS CHARACTER NO-UNDO.
DEFINE VARIABLE dml-no-remark AS CHARACTER NO-UNDO.

/* Oscar (11/04/25) - 4BF019 - change input method */
FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        curr-dept     = payload-list.curr-dept
        dml-no        = payload-list.dml-no       
    .

    selected-date = DATE(INTEGER(SUBSTRING(payload-list.selected-date, 1, 2)), 
                         INTEGER(SUBSTRING(payload-list.selected-date, 4, 2)), 
                         2000 + INTEGER(SUBSTRING(payload-list.selected-date, 7, 2))).

    /* Oscar (05/05/2025) - C4393F - remark failed to show */
    IF dml-no NE ? AND dml-no NE "" THEN
        dml-counter = INT(SUBSTRING(dml-no, 11, 2)).
    ELSE
        dml-counter = 1.

    RUN create-it.

    CREATE response-list.
    ASSIGN
        response-list.dml-hdr-remark  = dml-hdr-remark
        response-list.dml-grand-total = dml-grand-total
    .
END.

PROCEDURE create-it: 
    DEFINE VARIABLE dept   AS INTEGER NO-UNDO. 
    DEFINE VARIABLE liefNo AS INTEGER NO-UNDO.
    DEFINE VARIABLE chginit AS CHARACTER NO-UNDO.

    DEFINE BUFFER b-artdep  FOR dml-artdep.
    DEFINE BUFFER breslin   FOR reslin-queasy.

    FOR EACH c-list: 
        DELETE c-list. 
    END.
    
    FOR EACH supply-list:
        DELETE supply-list.
    END.
    CREATE supply-list.

    IF dml-no EQ ? THEN
        dml-no-remark = "D" + STRING(curr-dept, "99") + SUBSTR(STRING(YEAR(selected-date)),3,2) 
               + STRING(MONTH(selected-date), "99") + STRING(DAY(selected-date), "99") + STRING(1, "999").
    ELSE
        dml-no-remark = dml-no.

    /* Start - Oscar (25/02/25) - A36EF3 - show dml header remark */
    FIND FIRST queasy WHERE queasy.KEY EQ 342
        AND queasy.char1 EQ dml-no-remark
        AND queasy.number1 EQ curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        dml-hdr-remark = queasy.char2.
    END.
    ELSE
    DO:
        dml-hdr-remark = "".
    END.
    /* End - Oscar (25/02/25) - A36EF3 - show dml header remark */
    
    IF curr-dept = 0 THEN DO:
        /*FOR EACH dml-art WHERE dml-art.datum = selected-date NO-LOCK,
            FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr 
              /*AND l-artikel.bestellt = YES*/ NO-LOCK,
            FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK:*/

        /*naufal - test validation for dml closed report*/
        FIND FIRST dml-art WHERE dml-art.datum = selected-date /*AND NUM-ENTRIES(dml-art.chginit,";") LT 2 ENTRY(2, dml-art.chginit, ";") EQ dml-no*/ NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE dml-art:
            FIND FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-artikel THEN DO:
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK NO-ERROR.
                IF AVAILABLE l-untergrup THEN DO:
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
                        c-list.content    = l-artikel.lief-einheit /* Oscar (05/06/2025) - 5B3BE7 - change content from receipt qty to mess qty */ 
                        c-list.deliver    = dml-art.geliefert / l-artikel.lief-einheit
                        c-list.amount     = c-list.qty * c-list.price 
                        c-list.qty1       = c-list.qty 
                        c-list.price1     = c-list.price 
                        c-list.id         = ENTRY(1, dml-art.userinit, ";") 
                        c-list.cid        = REPLACE(ENTRY(1, dml-art.chginit, ";"), "!", "") 
                        c-list.dept       = curr-dept.

                    dml-grand-total = dml-grand-total + c-list.amount. /* Oscar (11/04/25) - 4BF019 - count grand total */
                        
                    IF NUM-ENTRIES(dml-art.chginit, ";") GT 1 THEN
                        c-list.dml-nr     = ENTRY(2, dml-art.chginit, ";").

                    IF NUM-ENTRIES(dml-art.chginit, ";") GT 2 THEN
                        c-list.qty2       = DECIMAL(ENTRY(3, dml-art.chginit, ";")).
                    
                    
                    IF NUM-ENTRIES(dml-art.chginit, ";") GT 1 AND ENTRY(1, dml-art.chginit, ";") NE "" 
                        AND SUBSTR(ENTRY(1, dml-art.chginit, ";"),LENGTH(ENTRY(1, dml-art.chginit, ";"))) = "!" THEN
                        c-list.approved = YES.
                    ELSE IF dml-art.chginit NE "" AND SUBSTR(dml-art.chginit,LENGTH(dml-art.chginit)) = "!" THEN
                            c-list.approved = YES.

                    ASSIGN
                        liefNo = 0
                        liefNo = INTEGER(ENTRY(2, dml-art.userinit, ";")) NO-ERROR.
            
                    /*NAUFAL 120321 - Testing validation for add stock oh value*/
                    FIND FIRST l-bestand WHERE l-bestand.artnr = dml-art.artnr
                        AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE l-bestand THEN
                    DO:
                        /*NAUFAL 120321 - Testing assign value for stock oh*/
                        c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                                   - l-bestand.anz-ausgang.
                        /*end*/
                    END.
                    /*end*/
                    
                    /*ITA 170518 --> add remark*/
                    FIND FIRST queasy WHERE queasy.KEY = 202 
                    AND queasy.number1 = 0 
                    AND queasy.number2 = dml-art.artnr
                    AND queasy.number3 = dml-counter /* show independent remark for multi DML by Oscar (01 November 2024) - B2F68F */
                    AND queasy.date1 = dml-art.datum NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN DO:
                        ASSIGN c-list.remark = queasy.char1.
                    END.
                    /*end*/
                    
                    IF liefNo NE 0 THEN
                    DO:
                        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = liefNo
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE l-lieferant THEN
                        DO:
                            ASSIGN
                                c-list.supplier = l-lieferant.firma
                                c-list.lief-nr  = liefNo.
                            FIND FIRST supply-list WHERE supply-list.lief-nr = liefNo NO-ERROR.
                            IF NOT AVAILABLE supply-list THEN
                            DO:
                                CREATE supply-list.
                                ASSIGN 
                                    supply-list.lief-nr     = l-lieferant.lief-nr
                                    supply-list.supplier    = l-lieferant.firma  
                                    supply-list.telefon     = l-lieferant.telefon
                                    supply-list.fax         = l-lieferant.fax
                                    supply-list.namekontakt = l-lieferant.namekontakt.
                            END.
                        END.
                    END.
                END.
            END.            
            FIND NEXT dml-art WHERE dml-art.datum = selected-date AND SUBSTR(dml-art.chginit,LENGTH(dml-art.chginit)) NE "*" NO-LOCK NO-ERROR.
        END.
    END.
    ELSE 
    DO:
        FIND FIRST breslin WHERE breslin.KEY EQ "DML"
        AND breslin.date1 EQ selected-date
        AND INT(ENTRY(2,breslin.char1,";")) EQ curr-dept
        AND ENTRY(2, breslin.char3, ";") EQ dml-no NO-LOCK NO-ERROR.
        IF AVAILABLE breslin THEN
        DO:
            FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
            AND reslin-queasy.date1 EQ selected-date
            AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept
            AND ENTRY(2, reslin-queasy.char3, ";") EQ dml-no NO-LOCK NO-ERROR.
            DO WHILE AVAILABLE reslin-queasy:
                FIND FIRST l-artikel WHERE l-artikel.artnr = INT(ENTRY(1,reslin-queasy.char1,";")) NO-LOCK NO-ERROR.
                IF AVAILABLE l-artikel THEN
                DO:
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK NO-ERROR.
                    IF AVAILABLE l-untergrup THEN DO:
                        CREATE c-list. 
                        ASSIGN 
                            c-list.artnr       = l-artikel.artnr 
                            c-list.grp         = l-untergrup.bezeich 
                            c-list.zwkum       = l-untergrup.zwkum 
                            c-list.bezeich     = l-artikel.bezeich 
                            c-list.qty         = reslin-queasy.deci2 
                            c-list.price       = reslin-queasy.deci1
                            c-list.l-price     = l-artikel.ek-letzter /*Naufal*/
                            c-list.unit        = l-artikel.traubensorte 
                            c-list.content     = l-artikel.lief-einheit /* Oscar (05/06/2025) - 5B3BE7 - change content from receipt qty to mess qty */
                            /*c-list.deliver     = reslin-queasy.number3*/
                            c-list.deliver     = reslin-queasy.deci3 / l-artikel.lief-einheit
                            c-list.amount      = c-list.qty * c-list.price 
                            c-list.qty1        = c-list.qty 
                            c-list.price1      = c-list.price 
                            c-list.id          = ENTRY(1, reslin-queasy.char2, ";") 
                            c-list.cid         = ENTRY(1, reslin-queasy.char3, ";")
                            c-list.dept        = curr-dept
                            c-list.dml-nr      = ENTRY(2, reslin-queasy.char3, ";").

                        dml-grand-total = dml-grand-total + c-list.amount. /* Oscar (11/04/25) - 4BF019 - count grand total */
                            
                        FIND FIRST queasy WHERE queasy.KEY EQ 352 
                            AND queasy.char1 EQ dml-no 
                            AND queasy.number1 EQ 1 NO-LOCK NO-ERROR.

                        IF AVAILABLE queasy THEN
                            c-list.app-id = queasy.char3.

                        IF NUM-ENTRIES(reslin-queasy.char3, ";") GT 2 THEN
                            c-list.qty2        = DECIMAL(ENTRY(3, reslin-queasy.char3, ";")).

                        IF ENTRY(1, reslin-queasy.char3, ";") NE "" 
                            AND SUBSTR(ENTRY(1, reslin-queasy.char3, ";"),LENGTH(ENTRY(1, reslin-queasy.char3, ";"))) = "!" THEN
                            c-list.approved = YES.
                        ASSIGN
                            liefNo = 0
                            liefNo = INTEGER(ENTRY(2, reslin-queasy.char2, ";")) NO-ERROR.
                    
                        /*NAUFAL 120321 - Testing validation for add stock oh value*/
                        FIND FIRST l-bestand WHERE l-bestand.artnr = INT(ENTRY(1,reslin-queasy.char1,";"))
                            AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
                        IF AVAILABLE l-bestand THEN
                        DO:
                            /*NAUFAL 120321 - Testing assign value for stock oh*/
                            c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                                       - l-bestand.anz-ausgang.
                            /*end*/
                        END.
                        /*end*/
                        
                        /*ITA 170518 --> add remark*/
                        FIND FIRST queasy WHERE queasy.KEY = 202 
                            AND queasy.number1 = INT(ENTRY(2,reslin-queasy.char1,";"))
                            AND queasy.number2 = INT(ENTRY(1,reslin-queasy.char1,";"))
                            AND queasy.number3 = dml-counter /* show independent remark for multi DML by Oscar (01 November 2024) - B2F68F */
                            AND queasy.date1 = reslin-queasy.date1 NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN DO:
                            ASSIGN c-list.remark = queasy.char1.
                        END.
                        /*end*/
                        
                        IF liefNo NE 0 THEN
                        DO:
                            FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = liefNo
                                NO-LOCK NO-ERROR.
                            IF AVAILABLE l-lieferant THEN
                            ASSIGN
                                c-list.supplier = l-lieferant.firma
                                c-list.lief-nr  = liefNo.
                            FIND FIRST supply-list WHERE supply-list.lief-nr = liefNo NO-ERROR.
                            IF NOT AVAILABLE supply-list THEN
                            DO:
                                CREATE supply-list.
                                ASSIGN 
                                    supply-list.lief-nr  = l-lieferant.lief-nr
                                    supply-list.supplier = l-lieferant.firma  
                                    supply-list.telefon  = l-lieferant.telefon
                                    supply-list.fax      = l-lieferant.fax
                                    supply-list.namekontakt = l-lieferant.namekontakt.
                            END.
                        END.
                    END.
                END.
                FIND NEXT reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
                    AND reslin-queasy.date1 EQ selected-date
                    AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept
                    AND ENTRY(2, reslin-queasy.char3, ";") EQ dml-no NO-LOCK NO-ERROR.
            END.
        END.
        ELSE
        DO:
            FIND FIRST dml-artdep WHERE dml-artdep.datum = selected-date AND dml-artdep.departement = curr-dept NO-LOCK NO-ERROR.
            DO WHILE AVAILABLE dml-artdep:
                FIND FIRST l-artikel WHERE l-artikel.artnr = dml-artdep.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE l-artikel THEN DO:
                    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK NO-ERROR.
                    IF AVAILABLE l-untergrup THEN DO:

                        /* fill dml nr if it is somehow blank by Oscar (21 November 2) - 9DB75F */
                        IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 1 THEN
                            IF ENTRY(2, dml-artdep.chginit, ";") NE "" THEN fill-dml-nr = ENTRY(2, dml-artdep.chginit, ";").

                        CREATE c-list. 
                        ASSIGN 
                            c-list.artnr       = l-artikel.artnr 
                            c-list.grp         = l-untergrup.bezeich 
                            c-list.zwkum       = l-untergrup.zwkum 
                            c-list.bezeich     = l-artikel.bezeich 
                            c-list.qty         = dml-artdep.anzahl 
                            c-list.price       = dml-artdep.einzelpreis
                            c-list.l-price     = l-artikel.ek-letzter /*Naufal*/
                            c-list.unit        = l-artikel.traubensorte 
                            c-list.content     = l-artikel.lief-einheit /* Oscar (05/06/2025) - 5B3BE7 - change content from receipt qty to mess qty */ 
                            c-list.deliver     = dml-artdep.geliefert / l-artikel.lief-einheit
                            c-list.amount      = c-list.qty * c-list.price 
                            c-list.qty1        = c-list.qty 
                            c-list.price1      = c-list.price 
                            c-list.id          = ENTRY(1, dml-artdep.userinit, ";") 
                            c-list.dept        = curr-dept.

                        dml-grand-total = dml-grand-total + c-list.amount. /* Oscar (11/04/25) - 4BF019 - count grand total */

                        /* fill dml nr if it is somehow blank by Oscar (21 November 2) - 9DB75F */
                        IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 1 THEN
                        DO:
                            ASSIGN
                                c-list.cid     = REPLACE(ENTRY(1, dml-artdep.chginit, ";"),"!","")
                                c-list.dml-nr  = ENTRY(2, dml-artdep.chginit, ";").

                            IF c-list.dml-nr EQ "" OR c-list.dml-nr EQ ? THEN
                                c-list.dml-nr = fill-dml-nr.
                        END.
                        ELSE
                        DO:
                            ASSIGN
                                c-list.cid    = REPLACE(dml-artdep.chginit,"!","")
                                c-list.dml-nr = fill-dml-nr.
                        END.

                        FIND FIRST queasy WHERE queasy.KEY EQ 352 
                            AND queasy.char1 EQ fill-dml-nr
                            AND queasy.number1 EQ 1 NO-LOCK NO-ERROR.

                        IF AVAILABLE queasy THEN
                            c-list.app-id = queasy.char3.

                        IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 2 THEN
                            c-list.qty2        = DECIMAL(ENTRY(3, dml-artdep.chginit, ";")).

                            /*ITA 24/06/24*/
                        IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 1 AND ENTRY(1, dml-artdep.chginit, ";") NE "" 
                            AND SUBSTR(ENTRY(1, dml-artdep.chginit, ";"),LENGTH(ENTRY(1, dml-artdep.chginit, ";"))) = "!" THEN
                            c-list.approved = YES.
                        ELSE IF dml-artdep.chginit NE "" AND SUBSTR(dml-artdep.chginit,LENGTH(dml-artdep.chginit)) = "!" THEN
                            c-list.approved = YES.

                        /*IF dml-artdep.chginit NE "" 
                            AND SUBSTR(dml-artdep.chginit,LENGTH(dml-artdep.chginit)) = "!" THEN
                            c-list.approved = YES.*/
                        ASSIGN
                            liefNo = 0
                            liefNo = INTEGER(ENTRY(2, dml-artdep.userinit, ";")) NO-ERROR.
                
                        /*NAUFAL 120321 - Testing validation for add stock oh value*/
                        FIND FIRST l-bestand WHERE l-bestand.artnr = dml-artdep.artnr
                            AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
                        IF AVAILABLE l-bestand THEN
                        DO:
                            /*NAUFAL 120321 - Testing assign value for stock oh*/
                            c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                                       - l-bestand.anz-ausgang.
                            /*end*/
                        END.
                        /*end*/
                        
                        /*ITA 170518 --> add remark*/
                        FIND FIRST queasy WHERE queasy.KEY = 202 
                            AND queasy.number1 = dml-artdep.departement 
                            AND queasy.number2 = dml-artdep.artnr
                            AND queasy.number3 = dml-counter /* show independent remark for multi DML by Oscar (01 November 2024) - B2F68F */
                            AND queasy.date1 = dml-artdep.datum NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN DO:
                            ASSIGN c-list.remark = queasy.char1.
                        END.
                        /*end*/
                        
                        IF liefNo NE 0 THEN
                        DO:
                            FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = liefNo
                                NO-LOCK NO-ERROR.
                            IF AVAILABLE l-lieferant THEN
                            ASSIGN
                                c-list.supplier = l-lieferant.firma
                                c-list.lief-nr  = liefNo.
                            FIND FIRST supply-list WHERE supply-list.lief-nr = liefNo NO-ERROR.
                            IF NOT AVAILABLE supply-list THEN
                            DO:
                                CREATE supply-list.
                                ASSIGN 
                                    supply-list.lief-nr  = l-lieferant.lief-nr
                                    supply-list.supplier = l-lieferant.firma  
                                    supply-list.telefon  = l-lieferant.telefon
                                    supply-list.fax      = l-lieferant.fax
                                    supply-list.namekontakt = l-lieferant.namekontakt.
                            END.
                        END.
                    END.
                END.
                FIND NEXT dml-artdep WHERE dml-artdep.datum = selected-date AND dml-artdep.departement = curr-dept NO-LOCK NO-ERROR.
            END.
        END.
    END.     
END. 


        /*FOR EACH dml-artdep WHERE dml-artdep.datum = selected-date 
            AND dml-artdep.departement = curr-dept NO-LOCK,
            FIRST l-artikel WHERE l-artikel.artnr = dml-artdep.artnr 
              /*AND l-artikel.bestellt = YES*/ NO-LOCK, 
            FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK:

        /*naufal - test validation for dml closed report*/
        FIND FIRST dml-artdep WHERE dml-artdep.datum = selected-date AND dml-artdep.departement = curr-dept
            AND ENTRY(2, dml-artdep.chginit, ";") EQ dml-no NO-LOCK NO-ERROR.
        /*FIND FIRST dml-artdep WHERE dml-artdep.datum EQ selected-date AND dml-artdep.departement EQ curr-dept NO-LOCK NO-ERROR.
        IF AVAILABLE dml-artdep THEN
        DO:
            FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML" AND reslin-queasy.date1 EQ selected-date AND reslin-queasy.number1 EQ curr-dept NO-LOCK NO-ERROR.
            IF AVAILABLE reslin-queasy THEN
            DO:
                CREATE dml-list.
                

            END.
        END.*/
        DO WHILE AVAILABLE dml-artdep:   
            FIND FIRST l-artikel WHERE l-artikel.artnr = dml-artdep.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-artikel THEN DO:
                FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK NO-ERROR.
                IF AVAILABLE l-untergrup THEN DO:
                    CREATE c-list. 
                    ASSIGN 
                        c-list.artnr       = l-artikel.artnr 
                        c-list.grp         = l-untergrup.bezeich 
                        c-list.zwkum       = l-untergrup.zwkum 
                        c-list.bezeich     = l-artikel.bezeich 
                        c-list.qty         = dml-artdep.anzahl 
                        c-list.price       = dml-artdep.einzelpreis
                        c-list.l-price    = l-artikel.ek-letzter /*Naufal*/
                        c-list.unit        = l-artikel.traubensorte 
                        c-list.content     = l-artikel.inhalt 
                        c-list.deliver     = dml-artdep.geliefert 
                        c-list.amount      = c-list.qty * c-list.price 
                        c-list.qty1        = c-list.qty 
                        c-list.price1      = c-list.price 
                        c-list.id          = ENTRY(1, dml-artdep.userinit, ";") 
                        c-list.cid         = dml-artdep.chginit 
                        c-list.dept        = curr-dept.
                        
                    IF dml-artdep.chginit NE "" 
                        AND SUBSTR(dml-artdep.chginit,LENGTH(dml-artdep.chginit)) = "!" THEN
                        c-list.approved = YES.
                    ASSIGN
                        liefNo = 0
                        liefNo = INTEGER(ENTRY(2, dml-artdep.userinit, ";")) NO-ERROR.
            
                    /*NAUFAL 120321 - Testing validation for add stock oh value*/
                    FIND FIRST l-bestand WHERE l-bestand.artnr = dml-artdep.artnr
                        AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE l-bestand THEN
                    DO:
                        /*NAUFAL 120321 - Testing assign value for stock oh*/
                        c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                                   - l-bestand.anz-ausgang.
                        /*end*/
                    END.
                    /*end*/
                    
                    /*ITA 170518 --> add remark*/
                    FIND FIRST queasy WHERE queasy.KEY = 202 
                        AND queasy.number1 = dml-artdep.departement 
                        AND queasy.number2 = dml-artdep.artnr
                        AND queasy.date1 = dml-artdep.datum NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN DO:
                        ASSIGN c-list.remark = queasy.char1.
                    END.
                    /*end*/
                    
                    IF liefNo NE 0 THEN
                    DO:
                        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = liefNo
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE l-lieferant THEN
                        ASSIGN
                            c-list.supplier = l-lieferant.firma
                            c-list.lief-nr  = liefNo.
                        FIND FIRST supply-list WHERE supply-list.lief-nr = liefNo NO-ERROR.
                        IF NOT AVAILABLE supply-list THEN
                        DO:
                            CREATE supply-list.
                            ASSIGN 
                                supply-list.lief-nr  = l-lieferant.lief-nr
                                supply-list.supplier = l-lieferant.firma  
                                supply-list.telefon  = l-lieferant.telefon
                                supply-list.fax      = l-lieferant.fax
                                supply-list.namekontakt = l-lieferant.namekontakt.
                        END.
                    END.
                END.
            END.
            FIND NEXT dml-artdep WHERE dml-artdep.datum = selected-date AND dml-artdep.departement = curr-dept
                AND NUM-ENTRIES(dml-artdep.chginit,";") LT 2 NO-LOCK NO-ERROR.
        END.
        IF NOT AVAILABLE dml-artdep THEN
        DO:
            
        END.*/
