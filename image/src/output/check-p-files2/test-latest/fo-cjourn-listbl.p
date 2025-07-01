DEFINE TEMP-TABLE output-list 
    FIELD STR AS CHAR.

DEFINE TEMP-TABLE cjourn-list
    FIELD artnr       AS INTEGER    FORMAT ">>>>>"
    FIELD bezeich     AS CHARACTER  FORMAT "x(24)"
    FIELD dept        AS CHARACTER  FORMAT "x(16)"
    FIELD datum       AS DATE       
    FIELD zinr        AS CHARACTER  FORMAT "x(8)"
    FIELD rechnr      AS INTEGER    FORMAT ">>>>>>>>>"
    FIELD canc-reason AS CHARACTER  FORMAT "x(24)"
    FIELD qty         AS INTEGER    FORMAT "->>>>"
    FIELD amount      AS DECIMAL    FORMAT "->,>>>,>>>,>>9.99"
    FIELD zeit        AS CHARACTER  FORMAT "x(5)"
    FIELD id          AS CHARACTER  FORMAT "x(3)"
    .

DEFINE INPUT PARAMETER from-art     AS INTEGER.
DEFINE INPUT PARAMETER to-art       AS INTEGER.
DEFINE INPUT PARAMETER from-dept    AS INTEGER.
DEFINE INPUT PARAMETER to-dept      AS INTEGER.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER foreign-flag AS LOGICAL.
DEFINE INPUT PARAMETER long-digit   AS LOGICAL.

DEFINE OUTPUT PARAMETER TABLE FOR cjourn-list.

DEFINE TEMP-TABLE htl-list 
    FIELD num AS INTEGER
    FIELD depart AS CHAR.

DEFINE TEMP-TABLE art-list
    FIELD artnr AS INTEGER
    FIELD departement AS INTEGER
    FIELD endkum AS INTEGER.

RUN journal-list.


/*************** PROCEDURES ***************/
 
PROCEDURE journal-list:
    DEFINE VARIABLE qty       AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
    DEFINE VARIABLE sub-tot   AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE tot       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE curr-date AS DATE. 
    DEFINE VARIABLE last-dept AS INTEGER INITIAL -1. 
    DEFINE VARIABLE it-exist  AS LOGICAL. 
    DEFINE VARIABLE ekumnr    AS INTEGER. 
    DEFINE VARIABLE amount    AS DECIMAL NO-UNDO. 
    DEFINE VARIABLE hoteldpt-num    AS INTEGER. /* Malik Serverless 237 */
    DEFINE VARIABLE hoteldpt-depart AS CHAR. /* Malik Serverless 237 */

    DEFINE VARIABLE curr-art AS INTEGER.
    DEFINE VARIABLE curr-dept AS INTEGER.
    DEFINE VARIABLE i AS INTEGER.
    
    FIND FIRST htparam WHERE paramnr = 555 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN ekumnr = htparam.finteger. 
    EMPTY TEMP-TABLE cjourn-list.

    FOR EACH artikel WHERE artikel.artnr GE from-art 
        AND artikel.artnr LE to-art 
        AND artikel.departement GE from-dept 
        AND artikel.departement LE to-dept 
        AND artikel.endkum NE ekumnr NO-LOCK BY (artikel.departement * 10000 + artikel.artnr): 
        
        FIND FIRST htl-list WHERE htl-list.num = artikel.departement NO-LOCK NO-ERROR.
        IF NOT AVAILABLE htl-list THEN
        DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-LOCK NO-ERROR.
            IF AVAILABLE hoteldpt THEN
            DO:
                CREATE htl-list.
                ASSIGN
                    htl-list.num = hoteldpt.num
                    htl-list.depart = hoteldpt.depart.
            END.
        END.

        CREATE art-list.
        BUFFER-COPY artikel TO art-list.
    END.

    FOR EACH billjournal WHERE billjournal.stornogrund NE "" 
        AND billjournal.bill-datum GE from-date
        AND billjournal.bill-datum LE to-date
        AND billjournal.artnr GE from-art
        AND billjournal.artnr LE to-art NO-LOCK 
        BY (billjournal.departement * 10000 + billjournal.artnr)
        BY billjournal.sysdate BY billjournal.zeit: 

        FIND FIRST art-list WHERE art-list.artnr = billjournal.artnr AND art-list.departement = billjournal.departement NO-LOCK NO-ERROR.
        IF AVAILABLE art-list THEN
        DO:
            i = i + 1.

            IF curr-art NE billjournal.artnr AND curr-dept NE billjournal.departement AND i NE 1 THEN
            DO: 
                CREATE cjourn-list.    
                ASSIGN         
                    cjourn-list.canc-reason = "T O T A L   "
                    cjourn-list.qty         = qty
                    cjourn-list.amount      = sub-tot
                    qty = 0
                    sub-tot = 0
                    curr-art = billjournal.artnr
                    curr-dept = billjournal.departement. 
            END.

            IF i = 1 THEN
            DO:
                curr-art = billjournal.artnr.
                curr-dept = billjournal.departement. 
            END.

            IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
            ELSE amount = billjournal.betrag. 

                    
            CREATE cjourn-list.
            ASSIGN
                 cjourn-list.artnr        = billjournal.artnr
                 cjourn-list.bezeich      = billjournal.bezeich
                 cjourn-list.datum        = billjournal.bill-datum
                 cjourn-list.zinr         = billjournal.zinr
                 cjourn-list.rechnr       = billjournal.rechnr
                 cjourn-list.canc-reason  = billjournal.stornogrund
                 cjourn-list.qty          = billjournal.anzahl
                 cjourn-list.amount       = amount
                 cjourn-list.zeit         = STRING(billjournal.zeit, "HH:MM") 
                 cjourn-list.id           = billjournal.userinit
                 qty = qty + billjournal.anzahl. 
                 sub-tot = sub-tot + amount. 
                 tot = tot + amount. 
            FIND FIRST htl-list WHERE htl-list.num = billjournal.departement NO-LOCK NO-ERROR.
            IF AVAILABLE htl-list THEN cjourn-list.dept = htl-list.depart.
        END.
    END.

    CREATE cjourn-list.    
    ASSIGN         
        cjourn-list.canc-reason = "T O T A L   "
        cjourn-list.qty         = qty
        cjourn-list.amount      = sub-tot.

    CREATE cjourn-list.    
    ASSIGN         
        cjourn-list.canc-reason = "Grand TOTAL"
        cjourn-list.qty         = 0
        cjourn-list.amount      = tot.   

    

    /*FOR EACH artikel WHERE artikel.artnr GE from-art 
        AND artikel.artnr LE to-art 
        AND artikel.departement GE from-dept 
        AND artikel.departement LE to-dept 
        AND artikel.endkum NE ekumnr NO-LOCK BY (artikel.departement * 10000 + artikel.artnr): 
        /* IF last-dept NE artikel.departement THEN FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-ERROR. */
        /* Malik Serverless 237 */
        IF last-dept NE artikel.departement THEN
        DO:
            FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-LOCK NO-ERROR.
            IF AVAILABLE hoteldpt THEN
            DO:
                ASSIGN
                    hoteldpt-num = hoteldpt.num
                    hoteldpt-depart = hoteldpt.depart.
            END.
            ELSE
            DO:
                ASSIGN
                    hoteldpt-num = 0
                    hoteldpt-depart = "".
            END.
        END.
        /* END Malik */
        last-dept = artikel.departement. 
        sub-tot   = 0. 
        it-exist  = NO. 
        qty       = 0. 

        DO curr-date = from-date TO to-date: 
            FOR EACH billjournal WHERE billjournal.stornogrund NE "" 
                AND billjournal.departement EQ hoteldpt-num /* Malik Serverless 237 hoteldpt.num -> hoteldpt-num */
                AND billjournal.bill-datum EQ curr-date 
                AND billjournal.artnr EQ artikel.artnr NO-LOCK 
                BY billjournal.sysdate BY billjournal.zeit: 
                
                IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
                ELSE amount = billjournal.betrag. 
                
                it-exist = YES. 
                CREATE cjourn-list.
                ASSIGN
                     cjourn-list.artnr        = billjournal.artnr
                     cjourn-list.bezeich      = billjournal.bezeich
                     cjourn-list.dept         = hoteldpt-depart /* Malik Serverless 237 : hoteldpt.depart -> hoteldpt-depart */
                     cjourn-list.datum        = billjournal.bill-datum
                     cjourn-list.zinr         = billjournal.zinr
                     cjourn-list.rechnr       = billjournal.rechnr
                     cjourn-list.canc-reason  = billjournal.stornogrund
                     cjourn-list.qty          = billjournal.anzahl
                     cjourn-list.amount       = amount
                     cjourn-list.zeit         = STRING(billjournal.zeit, "HH:MM") 
                     cjourn-list.id           = billjournal.userinit.
                /*
                create output-list. 
                IF NOT long-digit THEN output-list.STR = STRING(billjournal.bill-datum) 
                            + STRING(hoteldpt.depart, "x(16)") 
                            + STRING(billjournal.zinr, "999999") 
                            + STRING(billjournal.rechnr, ">>>>>>>>9") 
                            + STRING(billjournal.artnr, ">>>>9") 
                            + STRING(billjournal.bezeich, "x(24)") 
                            + STRING(billjournal.stornogrund, "x(74)") /*william - EC2332 add 50 spaces*/
                            + STRING(billjournal.anzahl, "-9999") 
                            + STRING(amount, "->,>>>,>>>,>>9.99") 
                            + STRING(billjournal.zeit, "HH:MM") 
                            + STRING(billjournal.userinit, "x(3)"). 
                ELSE output-list.STR = STRING(billjournal.bill-datum) 
                            + STRING(hoteldpt.depart, "x(16)") 
                            + STRING(billjournal.zinr, "999999") 
                            + STRING(billjournal.rechnr, ">>>>>>>>9") 
                            + STRING(billjournal.artnr, ">>>>9") 
                            + STRING(billjournal.bezeich, "x(24)") 
                            + STRING(billjournal.stornogrund, "x(74)") /*william - EC2332 add 50 spaces*/
                            + STRING(billjournal.anzahl, "-9999") 
                            + STRING(amount, " ->>>,>>>,>>>,>>9") 
                            + STRING(billjournal.zeit, "HH:MM") 
                            + STRING(billjournal.userinit, "x(3)"). 
                */
                qty = qty + billjournal.anzahl. 
                sub-tot = sub-tot + amount. 
                tot = tot + amount. 
            END. 
        END. 
        IF it-exist THEN 
        DO: 
            CREATE cjourn-list.    
            ASSIGN         
                cjourn-list.canc-reason = "T O T A L   "
                cjourn-list.qty         = qty
                cjourn-list.amount      = sub-tot.           
            /*    
            create output-list. 
            IF NOT long-digit THEN output-list.STR = STRING("", "x(118)") /*william - EC2332 add 50 spaces*/
              + STRING("T O T A L   ", "x(24)") 
              + STRING(qty, "-9999") 
              + STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
            ELSE output-list.STR = STRING("", "x(118)")                   /*william - EC2332 add 50 spaces*/
              + STRING("T O T A L   ", "x(24)") 
              + STRING(qty, "-9999") 
              + STRING(sub-tot, " ->>>,>>>,>>>,>>9"). 
            */
        END. 
    END. 
    CREATE cjourn-list.    
    ASSIGN         
        cjourn-list.canc-reason = "Grand TOTAL"
        cjourn-list.qty         = qty
        cjourn-list.amount      = sub-tot.   
    /*
    create output-list. 
    IF NOT long-digit THEN output-list.STR = STRING("", "x(118)") /*william - EC2332 add 50 spaces*/
          + STRING("Grand TOTAL", "x(24)") 
          + STRING(0, ">>>>>") 
          + STRING(tot, "->,>>>,>>>,>>9.99"). 
    ELSE output-list.STR = STRING("", "x(118)")                   /*william - EC2332 add 50 spaces*/
          + STRING("Grand TOTAL", "x(24)") 
          + STRING(0, ">>>>>") 
          + STRING(tot, " ->>>,>>>,>>>,>>9"). 
    */*/
END. 
 


