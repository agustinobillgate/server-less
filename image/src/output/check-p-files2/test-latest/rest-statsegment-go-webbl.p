
DEFINE TEMP-TABLE output-list
    FIELD flag          AS CHARACTER
    FIELD segm-no       AS CHARACTER
    FIELD g-segm        AS CHARACTER
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
/**/
DEFINE INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE.
DEFINE INPUT PARAMETER sorttype AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

/*
DEFINE VARIABLE pvILanguage AS INTEGER NO-UNDO.
DEFINE VARIABLE from-date   AS DATE.
DEFINE VARIABLE to-date     AS DATE.
DEFINE VARIABLE sorttype    AS INTEGER.
DEFINE VARIABLE detailed    AS LOGICAL.

ASSIGN
    pvILanguage  = 1
    from-date    = 01/12/19
    to-date      = 01/12/19
    sorttype     = 1
    detailed     = NO
.
*/
DEFINE TEMP-TABLE t-list
    FIELD flag          AS CHARACTER
    FIELD segm-no       AS INTEGER
    FIELD g-segm        AS CHARACTER
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

DEFINE TEMP-TABLE segm-list
    FIELD segmnr        AS INTEGER
    FIELD bezeich       AS CHARACTER
.

DEFINE VARIABLE price-decimal AS INTEGER.
DEFINE VARIABLE black-list AS INTEGER.
DEFINE VARIABLE start-month AS DATE.
DEFINE VARIABLE start-year AS DATE.
DEFINE VARIABLE long-digit AS LOGICAL.
DEFINE VARIABLE f-endkum AS INTEGER. 
DEFINE VARIABLE m-endkum AS INTEGER.
DEFINE VARIABLE b-endkum AS INTEGER.

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "rest-statsegment".

start-month = DATE(MONTH(to-date), 1, YEAR(to-date)).
start-year = DATE(1, 1, YEAR(to-date)).

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
IF sorttype EQ 1 THEN RUN create-list-food.
ELSE IF sorttype EQ 2 THEN RUN create-list-bev.
ELSE IF sorttype EQ 3 THEN RUN create-list-other.
ELSE IF sorttype EQ 4 THEN RUN create-list-all.
*/
RUN create-list.

/*****************************************************************************************************/
PROCEDURE create-list:
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

    FOR EACH output-list:
        DELETE output-list.
    END.    

    curr-zeit = TIME.
    
    /*
    command-str = "FOR EACH h-journal WHERE h-journal.bill-datum GE " + STRING(start-year) + " AND h-journal.bill-datum LE " + STRING(to-date) + " USE-INDEX segment_ix NO-LOCK".
    CREATE QUERY qh.
    qh:SET-BUFFERS(BUFFER h-journal:HANDLE).
    qh:QUERY-PREPARE(command-str).
    qh:QUERY-OPEN.

    REPEAT:  
        qh:GET-NEXT().
        IF NOT AVAILABLE h-journal THEN LEAVE.
    */
    /*
    FIND FIRST h-journal WHERE h-journal.bill-datum GE start-year 
        AND h-journal.bill-datum LE to-date NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE h-journal: FT serverless*/
    FOR EACH h-journal WHERE h-journal.bill-datum GE start-year 
        AND h-journal.bill-datum LE to-date NO-LOCK USE-INDEX segment_ix,
        FIRST h-bill WHERE h-bill.rechnr EQ h-journal.rechnr  
            AND h-bill.departement EQ h-journal.departement 
            AND h-bill.bilname NE "" NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr 
                AND h-artikel.departement EQ h-journal.departement
                AND h-artikel.artart EQ 0 NO-LOCK:
                   
        guest-no = 0.
        /*FIND FIRST h-bill WHERE h-bill.rechnr EQ h-journal.rechnr  
            AND h-bill.departement EQ h-journal.departement 
            AND h-bill.bilname NE "" NO-LOCK NO-ERROR.
        IF AVAILABLE h-bill THEN
        DO:
            FIND FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr 
                AND h-artikel.departement EQ h-journal.departement
                AND h-artikel.artart EQ 0 NO-LOCK NO-ERROR.
            IF AVAILABLE h-artikel THEN*/
            DO:
                IF sorttype EQ 1 THEN /*Food*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement                        
                        AND (artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5) NO-LOCK NO-ERROR.
                END.
                ELSE IF sorttype EQ 2 THEN /*Beverage*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement                        
                        AND artikel.umsatzart EQ 6 NO-LOCK NO-ERROR.
                END.
                ELSE IF sorttype EQ 3 THEN /*Other*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND artikel.umsatzart EQ 4 NO-LOCK NO-ERROR.
                END.
                ELSE IF sorttype EQ 4 THEN /*All*/
                DO:
                    FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                        AND artikel.departement EQ h-artikel.departement
                        AND artikel.umsatzart GE 3 AND artikel.umsatzart LE 6 NO-LOCK NO-ERROR.
                END.

                IF AVAILABLE artikel THEN
                DO:                
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

                    IF guest-no NE 0 AND h-bill.segmentcode NE 0 THEN
                    DO:
                        FIND FIRST guest WHERE guest.gastnr EQ guest-no NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN
                        DO:
                            FIND FIRST t-list WHERE t-list.segm-no EQ h-bill.segmentcode NO-LOCK NO-ERROR.
                            IF NOT AVAILABLE t-list THEN
                            DO:
                                CREATE t-list.
                                t-list.segm-no = h-bill.segmentcode.
    
                                FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.
                                IF AVAILABLE segment THEN t-list.g-segm = ENTRY(1, segment.bezeich, "$$0").
                            END.
                                                            
                            IF h-journal.bill-datum EQ to-date THEN
                            DO:
                                IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN
                                DO:
                                    ASSIGN
                                        t-list.pax = t-list.pax + h-bill.belegung
                                        tot-pax = tot-pax + h-bill.belegung                                            
                                    .
                                END.
                
                                t-list.t-rev = t-list.t-rev + h-journal.betrag.            
                                tot-rev = tot-rev + h-journal.betrag.
                            END.
                        
                            IF MONTH(h-journal.bill-datum) EQ MONTH(to-date) THEN
                            DO:
                                IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN
                                DO:
                                    ASSIGN
                                        t-list.m-pax = t-list.m-pax + h-bill.belegung
                                        tot-mpax = tot-mpax + h-bill.belegung
                                    .
                                END.
                                          
                                t-list.m-rev = t-list.m-rev + h-journal.betrag.            
                                tot-mrev = tot-mrev + h-journal.betrag.
                            END.      
                        
                            IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN
                            DO:
                                ASSIGN
                                    t-list.y-pax = t-list.y-pax + h-bill.belegung
                                    tot-ypax = tot-ypax + h-bill.belegung
                                .
                            END.
                                
                            t-list.y-rev = t-list.y-rev + h-journal.betrag.        
                            tot-yrev = tot-yrev + h-journal.betrag.                                                                     
                
                            curr-billno = STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement).                            
                        END.
                    END.
                    ELSE    /*UNKNOWN Segment*/
                    DO:
                        FIND FIRST t-list WHERE t-list.segm-no EQ 9999 NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE t-list THEN
                        DO:
                            CREATE t-list.
                            ASSIGN
                                t-list.segm-no  = 9999
                                t-list.g-segm   = "UNKNOWN"
                                .
                        END.    

                        IF h-journal.bill-datum EQ to-date THEN
                        DO:
                            IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN
                            DO:
                                ASSIGN
                                    t-list.pax = t-list.pax + h-bill.belegung
                                    tot-pax = tot-pax + h-bill.belegung                                            
                                .
                            END.
            
                            t-list.t-rev = t-list.t-rev + h-journal.betrag.            
                            tot-rev = tot-rev + h-journal.betrag.
                        END.
                    
                        IF MONTH(h-journal.bill-datum) EQ MONTH(to-date) THEN
                        DO:
                            IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN
                            DO:
                                ASSIGN
                                    t-list.m-pax = t-list.m-pax + h-bill.belegung
                                    tot-mpax = tot-mpax + h-bill.belegung
                                .
                            END.
                                      
                            t-list.m-rev = t-list.m-rev + h-journal.betrag.            
                            tot-mrev = tot-mrev + h-journal.betrag.
                        END.      
                    
                        IF curr-billno NE (STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement)) THEN
                        DO:
                            ASSIGN
                                t-list.y-pax = t-list.y-pax + h-bill.belegung
                                tot-ypax = tot-ypax + h-bill.belegung
                            .
                        END.
                            
                        t-list.y-rev = t-list.y-rev + h-journal.betrag.        
                        tot-yrev = tot-yrev + h-journal.betrag.                                                                     
            
                        curr-billno = STRING(h-bill.rechnr) + "-" + STRING(h-bill.departement).
                    END.
                END.
            END.                                
        /*END.       */

        /*FIND NEXT h-journal WHERE h-journal.bill-datum GE start-year 
            AND h-journal.bill-datum LE to-date NO-LOCK NO-ERROR.*/
    END.      
    /*              
    qh:QUERY-CLOSE().
    DELETE OBJECT qh.
    */

    FOR EACH t-list NO-LOCK BY t-list.segm-no:
        IF t-list.pax NE 0 THEN t-list.proz-pax = t-list.pax / tot-pax * 100.
        IF t-list.t-rev NE 0 THEN t-list.proz-trev = t-list.t-rev / tot-rev * 100.
        IF t-list.m-pax NE 0 THEN t-list.proz-mpax = t-list.m-pax / tot-mpax * 100.
        IF t-list.m-rev NE 0 THEN t-list.proz-mrev = t-list.m-rev / tot-mrev * 100.
        IF t-list.y-pax NE 0 THEN t-list.proz-ypax = t-list.y-pax / tot-ypax * 100.
        IF t-list.y-rev NE 0 THEN t-list.proz-yrev = t-list.y-rev / tot-yrev * 100.

        CREATE output-list.
        ASSIGN
            output-list.segm-no = STRING(t-list.segm-no, ">>>>>>>").    
            output-list.g-segm  = t-list.g-segm
        .

        IF long-digit THEN
        DO:
            ASSIGN
                output-list.pax         = STRING(t-list.pax, ">>>>>>9")
                output-list.t-rev       = STRING(t-list.t-rev, "->>>,>>>,>>>,>>>,>>9")
                output-list.m-pax       = STRING(t-list.m-pax, ">>>>>>9")
                output-list.m-rev       = STRING(t-list.m-rev, "->>>,>>>,>>>,>>>,>>9")
                output-list.y-pax       = STRING(t-list.y-pax, ">>>>>>9")
                output-list.y-rev       = STRING(t-list.y-rev, "->>>,>>>,>>>,>>>,>>9")
                output-list.proz-pax    = STRING(t-list.proz-pax, ">>9.99")
                output-list.proz-trev   = STRING(t-list.proz-trev, ">>9.99")
                output-list.proz-mpax   = STRING(t-list.proz-mpax, ">>9.99")
                output-list.proz-mrev   = STRING(t-list.proz-mrev, ">>9.99")
                output-list.proz-ypax   = STRING(t-list.proz-ypax, ">>9.99")
                output-list.proz-yrev   = STRING(t-list.proz-yrev, ">>9.99")
            .
        END.
        ELSE
        DO:
            ASSIGN
                output-list.pax         = STRING(t-list.pax, "  >>>>9")
                output-list.t-rev       = STRING(t-list.t-rev, ">,>>>,>>>,>>>,>>9.99")
                output-list.m-pax       = STRING(t-list.m-pax, " >>>>>9")
                output-list.m-rev       = STRING(t-list.m-rev, ">,>>>,>>>,>>>,>>9.99")
                output-list.y-pax       = STRING(t-list.y-pax, " >>>>>9")
                output-list.y-rev       = STRING(t-list.y-rev, ">,>>>,>>>,>>>,>>9.99")
                output-list.proz-pax    = STRING(t-list.proz-pax, ">>9.99")
                output-list.proz-trev   = STRING(t-list.proz-trev, ">>9.99")
                output-list.proz-mpax   = STRING(t-list.proz-mpax, ">>9.99")
                output-list.proz-mrev   = STRING(t-list.proz-mrev, ">>9.99")
                output-list.proz-ypax   = STRING(t-list.proz-ypax, ">>9.99")
                output-list.proz-yrev   = STRING(t-list.proz-yrev, ">>9.99")
            .
        END.
    END.

    FIND FIRST output-list NO-LOCK NO-ERROR.
    IF AVAILABLE output-list THEN
    DO:
        CREATE output-list.
        CREATE output-list.
        ASSIGN
            output-list.g-segm      = translateExtended("Total Revenue",lvCAREA,"")
            output-list.pax         = STRING(tot-pax, ">>>>>>9")
            output-list.t-rev       = STRING(tot-rev, ">,>>>,>>>,>>>,>>9.99")
            output-list.m-pax       = STRING(tot-mpax, ">>>>>>9")
            output-list.m-rev       = STRING(tot-mrev, ">,>>>,>>>,>>>,>>9.99")
            output-list.y-pax       = STRING(tot-ypax, ">>>>>>9")
            output-list.y-rev       = STRING(tot-yrev, ">,>>>,>>>,>>>,>>9.99")
            output-list.proz-pax    = STRING(100, ">>9.99")
            output-list.proz-trev   = STRING(100, ">>9.99")
            output-list.proz-mpax   = STRING(100, ">>9.99")
            output-list.proz-mrev   = STRING(100, ">>9.99")
            output-list.proz-ypax   = STRING(100, ">>9.99")
            output-list.proz-yrev   = STRING(100, ">>9.99")
        .
    END.
END PROCEDURE.
