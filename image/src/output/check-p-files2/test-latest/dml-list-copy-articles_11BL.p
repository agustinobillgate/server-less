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
    FIELD dml-nr   AS CHARACTER.
    
DEFINE TEMP-TABLE supply-list
    FIELD lief-nr  AS INTEGER
    FIELD supplier AS CHAR
    FIELD telefon  LIKE l-lieferant.telefon           /*MT 01/07/12 */
    FIELD fax      LIKE l-lieferant.fax               /*MT 01/07/12 */
    FIELD namekontakt LIKE l-lieferant.namekontakt.   /*MT 01/07/12 */

DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER curr-dept      AS INT.
DEF INPUT  PARAMETER selected-date  AS DATE.
DEF OUTPUT PARAMETER approve-flag   AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR c-list.
DEF OUTPUT PARAMETER TABLE FOR supply-list.

RUN copy-articles.

PROCEDURE copy-articles:
DEFINE VARIABLE liefNo AS INTEGER NO-UNDO.
DEFINE BUFFER d-art    FOR dml-art. 
DEFINE BUFFER d-art1   FOR dml-artdep. 
  
    FOR EACH c-list: 
        DELETE c-list. 
    END. 
    
    FOR EACH supply-list:
        DELETE supply-list.
    END.
    
    IF curr-dept = 0 THEN 
    FOR EACH dml-art WHERE dml-art.datum = (selected-date - 1) NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK: 
        create c-list. 
        ASSIGN
            c-list.artnr      = l-artikel.artnr
            c-list.grp        = l-untergrup.bezeich 
            c-list.zwkum      = l-untergrup.zwkum
            c-list.bezeich    = l-artikel.bezeich 
            c-list.qty        = dml-art.anzahl
            c-list.price      = dml-art.einzelpreis 
            c-list.unit       = l-artikel.masseinheit 
            c-list.content    = l-artikel.inhalt
            c-list.amount     = c-list.qty * c-list.price 
            c-list.qty1       = c-list.qty
            c-list.price1     = c-list.price 
            c-list.id         = ENTRY(1, dml-art.userinit, ";").
            

        /*NAUFAL 150321 - add validation for stock oh value*/
        FIND FIRST l-bestand WHERE l-bestand.artnr = dml-art.artnr 
            AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE l-bestand THEN
        DO:
            /*NAUFAL 150321 - assign value for stock oh*/
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
        
        CREATE d-art. 
        ASSIGN
            d-art.artnr       = dml-art.artnr 
            d-art.datum       = selected-date 
            d-art.userinit    = user-init
            d-art.anzahl      = dml-art.anzahl 
            d-art.einzelpreis = dml-art.einzelpreis. 
    END. 
    ELSE 
    FOR EACH dml-artdep WHERE dml-artdep.datum = (selected-date - 1) 
        AND dml-artdep.departement = curr-dept NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = dml-artdep.artnr NO-LOCK, 
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK: 
        create c-list. 
        ASSIGN 
            c-list.artnr      = l-artikel.artnr 
            c-list.grp        = l-untergrup.bezeich 
            c-list.zwkum      = l-untergrup.zwkum 
            c-list.bezeich    = l-artikel.bezeich 
            c-list.qty        = dml-artdep.anzahl 
            c-list.price      = dml-artdep.einzelpreis 
            c-list.unit       = l-artikel.masseinheit 
            c-list.content    = l-artikel.inhalt 
            c-list.deliver    = dml-artdep.geliefert 
            c-list.amount     = c-list.qty * c-list.price 
            c-list.qty1       = c-list.qty 
            c-list.price1     = c-list.price 
            c-list.id         = ENTRY(1, dml-artdep.userinit, ";")
            c-list.dept       = curr-dept.   
        
        /*NAUFAL 150321 - add validation for stock oh value*/
        FIND FIRST l-bestand WHERE l-bestand.artnr = dml-artdep.artnr
            AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE l-bestand THEN
        DO:
            /*NAUFAL 150321 - assign value for stock oh*/
            c-list.soh        = l-bestand.anz-anf-best + l-bestand.anz-eingang
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
        
        CREATE d-art1.
        ASSIGN
            d-art1.artnr          = dml-artdep.artnr
            d-art1.datum          = selected-date
            d-art1.userinit       = user-init
            d-art1.anzahl         = dml-artdep.anzahl
            d-art1.einzelpreis    = dml-artdep.einzelpreis 
            d-art1.departement    = curr-dept. 
    END. 
    
    approve-flag = NO.
END. 
