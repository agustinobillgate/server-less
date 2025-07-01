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
    FIELD dml-nr   AS CHARACTER
    FIELD qty2     AS DECIMAL. 
    /*end*/

DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER selected-date AS DATE.
DEF INPUT PARAMETER dml-no AS CHARACTER.
DEF OUTPUT PARAMETER TABLE FOR supply-list.
DEF OUTPUT PARAMETER TABLE FOR c-list.

RUN create-it.


PROCEDURE create-it: 
DEFINE VARIABLE dept   AS INTEGER NO-UNDO. 
DEFINE VARIABLE liefNo AS INTEGER NO-UNDO.

    FOR EACH c-list: 
        DELETE c-list. 
    END.
    
    FOR EACH supply-list:
        DELETE supply-list.
    END.
    CREATE supply-list.
    
    IF curr-dept = 0 THEN DO:
        /*FOR EACH dml-art WHERE dml-art.datum = selected-date NO-LOCK,
            FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr 
              /*AND l-artikel.bestellt = YES*/ NO-LOCK,
            FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK:*/

        FIND FIRST dml-art WHERE dml-art.datum = selected-date NO-LOCK NO-ERROR.
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
                        c-list.content    = l-artikel.inhalt 
                        c-list.deliver    = dml-art.geliefert 
                        c-list.amount     = c-list.qty * c-list.price 
                        c-list.qty1       = c-list.qty 
                        c-list.price1     = c-list.price 
                        c-list.id         = ENTRY(1, dml-art.userinit, ";") 
                        c-list.cid        = REPLACE(dml-art.chginit, "!", "") 
                        c-list.dept       = curr-dept.
                        
                    IF dml-art.chginit NE "" 
                        AND SUBSTR(dml-art.chginit,LENGTH(dml-art.chginit)) = "!" THEN
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
                        AND queasy.number1 = 0 AND queasy.number2 = dml-art.artnr
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
            FIND NEXT dml-art WHERE dml-art.datum = selected-date NO-LOCK NO-ERROR.
        END.
    END.
    ELSE DO: 
        /*FOR EACH dml-artdep WHERE dml-artdep.datum = selected-date 
            AND dml-artdep.departement = curr-dept NO-LOCK,
            FIRST l-artikel WHERE l-artikel.artnr = dml-artdep.artnr 
              /*AND l-artikel.bestellt = YES*/ NO-LOCK, 
            FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK: */

        FIND FIRST dml-artdep WHERE dml-artdep.datum = selected-date 
            AND dml-artdep.departement = curr-dept NO-LOCK NO-ERROR.
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
            FIND NEXT dml-artdep WHERE dml-artdep.datum = selected-date 
                AND dml-artdep.departement = curr-dept NO-LOCK NO-ERROR.
        END.
    END.     
END. 
