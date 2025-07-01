DEFINE TEMP-TABLE output-list 
    FIELD bezeich     AS CHAR 
    FIELD c           AS CHAR FORMAT "x(2)" 
    FIELD NS          AS CHAR FORMAT "x(1)"
    FIELD MB          AS CHAR FORMAT "x(1)"
    FIELD shift       AS CHAR FORMAT "x(2)"
    FIELD dept        AS CHAR FORMAT "x(2)"
    FIELD STR         AS CHAR
    FIELD remark      AS CHAR FORMAT "x(24)" LABEL "Remark"
    FIELD gname       AS CHAR FORMAT "x(24)" LABEL "Guest Name"
    FIELD descr       AS CHAR
    FIELD voucher     AS CHAR
    FIELD checkin     AS DATE
    FIELD checkout    AS DATE
    FIELD guestname   AS CHAR
    FIELD segcode     AS CHAR FORMAT "X(20)" LABEL "SegmentCode"
    FIELD amt-nett    AS DECIMAL
    FIELD service     AS DECIMAL
    FIELD vat         AS DECIMAL
    FIELD zinr        AS CHAR
    FIELD deptno      AS INT.

/**/
DEFINE INPUT PARAMETER from-art         AS INTEGER.
DEFINE INPUT PARAMETER to-art           AS INTEGER.
DEFINE INPUT PARAMETER from-dept        AS INTEGER.
DEFINE INPUT PARAMETER to-dept          AS INTEGER.
DEFINE INPUT PARAMETER from-date        AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.

DEFINE INPUT PARAMETER sorttype         AS INTEGER.
DEFINE INPUT PARAMETER exclude-ARTrans  AS LOGICAL.
DEFINE INPUT PARAMETER long-digit       AS LOGICAL.
DEFINE INPUT PARAMETER foreign-flag     AS LOGICAL.
DEFINE INPUT PARAMETER mi-onlyjournal   AS LOGICAL.
DEFINE INPUT PARAMETER mi-excljournal   AS LOGICAL.
DEFINE INPUT PARAMETER mi-post          AS LOGICAL.
DEFINE INPUT PARAMETER mi-showrelease   AS LOGICAL. 
DEFINE INPUT PARAMETER mi-break         AS LOGICAL.

DEFINE OUTPUT PARAMETER gtot            AS DECIMAL INITIAL 0. 
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
/**/
/*
DEFINE VARIABLE from-art         AS INTEGER INIT 200.
DEFINE VARIABLE to-art           AS INTEGER INIT 200.
DEFINE VARIABLE from-dept        AS INTEGER INIT 0.
DEFINE VARIABLE to-dept          AS INTEGER INIT 0.
DEFINE VARIABLE from-date        AS DATE    INIT 08/22/24.
DEFINE VARIABLE to-date          AS DATE    INIT 08/22/24.
DEFINE VARIABLE sorttype         AS INTEGER INIT 0.
DEFINE VARIABLE exclude-ARTrans  AS LOGICAL INIT NO.
DEFINE VARIABLE long-digit       AS LOGICAL INIT NO.
DEFINE VARIABLE foreign-flag     AS LOGICAL INIT NO.
DEFINE VARIABLE mi-onlyjournal   AS LOGICAL INIT NO.
DEFINE VARIABLE mi-excljournal   AS LOGICAL INIT YES.
DEFINE VARIABLE mi-post          AS LOGICAL INIT YES.
DEFINE VARIABLE gtot             AS DECIMAL INITIAL 0. 
DEFINE VARIABLE mi-showrelease   AS LOGICAL INIT YES.
DEFINE VARIABLE mi-break         AS LOGICAL INIT NO.
*/
/*===============================*/
DEFINE VARIABLE curr-date  AS DATE.
DEFINE VARIABLE descr1     AS CHAR    NO-UNDO.
DEFINE VARIABLE voucher-no AS CHAR    NO-UNDO.
DEFINE VARIABLE ind        AS INTEGER NO-UNDO.
DEFINE VARIABLE indexing   AS INTEGER NO-UNDO.
DEFINE VARIABLE gdelimiter AS CHAR    NO-UNDO.
DEFINE VARIABLE roomnumber AS CHAR NO-UNDO.
DEFINE VARIABLE zinrdate   AS DATE NO-UNDO.
DEFINE VARIABLE billnumber AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-str   AS CHAR NO-UNDO.
DEFINE VARIABLE curr-resnr AS INTEGER NO-UNDO.
DEFINE VARIABLE serv       AS DECIMAL    NO-UNDO.
DEFINE VARIABLE vat        AS DECIMAL    NO-UNDO.
DEFINE VARIABLE netto      AS DECIMAL    NO-UNDO.
DEFINE VARIABLE temp-str   AS CHAR    NO-UNDO.
DEFINE VARIABLE hoteldept  AS INTEGER.

DEFINE BUFFER buffguest FOR guest.

IF from-date EQ ? THEN RETURN.
IF to-date EQ ? THEN RETURN.
RUN journal-list.
RUN custom-record.
/*
CURRENT-WINDOW:WIDTH = 260.
FOR EACH output-list:
    DISP 
        INT(SUBSTR(output-list.STR,15,9)) FORMAT ">>>>>>>>>" COLUMN-LABEL "Bill No"
        INT(SUBSTR(output-list.STR,24,4)) FORMAT ">>>>"      COLUMN-LABEL "Art No" 
        SUBSTRING(STR,9,6)                FORMAT "x(6)"      COLUMN-LABEL "RmNo"  
        output-list.descr                 FORMAT "x(30)"     COLUMN-LABEL "Descr" 
        output-list.guestname             FORMAT "x(40)"     COLUMN-LABEL "Guest Name field" 
        SUBSTRING(output-list.STR,167,25) FORMAT "x(40)"     COLUMN-LABEL "Guest Name STR" 
        output-list.gname                 FORMAT "x(40)"     COLUMN-LABEL "Bill Receiver" 
        output-list.checkin  
        output-list.checkout 
        output-list.guestname
        output-list.segcode  
    WITH WIDTH 255.
END.
*/
/*************** PROCEDURES ***************/
PROCEDURE custom-record:
    DEFINE VARIABLE roomnumber AS CHAR NO-UNDO.
    DEFINE VARIABLE zinrdate   AS DATE NO-UNDO.
    DEFINE VARIABLE billnumber AS INTEGER NO-UNDO.
    DEFINE VARIABLE curr-str   AS CHAR NO-UNDO.
    DEFINE VARIABLE curr-resnr AS INTEGER NO-UNDO.
    DEFINE VARIABLE journdate  AS DATE.
    /* Dzikri - FO Ticket 10/10/2024 */
    DEFINE VARIABLE temp-resnr AS INTEGER NO-UNDO.
    DEFINE VARIABLE temp-descr AS CHAR NO-UNDO.
    DEFINE VARIABLE artikelnr  AS INTEGER NO-UNDO.
    /* Dzikri - FO Ticket 10/10/2024 */

    FIND FIRST htparam WHERE paramnr EQ 110 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        journdate = fdate.
    END.

    FOR EACH output-list:
        ASSIGN
            roomnumber = SUBSTRING(output-list.STR,9,6)
            zinrdate   = DATE(SUBSTRING(output-list.STR,1,8))
            billnumber = INT(SUBSTRING(output-list.STR,15,9))
            artikelnr  = INTEGER(SUBSTRING(STR,24,4)) /* Dzikri - FO Ticket 10/10/2024 */
            curr-str   = " "
            curr-resnr = 0
        .
        
        IF output-list.mb EQ "*" THEN /*output-list.guestname = "".*/
        DO:
            FIND FIRST bill WHERE bill.rechnr EQ billnumber NO-LOCK NO-ERROR.
            FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr AND bill-line.zinr EQ roomnumber NO-LOCK NO-ERROR.
            FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr AND res-line.zinr EQ roomnumber AND res-line.ankunft LE zinrdate AND res-line.abreise GE zinrdate NO-LOCK NO-ERROR.
            FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
            FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
            FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
                output-list.str        = output-list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1.  
                output-list.checkin    = res-line.ankunft. 
                output-list.checkout   = res-line.abreise. 
                output-list.guestname  = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                output-list.gname      = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1.
            END.
            FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
            IF AVAILABLE segment THEN output-list.segcode = segment.bezeich.
            ELSE output-list.segcode = "".
        END.
        /*
        IF output-list.mb EQ "*" AND SUBSTRING(output-list.STR,9,6) EQ "" THEN
        DO:
            output-list.guestname = "".
            output-list.checkin    = ?. 
            output-list.checkout   = ?. 
            output-list.segcode    = "".
        END.
         */
        /* Dzikri - FO Ticket 10/10/2024
        IF SUBSTRING(output-list.STR,9,6) EQ "" AND output-list.ns EQ "" THEN
        DO:
         /* output-lsit.guestname = "". */ /* Dzikri - FO Ticket 10/10/2024 */
            output-list.checkin    = ?. 
            output-list.checkout   = ?. 
            output-list.segcode    = "".
        END.
         */
        IF SUBSTRING(STR,78, 12) MATCHES "*T O T A L*" THEN 
            ASSIGN 
            output-list.guestname = ""
            output-list.segcode   = ""
            output-list.checkin   = ?  
            output-list.checkout  = ?  
            output-list.str       = SUBSTRING(output-list.str,1,122).
        IF SUBSTRING(STR,78, 12) MATCHES "*Grand TOTAL*" THEN 
            ASSIGN 
            output-list.guestname = ""
            output-list.segcode   = ""
            output-list.checkin   = ?  
            output-list.checkout  = ?  
            output-list.str       = SUBSTRING(output-list.str,1,122). 

        IF NUM-ENTRIES(output-list.gname,"|") GE 2 THEN
        DO:
            output-list.gname = ENTRY(1,output-list.gname,"|").
            output-list.guestname = ENTRY(1,output-list.gname,"|").
        END.

        /* Dzikri - FO Ticket 10/10/2024 */
        IF output-list.descr MATCHES "*[*" THEN
        DO:
            temp-resnr = 0.
            /*
            DEF VAR temp-resnr AS INT.
            DEF VAR temp-descr AS CHAR.
            temp-descr = ENTRY(2,output-list.descr,"[").
            temp-descr = REPLACE(temp-descr,"]","").
            temp-descr = REPLACE(temp-descr,"]","").
            temp-resnr = INT(ENTRY(2,temp-descr,"#")).
            */
            temp-descr = ENTRY(1,output-list.descr,"]").
            IF NUM-ENTRIES(temp-descr,"#") GE 2 THEN temp-resnr = INT(ENTRY(1,ENTRY(2,temp-descr,"#")," ")).
            ELSE IF NUM-ENTRIES(output-list.descr,"[") GT 1 THEN DO:
                IF NUM-ENTRIES(ENTRY(1,output-list.descr,"["),"/") LE 1 THEN
                DO:
                    FIND FIRST artikel where artikel.artnr EQ artikelnr.
                    temp-resnr = INT(SUBSTRING(ENTRY(1,output-list.descr,"["),LENGTH(artikel.bezeich) + 2)).
                END.
            END.
            /*
            ELSE IF NUM-ENTRIES(output-list.descr,"[") GT 1 THEN DO:
                FIND FIRST artikel where artikel.artnr EQ artikelnr.
                temp-resnr = INT(SUBSTRING(ENTRY(1,output-list.descr,"["),LENGTH(artikel.bezeich) + 2)).
            END.
            ELSE IF NUM-ENTRIES(output-list.descr,"/") GT 1 THEN DO:
                FIND FIRST artikel where artikel.artnr EQ artikelnr.
                temp-resnr = INT(SUBSTRING(ENTRY(2,output-list.descr,"/"),LENGTH(artikel.bezeich) + 2,5)).
            END.
            */
            IF temp-resnr NE 0 THEN DO:
                FIND FIRST res-line WHERE res-line.resnr EQ temp-resnr AND res-line.reslinnr EQ 1 AND res-line.ankunft LE zinrdate AND res-line.abreise GE zinrdate NO-LOCK NO-ERROR.
                FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                DO:
                    output-list.str        = output-list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1.  
                    output-list.checkin    = res-line.ankunft. 
                    output-list.checkout   = res-line.abreise. 
                    output-list.guestname  = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                    output-list.gname      = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1.
                END.
                FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN output-list.segcode = segment.bezeich.
                ELSE output-list.segcode = "".
            END.
        END.
        
        ELSE IF output-list.descr MATCHES "*#*" THEN
        DO:
            temp-descr = ENTRY(1,output-list.descr,"]").
            IF NUM-ENTRIES(temp-descr,"#") GE 2 THEN temp-resnr = INT(ENTRY(1,ENTRY(2,temp-descr,"#")," ")).
            ELSE IF NUM-ENTRIES(output-list.descr,"[") GT 1 THEN DO:
                FIND FIRST artikel where artikel.artnr EQ artikelnr.
                temp-resnr = INT(SUBSTRING(ENTRY(1,output-list.descr,"["),LENGTH(artikel.bezeich) + 2)).
            END.
            /*
            ELSE IF NUM-ENTRIES(output-list.descr,"[") GT 1 THEN DO:
                FIND FIRST artikel where artikel.artnr EQ artikelnr.
                temp-resnr = INT(SUBSTRING(ENTRY(1,output-list.descr,"["),LENGTH(artikel.bezeich) + 2)).
            END.
            ELSE IF NUM-ENTRIES(output-list.descr,"/") GT 1 THEN DO:
                FIND FIRST artikel where artikel.artnr EQ artikelnr.
                temp-resnr = INT(SUBSTRING(ENTRY(2,output-list.descr,"/"),LENGTH(artikel.bezeich) + 2,5)).
            END.
            */
            
            IF temp-resnr NE 0 THEN DO:
                FIND FIRST res-line WHERE res-line.resnr EQ temp-resnr AND res-line.reslinnr EQ 1 AND res-line.ankunft LE zinrdate AND res-line.abreise GE zinrdate NO-LOCK NO-ERROR.
                FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                DO:
                    output-list.str        = output-list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1.  
                    output-list.checkin    = res-line.ankunft. 
                    output-list.checkout   = res-line.abreise. 
                    output-list.guestname  = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                    output-list.gname      = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1.
                END.
                FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN output-list.segcode = segment.bezeich.
                ELSE output-list.segcode = "".
            END.
        END.
        /* Dzikri - FO Ticket 10/10/2024 -END */

        IF roomnumber NE "" AND billnumber EQ 0 THEN
        DO:
            IF zinrdate GE journdate THEN
            DO:
                FIND FIRST res-line WHERE res-line.zinr EQ roomnumber AND res-line.ankunft EQ zinrdate NO-LOCK NO-ERROR.
                FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                DO:
                    output-list.str        = output-list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1.  
                    output-list.checkin    = res-line.ankunft. 
                    output-list.checkout   = res-line.abreise. 
                    output-list.guestname  = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                    output-list.gname      = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1.
                END.
                FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
                IF AVAILABLE segment THEN output-list.segcode = segment.bezeich.
                ELSE output-list.segcode = "".
            END.
            ELSE IF zinrdate LT journdate THEN
            DO:
                FIND FIRST genstat WHERE genstat.datum EQ zinrdate AND genstat.zinr EQ roomnumber NO-LOCK NO-ERROR.
                IF AVAILABLE genstat THEN
                DO:
                    FIND FIRST reservation WHERE reservation.resnr EQ genstat.resnr NO-LOCK NO-ERROR.
                    FIND FIRST buffguest WHERE buffguest.gastnr EQ genstat.gastnr NO-LOCK NO-ERROR.
                    FIND FIRST guest WHERE guest.gastnr EQ genstat.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN
                    DO:
                        output-list.str        = output-list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1.  
                        output-list.checkin    = genstat.res-date[1]. 
                        output-list.checkout   = genstat.res-date[2]. 
                        output-list.guestname  = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                        output-list.gname      = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1.
                    END.
                    FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
                    IF AVAILABLE segment THEN output-list.segcode = segment.bezeich.
                    ELSE output-list.segcode = "". 
                END.
            END.
        END.
        /*
        IF output-list.gname EQ "" AND billnumber NE 0 THEN
        DO:
            FIND FIRST h-bill WHERE h-bill.rechnr EQ billnumber NO-LOCK NO-ERROR.
            IF AVAILABLE h-bill THEN output-list.gname = h-bill.bilname.
        END.

        IF output-list.guestname EQ "" AND billnumber NE 0 THEN
        DO:
            FIND FIRST h-bill WHERE h-bill.rechnr EQ billnumber NO-LOCK NO-ERROR.
            IF AVAILABLE h-bill THEN output-list.guestname = h-bill.bilname.
        END.
        */
        roomnumber = "".               
    END.
END.

PROCEDURE journal-list: 
    DEFINE VARIABLE qty         AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
    DEFINE VARIABLE sub-tot     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE tot         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE curr-date   AS DATE. 
    DEFINE VARIABLE last-dept   AS INTEGER INITIAL -1. 
    DEFINE VARIABLE it-exist    AS LOGICAL. 
    DEFINE VARIABLE lviresnr    AS INTEGER INITIAL -1 NO-UNDO.
    DEFINE VARIABLE lvcs        AS CHAR               NO-UNDO.
    DEFINE VARIABLE amount      AS DECIMAL NO-UNDO. 
    DEFINE VARIABLE s           AS CHAR NO-UNDO.
    DEFINE VARIABLE cnt         AS INTEGER NO-UNDO.
    DEFINE VARIABLE i           AS INTEGER NO-UNDO.
    DEFINE VARIABLE gqty        AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
    DEFINE VARIABLE do-it       AS LOGICAL INITIAL YES.  
    DEFINE VARIABLE deptname    AS CHAR INITIAL "" NO-UNDO.
    DEFINE VARIABLE t-amt       AS DECIMAL NO-UNDO.
    DEFINE VARIABLE t-vat       AS DECIMAL NO-UNDO.
    DEFINE VARIABLE t-service   AS DECIMAL NO-UNDO.
    DEFINE VARIABLE tot-amt     AS DECIMAL NO-UNDO.
    DEFINE VARIABLE tot-vat     AS DECIMAL NO-UNDO.
    DEFINE VARIABLE tot-service AS DECIMAL NO-UNDO.
    DEFINE VARIABLE loopind     AS INTEGER NO-UNDO.

    DEFINE BUFFER gbuff FOR guest.
 
    FOR EACH output-list: 
        delete output-list. 
    END. 
    
    FOR EACH artikel WHERE artikel.artnr GE from-art 
        AND artikel.artnr LE to-art 
        AND artikel.departement GE from-dept 
        AND artikel.departement LE to-dept NO-LOCK BY (artikel.departement * 10000 + artikel.artnr): 
        
        IF last-dept NE artikel.departement THEN 
        FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-LOCK NO-ERROR. 
        last-dept   = artikel.departement. 
        sub-tot     = 0. 
        it-exist    = NO. 
        qty         = 0. 
        DO curr-date = from-date TO to-date: 
            IF sorttype = 0 THEN 
                FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
                    AND billjournal.departement = artikel.departement 
                    AND bill-datum = curr-date AND billjournal.anzahl NE 0 NO-LOCK BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
                    it-exist = YES. 
                    do-it    = YES.
                    IF (mi-onlyjournal EQ YES AND billjournal.bediener-nr EQ 0) OR (mi-excljournal EQ YES AND billjournal.bediener-nr NE 0) THEN /* Dzikri - CA8E6D */
                    DO:
                        do-it = NO.
                    END.
                    IF exclude-ARTrans AND billjournal.kassarapport THEN do-it = NO.
                    IF NOT mi-showrelease AND billjournal.betrag = 0 THEN do-it = NO.
                    IF do-it THEN
                    DO:
                        CREATE output-list. 
                        IF (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO) OR (billjournal.bediener-nr NE 0 AND mi-excljournal = NO) THEN
                        DO:
                            output-list.remark = billjournal.stornogrund.
                        END.

                        IF NOT billjournal.bezeich MATCHES ("*<*") AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
                        DO: 
                            IF billjournal.rechnr GT 0 THEN
                            DO:
                                IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO THEN
                                DO:
                                    FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                                    IF AVAILABLE bill AND billjournal.zinr NE "" THEN
                                    DO:
                                        FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr AND res-line.zinr EQ bill.zinr /* Dzikri - FO Ticket 10/10/2024 : EQ roomnumber */ 
                                            AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                            NO-LOCK NO-ERROR.
                                        FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                                        FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                        FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR. /* Dzikri - FO Ticket 10/10/2024 */
                                        
                                        IF AVAILABLE guest THEN
                                        DO:
                                            output-list.str        = output-list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1.  
                                            output-list.checkin    = res-line.ankunft. 
                                            output-list.checkout   = res-line.abreise. 
                                            output-list.guestname  = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                            output-list.gname      = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1. /* Dzikri - FO Ticket 10/10/2024 */
                                            
                                            FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
                                            IF AVAILABLE segment THEN output-list.segcode = segment.bezeich.
                                            ELSE output-list.segcode = "".
                                        END.
                                    END.
                                    ELSE IF AVAILABLE bill THEN
                                    DO:
                                        IF bill.resnr = 0 AND bill.bilname NE "" THEN 
                                        DO:
                                             output-list.gname = bill.bilname.        
                                             output-list.guestname = bill.bilname.
                                        END.                         
                                        ELSE
                                        DO:
                                            FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                                            IF AVAILABLE gbuff THEN
                                            DO:
                                                output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                                output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            END.
                                        END.                                 
                                    END.   /*available bill*/
                                END. /*bediener-nr = 0*/
                                ELSE IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO THEN
                                DO:
                                    /*WRONG GUESTNAME IF TRANSACTION CAME FROM OUTLETS*/
                                    FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE h-bill THEN 
                                    DO:
                                        /*
                                        output-list.gname = h-bill.bilname.
                                        output-list.guestname = h-bill.bilname.
                                        */
                                        IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                                        DO:
                                            FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr 
                                                AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                                NO-LOCK NO-ERROR.
                                            IF AVAILABLE res-line THEN
                                            DO:
                                                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                                ASSIGN
                                                    output-list.checkin   = res-line.ankunft. 
                                                    output-list.checkout  = res-line.abreise. 
                                                    output-list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                                    output-list.gname     = h-bill.bilname.
                                                IF h-bill.bilname EQ "" THEN
                                                DO:
                                                    FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                                                    IF AVAILABLE buffguest THEN 
                                                    DO:
                                                        output-list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1.
                                                        output-list.guestname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1.
                                                    END.
                                                END.
                                                FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.               
                                                /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                   
                                                FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                       
                                                IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                     
                                                ELSE output-list.segcode = segment.bezeich.
                                            END.
                                            ELSE 
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                        END.
                                        ELSE IF h-bill.resnr GT 0 THEN
                                        DO:
                                            FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                                            IF AVAILABLE guest THEN
                                            ASSIGN
                                                output-list.guestname = guest.NAME + "," + guest.vorname1
                                                output-list.gname     = h-bill.bilname.
                                            /* Dzikri - FO Ticket 10/10/2024 */
                                            ELSE 
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                            /* Dzikri - FO Ticket 10/10/2024 - END */
                                            FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                            
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                         
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.
                                        ELSE IF h-bill.resnr = 0 AND h-bill.bilname NE "" THEN
                                        DO:
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                            FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                             
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                          
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.
                                        ELSE IF billjournal.betriebsnr EQ 0 THEN
                                        DO:
                                            FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                                            IF AVAILABLE bill THEN
                                            DO:
                                                FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND res-line.reslinnr = bill.reslinnr
                                                    AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                                    NO-LOCK NO-ERROR.
                                                IF AVAILABLE res-line THEN
                                                DO:
                                                    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                                    ASSIGN
                                                        output-list.checkin   = res-line.ankunft. 
                                                        output-list.checkout  = res-line.abreise. 
                                                        output-list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                                        output-list.gname     = bill.NAME.
                                                
                                                    FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.               
                                                    /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                   
                                                    FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                       
                                                    IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                     
                                                    ELSE output-list.segcode = segment.bezeich.
                                                END.
                                            END.
                                        END.
                                    END.
                                END.
                            END. /*rechnr GT 0*/
                            ELSE
                            DO:
                                IF INDEX(billjournal.bezeich," *BQT") GT 0 THEN
                                DO:
                                    FIND FIRST bk-veran WHERE bk-veran.veran-nr = INTEGER(SUBSTR(billjournal.bezeich,INDEX(billjournal.bezeich," *BQT") + 5)) NO-LOCK NO-ERROR.
                                    IF AVAILABLE bk-veran THEN
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN 
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                        END.                  
                                    END.
                                END.
                                ELSE IF artikel.artart = 5 AND INDEX(billjournal.bezeich," [#") GT 0 AND billjournal.departement = 0 THEN
                                DO:
                                    lviresnr = -1.
                                    lvcs     = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich,"[#") + 2).
                                    lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
                                    FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE reservation THEN
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN 
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                        END.                    
                                    END.
                                END.
                                ELSE IF INDEX(billjournal.bezeich," #") GT 0 AND billjournal.departement = 0 THEN
                                DO:
                                    lvcs     = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich," #") + 2).
                                    lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                                    FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE reservation THEN
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN 
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                        END.                  
                                    END.
                                END.
                            END.
                        END.
                        ELSE
                        DO:
                            /*MNAufal - validasi data dari non room arrangement*/
                            FIND FIRST arrangement WHERE arrangement.artnr-logis EQ artikel.artnr AND arrangement.intervall EQ artikel.departement NO-LOCK NO-ERROR.
                            IF AVAILABLE arrangement THEN
                            DO:
                                FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr 
                                    AND h-bill.departement = billjournal.departement NO-LOCK NO-ERROR.
                                IF AVAILABLE h-bill THEN
                                DO:
                                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                                    DO:
                                        FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr
                                            AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                            NO-LOCK NO-ERROR.
                                        IF AVAILABLE res-line THEN
                                        DO:
                                            ASSIGN
                                                output-list.guestname = res-line.NAME
                                                output-list.gname     = h-bill.bilname.
                                            FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                                            /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                    
                                            FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                        
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                      
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.       
                                        ELSE 
                                        ASSIGN
                                            output-list.guestname = h-bill.bilname
                                            output-list.gname     = h-bill.bilname.                     
                                    END.
                                    ELSE IF h-bill.resnr GT 0 THEN
                                    DO:
                                        FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE guest THEN
                                        ASSIGN
                                            output-list.guestname = guest.NAME + "," + guest.vorname1
                                            output-list.gname     = h-bill.bilname.
                                        /* Dzikri - FO Ticket 10/10/2024 */
                                        ELSE 
                                        ASSIGN
                                            output-list.guestname = h-bill.bilname
                                            output-list.gname     = h-bill.bilname.
                                        /* Dzikri - FO Ticket 10/10/2024 - END */
                                        FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                             
                                        IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                          
                                        ELSE output-list.segcode   = segment.bezeich.
                                    END.
                                    ELSE IF h-bill.resnr = 0 THEN
                                    DO:
                                        ASSIGN
                                            output-list.guestname = h-bill.bilname
                                            output-list.gname     = h-bill.bilname.
                                        FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                            
                                        IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                         
                                        ELSE output-list.segcode   = segment.bezeich.
                                    END.
                                END.
                            END.
                            ELSE
                            DO:
                                FIND FIRST argt-line WHERE argt-line.argt-artnr EQ artikel.artnr AND argt-line.departement EQ artikel.departement NO-LOCK NO-ERROR.
                                IF AVAILABLE argt-line THEN
                                DO:
                                    /* Dzikri - FO Ticket 10/10/2024 */
                                    hoteldept = billjournal.departement.
                                    IF billjournal.bezeich MATCHES ("*<*") AND billjournal.bezeich MATCHES ("*>*") THEN
                                    DO:
                                        hoteldept = INTEGER(SUBSTRING(billjournal.bezeich, INDEX(billjournal.bezeich,"<") + 1, INDEX(billjournal.bezeich,">") - INDEX(billjournal.bezeich,"<") - 1)).
                                    END.
                                    /*ELSE IF billjournal.betriebsnr NE 0 THEN hoteldept = billjournal.betriebsnr.*/
                                    FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr 
                                        AND h-bill.departement = hoteldept NO-LOCK NO-ERROR.
                                    /* Dzikri - FO Ticket 10/10/2024 - END */
                                    IF AVAILABLE h-bill THEN
                                    DO:
                                        IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                                        DO:
                                            FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr
                                                AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                                NO-LOCK NO-ERROR.
                                            IF AVAILABLE res-line THEN
                                            DO:
                                                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                                ASSIGN
                                                    output-list.checkin   = res-line.ankunft. 
                                                    output-list.checkout  = res-line.abreise. 
                                                    output-list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                                    output-list.gname     = h-bill.bilname.
            
                                                FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.               
                                                /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                   
                                                FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                       
                                                IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                     
                                                ELSE output-list.segcode = segment.bezeich.
                                            END.    
                                            ELSE 
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.                        
                                        END.
                                        ELSE IF h-bill.resnr GT 0 THEN
                                        DO:
                                            FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                                            IF AVAILABLE guest THEN
                                            ASSIGN
                                                output-list.guestname = guest.NAME + "," + guest.vorname1
                                                output-list.gname     = h-bill.bilname.
                                            /* Dzikri - FO Ticket 10/10/2024 */
                                            ELSE 
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                            /* Dzikri - FO Ticket 10/10/2024 - END */
                                            FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                            
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                         
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.
                                        ELSE IF h-bill.resnr = 0 THEN
                                        DO:
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                            FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                             
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                          
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.
                                    END.
                                END.
                            END.
                        END.
                        
                        IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO AND billjournal.anzahl = 0) OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO AND billjournal.anzahl = 0) THEN output-list.bezeich = artikel.bezeich. 
            
                        IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN
                        DO:
                            ASSIGN 
                            output-list.c     = STRING(billjournal.betriebsnr,"99")
                            output-list.shift = STRING(billjournal.betriebsnr, "99"). 
                        END.
                        ELSE IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */ THEN 
                        DO: 
                            IF AVAILABLE bill THEN 
                            DO: 
                                IF bill.reslinnr = 1 AND bill.zinr = "" THEN 
                                DO:
                                    ASSIGN 
                                    output-list.c = "N"
                                    output-list.NS = "*".
                                END.
                                ELSE IF bill.reslinnr = 0 THEN 
                                DO:
                                    ASSIGN
                                    output-list.c = "M"
                                    output-list.MB = "*". 
                                END.
                            END. 
                        END. 
           
                        IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
                        ELSE amount = billjournal.betrag. 

                        IF mi-break = YES THEN 
                        DO:
                            ASSIGN
                              serv        = 0
                              vat         = 0
                            .
        
                            RUN calc-servvat.p (artikel.departement, artikel.artnr, billjournal.bill-datum,
                                                artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                            ASSIGN 
                                  output-list.amt-nett = amount / (1 + serv + vat)
                                  output-list.service  = output-list.amt-nett * serv
                                  output-list.vat      = output-list.amt-nett * vat
                                  t-amt                = t-amt + output-list.amt-nett
                                  t-vat                = t-vat + output-list.vat
                                  t-service            = t-service + output-list.service
                                  tot-amt              = tot-amt + output-list.amt-nett
                                  tot-vat              = tot-vat + output-list.vat
                                  tot-service          = tot-service + output-list.service
                              .                        
                        END.
                        ASSIGN 
                            descr1     = ""
                            voucher-no = "".
                        IF SUBSTR(billjournal.bezeich, 1, 1) = "*" OR billjournal.kassarapport THEN
                        ASSIGN
                            descr1 = billjournal.bezeich
                            voucher-no = "".
                        ELSE
                        DO:
                            IF NOT artikel.bezaendern THEN
                            DO:
                                /* Dzikri - FO Ticket 10/10/2024 */
                                ind = NUM-ENTRIES(billjournal.bezeich, "]").
                                IF ind GE 2 THEN gdelimiter = "]".
                                ELSE
                                DO:
                                    ind = NUM-ENTRIES(billjournal.bezeich, "/").
                                    IF ind GE 2 AND LENGTH(artikel.bezeich) LE INDEX(billjournal.bezeich, "/") AND billjournal.betrag NE 0 THEN gdelimiter = "/".
                                    ELSE
                                    DO:
                                        ind = NUM-ENTRIES(billjournal.bezeich, "|").
                                        IF ind GE 2 THEN gdelimiter = "|".
                                    END.
                                END.
                                /* Dzikri - FO Ticket 10/10/2024 - END */
                                IF ind NE 0 THEN
                                DO: 
                                    /*
                                    IF ind GT LENGTH(artikel.bezeich) THEN
                                        ASSIGN
                                        descr1 = ENTRY(1, billjournal.bezeich, gdelimiter)
                                        voucher-no = SUBSTRING(billjournal.bezeich, (ind + 1)).
                                    ELSE
                                    DO:
                                        cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                                        DO i = 1 TO cnt:
                                            IF descr1 = "" THEN descr1 = ENTRY(i, billjournal.bezeich, gdelimiter).    
                                            ELSE descr1 = descr1 + "/" + ENTRY(i, billjournal.bezeich, gdelimiter).
                                        END.
                                        voucher-no = SUBSTR(billjournal.bezeich, LENGTH(descr1) + 2). 
                                    END.
                                    IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                    */
                                    IF ind EQ 1 THEN
                                        ASSIGN
                                        descr1 = billjournal.bezeich
                                        voucher-no = "".
                                    ELSE IF ind EQ 2 THEN
                                    DO:
                                    ASSIGN 
                                        descr1 = ENTRY(1, billjournal.bezeich, gdelimiter) 
                                        voucher-no = ENTRY(2, billjournal.bezeich, gdelimiter).
                                    IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                    END.
                                    ELSE IF ind GT 2  THEN
                                    DO:
                                        voucher-no = "".
                                        descr1 = ENTRY(1, billjournal.bezeich, gdelimiter).
                                        DO loopind = 2 TO ind:
                                            voucher-no = voucher-no + ENTRY(loopind, billjournal.bezeich, gdelimiter) + gdelimiter.
                                        END.
                                        voucher-no = SUBSTRING(voucher-no,1,LENGTH(voucher-no) - 1).
                                    END.
                                END.
                                ELSE descr1 = billjournal.bezeich.
                            END.
                            ELSE /*M 110112 -> got voucher info if desc contains "/" */
                            DO:
                                ind = NUM-ENTRIES(billjournal.bezeich, "/").
                                IF ind EQ 1 THEN
                                    ASSIGN 
                                        descr1 = billjournal.bezeich
                                        voucher-no = "".
                                ELSE IF ind EQ 2 THEN
                                    ASSIGN 
                                        descr1 = ENTRY(1, billjournal.bezeich, "/") 
                                        voucher-no = ENTRY(2, billjournal.bezeich, "/").
                                /* Dzikri - FO Ticket 10/10/2024 */
                                ELSE IF ind GT 2 THEN
                                DO:
                                    descr1 = ENTRY(1, billjournal.bezeich, "/").
                                    DO loopind = 2 TO ind:
                                        voucher-no = voucher-no + ENTRY(loopind, billjournal.bezeich, "/") + "/".
                                    END.
                                    voucher-no = SUBSTRING(voucher-no,1,LENGTH(voucher-no) - 1).
                                END.
                                ELSE descr1 = billjournal.bezeich.
                                /* Dzikri - FO Ticket 10/10/2024 -END */
                            END. 
                        END.
                        /*M 020412 -> contain long descr*/ /*ITA 080713 -> add IF available output-list*/
                        IF AVAILABLE output-list THEN
                        ASSIGN
                            output-list.descr   = STRING(descr1, "x(100)")
                            output-list.voucher = STRING(voucher-no, "x(40)").  /*MT 03/12/13 */
                        IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO  THEN
                        DO:
                            FIND FIRST hoteldpt WHERE hoteldpt.num = billjournal.departement NO-LOCK NO-ERROR.
                            IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.
            
                            output-list.zinr = billjournal.zinr.
                            output-list.deptno = billjournal.departement. 

                            IF NOT long-digit THEN STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)") /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(descr1, "x(50)") 
                                + STRING(deptname, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>") /* Malik 2A7616 : "", "x(6)" -> billjournal.betriebsnr, ">>>>>>" */
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
                            ELSE STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(billjournal.bezeich, "x(50)") 
                                + STRING(deptname, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>") /* Malik 2A7616 : "", "x(6)" -> billjournal.betriebsnr, ">>>>>>" */
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
            
                            qty = qty + billjournal.anzahl. 
                            gqty = gqty + billjournal.anzahl. 
                    /*      IF billjournal.anzahl NE 0 THEN  */ 
                            DO: 
                                IF foreign-flag THEN 
                                DO: 
                                    sub-tot = sub-tot + billjournal.fremdwaehrng. 
                                    tot = tot + billjournal.fremdwaehrng. 
                                END. 
                                ELSE 
                                DO: 
                                    sub-tot = sub-tot + billjournal.betrag. 
                                    tot = tot + billjournal.betrag. 
                                END. 
                            END. 
                        END.
                        ELSE IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO THEN
                        DO:
                            FIND FIRST hoteldpt WHERE hoteldpt.num = billjournal.departement NO-LOCK NO-ERROR.
                            IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.
            
                            output-list.zinr = billjournal.zinr.
                            output-list.deptno = billjournal.departement. 

                            IF NOT long-digit THEN STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(descr1, "x(50)") 
                                + STRING(deptname, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>")
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
                            ELSE STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(billjournal.bezeich, "x(50)") 
                                + STRING(deptname, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>")
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
                            qty = qty + billjournal.anzahl. 
                            gqty = gqty + billjournal.anzahl. 
                    /*      IF billjournal.anzahl NE 0 THEN  */ 
                            DO: 
                                IF foreign-flag THEN 
                                DO: 
                                    sub-tot = sub-tot + billjournal.fremdwaehrng. 
                                    tot = tot + billjournal.fremdwaehrng. 
                                END. 
                                ELSE 
                                DO: 
                                    sub-tot = sub-tot + billjournal.betrag. 
                                    tot = tot + billjournal.betrag. 
                                END. 
                            END.
                        END.
                        ELSE IF mi-excljournal THEN
                        DO:
                            FIND FIRST hoteldpt WHERE hoteldpt.num = billjournal.departement NO-LOCK NO-ERROR.
                            IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.
            
                            output-list.zinr = billjournal.zinr.
                            output-list.deptno = billjournal.departement. 

                            IF NOT long-digit THEN STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(descr1, "x(50)") 
                                + STRING(deptname, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>")
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
                            ELSE STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(billjournal.bezeich, "x(50)") 
                                + STRING(deptname, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>")
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
                            qty = qty + billjournal.anzahl. 
                            gqty = gqty + billjournal.anzahl. 
                        /*  IF billjournal.anzahl NE 0 THEN  */ 
                            DO: 
                                IF foreign-flag THEN 
                                DO: 
                                    sub-tot = sub-tot + billjournal.fremdwaehrng. 
                                    tot = tot + billjournal.fremdwaehrng. 
                                END. 
                                ELSE 
                                DO: 
                                    sub-tot = sub-tot + billjournal.betrag. 
                                    tot = tot + billjournal.betrag. 
                                END. 
                            END. 
                        END.
                        /* Dzikri B8BF2D 22/10/2024 - get adult amount instead of bill amount if dayuse reservation for POS/outlet bill */
                        IF AVAILABLE res-line AND res-line.ankunft EQ res-line.abreise AND artikel.departement GT 0 THEN 
                        DO:
                            qty = qty - billjournal.anzahl + res-line.erwachs.
                            gqty = gqty - billjournal.anzahl + res-line.erwachs. 
                            temp-str = SUBSTRING(STR,101).
                            STR = SUBSTRING(STR,1,95).
                            STR = STR + STRING(res-line.erwachs, "-9999") + temp-str.
                            temp-str = "".
                        END.
                        /* Dzikri B8BF2D 22/10/2024 - END*/
                    END. /*if do-it*/
                END. /*each billjournal*/
            ELSE IF sorttype = 1 THEN 
                FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
                    AND billjournal.departement = artikel.departement 
                    AND bill-datum = curr-date NO-LOCK BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
                    it-exist = YES. 
                    do-it    = YES.
                    IF (mi-onlyjournal EQ YES AND billjournal.bediener-nr EQ 0) OR (mi-excljournal EQ YES AND billjournal.bediener-nr NE 0) THEN /* Dzikri - CA8E6D */
                    DO:
                        do-it = NO.
                    END.
                    IF exclude-ARTrans AND billjournal.kassarapport THEN do-it = NO.
                    IF NOT mi-showrelease AND billjournal.betrag = 0 THEN do-it = NO.
                    IF do-it THEN
                    DO:
                        CREATE output-list. 
                        IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) OR 
                            (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) THEN
                        DO:
                            output-list.remark = billjournal.stornogrund.
                        END.
                        IF NOT billjournal.bezeich MATCHES ("*<*") AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
                        DO: 
                            IF billjournal.rechnr GT 0 THEN
                            DO:
                                IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO THEN
                                DO:
                                    FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                                    IF AVAILABLE bill AND billjournal.zinr NE "" THEN
                                    DO:
                                        FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr AND res-line.zinr EQ bill.zinr /* Dzikri - FO Ticket 10/10/2024 : EQ roomnumber */
                                            AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                            NO-LOCK NO-ERROR.
                                        FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                                        FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                        FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR. /* Dzikri - FO Ticket 10/10/2024 */
                                        
                                        IF AVAILABLE guest THEN
                                        DO:
                                            output-list.str        = output-list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1.  
                                            output-list.checkin    = res-line.ankunft. 
                                            output-list.checkout   = res-line.abreise. 
                                            output-list.guestname  = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                            output-list.gname      = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1. /* Dzikri - FO Ticket 10/10/2024 */
                                            
                                            FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
                                            IF AVAILABLE segment THEN output-list.segcode = segment.bezeich.
                                            ELSE output-list.segcode = "".
                                        END.
                                    END.
                                    ELSE IF AVAILABLE bill THEN
                                    DO:
                                        IF bill.resnr = 0 AND bill.bilname NE "" THEN 
                                        DO:
                                             output-list.gname = bill.bilname.        
                                             output-list.guestname = bill.bilname.
                                        END.                         
                                        ELSE
                                        DO:
                                            FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                                            IF AVAILABLE gbuff THEN
                                            DO:
                                                output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                                output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            END.
                                        END.                                 
                                    END.   /*available bill*/
                                END. /*bediener-nr = 0*/
                                ELSE IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO THEN
                                DO:
                                    /*WRONG GUESTNAME IF TRANSACTION CAME FROM OUTLETS*/
                                    FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE h-bill THEN 
                                    DO:
                                        /*
                                        output-list.gname = h-bill.bilname.
                                        output-list.guestname = h-bill.bilname.
                                        */
                                        IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                                        DO:
                                            FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr
                                                AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                                NO-LOCK NO-ERROR.
                                            IF AVAILABLE res-line THEN
                                            DO:
                                                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                                ASSIGN
                                                    output-list.checkin   = res-line.ankunft. 
                                                    output-list.checkout  = res-line.abreise. 
                                                    output-list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                                    output-list.gname     = h-bill.bilname.
                                                IF h-bill.bilname EQ "" THEN
                                                DO:
                                                    FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
                                                    IF AVAILABLE buffguest THEN 
                                                    DO:
                                                        output-list.gname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1.
                                                        output-list.guestname = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1.
                                                    END.
                                                END.
                                                FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.               
                                                /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                   
                                                FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                       
                                                IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                     
                                                ELSE output-list.segcode = segment.bezeich.
                                            END.
                                            ELSE 
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                        END.
                                        ELSE IF h-bill.resnr GT 0 THEN
                                        DO:
                                            FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                                            IF AVAILABLE guest THEN
                                            ASSIGN
                                                output-list.guestname = guest.NAME + "," + guest.vorname1
                                                output-list.gname     = h-bill.bilname.
                                            /* Dzikri - FO Ticket 10/10/2024 */
                                            ELSE 
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                            /* Dzikri - FO Ticket 10/10/2024 - END */
                                            FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                            
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                         
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.
                                        ELSE IF h-bill.resnr = 0 AND h-bill.bilname NE "" THEN
                                        DO:
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                            FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                             
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                          
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.
                                        ELSE IF billjournal.betriebsnr EQ 0 THEN
                                        DO:
                                            FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                                            IF AVAILABLE bill THEN
                                            DO:
                                                FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND res-line.reslinnr = bill.reslinnr
                                                    AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                                    NO-LOCK NO-ERROR.
                                                IF AVAILABLE res-line THEN
                                                DO:
                                                    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                                    ASSIGN
                                                        output-list.checkin   = res-line.ankunft. 
                                                        output-list.checkout  = res-line.abreise. 
                                                        output-list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                                        output-list.gname     = bill.NAME.
                                                
                                                    FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.               
                                                    /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                   
                                                    FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                       
                                                    IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                     
                                                    ELSE output-list.segcode = segment.bezeich.
                                                END.
                                            END.
                                        END.
                                    END.
                                END.
                            END.
                            ELSE
                            DO:
                                IF artikel.artart = 5 AND INDEX(billjournal.bezeich," [#") GT 0 AND billjournal.departement = 0 THEN
                                DO:
                                    lviresnr = -1.
                                    lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich,"[#") + 2).
                                    lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
                                    FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE reservation THEN
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN 
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                        END.                    
                                    END.
                                END.
                                ELSE IF INDEX(billjournal.bezeich," #") GT 0 AND billjournal.departement = 0 THEN
                                DO:
                                    lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich," #") + 2).
                                    lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                                    FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE reservation THEN
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN 
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                        END.                    
                                    END.
                                END.
                            END.
                        END.
                        ELSE
                        DO:
                            /*MNAufal - validasi data dari non room arrangement*/
                            FIND FIRST arrangement WHERE arrangement.artnr-logis EQ artikel.artnr AND arrangement.intervall EQ artikel.departement NO-LOCK NO-ERROR.
                            IF AVAILABLE arrangement THEN
                            DO:
                                FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr 
                                    AND h-bill.departement = billjournal.departement NO-LOCK NO-ERROR.
                                IF AVAILABLE h-bill THEN
                                DO:
                                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                                    DO:
                                        FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr
                                            AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                            NO-LOCK NO-ERROR.
                                        IF AVAILABLE res-line THEN
                                        DO:
                                            ASSIGN
                                                output-list.guestname = res-line.NAME
                                                output-list.gname     = h-bill.bilname.
                                            FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                                            /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                    
                                            FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                        
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                      
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.        
                                        ELSE 
                                        ASSIGN
                                            output-list.guestname = h-bill.bilname
                                            output-list.gname     = h-bill.bilname.                    
                                    END.
                                    ELSE IF h-bill.resnr GT 0 THEN
                                    DO:
                                        FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE guest THEN
                                        ASSIGN
                                            output-list.guestname = guest.NAME + "," + guest.vorname1
                                            output-list.gname     = h-bill.bilname.
                                        /* Dzikri - FO Ticket 10/10/2024 */
                                        ELSE 
                                        ASSIGN
                                            output-list.guestname = h-bill.bilname
                                            output-list.gname     = h-bill.bilname.
                                        /* Dzikri - FO Ticket 10/10/2024 - END */
                                        FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                             
                                        IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                          
                                        ELSE output-list.segcode   = segment.bezeich.
                                    END.
                                    ELSE IF h-bill.resnr = 0 THEN
                                    DO:
                                        ASSIGN
                                            output-list.guestname = h-bill.bilname
                                            output-list.gname     = h-bill.bilname.
                                        FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                            
                                        IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                         
                                        ELSE output-list.segcode   = segment.bezeich.
                                    END.
                                END.
                            END.
                            ELSE
                            DO:
                                FIND FIRST argt-line WHERE argt-line.argt-artnr EQ artikel.artnr AND argt-line.departement EQ artikel.departement NO-LOCK NO-ERROR.
                                IF AVAILABLE argt-line THEN
                                DO:
                                    /* Dzikri - FO Ticket 10/10/2024 */
                                    hoteldept = billjournal.departement.
                                    IF billjournal.bezeich MATCHES ("*<*") AND billjournal.bezeich MATCHES ("*>*") THEN
                                    DO:
                                        hoteldept = INTEGER(SUBSTRING(billjournal.bezeich, INDEX(billjournal.bezeich,"<") + 1, INDEX(billjournal.bezeich,">") - INDEX(billjournal.bezeich,"<") - 1)).
                                    END.
                                    /*ELSE IF billjournal.betriebsnr NE 0 THEN hoteldept = billjournal.betriebsnr.*/
                                    FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr 
                                        AND h-bill.departement = hoteldept NO-LOCK NO-ERROR.
                                    /* Dzikri - FO Ticket 10/10/2024 - END */
                                    IF AVAILABLE h-bill THEN
                                    DO:
                                        IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                                        DO:
                                            FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr
                                                AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                                NO-LOCK NO-ERROR.
                                            IF AVAILABLE res-line THEN
                                            DO:
                                                FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                                ASSIGN
                                                    output-list.checkin   = res-line.ankunft. 
                                                    output-list.checkout  = res-line.abreise. 
                                                    output-list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                                    output-list.gname     = h-bill.bilname.
            
                                                FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.               
                                                /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                   
                                                FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                       
                                                IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                     
                                                ELSE output-list.segcode = segment.bezeich.
                                            END.  
                                            ELSE 
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.                          
                                        END.
                                        ELSE IF h-bill.resnr GT 0 THEN
                                        DO:
                                            FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                                            IF AVAILABLE guest THEN
                                            ASSIGN
                                                output-list.guestname = guest.NAME + "," + guest.vorname1
                                                output-list.gname     = h-bill.bilname.
                                            /* Dzikri - FO Ticket 10/10/2024 */
                                            ELSE 
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                            /* Dzikri - FO Ticket 10/10/2024 - END */
                                            FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                            
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                         
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.
                                        ELSE IF h-bill.resnr = 0 THEN
                                        DO:
                                            ASSIGN
                                                output-list.guestname = h-bill.bilname
                                                output-list.gname     = h-bill.bilname.
                                            FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                             
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                          
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.
                                    END.
                                END.
                            END.
                        END.
                
                        IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO
                            AND billjournal.anzahl = 0 /** AND billjournal.bediener NE 0 */) 
                            OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO
                            AND billjournal.anzahl = 0 /** AND billjournal.bediener EQ 0 */ ) THEN output-list.bezeich = artikel.bezeich. 
            
                        IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN 
                        ASSIGN
                            output-list.shift = STRING(billjournal.betriebsnr,"99")
                            output-list.c = STRING(billjournal.betriebsnr,"99"). 
                        ELSE IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */ THEN  
                        DO: 
                            IF AVAILABLE bill THEN 
                            DO: 
                                IF bill.reslinnr = 1 AND bill.zinr = "" THEN 
                                ASSIGN
                                output-list.c = "N"
                                output-list.NS = "*". 
                                ELSE IF bill.reslinnr = 0 THEN 
                                ASSIGN 
                                output-list.c = "M"
                                output-list.MB = "*". 
                            END. 
                        END. 
                 
                        IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
                        ELSE amount = billjournal.betrag. 
            
                        IF mi-break = YES THEN 
                        DO:
                            ASSIGN
                              serv        = 0
                              vat         = 0
                            .
            
                            RUN calc-servvat.p (artikel.departement, artikel.artnr, billjournal.bill-datum,
                                                artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                            ASSIGN 
                                  output-list.amt-nett = amount / (1 + serv + vat)
                                  output-list.service  = output-list.amt-nett * serv
                                  output-list.vat      = output-list.amt-nett * vat
                                  t-amt                = t-amt + output-list.amt-nett
                                  t-vat                = t-vat + output-list.vat
                                  t-service            = t-service + output-list.service
                                  tot-amt              = tot-amt + output-list.amt-nett
                                  tot-vat              = tot-vat + output-list.vat
                                  tot-service          = tot-service + output-list.service
                              .                        
                        END.
                
                        ASSIGN 
                            descr1 = ""
                            voucher-no = "".
                        IF SUBSTR(billjournal.bezeich, 1, 1) = "*" OR billjournal.kassarapport THEN
                        ASSIGN
                            descr1 = billjournal.bezeich
                            voucher-no = "".
                        ELSE
                        DO:
                            IF NOT artikel.bezaendern THEN
                            DO:
                                /* Dzikri - FO Ticket 10/10/2024 */
                                ind = NUM-ENTRIES(billjournal.bezeich, "]").
                                IF ind GE 2 THEN gdelimiter = "]".
                                ELSE
                                DO:
                                    ind = NUM-ENTRIES(billjournal.bezeich, "/").
                                    IF ind GE 2 AND LENGTH(artikel.bezeich) LE INDEX(billjournal.bezeich, "/") AND billjournal.betrag NE 0 THEN gdelimiter = "/".
                                    ELSE
                                    DO:
                                        ind = NUM-ENTRIES(billjournal.bezeich, "|").
                                        IF ind GE 2 THEN gdelimiter = "|".
                                    END.
                                END.
                                /* Dzikri - FO Ticket 10/10/2024 - END */
                                IF ind NE 0 THEN
                                DO: 
                                    /*
                                    IF ind GT LENGTH(artikel.bezeich) THEN
                                        ASSIGN
                                        descr1 = ENTRY(1, billjournal.bezeich, gdelimiter)
                                        voucher-no = SUBSTRING(billjournal.bezeich, (ind + 1)).
                                    ELSE
                                    DO:
                                        cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                                        DO i = 1 TO cnt:
                                            IF descr1 = "" THEN descr1 = ENTRY(i, billjournal.bezeich, gdelimiter).    
                                            ELSE descr1 = descr1 + "/" + ENTRY(i, billjournal.bezeich, gdelimiter).
                                        END.
                                        voucher-no = SUBSTR(billjournal.bezeich, LENGTH(descr1) + 2). 
                                    END.
                                    IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                    */
                                    IF ind EQ 1 THEN
                                        ASSIGN
                                        descr1 = billjournal.bezeich
                                        voucher-no = "".
                                    ELSE IF ind EQ 2 THEN
                                    DO:
                                    ASSIGN 
                                        descr1 = ENTRY(1, billjournal.bezeich, gdelimiter) 
                                        voucher-no = ENTRY(2, billjournal.bezeich, gdelimiter).
                                    IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                    END.
                                    ELSE IF ind GT 2  THEN
                                    DO:
                                        voucher-no = "".
                                        descr1 = ENTRY(1, billjournal.bezeich, gdelimiter).
                                        DO loopind = 2 TO ind:
                                            voucher-no = voucher-no + ENTRY(loopind, billjournal.bezeich, gdelimiter) + gdelimiter.
                                        END.
                                        voucher-no = SUBSTRING(voucher-no,1,LENGTH(voucher-no) - 1).
                                    END.
                                END.
                                ELSE descr1 = billjournal.bezeich.
                            END.
                            ELSE /*M 110112 -> got voucher info if desc contains "/" */
                            DO:
                                ind = NUM-ENTRIES(billjournal.bezeich, "/").
                                IF ind EQ 1 THEN
                                    ASSIGN 
                                        descr1 = billjournal.bezeich
                                        voucher-no = "".
                                ELSE IF ind EQ 2 THEN
                                    ASSIGN 
                                        descr1 = ENTRY(1, billjournal.bezeich, "/") 
                                        voucher-no = ENTRY(2, billjournal.bezeich, "/").
                                /* Dzikri - FO Ticket 10/10/2024 */
                                ELSE IF ind GT 2 THEN
                                DO:
                                    descr1 = ENTRY(1, billjournal.bezeich, "/").
                                    DO loopind = 2 TO ind:
                                        voucher-no = voucher-no + ENTRY(loopind, billjournal.bezeich, "/") + "/".
                                    END.
                                    voucher-no = SUBSTRING(voucher-no,1,LENGTH(voucher-no) - 1).
                                END.
                                ELSE descr1 = billjournal.bezeich.
                                /* Dzikri - FO Ticket 10/10/2024 -END */
                            END. 
                        END.
                 
                        /*M 020412 -> contain long descr */ /*ITA 080713 -> add IF available output-list*/
                        IF AVAILABLE output-list THEN
                            ASSIGN
                                output-list.descr = STRING(descr1, "x(100)")
                                output-list.voucher = STRING(voucher-no, "x(40)").  /*MT 03/12/13 */
                        IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */ THEN
                        DO:
                            output-list.zinr = billjournal.zinr.
                            output-list.deptno = billjournal.departement. 
            
                            IF NOT long-digit THEN STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(descr1, "x(50)") 
                                + STRING(hoteldpt.depart, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>") /* Malik 2A7616 : "", "x(6)" -> billjournal.betriebsnr, ">>>>>>" */
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
                            ELSE STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(descr1, "x(50)") 
                                + STRING(hoteldpt.depart, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>") /* Malik 2A7616 : "", "x(6)" -> billjournal.betriebsnr, ">>>>>>" */
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
                            qty = qty + billjournal.anzahl.
                            gqty = gqty + billjournal.anzahl. 
                            IF foreign-flag THEN 
                            DO: 
                                sub-tot = sub-tot + billjournal.fremdwaehrng. 
                                tot = tot + billjournal.fremdwaehrng. 
                            END. 
                            ELSE DO: 
                              sub-tot = sub-tot + billjournal.betrag. 
                              tot = tot + billjournal.betrag. 
                            END. 
                        END.
                        ELSE IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN
                        DO:
                            output-list.zinr = billjournal.zinr.
                            output-list.deptno = billjournal.departement. 
            
                            IF NOT long-digit THEN STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(descr1, "x(50)") 
                                + STRING(hoteldpt.depart, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>")
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
                            ELSE STR = STRING(bill-datum) 
                                + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                + STRING(billjournal.rechnr, "999999999") 
                                + STRING(billjournal.artnr, "9999") 
                                + STRING(descr1, "x(50)") 
                                + STRING(hoteldpt.depart, "x(12)") 
                                + STRING(billjournal.betriebsnr, ">>>>>>")
                                + STRING(billjournal.anzahl, "-9999") 
                                + STRING(amount, "->>,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                                + STRING(zeit, "HH:MM:SS") 
                                + STRING(billjournal.userinit,"x(4)") 
                                + STRING(billjournal.sysdate)
                                + STRING(voucher-no, "x(24)"). 
                            qty = qty + billjournal.anzahl.
                            gqty = gqty + billjournal.anzahl. 
                            IF foreign-flag THEN 
                            DO: 
                                sub-tot = sub-tot + billjournal.fremdwaehrng. 
                                tot = tot + billjournal.fremdwaehrng. 
                            END. 
                            ELSE DO: 
                              sub-tot = sub-tot + billjournal.betrag. 
                              tot = tot + billjournal.betrag. 
                            END. 
                        END.
                        /* Dzikri B8BF2D 22/10/2024 - get adult amount instead of bill amount if dayuse reservation for POS/outlet bill */
                        IF AVAILABLE res-line AND res-line.ankunft EQ res-line.abreise AND artikel.departement GT 0 THEN 
                        DO:
                            qty = qty - billjournal.anzahl + res-line.erwachs.
                            gqty = gqty - billjournal.anzahl + res-line.erwachs. 
                            temp-str = SUBSTRING(STR,101).
                            STR = SUBSTRING(STR,1,95).
                            STR = STR + STRING(res-line.erwachs, "-9999") + temp-str.
                            temp-str = "".
                        END.
                        /* Dzikri B8BF2D 22/10/2024 - END*/
                    END. /*if do-it*/
                END. /*each billjournal*/
            ELSE IF sorttype = 2 THEN 
            DO: 
                IF mi-post = YES THEN 
                    FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
                        AND billjournal.departement = artikel.departement 
                        AND bill-datum = curr-date AND billjournal.anzahl EQ 0 NO-LOCK BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
                        it-exist = YES.
                        do-it = YES.
                        IF (mi-onlyjournal EQ YES AND billjournal.bediener-nr EQ 0) OR (mi-excljournal EQ YES AND billjournal.bediener-nr NE 0) THEN /* Dzikri - CA8E6D */
                        DO:
                            do-it = NO.
                        END.
                        IF exclude-ARTrans AND billjournal.kassarapport THEN do-it = NO.
                        IF NOT mi-showrelease AND billjournal.betrag = 0 THEN do-it = NO.
                        IF do-it THEN
                        DO:
                            CREATE output-list. 
                            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO) OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO) THEN
                            DO:
                                output-list.remark = billjournal.stornogrund.
                            END.
        
                            IF NOT billjournal.bezeich MATCHES ("*<*") AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
                            DO: 
                                IF billjournal.rechnr GT 0 THEN
                                DO:
                                    FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                                    IF AVAILABLE bill AND billjournal.zinr NE "" THEN
                                    DO:
                                        FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr AND res-line.zinr EQ bill.zinr /* Dzikri - FO Ticket 10/10/2024 : EQ roomnumber */
                                            AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                            NO-LOCK NO-ERROR.
                                        FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                                        FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                        FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR. /* Dzikri - FO Ticket 10/10/2024 */
                                        
                                        IF AVAILABLE guest THEN
                                        DO:
                                            output-list.str        = output-list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1.  
                                            output-list.checkin    = res-line.ankunft. 
                                            output-list.checkout   = res-line.abreise. 
                                            output-list.guestname  = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                            output-list.gname      = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1. /* Dzikri - FO Ticket 10/10/2024 */
                                            
                                            FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
                                            IF AVAILABLE segment THEN output-list.segcode = segment.bezeich.
                                            ELSE output-list.segcode = "".
                                        END.
                                    END.
                                    ELSE IF AVAILABLE bill THEN
                                    DO: 
                                        IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) 
                                            OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) THEN
                                        DO: 
                                            IF bill.resnr = 0 AND bill.bilname NE "" THEN 
                                            DO:
                                                output-list.gname = bill.bilname.   
                                                output-list.guestname = bill.bilname.
                                            END.                            
                                            ELSE
                                            DO: 
                                                FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                                                IF AVAILABLE gbuff THEN
                                                DO:
                                                    output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                                    output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                                END. 
                                            END.
                                        END.
                                    END.
                                END.
                                ELSE
                                DO:
                                    IF artikel.artart = 5 AND INDEX(billjournal.bezeich," [#") GT 0 AND billjournal.departement = 0 THEN
                                    DO:
                                        lviresnr = -1.
                                        lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich,"[#") + 2).
                                        lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
                                        FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE reservation THEN
                                        DO:
                                            FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                            IF AVAILABLE gbuff THEN 
                                            DO:
                                                output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                                output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            END.                    
                                        END.
                                    END.
                                    ELSE IF INDEX(billjournal.bezeich," #") GT 0 AND billjournal.departement = 0 THEN
                                    DO:
                                        lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich," #") + 2).
                                        lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                                        FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE reservation THEN
                                        DO:
                                            FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                            IF AVAILABLE gbuff THEN 
                                            DO:
                                                output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                                output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            END.                  
                                        END.
                                    END.
                                END. /*else billjournal Le 0 */
                            END.  /*IF NOT billjournal.bezeich MATCHES ("*<*") AND NOT billjournal.bezeich MATCHES ("*>*") THEN */
                            ELSE
                            DO:
        
                            END.
                
                            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO AND billjournal.anzahl = 0) 
                            OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO AND billjournal.anzahl = 0) THEN output-list.bezeich = artikel.bezeich. 
            
                            IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO THEN 
                            ASSIGN
                                output-list.shift = STRING(billjournal.betriebsnr, "99")
                                output-list.c = STRING(billjournal.betriebsnr,"99"). 
                            ELSE IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO  THEN   
                            DO: 
                                IF AVAILABLE bill THEN 
                                DO: 
                                    IF bill.reslinnr = 1 AND bill.zinr = "" THEN 
                                    ASSIGN
                                    output-list.c = "N"
                                    output-list.NS = "*". 
                                    ELSE IF bill.reslinnr = 0 THEN 
                                    ASSIGN
                                    output-list.c = "M"
                                    output-list.MB = "*". 
                                END. 
                            END. 
             
                            IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
                            ELSE amount = billjournal.betrag. 
                            IF mi-break = YES THEN 
                            DO:
                                ASSIGN
                                  serv        = 0
                                  vat         = 0
                                .
            
                                RUN calc-servvat.p (artikel.departement, artikel.artnr, billjournal.bill-datum,
                                                    artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                                ASSIGN 
                                      output-list.amt-nett = amount / (1 + serv + vat)
                                      output-list.service  = output-list.amt-nett * serv
                                      output-list.vat      = output-list.amt-nett * vat
                                      t-amt                = t-amt + output-list.amt-nett
                                      t-vat                = t-vat + output-list.vat
                                      t-service            = t-service + output-list.service
                                      tot-amt              = tot-amt + output-list.amt-nett
                                      tot-vat              = tot-vat + output-list.vat
                                      tot-service          = tot-service + output-list.service
                                  .                        
                            END.
            
                            ASSIGN 
                            descr1 = ""
                            voucher-no = "".
                            IF SUBSTR(billjournal.bezeich, 1, 1) = "*" OR billjournal.kassarapport THEN
                            ASSIGN
                                descr1 = billjournal.bezeich
                                voucher-no = "".
                            ELSE
                            DO:
                                IF NOT artikel.bezaendern THEN
                                DO:
                                    /* Dzikri - FO Ticket 10/10/2024 */
                                    ind = NUM-ENTRIES(billjournal.bezeich, "]").
                                    IF ind GE 2 THEN gdelimiter = "]".
                                    ELSE
                                    DO:
                                        ind = NUM-ENTRIES(billjournal.bezeich, "/").
                                        IF ind GE 2 AND LENGTH(artikel.bezeich) LE INDEX(billjournal.bezeich, "/") AND billjournal.betrag NE 0 THEN gdelimiter = "/".
                                        ELSE
                                        DO:
                                            ind = NUM-ENTRIES(billjournal.bezeich, "|").
                                            IF ind GE 2 THEN gdelimiter = "|".
                                        END.
                                    END.
                                    /* Dzikri - FO Ticket 10/10/2024 - END */
                                    IF ind NE 0 THEN
                                    DO: 
                                        /*
                                        IF ind GT LENGTH(artikel.bezeich) THEN
                                            ASSIGN
                                            descr1 = ENTRY(1, billjournal.bezeich, gdelimiter)
                                            voucher-no = SUBSTRING(billjournal.bezeich, (ind + 1)).
                                        ELSE
                                        DO:
                                            cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                                            DO i = 1 TO cnt:
                                                IF descr1 = "" THEN descr1 = ENTRY(i, billjournal.bezeich, gdelimiter).    
                                                ELSE descr1 = descr1 + "/" + ENTRY(i, billjournal.bezeich, gdelimiter).
                                            END.
                                            voucher-no = SUBSTR(billjournal.bezeich, LENGTH(descr1) + 2). 
                                        END.
                                        IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                        */
                                        IF ind EQ 1 THEN
                                            ASSIGN
                                            descr1 = billjournal.bezeich
                                            voucher-no = "".
                                        ELSE IF ind EQ 2 THEN
                                        DO:
                                        ASSIGN 
                                            descr1 = ENTRY(1, billjournal.bezeich, gdelimiter) 
                                            voucher-no = ENTRY(2, billjournal.bezeich, gdelimiter).
                                        IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                        END.
                                        ELSE IF ind GT 2  THEN
                                        DO:
                                            voucher-no = "".
                                            descr1 = ENTRY(1, billjournal.bezeich, gdelimiter).
                                            DO loopind = 2 TO ind:
                                                voucher-no = voucher-no + ENTRY(loopind, billjournal.bezeich, gdelimiter) + gdelimiter.
                                            END.
                                            voucher-no = SUBSTRING(voucher-no,1,LENGTH(voucher-no) - 1).
                                        END.
                                    END.
                                    ELSE descr1 = billjournal.bezeich.
                                END.
                                ELSE /*M 110112 -> got voucher info if desc contains "/" */
                                DO:
                                    ind = NUM-ENTRIES(billjournal.bezeich, "/").
                                    IF ind EQ 1 THEN
                                        ASSIGN 
                                            descr1 = billjournal.bezeich
                                            voucher-no = "".
                                    ELSE IF ind EQ 2 THEN
                                        ASSIGN 
                                            descr1 = ENTRY(1, billjournal.bezeich, "/") 
                                            voucher-no = ENTRY(2, billjournal.bezeich, "/").
                                    /* Dzikri - FO Ticket 10/10/2024 */
                                    ELSE IF ind GT 2 THEN
                                    DO:
                                        descr1 = ENTRY(1, billjournal.bezeich, "/").
                                        DO loopind = 2 TO ind:
                                            voucher-no = voucher-no + ENTRY(loopind, billjournal.bezeich, "/") + "/".
                                        END.
                                        voucher-no = SUBSTRING(voucher-no,1,LENGTH(voucher-no) - 1).
                                    END.
                                    ELSE descr1 = billjournal.bezeich.
                                    /* Dzikri - FO Ticket 10/10/2024 -END */
                                END. 
                            END.
            
                            /*M 020412 -> contain long descr */ /*ITA 080713 -> add IF available output-list*/
                            IF AVAILABLE output-list THEN
                            ASSIGN
                                output-list.descr = STRING(descr1, "x(100)")
                                output-list.voucher = STRING(voucher-no, "x(40)").  /*MT 03/12/13 */
                            IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */ THEN
                            DO:
                                output-list.zinr = billjournal.zinr.
                                output-list.deptno = billjournal.departement. 

                                IF NOT long-digit THEN STR = STRING(bill-datum) 
                                    + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                    + STRING(billjournal.rechnr, "999999999") 
                                    + STRING(billjournal.artnr, "9999") 
                                    + STRING(descr1, "x(50)") 
                                    + STRING(hoteldpt.depart, "x(12)") 
                                    + STRING(billjournal.betriebsnr, ">>>>>>") /* Malik 2A7616 : "", "x(6)" -> billjournal.betriebsnr, ">>>>>>" */
                                    + STRING(billjournal.anzahl, "-9999") 
                                    + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                                    + STRING(zeit, "HH:MM:SS") 
                                    + STRING(billjournal.userinit,"x(4)") 
                                    + STRING(billjournal.sysdate)
                                    + STRING(voucher-no, "x(24)")
                                    . 
                                ELSE STR = STRING(bill-datum) 
                                    + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                    + STRING(billjournal.rechnr, "999999999") 
                                    + STRING(billjournal.artnr, "9999") 
                                    + STRING(descr1, "x(50)") 
                                    + STRING(hoteldpt.depart, "x(12)") 
                                    + STRING(billjournal.betriebsnr, ">>>>>>") /* Malik 2A7616 : "", "x(6)" -> billjournal.betriebsnr, ">>>>>>" */
                                    + STRING(billjournal.anzahl, "-9999") 
                                    + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                                    + STRING(zeit, "HH:MM:SS") 
                                    + STRING(billjournal.userinit,"x(4)") 
                                    + STRING(billjournal.sysdate)
                                    + STRING(voucher-no, "x(24)").
                                qty = qty + billjournal.anzahl. 
                                gqty = gqty + billjournal.anzahl. 
                                IF foreign-flag THEN 
                                DO: 
                                    sub-tot = sub-tot + billjournal.fremdwaehrng. 
                                    tot = tot + billjournal.fremdwaehrng. 
                                END. 
                                ELSE 
                                DO: 
                                    sub-tot = sub-tot + billjournal.betrag. 
                                    tot = tot + billjournal.betrag. 
                                END. 
                            END.
                            ELSE IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN
                            DO:
                                output-list.zinr = billjournal.zinr.
                                output-list.deptno = billjournal.departement. 

                                IF NOT long-digit THEN STR = STRING(bill-datum) 
                                    + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                    + STRING(billjournal.rechnr, "999999999") 
                                    + STRING(billjournal.artnr, "9999") 
                                    + STRING(descr1, "x(50)") 
                                    + STRING(hoteldpt.depart, "x(12)") 
                                    + STRING(billjournal.betriebsnr, ">>>>>>")
                                    + STRING(billjournal.anzahl, "-9999") 
                                    + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                                    + STRING(zeit, "HH:MM:SS") 
                                    + STRING(billjournal.userinit,"x(4)") 
                                    + STRING(billjournal.sysdate)
                                    + STRING(voucher-no, "x(24)")
                                    . 
                                ELSE STR = STRING(bill-datum) 
                                    + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                                    + STRING(billjournal.rechnr, "999999999") 
                                    + STRING(billjournal.artnr, "9999") 
                                    + STRING(descr1, "x(50)") 
                                    + STRING(hoteldpt.depart, "x(12)") 
                                    + STRING(billjournal.betriebsnr, ">>>>>>")
                                    + STRING(billjournal.anzahl, "-9999") 
                                    + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/ 
                                    + STRING(zeit, "HH:MM:SS") 
                                    + STRING(billjournal.userinit,"x(4)") 
                                    + STRING(billjournal.sysdate)
                                    + STRING(voucher-no, "x(24)").
                                qty = qty + billjournal.anzahl. 
                                gqty = gqty + billjournal.anzahl. 
                                IF foreign-flag THEN 
                                DO: 
                                    sub-tot = sub-tot + billjournal.fremdwaehrng. 
                                    tot = tot + billjournal.fremdwaehrng. 
                                END. 
                                ELSE 
                                DO: 
                                    sub-tot = sub-tot + billjournal.betrag. 
                                    tot = tot + billjournal.betrag. 
                                END. 
                            END.
                            /* Dzikri B8BF2D 22/10/2024 - get adult amount instead of bill amount if dayuse reservation for POS/outlet bill */
                            IF AVAILABLE res-line AND res-line.ankunft EQ res-line.abreise AND artikel.departement GT 0 THEN 
                            DO:
                                qty = qty - billjournal.anzahl + res-line.erwachs.
                                gqty = gqty - billjournal.anzahl + res-line.erwachs. 
                                temp-str = SUBSTRING(STR,101).
                                STR = SUBSTRING(STR,1,95).
                                STR = STR + STRING(res-line.erwachs, "-9999") + temp-str.
                                temp-str = "".
                            END.
                            /* Dzikri B8BF2D 22/10/2024 - END*/
                        END. /*if do-it*/
                    END. /*each billjournal*/
                ELSE 
                    FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
                        AND billjournal.departement = artikel.departement 
                        AND billjournal.sysdate = curr-date AND billjournal.anzahl EQ 0 NO-LOCK BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
                        it-exist = YES. 
                        do-it = YES.
                        IF (mi-onlyjournal EQ YES AND billjournal.bediener-nr EQ 0) OR (mi-excljournal EQ YES AND billjournal.bediener-nr NE 0) THEN /* Dzikri - CA8E6D */
                        DO:
                            do-it = NO.
                        END.
                        IF exclude-ARTrans AND billjournal.kassarapport THEN do-it = NO.
                        IF NOT mi-showrelease AND billjournal.betrag = 0 THEN do-it = NO.
                        IF do-it THEN
                        DO:
                            CREATE output-list. 
                            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO) OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO) THEN
                            DO:
                                output-list.remark = billjournal.stornogrund.
                            END.
                            IF NOT billjournal.bezeich MATCHES ("*<*") AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
                            DO:
                                FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                                IF AVAILABLE bill AND billjournal.zinr NE "" THEN
                                DO:
                                    FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr AND res-line.zinr EQ bill.zinr /* Dzikri - FO Ticket 10/10/2024 : EQ roomnumber */
                                        AND res-line.ankunft LE billjournal.bill-datum AND res-line.abreise GE billjournal.bill-datum /* Dzikri 553DE9, B2F161 - Wrong reservation data if longterm and group reservation */ 
                                        NO-LOCK NO-ERROR.
                                    FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                                    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                                    FIND FIRST buffguest WHERE buffguest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR. /* Dzikri - FO Ticket 10/10/2024 */
                                    
                                    IF AVAILABLE guest THEN
                                    DO:
                                        output-list.str        = output-list.str + guest.name + ", " + guest.vorname1 + " " + guest.anrede1.  
                                        output-list.checkin    = res-line.ankunft. 
                                        output-list.checkout   = res-line.abreise. 
                                        output-list.guestname  = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                                        output-list.gname      = buffguest.name + ", " + buffguest.vorname1 + " " + buffguest.anrede1. /* Dzikri - FO Ticket 10/10/2024 */
                                        
                                        FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
                                        IF AVAILABLE segment THEN output-list.segcode = segment.bezeich.
                                        ELSE output-list.segcode = "".
                                    END.
                                END.
                                ELSE IF AVAILABLE bill THEN
                                DO:
                                    IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO) OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO) THEN
                                    DO:
                                        IF bill.resnr = 0 AND bill.bilname NE "" THEN 
                                        DO:
                                            output-list.gname = bill.bilname.        
                                            output-list.guestname = bill.bilname.
                                        END.                             
                                        ELSE
                                        DO:
                                            FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                                            IF AVAILABLE gbuff THEN
                                            DO:
                                                output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                                output-list.guestname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                            END. 
                                        END.
                                    END.
                                END.
                            END.
                            /*
                            ELSE
                            DO:

                            END.
                            */
    
                            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO AND billjournal.anzahl = 0) 
                                OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO AND billjournal.anzahl = 0 ) THEN output-list.bezeich = artikel.bezeich. 
                                
                                IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO THEN 
                                ASSIGN
                                output-list.shift = STRING(billjournal.betriebsnr,"99")
                                output-list.c = STRING(billjournal.betriebsnr,"99"). 
                            ELSE IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO THEN    
                            DO: 
                                IF AVAILABLE bill THEN 
                                DO: 
                                    IF bill.reslinnr = 1 AND bill.zinr = "" THEN 
                                    ASSIGN
                                        output-list.NS = "*"
                                        output-list.c = "N". 
                                    ELSE IF bill.reslinnr = 0 THEN 
                                    ASSIGN
                                        output-list.c = "M"
                                        output-list.MB = "*". 
                                END. 
                            END. 
                            IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
                            ELSE amount = billjournal.betrag. 

                            IF mi-break = YES THEN 
                            DO:
                                ASSIGN
                                  serv        = 0
                                  vat         = 0
                                .
                            
                                RUN calc-servvat.p (artikel.departement, artikel.artnr, billjournal.bill-datum,
                                                    artikel.service-code, artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                                ASSIGN 
                                      output-list.amt-nett = amount / (1 + serv + vat)
                                      output-list.service  = output-list.amt-nett * serv
                                      output-list.vat      = output-list.amt-nett * vat
                                      t-amt                = t-amt + output-list.amt-nett
                                      t-vat                = t-vat + output-list.vat
                                      t-service            = t-service + output-list.service
                                      tot-amt              = tot-amt + output-list.amt-nett
                                      tot-vat              = tot-vat + output-list.vat
                                      tot-service          = tot-service + output-list.service
                                  .                        
                            END.
    
                            ASSIGN 
                                descr1 = ""
                                voucher-no = "".
                            IF SUBSTR(billjournal.bezeich, 1, 1) = "*" OR billjournal.kassarapport THEN
                            ASSIGN
                                descr1 = billjournal.bezeich
                                voucher-no = "".
                            ELSE
                            DO:
                                IF NOT artikel.bezaendern THEN
                                DO:
                                    /* Dzikri - FO Ticket 10/10/2024 */
                                    ind = NUM-ENTRIES(billjournal.bezeich, "]").
                                    IF ind GE 2 THEN gdelimiter = "]".
                                    ELSE
                                    DO:
                                        ind = NUM-ENTRIES(billjournal.bezeich, "/").
                                        IF ind GE 2 AND LENGTH(artikel.bezeich) LE INDEX(billjournal.bezeich, "/") AND billjournal.betrag NE 0 THEN gdelimiter = "/".
                                        ELSE
                                        DO:
                                            ind = NUM-ENTRIES(billjournal.bezeich, "|").
                                            IF ind GE 2 THEN gdelimiter = "|".
                                        END.
                                    END.
                                    /* Dzikri - FO Ticket 10/10/2024 - END */
                                    IF ind NE 0 THEN
                                    DO: 
                                        /*
                                        IF ind GT LENGTH(artikel.bezeich) THEN
                                            ASSIGN
                                            descr1 = ENTRY(1, billjournal.bezeich, gdelimiter)
                                            voucher-no = SUBSTRING(billjournal.bezeich, (ind + 1)).
                                        ELSE
                                        DO:
                                            cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                                            DO i = 1 TO cnt:
                                                IF descr1 = "" THEN descr1 = ENTRY(i, billjournal.bezeich, gdelimiter).    
                                                ELSE descr1 = descr1 + "/" + ENTRY(i, billjournal.bezeich, gdelimiter).
                                            END.
                                            voucher-no = SUBSTR(billjournal.bezeich, LENGTH(descr1) + 2). 
                                        END.
                                        IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                        */
                                        IF ind EQ 1 THEN
                                            ASSIGN
                                            descr1 = billjournal.bezeich
                                            voucher-no = "".
                                        ELSE IF ind EQ 2 THEN
                                        DO:
                                        ASSIGN 
                                            descr1 = ENTRY(1, billjournal.bezeich, gdelimiter) 
                                            voucher-no = ENTRY(2, billjournal.bezeich, gdelimiter).
                                        IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                        END.
                                        ELSE IF ind GT 2  THEN
                                        DO:
                                            voucher-no = "".
                                            descr1 = ENTRY(1, billjournal.bezeich, gdelimiter).
                                            DO loopind = 2 TO ind:
                                                voucher-no = voucher-no + ENTRY(loopind, billjournal.bezeich, gdelimiter) + gdelimiter.
                                            END.
                                            voucher-no = SUBSTRING(voucher-no,1,LENGTH(voucher-no) - 1).
                                        END.
                                    END.
                                    ELSE descr1 = billjournal.bezeich.
                                END.
                                ELSE /*M 110112 -> got voucher info if desc contains "/" */
                                DO:
                                    ind = NUM-ENTRIES(billjournal.bezeich, "/").
                                    IF ind EQ 1 THEN
                                        ASSIGN 
                                            descr1 = billjournal.bezeich
                                            voucher-no = "".
                                    ELSE IF ind EQ 2 THEN
                                        ASSIGN 
                                            descr1 = ENTRY(1, billjournal.bezeich, "/") 
                                            voucher-no = ENTRY(2, billjournal.bezeich, "/").
                                    /* Dzikri - FO Ticket 10/10/2024 */
                                    ELSE IF ind GT 2 THEN
                                    DO:
                                        descr1 = ENTRY(1, billjournal.bezeich, "/").
                                        DO loopind = 2 TO ind:
                                            voucher-no = voucher-no + ENTRY(loopind, billjournal.bezeich, "/") + "/".
                                        END.
                                        voucher-no = SUBSTRING(voucher-no,1,LENGTH(voucher-no) - 1).
                                    END.
                                    ELSE descr1 = billjournal.bezeich.
                                    /* Dzikri - FO Ticket 10/10/2024 -END */
                                END. 
                            END.
     
                            /*M 020412 -> contain long descr */ /*ITA 080713 -> add IF available output-list*/
                            IF AVAILABLE output-list THEN
                            ASSIGN
                            output-list.descr = STRING(descr1, "x(100)")
                            output-list.voucher = STRING(voucher-no, "x(40)").  /*MT 03/12/13 */
                            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO) OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO) THEN
                            DO:
                                output-list.zinr = billjournal.zinr.
                                output-list.deptno = billjournal.departement. 

                                IF NOT long-digit THEN STR = STRING(bill-datum) 
                                    + STRING(billjournal.zinr, "x(6)")     /*MT 25/07/12 */
                                    + STRING(billjournal.rechnr, "999999999") 
                                    + STRING(billjournal.artnr, "9999") 
                                    + STRING(billjournal.bezeich, "x(50)") 
                                    + STRING(hoteldpt.depart, "x(12)") 
                                    + STRING(billjournal.betriebsnr, ">>>>>>") /* Malik 2A7616 : "", "x(6)" -> billjournal.betriebsnr, ">>>>>>" */
                                    + STRING(billjournal.anzahl, "-9999") 
                                    + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                                    + STRING(zeit, "HH:MM:SS") 
                                    + STRING(billjournal.userinit,"x(4)") 
                                    + STRING(billjournal.sysdate). 
                                ELSE STR = STRING(bill-datum) 
                                    + STRING(billjournal.zinr, "x(6)")     /*MT 25/07/12 */
                                    + STRING(billjournal.rechnr, "999999999") 
                                    + STRING(billjournal.artnr, "9999") 
                                    + STRING(billjournal.bezeich, "x(50)") 
                                    + STRING(hoteldpt.depart, "x(12)") 
                                    + STRING(billjournal.betriebsnr, ">>>>>>") /* Malik 2A7616 : "", "x(6)" -> billjournal.betriebsnr, ">>>>>>" */
                                    + STRING(billjournal.anzahl, "-9999") 
                                    + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                                    + STRING(zeit, "HH:MM:SS") 
                                    + STRING(billjournal.userinit,"x(4)") 
                                    + STRING(billjournal.sysdate). 
                                qty = qty + billjournal.anzahl. 
                                gqty = gqty + billjournal.anzahl. 
                                IF foreign-flag THEN 
                                DO: 
                                    sub-tot = sub-tot + billjournal.fremdwaehrng. 
                                    tot = tot + billjournal.fremdwaehrng. 
                                END. 
                                ELSE 
                                DO: 
                                    sub-tot = sub-tot + billjournal.betrag. 
                                    tot = tot + billjournal.betrag. 
                                END. 
                            END.
                            ELSE IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN
                            DO: 
                                output-list.zinr = billjournal.zinr.
                                output-list.deptno = billjournal.departement. 

                                IF NOT long-digit THEN STR = STRING(bill-datum) 
                                    + STRING(billjournal.zinr, "x(6)")     /*MT 25/07/12 */
                                    + STRING(billjournal.rechnr, "999999999") 
                                    + STRING(billjournal.artnr, "9999") 
                                    + STRING(billjournal.bezeich, "x(50)") 
                                    + STRING(hoteldpt.depart, "x(12)") 
                                    + STRING(billjournal.betriebsnr, ">>>>>>")
                                    + STRING(billjournal.anzahl, "-9999") 
                                    + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                                    + STRING(zeit, "HH:MM:SS") 
                                    + STRING(billjournal.userinit,"x(4)") 
                                    + STRING(billjournal.sysdate). 
                                ELSE STR = STRING(bill-datum) 
                                    + STRING(billjournal.zinr, "x(6)")     /*MT 25/07/12 */
                                    + STRING(billjournal.rechnr, "999999999") 
                                    + STRING(billjournal.artnr, "9999") 
                                    + STRING(billjournal.bezeich, "x(50)") 
                                    + STRING(hoteldpt.depart, "x(12)") 
                                    + STRING(billjournal.betriebsnr, ">>>>>>")
                                    + STRING(billjournal.anzahl, "-9999") 
                                    + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                                    + STRING(zeit, "HH:MM:SS") 
                                    + STRING(billjournal.userinit,"x(4)") 
                                    + STRING(billjournal.sysdate). 
                                qty = qty + billjournal.anzahl. 
                                gqty = gqty + billjournal.anzahl. 
                            
                                IF foreign-flag THEN 
                                DO: 
                                    sub-tot = sub-tot + billjournal.fremdwaehrng. 
                                    tot = tot + billjournal.fremdwaehrng. 
                                END. 
                                ELSE 
                                DO: 
                                    sub-tot = sub-tot + billjournal.betrag. 
                                    tot = tot + billjournal.betrag. 
                                END. 
                            END.
                            /* Dzikri B8BF2D 22/10/2024 - get adult amount instead of bill amount if dayuse reservation for POS/outlet bill */
                            IF AVAILABLE res-line AND res-line.ankunft EQ res-line.abreise AND artikel.departement GT 0 THEN 
                            DO:
                                qty = qty - billjournal.anzahl + res-line.erwachs.
                                gqty = gqty - billjournal.anzahl + res-line.erwachs. 
                                temp-str = SUBSTRING(STR,101).
                                STR = SUBSTRING(STR,1,95).
                                STR = STR + STRING(res-line.erwachs, "-9999") + temp-str.
                                temp-str = "".
                            END.
                            /* Dzikri B8BF2D 22/10/2024 - END*/
                        END. /*do-it*/
                    END. /*each billjournal*/
            END. /*if sorttype = 2*/
        END. 
        IF it-exist AND qty NE 0 THEN 
        DO: 
            CREATE output-list. 
            IF NOT long-digit THEN 
            DO:
                STR = STRING("", "x(77)")     /*MT 28/11/12 */
                    + STRING("T O T A L   ", "x(12)") 
                    + STRING("", "x(6)")
                    + STRING(qty, "-9999") 
                    + STRING(sub-tot, "->>,>>>,>>>,>>>,>>9.99"). 
    
                output-list.amt-nett = t-amt.
                output-list.service  = t-service.
                output-list.vat      = t-vat.

                t-amt     = 0.
                t-service = 0.
                t-vat     = 0.
            END.
            ELSE  
            DO:
                STR = STRING("", "x(77)")   /*MT 28/11/12 */
                    + STRING("T O T A L   ", "x(12)") 
                    + STRING("", "x(6)")
                    + STRING(qty, "-9999") 
                    + STRING(sub-tot, "->,>>>,>>>,>>>,>>>,>>9").
    
                output-list.amt-nett = t-amt.
                output-list.service  = t-service.
                output-list.vat      = t-vat.

                t-amt     = 0.
                t-service = 0.
                t-vat     = 0.
            END.
        END.
    END.

    CREATE output-list. 
    IF NOT long-digit THEN 
        ASSIGN STR = STRING("", "x(77)") /*MT 28/11/12 */
                + STRING("Grand TOTAL ", "x(12)") 
                + STRING("", "x(6)")
                + STRING(gqty, "-9999") 
                + STRING(tot, "->>,>>>,>>>,>>>,>>9.99")

               output-list.amt-nett = tot-amt
               output-list.service  = tot-service
               output-list.vat      = tot-vat. 
    ELSE 
       ASSIGN STR = STRING("", "x(77)")    /*MT 28/11/12 */
                + STRING("Grand TOTAL ", "x(12)") 
                + STRING("", "x(6)")
                + STRING(gqty, "-9999") 
                + STRING(tot, "->,>>>,>>>,>>>,>>>,>>9")

              output-list.amt-nett = tot-amt
              output-list.service  = tot-service
              output-list.vat      = tot-vat
           . /*IT 130513*/ 
    gtot = tot. 
END. 

