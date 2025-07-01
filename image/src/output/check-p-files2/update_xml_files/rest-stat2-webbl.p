
DEFINE TEMP-TABLE detail-list
    FIELD flag          AS CHARACTER
    FIELD segm-no       AS INTEGER
    FIELD guest-name    AS CHARACTER
    FIELD descipt       AS CHARACTER
    FIELD bill-no       AS CHARACTER
    FIELD dept          AS INTEGER
    FIELD pax           AS CHARACTER
    FIELD proz-pax      AS CHARACTER
    FIELD t-rev         AS CHARACTER
    FIELD proz-trev     AS CHARACTER
    FIELD m-pax         AS CHARACTER
    FIELD proz-mpax     AS CHARACTER
    FIELD m-rev         AS CHARACTER
    FIELD proz-mrev     AS CHARACTER
    FIELD y-pax         AS CHARACTER
    FIELD proz-ypax     AS CHARACTER
    FIELD y-rev         AS CHARACTER
    FIELD proz-yrev     AS CHARACTER
.

DEFINE TEMP-TABLE t-list
    FIELD flag          AS CHARACTER
    FIELD segm-no       AS INTEGER
    FIELD guest-name    AS CHARACTER
    FIELD bill-no       AS INTEGER
    FIELD dept          AS INTEGER
    FIELD pax           AS INTEGER
    FIELD proz-pax      AS DECIMAL
    FIELD t-rev         AS DECIMAL
    FIELD proz-trev     AS DECIMAL
    FIELD m-pax         AS INTEGER
    FIELD proz-mpax     AS DECIMAL
    FIELD m-rev         AS DECIMAL
    FIELD proz-mrev     AS DECIMAL
    FIELD y-pax         AS INTEGER
    FIELD proz-ypax     AS DECIMAL
    FIELD y-rev         AS DECIMAL
    FIELD proz-yrev     AS DECIMAL
.

DEFINE TEMP-TABLE input-list
    FIELD sorttype     AS INTEGER
    FIELD segmcode     AS INTEGER
    FIELD start-jan    AS DATE
    FIELD from-date    AS DATE
    FIELD to-date      AS DATE
    FIELD excl-tax     AS LOGICAL   /* Dzikri D7F303 - new filter */
.

/* 
DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE INPUT PARAMETER segmcode     AS INTEGER.
DEFINE INPUT PARAMETER start-jan    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER excl-tax     AS LOGICAL.
*/
DEFINE INPUT  PARAMETER TABLE FOR input-list. /* Dzikri D7F303 - new filter */
DEFINE OUTPUT PARAMETER TABLE FOR detail-list.

FIND FIRST input-list NO-LOCK.
IF NOT AVAILABLE input-list THEN RETURN.

DEFINE VARIABLE price-decimal AS INTEGER.
DEFINE VARIABLE black-list AS INTEGER.
DEFINE VARIABLE long-digit AS LOGICAL.
DEFINE VARIABLE f-endkum AS INTEGER. 
DEFINE VARIABLE m-endkum AS INTEGER.
DEFINE VARIABLE b-endkum AS INTEGER.

DEFINE VARIABLE tot-pax AS INTEGER.
DEFINE VARIABLE tot-rev AS DECIMAL.
DEFINE VARIABLE tot-mpax AS INTEGER.
DEFINE VARIABLE tot-mrev AS DECIMAL.
DEFINE VARIABLE tot-ypax AS INTEGER.
DEFINE VARIABLE tot-yrev AS DECIMAL.
DEFINE VARIABLE detail-pax AS INTEGER.
DEFINE VARIABLE detail-rev AS DECIMAL.
DEFINE VARIABLE curr-segm AS INTEGER. 
DEFINE VARIABLE gname AS CHARACTER.
DEFINE VARIABLE curr-billno AS CHARACTER.
DEFINE VARIABLE curr-dept AS INTEGER.
DEFINE VARIABLE command-str AS CHARACTER.
DEFINE VARIABLE curr-zeit AS INTEGER.
DEFINE VARIABLE guest-no AS INTEGER.
DEFINE VARIABLE segm-no AS INTEGER.

FIND FIRST htparam WHERE htparam.paramnr EQ 491 NO-LOCK.
price-decimal = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr EQ 709 NO-LOCK. 
black-list = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 862 NO-LOCK. 
f-endkum = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr = 273 NO-LOCK. 
m-endkum = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 892 NO-LOCK. 
b-endkum = htparam.finteger.
/*
IF sorttype EQ 1 THEN RUN create-detail-food.
ELSE IF sorttype EQ 2 THEN RUN create-list-bev.
ELSE IF sorttype EQ 3 THEN RUN create-list-other.
ELSE IF sorttype EQ 4 THEN RUN create-list-all.
*/

/* Dzikri D7F303 - new filter */
DEFINE VARIABLE vat     AS DECIMAL. 
DEFINE VARIABLE vat2    AS DECIMAL NO-UNDO.
DEFINE VARIABLE service AS DECIMAL. 
DEFINE VARIABLE fact    AS DECIMAL NO-UNDO.

FUNCTION calculate-betrag RETURNS DECIMAL(inp-deci AS DECIMAL): 
    IF input-list.excl-tax EQ YES AND inp-deci NE 0 THEN 
    DO:
        service = 0. 
        vat     = 0. 
        vat2    = 0.
        RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                                h-journal.bill-datum, OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).

        inp-deci = inp-deci / (1 + vat + vat2 + service). 
    END.
    RETURN inp-deci.
END FUNCTION.
/* Dzikri D7F303 - END */

IF input-list.segmcode NE 9999 THEN RUN create-detail.
ELSE RUN create-detail-unknown.

/*****************************************************************************************************/
PROCEDURE create-detail:
DEFINE VARIABLE qh AS HANDLE.

    tot-pax     = 0.
    tot-rev     = 0.
    tot-mpax    = 0.
    tot-mrev    = 0.
    tot-ypax    = 0.
    tot-yrev    = 0.

    FOR EACH t-list:
        DELETE t-list.
    END.

    FOR EACH detail-list:
        DELETE detail-list.
    END.    

    curr-zeit = TIME.

    /*FIND FIRST h-journal WHERE h-journal.bill-datum GE input-list.start-jan 
        AND h-journal.bill-datum LE input-list.to-date NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE h-journal:*/
    FOR EACH h-journal WHERE h-journal.bill-datum GE input-list.start-jan 
        AND h-journal.bill-datum LE input-list.to-date NO-LOCK BY h-journal.rechnr:
        
        IF input-list.segmcode NE 9999 THEN
        DO:
            FIND FIRST h-bill WHERE h-bill.rechnr EQ h-journal.rechnr            
                AND h-bill.departement EQ h-journal.departement
                /* AND h-bill.bilname NE "" */ NO-LOCK NO-ERROR.
        END.
        /*ELSE
       
        DO:
            FIND FIRST h-bill WHERE h-bill.rechnr EQ h-journal.rechnr            
                AND h-bill.departement EQ h-journal.departement
                AND h-bill.bilname NE "" NO-LOCK NO-ERROR.
        END.*/
                
        IF AVAILABLE h-bill THEN
        DO:                        
            FIND FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr 
                AND h-artikel.departement EQ h-journal.departement
                AND h-artikel.artart EQ 0 NO-LOCK NO-ERROR.
            IF AVAILABLE h-artikel THEN
            DO:
                IF input-list.sorttype EQ 1 THEN /*Food*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) NO-LOCK NO-ERROR.
                END.
                ELSE IF input-list.sorttype EQ 2 THEN /*Beverage*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND artikel.umsatzart EQ 6 NO-LOCK NO-ERROR.
                END.
                ELSE IF input-list.sorttype EQ 3 THEN /*Other*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND artikel.umsatzart EQ 4 NO-LOCK NO-ERROR.
                END.
                ELSE IF input-list.sorttype EQ 4 THEN /*All*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND artikel.umsatzart GE 3 AND artikel.umsatzart LE 6 NO-LOCK NO-ERROR.
                END.
                
                IF AVAILABLE artikel THEN
                DO:
                    segm-no  = 0.
                    guest-no = 0.

                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN /*Inhouse*/
                    DO:
                        FIND FIRST res-line WHERE res-line.resnr EQ h-bill.resnr
                            AND res-line.reslinnr EQ h-bill.reslinnr NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN guest-no = res-line.gastnrmember.
                    END.
                    ELSE IF h-bill.resnr GT 0 THEN  /*only consume*/
                    DO:
                        guest-no = h-bill.resnr.
                    END.

                    /* Dzikri 886ACD - Repair wrong validation for segment */
                    IF h-bill.segmentcode EQ 0 THEN
                    DO:
                        FIND FIRST guestseg WHERE guestseg.gastnr EQ guest-no AND guestseg.reihenfolge EQ 1 NO-LOCK NO-ERROR.
                        IF AVAILABLE guestseg THEN segm-no = guestseg.segmentcode.
                    END.
                    ELSE segm-no = h-bill.segmentcode.

                    /* Dzikri 886ACD - Repair wrong validation for segment */
                    IF input-list.segmcode EQ segm-no THEN
                    DO:
                        FIND FIRST t-list WHERE t-list.bill-no EQ h-bill.rechnr 
                            AND t-list.dept EQ h-bill.departement NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE t-list THEN
                        DO:
                            CREATE t-list.
                            ASSIGN
                                t-list.bill-no  = h-bill.rechnr
                                t-list.dept     = h-bill.departement
                                t-list.segm-no  = input-list.segmcode
                            .
                            
                            /* Dzikri 886ACD - Repair wrong validation for segment */
                            FIND FIRST guest WHERE guest.gastnr EQ guest-no AND guest-no NE 0 NO-LOCK NO-ERROR.
                            IF AVAILABLE guest THEN
                            DO:                        
                                t-list.guest-name = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1. 
                            END.
                            ELSE
                            DO:
                                t-list.guest-name = h-bill.bilname.
                            END.
                        END.
    
                        IF h-journal.bill-datum EQ input-list.to-date THEN
                        DO:
                            IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN 
                            ASSIGN
                                t-list.pax = h-bill.belegung        
                                tot-pax = tot-pax + h-bill.belegung
                            .
    
                            ASSIGN                                                                
                                t-list.t-rev = t-list.t-rev + calculate-betrag(h-journal.betrag)            
                                tot-rev = tot-rev + calculate-betrag(h-journal.betrag)                                               
                            .                                            
                        END.
                        
                        /* Dzikri 83B230 - same logic as department turnover 
                        IF MONTH(h-journal.bill-datum) EQ MONTH(input-list.to-date) THEN */
                        IF h-journal.bill-datum GE input-list.from-date AND h-journal.bill-datum LE input-list.to-date THEN
                        DO:            
                            IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN 
                            ASSIGN
                                t-list.m-pax = h-bill.belegung        
                                tot-mpax = tot-mpax + h-bill.belegung
                            .
    
                            ASSIGN                               
                                t-list.m-rev = t-list.m-rev + calculate-betrag(h-journal.betrag)           
                                tot-mrev = tot-mrev + calculate-betrag(h-journal.betrag)
                            .                                                                          
                        END.      
                        
                        IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN 
                        ASSIGN
                            t-list.y-pax = h-bill.belegung      
                            tot-ypax = tot-ypax + h-bill.belegung
                        .
    
                        ASSIGN                          
                            t-list.y-rev = t-list.y-rev + calculate-betrag(h-journal.betrag)     
                            tot-yrev = tot-yrev + calculate-betrag(h-journal.betrag) 
                        .
                                                        
                        curr-billno = STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement).
                    END.              
                END.
            END.                        
        END.

        /*FIND NEXT h-journal WHERE h-journal.bill-datum GE input-list.start-jan 
            AND h-journal.bill-datum LE input-list.to-date NO-LOCK NO-ERROR.*/
    END.

    FOR EACH t-list WHERE t-list.pax EQ 0 AND t-list.t-rev EQ 0 
        AND t-list.m-pax EQ 0 AND t-list.m-rev EQ 0 
        AND t-list.y-pax EQ 0 AND t-list.y-rev EQ 0 NO-LOCK:

        DELETE t-list.
    END.

    FOR EACH t-list NO-LOCK BY t-list.bill-no:
        IF t-list.pax NE 0 THEN t-list.proz-pax = t-list.pax / tot-pax * 100.
        IF t-list.t-rev NE 0 THEN t-list.proz-trev = t-list.t-rev / tot-rev * 100.
        IF t-list.m-pax NE 0 THEN t-list.proz-mpax = t-list.m-pax / tot-mpax * 100.
        IF t-list.m-rev NE 0 THEN t-list.proz-mrev = t-list.m-rev / tot-mrev * 100.
        IF t-list.y-pax NE 0 THEN t-list.proz-ypax = t-list.y-pax / tot-ypax * 100.
        IF t-list.y-rev NE 0 THEN t-list.proz-yrev = t-list.y-rev / tot-yrev * 100.

        CREATE detail-list.
        ASSIGN
            detail-list.descipt = STRING(t-list.bill-no) + " - " + STRING(t-list.dept, "99")
            detail-list.guest-name = t-list.guest-name
            detail-list.segm-no = t-list.segm-no
        .

        IF long-digit THEN
        DO:
            ASSIGN
                detail-list.pax         = STRING(t-list.pax, "->>>>>>9")
                detail-list.t-rev       = STRING(t-list.t-rev, "->>>,>>>,>>>,>>>,>>9")
                detail-list.m-pax       = STRING(t-list.m-pax, "->>>>>>9")
                detail-list.m-rev       = STRING(t-list.m-rev, "->>>,>>>,>>>,>>>,>>9")
                detail-list.y-pax       = STRING(t-list.y-pax, "->>>>>>9")
                detail-list.y-rev       = STRING(t-list.y-rev, "->>>,>>>,>>>,>>>,>>9")
                detail-list.proz-pax    = STRING(t-list.proz-pax, "->>9.99")
                detail-list.proz-trev   = STRING(t-list.proz-trev, "->>9.99")
                detail-list.proz-mpax   = STRING(t-list.proz-mpax, "->>9.99")
                detail-list.proz-mrev   = STRING(t-list.proz-mrev, "->>9.99")
                detail-list.proz-ypax   = STRING(t-list.proz-ypax, "->>9.99")
                detail-list.proz-yrev   = STRING(t-list.proz-yrev, "->>9.99")
            .
        END.
        ELSE
        DO:
            ASSIGN
                detail-list.pax         = STRING(t-list.pax, "  ->>>>9")
                detail-list.t-rev       = STRING(t-list.t-rev, "->,>>>,>>>,>>>,>>9.99")
                detail-list.m-pax       = STRING(t-list.m-pax, " ->>>>>9")
                detail-list.m-rev       = STRING(t-list.m-rev, "->,>>>,>>>,>>>,>>9.99")
                detail-list.y-pax       = STRING(t-list.y-pax, " ->>>>>9")
                detail-list.y-rev       = STRING(t-list.y-rev, "->,>>>,>>>,>>>,>>9.99")
                detail-list.proz-pax    = STRING(t-list.proz-pax, "->>9.99")
                detail-list.proz-trev   = STRING(t-list.proz-trev, "->>9.99")
                detail-list.proz-mpax   = STRING(t-list.proz-mpax, "->>9.99")
                detail-list.proz-mrev   = STRING(t-list.proz-mrev, "->>9.99")
                detail-list.proz-ypax   = STRING(t-list.proz-ypax, "->>9.99")
                detail-list.proz-yrev   = STRING(t-list.proz-yrev, "->>9.99")
            .
        END.
    END.

    FIND FIRST detail-list NO-LOCK NO-ERROR.
    IF AVAILABLE detail-list THEN
    DO:
        CREATE detail-list.
        ASSIGN
            detail-list.flag        = "*"
            detail-list.descipt     = "T O T A L"
            detail-list.pax         = STRING(tot-pax, "->>>>>>9")
            detail-list.t-rev       = STRING(tot-rev, "->,>>>,>>>,>>>,>>9.99")
            detail-list.m-pax       = STRING(tot-mpax, "->>>>>>9")
            detail-list.m-rev       = STRING(tot-mrev, "->,>>>,>>>,>>>,>>9.99")
            detail-list.y-pax       = STRING(tot-ypax, "->>>>>>9")
            detail-list.y-rev       = STRING(tot-yrev, "->,>>>,>>>,>>>,>>9.99")
            detail-list.proz-pax    = STRING(100, ">>9.99")
            detail-list.proz-trev   = STRING(100, ">>9.99")
            detail-list.proz-mpax   = STRING(100, ">>9.99")
            detail-list.proz-mrev   = STRING(100, ">>9.99")
            detail-list.proz-ypax   = STRING(100, ">>9.99")
            detail-list.proz-yrev   = STRING(100, ">>9.99")
        .
    END.   
END PROCEDURE.

PROCEDURE create-detail-unknown:
DEFINE VARIABLE qh AS HANDLE.

    tot-pax     = 0.
    tot-rev     = 0.
    tot-mpax    = 0.
    tot-mrev    = 0.
    tot-ypax    = 0.
    tot-yrev    = 0.

    FOR EACH t-list:
        DELETE t-list.
    END.

    FOR EACH detail-list:
        DELETE detail-list.
    END.    

    curr-zeit = TIME.

    /*FIND FIRST h-journal WHERE h-journal.bill-datum GE input-list.start-jan 
        AND h-journal.bill-datum LE input-list.to-date NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE h-journal:*/
    FOR EACH h-journal WHERE h-journal.bill-datum GE input-list.start-jan 
        AND h-journal.bill-datum LE input-list.to-date NO-LOCK BY h-journal.departement BY h-journal.rechnr:

        FIND FIRST h-bill WHERE h-bill.rechnr EQ h-journal.rechnr            
            AND h-bill.departement EQ h-journal.departement 
            AND h-bill.segment EQ 0
            /* AND h-bill.bilname NE "" */ NO-LOCK NO-ERROR.   

        IF AVAILABLE h-bill THEN
        DO:                        
            FIND FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr 
                AND h-artikel.departement EQ h-journal.departement
                AND h-artikel.artart EQ 0 NO-LOCK NO-ERROR.
            IF AVAILABLE h-artikel THEN
            DO:
                IF input-list.sorttype EQ 1 THEN /*Food*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) NO-LOCK NO-ERROR.
                END.
                ELSE IF input-list.sorttype EQ 2 THEN /*Beverage*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND artikel.umsatzart EQ 6 NO-LOCK NO-ERROR.
                END.
                ELSE IF input-list.sorttype EQ 3 THEN /*Other*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND artikel.umsatzart EQ 4 NO-LOCK NO-ERROR.
                END.
                ELSE IF input-list.sorttype EQ 4 THEN /*All*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND artikel.umsatzart GE 3 AND artikel.umsatzart LE 6 NO-LOCK NO-ERROR.
                END.
                
                IF AVAILABLE artikel THEN
                DO:
                    segm-no  = 0.
                    guest-no = 0.

                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN /*Inhouse*/
                    DO:
                        FIND FIRST res-line WHERE res-line.resnr EQ h-bill.resnr
                            AND res-line.reslinnr EQ h-bill.reslinnr NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN guest-no = res-line.gastnrmember.
                    END.
                    ELSE IF h-bill.resnr GT 0 THEN  /*only consume*/
                    DO:
                        guest-no = h-bill.resnr.
                    END.

                    /* Dzikri 886ACD - Repair wrong validation for segment */
                    IF h-bill.segmentcode EQ 0 THEN
                    DO:
                        FIND FIRST guestseg WHERE guestseg.gastnr EQ guest-no AND guestseg.reihenfolge EQ 1 NO-LOCK NO-ERROR.
                        IF AVAILABLE guestseg THEN segm-no = guestseg.segmentcode.
                    END.
                    ELSE segm-no = h-bill.segmentcode.
                    
                    IF segm-no EQ 0 THEN
                    DO:
                        FIND FIRST t-list WHERE t-list.bill-no EQ h-bill.rechnr 
                            AND t-list.dept EQ h-bill.departement NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE t-list THEN
                        DO:
                            CREATE t-list.
                            ASSIGN
                                t-list.bill-no  = h-bill.rechnr
                                t-list.dept     = h-bill.departement
                                t-list.guest-name = h-bill.bilname   
                                t-list.segm-no  = 9999
                            .
                        END.

                        IF h-journal.bill-datum EQ input-list.to-date THEN
                        DO:
                            IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN 
                            DO:
                                t-list.pax = h-bill.belegung.    
                                tot-pax = tot-pax + h-bill.belegung.
                            END.

                            ASSIGN                                                               
                                t-list.t-rev = t-list.t-rev + calculate-betrag(h-journal.betrag)            
                                tot-rev = tot-rev + calculate-betrag(h-journal.betrag)                                               
                            .                                            
                        END.

                        /* Dzikri 83B230 - same logic as department turnover 
                        IF MONTH(h-journal.bill-datum) EQ MONTH(input-list.to-date) THEN */
                        IF h-journal.bill-datum GE input-list.from-date AND h-journal.bill-datum LE input-list.to-date THEN
                        DO:            
                            IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN 
                            DO:
                                t-list.m-pax = h-bill.belegung.
                                tot-mpax = tot-mpax + h-bill.belegung.
                            END.

                            ASSIGN                                      
                                t-list.m-rev = t-list.m-rev + calculate-betrag(h-journal.betrag)           
                                tot-mrev = tot-mrev + calculate-betrag(h-journal.betrag)
                            .                                                                          
                        END.      
                        
                        IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN 
                        ASSIGN
                            t-list.y-pax = h-bill.belegung   
                            tot-ypax = tot-ypax + h-bill.belegung
                        .

                        ASSIGN                             
                            t-list.y-rev = t-list.y-rev + calculate-betrag(h-journal.betrag)     
                            tot-yrev = tot-yrev + calculate-betrag(h-journal.betrag) 
                        .
                                                        
                        curr-billno = STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement).                                      
                    END.
                END.
            END.                        
        END.

        /*FIND NEXT h-journal WHERE h-journal.bill-datum GE input-list.start-jan 
            AND h-journal.bill-datum LE input-list.to-date NO-LOCK NO-ERROR.*/
    END.

    FOR EACH t-list WHERE t-list.pax EQ 0 AND t-list.t-rev EQ 0 
        AND t-list.m-pax EQ 0 AND t-list.m-rev EQ 0 
        AND t-list.y-pax EQ 0 AND t-list.y-rev EQ 0 NO-LOCK:

        DELETE t-list.
    END.

    FOR EACH t-list NO-LOCK BY t-list.bill-no:
        IF t-list.pax NE 0 THEN t-list.proz-pax = t-list.pax / tot-pax * 100.
        IF t-list.t-rev NE 0 THEN t-list.proz-trev = t-list.t-rev / tot-rev * 100.
        IF t-list.m-pax NE 0 THEN t-list.proz-mpax = t-list.m-pax / tot-mpax * 100.
        IF t-list.m-rev NE 0 THEN t-list.proz-mrev = t-list.m-rev / tot-mrev * 100.
        IF t-list.y-pax NE 0 THEN t-list.proz-ypax = t-list.y-pax / tot-ypax * 100.
        IF t-list.y-rev NE 0 THEN t-list.proz-yrev = t-list.y-rev / tot-yrev * 100.

        CREATE detail-list.
        ASSIGN
            detail-list.descipt = STRING(t-list.bill-no) + " - " + STRING(t-list.dept, "99")
            detail-list.guest-name = t-list.guest-name
            detail-list.segm-no = t-list.segm-no
        .

        IF long-digit THEN
        DO:
            ASSIGN
                detail-list.pax         = STRING(t-list.pax, "->>>>>>9")
                detail-list.t-rev       = STRING(t-list.t-rev, "->>>,>>>,>>>,>>>,>>9")
                detail-list.m-pax       = STRING(t-list.m-pax, "->>>>>>9")
                detail-list.m-rev       = STRING(t-list.m-rev, "->>>,>>>,>>>,>>>,>>9")
                detail-list.y-pax       = STRING(t-list.y-pax, "->>>>>>9")
                detail-list.y-rev       = STRING(t-list.y-rev, "->>>,>>>,>>>,>>>,>>9")
                detail-list.proz-pax    = STRING(t-list.proz-pax, "->>9.99")
                detail-list.proz-trev   = STRING(t-list.proz-trev, "->>9.99")
                detail-list.proz-mpax   = STRING(t-list.proz-mpax, "->>9.99")
                detail-list.proz-mrev   = STRING(t-list.proz-mrev, "->>9.99")
                detail-list.proz-ypax   = STRING(t-list.proz-ypax, "->>9.99")
                detail-list.proz-yrev   = STRING(t-list.proz-yrev, "->>9.99")
            .
        END.
        ELSE
        DO:
            ASSIGN
                detail-list.pax         = STRING(t-list.pax, "  ->>>>9")
                detail-list.t-rev       = STRING(t-list.t-rev, "->,>>>,>>>,>>>,>>9.99")
                detail-list.m-pax       = STRING(t-list.m-pax, " ->>>>>9")
                detail-list.m-rev       = STRING(t-list.m-rev, "->,>>>,>>>,>>>,>>9.99")
                detail-list.y-pax       = STRING(t-list.y-pax, " ->>>>>9")
                detail-list.y-rev       = STRING(t-list.y-rev, "->,>>>,>>>,>>>,>>9.99")
                detail-list.proz-pax    = STRING(t-list.proz-pax, "->>9.99")
                detail-list.proz-trev   = STRING(t-list.proz-trev, "->>9.99")
                detail-list.proz-mpax   = STRING(t-list.proz-mpax, "->>9.99")
                detail-list.proz-mrev   = STRING(t-list.proz-mrev, "->>9.99")
                detail-list.proz-ypax   = STRING(t-list.proz-ypax, "->>9.99")
                detail-list.proz-yrev   = STRING(t-list.proz-yrev, "->>9.99")
            .
        END.
    END.

    FIND FIRST detail-list NO-LOCK NO-ERROR.
    IF AVAILABLE detail-list THEN
    DO:
        CREATE detail-list.
        ASSIGN
            detail-list.flag        = "*"
            detail-list.descipt     = "T O T A L"
            detail-list.pax         = STRING(tot-pax, "->>>>>>9")
            detail-list.t-rev       = STRING(tot-rev, "->,>>>,>>>,>>>,>>9.99")
            detail-list.m-pax       = STRING(tot-mpax, "->>>>>>9")
            detail-list.m-rev       = STRING(tot-mrev, "->,>>>,>>>,>>>,>>9.99")
            detail-list.y-pax       = STRING(tot-ypax, "->>>>>>9")
            detail-list.y-rev       = STRING(tot-yrev, "->,>>>,>>>,>>>,>>9.99")
            detail-list.proz-pax    = STRING(100, ">>9.99")
            detail-list.proz-trev   = STRING(100, ">>9.99")
            detail-list.proz-mpax   = STRING(100, ">>9.99")
            detail-list.proz-mrev   = STRING(100, ">>9.99")
            detail-list.proz-ypax   = STRING(100, ">>9.99")
            detail-list.proz-yrev   = STRING(100, ">>9.99")
        .
    END.   
END PROCEDURE.
