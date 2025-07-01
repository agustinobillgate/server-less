
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
    FIELD gst         AS DECIMAL.


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

DEFINE OUTPUT PARAMETER gtot            AS DECIMAL INITIAL 0. 
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE curr-date  AS DATE.
DEFINE VARIABLE descr1     AS CHAR    NO-UNDO.
DEFINE VARIABLE voucher-no AS CHAR    NO-UNDO.
DEFINE VARIABLE ind        AS INTEGER NO-UNDO.
DEFINE VARIABLE gdelimiter AS CHAR    NO-UNDO.

RUN journal-list.

/*************** PROCEDURES ***************/

PROCEDURE journal-list: 
DEFINE VARIABLE qty       AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sub-tot   AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE sub-gst   AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE ggst      AS DECIMAL FORMAT "->>>,>>>,>>9.99" INITIAL 0. 
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
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
  FOR EACH artikel WHERE artikel.artnr GE from-art AND artikel.artnr LE to-art 
      AND artikel.departement GE from-dept 
      AND artikel.departement LE to-dept NO-LOCK 
      BY (artikel.departement * 10000 + artikel.artnr): 
    IF last-dept NE artikel.departement THEN 
      FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-LOCK NO-ERROR. 
    last-dept = artikel.departement. 
    sub-tot = 0.
    sub-gst = 0.
    it-exist = NO. 
    qty = 0. 
    DO curr-date = from-date TO to-date: 
      IF sorttype = 0 THEN 
      FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
        AND billjournal.departement = artikel.departement 
        AND bill-datum = curr-date AND billjournal.anzahl NE 0 NO-LOCK 
        BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
        it-exist = YES. 
        do-it = YES.
        IF exclude-ARTrans AND billjournal.kassarapport THEN
            do-it = NO.
        IF do-it THEN
        DO:
            IF (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) OR
               (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) THEN
            DO:
                CREATE output-list. 
                output-list.remark = billjournal.stornogrund.

                IF billjournal.bill-datum GT 08/31/18 THEN DO:
                    IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN DO:
                          IF artikel.artart = 1 THEN 
                              ASSIGN output-list.gst = (billjournal.betrag / 1.06) * (6 / 100).
                          ELSE DO:
                              IF artikel.mwst-code NE 0 THEN 
                                  ASSIGN output-list.gst = (billjournal.betrag / 1.06) * (6 / 100).
                          END.
                          ASSIGN 
                                sub-gst         = sub-gst + output-list.gst
                                ggst            = ggst + output-list.gst.
                    END.
                END.                
            END.           

            
            IF NOT billjournal.bezeich MATCHES ("*<*") 
                AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
            DO: 
              IF billjournal.rechnr GT 0 THEN
              DO:
                  /** 01 April 2010 -- display opt, by MD */
                IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */ THEN
                DO:
                    /** DISP 0 billjournal.betriebsnr. PAUSE. */
                    FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                    IF AVAILABLE bill THEN
                    DO:
                        IF bill.resnr = 0 AND bill.bilname NE "" THEN
                          output-list.gname = bill.bilname.
                        ELSE
                        DO:
                          FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index
                            NO-LOCK NO-ERROR.
                          IF AVAILABLE gbuff THEN
                          DO:
                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                              + gbuff.anrede1 + gbuff.anredefirma.
                          END.
                        END.
                    END.   /*available bill*/
                END. /*bediener-nr = 0*/
                ELSE IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN
                DO:
                    /** DISP 1 billjournal.betriebsnr. PAUSE. */
                    /*NEW  APRIL 14, 2009, BY LN --> WRONG GUESTNAME IF TRANSACTION CAME FROM OUTLETS*/
                    FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND
                        h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
                    IF AVAILABLE h-bill THEN DO:
                       output-list.gname = h-bill.bilname.
                    END.
                END.
              END. /*rechnr GT 0*/
              ELSE
              DO:
               
                IF INDEX(billjournal.bezeich," *BQT") GT 0 THEN
                DO:
                  FIND FIRST bk-veran WHERE bk-veran.veran-nr =
                    INTEGER(SUBSTR(billjournal.bezeich,INDEX(billjournal.bezeich," *BQT") + 5))
                    NO-LOCK NO-ERROR.
                  IF AVAILABLE bk-veran THEN
                  DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr = bk-veran.gastnr
                      NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN
                    output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                      + gbuff.anrede1 + gbuff.anredefirma.
                  END.
                END.
                ELSE
                IF artikel.artart = 5 AND INDEX(billjournal.bezeich," [#") GT 0 
                  AND billjournal.departement = 0 THEN
                DO:
                  lviresnr = -1.
                  lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich,"[#") + 2).
                  lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
                  FIND FIRST reservation WHERE reservation.resnr = lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE reservation THEN
                  DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN
                    output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                      + gbuff.anrede1 + gbuff.anredefirma.
                  END.
                END.
                ELSE IF INDEX(billjournal.bezeich," #") GT 0 
                  AND billjournal.departement = 0 THEN
                DO:
                  lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich," #") + 2).
                  lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                  FIND FIRST reservation WHERE reservation.resnr = lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE reservation THEN
                  DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN
                    output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                      + gbuff.anrede1 + gbuff.anredefirma.
                  END.
                END.
              END.
            END.
            ELSE
            DO:
    /*
                FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND 
                    h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
                IF AVAILABLE h-bill THEN
                    output-list.gname = h-bill.bilname.
    */
            END.
            
            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO AND 
                billjournal.anzahl = 0) /** AND billjournal.bediener NE 0 */ OR
               (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO AND 
                billjournal.anzahl = 0) /** AND billjournal.bediener EQ 0 */ THEN 
                output-list.bezeich = artikel.bezeich. 
            
            IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN
            DO:
              ASSIGN 
                output-list.c = STRING(billjournal.betriebsnr,"99")
                output-list.shift = STRING(billjournal.betriebsnr, "99"). 
            END.
              
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
    
            ASSIGN descr1 = ""
                voucher-no = "".
    
            IF SUBSTR(billjournal.bezeich, 1, 1) = "*" OR 
                billjournal.kassarapport THEN
                ASSIGN
                    descr1 = billjournal.bezeich
                    voucher-no = "".
            ELSE
            DO:
                IF NOT artikel.bezaendern THEN
                DO:
                    ind = INDEX(billjournal.bezeich, "/").
                    IF ind NE 0 THEN gdelimiter = "/".
                    ELSE
                    DO:
                      ind = INDEX(billjournal.bezeich, "]").
                      IF ind NE 0 THEN gdelimiter = "]".
                    END.
                    IF ind NE 0 THEN
                    DO: 
                        IF ind GT LENGTH(artikel.bezeich) THEN
                            ASSIGN
                                descr1 = ENTRY(1, billjournal.bezeich, gdelimiter)
                                voucher-no = SUBSTRING(billjournal.bezeich, (ind + 1)).
                        ELSE
                        DO:
                            cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                            DO i = 1 TO cnt:
                                IF descr1 = "" THEN
                                    descr1 = ENTRY(i, billjournal.bezeich, gdelimiter).    
                                ELSE descr1 = descr1 + "/" + ENTRY(i, billjournal.bezeich, gdelimiter).
                            END.
                            voucher-no = SUBSTR(billjournal.bezeich, LENGTH(descr1) + 2). 
        
                            /*descr1 = billjournal.bezeich.*/
                        END.
                        IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                    END.
                    ELSE descr1 = billjournal.bezeich.
                END.
                ELSE /*M 110112 -> got voucher info if desc contains "/" */
                DO:
                    ind = NUM-ENTRIES(billjournal.bezeich, "/").
                    IF ind EQ 1 THEN
                        ASSIGN descr1 = billjournal.bezeich
                               voucher-no = "".
                    ELSE
                        ASSIGN descr1 = ENTRY(ind - 1, billjournal.bezeich, "/") 
                               voucher-no = ENTRY(ind, billjournal.bezeich, "/").
                END.                    
            END.

            
            /*M 020412 -> contain long descr*/ /*ITA 080713 -> add IF available output-list*/
            IF AVAILABLE output-list THEN
                ASSIGN
                    output-list.descr = STRING(descr1, "x(100)")
                    output-list.voucher = STRING(voucher-no, "x(20)").  /*MT 03/12/13 */
            IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */ THEN
            DO:
                FIND FIRST hoteldpt WHERE hoteldpt.num = billjournal.departement NO-LOCK NO-ERROR.
                IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.

                IF NOT long-digit THEN STR = STRING(bill-datum) 
                    + STRING(billjournal.zinr, "x(6)") /*MT 25/07/12 */
                    + STRING(billjournal.rechnr, "999999999") 
                    + STRING(billjournal.artnr, "9999") 
                    + STRING(descr1, "x(50)") 
                    + STRING(deptname, "x(12)") 
                    + STRING("", "x(6)")
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
                    + STRING("", "x(6)")
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
            ELSE IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN
            DO:
                
                FIND FIRST hoteldpt WHERE hoteldpt.num = billjournal.departement NO-LOCK NO-ERROR.
                IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.

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
        END. /*if do-it*/
      END. /*each billjournal*/
      /****/
      ELSE IF sorttype = 1 THEN 
      FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
        AND billjournal.departement = artikel.departement 
        AND bill-datum = curr-date NO-LOCK 
        BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
        it-exist = YES. 
        do-it = YES.
        IF exclude-ARTrans AND billjournal.kassarapport THEN
            do-it = NO.
        IF do-it  THEN
        DO:
            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) OR 
                (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) THEN
            DO:
                CREATE output-list. 
                output-list.remark = billjournal.stornogrund.
                
                IF billjournal.bill-datum GT 08/31/18 THEN DO:
                    IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN DO:
                          IF artikel.artart = 1 THEN 
                              ASSIGN output-list.gst = (billjournal.betrag / 1.06) * (6 / 100).
                          ELSE DO:
                              IF artikel.mwst-code NE 0 THEN 
                                  ASSIGN output-list.gst = (billjournal.betrag / 1.06) * (6 / 100).
                          END.
                          ASSIGN 
                                sub-gst         = sub-gst + output-list.gst
                                ggst            = ggst + output-list.gst.
                    END.
                END.
            END.
            IF NOT billjournal.bezeich MATCHES ("*<*") 
                AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
            DO: 
              IF billjournal.rechnr GT 0 THEN
              DO:
                FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                IF AVAILABLE bill THEN
                DO:
                    IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) OR 
                        (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) THEN
                    DO:
                        IF bill.resnr = 0 AND bill.bilname NE "" THEN
                          output-list.gname = bill.bilname.
                        ELSE
                        DO:
                          FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index
                            NO-LOCK NO-ERROR.
                          IF AVAILABLE gbuff THEN
                          DO:
                            output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                              + gbuff.anrede1 + gbuff.anredefirma.
                          END.
                        END.
                    END.
                END.
              END.
              ELSE
              DO:
                IF artikel.artart = 5 AND INDEX(billjournal.bezeich," [#") GT 0 
                  AND billjournal.departement = 0 THEN
                DO:
                  lviresnr = -1.
                  lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich,"[#") + 2).
                  lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
                  FIND FIRST reservation WHERE reservation.resnr = lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE reservation THEN
                  DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN
                    output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                      + gbuff.anrede1 + gbuff.anredefirma.
                  END.
                END.
                ELSE IF INDEX(billjournal.bezeich," #") GT 0 
                  AND billjournal.departement = 0 THEN
                DO:
                  lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich," #") + 2).
                  lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                  FIND FIRST reservation WHERE reservation.resnr = lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE reservation THEN
                  DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN
                    output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                      + gbuff.anrede1 + gbuff.anredefirma.
                  END.
                END.
              END.
            END.
            ELSE
            DO:
    /*
               FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND 
                   h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
               IF AVAILABLE h-bill THEN
                   output-list.gname = h-bill.bilname.
    */
            END.
    
            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO
                AND billjournal.anzahl = 0 /** AND billjournal.bediener NE 0 */) 
                OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO
                AND billjournal.anzahl = 0 /** AND billjournal.bediener EQ 0 */ ) THEN 
                output-list.bezeich = artikel.bezeich. 

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
    
            ASSIGN descr1 = ""
                voucher-no = "".
    
            IF SUBSTR(billjournal.bezeich, 1, 1) = "*" OR 
                billjournal.kassarapport THEN
                ASSIGN
                    descr1 = billjournal.bezeich
                    voucher-no = "".
            ELSE
            DO:
                IF NOT artikel.bezaendern THEN
                DO:
                    ind = INDEX(billjournal.bezeich, "/").
                    IF ind NE 0 THEN gdelimiter = "/".
                    ELSE
                    DO:
                      ind = INDEX(billjournal.bezeich, "]").
                      IF ind NE 0 THEN gdelimiter = "]".
                    END.
                    IF ind NE 0 THEN
                    DO: 
                        IF ind GT LENGTH(artikel.bezeich) THEN
                            ASSIGN
                                descr1 = ENTRY(1, billjournal.bezeich, gdelimiter)
                                voucher-no = SUBSTRING(billjournal.bezeich, (ind + 1)).
                        ELSE
                        DO:
                            cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                            DO i = 1 TO cnt:
                                IF descr1 = "" THEN
                                    descr1 = ENTRY(i, billjournal.bezeich, gdelimiter).    
                                ELSE descr1 = descr1 + "/" + ENTRY(i, billjournal.bezeich, gdelimiter).
                            END.
                            voucher-no = SUBSTR(billjournal.bezeich, LENGTH(descr1) + 2). 
        
                            /*descr1 = billjournal.bezeich.*/
                        END.
                        IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                    END.
                    ELSE descr1 = billjournal.bezeich.
                END.
                ELSE /*M 110112 -> got voucher info if desc contains "/" */
                DO:
                    ind = NUM-ENTRIES(billjournal.bezeich, "/").
                    IF ind EQ 1 THEN
                        ASSIGN descr1 = billjournal.bezeich
                               voucher-no = "".
                    ELSE
                        ASSIGN descr1 = ENTRY(ind - 1, billjournal.bezeich, "/") 
                               voucher-no = ENTRY(ind, billjournal.bezeich, "/").
                END.                    
            END.
     
            /*M 020412 -> contain long descr */ /*ITA 080713 -> add IF available output-list*/
            IF AVAILABLE output-list THEN
                ASSIGN
                    output-list.descr = STRING(descr1, "x(100)")
                    output-list.voucher = STRING(voucher-no, "x(20)").  /*MT 03/12/13 */
            IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */ THEN
            DO:
                IF NOT long-digit THEN STR = STRING(bill-datum) 
                    + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                    + STRING(billjournal.rechnr, "999999999") 
                    + STRING(billjournal.artnr, "9999") 
                    + STRING(descr1, "x(50)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING("", "x(6)")
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
                    + STRING("", "x(6)")
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
        END. /*if do-it*/
      END. /*each billjournal*/
      ELSE IF sorttype = 2 THEN 
      DO: 
        IF mi-post = YES THEN 
        FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
          AND billjournal.departement = artikel.departement 
          AND bill-datum = curr-date AND billjournal.anzahl EQ 0 NO-LOCK 
          BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
          it-exist = YES.
          do-it = YES.
          IF exclude-ARTrans AND billjournal.kassarapport THEN
              do-it = NO.
          IF do-it THEN
          DO:
            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) 
                OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) THEN
            DO:
              CREATE output-list. 
              output-list.remark = billjournal.stornogrund.
              
              IF billjournal.bill-datum GT 08/31/18 THEN DO:
                  IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN DO:
                      IF artikel.artart = 1 THEN 
                          ASSIGN output-list.gst = (billjournal.betrag / 1.06) * (6 / 100).
                      ELSE DO:
                          IF artikel.mwst-code NE 0 THEN 
                              ASSIGN output-list.gst = (billjournal.betrag / 1.06) * (6 / 100).
                      END.
                      ASSIGN 
                            sub-gst         = sub-gst + output-list.gst
                            ggst            = ggst + output-list.gst.
                  END.
              END.
            END.

              IF NOT billjournal.bezeich MATCHES ("*<*") 
                  AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
              DO: 
                IF billjournal.rechnr GT 0 THEN
                DO:
                  FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                  IF AVAILABLE bill THEN
                  DO:
                      IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) 
                        OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) THEN
                      DO:
                          IF bill.resnr = 0 AND bill.bilname NE "" THEN
                            output-list.gname = bill.bilname.
                          ELSE
                          DO:
                            FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index
                              NO-LOCK NO-ERROR.
                            IF AVAILABLE gbuff THEN
                            DO:
                              output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                                + gbuff.anrede1 + gbuff.anredefirma.
                            END.
                          END.
                      END.
                  END.
                END.
                ELSE
                DO:
                  IF artikel.artart = 5 AND INDEX(billjournal.bezeich," [#") GT 0 
                    AND billjournal.departement = 0 THEN
                  DO:
                    lviresnr = -1.
                    lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich,"[#") + 2).
                    lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
                    FIND FIRST reservation WHERE reservation.resnr = lviresnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE reservation THEN
                    DO:
                      FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr
                          NO-LOCK NO-ERROR.
                      IF AVAILABLE gbuff THEN
                      output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                        + gbuff.anrede1 + gbuff.anredefirma.
                    END.
                  END.
                  ELSE IF INDEX(billjournal.bezeich," #") GT 0 
                    AND billjournal.departement = 0 THEN
                  DO:
                    lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich," #") + 2).
                    lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                    FIND FIRST reservation WHERE reservation.resnr = lviresnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE reservation THEN
                    DO:
                      FIND FIRST gbuff WHERE gbuff.gastnr = reservation.gastnr
                          NO-LOCK NO-ERROR.
                      IF AVAILABLE gbuff THEN
                      output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                        + gbuff.anrede1 + gbuff.anredefirma.
                    END.
                  END.
                END. /*else billjournal Le 0 */
              END.  /*IF NOT billjournal.bezeich MATCHES ("*<*") 
                  AND NOT billjournal.bezeich MATCHES ("*>*") THEN */
              ELSE
              DO:
    /*
                 FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND 
                     h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
                 IF AVAILABLE h-bill THEN
                     output-list.gname = h-bill.bilname.
    */           
               END.
    
              IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO
                AND billjournal.anzahl = 0 /** AND billjournal.bediener NE 0 */) 
                OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO
                AND billjournal.anzahl = 0 /** AND billjournal.bediener EQ 0 */ ) THEN output-list.bezeich = artikel.bezeich. 

              IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN 
                  ASSIGN
                  output-list.shift = STRING(billjournal.betriebsnr, "99")
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
    
              ASSIGN descr1 = ""
                voucher-no = "".
    
             IF SUBSTR(billjournal.bezeich, 1, 1) = "*" OR 
                 billjournal.kassarapport THEN
                ASSIGN
                    descr1 = billjournal.bezeich
                    voucher-no = "".
             ELSE
             DO:
                IF NOT artikel.bezaendern THEN
                DO:
                    ind = INDEX(billjournal.bezeich, "/").
                    IF ind NE 0 THEN gdelimiter = "/".
                    ELSE
                    DO:
                      ind = INDEX(billjournal.bezeich, "]").
                      IF ind NE 0 THEN gdelimiter = "]".
                    END.
                    IF ind NE 0 THEN
                    DO: 
                        IF ind GT LENGTH(artikel.bezeich) THEN
                            ASSIGN
                                descr1 = ENTRY(1, billjournal.bezeich, gdelimiter)
                                voucher-no = SUBSTRING(billjournal.bezeich, (ind + 1)).
                        ELSE
                        DO:
                            cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                            DO i = 1 TO cnt:
                                IF descr1 = "" THEN
                                    descr1 = ENTRY(i, billjournal.bezeich, gdelimiter).    
                                ELSE descr1 = descr1 + "/" + ENTRY(i, billjournal.bezeich, gdelimiter).
                            END.
                            voucher-no = SUBSTR(billjournal.bezeich, LENGTH(descr1) + 2). 
        
                            /*descr1 = billjournal.bezeich.*/
                        END.
                        IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                    END.
                    ELSE descr1 = billjournal.bezeich.
                END.
                ELSE /*M 110112 -> got voucher info if desc contains "/" */
                DO:
                    ind = NUM-ENTRIES(billjournal.bezeich, "/").
                    IF ind EQ 1 THEN
                        ASSIGN descr1 = billjournal.bezeich
                               voucher-no = "".
                    ELSE
                        ASSIGN descr1 = ENTRY(ind - 1, billjournal.bezeich, "/") 
                               voucher-no = ENTRY(ind, billjournal.bezeich, "/").
                END.                    
             END.
    
             /*M 020412 -> contain long descr */ /*ITA 080713 -> add IF available output-list*/
             IF AVAILABLE output-list THEN
                 ASSIGN
                    output-list.descr = STRING(descr1, "x(100)")
                    output-list.voucher = STRING(voucher-no, "x(20)").  /*MT 03/12/13 */
            IF billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */ THEN
             DO:
                  IF NOT long-digit THEN STR = STRING(bill-datum) 
                    + STRING(billjournal.zinr, "x(6)")  /*MT 25/07/12 */
                    + STRING(billjournal.rechnr, "999999999") 
                    + STRING(billjournal.artnr, "9999") 
                    + STRING(descr1, "x(50)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING("", "x(6)")
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
                    + STRING("", "x(6)")
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
                  ELSE DO: 
                    sub-tot = sub-tot + billjournal.betrag. 
                    tot = tot + billjournal.betrag. 
                  END. 
             END.
          END. /*if do-it*/
        END. /*each billjournal*/
        ELSE 
        FOR EACH billjournal WHERE billjournal.artnr = artikel.artnr 
          AND billjournal.departement = artikel.departement 
          AND billjournal.sysdate = curr-date AND billjournal.anzahl EQ 0 
          NO-LOCK 
          BY billjournal.sysdate BY billjournal.zeit BY billjournal.zinr: 
          it-exist = YES. 
          do-it = YES.
          IF exclude-ARTrans AND billjournal.kassarapport THEN
              do-it = NO.
          IF do-it THEN
          DO:
            IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) 
                OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) THEN
            DO:
                CREATE output-list. 
                output-list.remark = billjournal.stornogrund.
            END.
              IF NOT billjournal.bezeich MATCHES ("*<*") 
                  AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
              DO:
                   FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr NO-LOCK NO-ERROR. 
                   IF AVAILABLE bill THEN
                   DO:
                       IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) 
                        OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) THEN
                       DO:
                           IF bill.resnr = 0 AND bill.bilname NE "" THEN
                             output-list.gname = bill.bilname.
                           ELSE
                           DO:
                             FIND FIRST gbuff WHERE gbuff.gastnr = bill.gastnr USE-INDEX gastnr_index
                               NO-LOCK NO-ERROR.
                             IF AVAILABLE gbuff THEN
                             DO:
                               output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                                 + gbuff.anrede1 + gbuff.anredefirma.
                             END.
                           END.
                       END.
                   END.
               END.
               ELSE
               DO:
    /*
                   FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND 
                       h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
                   IF AVAILABLE h-bill THEN
                       output-list.gname = h-bill.bilname.
    */
              END.
    
              IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO
                  AND billjournal.anzahl = 0 /** AND billjournal.bediener NE 0 */) 
                  OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO
                  AND billjournal.anzahl = 0 /** AND billjournal.bediener EQ 0 */ ) THEN 
                  output-list.bezeich = artikel.bezeich. 

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
    
              ASSIGN descr1 = ""
                voucher-no = "".
     
               IF SUBSTR(billjournal.bezeich, 1, 1) = "*" OR
                   billjournal.kassarapport THEN
                ASSIGN
                    descr1 = billjournal.bezeich
                    voucher-no = "".
               ELSE
               DO:
                  IF NOT artikel.bezaendern THEN
                  DO:
                    ind = INDEX(billjournal.bezeich, "/").
                    IF ind NE 0 THEN gdelimiter = "/".
                    ELSE
                    DO:
                      ind = INDEX(billjournal.bezeich, "]").
                      IF ind NE 0 THEN gdelimiter = "]".
                    END.
                    IF ind NE 0 THEN
                    DO: 
                        IF ind GT LENGTH(artikel.bezeich) THEN
                            ASSIGN
                                descr1 = ENTRY(1, billjournal.bezeich, gdelimiter)
                                voucher-no = SUBSTRING(billjournal.bezeich, (ind + 1)).
                        ELSE
                        DO:
                            cnt = NUM-ENTRIES(artikel.bezeich, gdelimiter).
                            DO i = 1 TO cnt:
                                IF descr1 = "" THEN
                                    descr1 = ENTRY(i, billjournal.bezeich, gdelimiter).    
                                ELSE descr1 = descr1 + "/" + ENTRY(i, billjournal.bezeich, gdelimiter).
                            END.
                            voucher-no = SUBSTR(billjournal.bezeich, LENGTH(descr1) + 2). 
        
                            /*descr1 = billjournal.bezeich.*/
                        END.
                        IF gdelimiter = "]" THEN descr1 = descr1 + gdelimiter.
                    END.
                    ELSE descr1 = billjournal.bezeich.
                  END.
                  ELSE /*M 110112 -> got voucher info if desc contains "/" */
                  DO:
                      ind = NUM-ENTRIES(billjournal.bezeich, "/").
                      IF ind EQ 1 THEN
                          ASSIGN descr1 = billjournal.bezeich
                                 voucher-no = "".
                      ELSE
                          ASSIGN descr1 = ENTRY(ind - 1, billjournal.bezeich, "/") 
                                 voucher-no = ENTRY(ind, billjournal.bezeich, "/").
                  END.                    
               END.
     
               /*M 020412 -> contain long descr */ /*ITA 080713 -> add IF available output-list*/
               IF AVAILABLE output-list THEN
                   ASSIGN
                    output-list.descr = STRING(descr1, "x(100)")
                    output-list.voucher = STRING(voucher-no, "x(20)").  /*MT 03/12/13 */
               IF (billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */) 
                 OR (billjournal.bediener-nr = 0 AND mi-onlyjournal = NO /** AND billjournal.bediener EQ 0 */) THEN
               DO:
                   IF NOT long-digit THEN STR = STRING(bill-datum) 
                     + STRING(billjournal.zinr, "x(6)")     /*MT 25/07/12 */
                     + STRING(billjournal.rechnr, "999999999") 
                     + STRING(billjournal.artnr, "9999") 
                     + STRING(billjournal.bezeich, "x(50)") 
                     + STRING(hoteldpt.depart, "x(12)") 
                     + STRING("", "x(6)")
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
                     + STRING("", "x(6)")
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
                   ELSE DO: 
                     sub-tot = sub-tot + billjournal.betrag. 
                     tot = tot + billjournal.betrag. 
                   END. 
               END.
               ELSE IF billjournal.bediener-nr NE 0 AND mi-excljournal = NO /** AND billjournal.bediener NE 0 */ THEN
               DO: 
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
                   ELSE DO: 
                     sub-tot = sub-tot + billjournal.betrag. 
                     tot = tot + billjournal.betrag. 
                   END. 
               END.
          END. /*do-it*/
        END. /*each billjournal*/
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
            + STRING(sub-tot, "->>,>>>,>>>,>>>,>>>,>>9"). /*IT 130513*/
       ASSIGN output-list.gst = sub-gst.
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
  ASSIGN 
      gtot = tot
      output-list.gst = ggst.

END. 

