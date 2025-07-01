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
    FIELD segcode     AS CHAR FORMAT "X(20)" LABEL "SegmentCode" /*william 28/6/23 BA598B add segmentcode*/.

/**/
DEFINE TEMP-TABLE t-billjournal LIKE billjournal.

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
DEFINE INPUT PARAMETER mi-showrelease    AS LOGICAL. /*gerald show-hide release AR F2C3AB*/

DEFINE OUTPUT PARAMETER gtot            AS DECIMAL INITIAL 0. 
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
/**/
    /*
DEFINE VAR from-art         AS INTEGER.
DEFINE VAR to-art           AS INTEGER.
DEFINE VAR from-dept        AS INTEGER.
DEFINE VAR to-dept          AS INTEGER.
DEFINE VAR from-date        AS DATE.
DEFINE VAR to-date          AS DATE.
DEFINE VAR sorttype         AS INTEGER.
DEFINE VAR exclude-ARTrans  AS LOGICAL.
DEFINE VAR long-digit       AS LOGICAL.
DEFINE VAR foreign-flag     AS LOGICAL.
DEFINE VAR mi-onlyjournal   AS LOGICAL.
DEFINE VAR mi-excljournal   AS LOGICAL.
DEFINE VAR mi-post          AS LOGICAL.
DEFINE VAR mi-showrelease   AS LOGICAL. /*gerald show-hide release AR F2C3AB*/
DEFINE VAR gtot             AS DECIMAL INITIAL 0. 

from-art        = 1.
to-art          = 9999.
from-dept       = 0.
to-dept         = 0.
from-date       = 02/07/23.
to-date         = 02/14/23.
sorttype        = 0.
exclude-ARTrans = YES.
long-digit      = NO.
foreign-flag    = NO.
mi-onlyjournal  = NO.
mi-excljournal  = NO.
mi-post         = NO.
mi-showrelease  = YES.
*/

DEFINE VARIABLE curr-date  AS DATE.
DEFINE VARIABLE descr1     AS CHAR    NO-UNDO.
DEFINE VARIABLE voucher-no AS CHAR    NO-UNDO.
DEFINE VARIABLE ind        AS INTEGER NO-UNDO.
DEFINE VARIABLE gdelimiter AS CHAR    NO-UNDO.
DEFINE VARIABLE roomnumber AS CHAR NO-UNDO.
DEFINE VARIABLE zinrdate   AS DATE NO-UNDO.
DEFINE VARIABLE billnumber AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-str   AS CHAR NO-UNDO.
DEFINE VARIABLE curr-resnr AS INTEGER NO-UNDO.

IF from-date EQ ? THEN RETURN.
IF to-date EQ ? THEN RETURN.

/*MASDOD 290124 stuck trace*/
FOR EACH billjournal WHERE billjournal.departement GE from-dept
    AND billjournal.departement LE to-dept 
    AND billjournal.bill-datum GE from-date
    AND billjournal.bill-datum LE to-date
    AND billjournal.anzahl NE 0 NO-LOCK BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
    CREATE t-billjournal.
    BUFFER-COPY billjournal TO t-billjournal.
END.


RUN journal-list.

/*MASDOD 09022023 benerin ticket dari nopla + riven*/
DEF VAR lvcs AS CHAR.
FIND FIRST output-list NO-LOCK NO-ERROR.
DO WHILE AVAILABLE output-list:
    IF output-list.MB EQ "*" AND roomnumber EQ "" THEN
    DO:
        ASSIGN
            output-list.guestname   = ""
            output-list.segcode     = "".
    END.
    ELSE IF output-list.shift NE "" THEN
    DO:
        ASSIGN
            output-list.checkin     = ?
            output-list.checkout    = ?
            output-list.guestname   = ""
            output-list.segcode     = "".
    END.
    FIND NEXT output-list NO-LOCK NO-ERROR.
END.

/*************** PROCEDURES ***************/

PROCEDURE journal-list: 
    DEFINE VARIABLE qty       AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
    DEFINE VARIABLE sub-tot   AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE tot       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE curr-date AS DATE. 
    DEFINE VARIABLE last-dept AS INTEGER INITIAL -1. 
    DEFINE VARIABLE it-exist  AS LOGICAL. 
    DEFINE VARIABLE lviresnr  AS INTEGER INITIAL -1 NO-UNDO.
    DEFINE VARIABLE lvcs      AS CHAR               NO-UNDO.
    DEFINE VARIABLE amount    AS DECIMAL NO-UNDO. 
    DEFINE VARIABLE s         AS CHAR NO-UNDO.
    DEFINE VARIABLE cnt       AS INTEGER NO-UNDO.
    DEFINE VARIABLE i         AS INTEGER NO-UNDO.
    DEFINE VARIABLE gqty      AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
    DEFINE VARIABLE do-it     AS LOGICAL INITIAL YES.  
    DEFINE VARIABLE deptname  AS CHAR INITIAL "" NO-UNDO.
    
    DEFINE BUFFER gbuff FOR guest.
 
    EMPTY TEMP-TABLE output-list.
 
    FOR EACH artikel WHERE artikel.artnr GE from-art AND artikel.artnr LE to-art 
        AND artikel.departement GE from-dept 
        AND artikel.departement LE to-dept NO-LOCK BY (artikel.departement * 10000 + artikel.artnr): 
        IF last-dept NE artikel.departement THEN FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-LOCK NO-ERROR. 
        last-dept   = artikel.departement. 
        sub-tot     = 0. 
        it-exist    = NO. 
        qty         = 0. 
        DO curr-date = from-date TO to-date: 
            IF sorttype = 0 THEN 
            FOR EACH t-billjournal WHERE t-billjournal.artnr = artikel.artnr 
                AND t-billjournal.departement = artikel.departement 
                AND bill-datum = curr-date AND t-billjournal.anzahl NE 0 NO-LOCK BY t-billjournal.sysdate BY t-billjournal.zeit BY t-billjournal.zinr: 
                it-exist    = YES. 
                do-it       = YES.
                IF exclude-ARTrans AND t-billjournal.kassarapport THEN do-it = NO.
                IF NOT mi-showrelease AND t-billjournal.betrag = 0 THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */) OR
                       (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */) THEN
                    DO:
                        CREATE output-list. 
                        output-list.remark = t-billjournal.stornogrund.
                    END.                                                                                   

                    IF NOT t-billjournal.bezeich MATCHES ("*<*") AND NOT t-billjournal.bezeich MATCHES ("*>*") THEN 
                    DO: 
                        IF t-billjournal.rechnr GT 0 THEN
                        DO:
                            /** 01 April 2010 -- display opt, by MD */
                            IF t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */ THEN
                            DO:
                                /** DISP 0 t-billjournal.betriebsnr. PAUSE. */
                                FIND FIRST bill WHERE bill.rechnr = t-billjournal.rechnr NO-LOCK NO-ERROR. 
                                IF AVAILABLE bill THEN
                                DO:
                                    IF bill.resnr = 0 AND bill.bilname NE "" THEN DO:
                                         output-list.gname = bill.bilname.
                                    END.                         
                                    ELSE
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.                            
                                        END.
                                    END.
                                END.   /*available bill*/
                            END. /*bediener-nr = 0*/
                            ELSE IF t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */ THEN
                            DO:
                                /** DISP 1 t-billjournal.betriebsnr. PAUSE. */
                                /*NEW  APRIL 14, 2009, BY LN --> WRONG GUESTNAME IF TRANSACTION CAME FROM OUTLETS*/
                                FIND FIRST h-bill WHERE h-bill.rechnr = t-billjournal.rechnr AND h-bill.departement = t-billjournal.betriebsnr NO-LOCK NO-ERROR.
                                IF AVAILABLE h-bill THEN 
                                DO:
                                    output-list.gname = h-bill.bilname. /* tidak */                       
                                END.
                            END.
                        END. /*rechnr GT 0*/
                        ELSE
                        DO:
                            IF INDEX(t-billjournal.bezeich," *BQT") GT 0 THEN
                            DO: 
                                FIND FIRST bk-veran WHERE bk-veran.veran-nr = INTEGER(SUBSTR(t-billjournal.bezeich,INDEX(t-billjournal.bezeich," *BQT") + 5)) NO-LOCK NO-ERROR.
                                IF AVAILABLE bk-veran THEN
                                DO: 
                                    FIND FIRST gbuff WHERE gbuff.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE gbuff THEN 
                                    DO:
                                        output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                    END.                    
                                END.
                            END.
                            ELSE IF artikel.artart = 5 AND INDEX(t-billjournal.bezeich," [#") GT 0 AND t-billjournal.departement = 0 THEN
                            DO:
                                lviresnr = -1.
                                lvcs     = SUBSTR(t-billjournal.bezeich, INDEX(t-billjournal.bezeich,"[#") + 2).
                                lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
                                FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                IF AVAILABLE reservation THEN
                                DO:
                                    FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE gbuff THEN 
                                    DO:
                                        output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.
                                    END.                    
                                END.
                            END.
                            ELSE IF INDEX(t-billjournal.bezeich," #") GT 0 AND t-billjournal.departement = 0 THEN
                            DO:
                                lvcs     = SUBSTR(t-billjournal.bezeich, INDEX(t-billjournal.bezeich," #") + 2).
                                lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                                FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                IF AVAILABLE reservation THEN
                                DO: 
                                    FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE gbuff THEN 
                                    DO:
                                        output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.                        
                                    END.                    
                                END.
                            END.
                        END.
                    END.
                    ELSE
                    DO:
                        /*
                        FIND FIRST h-bill WHERE h-bill.rechnr = t-billjournal.rechnr AND h-bill.departement = t-billjournal.betriebsnr NO-LOCK NO-ERROR.
                        IF AVAILABLE h-bill THEN output-list.gname = h-bill.bilname.
                        */
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
                                    FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE res-line THEN
                                    DO:
                                        ASSIGN
                                            output-list.guestname = res-line.NAME
                                            output-list.gname     = h-bill.bilname.
                                        FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
                                        /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                           /* william 28/06/23             */
                                        FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                               /* add segment code description */
                                        IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                             /* BA598B                       */
                                        ELSE output-list.segcode   = segment.bezeich.
                                    END.                            
                                END.
                                ELSE IF h-bill.resnr GT 0 THEN
                                DO:
                                    FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE guest THEN
                                    ASSIGN
                                        output-list.guestname = guest.NAME + "," + guest.vorname1
                                        output-list.gname     = h-bill.bilname.
                                    FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                               /* add segment code description */
                                    IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                              /* BA598B                       */
                                    ELSE output-list.segcode   = segment.bezeich.
                                END.
                                ELSE IF h-bill.resnr = 0 THEN
                                DO:
                                    ASSIGN
                                        output-list.guestname = h-bill.bilname
                                        output-list.gname     = h-bill.bilname.
                                    FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                               /* add segment code description */
                                    IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                              /* BA598B                       */
                                    ELSE output-list.segcode   = segment.bezeich.
                                END.
                            END.
                        END.
                        ELSE
                        DO:
                            FIND FIRST argt-line WHERE argt-line.argt-artnr EQ artikel.artnr AND argt-line.departement EQ artikel.departement NO-LOCK NO-ERROR.
                            IF AVAILABLE argt-line THEN
                            DO:
                                FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr 
                                    AND h-bill.departement = billjournal.departement NO-LOCK NO-ERROR.
                                IF AVAILABLE h-bill THEN
                                DO:
                                    IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                                    DO:
                                        FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE res-line THEN
                                        DO:
                                            ASSIGN
                                                output-list.guestname = res-line.NAME
                                                output-list.gname     = h-bill.bilname.
        
                                            FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr NO-LOCK NO-ERROR.               
                                            /*FIND FIRST guestseg WHERE guestseg.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR. */                                            /* william 28/06/23             */
                                            FIND FIRST segment WHERE segment.segmentcode EQ genstat.segmentcode NO-LOCK NO-ERROR.                                                /* add segment code description */
                                            IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                              /* BA598B                       */
                                            ELSE output-list.segcode   = segment.bezeich.
                                        END.                            
                                    END.
                                    ELSE IF h-bill.resnr GT 0 THEN
                                    DO:
                                        FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE guest THEN
                                        ASSIGN
                                            output-list.guestname = guest.NAME + "," + guest.vorname1
                                            output-list.gname     = h-bill.bilname.
                                        FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                               /* add segment code description */
                                        IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                              /* BA598B                       */
                                        ELSE output-list.segcode   = segment.bezeich.
                                    END.
                                    ELSE IF h-bill.resnr = 0 THEN
                                    DO:
                                        ASSIGN
                                            output-list.guestname = h-bill.bilname
                                            output-list.gname     = h-bill.bilname.
                                        FIND FIRST segment WHERE segment.segmentcode EQ h-bill.segmentcode NO-LOCK NO-ERROR.                                               /* add segment code description */
                                        IF NOT AVAILABLE segment THEN output-list.segcode = "".                                                                              /* BA598B                       */
                                        ELSE output-list.segcode   = segment.bezeich.
                                    END.
                                END.
                            END.
                        END.
                    END.
            
                    IF (t-billjournal.bediener-nr NE 0 
                        AND mi-excljournal = NO 
                        AND t-billjournal.anzahl = 0) /** AND t-billjournal.bediener NE 0 */ OR (t-billjournal.bediener-nr = 0 
                        AND mi-onlyjournal = NO 
                        AND t-billjournal.anzahl = 0) /** AND t-billjournal.bediener EQ 0 */ THEN output-list.bezeich = artikel.bezeich. 
            
                    IF t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */ THEN
                    DO:
                        ASSIGN 
                        output-list.c     = STRING(t-billjournal.betriebsnr,"99")
                        output-list.shift = STRING(t-billjournal.betriebsnr, "99"). 
                    END.
                    ELSE IF t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */ THEN 
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
           
                    IF foreign-flag THEN amount = t-billjournal.fremdwaehrng. 
                    ELSE amount = t-billjournal.betrag. 
 
                    descr1     = "".
                    voucher-no = "".
        
                    IF SUBSTR(t-billjournal.bezeich, 1, 1) = "*" OR t-billjournal.kassarapport THEN
                    ASSIGN
                        descr1     = t-billjournal.bezeich
                        voucher-no = "".
                    ELSE
                    DO:
                        IF NOT artikel.bezaendern THEN
                        DO:
                            ind = INDEX(t-billjournal.bezeich, "/").
                            IF ind NE 0 THEN gdelimiter = "/".
                            ELSE
                            DO:
                                ind = INDEX(t-billjournal.bezeich, "]").
                                IF ind NE 0 THEN gdelimiter = "]".
                            END.
                            IF ind NE 0 THEN
                            DO: 
                                IF ind GT LENGTH(artikel.bezeich) THEN
                                    ASSIGN
                                        descr1 = ENTRY(1, t-billjournal.bezeich, gdelimiter)
                                        voucher-no = SUBSTRING(t-billjournal.bezeich, (ind + 1)).
                                ELSE
                                DO:
                                    cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                                    DO i = 1 TO cnt:
                                        IF descr1 = "" THEN
                                            descr1 = ENTRY(i, t-billjournal.bezeich, gdelimiter).    
                                        ELSE descr1 = descr1 + "/" + ENTRY(i, t-billjournal.bezeich, gdelimiter).
                                    END.
                                    voucher-no = SUBSTR(t-billjournal.bezeich, LENGTH(descr1) + 2). 
                
                                    /*descr1 = t-billjournal.bezeich.*/
                                END.
                                IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                            END.
                            ELSE descr1 = t-billjournal.bezeich.
                        END.
                        ELSE /*M 110112 -> got voucher info if desc contains "/" */
                        DO:
                            ind = INDEX(t-billjournal.bezeich, "/").
                            IF ind NE 0 THEN gdelimiter = "/".
                            ELSE
                            DO:
                                ind = INDEX(t-billjournal.bezeich, "]").
                                IF ind NE 0 THEN gdelimiter = "]".
                            END.
                            IF ind NE 0 THEN
                            DO: 
                                IF ind GT LENGTH(artikel.bezeich) THEN
                                    ASSIGN
                                        descr1 = ENTRY(1, t-billjournal.bezeich, gdelimiter)
                                        voucher-no = SUBSTRING(t-billjournal.bezeich, (ind + 1)).
                                ELSE
                                DO:
                                    cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                                    IF cnt GT NUM-ENTRIES(t-billjournal.bezeich, gdelimiter) THEN
                                    DO:
                                        IF NUM-ENTRIES(t-billjournal.bezeich, gdelimiter) GT 1 THEN
                                            cnt = NUM-ENTRIES(t-billjournal.bezeich, gdelimiter) - 1.
                                        ELSE
                                            cnt = NUM-ENTRIES(t-billjournal.bezeich, gdelimiter).
                                    END.
                                    DO i = 1 TO cnt:
                                        IF descr1 = "" THEN
                                            descr1 = ENTRY(i, t-billjournal.bezeich, gdelimiter).    
                                        ELSE descr1 = descr1 + "/" + ENTRY(i, t-billjournal.bezeich, gdelimiter).
                                    END.
                                    voucher-no = SUBSTR(t-billjournal.bezeich, LENGTH(descr1) + 2). 
                
                                    /*descr1 = t-billjournal.bezeich.*/
                                END.
                                IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                            END.
                            ELSE descr1 = t-billjournal.bezeich.
                            /*IF t-billjournal.bezeich MATCHES "*//*" THEN
                            DO:
                                ind = NUM-ENTRIES(t-billjournal.bezeich, "/").
                                /*MNaufal - bugs fix field tidak muncul tetapi recordnya ada */
                                IF ind LE 1 THEN    /*change from EQ 1*/
                                    ASSIGN descr1     = t-billjournal.bezeich
                                           voucher-no = "".
                                ELSE
                                    ASSIGN descr1     = ENTRY(1, t-billjournal.bezeich, "/")  /*change from ind - 1*/
                                           voucher-no = ENTRY(2, t-billjournal.bezeich, "/"). /*change from ind*/
                                
                                IF descr1 EQ "" OR descr1 EQ " " THEN
                                    descr1 = artikel.bezeich.
                            END.
                            /*MNAUFAL - move update from #wen*/
                            ELSE IF t-billjournal.bezeich MATCHES "*]*" THEN
                            DO:
                                ind = NUM-ENTRIES(t-billjournal.bezeich, "]").
                                /*MNaufal - bugs fix field tidak muncul tetapi recordnya ada */
                                IF ind LE 1 THEN    /*change from EQ 1*/
                                    ASSIGN descr1     = t-billjournal.bezeich
                                           voucher-no = "".
                                ELSE
                                    ASSIGN descr1     = ENTRY(1, t-billjournal.bezeich, "]")  /*change from ind - 1*/
                                           voucher-no = ENTRY(2, t-billjournal.bezeich, "]"). /*change from ind*/ 
                                
                                IF descr1 EQ "" OR descr1 EQ " " THEN descr1 = artikel.bezeich.
                            END.
                            ELSE DO:
                                ASSIGN 
                                    descr1     = t-billjournal.bezeich
                                    voucher-no = "".
                                IF descr1 EQ "" OR descr1 EQ " " THEN descr1 = artikel.bezeich.
                            END.*/
                        END. 
                        /*
                        /*wen*/
                        IF artikel.bezaendern THEN 
                        DO:
                            
                        END.
                        */
                    END. 
                    /*M 020412 -> contain long descr*/ /*ITA 080713 -> add IF available output-list*/
                    IF AVAILABLE output-list THEN
                    ASSIGN
                        output-list.descr = STRING(descr1, "x(100)")
                        output-list.voucher = STRING(voucher-no, "x(20)").  /*MT 03/12/13 */
                    IF t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */ THEN
                    DO:
                        FIND FIRST hoteldpt WHERE hoteldpt.num = t-billjournal.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.
        
                        IF NOT long-digit THEN STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)") /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(deptname, "x(12)") 
                            + STRING("", "x(6)")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)"). 
                        ELSE STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(t-billjournal.bezeich, "x(50)") 
                            + STRING(deptname, "x(12)") 
                            + STRING("", "x(6)")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)"). 
    
                        qty = qty + t-billjournal.anzahl. 
                        gqty = gqty + t-billjournal.anzahl. 
                /*      IF t-billjournal.anzahl NE 0 THEN  */ 
                        DO: 
                            IF foreign-flag THEN 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.fremdwaehrng. 
                                tot = tot + t-billjournal.fremdwaehrng. 
                            END. 
                            ELSE 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.betrag. 
                                tot = tot + t-billjournal.betrag. 
                            END. 
                        END. 
                    END.
                    ELSE IF t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */ THEN
                    DO:
                        FIND FIRST hoteldpt WHERE hoteldpt.num = t-billjournal.departement NO-LOCK NO-ERROR.
                        IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.
        
                        IF NOT long-digit THEN STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(deptname, "x(12)") 
                            + STRING(t-billjournal.betriebsnr, ">>>>>>")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)"). 
                        ELSE STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(t-billjournal.bezeich, "x(50)") 
                            + STRING(deptname, "x(12)") 
                            + STRING(t-billjournal.betriebsnr, ">>>>>>")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)"). 
        
                        qty = qty + t-billjournal.anzahl. 
                        gqty = gqty + t-billjournal.anzahl. 
                /*      IF t-billjournal.anzahl NE 0 THEN  */ 
                        DO: 
                            IF foreign-flag THEN 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.fremdwaehrng. 
                                tot = tot + t-billjournal.fremdwaehrng. 
                            END. 
                            ELSE 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.betrag. 
                                tot = tot + t-billjournal.betrag. 
                            END. 
                        END. 
                    END.
                END. /*if do-it*/
                RUN add-field.
            END. /*each t-billjournal*/
            ELSE IF sorttype = 1 THEN 
            FOR EACH t-billjournal WHERE t-billjournal.artnr = artikel.artnr 
                AND t-billjournal.departement = artikel.departement 
                AND t-billjournal.bill-datum = curr-date NO-LOCK BY t-billjournal.sysdate BY t-billjournal.zeit BY t-billjournal.zinr: 
                it-exist = YES. 
                do-it    = YES.
                IF exclude-ARTrans AND t-billjournal.kassarapport THEN do-it = NO.
                IF NOT mi-showrelease AND t-billjournal.betrag = 0 THEN do-it = NO.
                IF do-it  THEN
                DO:
                    IF (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */) OR 
                       (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */) THEN
                    DO:
                        CREATE output-list. 
                        output-list.remark = t-billjournal.stornogrund.
                    END.
                    IF NOT t-billjournal.bezeich MATCHES ("*<*") AND NOT t-billjournal.bezeich MATCHES ("*>*") THEN 
                    DO: 
                        IF t-billjournal.rechnr GT 0 THEN
                        DO:
                            FIND FIRST bill WHERE bill.rechnr = t-billjournal.rechnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE bill THEN
                            DO:
                                IF (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */) OR 
                                  (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */) THEN
                                DO:
                                    IF bill.resnr = 0 AND bill.bilname NE "" THEN 
                                    DO:
                                        output-list.gname = bill.bilname.                            
                                    END.                          
                                    ELSE
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.                            
                                        END.
                                    END.
                                END.
                            END.
                        END.
                        ELSE
                        DO:
                            IF artikel.artart = 5 AND INDEX(t-billjournal.bezeich," [#") GT 0 AND t-billjournal.departement = 0 THEN
                            DO:
                                lviresnr = -1.
                                lvcs     = SUBSTR(t-billjournal.bezeich, INDEX(t-billjournal.bezeich,"[#") + 2).
                                lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
                                FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                IF AVAILABLE reservation THEN
                                DO:
                                    FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE gbuff THEN 
                                    DO:
                                        output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.                        
                                    END.                    
                                END.
                            END.
                            ELSE IF INDEX(t-billjournal.bezeich," #") GT 0 AND t-billjournal.departement = 0 THEN
                            DO:
                                lvcs     = SUBSTR(t-billjournal.bezeich, INDEX(t-billjournal.bezeich," #") + 2).
                                lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                                FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                IF AVAILABLE reservation THEN
                                DO:
                                    FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE gbuff THEN 
                                    DO:
                                        output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.                        
                                    END.                    
                                END.
                            END.
                        END.
                    END.
                    ELSE
                    DO:
                        /*
                        FIND FIRST h-bill WHERE h-bill.rechnr = t-billjournal.rechnr AND 
                        h-bill.departement = t-billjournal.betriebsnr NO-LOCK NO-ERROR.
                        IF AVAILABLE h-bill THEN
                        output-list.gname = h-bill.bilname.
                        */
                    END.
                    
                    IF (t-billjournal.bediener-nr NE 0 
                        AND mi-excljournal = NO
                        AND t-billjournal.anzahl = 0 /** AND t-billjournal.bediener NE 0 */) OR (t-billjournal.bediener-nr = 0 
                        AND mi-onlyjournal = NO
                        AND t-billjournal.anzahl = 0 /** AND t-billjournal.bediener EQ 0 */ ) THEN output-list.bezeich = artikel.bezeich. 
                    
                    IF t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */ THEN 
                    ASSIGN
                        output-list.shift = STRING(t-billjournal.betriebsnr,"99")
                        output-list.c = STRING(t-billjournal.betriebsnr,"99"). 
                    ELSE IF t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */ THEN  
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
     
                    IF foreign-flag THEN amount = t-billjournal.fremdwaehrng. 
                    ELSE amount = t-billjournal.betrag. 
            
                    descr1 = "".
                    voucher-no = "".
            
                    IF SUBSTR(t-billjournal.bezeich, 1, 1) = "*" OR t-billjournal.kassarapport THEN
                    ASSIGN
                        descr1 = t-billjournal.bezeich
                        voucher-no = "".
                    ELSE
                    DO:
                        IF NOT artikel.bezaendern THEN
                        DO:
                            ind = INDEX(t-billjournal.bezeich, "/").
                            IF ind NE 0 THEN gdelimiter = "/".
                            ELSE
                            DO:
                                ind = INDEX(t-billjournal.bezeich, "]").
                                IF ind NE 0 THEN gdelimiter = "]".
                            END.
                            IF ind NE 0 THEN
                            DO: 
                                IF ind GT LENGTH(artikel.bezeich) THEN
                                    ASSIGN
                                        descr1 = ENTRY(1, t-billjournal.bezeich, gdelimiter)
                                        voucher-no = SUBSTRING(t-billjournal.bezeich, (ind + 1)).
                                ELSE
                                DO:
                                    cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                                    DO i = 1 TO cnt:
                                        IF descr1 = "" THEN
                                            descr1 = ENTRY(i, t-billjournal.bezeich, gdelimiter).    
                                        ELSE descr1 = descr1 + "/" + ENTRY(i, t-billjournal.bezeich, gdelimiter).
                                    END.
                                    voucher-no = SUBSTR(t-billjournal.bezeich, LENGTH(descr1) + 2). 
                
                                    /*descr1 = t-billjournal.bezeich.*/
                                END.
                                IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                            END.
                            ELSE descr1 = t-billjournal.bezeich.
                        END.
                        ELSE /*M 110112 -> got voucher info if desc contains "/" */
                        DO:
                            ind = NUM-ENTRIES(t-billjournal.bezeich, "/").
                            /*MNaufal - bugs fix field tidak muncul tetapi recordnya ada */
                            IF ind LE 1 THEN    /*change from EQ 1*/
                                ASSIGN descr1     = t-billjournal.bezeich
                                       voucher-no = "".
                            ELSE
                                ASSIGN descr1     = ENTRY(1, t-billjournal.bezeich, "/")  /*change from ind - 1*/ 
                                       voucher-no = ENTRY(2, t-billjournal.bezeich, "/"). /*change from ind*/
        
                            IF descr1 EQ "" OR descr1 EQ " " THEN
                                descr1 = artikel.bezeich.
                        END.                    
                    END.
                    /*M 020412 -> contain long descr */ /*ITA 080713 -> add IF available output-list*/
                    IF AVAILABLE output-list THEN
                        ASSIGN
                            output-list.descr = STRING(descr1, "x(100)")
                            output-list.voucher = STRING(voucher-no, "x(20)").  /*MT 03/12/13 */
                    IF t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */ THEN
                    DO:
                        IF NOT long-digit THEN STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(hoteldpt.depart, "x(12)") 
                            + STRING("", "x(6)")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)"). 
                        ELSE STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(hoteldpt.depart, "x(12)") 
                            + STRING("", "x(6)")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)"). 
                        qty = qty + t-billjournal.anzahl.
                        gqty = gqty + t-billjournal.anzahl. 
                        IF foreign-flag THEN 
                        DO: 
                            sub-tot = sub-tot + t-billjournal.fremdwaehrng. 
                            tot = tot + t-billjournal.fremdwaehrng. 
                        END. 
                        ELSE DO: 
                          sub-tot = sub-tot + t-billjournal.betrag. 
                          tot = tot + t-billjournal.betrag. 
                        END. 
                    END.
                    ELSE IF t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */ THEN
                    DO:
                        IF NOT long-digit THEN STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(hoteldpt.depart, "x(12)") 
                            + STRING(t-billjournal.betriebsnr, ">>>>>>")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)"). 
                        ELSE STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(hoteldpt.depart, "x(12)") 
                            + STRING(t-billjournal.betriebsnr, ">>>>>>")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->>,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)"). 
                        qty = qty + t-billjournal.anzahl.
                        gqty = gqty + t-billjournal.anzahl. 
                        IF foreign-flag THEN 
                        DO: 
                            sub-tot = sub-tot + t-billjournal.fremdwaehrng. 
                            tot = tot + t-billjournal.fremdwaehrng. 
                        END. 
                        ELSE DO: 
                          sub-tot = sub-tot + t-billjournal.betrag. 
                          tot = tot + t-billjournal.betrag. 
                        END. 
                    END.
                END. /*if do-it*/
                RUN add-field.
            END. /*each t-billjournal*/
            ELSE IF sorttype = 2 THEN 
            DO: 
                IF mi-post = YES THEN 
                FOR EACH t-billjournal WHERE t-billjournal.artnr = artikel.artnr 
                    AND t-billjournal.departement = artikel.departement 
                    AND t-billjournal.bill-datum = curr-date AND t-billjournal.anzahl EQ 0 NO-LOCK BY t-billjournal.sysdate BY t-billjournal.zeit BY t-billjournal.zinr: 
                    it-exist = YES.
                    do-it    = YES.
                    IF exclude-ARTrans AND t-billjournal.kassarapport THEN do-it = NO.
                    IF NOT mi-showrelease AND t-billjournal.betrag = 0 THEN do-it = NO.
                    IF do-it THEN
                    DO:
                        IF (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */) 
                            OR (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */) THEN
                        DO:
                            CREATE output-list. 
                            output-list.remark = t-billjournal.stornogrund.
                        END.

                        IF NOT t-billjournal.bezeich MATCHES ("*<*") AND NOT t-billjournal.bezeich MATCHES ("*>*") THEN 
                        DO: 
                            IF t-billjournal.rechnr GT 0 THEN
                            DO:
                                FIND FIRST bill WHERE bill.rechnr = t-billjournal.rechnr NO-LOCK NO-ERROR. 
                                IF AVAILABLE bill THEN
                                DO:
                                    IF (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */) 
                                    OR (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */) THEN
                                    DO:
                                        IF bill.resnr = 0 AND bill.bilname NE "" THEN 
                                        DO:
                                            output-list.gname = bill.bilname.                              
                                        END.                            
                                        ELSE
                                        DO:
                                            FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                                            IF AVAILABLE gbuff THEN
                                            DO:
                                                output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.                              
                                            END.
                                        END.
                                    END.
                                END.
                            END.
                            ELSE
                            DO:
                                IF artikel.artart = 5 AND INDEX(t-billjournal.bezeich," [#") GT 0 AND t-billjournal.departement = 0 THEN
                                DO:
                                    lviresnr = -1.
                                    lvcs     = SUBSTR(t-billjournal.bezeich, INDEX(t-billjournal.bezeich,"[#") + 2).
                                    lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
                                    FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE reservation THEN
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN 
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.                          
                                        END.                      
                                    END.
                                END.
                                ELSE IF INDEX(t-billjournal.bezeich," #") GT 0 AND t-billjournal.departement = 0 THEN
                                DO:
                                    lvcs     = SUBSTR(t-billjournal.bezeich, INDEX(t-billjournal.bezeich," #") + 2).
                                    lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                                    FIND FIRST reservation WHERE reservation.resnr = lviresnr NO-LOCK NO-ERROR.
                                    IF AVAILABLE reservation THEN
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN 
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma.                          
                                        END.                      
                                    END.
                                END.
                            END. /*else t-billjournal Le 0 */
                        END.  /*IF NOT t-billjournal.bezeich MATCHES ("*<*") 
                        AND NOT t-billjournal.bezeich MATCHES ("*>*") THEN */
                        ELSE
                        DO:
                            /* 
                            FIND FIRST h-bill WHERE h-bill.rechnr = t-billjournal.rechnr AND 
                            h-bill.departement = t-billjournal.betriebsnr NO-LOCK NO-ERROR.
                            IF AVAILABLE h-bill THEN
                            output-list.gname = h-bill.bilname.
                            */         
                        END.
                        
                        IF (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO
                        AND t-billjournal.anzahl = 0 /** AND t-billjournal.bediener NE 0 */) OR (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO
                        AND t-billjournal.anzahl = 0 /** AND t-billjournal.bediener EQ 0 */ ) THEN output-list.bezeich = artikel.bezeich. 
                    
                        IF t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */ THEN 
                        ASSIGN
                            output-list.shift = STRING(t-billjournal.betriebsnr, "99")
                            output-list.c = STRING(t-billjournal.betriebsnr,"99"). 
                        ELSE IF t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */ THEN   
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
 
                        IF foreign-flag THEN amount = t-billjournal.fremdwaehrng. 
                        ELSE amount = t-billjournal.betrag. 
                        
                        descr1 = "".
                        voucher-no = "".

                        IF SUBSTR(t-billjournal.bezeich, 1, 1) = "*" OR t-billjournal.kassarapport THEN
                        ASSIGN
                            descr1 = t-billjournal.bezeich
                            voucher-no = "".
                        ELSE
                        DO:
                            IF NOT artikel.bezaendern THEN
                            DO:
                                ind = INDEX(t-billjournal.bezeich, "/").
                                IF ind NE 0 THEN gdelimiter = "/".
                                ELSE
                                DO:
                                    ind = INDEX(t-billjournal.bezeich, "]").
                                    IF ind NE 0 THEN gdelimiter = "]".
                                END.
                                IF ind NE 0 THEN
                                DO: 
                                    IF ind GT LENGTH(artikel.bezeich) THEN
                                        ASSIGN
                                        descr1 = ENTRY(1, t-billjournal.bezeich, gdelimiter)
                                        voucher-no = SUBSTRING(t-billjournal.bezeich, (ind + 1)).
                                    ELSE
                                    DO:
                                        cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                                        DO i = 1 TO cnt:
                                            IF descr1 = "" THEN descr1 = ENTRY(i, t-billjournal.bezeich, gdelimiter).    
                                            ELSE descr1 = descr1 + "/" + ENTRY(i, t-billjournal.bezeich, gdelimiter).
                                        END.
                                        voucher-no = SUBSTR(t-billjournal.bezeich, LENGTH(descr1) + 2). 
                                
                                        /*descr1 = t-billjournal.bezeich.*/
                                    END.
                                    IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                END.
                                ELSE descr1 = t-billjournal.bezeich.
                            END.
                            ELSE /*M 110112 -> got voucher info if desc contains "/" */
                            DO:
                                ind = NUM-ENTRIES(t-billjournal.bezeich, "/").
                                /*MNaufal - bugs fix field tidak muncul tetapi recordnya ada */
                                IF ind LE 1 THEN    /*change from EQ 1*/
                                    ASSIGN descr1     = t-billjournal.bezeich
                                           voucher-no = "".
                                ELSE
                                    ASSIGN descr1     = ENTRY(1, t-billjournal.bezeich, "/")  /*change from ind - 1*/
                                           voucher-no = ENTRY(2, t-billjournal.bezeich, "/"). /*change from ind*/
            
                                IF descr1 EQ "" OR descr1 EQ " " THEN
                                    descr1 = artikel.bezeich.
                            END.                    
                        END.   
                        /*M 020412 -> contain long descr */ /*ITA 080713 -> add IF available output-list*/
                        IF AVAILABLE output-list THEN
                        ASSIGN
                            output-list.descr = STRING(descr1, "x(100)")
                            output-list.voucher = STRING(voucher-no, "x(20)").  /*MT 03/12/13 */
                        IF t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */ THEN
                        DO:
                            IF NOT long-digit THEN STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(hoteldpt.depart, "x(12)") 
                            + STRING("", "x(6)")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)")
                            . 
                            ELSE STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(hoteldpt.depart, "x(12)") 
                            + STRING("", "x(6)")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)").
                            qty = qty + t-billjournal.anzahl. 
                            gqty = gqty + t-billjournal.anzahl. 
                            IF foreign-flag THEN 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.fremdwaehrng. 
                                tot = tot + t-billjournal.fremdwaehrng. 
                            END. 
                            ELSE 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.betrag. 
                                tot = tot + t-billjournal.betrag. 
                            END. 
                        END.
                        ELSE IF t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */ THEN
                        DO:
                            IF NOT long-digit THEN STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(hoteldpt.depart, "x(12)") 
                            + STRING(t-billjournal.betriebsnr, ">>>>>>")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)")
                            . 
                            ELSE STR = STRING(t-billjournal.bill-datum) 
                            + STRING(t-billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                            + STRING(t-billjournal.rechnr, "999999999") 
                            + STRING(t-billjournal.artnr, "9999") 
                            + STRING(descr1, "x(50)") 
                            + STRING(hoteldpt.depart, "x(12)") 
                            + STRING(t-billjournal.betriebsnr, ">>>>>>")
                            + STRING(t-billjournal.anzahl, "-9999") 
                            + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/ 
                            + STRING(t-billjournal.zeit, "HH:MM:SS") 
                            + STRING(t-billjournal.userinit,"x(4)") 
                            + STRING(t-billjournal.sysdate)
                            + STRING(voucher-no, "x(24)").
                            qty = qty + t-billjournal.anzahl. 
                            gqty = gqty + t-billjournal.anzahl. 
                            IF foreign-flag THEN 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.fremdwaehrng. 
                                tot = tot + t-billjournal.fremdwaehrng. 
                            END. 
                            ELSE DO: 
                                sub-tot = sub-tot + t-billjournal.betrag. 
                                tot = tot + t-billjournal.betrag. 
                            END. 
                        END.
                    END. /*if do-it*/
                    RUN add-field.
                END. /*each t-billjournal*/
                ELSE 
                FOR EACH t-billjournal WHERE t-billjournal.artnr = artikel.artnr 
                    AND t-billjournal.departement = artikel.departement 
                    AND t-billjournal.sysdate = curr-date AND t-billjournal.anzahl EQ 0 NO-LOCK BY t-billjournal.sysdate BY t-billjournal.zeit BY t-billjournal.zinr: 
                    it-exist = YES. 
                    do-it    = YES.
                    IF exclude-ARTrans AND t-billjournal.kassarapport THEN do-it = NO.
                    IF NOT mi-showrelease AND t-billjournal.betrag = 0 THEN do-it = NO.
                    IF do-it THEN
                    DO:
                        IF (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */) 
                        OR (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */) THEN
                        DO:
                            CREATE output-list. 
                            output-list.remark = t-billjournal.stornogrund.
                        END.
                        IF NOT t-billjournal.bezeich MATCHES ("*<*") AND NOT t-billjournal.bezeich MATCHES ("*>*") THEN 
                        DO:
                            FIND FIRST bill WHERE bill.rechnr = t-billjournal.rechnr NO-LOCK NO-ERROR. 
                            IF AVAILABLE bill THEN
                            DO:
                                IF (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */) 
                                OR (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */) THEN
                                DO:
                                    IF bill.resnr = 0 AND bill.bilname NE "" THEN 
                                    DO:
                                        output-list.gname = bill.bilname.                                
                                    END.                             
                                    ELSE
                                    DO:
                                        FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                                        IF AVAILABLE gbuff THEN
                                        DO:
                                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma. /* tidak */                               
                                        END.
                                    END.
                                END.
                            END.
                        END.
                        ELSE
                        DO:
                            /*
                            FIND FIRST h-bill WHERE h-bill.rechnr = t-billjournal.rechnr AND 
                            h-bill.departement = t-billjournal.betriebsnr NO-LOCK NO-ERROR.
                            IF AVAILABLE h-bill THEN
                            output-list.gname = h-bill.bilname.
                            */
                        END.
        
                        IF (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO
                        AND t-billjournal.anzahl = 0 /** AND t-billjournal.bediener NE 0 */) OR (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO
                        AND t-billjournal.anzahl = 0 /** AND t-billjournal.bediener EQ 0 */ ) THEN output-list.bezeich = artikel.bezeich. 
                        
                        IF t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */ THEN 
                        ASSIGN
                            output-list.shift = STRING(t-billjournal.betriebsnr,"99")
                            output-list.c     = STRING(t-billjournal.betriebsnr,"99"). 
                        ELSE IF t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */ THEN    
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
         
                        IF foreign-flag THEN amount = t-billjournal.fremdwaehrng. 
                        ELSE amount = t-billjournal.betrag. 
        
                        descr1 = "".
                        voucher-no = "".
         
                        IF SUBSTR(t-billjournal.bezeich, 1, 1) = "*" OR t-billjournal.kassarapport THEN
                        ASSIGN
                            descr1 = t-billjournal.bezeich
                            voucher-no = "".
                        ELSE
                        DO:
                            IF NOT artikel.bezaendern THEN
                            DO:
                                ind = INDEX(t-billjournal.bezeich, "/").
                                IF ind NE 0 THEN gdelimiter = "/".
                                ELSE
                                DO:
                                    ind = INDEX(t-billjournal.bezeich, "]").
                                    IF ind NE 0 THEN gdelimiter = "]".
                                END.
                                IF ind NE 0 THEN
                                DO: 
                                    IF ind GT LENGTH(artikel.bezeich) THEN
                                    ASSIGN
                                    descr1 = ENTRY(1, t-billjournal.bezeich, gdelimiter)
                                    voucher-no = SUBSTRING(t-billjournal.bezeich, (ind + 1)).
                                    ELSE
                                    DO:
                                        cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                                        DO i = 1 TO cnt:
                                            IF descr1 = "" THEN descr1 = ENTRY(i, t-billjournal.bezeich, gdelimiter).    
                                            ELSE descr1 = descr1 + "/" + ENTRY(i, t-billjournal.bezeich, gdelimiter).
                                        END.
                                        voucher-no = SUBSTR(t-billjournal.bezeich, LENGTH(descr1) + 2). 
                                    /*descr1 = t-billjournal.bezeich.*/
                                    END.
                                    IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                                END.
                                ELSE descr1 = t-billjournal.bezeich.
                            END.
                            ELSE /*M 110112 -> got voucher info if desc contains "/" */
                            DO:
                                ind = NUM-ENTRIES(t-billjournal.bezeich, "/").
                                /*MNaufal - bugs fix field tidak muncul tetapi recordnya ada */
                                IF ind LE 1 THEN    /*change from EQ 1*/
                                ASSIGN 
                                    descr1     = t-billjournal.bezeich
                                    voucher-no = "".
                                ELSE
                                ASSIGN 
                                    descr1     = ENTRY(1, t-billjournal.bezeich, "/")    /*change from ind - 1*/
                                    voucher-no = ENTRY(2, t-billjournal.bezeich, "/").   /*change from ind*/
                                
                                IF descr1 EQ "" OR descr1 EQ " " THEN descr1 = artikel.bezeich.
                            END.                    
                        END.
                        
                        /*M 020412 -> contain long descr */ /*ITA 080713 -> add IF available output-list*/
                        IF AVAILABLE output-list THEN
                        ASSIGN
                            output-list.descr = STRING(descr1, "x(100)")
                            output-list.voucher = STRING(voucher-no, "x(20)").  /*MT 03/12/13 */
                        IF (t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */) 
                        OR (t-billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND t-billjournal.bediener EQ 0 */) THEN
                        DO:
                            IF NOT long-digit THEN STR = STRING(t-billjournal.bill-datum) 
                             + STRING(t-billjournal.zinr, "x(6)")     /*MT 25/07/12 */
                             + STRING(t-billjournal.rechnr, "999999999") 
                             + STRING(t-billjournal.artnr, "9999") 
                             + STRING(t-billjournal.bezeich, "x(50)") 
                             + STRING(hoteldpt.depart, "x(12)") 
                             + STRING("", "x(6)")
                             + STRING(t-billjournal.anzahl, "-9999") 
                             + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                             + STRING(t-billjournal.zeit, "HH:MM:SS") 
                             + STRING(t-billjournal.userinit,"x(4)") 
                             + STRING(t-billjournal.sysdate). 
                            ELSE STR = STRING(t-billjournal.bill-datum) 
                             + STRING(t-billjournal.zinr, "x(6)")     /*MT 25/07/12 */
                             + STRING(t-billjournal.rechnr, "999999999") 
                             + STRING(t-billjournal.artnr, "9999") 
                             + STRING(t-billjournal.bezeich, "x(50)") 
                             + STRING(hoteldpt.depart, "x(12)") 
                             + STRING("", "x(6)")
                             + STRING(t-billjournal.anzahl, "-9999") 
                             + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                             + STRING(t-billjournal.zeit, "HH:MM:SS") 
                             + STRING(t-billjournal.userinit,"x(4)") 
                             + STRING(t-billjournal.sysdate). 
                            qty = qty + t-billjournal.anzahl. 
                            gqty = gqty + t-billjournal.anzahl. 
                            IF foreign-flag THEN 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.fremdwaehrng. 
                                tot = tot + t-billjournal.fremdwaehrng. 
                            END. 
                            ELSE 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.betrag. 
                                tot = tot + t-billjournal.betrag. 
                            END. 
                        END.
                        ELSE IF t-billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND t-billjournal.bediener NE 0 */ THEN
                        DO: 
                            IF NOT long-digit THEN STR = STRING(t-billjournal.bill-datum) 
                             + STRING(t-billjournal.zinr, "x(6)")     /*MT 25/07/12 */
                             + STRING(t-billjournal.rechnr, "999999999") 
                             + STRING(t-billjournal.artnr, "9999") 
                             + STRING(t-billjournal.bezeich, "x(50)") 
                             + STRING(hoteldpt.depart, "x(12)") 
                             + STRING(t-billjournal.betriebsnr, ">>>>>>")
                             + STRING(t-billjournal.anzahl, "-9999") 
                             + STRING(amount, "->>,>>>,>>>,>>>,>>9.99") /*IT 130513*/
                             + STRING(t-billjournal.zeit, "HH:MM:SS") 
                             + STRING(t-billjournal.userinit,"x(4)") 
                             + STRING(t-billjournal.sysdate). 
                            ELSE STR = STRING(t-billjournal.bill-datum) 
                             + STRING(t-billjournal.zinr, "x(6)")     /*MT 25/07/12 */
                             + STRING(t-billjournal.rechnr, "999999999") 
                             + STRING(t-billjournal.artnr, "9999") 
                             + STRING(t-billjournal.bezeich, "x(50)") 
                             + STRING(hoteldpt.depart, "x(12)") 
                             + STRING(t-billjournal.betriebsnr, ">>>>>>")
                             + STRING(t-billjournal.anzahl, "-9999") 
                             + STRING(amount, "->,>>>,>>>,>>>,>>>,>>9") /*IT 130513*/
                             + STRING(t-billjournal.zeit, "HH:MM:SS") 
                             + STRING(t-billjournal.userinit,"x(4)") 
                             + STRING(t-billjournal.sysdate). 
                            qty = qty + t-billjournal.anzahl. 
                            gqty = gqty + t-billjournal.anzahl. 
                            IF foreign-flag THEN 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.fremdwaehrng. 
                                tot = tot + t-billjournal.fremdwaehrng. 
                            END. 
                            ELSE 
                            DO: 
                                sub-tot = sub-tot + t-billjournal.betrag. 
                                tot = tot + t-billjournal.betrag. 
                            END. 
                        END.
                    END. /*do-it*/
                    RUN add-field.
                END. /*each t-billjournal*/
            END. /*if sorttype = 2*/
        END. 
        IF it-exist THEN 
        DO: 
            CREATE output-list. 
            IF NOT long-digit THEN 
                STR = STRING("", "x(77)")     /*MT 28/11/12 */
                + STRING("T O T A L   ", "x(12)") 
                + STRING("", "x(6)")
                + STRING(qty, "-9999") 
                + STRING(sub-tot, "->>,>>>,>>>,>>>,>>9.99"). /*IT 130513*/
            ELSE  STR = STRING("", "x(77)")   /*MT 28/11/12 */
                + STRING("T O T A L   ", "x(12)") 
                + STRING("", "x(6)")
                + STRING(qty, "-9999") 
                + STRING(sub-tot, "->,>>>,>>>,>>>,>>>,>>9"). /*IT 130513*/            
        END. 
    END. 
    CREATE output-list. 
    IF NOT long-digit THEN STR = STRING("", "x(77)") /*MT 28/11/12 */
        + STRING("Grand TOTAL ", "x(12)") 
        + STRING("", "x(6)")
        + STRING(gqty, "-9999") 
        + STRING(tot, "->>,>>>,>>>,>>>,>>9.99"). 
    ELSE STR = STRING("", "x(77)")    /*MT 28/11/12 */
        + STRING("Grand TOTAL ", "x(12)") 
        + STRING("", "x(6)")
        + STRING(gqty, "-9999") 
        + STRING(tot, "->,>>>,>>>,>>>,>>>,>>9"). /*IT 130513*/ 
    gtot = tot. 
END.

/*MASDOD 15022023 fixing slow loading*/
PROCEDURE add-field:
    roomnumber = SUBSTRING(output-list.STR,9,6).

    IF t-billjournal.rechnr GT 0 THEN
    DO:
        FIND FIRST bill WHERE bill.rechnr EQ t-billjournal.rechnr NO-LOCK NO-ERROR. 
        IF AVAILABLE bill THEN
        DO:
            IF bill.resnr NE 0 THEN
            DO:
                FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr AND res-line.zinr EQ roomnumber NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                    output-list.checkin   = res-line.ankunft. 
                    output-list.checkout  = res-line.abreise. 
                    output-list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                END.
                ELSE
                DO:
                    FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN
                    DO:
                        FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
                        output-list.checkin   = res-line.ankunft. 
                        output-list.checkout  = res-line.abreise. 
                        output-list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
                    END.
                END.
            END.
        END.
    END.
    ELSE DO:
        IF INDEX(output-list.descr,"[#") GT 0 THEN DO:
            curr-str = SUBSTR(output-list.descr, INDEX(output-list.descr,"[#") + 2).
            curr-resnr = INTEGER(ENTRY(1,curr-str," ")) NO-ERROR.
        END.
        ELSE IF INDEX(output-list.descr," #") GT 0 THEN DO:
            curr-str = SUBSTR(output-list.descr, INDEX(output-list.descr," #") + 2).
            curr-resnr = INTEGER(ENTRY(1,curr-str,"]")) NO-ERROR.
        END.
        FIND FIRST res-line WHERE res-line.resnr EQ curr-resnr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
            output-list.checkin   = res-line.ankunft. 
            output-list.checkout  = res-line.abreise. 
            output-list.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
        END.
    END.
END.
