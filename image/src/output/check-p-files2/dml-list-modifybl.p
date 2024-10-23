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
    FIELD qty2     AS DECIMAL.

DEF INPUT PARAMETER user-init       AS CHAR.
DEF INPUT PARAMETER dml-no          AS CHAR.
DEF INPUT PARAMETER curr-dept       AS INT.
DEF INPUT PARAMETER selected-date   AS DATE.   
DEF OUTPUT PARAMETER TABLE FOR c-list.

DEFINE BUFFER breslin       FOR reslin-queasy.
DEFINE BUFFER bdml-artdep   FOR dml-artdep.
DEFINE BUFFER bdml-art      FOR dml-art.
DEFINE BUFFER bartikel      FOR l-artikel.

DEFINE VARIABLE counter AS INTEGER.

IF dml-no EQ ? THEN
    dml-no = "".

IF dml-no NE "" THEN
    counter = INT(SUBSTRING(dml-no, 11, 2)).
ELSE
    counter = 1.

/*FOR EACH c-list.
    DELETE c-list.
END.*/

RUN modify-dml.

PROCEDURE modify-dml:
    DEFINE VARIABLE liefNo AS INTEGER NO-UNDO.

    FOR EACH l-artikel /*WHERE l-artikel.bestellt*/ USE-INDEX artnr_ix NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK:
        IF counter GT 1 THEN
        DO:
            FIND FIRST breslin WHERE breslin.KEY EQ "DML"
                AND INT(ENTRY(1,breslin.char1,";")) EQ l-artikel.artnr
                AND breslin.date1 EQ selected-date 
                AND ENTRY(2, breslin.char3, ";") EQ dml-no NO-LOCK NO-ERROR.
            IF AVAILABLE breslin THEN
            DO:
                FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
                    AND INT(ENTRY(1,reslin-queasy.char1,";")) EQ l-artikel.artnr
                    AND reslin-queasy.date1 EQ selected-date 
                    AND ENTRY(2, reslin-queasy.char3, ";") EQ dml-no NO-LOCK NO-ERROR.
                IF AVAILABLE reslin-queasy THEN
                DO:
                    CREATE c-list. 
                    ASSIGN 
                        c-list.artnr       = INT(ENTRY(1,reslin-queasy.char1,";")) 
                        c-list.grp         = l-untergrup.bezeich 
                        c-list.zwkum       = l-untergrup.zwkum 
                        c-list.bezeich     = l-artikel.bezeich 
                        c-list.qty         = reslin-queasy.deci2 
                        c-list.price       = reslin-queasy.deci1
                        c-list.l-price     = l-artikel.ek-letzter /*Naufal*/
                        c-list.unit        = l-artikel.traubensorte 
                        c-list.content     = l-artikel.inhalt 
                        c-list.deliver     = reslin-queasy.number3
                        c-list.amount      = c-list.qty * c-list.price 
                        c-list.qty1        = c-list.qty 
                        c-list.price1      = c-list.price 
                        c-list.id          = ENTRY(1, reslin-queasy.char2, ";") 
                        c-list.cid         = ENTRY(1, reslin-queasy.char3, ";")
                        c-list.dept        = curr-dept
                        c-list.dml-nr      = ENTRY(2, reslin-queasy.char3, ";").
                        
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
                    END.
                END.
            END.
            ELSE 
            DO:
                FIND FIRST bartikel WHERE bartikel.bestellt AND bartikel.artnr EQ l-artikel.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE bartikel THEN
                DO:
                    CREATE c-list. 
                    ASSIGN
                        c-list.artnr 	= bartikel.artnr 
                        c-list.grp 	    = l-untergrup.bezeich 
                        c-list.zwkum 	= l-untergrup.zwkum 
                        c-list.bezeich  = bartikel.bezeich 
                        c-list.price 	= bartikel.ek-aktuell
                        c-list.l-price  = bartikel.ek-letzter /*Naufal*/
                        c-list.unit 	= bartikel.traubensorte 
                        c-list.content  = bartikel.inhalt 
                        c-list.price1   = c-list.price 
                        c-list.id 	    = user-init
                        c-list.dept 	= curr-dept
                    .
                    
                    /*NAUFAL 150321 - add validation for add stock oh value*/
                    FIND FIRST l-bestand WHERE l-bestand.artnr = bartikel.artnr
                        AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
                    IF AVAILABLE l-bestand THEN
                    DO:
                      c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                                 - l-bestand.anz-ausgang.
                    END.
                END.     
            END.
        END.   
        ELSE
        DO:
            IF curr-dept NE 0 THEN
            DO:
                FIND FIRST bdml-artdep WHERE bdml-artdep.datum = selected-date
                    AND bdml-artdep.artnr = l-artikel.artnr
                    AND bdml-artdep.departement = curr-dept NO-LOCK NO-ERROR.
                IF AVAILABLE bdml-artdep THEN
                DO:
                    FIND FIRST dml-artdep WHERE dml-artdep.datum = selected-date 
                        AND dml-artdep.departement = curr-dept 
                        AND dml-artdep.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
                    IF AVAILABLE dml-artdep THEN 
                    DO:
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
                            c-list.content     = l-artikel.inhalt 
                            c-list.deliver     = dml-artdep.geliefert 
                            c-list.amount      = c-list.qty * c-list.price 
                            c-list.qty1        = c-list.qty 
                            c-list.price1      = c-list.price 
                            c-list.id          = ENTRY(1, dml-artdep.userinit, ";") 
                            c-list.dept        = curr-dept.
                
                        IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 1 THEN
                            ASSIGN
                                c-list.cid     = ENTRY(1, dml-artdep.chginit, ";")
                                c-list.dml-nr  = ENTRY(2, dml-artdep.chginit, ";").
                        ELSE
                            c-list.cid         = dml-artdep.chginit.
                
                        IF NUM-ENTRIES(dml-artdep.chginit, ";") GT 2 THEN
                            c-list.qty2        = DECIMAL(ENTRY(3, dml-artdep.chginit, ";")).
                            
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
                        END.
                    END.
                END.
                ELSE 
                DO:
                    FIND FIRST bartikel WHERE bartikel.bestellt AND bartikel.artnr EQ l-artikel.artnr NO-LOCK NO-ERROR.
                    IF AVAILABLE bartikel THEN
                    DO:
                        CREATE c-list. 
                        ASSIGN
                            c-list.artnr 	= bartikel.artnr 
                            c-list.grp 	    = l-untergrup.bezeich 
                            c-list.zwkum 	= l-untergrup.zwkum 
                            c-list.bezeich  = bartikel.bezeich 
                            c-list.price 	= bartikel.ek-aktuell
                            c-list.l-price  = bartikel.ek-letzter /*Naufal*/
                            c-list.unit 	= bartikel.traubensorte 
                            c-list.content  = bartikel.inhalt 
                            c-list.price1   = c-list.price 
                            c-list.id 	    = user-init
                            c-list.dept 	= curr-dept
                        .
                        
                        /*NAUFAL 150321 - add validation for add stock oh value*/
                        FIND FIRST l-bestand WHERE l-bestand.artnr = bartikel.artnr
                            AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
                        IF AVAILABLE l-bestand THEN
                        DO:
                          c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                                     - l-bestand.anz-ausgang.
                        END.
                    END.
                END.
            END.
            ELSE
            DO:
                FIND FIRST bdml-art WHERE bdml-art.datum = selected-date
                    AND bdml-art.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE bdml-art THEN
                DO:
                    FIND FIRST dml-art WHERE dml-art.datum = selected-date
                        AND dml-art.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
                    IF AVAILABLE dml-art THEN 
                    DO:
                        CREATE c-list. 
                        ASSIGN 
                            c-list.artnr       = l-artikel.artnr 
                            c-list.grp         = l-untergrup.bezeich 
                            c-list.zwkum       = l-untergrup.zwkum 
                            c-list.bezeich     = l-artikel.bezeich 
                            c-list.qty         = dml-art.anzahl 
                            c-list.price       = dml-art.einzelpreis
                            c-list.l-price     = l-artikel.ek-letzter /*Naufal*/
                            c-list.unit        = l-artikel.traubensorte 
                            c-list.content     = l-artikel.inhalt 
                            c-list.deliver     = dml-art.geliefert 
                            c-list.amount      = c-list.qty * c-list.price 
                            c-list.qty1        = c-list.qty 
                            c-list.price1      = c-list.price 
                            c-list.id          = ENTRY(1, dml-art.userinit, ";") 
                            c-list.dept        = curr-dept.
                
                        IF NUM-ENTRIES(dml-art.chginit, ";") GT 1 THEN
                            ASSIGN
                                c-list.cid     = ENTRY(1, dml-art.chginit, ";")
                                c-list.dml-nr  = ENTRY(2, dml-art.chginit, ";").
                        ELSE
                            c-list.cid         = dml-art.chginit.
                
                        IF NUM-ENTRIES(dml-art.chginit, ";") GT 2 THEN
                            c-list.qty2        = DECIMAL(ENTRY(3, dml-art.chginit, ";")).
                            
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
                            AND queasy.number1 = 0
                            AND queasy.number2 = dml-art.artnr
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
                            ASSIGN
                                c-list.supplier = l-lieferant.firma
                                c-list.lief-nr  = liefNo.
                        END.
                    END.
                END.
                ELSE 
                DO:
                    FIND FIRST bartikel WHERE bartikel.bestellt AND bartikel.artnr EQ l-artikel.artnr NO-LOCK NO-ERROR.
                    IF AVAILABLE bartikel THEN
                    DO:
                        CREATE c-list. 
                        ASSIGN
                            c-list.artnr 	= bartikel.artnr 
                            c-list.grp 	    = l-untergrup.bezeich 
                            c-list.zwkum 	= l-untergrup.zwkum 
                            c-list.bezeich  = bartikel.bezeich 
                            c-list.price 	= bartikel.ek-aktuell
                            c-list.l-price  = bartikel.ek-letzter /*Naufal*/
                            c-list.unit 	= bartikel.traubensorte 
                            c-list.content  = bartikel.inhalt 
                            c-list.price1   = c-list.price 
                            c-list.id 	    = user-init
                            c-list.dept 	= curr-dept
                        .
                        
                        /*NAUFAL 150321 - add validation for add stock oh value*/
                        FIND FIRST l-bestand WHERE l-bestand.artnr = bartikel.artnr
                            AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
                        IF AVAILABLE l-bestand THEN
                        DO:
                          c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                                     - l-bestand.anz-ausgang.
                        END.
                    END.
                END.
            END.
        END.
    END.
END. 
