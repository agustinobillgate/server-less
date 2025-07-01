

DEFINE TEMP-TABLE bline-list 
  FIELD flag        AS INTEGER INITIAL 0 
  FIELD userinit    LIKE bediener.userinit 
  FIELD selected    AS LOGICAL INITIAL NO 
  FIELD name        LIKE bediener.username 
  FIELD bl-recid    AS INTEGER INITIAL 0. 

DEFINE WORKFILE sum-list 
  FIELD artnr   AS INTEGER 
  FIELD artart  AS INTEGER 
  FIELD bezeich AS CHAR 
  FIELD f-amt   AS DECIMAL 
  FIELD amt     AS DECIMAL. 

DEFINE TEMP-TABLE output-list 
  FIELD flag        AS CHAR 
  FIELD amt-foreign AS DECIMAL 
  FIELD str-foreign AS CHAR FORMAT "x(16)" LABEL "        F-Amount" 
  FIELD STR         AS CHAR
  FIELD gname       AS CHAR FORMAT "x(21)" COLUMN-LABEL "Guest Name". 

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER curr-shift   AS INTEGER.
DEFINE INPUT PARAMETER summary-flag AS LOGICAL.

DEFINE INPUT-OUTPUT PARAMETER from-date  AS DATE.
DEFINE OUTPUT PARAMETER double-currency  AS LOGICAL.
DEFINE OUTPUT PARAMETER foreign-curr     AS CHAR INIT "".

DEFINE INPUT-OUTPUT PARAMETER TABLE FOR bline-list.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE long-digit AS LOGICAL INIT NO NO-UNDO.

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "fo-cashgjourn". 
DEFINE BUFFER usr FOR bediener. 

IF from-date = ? THEN RUN htpdate.p (110, OUTPUT from-date). 

RUN htplogic.p (240, OUTPUT double-currency).
IF double-currency THEN RUN htpchar.p (144, OUTPUT foreign-curr).

IF case-type = 1 THEN RUN cr-bline-list.
ELSE IF case-type = 2 THEN
DO:
  IF curr-shift = 0 THEN RUN journal-list. 
  ELSE RUN journal-list1. 
END.

PROCEDURE cr-bline-list:
    FOR EACH usr WHERE usr.username NE "" 
        AND usr.flag = 0 NO-LOCK BY usr.username: 
      create bline-list. 
      bline-list.userinit = usr.userinit. 
      bline-list.name = usr.username. 
      bline-list.bl-recid = RECID(usr). 
      IF SUBSTR(usr.permissions,8,1) GE "2" THEN bline-list.flag = 1. 
    END. 
END.


PROCEDURE journal-list: 
  DEFINE VARIABLE qty         AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
  DEFINE VARIABLE art-tot     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE art-foreign AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE sub-tot     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE sub-foreign AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE tot         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE tot-foreign AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0. 
  DEFINE VARIABLE curr-art    AS INTEGER. 
  DEFINE VARIABLE curr-date   AS DATE. 
  DEFINE VARIABLE last-dept   AS INTEGER INITIAL -1. 
  DEFINE VARIABLE it-exist    AS LOGICAL INITIAL NO. 
  DEFINE VARIABLE amt         AS DECIMAL. 
  DEFINE VARIABLE tot-cash    AS DECIMAL INITIAL 0  NO-UNDO. 
  DEFINE VARIABLE lviresnr    AS INTEGER INITIAL -1 NO-UNDO.
  DEFINE VARIABLE lvcs        AS CHAR               NO-UNDO.
  DEFINE BUFFER gbuff FOR guest.

  FOR EACH sum-list: 
    delete sum-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
 FOR EACH bline-list WHERE bline-list.selected = YES BY bline-list.name: 
    FIND FIRST bediener WHERE RECID(bediener) = bline-list.bl-recid NO-LOCK NO-ERROR. /* Malik Serverless : NO-LOCK -> NO-LOCK NO-ERROR */ 
    IF AVAILABLE bediener THEN /*Alder - Serverless - Issue 630*/
    DO:
        it-exist = NO. 
        /* Malik Serverless */
        IF NOT summary-flag THEN 
        DO:
            IF AVAILABLE bediener THEN
            DO:
              create output-list. 
              output-list.flag = "*". 
              output-list.STR = STRING("", "x(27)") + 
              STRING((translateExtended("User:",lvCAREA,"") + " " + bediener.username), "x(22)").
            END.
            ELSE
            DO:
              create output-list. 
              output-list.flag = "*". 
              output-list.STR = STRING("", "x(27)") + 
              STRING((translateExtended("User:",lvCAREA,"") + " " + ""), "x(22)"). 
            END.
           
        END.
        /* END Malik */
        sub-tot = 0. 
     
        curr-art = 0. 
        art-tot = 0. 
        art-foreign = 0. 
        FOR EACH artikel WHERE (artikel.artart = 2 OR 
          artikel.artart = 6 OR artikel.artart = 7) 
          AND artikel.departement = 0 NO-LOCK BY artikel.bezeich: 
     
          FIND FIRST sum-list WHERE sum-list.artnr = artikel.artnr NO-ERROR. 
          IF NOT AVAILABLE sum-list THEN 
          DO: 
            CREATE sum-list. 
            ASSIGN 
              sum-list.artnr   = artikel.artnr 
              sum-list.artart  = artikel.artart 
              sum-list.bezeich = artikel.bezeich. 
          END. 
          /* Malik Serverless */
          IF AVAILABLE bediener THEN 
          DO:
            FOR EACH billjournal WHERE billjournal.userinit = bediener.userinit 
              AND billjournal.artnr = artikel.artnr AND billjournal.anzahl NE 0 
              AND billjournal.departement = artikel.departement 
              AND bill-datum = from-date NO-LOCK /*BY billjournal.rechnr 
              BY billjournal.zeit*/ BY billjournal.zeit BY billjournal.rechnr: /*FDL Ticket 97182B*/ 
      
              IF curr-art = 0 THEN curr-art = artikel.artnr. 
              IF curr-art NE artikel.artnr THEN 
              DO: 
                IF NOT summary-flag THEN 
                DO: 
                  create output-list. 
                  output-list.flag = "**". 
                  output-list.amt-foreign = art-foreign. 
                  IF NOT long-digit THEN output-list.STR = STRING("", "x(67)") 
                    + STRING(translateExtended("Sub Total",lvCAREA,""), "x(16)") + " " 
                    + STRING(art-tot, "->,>>>,>>>,>>9.99")
                    + STRING(CHR(10)).    /*MT 20/05/14 */
                  ELSE output-list.STR = STRING("", "x(67)") 
                    + STRING(translateExtended("Sub Total",lvCAREA,""), "x(16)") + " " 
                    + STRING(art-tot, " ->>>,>>>,>>>,>>9")
                    + STRING(CHR(10)).    /*MT 20/05/14 */
                END. 
                art-tot = 0. 
                art-foreign = 0. 
                curr-art = artikel.artnr. 
              END. 
              IF artikel.pricetab OR artikel.betriebsnr NE 0 THEN 
              DO: 
                art-foreign = art-foreign + billjournal.fremdwaehrng. 
                sum-list.f-amt = sum-list.f-amt + billjournal.fremdwaehrng. 
              END. 
              ELSE 
              DO: 
                art-tot = art-tot + billjournal.betrag. 
                sum-list.amt = sum-list.amt + billjournal.betrag. 
              END. 
      
              it-exist = YES. 
              IF last-dept NE billjournal.departement THEN FIND FIRST hoteldpt 
                WHERE hoteldpt.num = billjournal.departement NO-LOCK. 
              last-dept = hoteldpt.num. 
              IF NOT summary-flag THEN 
              DO: 
                create output-list. 
                IF artikel.pricetab OR artikel.betriebsnr NE 0 THEN 
                DO: 
                  amt-foreign = billjournal.fremdwaehrng. 
                  amt = 0. 
                END. 
                ELSE amt = billjournal.betrag. 
                
                IF NOT billjournal.bezeich MATCHES ("*<*") 
                    AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
                DO: 
                    /*MT 26/05/14 */
                    IF billjournal.rechnr GT 0 THEN
                    DO:
                      IF billjournal.bediener-nr = 0 /** AND billjournal.bediener EQ 0 */ THEN
                      DO:
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
                      ELSE IF billjournal.bediener-nr NE 0 THEN
                      DO:
                          FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND
                              h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
                          IF AVAILABLE h-bill THEN DO:
                            output-list.gname = h-bill.bilname.
                          END.
                      END.
                    END.
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
    
                    /*MT 26/05/14
                    IF billjournal.betriebsnr GT 0 THEN /* AR from POS, see rinv-ar.i */ 
                    DO:
                      IF billjournal.rechnr GT 0 THEN
                      DO:
                        FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr 
                            AND h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE h-bill THEN output-list.gname = h-bill.bilname.
                      END.
                    END.
                    ELSE IF billjournal.betriebsnr = 0 THEN /* CL comes from FO */ 
                    DO:
                      IF billjournal.rechnr GT 0 THEN
                      DO:
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
                    */
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
                IF NOT long-digit THEN output-list.STR = STRING(billjournal.bill-datum) 
                          + STRING(billjournal.zinr, "x(6)") 
                          + STRING(billjournal.rechnr, ">>>>>>>>9") 
                          + STRING(billjournal.artnr, "9999") 
                          + STRING(billjournal.bezeich, "x(40)") 
                          + STRING(hoteldpt.depart, "x(17)") 
                          + STRING(amt, "->,>>>,>>>,>>9.99") 
                          + STRING(billjournal.zeit, "HH:MM:SS") 
                          + STRING(bediener.userinit, "x(3)"). 
                ELSE output-list.STR = STRING(billjournal.bill-datum) 
                          + STRING(billjournal.zinr, "x(6)") 
                          + STRING(billjournal.rechnr, ">>>>>>>>9") 
                          + STRING(billjournal.artnr, "9999") 
                          + STRING(billjournal.bezeich, "x(40)") 
                          + STRING(hoteldpt.depart, "x(17)") 
                          + STRING(amt, "->>>>,>>>,>>>,>>9") 
                          + STRING(billjournal.zeit, "HH:MM:SS") 
                          + STRING(bediener.userinit, "x(3)"). 
              END. 
              qty = qty + billjournal.anzahl. 
              IF artikel.pricetab OR artikel.betriebsnr NE 0 THEN 
                sub-foreign = sub-foreign + billjournal.fremdwaehrng. 
              ELSE sub-tot = sub-tot + billjournal.betrag. 
            END.
          END.
          /* END Malik */
     
        END. 
        IF it-exist AND NOT summary-flag THEN 
        DO: 
          create output-list. 
          output-list.flag = "**". 
          output-list.amt-foreign = art-foreign. 
          IF NOT long-digit THEN output-list.STR = STRING("", "x(27)") 
              + STRING(translateExtended("Sub Total",lvCAREA,""), "x(56)") + " " 
              + STRING(art-tot, "->,>>>,>>>,>>9.99")
              + STRING(CHR(10)).    /*MT 20/05/14 */
          ELSE output-list.STR = STRING("", "x(27)") 
              + STRING(translateExtended("Sub Total",lvCAREA,""), "x(56)") + " " 
              + STRING(art-tot, " ->>>,>>>,>>>,>>9")
              + STRING(CHR(10)).    /*MT 20/05/14 */
          tot-foreign = tot-foreign + sub-foreign. 
          tot = tot + sub-tot. 
        END. 
        ELSE IF NOT it-exist AND NOT summary-flag THEN delete output-list. 
    END.
  END. 
  IF NOT summary-flag THEN 
  DO: 
    create output-list. 
    output-list.flag = "***". 
    output-list.amt-foreign = /*tot-foreign*/ 0. 
    IF NOT long-digit THEN output-list.STR = STRING("", "x(27)") 
          + STRING(translateExtended("Grand TOTAL",lvCAREA,""), "x(56)") + " " 
          + STRING(tot, "->,>>>,>>>,>>9.99"). 
    ELSE output-list.STR = STRING("", "x(27)") 
          + STRING(translateExtended("Grand TOTAL",lvCAREA,""), "x(56)") + " " 
          + STRING(tot, "->>>>,>>>,>>>,>>9"). 
  END. 
 
  FIND FIRST sum-list WHERE (sum-list.f-amt NE 0 OR sum-list.amt NE 0) 
    AND sum-list.artart = 6 NO-ERROR. 
  IF AVAILABLE sum-list THEN 
  DO: 
    CREATE output-list. 
    CREATE output-list. 
    output-list.str = STRING("", "x(31)") 
       + STRING(translateExtended ("SUMMARY OF CASH PAYMENT:",lvCAREA,""), "x(57)"). 
    output-list.flag = "#". 
    tot-cash = 0. 
    FOR EACH sum-list WHERE (sum-list.f-amt NE 0 OR 
       sum-list.amt NE 0) AND sum-list.artart = 6 BY sum-list.artnr: 
       tot-cash = tot-cash + sum-list.amt. 
       CREATE output-list. 
       output-list.flag = "SUM". 
       IF NOT long-digit THEN 
       DO: 
         output-list.STR = STRING(" ", "x(8)") 
                    + STRING(" ", "x(6)") 
                    + STRING(0, ">>>>>>>>>") 
                    + STRING(sum-list.artnr, "9999") 
                    + STRING(sum-list.bezeich, "x(40)") 
                    + STRING(" ", "x(17)") 
                    + STRING(sum-list.amt, "->,>>>,>>>,>>9.99"). 
         output-list.amt-foreign = sum-list.f-amt. 
       END. 
       ELSE 
       DO: 
         output-list.STR = STRING(" ", "x(8)") 
                    + STRING(" ", "x(6)") 
                    + STRING(0, ">>>>>>>>>") 
                    + STRING(sum-list.artnr, "9999") 
                    + STRING(sum-list.bezeich, "x(40)") 
                    + STRING(" ", "x(17)") 
                    + STRING(sum-list.amt, "->>>>,>>>,>>>,>>9"). 
         output-list.amt-foreign = sum-list.f-amt. 
       END. 
     END. 
 
     CREATE output-list. 
     output-list.flag = "SUM". 
     output-list.flag = "***". 
     IF NOT long-digit THEN 
     DO: 
       output-list.STR = STRING(" ", "x(8)") 
                  + STRING(" ", "x(6)") 
                  + STRING(0, ">>>>>>>>>") 
                  + STRING(0, ">>>>") 
                  + STRING("TOTAL", "x(40)") 
                  + STRING(" ", "x(17)") 
                  + STRING(tot-cash, "->,>>>,>>>,>>9.99"). 
       output-list.amt-foreign = 0. 
     END. 
     ELSE 
     DO: 
       output-list.STR = STRING(" ", "x(8)") 
                  + STRING(" ", "x(6)") 
                  + STRING(0, ">>>>>>>>>") 
                  + STRING(0, ">>>>") 
                  + STRING("TOTAL", "x(40)") 
                  + STRING(" ", "x(17)") 
                  + STRING(tot-cash, "->>>>,>>>,>>>,>>9"). 
       output-list.amt-foreign = 0. 
     END. 
  END. 
 
  FIND FIRST sum-list WHERE sum-list.f-amt NE 0 OR sum-list.amt NE 0 NO-ERROR. 
  IF AVAILABLE sum-list THEN 
  DO: 
    create output-list. 
    create output-list. 
    output-list.str = STRING("", "x(31)") 
       + STRING(translateExtended ("SUMMARY OF PAYMENT:",lvCAREA,""), "x(57)"). 
    output-list.flag = "#". 
    FOR EACH sum-list WHERE sum-list.f-amt NE 0 OR 
       sum-list.amt NE 0 BY sum-list.artnr: 
       create output-list. 
       output-list.flag = "SUM". 
       IF NOT long-digit THEN 
       DO: 
         output-list.STR = STRING(" ", "x(8)") 
                    + STRING(" ", "x(6)") 
                    + STRING(0, ">>>>>>>>>") 
                    + STRING(sum-list.artnr, "9999") 
                    + STRING(sum-list.bezeich, "x(40)") 
                    + STRING(" ", "x(17)") 
                    + STRING(sum-list.amt, "->,>>>,>>>,>>9.99"). 
         output-list.amt-foreign = sum-list.f-amt. 
       END. 
       ELSE 
       DO: 
         output-list.STR = STRING(" ", "x(8)") 
                    + STRING(" ", "x(6)") 
                    + STRING(0, ">>>>>>>>>") 
                    + STRING(sum-list.artnr, "9999") 
                    + STRING(sum-list.bezeich, "x(40)") 
                    + STRING(" ", "x(17)") 
                    + STRING(sum-list.amt, "->>>>,>>>,>>>,>>9"). 
         output-list.amt-foreign = sum-list.f-amt. 
       END. 
     END. 
  END. 
 
  FOR EACH output-list WHERE output-list.amt-foreign NE 0: 
    IF (output-list.amt-foreign GT  99999999) OR 
       (output-list.amt-foreign LT -99999999) THEN 
    output-list.str-foreign = STRING(output-list.amt-foreign,"->>>,>>>,>>>,>>9"). 
    ELSE 
    output-list.str-foreign = STRING(output-list.amt-foreign,"->,>>>,>>>,>>9.99"). 
  END. 
END. 

PROCEDURE journal-list1: 
DEFINE VARIABLE qty         AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE art-tot     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE art-foreign AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE sub-tot     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE sub-foreign AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot-foreign AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE curr-art    AS INTEGER. 
DEFINE VARIABLE curr-date   AS DATE. 
DEFINE VARIABLE last-dept   AS INTEGER INITIAL -1. 
DEFINE VARIABLE it-exist    AS LOGICAL INITIAL NO. 
DEFINE VARIABLE amt         AS DECIMAL. 
DEFINE VARIABLE tot-cash    AS DECIMAL INITIAL 0  NO-UNDO. 
DEFINE VARIABLE lviresnr    AS INTEGER INITIAL -1 NO-UNDO.
DEFINE VARIABLE lvcs        AS CHAR               NO-UNDO.
DEFINE BUFFER gbuff FOR guest.
 
  FOR EACH sum-list: 
    delete sum-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
 FOR EACH bline-list WHERE bline-list.selected = YES BY bline-list.name: 
    FIND FIRST bediener WHERE RECID(bediener) = bline-list.bl-recid NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN /*Alder - Serverless - Issue 630*/
    DO:
        it-exist = NO. 
        IF NOT summary-flag THEN
        DO:
            create output-list. 
            output-list.flag = "*". 
            output-list.STR = STRING("", "x(27)") + 
            STRING((translateExtended("User:",lvCAREA,"") + " " + bediener.username), "x(22)"). 
        END.
        sub-tot = 0. 
     
        curr-art = 0. 
        art-tot = 0. 
        art-foreign = 0. 
        FOR EACH artikel WHERE (artikel.artart = 2 OR 
          artikel.artart = 6 OR artikel.artart = 7) 
          AND artikel.departement = 0 NO-LOCK BY artikel.bezeich: 
     
          FIND FIRST sum-list WHERE sum-list.artnr = artikel.artnr NO-ERROR. 
          IF NOT AVAILABLE sum-list THEN 
          DO: 
              CREATE sum-list. 
              ASSIGN 
                sum-list.artnr   = artikel.artnr 
                sum-list.artart  = artikel.artart 
                sum-list.bezeich = artikel.bezeich. 
          END. 
     
          FOR EACH billjournal WHERE billjournal.userinit = bediener.userinit 
            AND billjournal.artnr = artikel.artnr AND billjournal.anzahl NE 0 
            AND billjournal.departement = artikel.departement 
            AND bill-datum = from-date AND billjournal.betriebsnr = curr-shift 
            NO-LOCK /*BY billjournal.rechnr BY billjournal.zeit*/
              BY billjournal.zeit BY billjournal.rechnr: /*FDL Ticket 97182B*/ 
     
            IF curr-art = 0 THEN curr-art = artikel.artnr. 
            IF curr-art NE artikel.artnr THEN 
            DO: 
              IF NOT summary-flag THEN 
              DO: 
                create output-list. 
                output-list.flag = "**". 
                output-list.amt-foreign = art-foreign. 
                IF NOT long-digit THEN output-list.STR = STRING("", "x(67)") 
                  + STRING(translateExtended("Sub Total",lvCAREA,""), "x(16)") + " " 
                  + STRING(art-tot, "->,>>>,>>>,>>9.99")
                  + STRING(CHR(10)).    /*MT 20/05/14 */
                ELSE output-list.STR = STRING("", "x(67)") 
                  + STRING(translateExtended("Sub Total",lvCAREA,""), "x(16)") + " " 
                  + STRING(art-tot, " ->>>,>>>,>>>,>>9")
                  + STRING(CHR(10)).    /*MT 20/05/14 */
              END. 
              art-tot = 0. 
              art-foreign = 0. 
              curr-art = artikel.artnr. 
            END. 
            IF artikel.pricetab OR artikel.betriebsnr NE 0 THEN 
            DO: 
              art-foreign = art-foreign + billjournal.fremdwaehrng. 
              sum-list.f-amt = sum-list.f-amt + billjournal.fremdwaehrng. 
            END. 
            ELSE 
            DO: 
              art-tot = art-tot + billjournal.betrag. 
              sum-list.amt = sum-list.amt + billjournal.betrag. 
            END. 
     
            it-exist = YES. 
            IF last-dept NE billjournal.departement THEN FIND FIRST hoteldpt 
               WHERE hoteldpt.num = billjournal.departement NO-LOCK. 
            last-dept = hoteldpt.num. 
            IF NOT summary-flag THEN 
            DO: 
              create output-list. 
              IF artikel.pricetab OR artikel.betriebsnr NE 0 THEN 
              DO: 
                amt-foreign = billjournal.fremdwaehrng. 
                amt = 0. 
              END. 
              ELSE amt = billjournal.betrag. 
              
              IF NOT billjournal.bezeich MATCHES ("*<*") 
                  AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
              DO:
                  /*MT 26/05/14 */
                  IF billjournal.rechnr GT 0 THEN
                  DO:
                    IF billjournal.bediener-nr = 0 /** AND billjournal.bediener EQ 0 */ THEN
                    DO:
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
                    ELSE IF billjournal.bediener-nr NE 0 THEN
                    DO:
                        FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND
                            h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
                        IF AVAILABLE h-bill THEN DO:
                           output-list.gname = h-bill.bilname.
                        END.
                    END.
                  END.
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
    
                  /*MT 26/05/14
                  IF billjournal.betriebsnr GT 0 THEN /* AR from POS, see rinv-ar.i */ 
                  DO:
                    IF billjournal.rechnr GT 0 THEN
                    DO:
                      FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr 
                          AND h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR. 
                      IF AVAILABLE h-bill THEN output-list.gname = h-bill.bilname.
                    END.
                  END.
                  ELSE IF billjournal.betriebsnr = 0 THEN /* CL comes from FO */ 
                  DO:
                    IF billjournal.rechnr GT 0 THEN
                    DO:
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
                  */
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
              IF NOT long-digit THEN 
                  output-list.STR = STRING(bill-datum) 
                        + STRING(billjournal.zinr, "x(6)") 
                        + STRING(billjournal.rechnr, ">>>>>>>>9") 
                        + STRING(billjournal.artnr, "9999") 
                        + STRING(billjournal.bezeich, "x(40)") 
                        + STRING(hoteldpt.depart, "x(17)") 
                        + STRING(amt, "->,>>>,>>>,>>9.99") 
                        + STRING(zeit, "HH:MM:SS") 
                        + STRING(bediener.userinit, "x(3)"). 
              ELSE output-list.STR = STRING(bill-datum) 
                        + STRING(billjournal.zinr, "x(6)") 
                        + STRING(billjournal.rechnr, ">>>>>>>>9") 
                        + STRING(billjournal.artnr, "9999") 
                        + STRING(billjournal.bezeich, "x(40)") 
                        + STRING(hoteldpt.depart, "x(17)") 
                        + STRING(amt, "->>>>,>>>,>>>,>>9") 
                        + STRING(zeit, "HH:MM:SS") 
                        + STRING(bediener.userinit, "x(3)"). 
            END. 
            qty = qty + billjournal.anzahl. 
            IF artikel.pricetab OR artikel.betriebsnr NE 0 THEN 
              sub-foreign = sub-foreign + billjournal.fremdwaehrng. 
            ELSE sub-tot = sub-tot + billjournal.betrag. 
          END. 
        END. 
    END.
    
    IF it-exist AND NOT summary-flag THEN 
    DO: 
      create output-list. 
      output-list.flag = "**". 
      output-list.amt-foreign = art-foreign. 
      IF NOT long-digit THEN output-list.STR = STRING("", "x(27)") 
          + STRING(translateExtended("Sub Total",lvCAREA,""), "x(56)") + " " 
          + STRING(art-tot, "->,>>>,>>>,>>9.99")
          + STRING(CHR(10)).    /*MT 20/05/14 */
      ELSE output-list.STR = STRING("", "x(27)") 
          + STRING(translateExtended("Sub Total",lvCAREA,""), "x(56)") + " " 
          + STRING(art-tot, " ->>>,>>>,>>>,>>9")
          + STRING(CHR(10)).    /*MT 20/05/14 */
      tot-foreign = tot-foreign + sub-foreign. 
      tot = tot + sub-tot. 
    END. 
    ELSE IF NOT it-exist AND NOT summary-flag THEN delete output-list. 
  END. 
  IF NOT summary-flag THEN 
  DO: 
    create output-list. 
    output-list.flag = "***". 
    output-list.amt-foreign = /*tot-foreign*/ 0. 
    IF NOT long-digit THEN output-list.STR = STRING("", "x(27)") 
          + STRING(translateExtended("Grand TOTAL",lvCAREA,""), "x(56)") + " " 
          + STRING(tot, "->,>>>,>>>,>>9.99"). 
    ELSE output-list.STR = STRING("", "x(27)") 
          + STRING(translateExtended("Grand TOTAL",lvCAREA,""), "x(56)") + " " 
          + STRING(tot, "->>>>,>>>,>>>,>>9"). 
  END. 
 
  FIND FIRST sum-list WHERE (sum-list.f-amt NE 0 OR sum-list.amt NE 0) 
    AND sum-list.artart = 6 NO-ERROR. 
  IF AVAILABLE sum-list THEN 
  DO: 
    CREATE output-list. 
    CREATE output-list. 
    output-list.str = STRING("", "x(31)") 
       + STRING(translateExtended ("SUMMARY OF CASH PAYMENT:",lvCAREA,""), "x(57)"). 
    output-list.flag = "#". 
    tot-cash = 0. 
    FOR EACH sum-list WHERE (sum-list.f-amt NE 0 OR 
       sum-list.amt NE 0) AND sum-list.artart = 6 BY sum-list.artnr: 
       tot-cash = tot-cash + sum-list.amt. 
       CREATE output-list. 
       output-list.flag = "SUM". 
       IF NOT long-digit THEN 
       DO: 
         output-list.STR = STRING(" ", "x(8)") 
                    + STRING(" ", "x(6)") 
                    + STRING(0, ">>>>>>>>>") 
                    + STRING(sum-list.artnr, "9999") 
                    + STRING(sum-list.bezeich, "x(40)") 
                    + STRING(" ", "x(17)") 
                    + STRING(sum-list.amt, "->,>>>,>>>,>>9.99"). 
         output-list.amt-foreign = sum-list.f-amt. 
       END. 
       ELSE 
       DO: 
         output-list.STR = STRING(" ", "x(8)") 
                    + STRING(" ", "x(6)") 
                    + STRING(0, ">>>>>>>>>") 
                    + STRING(sum-list.artnr, "9999") 
                    + STRING(sum-list.bezeich, "x(40)") 
                    + STRING(" ", "x(17)") 
                    + STRING(sum-list.amt, "->>>>,>>>,>>>,>>9"). 
         output-list.amt-foreign = sum-list.f-amt. 
       END. 
     END. 
 
     CREATE output-list. 
     output-list.flag = "SUM". 
     output-list.flag = "***". 
     IF NOT long-digit THEN 
     DO: 
       output-list.STR = STRING(" ", "x(8)") 
                  + STRING(" ", "x(6)") 
                  + STRING(0, ">>>>>>>>>") 
                  + STRING(0, ">>>>") 
                  + STRING("TOTAL", "x(40)") 
                  + STRING(" ", "x(17)") 
                  + STRING(tot-cash, "->,>>>,>>>,>>9.99"). 
       output-list.amt-foreign = 0. 
     END. 
     ELSE 
     DO: 
       output-list.STR = STRING(" ", "x(8)") 
                  + STRING(" ", "x(6)") 
                  + STRING(0, ">>>>>>>>>") 
                  + STRING(0, ">>>>") 
                  + STRING("TOTAL", "x(40)") 
                  + STRING(" ", "x(17)") 
                  + STRING(tot-cash, "->>>>,>>>,>>>,>>9"). 
       output-list.amt-foreign = 0. 
     END. 
  END. 
 
  FIND FIRST sum-list WHERE sum-list.f-amt NE 0 OR sum-list.amt NE 0 NO-ERROR. 
  IF AVAILABLE sum-list THEN 
  DO: 
    create output-list. 
    create output-list. 
    output-list.str = STRING("", "x(31)") 
       + STRING(translateExtended ("SUMMARY OF PAYMENT:",lvCAREA,""), "x(47)"). 
    output-list.flag = "#". 
    FOR EACH sum-list WHERE sum-list.f-amt NE 0 OR 
       sum-list.amt NE 0 BY sum-list.artnr: 
       create output-list. 
       output-list.flag = "SUM". 
       IF NOT long-digit THEN 
       DO: 
         output-list.STR = STRING(" ", "x(8)") 
                    + STRING(" ", "x(6)") 
                    + STRING(0, ">>>>>>>>>") 
                    + STRING(sum-list.artnr, "9999") 
                    + STRING(sum-list.bezeich, "x(40)") 
                    + STRING(" ", "x(17)") 
                    + STRING(sum-list.amt, "->,>>>,>>>,>>9.99"). 
         output-list.amt-foreign = sum-list.f-amt. 
       END. 
       ELSE 
       DO: 
         output-list.STR = STRING(" ", "x(8)") 
                    + STRING(" ", "x(6)") 
                    + STRING(0, ">>>>>>>>>") 
                    + STRING(sum-list.artnr, "9999") 
                    + STRING(sum-list.bezeich, "x(40)") 
                    + STRING(" ", "x(17)") 
                    + STRING(sum-list.amt, "->>>>,>>>,>>>,>>9"). 
         output-list.amt-foreign = sum-list.f-amt. 
       END. 
     END. 
  END. 
  FOR EACH output-list WHERE output-list.amt-foreign NE 0: 
    IF (output-list.amt-foreign GT  99999999) OR 
       (output-list.amt-foreign LT -99999999) THEN 
    output-list.str-foreign = STRING(output-list.amt-foreign,"->>>,>>>,>>>,>>9"). 
    ELSE 
    output-list.str-foreign = STRING(output-list.amt-foreign,"->,>>>,>>>,>>9.99"). 
  END. 
END. 



