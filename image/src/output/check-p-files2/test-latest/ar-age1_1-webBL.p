
DEFINE TEMP-TABLE arage-balance-list 
    FIELD strdate AS CHAR FORMAT "x(8)"
    FIELD curr    AS CHAR FORMAT "x(4)"
    FIELD gastnr  AS INTEGER INITIAL 0
    FIELD artnr   AS INTEGER INITIAL 0
    FIELD age1    AS CHAR FORMAT "x(18)" 
    FIELD age2    AS CHAR FORMAT "x(18)" 
    FIELD age3    AS CHAR FORMAT "x(18)" 
    FIELD age4    AS CHAR FORMAT "x(18)" 
    FIELD rechnr  AS CHAR FORMAT "x(9)"
    FIELD num     AS CHARACTER
    FIELD cust-nm AS CHARACTER
    FIELD p-bal   AS CHARACTER
    FIELD debit   AS CHARACTER
    FIELD credit  AS CHARACTER
    FIELD end-bal AS CHARACTER
. 

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER case-type        AS INTEGER.
DEFINE INPUT PARAMETER mtd-flag         AS LOGICAL.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE INPUT PARAMETER fdate            AS DATE.
DEFINE INPUT PARAMETER tdate            AS DATE.
DEFINE INPUT PARAMETER from-art         AS INTEGER.
DEFINE INPUT PARAMETER to-art           AS INTEGER.
DEFINE INPUT PARAMETER from-name        AS CHARACTER.
DEFINE INPUT PARAMETER to-name          AS CHARACTER.
DEFINE INPUT PARAMETER disptype         AS INTEGER.
DEFINE INPUT PARAMETER mi-bill          AS LOGICAL.
DEFINE INPUT PARAMETER day1             AS INTEGER.
DEFINE INPUT PARAMETER day2             AS INTEGER.
DEFINE INPUT PARAMETER day3             AS INTEGER.
DEFINE INPUT PARAMETER detailed         AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR arage-balance-list.
               
/* For Local Testing
DEFINE VARIABLE pvILanguage      AS INTEGER.
DEFINE VARIABLE case-type        AS INTEGER.
DEFINE VARIABLE mtd-flag         AS LOGICAL.
DEFINE VARIABLE to-date          AS DATE.
DEFINE VARIABLE fdate            AS DATE.
DEFINE VARIABLE tdate            AS DATE.
DEFINE VARIABLE from-art         AS INTEGER.
DEFINE VARIABLE to-art           AS INTEGER.
DEFINE VARIABLE from-name        AS CHARACTER.
DEFINE VARIABLE to-name          AS CHARACTER.
DEFINE VARIABLE disptype         AS INTEGER.
DEFINE VARIABLE mi-bill          AS LOGICAL.
DEFINE VARIABLE day1             AS INTEGER.
DEFINE VARIABLE day2             AS INTEGER.
DEFINE VARIABLE day3             AS INTEGER.
DEFINE VARIABLE detailed         AS LOGICAL.

ASSIGN
    pvILanguage = 1
    case-type   = 1
    mtd-flag    = YES
    to-date     = 11/22/21
    fdate       = ?
    tdate       = ?
    from-art    = 1
    to-art      = 30
    from-name   = ""
    to-name     = "zz"
    disptype    = 0
    mi-bill     = NO
    day1        = 30
    day2        = 60
    day3        = 90
    detailed    = NO
.
*/
DEFINE TEMP-TABLE arage-list 
    FIELD strdate AS CHAR FORMAT "x(8)"
    FIELD curr    AS CHAR FORMAT "x(4)"
    FIELD gastnr  AS INTEGER INITIAL 0
    FIELD artnr   AS INTEGER INITIAL 0
    FIELD age1    AS CHAR FORMAT "x(18)" 
    FIELD age2    AS CHAR FORMAT "x(18)" 
    FIELD age3    AS CHAR FORMAT "x(18)" 
    FIELD age4    AS CHAR FORMAT "x(18)" 
    FIELD rechnr  AS CHAR FORMAT "x(9)" 
    FIELD STR     AS CHAR. 

DEFINE TEMP-TABLE age-list 
    FIELD fcurr            AS CHAR 
    FIELD artnr           AS INTEGER 
    FIELD rechnr          AS INTEGER 
    FIELD counter         AS INTEGER 
    FIELD gastnr          AS INTEGER 
    FIELD rgdatum         AS DATE 
    FIELD gastname        AS CHARACTER FORMAT "x(34)" 
    FIELD p-bal           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debit           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD credit          AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD saldo           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt0           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt1           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt2           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt3           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0. 
 
DEFINE TEMP-TABLE ledger 
    FIELD artnr           AS INTEGER 
    FIELD bezeich         AS CHARACTER FORMAT "x(24)" INITIAL "?????" 
    FIELD p-bal           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debit           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD credit          AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt0           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt1           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt2           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD debt3           AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
    FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0. 


DEFINE VARIABLE curr-art AS INTEGER. 
DEFINE VARIABLE counter AS INTEGER FORMAT ">>>9". 
DEFINE VARIABLE t-saldo      AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-prev       AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debit      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-credit     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt0      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt1      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt2      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt3      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE tmp-saldo    AS DECIMAL FORMAT "->>>>>>>>>>9" INITIAL 0. 
DEFINE VARIABLE curr-name    AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE curr-gastnr  AS INTEGER. 
DEFINE VARIABLE gastname     AS CHARACTER FORMAT "x(34)". 
DEFINE VARIABLE p-bal        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debit        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE credit       AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt0        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt1        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt2        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt3        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE curr-counter AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-fcurr   AS CHAR NO-UNDO.
                           
DEFINE VARIABLE i   AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-debt AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" 
    LABEL "Total Debt" BGCOLOR 2  FGCOLOR 15. 

DEFINE VARIABLE from-date       AS DATE NO-UNDO. 
DEFINE VARIABLE default-fcurr   AS CHARACTER NO-UNDO.
DEFINE VARIABLE outlist         AS CHARACTER NO-UNDO FORMAT "x(172)". 
DEFINE VARIABLE long-digit      AS LOGICAL   NO-UNDO. 
DEFINE VARIABLE curr-rgdatum    AS DATE NO-UNDO. 

DEFINE BUFFER debtrec   FOR debitor.
DEFINE BUFFER debt      FOR debitor. 

DEFINE VARIABLE bill-number AS INTEGER INITIAL 0. 
DEFINE VARIABLE inp-gastnr  AS INTEGER INITIAL 0.
DEFINE VARIABLE inp-artnr   AS INTEGER INITIAL 0.

DEFINE VARIABLE tot-debtall  AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE tot-debt0    AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE tot-debt1    AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE tot-debt2    AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE tot-debt3    AS DECIMAL NO-UNDO INIT 0.

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "ar-age1". 

/*****************************************************************************/
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK.
default-fcurr = htparam.fchar.

IF mtd-flag THEN DO:
    IF case-type = 1 THEN
        RUN age-list1.
    ELSE RUN age-list2.
END.
ELSE DO:
    IF case-type = 1 THEN
        RUN age-list1a.
    ELSE RUN age-list2a.
END.

FOR EACH arage-balance-list:
    DELETE arage-balance-list.
END.

FOR EACH arage-list WHERE SUBSTRING(arage-list.STR, 1, 7) NE "-------":
    CREATE arage-balance-list.
    ASSIGN
        arage-balance-list.strdate   = arage-list.strdate
        arage-balance-list.curr      = arage-list.curr   
        arage-balance-list.gastnr    = arage-list.gastnr 
        arage-balance-list.artnr     = arage-list.artnr  
        arage-balance-list.age1      = arage-list.age1   
        arage-balance-list.age2      = arage-list.age2   
        arage-balance-list.age3      = arage-list.age3   
        arage-balance-list.age4      = arage-list.age4   
        arage-balance-list.rechnr    = arage-list.rechnr
        arage-balance-list.num       = SUBSTRING(arage-list.STR, 1, 7) 
        arage-balance-list.cust-nm   = SUBSTRING(arage-list.STR, 8, 30)
        arage-balance-list.p-bal     = SUBSTRING(arage-list.STR,56, 18)
        arage-balance-list.debit     = SUBSTRING(arage-list.STR,74, 18)
        arage-balance-list.credit    = SUBSTRING(arage-list.STR,92, 18)
        arage-balance-list.end-bal   = SUBSTRING(arage-list.STR,38, 18)
    .
END.

/****************************************************************************/

PROCEDURE age-list1: 
    ASSIGN  curr-art    = 0
            counter     = 0
            t-saldo     = 0
            t-prev      = 0
            t-debit     = 0
            t-credit    = 0
            t-debt0     = 0
            t-debt1     = 0
            t-debt2     = 0
            t-debt3     = 0
            tmp-saldo   = 0 
            curr-name = ""
            curr-gastnr = 0
            gastname    = ""
            p-bal       = 0
            debit       = 0
            credit      = 0
            debt0       = 0
            debt1       = 0
            debt2       = 0
            debt3       = 0
            tot-debt    = 0 
            i           = 0
            curr-counter = 0
            curr-fcurr = "".
 
    from-date = DATE(MONTH(to-date), 1, YEAR(to-date)). 
    FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
        AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
        AND artikel.departement = 0 
        NO-LOCK BY (STRING(artikel.artart) + STRING(artikel.artnr,"9999")): 

        /*M
        curr-bezeich = STRING(artikel.artnr, ">>>9") + " - " + artikel.bezeich. 
        DISP curr-bezeich WITH FRAME frame2. 
        */

        CREATE ledger. 
        ledger.artnr = artikel.artnr. 
        ledger.bezeich = STRING(artikel.artnr) + "  -  " + artikel.bezeich. 
    END. 

    /* NOT paid OR partial paid */ 
    curr-art = 0. 
    FOR EACH debitor WHERE debitor.rgdatum LE to-date 
        AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
        AND debitor.opart LE 1 NO-LOCK USE-INDEX artdat_ix 
        BY debitor.artnr BY debitor.zahlkonto: 

        IF debitor.name GE from-name THEN 
        DO: 
            IF curr-art NE debitor.artnr THEN 
            DO: 
                curr-art = debitor.artnr. 
                FIND FIRST artikel WHERE artikel.artnr = curr-art 
                    AND artikel.departement = 0  NO-LOCK NO-ERROR. 
            END. 

            IF debitor.counter > 0 THEN 
                FIND FIRST age-list WHERE age-list.counter = debitor.counter NO-ERROR. 
            IF (debitor.counter = 0) OR (NOT AVAILABLE age-list) THEN 
            DO: 
                /* create aging record FOR a specific guest, based ON A/R-debit record */ 
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
                CREATE age-list. 
                age-list.artnr = debitor.artnr. 
                age-list.rechnr = debitor.rechnr. 
                age-list.rgdatum = debitor.rgdatum. 
                age-list.counter = debitor.counter. 
                age-list.gastnr = debitor.gastnr. 
                age-list.tot-debt = 0. 

                IF debitor.betrieb-gastmem = 0 THEN
                    age-list.fcurr = default-fcurr.
                ELSE
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN age-list.fcurr = waehrung.wabkurz.
                END.

                IF artikel.artart = 2 THEN 
                    age-list.gastname = guest.name + ", " + guest.vorname1 + 
                                    guest.anredefirma + " " + guest.anrede1. 
                ELSE 
                DO: 
                    FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
                    IF debitor.gastnr = htparam.finteger THEN 
                        age-list.gastname = "F&B " + artikel.bezeich. 
                    ELSE age-list.gastname = "F/O " + artikel.bezeich. 
                END. 

                /*M
                guest-name = guest.name + ", " + guest.vorname1 
                + guest.anredefirma + " " + guest.anrede1. 
                DISP guest-name WITH FRAME frame2. 
                */
            END. 
            IF disptype = 0 THEN
                age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
            ELSE 
                age-list.tot-debt = age-list.tot-debt + debitor.vesrdep. 

            /* previous balance  */ 
            IF debitor.rgdatum LT from-date AND debitor.zahlkonto = 0 THEN 
            DO:
                IF disptype = 0 THEN
                    age-list.p-bal = age-list.p-bal + debitor.saldo. 
                ELSE
                    age-list.p-bal = age-list.p-bal + debitor.vesrdep. 
            END.

            /* debit transaction */ 
            IF debitor.rgdatum GE from-date AND debitor.zahlkonto = 0 THEN 
            DO:
                IF disptype = 0 THEN
                    age-list.debit = age-list.debit + debitor.saldo. 
                ELSE
                    age-list.debit = age-list.debit + debitor.vesrdep. 
            END.
            
            /* credit transaction */ 
            IF debitor.rgdatum LT from-date AND debitor.zahlkonto NE 0 THEN 
            DO:
                IF disptype = 0 THEN
                    age-list.p-bal = age-list.p-bal + debitor.saldo. 
                ELSE
                    age-list.p-bal = age-list.p-bal + debitor.vesrdep. 
            END.
            ELSE 
            DO: 
                IF debitor.rgdatum GE from-date AND debitor.zahlkonto NE 0 THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.credit = age-list.credit - debitor.saldo. 
                    ELSE 
                        age-list.credit = age-list.credit - debitor.vesrdep. 
                END.
            END. 
        END. 
    END. 

    /*  within period's full paid transaction */ 
    FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
        AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
        AND artikel.departement = 0 NO-LOCK BY artikel.artnr: 

        /*M
        curr-bezeich = STRING(artikel.artnr, ">>>9") + " - " + artikel.bezeich. 
        DISP curr-bezeich WITH FRAME frame2. 
        */
        
        curr-counter = 0. 
        FOR EACH debitor WHERE debitor.artnr = artikel.artnr 
            AND debitor.rgdatum LE to-date 
            AND debitor.opart EQ 2 AND debitor.zahlkonto EQ 0 
            USE-INDEX artdat_ix NO-LOCK: 
            IF debitor.name GE from-name  THEN 
            DO: 
                /* create aging record FOR a specific guest */ 
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
                CREATE age-list. 
                age-list.artnr = debitor.artnr. 
                age-list.rechnr = debitor.rechnr. 
                age-list.rgdatum = debitor.rgdatum. 
                age-list.counter = debitor.counter. 
                age-list.gastnr = debitor.gastnr.  
                age-list.tot-debt = debitor.saldo. 

                IF debitor.betrieb-gastmem = 0 THEN
                    age-list.fcurr = default-fcurr.
                ELSE
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN
                        age-list.fcurr = waehrung.wabkurz.
                END.

                IF artikel.artart = 2 THEN 
                    age-list.gastname = guest.name + ", " + guest.vorname1 +
                                        guest.anredefirma + " " + guest.anrede1. 
                ELSE 
                DO: 
                    FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
                    IF debitor.gastnr = htparam.finteger THEN 
                        age-list.gastname = "F&B " + artikel.bezeich. 
                    ELSE age-list.gastname = "F/O " + artikel.bezeich. 
                END. 

                /*M
                guest-name = guest.name + ", " + guest.vorname1 
                + guest.anredefirma + " " + guest.anrede1. 
                DISP guest-name WITH FRAME frame2. 
                */

                IF debitor.rgdatum LT from-date THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.p-bal = age-list.p-bal + debitor.saldo. 
                    ELSE
                        age-list.p-bal = age-list.p-bal + debitor.vesrdep. 
                END.
                ELSE IF debitor.rgdatum GE from-date THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.debit = age-list.debit + debitor.saldo. 
                    ELSE
                        age-list.debit = age-list.debit + debitor.vesrdep. 
                END.                                                     

                FOR EACH debtrec WHERE debtrec.counter = debitor.counter 
                    AND debtrec.rechnr = debitor.rechnr AND debtrec.zahlkonto GT 0 
                    AND debtrec.rgdatum LE to-date NO-LOCK USE-INDEX counter_ix: 
                    age-list.tot-debt = age-list.tot-debt + debtrec.saldo. 
                    
                    IF debtrec.rgdatum LT from-date THEN 
                    DO:
                        IF disptype = 0 THEN
                            age-list.p-bal = age-list.p-bal + debtrec.saldo. 
                        ELSE 
                            age-list.p-bal = age-list.p-bal + debtrec.vesrdep. 
                    END.
                    ELSE IF debtrec.rgdatum GE from-date THEN 
                    DO:
                        IF disptype = 0 THEN
                            age-list.credit = age-list.credit - debtrec.saldo. 
                        ELSE 
                            age-list.credit = age-list.credit - debtrec.vesrdep. 
                    END.
                END. 
            END. 
        END. 
    END. 

    FOR EACH age-list:
        IF age-list.p-bal GE - 0.01 AND age-list.p-bal LE 0.01
            AND age-list.debit = 0 AND age-list.credit = 0 THEN
            DELETE age-list.
    END.

    FOR EACH ledger BY ledger.artnr: 
        outlist = "    " + caps(ledger.bezeich). 
        RUN fill-in-list(NO, "", ?). 
        outlist = "". 
        RUN fill-in-list(NO, "", ?). 
        counter = 0. 
        curr-gastnr = 0. 

        IF mi-bill THEN
            FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
                /* AND age-list.tot-debt NE 0 */ BY age-list.rgdatum
                BY age-list.gastname BY age-list.rechnr: 
                RUN create-output.
            END.
        ELSE
            FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
                /* AND age-list.tot-debt NE 0 */ BY age-list.gastname 
                BY age-list.rechnr: 
                RUN create-output.
            END. 

        IF counter GT 0 AND (p-bal NE 0 OR debit NE 0 OR credit NE 0) THEN 
        DO: 
            IF NOT long-digit THEN 
                outlist = "  " + STRING(counter,">>>9 ") 
                            + STRING(gastname, "x(30)") 
                            + STRING(tot-debt, "->>,>>>,>>>,>>9.99") 
                            + STRING(p-bal, "->>,>>>,>>>,>>9.99") 
                            + STRING(debit, "->>,>>>,>>>,>>9.99") 
                            + STRING(credit, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt0, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt1, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt2, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt3, "->>,>>>,>>>,>>9.99"). 
            ELSE outlist = "  " + STRING(counter,">>>9 ") 
                            + STRING(gastname, "x(30)") 
                            + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") 
                            + STRING(p-bal, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debit, "->,>>>,>>>,>>>,>>9") 
                            + STRING(credit, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt0, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt1, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt2, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt3, "->,>>>,>>>,>>>,>>9"). 

            RUN fill-in-list(YES, curr-fcurr, curr-rgdatum). 
        END. 
        ELSE counter = counter - 1. 

        tmp-saldo = ledger.tot-debt. 
        IF tmp-saldo = 0 THEN tmp-saldo = 1. 
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
        RUN fill-in-list(NO, "----", ?). 
        IF NOT long-digit THEN 
            outlist = "       " 
                    + STRING(translateExtended ("T o t a l",lvCAREA,""), "x(30)") 
                    + STRING(ledger.tot-debt, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.p-bal, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debit, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.credit, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt0, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt1, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt2, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt3, "->>,>>>,>>>,>>9.99"). 
        ELSE outlist = "       " 
                    + STRING(translateExtended ("T o t a l",lvCAREA,""), "x(30)") 
                    + STRING(ledger.tot-debt, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.p-bal, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debit, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.credit, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debt0, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debt1, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debt2, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debt3, "->,>>>,>>>,>>>,>>9"). 

        RUN fill-in-list(NO, "", ?). 
        outlist = "       " 
                + STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)") 
                + "            100.00". 

        DO i = 1 TO 54: 
            outlist = outlist + " ". 
        END. 

        ASSIGN
            tot-debt0   = (ledger.debt0 / tmp-saldo * 100)
            tot-debt1   = (ledger.debt1 / tmp-saldo * 100)
            tot-debt2   = (ledger.debt2 / tmp-saldo * 100)
            tot-debt3   = (ledger.debt3 / tmp-saldo * 100).

        IF tot-debt0 = ? THEN tot-debt0 = 0.
        IF tot-debt1 = ? THEN tot-debt1 = 0.
        IF tot-debt2 = ? THEN tot-debt2 = 0.
        IF tot-debt3 = ? THEN tot-debt3 = 0.

        
        outlist = outlist + STRING(tot-debt0, "         ->,>>9.99") /*->>9.99*/
                + STRING(tot-debt1, "         ->,>>9.99") /*->>9.99*/
                + STRING(tot-debt2, "         ->,>>9.99") /*->>9.99*/
                + STRING(tot-debt3, "         ->,>>9.99") /*->>9.99*/. 
        
        RUN fill-in-list(NO, "", ?). 
        outlist = "". 
        RUN fill-in-list(NO, "", ?). 
    END. 

    outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
    RUN fill-in-list(NO, "----", ?). 
    IF NOT long-digit THEN 
        outlist = "       " 
                + STRING(translateExtended ("T O T A L  A/R:",lvCAREA,""), "x(30)") 
                + STRING(t-saldo, "->>,>>>,>>>,>>9.99") 
                + STRING(t-prev, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debit, "->>,>>>,>>>,>>9.99") 
                + STRING(t-credit, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt0, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt1, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt2, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt3, "->>,>>>,>>>,>>9.99"). 
    ELSE outlist = "       " 
                + STRING(translateExtended ("T O T A L  A/R:",lvCAREA,""), "x(30)") 
                + STRING(t-saldo, "->,>>>,>>>,>>>,>>9")     
                + STRING(t-prev, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debit, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-credit, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt0, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt1, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt2, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt3, "->,>>>,>>>,>>>,>>9"). 

    RUN fill-in-list(NO, "", ?). 
    outlist = "       " 
            + STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)") 
            + "            100.00". 

    DO i = 1 TO 54: 
        outlist = outlist + " ". 
    END. 

    ASSIGN
        tot-debt0   = (t-debt0 / t-saldo * 100)
        tot-debt1   = (t-debt1 / t-saldo * 100)
        tot-debt2   = (t-debt2 / t-saldo * 100)
        tot-debt3   = (t-debt3 / t-saldo * 100).

    IF tot-debt0 = ? THEN tot-debt0 = 0.
    IF tot-debt1 = ? THEN tot-debt1 = 0.
    IF tot-debt2 = ? THEN tot-debt2 = 0.
    IF tot-debt3 = ? THEN tot-debt3 = 0.

    outlist = outlist 
            + STRING(tot-debt0, "           ->>9.99") 
            + STRING(tot-debt1, "           ->>9.99") 
            + STRING(tot-debt2, "           ->>9.99") 
            + STRING(tot-debt3, "           ->>9.99"). 

    RUN fill-in-list(NO, "", ?). 
    outlist = "". 
    RUN fill-in-list(NO, "", ?). 
    /*M
    HIDE FRAME frame2 NO-PAUSE. 
    */
END. 


PROCEDURE age-list2: 
    ASSIGN  curr-art    = 0
            counter     = 0
            t-saldo     = 0
            t-prev      = 0
            t-debit     = 0
            t-credit    = 0
            t-debt0     = 0
            t-debt1     = 0
            t-debt2     = 0
            t-debt3     = 0
            tmp-saldo   = 0 
            curr-name = ""
            curr-gastnr = 0
            gastname    = ""
            p-bal       = 0
            debit       = 0
            credit      = 0
            debt0       = 0
            debt1       = 0
            debt2       = 0
            debt3       = 0
            tot-debt    = 0 
            i           = 0
            curr-counter = 0
            curr-fcurr = "".

    from-date = DATE(MONTH(to-date), 1, YEAR(to-date)). 
    FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
        AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
        AND artikel.departement = 0 NO-LOCK 
        BY (STRING(artikel.artart) + STRING(artikel.artnr,"9999")): 

        /*M
        curr-bezeich = STRING(artikel.artnr, ">>>9") + " - " + artikel.bezeich. 
        DISP curr-bezeich WITH FRAME frame2. 
        */
        CREATE ledger. 
        ledger.artnr = artikel.artnr. 
        ledger.bezeich = STRING(artikel.artnr) + "  -  " + artikel.bezeich. 
    END. 

    /* NOT paid OR partial paid */ 
    curr-art = 0. 
    FOR EACH debitor WHERE debitor.rgdatum LE to-date 
        AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
        AND debitor.opart LE 1 NO-LOCK USE-INDEX artdat_ix 
        BY debitor.artnr BY debitor.zahlkonto: 
        
        IF debitor.name GE from-name AND debitor.name LE to-name THEN 
        DO: 
            IF curr-art NE debitor.artnr THEN 
            DO: 
                curr-art = debitor.artnr. 
                FIND FIRST artikel WHERE artikel.artnr = curr-art 
                    AND artikel.departement = 0  NO-LOCK NO-ERROR. 
            END. 

            IF debitor.counter > 0 THEN 
                FIND FIRST age-list WHERE age-list.counter = debitor.counter NO-ERROR. 
            IF (debitor.counter = 0) OR (NOT AVAILABLE age-list) THEN 
            DO: 
                /* create aging record FOR a specific guest, based ON A/R-debit record */ 
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
                CREATE age-list. 
                age-list.artnr = debitor.artnr. 
                age-list.rechnr = debitor.rechnr. 
                age-list.rgdatum = debitor.rgdatum. 
                age-list.counter = debitor.counter. 
                age-list.gastnr = debitor.gastnr. 
                age-list.tot-debt = 0. 
                IF debitor.betrieb-gastmem = 0 THEN
                    age-list.fcurr = default-fcurr.
                ELSE
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN
                        age-list.fcurr = waehrung.wabkurz.
                END.

                IF artikel.artart = 2 THEN 
                    age-list.gastname = guest.name + ", " + guest.vorname1 + 
                                        guest.anredefirma + " " + guest.anrede1. 
                ELSE 
                DO: 
                    FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
                    IF debitor.gastnr = htparam.finteger THEN 
                        age-list.gastname = "F&B " + artikel.bezeich. 
                    ELSE age-list.gastname = "F/O " + artikel.bezeich. 
                END. 

                /*M
                guest-name = guest.name + ", " + guest.vorname1 
                             + guest.anredefirma + " " + guest.anrede1. 
                DISP guest-name WITH FRAME frame2. 
                */
            END. 

            IF disptype = 0 THEN
                age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
            ELSE
                age-list.tot-debt = age-list.tot-debt + debitor.vesrdep. 

            /* previous balance  */ 
            IF debitor.rgdatum LT from-date AND debitor.zahlkonto = 0 THEN 
            DO:
                IF disptype = 0 THEN
                    age-list.p-bal = age-list.p-bal + debitor.saldo. 
                ELSE age-list.p-bal = age-list.p-bal + debitor.vesrdep. 
            END.

            /* debit transaction */ 
            IF debitor.rgdatum GE from-date AND debitor.zahlkonto = 0 THEN 
            DO: 
                IF disptype = 0 THEN
                    age-list.debit = age-list.debit + debitor.saldo. 
                ELSE age-list.debit = age-list.debit + debitor.vesrdep. 
            END.

            /* credit transaction */ 
            IF debitor.rgdatum LT from-date AND debitor.zahlkonto NE 0 THEN 
                age-list.p-bal = age-list.p-bal + debitor.saldo. 
            ELSE 
            DO: 
                IF debitor.rgdatum GE from-date AND debitor.zahlkonto NE 0 THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.credit = age-list.credit - debitor.saldo. 
                    ELSE age-list.credit = age-list.credit - debitor.vesrdep. 
                END.
            END. 
        END. 
    END. 

    /*  within period's full paid transaction */ 
    FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
        AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
        AND artikel.departement = 0 NO-LOCK BY artikel.artnr: 

        /*M
        curr-bezeich = STRING(artikel.artnr, ">>>9") + " - " + artikel.bezeich. 
        DISP curr-bezeich WITH FRAME frame2. 
        */

        curr-counter = 0. 
        FOR EACH debitor WHERE debitor.artnr = artikel.artnr 
            AND debitor.rgdatum LE to-date 
            AND debitor.opart EQ 2 AND debitor.zahlkonto EQ 0 
            USE-INDEX artdat_ix NO-LOCK: 
            IF debitor.name GE from-name AND debitor.name LE to-name THEN 
            DO: 
                /* create aging record FOR a specific guest */ 
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
                CREATE age-list. 
                age-list.artnr = debitor.artnr. 
                age-list.rechnr = debitor.rechnr. 
                age-list.rgdatum = debitor.rgdatum. 
                age-list.counter = debitor.counter. 
                age-list.gastnr = debitor.gastnr. 
                age-list.tot-debt = debitor.saldo. 
                IF debitor.betrieb-gastmem = 0 THEN
                    age-list.fcurr = default-fcurr.
                ELSE
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN
                        age-list.fcurr = waehrung.wabkurz.
                END.

                IF artikel.artart = 2 THEN 
                    age-list.gastname = guest.name + ", " + guest.vorname1 + 
                                        guest.anredefirma + " " + guest.anrede1. 
                ELSE 
                DO: 
                    FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
                    IF debitor.gastnr = htparam.finteger THEN 
                        age-list.gastname = "F&B " + artikel.bezeich. 
                    ELSE age-list.gastname = "F/O " + artikel.bezeich. 
                END. 

                /*M
                guest-name = guest.name + ", " + guest.vorname1 
                            + guest.anredefirma + " " + guest.anrede1. 
                DISP guest-name WITH FRAME frame2. 
                */

                IF debitor.rgdatum LT from-date THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.p-bal = age-list.p-bal + debitor.saldo. 
                    ELSE
                        age-list.p-bal = age-list.p-bal + debitor.vesrdep.
                END.
                ELSE IF debitor.rgdatum GE from-date THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.debit = age-list.debit + debitor.saldo. 
                    ELSE 
                        age-list.debit = age-list.debit + debitor.vesrdep. 
                END.

                FOR EACH debtrec WHERE debtrec.counter = debitor.counter 
                    AND debtrec.rechnr = debitor.rechnr AND debtrec.zahlkonto GT 0 
                    AND debtrec.rgdatum LE to-date NO-LOCK USE-INDEX counter_ix: 
                    age-list.tot-debt = age-list.tot-debt + debtrec.saldo. 
                    IF debtrec.rgdatum LT from-date THEN 
                    DO:
                        IF disptype = 0 THEN
                            age-list.p-bal = age-list.p-bal + debtrec.saldo. 
                        ELSE 
                            age-list.p-bal = age-list.p-bal + debtrec.vesrdep. 
                    END.
                    ELSE IF debtrec.rgdatum GE from-date THEN 
                    DO:
                        IF disptype = 0 THEN
                            age-list.credit = age-list.credit - debtrec.saldo. 
                        ELSE
                            age-list.credit = age-list.credit - debtrec.vesrdep. 
                    END.
                END. 
            END. 
        END. 
    END. 
     
    FOR EACH age-list:
        IF age-list.p-bal GE - 0.01 AND age-list.p-bal LE 0.01
            AND age-list.debit = 0 AND age-list.credit = 0 THEN
            DELETE age-list.
    END.

    FOR EACH ledger BY ledger.artnr: 
        outlist = "    " + caps(ledger.bezeich). 
        RUN fill-in-list(NO, "", ?). 
        outlist = "". 
        RUN fill-in-list(NO, "", ?). 
        counter = 0. 
        curr-gastnr = 0. 
        IF mi-bill THEN
            FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
                BY age-list.rgdatum BY age-list.gastname :
                RUN create-output.
            END.
        ELSE
            FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
                BY age-list.gastname BY age-list.rechnr: 
                RUN create-output.
            END. 

        IF counter GT 0 AND (p-bal NE 0 OR debit NE 0 OR credit NE 0) THEN 
        DO: 
            IF NOT long-digit THEN 
                outlist = "  " + STRING(counter,">>>9 ") 
                        + STRING(gastname, "x(30)") 
                        + STRING(tot-debt, "->>,>>>,>>>,>>9.99") 
                        + STRING(p-bal, "->>,>>>,>>>,>>9.99") 
                        + STRING(debit, "->>,>>>,>>>,>>9.99") 
                        + STRING(credit, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt0, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt1, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt2, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt3, "->>,>>>,>>>,>>9.99"). 
            ELSE outlist = "  " + STRING(counter,">>>9 ") 
                        + STRING(gastname, "x(30)") 
                        + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") 
                        + STRING(p-bal, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debit, "->,>>>,>>>,>>>,>>9") 
                        + STRING(credit, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debt0, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debt1, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debt2, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debt3, "->,>>>,>>>,>>>,>>9"). 
            RUN fill-in-list(YES, curr-fcurr, curr-rgdatum). 
        END. 
        ELSE counter = counter - 1. 

        tmp-saldo = ledger.tot-debt. 
        IF tmp-saldo = 0 THEN tmp-saldo = 1. 
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
        RUN fill-in-list(NO, "----", ?). 
        IF NOT long-digit THEN 
            outlist = "       " 
                    + STRING(translateExtended ("T o t a l",lvCAREA,""), "x(30)") 
                    + STRING(ledger.tot-debt, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.p-bal, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debit, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.credit, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt0, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt1, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt2, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt3, "->>,>>>,>>>,>>9.99"). 
        ELSE outlist = "       " 
            + STRING(translateExtended ("T o t a l",lvCAREA,""), "x(30)") 
            + STRING(ledger.tot-debt, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.p-bal, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debit, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.credit, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debt0, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debt1, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debt2, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debt3, "->,>>>,>>>,>>>,>>9"). 

        RUN fill-in-list(NO, "", ?). 
        outlist = "       " 
                + STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)") 
                + "            100.00". 

        DO i = 1 TO 54: 
            outlist = outlist + " ". 
        END. 

         ASSIGN
            tot-debt0   = (ledger.debt0 / tmp-saldo * 100)
            tot-debt1   = (ledger.debt1 / tmp-saldo * 100)
            tot-debt2   = (ledger.debt2 / tmp-saldo * 100)
            tot-debt3   = (ledger.debt3 / tmp-saldo * 100).

        IF tot-debt0 = ? THEN tot-debt0 = 0.
        IF tot-debt1 = ? THEN tot-debt1 = 0.
        IF tot-debt2 = ? THEN tot-debt2 = 0.
        IF tot-debt3 = ? THEN tot-debt3 = 0.

        
        outlist = outlist 
                + STRING(tot-debt0, "           ->>9.99") 
                + STRING(tot-debt1, "           ->>9.99") 
                + STRING(tot-debt2, "           ->>9.99") 
                + STRING(tot-debt3, "           ->>9.99"). 
        RUN fill-in-list(NO, "", ?). 
        outlist = "". 
        RUN fill-in-list(NO, "", ?). 
    END. 

    outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
    RUN fill-in-list(NO, "----", ?). 
    IF NOT long-digit THEN 
        outlist = "       " 
                + STRING(translateExtended ("T O T A L  A/R:",lvCAREA,""), "x(30)")
                + STRING(t-saldo, "->>,>>>,>>>,>>9.99") 
                + STRING(t-prev, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debit, "->>,>>>,>>>,>>9.99") 
                + STRING(t-credit, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt0, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt1, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt2, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt3, "->>,>>>,>>>,>>9.99"). 
    ELSE outlist = "       " 
                + STRING(translateExtended ("T O T A L  A/R:",lvCAREA,""), "x(30)")
                + STRING(t-saldo, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-prev, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debit, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-credit, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt0, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt1, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt2, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt3, "->,>>>,>>>,>>>,>>9"). 

    RUN fill-in-list(NO, "", ?). 
    outlist = "       " 
            + STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)") 
            + "            100.00". 
    
    DO i = 1 TO 54: 
        outlist = outlist + " ". 
    END. 

    ASSIGN
        tot-debt0   = (t-debt0 / t-saldo * 100)
        tot-debt1   = (t-debt1 / t-saldo * 100)
        tot-debt2   = (t-debt2 / t-saldo * 100)
        tot-debt3   = (t-debt3 / t-saldo * 100).

    IF tot-debt0 = ? THEN tot-debt0 = 0.
    IF tot-debt1 = ? THEN tot-debt1 = 0.
    IF tot-debt2 = ? THEN tot-debt2 = 0.
    IF tot-debt3 = ? THEN tot-debt3 = 0.

    outlist = outlist 
            + STRING(tot-debt0, "           ->>9.99") 
            + STRING(tot-debt1, "           ->>9.99") 
            + STRING(tot-debt2, "           ->>9.99") 
            + STRING(tot-debt3, "           ->>9.99"). 

    RUN fill-in-list(NO, "", ?). 
    outlist = "". 
    RUN fill-in-list(NO, "", ?). 
    /*M
    hide FRAME frame2 NO-PAUSE. 
    */
END. 

PROCEDURE age-list1a: 
    ASSIGN  curr-art    = 0
            counter     = 0
            t-saldo     = 0
            t-prev      = 0
            t-debit     = 0
            t-credit    = 0
            t-debt0     = 0
            t-debt1     = 0
            t-debt2     = 0
            t-debt3     = 0
            tmp-saldo   = 0 
            curr-name = ""
            curr-gastnr = 0
            gastname    = ""
            p-bal       = 0
            debit       = 0
            credit      = 0
            debt0       = 0
            debt1       = 0
            debt2       = 0
            debt3       = 0
            tot-debt    = 0 
            i           = 0
            curr-counter = 0
            curr-fcurr = "".
 
    from-date = fdate. 
    FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
        AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
        AND artikel.departement = 0 
        NO-LOCK BY (STRING(artikel.artart) + STRING(artikel.artnr,"9999")): 

        /*M
        curr-bezeich = STRING(artikel.artnr, ">>>9") + " - " + artikel.bezeich. 
        DISP curr-bezeich WITH FRAME frame2. 
        */

        CREATE ledger. 
        ledger.artnr = artikel.artnr. 
        ledger.bezeich = STRING(artikel.artnr) + "  -  " + artikel.bezeich. 
    END. 

    /* NOT paid OR partial paid */ 
    curr-art = 0. 
    FOR EACH debitor WHERE debitor.rgdatum LE tdate 
        AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
        AND debitor.opart LE 1 NO-LOCK USE-INDEX artdat_ix 
        BY debitor.artnr BY debitor.zahlkonto: 

        IF debitor.name GE from-name THEN 
        DO: 
            IF curr-art NE debitor.artnr THEN 
            DO: 
                curr-art = debitor.artnr. 
                FIND FIRST artikel WHERE artikel.artnr = curr-art 
                    AND artikel.departement = 0  NO-LOCK NO-ERROR. 
            END. 

            IF debitor.counter > 0 THEN 
                FIND FIRST age-list WHERE age-list.counter = debitor.counter NO-ERROR. 
            IF (debitor.counter = 0) OR (NOT AVAILABLE age-list) THEN 
            DO: 
                /* create aging record FOR a specific guest, based ON A/R-debit record */ 
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
                CREATE age-list. 
                age-list.artnr = debitor.artnr. 
                age-list.rechnr = debitor.rechnr. 
                age-list.rgdatum = debitor.rgdatum. 
                age-list.counter = debitor.counter. 
                age-list.gastnr = debitor.gastnr. 
                age-list.tot-debt = 0. 

                IF debitor.betrieb-gastmem = 0 THEN
                    age-list.fcurr = default-fcurr.
                ELSE
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN age-list.fcurr = waehrung.wabkurz.
                END.

                IF artikel.artart = 2 THEN 
                    age-list.gastname = guest.name + ", " + guest.vorname1 + 
                                    guest.anredefirma + " " + guest.anrede1. 
                ELSE 
                DO: 
                    FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
                    IF debitor.gastnr = htparam.finteger THEN 
                        age-list.gastname = "F&B " + artikel.bezeich. 
                    ELSE age-list.gastname = "F/O " + artikel.bezeich. 
                END. 

                /*M
                guest-name = guest.name + ", " + guest.vorname1 
                + guest.anredefirma + " " + guest.anrede1. 
                DISP guest-name WITH FRAME frame2. 
                */
            END. 
            IF disptype = 0 THEN
                age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
            ELSE 
                age-list.tot-debt = age-list.tot-debt + debitor.vesrdep. 

            /* previous balance  */ 
            IF debitor.rgdatum LT from-date AND debitor.zahlkonto = 0 THEN 
            DO:
                IF disptype = 0 THEN
                    age-list.p-bal = age-list.p-bal + debitor.saldo. 
                ELSE
                    age-list.p-bal = age-list.p-bal + debitor.vesrdep. 
            END.

            /* debit transaction */ 
            IF debitor.rgdatum GE from-date AND debitor.zahlkonto = 0 THEN 
            DO:
                IF disptype = 0 THEN
                    age-list.debit = age-list.debit + debitor.saldo. 
                ELSE
                    age-list.debit = age-list.debit + debitor.vesrdep. 
            END.
            
            /* credit transaction */ 
            IF debitor.rgdatum LT from-date AND debitor.zahlkonto NE 0 THEN 
            DO:
                IF disptype = 0 THEN
                    age-list.p-bal = age-list.p-bal + debitor.saldo. 
                ELSE
                    age-list.p-bal = age-list.p-bal + debitor.vesrdep. 
            END.
            ELSE 
            DO: 
                IF debitor.rgdatum GE from-date AND debitor.zahlkonto NE 0 THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.credit = age-list.credit - debitor.saldo. 
                    ELSE 
                        age-list.credit = age-list.credit - debitor.vesrdep. 
                END.
            END. 
        END. 
    END. 

    /*  within period's full paid transaction */ 
    FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
        AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
        AND artikel.departement = 0 NO-LOCK BY artikel.artnr: 

        /*M
        curr-bezeich = STRING(artikel.artnr, ">>>9") + " - " + artikel.bezeich. 
        DISP curr-bezeich WITH FRAME frame2. 
        */
        
        curr-counter = 0. 
        FOR EACH debitor WHERE debitor.artnr = artikel.artnr 
            AND debitor.rgdatum LE to-date 
            AND debitor.opart EQ 2 AND debitor.zahlkonto EQ 0 
            USE-INDEX artdat_ix NO-LOCK: 
            IF debitor.name GE from-name  THEN 
            DO: 
                /* create aging record FOR a specific guest */ 
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
                CREATE age-list. 
                age-list.artnr = debitor.artnr. 
                age-list.rechnr = debitor.rechnr. 
                age-list.rgdatum = debitor.rgdatum. 
                age-list.counter = debitor.counter. 
                age-list.gastnr = debitor.gastnr.  
                age-list.tot-debt = debitor.saldo. 

                IF debitor.betrieb-gastmem = 0 THEN
                    age-list.fcurr = default-fcurr.
                ELSE
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN
                        age-list.fcurr = waehrung.wabkurz.
                END.

                IF artikel.artart = 2 THEN 
                    age-list.gastname = guest.name + ", " + guest.vorname1 +
                                        guest.anredefirma + " " + guest.anrede1. 
                ELSE 
                DO: 
                    FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
                    IF debitor.gastnr = htparam.finteger THEN 
                        age-list.gastname = "F&B " + artikel.bezeich. 
                    ELSE age-list.gastname = "F/O " + artikel.bezeich. 
                END. 

                /*M
                guest-name = guest.name + ", " + guest.vorname1 
                + guest.anredefirma + " " + guest.anrede1. 
                DISP guest-name WITH FRAME frame2. 
                */

                IF debitor.rgdatum LT from-date THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.p-bal = age-list.p-bal + debitor.saldo. 
                    ELSE
                        age-list.p-bal = age-list.p-bal + debitor.vesrdep. 
                END.
                ELSE IF debitor.rgdatum GE from-date THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.debit = age-list.debit + debitor.saldo. 
                    ELSE
                        age-list.debit = age-list.debit + debitor.vesrdep. 
                END.                                                     

                FOR EACH debtrec WHERE debtrec.counter = debitor.counter 
                    AND debtrec.rechnr = debitor.rechnr AND debtrec.zahlkonto GT 0 
                    AND debtrec.rgdatum LE to-date NO-LOCK USE-INDEX counter_ix: 
                    age-list.tot-debt = age-list.tot-debt + debtrec.saldo. 
                    
                    IF debtrec.rgdatum LT from-date THEN 
                    DO:
                        IF disptype = 0 THEN
                            age-list.p-bal = age-list.p-bal + debtrec.saldo. 
                        ELSE 
                            age-list.p-bal = age-list.p-bal + debtrec.vesrdep. 
                    END.
                    ELSE IF debtrec.rgdatum GE from-date THEN 
                    DO:
                        IF disptype = 0 THEN
                            age-list.credit = age-list.credit - debtrec.saldo. 
                        ELSE 
                            age-list.credit = age-list.credit - debtrec.vesrdep. 
                    END.
                END. 
            END. 
        END. 
    END. 

    FOR EACH age-list:
        IF age-list.p-bal GE - 0.01 AND age-list.p-bal LE 0.01
            AND age-list.debit = 0 AND age-list.credit = 0 THEN
            DELETE age-list.
    END.

    FOR EACH ledger BY ledger.artnr: 
        outlist = "    " + caps(ledger.bezeich). 
        RUN fill-in-list(NO, "", ?). 
        outlist = "". 
        RUN fill-in-list(NO, "", ?). 
        counter = 0. 
        curr-gastnr = 0. 

        IF mi-bill THEN
            FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
                /* AND age-list.tot-debt NE 0 */ BY age-list.rgdatum
                BY age-list.gastname BY age-list.rechnr: 
                RUN create-output.
            END.
        ELSE
            FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
                /* AND age-list.tot-debt NE 0 */ BY age-list.gastname 
                BY age-list.rechnr: 
                RUN create-output.
            END. 

        IF counter GT 0 AND (p-bal NE 0 OR debit NE 0 OR credit NE 0) THEN 
        DO: 
            IF NOT long-digit THEN 
                outlist = "  " + STRING(counter,">>>9 ") 
                            + STRING(gastname, "x(30)") 
                            + STRING(tot-debt, "->>,>>>,>>>,>>9.99") 
                            + STRING(p-bal, "->>,>>>,>>>,>>9.99") 
                            + STRING(debit, "->>,>>>,>>>,>>9.99") 
                            + STRING(credit, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt0, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt1, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt2, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt3, "->>,>>>,>>>,>>9.99"). 
            ELSE outlist = "  " + STRING(counter,">>>9 ") 
                            + STRING(gastname, "x(30)") 
                            + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") 
                            + STRING(p-bal, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debit, "->,>>>,>>>,>>>,>>9") 
                            + STRING(credit, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt0, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt1, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt2, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt3, "->,>>>,>>>,>>>,>>9"). 

            RUN fill-in-list(YES, curr-fcurr, curr-rgdatum). 
        END. 
        ELSE counter = counter - 1. 

        tmp-saldo = ledger.tot-debt. 
        IF tmp-saldo = 0 THEN tmp-saldo = 1. 
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
        RUN fill-in-list(NO, "----", ?). 
        IF NOT long-digit THEN 
            outlist = "       " 
                    + STRING(translateExtended ("T o t a l",lvCAREA,""), "x(30)") 
                    + STRING(ledger.tot-debt, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.p-bal, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debit, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.credit, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt0, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt1, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt2, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt3, "->>,>>>,>>>,>>9.99"). 
        ELSE outlist = "       " 
                    + STRING(translateExtended ("T o t a l",lvCAREA,""), "x(30)") 
                    + STRING(ledger.tot-debt, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.p-bal, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debit, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.credit, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debt0, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debt1, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debt2, "->,>>>,>>>,>>>,>>9") 
                    + STRING(ledger.debt3, "->,>>>,>>>,>>>,>>9"). 

        RUN fill-in-list(NO, "", ?). 
        outlist = "       " 
                + STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)") 
                + "            100.00". 

        DO i = 1 TO 54: 
            outlist = outlist + " ". 
        END. 

        ASSIGN
            tot-debt0   = (ledger.debt0 / tmp-saldo * 100)
            tot-debt1   = (ledger.debt1 / tmp-saldo * 100)
            tot-debt2   = (ledger.debt2 / tmp-saldo * 100)
            tot-debt3   = (ledger.debt3 / tmp-saldo * 100).

        IF tot-debt0 = ? THEN tot-debt0 = 0.
        IF tot-debt1 = ? THEN tot-debt1 = 0.
        IF tot-debt2 = ? THEN tot-debt2 = 0.
        IF tot-debt3 = ? THEN tot-debt3 = 0.
        
        outlist = outlist + STRING(tot-debt0, "           ->>9.99") 
                + STRING(tot-debt1, "           ->>9.99") 
                + STRING(tot-debt2, "           ->>9.99") 
                + STRING(tot-debt3, "           ->>9.99"). 
        
        RUN fill-in-list(NO, "", ?). 
        outlist = "". 
        RUN fill-in-list(NO, "", ?). 
    END. 

    outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
    RUN fill-in-list(NO, "----", ?). 
    IF NOT long-digit THEN 
        outlist = "       " 
                + STRING(translateExtended ("T O T A L  A/R:",lvCAREA,""), "x(30)") 
                + STRING(t-saldo, "->>,>>>,>>>,>>9.99") 
                + STRING(t-prev, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debit, "->>,>>>,>>>,>>9.99") 
                + STRING(t-credit, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt0, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt1, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt2, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt3, "->>,>>>,>>>,>>9.99"). 
    ELSE outlist = "       " 
                + STRING(translateExtended ("T O T A L  A/R:",lvCAREA,""), "x(30)") 
                + STRING(t-saldo, "->,>>>,>>>,>>>,>>9")     
                + STRING(t-prev, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debit, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-credit, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt0, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt1, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt2, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt3, "->,>>>,>>>,>>>,>>9"). 

    RUN fill-in-list(NO, "", ?). 
    outlist = "       " 
            + STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)") 
            + "            100.00". 

    DO i = 1 TO 54: 
        outlist = outlist + " ". 
    END. 

    ASSIGN
        tot-debt0   = (t-debt0 / t-saldo * 100)
        tot-debt1   = (t-debt1 / t-saldo * 100)
        tot-debt2   = (t-debt2 / t-saldo * 100)
        tot-debt3   = (t-debt3 / t-saldo * 100).

    IF tot-debt0 = ? THEN tot-debt0 = 0.
    IF tot-debt1 = ? THEN tot-debt1 = 0.
    IF tot-debt2 = ? THEN tot-debt2 = 0.
    IF tot-debt3 = ? THEN tot-debt3 = 0.

    outlist = outlist 
            + STRING(tot-debt0, "           ->>9.99") 
            + STRING(tot-debt1, "           ->>9.99") 
            + STRING(tot-debt2, "           ->>9.99") 
            + STRING(tot-debt3, "           ->>9.99"). 

    RUN fill-in-list(NO, "", ?). 
    outlist = "". 
    RUN fill-in-list(NO, "", ?). 
    /*M
    HIDE FRAME frame2 NO-PAUSE. 
    */
END. 


PROCEDURE age-list2a: 
    ASSIGN  curr-art    = 0
            counter     = 0
            t-saldo     = 0
            t-prev      = 0
            t-debit     = 0
            t-credit    = 0
            t-debt0     = 0
            t-debt1     = 0
            t-debt2     = 0
            t-debt3     = 0
            tmp-saldo   = 0 
            curr-name = ""
            curr-gastnr = 0
            gastname    = ""
            p-bal       = 0
            debit       = 0
            credit      = 0
            debt0       = 0
            debt1       = 0
            debt2       = 0
            debt3       = 0
            tot-debt    = 0 
            i           = 0
            curr-counter = 0
            curr-fcurr = "".

    from-date = fdate. 
    FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
        AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
        AND artikel.departement = 0 NO-LOCK 
        BY (STRING(artikel.artart) + STRING(artikel.artnr,"9999")): 

        /*M
        curr-bezeich = STRING(artikel.artnr, ">>>9") + " - " + artikel.bezeich. 
        DISP curr-bezeich WITH FRAME frame2. 
        */
        CREATE ledger. 
        ledger.artnr = artikel.artnr. 
        ledger.bezeich = STRING(artikel.artnr) + "  -  " + artikel.bezeich. 
    END. 

    /* NOT paid OR partial paid */ 
    curr-art = 0. 
    FOR EACH debitor WHERE debitor.rgdatum LE tdate 
        AND debitor.artnr GE from-art AND debitor.artnr LE to-art 
        AND debitor.opart LE 1 NO-LOCK USE-INDEX artdat_ix 
        BY debitor.artnr BY debitor.zahlkonto: 
        
        IF debitor.name GE from-name AND debitor.name LE to-name THEN 
        DO: 
            IF curr-art NE debitor.artnr THEN 
            DO: 
                curr-art = debitor.artnr. 
                FIND FIRST artikel WHERE artikel.artnr = curr-art 
                    AND artikel.departement = 0  NO-LOCK NO-ERROR. 
            END. 

            IF debitor.counter > 0 THEN 
                FIND FIRST age-list WHERE age-list.counter = debitor.counter NO-ERROR. 
            IF (debitor.counter = 0) OR (NOT AVAILABLE age-list) THEN 
            DO: 
                /* create aging record FOR a specific guest, based ON A/R-debit record */ 
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
                CREATE age-list. 
                age-list.artnr = debitor.artnr. 
                age-list.rechnr = debitor.rechnr. 
                age-list.rgdatum = debitor.rgdatum. 
                age-list.counter = debitor.counter. 
                age-list.gastnr = debitor.gastnr. 
                age-list.tot-debt = 0. 
                IF debitor.betrieb-gastmem = 0 THEN
                    age-list.fcurr = default-fcurr.
                ELSE
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN
                        age-list.fcurr = waehrung.wabkurz.
                END.

                IF artikel.artart = 2 THEN 
                    age-list.gastname = guest.name + ", " + guest.vorname1 + 
                                        guest.anredefirma + " " + guest.anrede1. 
                ELSE 
                DO: 
                    FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
                    IF debitor.gastnr = htparam.finteger THEN 
                        age-list.gastname = "F&B " + artikel.bezeich. 
                    ELSE age-list.gastname = "F/O " + artikel.bezeich. 
                END. 

                /*M
                guest-name = guest.name + ", " + guest.vorname1 
                             + guest.anredefirma + " " + guest.anrede1. 
                DISP guest-name WITH FRAME frame2. 
                */
            END. 

            IF disptype = 0 THEN
                age-list.tot-debt = age-list.tot-debt + debitor.saldo. 
            ELSE
                age-list.tot-debt = age-list.tot-debt + debitor.vesrdep. 

            /* previous balance  */ 
            IF debitor.rgdatum LT from-date AND debitor.zahlkonto = 0 THEN 
            DO:
                IF disptype = 0 THEN
                    age-list.p-bal = age-list.p-bal + debitor.saldo. 
                ELSE age-list.p-bal = age-list.p-bal + debitor.vesrdep. 
            END.

            /* debit transaction */ 
            IF debitor.rgdatum GE from-date AND debitor.zahlkonto = 0 THEN 
            DO: 
                IF disptype = 0 THEN
                    age-list.debit = age-list.debit + debitor.saldo. 
                ELSE age-list.debit = age-list.debit + debitor.vesrdep. 
            END.

            /* credit transaction */ 
            IF debitor.rgdatum LT from-date AND debitor.zahlkonto NE 0 THEN 
                age-list.p-bal = age-list.p-bal + debitor.saldo. 
            ELSE 
            DO: 
                IF debitor.rgdatum GE from-date AND debitor.zahlkonto NE 0 THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.credit = age-list.credit - debitor.saldo. 
                    ELSE age-list.credit = age-list.credit - debitor.vesrdep. 
                END.
            END. 
        END. 
    END. 

    /*  within period's full paid transaction */ 
    FOR EACH artikel WHERE (artikel.artart = 2 OR artikel.artart = 7) 
        AND artikel.artnr GE from-art AND artikel.artnr LE to-art 
        AND artikel.departement = 0 NO-LOCK BY artikel.artnr: 

        /*M
        curr-bezeich = STRING(artikel.artnr, ">>>9") + " - " + artikel.bezeich. 
        DISP curr-bezeich WITH FRAME frame2. 
        */

        curr-counter = 0. 
        FOR EACH debitor WHERE debitor.artnr = artikel.artnr 
            AND debitor.rgdatum LE to-date 
            AND debitor.opart EQ 2 AND debitor.zahlkonto EQ 0 
            USE-INDEX artdat_ix NO-LOCK: 
            IF debitor.name GE from-name AND debitor.name LE to-name THEN 
            DO: 
                /* create aging record FOR a specific guest */ 
                FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
                CREATE age-list. 
                age-list.artnr = debitor.artnr. 
                age-list.rechnr = debitor.rechnr. 
                age-list.rgdatum = debitor.rgdatum. 
                age-list.counter = debitor.counter. 
                age-list.gastnr = debitor.gastnr. 
                age-list.tot-debt = debitor.saldo. 
                IF debitor.betrieb-gastmem = 0 THEN
                    age-list.fcurr = default-fcurr.
                ELSE
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN
                        age-list.fcurr = waehrung.wabkurz.
                END.

                IF artikel.artart = 2 THEN 
                    age-list.gastname = guest.name + ", " + guest.vorname1 + 
                                        guest.anredefirma + " " + guest.anrede1. 
                ELSE 
                DO: 
                    FIND FIRST htparam WHERE paramnr = 867 NO-LOCK. 
                    IF debitor.gastnr = htparam.finteger THEN 
                        age-list.gastname = "F&B " + artikel.bezeich. 
                    ELSE age-list.gastname = "F/O " + artikel.bezeich. 
                END. 

                /*M
                guest-name = guest.name + ", " + guest.vorname1 
                            + guest.anredefirma + " " + guest.anrede1. 
                DISP guest-name WITH FRAME frame2. 
                */

                IF debitor.rgdatum LT from-date THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.p-bal = age-list.p-bal + debitor.saldo. 
                    ELSE
                        age-list.p-bal = age-list.p-bal + debitor.vesrdep.
                END.
                ELSE IF debitor.rgdatum GE from-date THEN 
                DO:
                    IF disptype = 0 THEN
                        age-list.debit = age-list.debit + debitor.saldo. 
                    ELSE 
                        age-list.debit = age-list.debit + debitor.vesrdep. 
                END.

                FOR EACH debtrec WHERE debtrec.counter = debitor.counter 
                    AND debtrec.rechnr = debitor.rechnr AND debtrec.zahlkonto GT 0 
                    AND debtrec.rgdatum LE to-date NO-LOCK USE-INDEX counter_ix: 
                    age-list.tot-debt = age-list.tot-debt + debtrec.saldo. 
                    IF debtrec.rgdatum LT from-date THEN 
                    DO:
                        IF disptype = 0 THEN
                            age-list.p-bal = age-list.p-bal + debtrec.saldo. 
                        ELSE 
                            age-list.p-bal = age-list.p-bal + debtrec.vesrdep. 
                    END.
                    ELSE IF debtrec.rgdatum GE from-date THEN 
                    DO:
                        IF disptype = 0 THEN
                            age-list.credit = age-list.credit - debtrec.saldo. 
                        ELSE
                            age-list.credit = age-list.credit - debtrec.vesrdep. 
                    END.
                END. 
            END. 
        END. 
    END. 
     
    FOR EACH age-list:
        IF age-list.p-bal GE - 0.01 AND age-list.p-bal LE 0.01
            AND age-list.debit = 0 AND age-list.credit = 0 THEN
            DELETE age-list.
    END.

    FOR EACH ledger BY ledger.artnr: 
        outlist = "    " + caps(ledger.bezeich). 
        RUN fill-in-list(NO, "", ?). 
        outlist = "". 
        RUN fill-in-list(NO, "", ?). 
        counter = 0. 
        curr-gastnr = 0. 
        IF mi-bill THEN
            FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
                BY age-list.rgdatum BY age-list.gastname :
                RUN create-output.
            END.
        ELSE
            FOR EACH age-list WHERE age-list.artnr = ledger.artnr 
                BY age-list.gastname BY age-list.rechnr: 
                RUN create-output.
            END. 

        IF counter GT 0 AND (p-bal NE 0 OR debit NE 0 OR credit NE 0) THEN 
        DO: 
            IF NOT long-digit THEN 
                outlist = "  " + STRING(counter,">>>9 ") 
                        + STRING(gastname, "x(30)") 
                        + STRING(tot-debt, "->>,>>>,>>>,>>9.99") 
                        + STRING(p-bal, "->>,>>>,>>>,>>9.99") 
                        + STRING(debit, "->>,>>>,>>>,>>9.99") 
                        + STRING(credit, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt0, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt1, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt2, "->>,>>>,>>>,>>9.99") 
                        + STRING(debt3, "->>,>>>,>>>,>>9.99"). 
            ELSE outlist = "  " + STRING(counter,">>>9 ") 
                        + STRING(gastname, "x(30)") 
                        + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") 
                        + STRING(p-bal, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debit, "->,>>>,>>>,>>>,>>9") 
                        + STRING(credit, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debt0, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debt1, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debt2, "->,>>>,>>>,>>>,>>9") 
                        + STRING(debt3, "->,>>>,>>>,>>>,>>9"). 
            RUN fill-in-list(YES, curr-fcurr, curr-rgdatum). 
        END. 
        ELSE counter = counter - 1. 

        tmp-saldo = ledger.tot-debt. 
        IF tmp-saldo = 0 THEN tmp-saldo = 1. 
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
        RUN fill-in-list(NO, "----", ?). 
        IF NOT long-digit THEN 
            outlist = "       " 
                    + STRING(translateExtended ("T o t a l",lvCAREA,""), "x(30)") 
                    + STRING(ledger.tot-debt, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.p-bal, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debit, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.credit, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt0, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt1, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt2, "->>,>>>,>>>,>>9.99") 
                    + STRING(ledger.debt3, "->>,>>>,>>>,>>9.99"). 
        ELSE outlist = "       " 
            + STRING(translateExtended ("T o t a l",lvCAREA,""), "x(30)") 
            + STRING(ledger.tot-debt, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.p-bal, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debit, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.credit, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debt0, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debt1, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debt2, "->,>>>,>>>,>>>,>>9") 
            + STRING(ledger.debt3, "->,>>>,>>>,>>>,>>9"). 

        RUN fill-in-list(NO, "", ?). 
        outlist = "       " 
                + STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)") 
                + "            100.00". 

        DO i = 1 TO 54: 
            outlist = outlist + " ". 
        END. 

        ASSIGN
            tot-debt0   = (ledger.debt0 / tmp-saldo * 100)
            tot-debt1   = (ledger.debt1 / tmp-saldo * 100)
            tot-debt2   = (ledger.debt2 / tmp-saldo * 100)
            tot-debt3   = (ledger.debt3 / tmp-saldo * 100).

        IF tot-debt0 = ? THEN tot-debt0 = 0.
        IF tot-debt1 = ? THEN tot-debt1 = 0.
        IF tot-debt2 = ? THEN tot-debt2 = 0.
        IF tot-debt3 = ? THEN tot-debt3 = 0.

        outlist = outlist 
                + STRING(tot-debt0, "           ->>9.99") 
                + STRING(tot-debt1, "           ->>9.99") 
                + STRING(tot-debt2, "           ->>9.99") 
                + STRING(tot-debt3, "           ->>9.99"). 
        RUN fill-in-list(NO, "", ?). 
        outlist = "". 
        RUN fill-in-list(NO, "", ?). 
    END. 

    outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------". 
    RUN fill-in-list(NO, "----", ?). 
    IF NOT long-digit THEN 
        outlist = "       " 
                + STRING(translateExtended ("T O T A L  A/R:",lvCAREA,""), "x(30)")
                + STRING(t-saldo, "->>,>>>,>>>,>>9.99") 
                + STRING(t-prev, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debit, "->>,>>>,>>>,>>9.99") 
                + STRING(t-credit, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt0, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt1, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt2, "->>,>>>,>>>,>>9.99") 
                + STRING(t-debt3, "->>,>>>,>>>,>>9.99"). 
    ELSE outlist = "       " 
                + STRING(translateExtended ("T O T A L  A/R:",lvCAREA,""), "x(30)")
                + STRING(t-saldo, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-prev, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debit, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-credit, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt0, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt1, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt2, "->,>>>,>>>,>>>,>>9") 
                + STRING(t-debt3, "->,>>>,>>>,>>>,>>9"). 

    RUN fill-in-list(NO, "", ?). 
    outlist = "       " 
            + STRING(translateExtended ("Statistic Percentage (%) :",lvCAREA,""), "x(30)") 
            + "            100.00". 
    
    DO i = 1 TO 54: 
        outlist = outlist + " ". 
    END. 

     ASSIGN
        tot-debt0   = (t-debt0 / t-saldo * 100)
        tot-debt1   = (t-debt1 / t-saldo * 100)
        tot-debt2   = (t-debt2 / t-saldo * 100)
        tot-debt3   = (t-debt3 / t-saldo * 100).

    IF tot-debt0 = ? THEN tot-debt0 = 0.
    IF tot-debt1 = ? THEN tot-debt1 = 0.
    IF tot-debt2 = ? THEN tot-debt2 = 0.
    IF tot-debt3 = ? THEN tot-debt3 = 0.

    outlist = outlist 
            + STRING(tot-debt0, "           ->>9.99") 
            + STRING(tot-debt1, "           ->>9.99") 
            + STRING(tot-debt2, "           ->>9.99") 
            + STRING(tot-debt3, "           ->>9.99"). 

    RUN fill-in-list(NO, "", ?). 
    outlist = "". 
    RUN fill-in-list(NO, "", ?). 
    /*M
    hide FRAME frame2 NO-PAUSE. 
    */
END. 




PROCEDURE create-output:
    IF to-date - age-list.rgdatum GT day3 THEN 
        age-list.debt3 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day2 THEN 
        age-list.debt2 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day1 THEN 
        age-list.debt1 = age-list.tot-debt. 
    ELSE age-list.debt0 = age-list.tot-debt. 

    ledger.tot-debt = ledger.tot-debt + age-list.tot-debt. 
    ledger.p-bal = ledger.p-bal + age-list.p-bal. 
    ledger.debit = ledger.debit + age-list.debit. 
    ledger.credit = ledger.credit + age-list.credit. 
    ledger.debt0 = ledger.debt0 + age-list.debt0. 
    ledger.debt1 = ledger.debt1 + age-list.debt1. 
    ledger.debt2 = ledger.debt2 + age-list.debt2. 
    ledger.debt3 = ledger.debt3 + age-list.debt3. 
    t-saldo  = t-saldo  + age-list.tot-debt. 
    t-prev   = t-prev   + age-list.p-bal. 
    t-debit  = t-debit  + age-list.debit. 
    t-credit = t-credit + age-list.credit. 
    t-debt0  = t-debt0 + age-list.debt0. 
    t-debt1  = t-debt1 + age-list.debt1. 
    t-debt2  = t-debt2 + age-list.debt2. 
    t-debt3  = t-debt3 + age-list.debt3. 

    IF curr-gastnr = 0 THEN 
    DO: 
        curr-rgdatum = age-list.rgdatum. 
        bill-number = age-list.rechnr.
        inp-gastnr  = age-list.gastnr.
        inp-artnr   = age-list.artnr.
        gastname = age-list.gastname. 
        tot-debt = age-list.tot-debt. 
        p-bal = age-list.p-bal. 
        debit = age-list.debit. 
        credit = age-list.credit. 
        debt0 = age-list.debt0. 
        debt1 = age-list.debt1. 
        debt2 = age-list.debt2. 
        debt3 = age-list.debt3. 
        counter = counter + 1. 
    END. 
    ELSE IF curr-name NE age-list.gastname THEN 
    /*ELSE IF curr-gastnr NE age-list.gastnr THEN */
    DO: 
        IF p-bal NE 0 OR debit NE 0 OR credit NE 0 THEN 
        DO: 
            IF NOT long-digit THEN 
                outlist = "  " + STRING(counter,">>>9 ") 
                            + STRING(gastname, "x(30)") 
                            + STRING(tot-debt, "->>,>>>,>>>,>>9.99") 
                            + STRING(p-bal, "->>,>>>,>>>,>>9.99") 
                            + STRING(debit, "->>,>>>,>>>,>>9.99") 
                            + STRING(credit, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt0, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt1, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt2, "->>,>>>,>>>,>>9.99") 
                            + STRING(debt3, "->>,>>>,>>>,>>9.99"). 
            ELSE outlist = "  " + STRING(counter,">>>9 ") 
                            + STRING(gastname, "x(30)") 
                            + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") 
                            + STRING(p-bal, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debit, "->,>>>,>>>,>>>,>>9") 
                            + STRING(credit, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt0, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt1, "->,>>>,>>>,>>>,>>9")   
                            + STRING(debt2, "->,>>>,>>>,>>>,>>9") 
                            + STRING(debt3, "->,>>>,>>>,>>>,>>9"). 
            RUN fill-in-list(YES, age-list.fcurr, curr-rgdatum). 
        END. 
        ELSE counter = counter - 1. 

        curr-rgdatum = age-list.rgdatum.
        bill-number = age-list.rechnr. 
        inp-gastnr  = age-list.gastnr.
        inp-artnr   = age-list.artnr.
        gastname = age-list.gastname. 
        tot-debt = age-list.tot-debt. 
        p-bal = age-list.p-bal. 
        debit = age-list.debit. 
        credit = age-list.credit. 
        debt0 = age-list.debt0. 
        debt1 = age-list.debt1. 
        debt2 = age-list.debt2. 
        debt3 = age-list.debt3. 
        counter = counter + 1. 
    END. 
    ELSE 
    DO: 
        tot-debt = tot-debt + age-list.tot-debt. 
        p-bal = p-bal + age-list.p-bal. 
        debit = debit + age-list.debit. 
        credit = credit + age-list.credit. 
        debt0 = debt0 + age-list.debt0. 
        debt1 = debt1 + age-list.debt1. 
        debt2 = debt2 + age-list.debt2. 
        debt3 = debt3 + age-list.debt3. 
    END. 

    curr-gastnr = age-list.gastnr. 
    curr-fcurr  = age-list.fcurr.
    IF NOT detailed THEN curr-name = age-list.gastname. 
    DELETE age-list. 
END.

PROCEDURE fill-in-list: 
    DEFINE INPUT PARAMETER fill-billno  AS LOGICAL. 
    DEFINE INPUT PARAMETER currency     AS CHARACTER NO-UNDO.
    DEFINE INPUT PARAMETER curr-rgdatum AS DATE.

    CREATE arage-list. 
    IF fill-billno /* AND AVAILABLE age-list */ THEN
    DO:
        arage-list.rechnr = STRING(bill-number,">>>>>>>>>"). 
        arage-list.gastnr = inp-gastnr.
        arage-list.artnr  = inp-artnr.
        
        IF curr-rgdatum NE ? THEN
            arage-list.strdate = STRING(curr-rgdatum, "99/99/99").
    END.

    arage-list.str = outlist. 
    IF SUBSTR(outlist,1,5) = "-----" THEN 
        ASSIGN  arage-list.rechnr = "---------"
                arage-list.strdate = "--------". 
                arage-list.age1 = SUBSTRING(STR,110, 18). 
                arage-list.age2 = SUBSTRING(STR,128, 18). 
                arage-list.age3 = SUBSTRING(STR,146, 18). 
                arage-list.age4 = SUBSTRING(STR,164, 18). 
                arage-list.curr = currency.
END. 
