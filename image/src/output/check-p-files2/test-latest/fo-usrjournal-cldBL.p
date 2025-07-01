DEFINE TEMP-TABLE output-list 
  FIELD STR     AS CHAR
  FIELD gname   AS CHAR FORMAT "x(32)" COLUMN-LABEL "Guest Name". 

DEFINE INPUT PARAMETER mi-incl AS LOGICAL.
DEFINE INPUT PARAMETER mi-excl AS LOGICAL.
DEFINE INPUT PARAMETER mi-tran AS LOGICAL.

DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE INPUT PARAMETER from-dept AS INTEGER.
DEFINE INPUT PARAMETER to-dept   AS INTEGER.
DEFINE INPUT PARAMETER from-art  AS INTEGER.
DEFINE INPUT PARAMETER to-art    AS INTEGER.

DEFINE INPUT PARAMETER usr-init     AS CHAR.
DEFINE INPUT PARAMETER long-digit   AS LOGICAL.
DEFINE INPUT PARAMETER foreign-flag AS LOGICAL.

DEFINE OUTPUT PARAMETER TABLE FOR output-list.

/* Add by Michael @ 02/04/2019 for fixing value of foreign amount - ticket no 904E1F */
IF foreign-flag THEN
DO:
    DEFINE VARIABLE def-rate AS CHARACTER NO-UNDO.
    DEFINE VARIABLE x-rate AS DECIMAL NO-UNDO.
    RUN htpchar.p (144, OUTPUT def-rate).
    IF def-rate EQ "" THEN 
    DO:
        MESSAGE "Htparam group 7 param no 144 is undefine. Please define it first" VIEW-AS ALERT-BOX INFO.
        RETURN NO-APPLY.
    END.
    FIND FIRST waehrung WHERE waehrung.wabkurz EQ def-rate NO-ERROR.
    IF AVAILABLE waehrung THEN 
    DO:
        ASSIGN x-rate = waehrung.ankauf.
        IF x-rate LE 0 THEN
        DO:
            MESSAGE "Foreign Currency Exchange Rate for " def-rate " can not 0 or less. Please correct it first" VIEW-AS ALERT-BOX INFO.
            RETURN NO-APPLY.
        END.
    END.
    ELSE 
    DO:
        MESSAGE "Foreign Currency Exchange Rate for " def-rate " is undefine. Please define it first" VIEW-AS ALERT-BOX INFO.
        RETURN NO-APPLY.
    END.
END.
/* End of add */

IF mi-incl = YES THEN RUN journal-list1. 
ELSE IF mi-excl = YES THEN RUN journal-list2. 
ELSE IF mi-tran = YES THEN RUN journal-list3.


/**************************** PROCEDURES **************************************/ 
 
PROCEDURE journal-list1: 
DEFINE VARIABLE qty        AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sub-tot    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE curr-date  AS DATE. 
DEFINE VARIABLE last-dept  AS INTEGER INITIAL -1. 
 
DEFINE VARIABLE last-artnr AS INTEGER INITIAL -1. 
DEFINE VARIABLE a-qty      AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE a-tot      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE lviresnr   AS INTEGER INITIAL -1 NO-UNDO.
DEFINE VARIABLE lvcs       AS CHAR               NO-UNDO.
DEF BUFFER gbuff FOR guest.
 
DEF VAR amount AS DECIMAL NO-UNDO. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  DO curr-date = from-date TO to-date: 
    FOR EACH billjournal WHERE billjournal.userinit = usr-init 
      AND bill-datum = curr-date 
      AND billjournal.departement GE from-dept 
      AND billjournal.departement LE to-dept 
      AND billjournal.artnr GE from-art AND billjournal.artnr LE to-art 
      NO-LOCK BY billjournal.departement BY billjournal.artnr BY billjournal.zeit: 
      
      FIND FIRST artikel WHERE artikel.artnr = billjournal.artnr
          AND artikel.departement = billjournal.departement NO-LOCK.

      IF last-dept NE billjournal.departement THEN 
      DO: 
        FIND FIRST hoteldpt WHERE hoteldpt.num = billjournal.departement NO-LOCK. 
        IF last-dept EQ -1 THEN last-dept = billjournal.departement. 
      END. 
      IF last-artnr EQ -1 THEN last-artnr = billjournal.artnr. 
      IF last-artnr NE billjournal.artnr OR 
        last-dept NE billjournal.departement THEN 
      DO: 
        last-dept = hoteldpt.num. 
        last-artnr = billjournal.artnr. 
        create output-list. 
        IF NOT long-digit THEN STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
        ELSE STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
        a-qty = 0. 
        a-tot = 0. 
      END. 
 
      /*IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
      ELSE amount = billjournal.betrag.*/
      /* Modify by Michael @ 02/04/2019 for fixing value of foreign amount - ticket no 904E1F */
      IF foreign-flag THEN amount = billjournal.betrag / x-rate. 
      ELSE amount = billjournal.betrag. 
      /* End of modify */
 
      a-qty = a-qty + billjournal.anzahl. 
      a-tot = a-tot + amount.

      
      create output-list. 
      IF NOT long-digit THEN STR = STRING(billjournal.bill-datum) 
                    + STRING(billjournal.zinr, "x(6)") 
                    + STRING(billjournal.rechnr, "9,999,999") 
                    + STRING(billjournal.artnr, "9999") 
                    + STRING(billjournal.bezeich, "x(30)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(billjournal.anzahl, "-9999") 
                    + STRING(amount, "->,>>>,>>>,>>9.99") 
                    + STRING(billjournal.zeit, "HH:MM:SS") 
                    + STRING(billjournal.userinit,"x(4)") 
                    + STRING(billjournal.sysdate)
                    + STRING(RECID(billjournal)) /*FD for uniqe id at vhp web based*/. 
      ELSE STR = STRING(billjournal.bill-datum) 
                    + STRING(billjournal.zinr, "x(6)") 
                    + STRING(billjournal.rechnr, "9,999,999") 
                    + STRING(billjournal.artnr, "9999") 
                    + STRING(billjournal.bezeich, "x(30)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(billjournal.anzahl, "-9999") 
                    + STRING(amount, " ->>>,>>>,>>>,>>9") 
                    + STRING(billjournal.zeit, "HH:MM:SS") 
                    + STRING(billjournal.userinit,"x(4)") 
                    + STRING(billjournal.sysdate)
                    + STRING(RECID(billjournal)) /*FD for uniqe id at vhp web based*/. 
      /* Dzikri 1795E7 - wrong guest name
      IF NOT billjournal.bezeich MATCHES ("*<*") 
          AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
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
      ELSE
      DO:
        /*
          FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND 
              h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
          IF AVAILABLE h-bill THEN
              output-list.gname = h-bill.bilname.
        */
      END.          */
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
            ELSE IF NUM-ENTRIES(billjournal.bezeich,"#") GT 1 
              AND billjournal.departement = 0 THEN
            DO:
              /* Dzikri 34D045 - wrong guest deposit guest name */
                lviresnr = -1.
                lvcs = ENTRY(2,billjournal.bezeich, "#").
                IF INDEX(billjournal.bezeich,"Guest") GT 0 THEN
                DO:
                  lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                  FIND FIRST gbuff WHERE gbuff.gastnr EQ lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE gbuff THEN
                  output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                    + gbuff.anrede1 + gbuff.anredefirma.
                END.
                ELSE
                DO:
                  lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                  FIND FIRST reservation WHERE reservation.resnr EQ lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE reservation THEN
                  DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr EQ reservation.gastnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN
                    output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                      + gbuff.anrede1 + gbuff.anredefirma.
                  END.
                END.
              /* Dzikri 34D045 - END */
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
      /*  Dzikri 1795E7 - END */
      qty = qty + billjournal.anzahl. 
/*    IF billjournal.anzahl NE 0 THEN  */ 
      DO: 
        sub-tot = sub-tot + amount. 
        tot = tot + amount. 
      END. 
    END. 
  END.
  
  create output-list. 
  IF NOT long-digit THEN STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
  ELSE STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
END. 
 
PROCEDURE journal-list2: 
DEFINE VARIABLE qty        AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sub-tot    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE curr-date  AS DATE. 
DEFINE VARIABLE last-dept  AS INTEGER INITIAL -1. 
DEFINE VARIABLE last-artnr AS INTEGER INITIAL -1. 
DEFINE VARIABLE a-qty      AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE a-tot      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE lviresnr   AS INTEGER INITIAL -1 NO-UNDO.
DEFINE VARIABLE lvcs       AS CHAR               NO-UNDO.
DEFINE BUFFER gbuff FOR guest.
DEF VAR amount AS DECIMAL NO-UNDO. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  DO curr-date = from-date TO to-date: 
    FOR EACH billjournal WHERE billjournal.userinit = usr-init 
      AND bill-datum = curr-date 
      AND billjournal.departement GE from-dept 
      AND billjournal.departement LE to-dept 
      AND billjournal.artnr GE from-art AND billjournal.artnr LE to-art 
      AND billjournal.anzahl NE 0
      NO-LOCK BY billjournal.departement BY billjournal.artnr BY billjournal.zeit: 
      
      FIND FIRST artikel WHERE artikel.artnr = billjournal.artnr
        AND artikel.departement = billjournal.departement NO-LOCK.
      
      IF last-dept NE billjournal.departement THEN 
      DO: 
        FIND FIRST hoteldpt WHERE hoteldpt.num = billjournal.departement NO-LOCK. 
        IF last-dept EQ -1 THEN last-dept = billjournal.departement. 
      END. 
      IF last-artnr EQ -1 THEN last-artnr = billjournal.artnr. 
      IF last-artnr NE billjournal.artnr OR 
        last-dept NE billjournal.departement THEN 
      DO: 
        last-dept = hoteldpt.num. 
        last-artnr = billjournal.artnr. 
        create output-list. 
        IF NOT long-digit THEN STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
        ELSE STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
        a-qty = 0. 
        a-tot = 0. 
      END. 
 
      /*IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
      ELSE amount = billjournal.betrag.*/
      /* Modify by Michael @ 02/04/2019 for fixing value of foreign amount - ticket no 904E1F */
      IF foreign-flag THEN amount = billjournal.betrag / x-rate. 
      ELSE amount = billjournal.betrag. 
      /* End of modify */
 
      a-qty = a-qty + billjournal.anzahl. 
      a-tot = a-tot + amount. 
      create output-list. 
      IF NOT long-digit THEN STR = STRING(billjournal.bill-datum) 
                    + STRING(billjournal.zinr, "x(6)") 
                    + STRING(billjournal.rechnr, "9,999,999") 
                    + STRING(billjournal.artnr, "9999") 
                    + STRING(billjournal.bezeich, "x(30)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(billjournal.anzahl, "-9999") 
                    + STRING(amount, "->,>>>,>>>,>>9.99") 
                    + STRING(billjournal.zeit, "HH:MM:SS") 
                    + STRING(billjournal.userinit,"x(4)") 
                    + STRING(billjournal.sysdate)
                    + STRING(RECID(billjournal)) /*FD for uniqe id at vhp web based*/. 
      ELSE STR = STRING(billjournal.bill-datum) 
                    + STRING(billjournal.zinr, "x(6)") 
                    + STRING(billjournal.rechnr, "9,999,999") 
                    + STRING(billjournal.artnr, "9999") 
                    + STRING(billjournal.bezeich, "x(30)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(billjournal.anzahl, "-9999") 
                    + STRING(amount, " ->>>,>>>,>>>,>>9") 
                    + STRING(billjournal.zeit, "HH:MM:SS") 
                    + STRING(billjournal.userinit,"x(4)") 
                    + STRING(billjournal.sysdate)
                    + STRING(RECID(billjournal)) /*FD for uniqe id at vhp web based*/. 
      /*  Dzikri 1795E7 - wrong guest name
      IF NOT billjournal.bezeich MATCHES ("*<*") 
          AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
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
      ELSE
      DO:
        /*
          FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND 
              h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
          IF AVAILABLE h-bill THEN
              output-list.gname = h-bill.bilname.
        */        
      END. */
      
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
            ELSE IF NUM-ENTRIES(billjournal.bezeich,"#") GT 1 
              AND billjournal.departement = 0 THEN
            DO:
              /* Dzikri 34D045 - wrong guest deposit guest name */
                lviresnr = -1.
                lvcs = ENTRY(2,billjournal.bezeich, "#").
                IF INDEX(billjournal.bezeich,"Guest") GT 0 THEN
                DO:
                  lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                  FIND FIRST gbuff WHERE gbuff.gastnr EQ lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE gbuff THEN
                  output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                    + gbuff.anrede1 + gbuff.anredefirma.
                END.
                ELSE
                DO:
                  lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                  FIND FIRST reservation WHERE reservation.resnr EQ lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE reservation THEN
                  DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr EQ reservation.gastnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN
                    output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                      + gbuff.anrede1 + gbuff.anredefirma.
                  END.
                END.
              /* Dzikri 34D045 - END */
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
      /*  Dzikri 1795E7 - END */
      qty = qty + billjournal.anzahl. 
    /* IF billjournal.anzahl NE 0 THEN  */ 
      DO: 
        sub-tot = sub-tot + amount. 
        tot = tot + amount. 
      END. 
    END. 
  END. 
  create output-list. 
  IF NOT long-digit THEN STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
  ELSE STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
END. 
 
PROCEDURE journal-list3: 
DEFINE VARIABLE qty        AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sub-tot    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE curr-date  AS DATE. 
DEFINE VARIABLE last-dept  AS INTEGER INITIAL -1. 
DEFINE VARIABLE last-artnr AS INTEGER INITIAL -1. 
DEFINE VARIABLE a-qty      AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE a-tot      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE lviresnr   AS INTEGER INITIAL -1 NO-UNDO.
DEFINE VARIABLE lvcs       AS CHAR               NO-UNDO.
DEFINE BUFFER gbuff FOR guest. 
DEF VAR amount AS DECIMAL NO-UNDO. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  DO curr-date = from-date TO to-date: 
    FOR EACH billjournal WHERE billjournal.userinit = usr-init 
      AND bill-datum = curr-date 
      AND billjournal.departement GE from-dept 
      AND billjournal.departement LE to-dept 
      AND billjournal.artnr GE from-art AND billjournal.artnr LE to-art 
      AND billjournal.anzahl = 0
      NO-LOCK BY billjournal.departement BY billjournal.artnr BY billjournal.zeit: 
        
      FIND FIRST artikel WHERE artikel.artnr = billjournal.artnr
        AND artikel.departement = billjournal.departement NO-LOCK.

      IF last-dept NE billjournal.departement THEN 
      DO: 
        FIND FIRST hoteldpt WHERE hoteldpt.num = billjournal.departement NO-LOCK. 
        IF last-dept EQ -1 THEN last-dept = billjournal.departement. 
      END. 
      IF last-artnr EQ -1 THEN last-artnr = billjournal.artnr. 
      IF last-artnr NE billjournal.artnr OR 
        last-dept NE billjournal.departement THEN 
      DO: 
        last-dept = hoteldpt.num. 
        last-artnr = billjournal.artnr. 
        create output-list. 
        IF NOT long-digit THEN STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
        ELSE STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
        a-qty = 0. 
        a-tot = 0. 
      END. 
 
      /*IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
      ELSE amount = billjournal.betrag.*/
      /* Modify by Michael @ 02/04/2019 for fixing value of foreign amount - ticket no 904E1F */
      IF foreign-flag THEN amount = billjournal.betrag / x-rate. 
      ELSE amount = billjournal.betrag. 
      /* End of modify */
 
      a-qty = a-qty + billjournal.anzahl. 
      a-tot = a-tot + amount. 
      create output-list. 
      IF NOT long-digit THEN STR = STRING(billjournal.bill-datum) 
                    + STRING(billjournal.zinr, "x(6)") 
                    + STRING(billjournal.rechnr, "9,999,999") 
                    + STRING(billjournal.artnr, "9999") 
                    + STRING(billjournal.bezeich, "x(30)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(billjournal.anzahl, "-9999") 
                    + STRING(amount, "->,>>>,>>>,>>9.99") 
                    + STRING(billjournal.zeit, "HH:MM:SS") 
                    + STRING(billjournal.userinit,"x(4)") 
                    + STRING(billjournal.sysdate)
                    + STRING(RECID(billjournal)) /*FD for uniqe id at vhp web based*/. 
      ELSE STR = STRING(billjournal.bill-datum) 
                    + STRING(billjournal.zinr, "x(6)") 
                    + STRING(billjournal.rechnr, "9,999,999") 
                    + STRING(billjournal.artnr, "9999") 
                    + STRING(billjournal.bezeich, "x(30)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(billjournal.anzahl, "-9999") 
                    + STRING(amount, " ->>>,>>>,>>>,>>9") 
                    + STRING(billjournal.zeit, "HH:MM:SS") 
                    + STRING(billjournal.userinit,"x(4)") 
                    + STRING(billjournal.sysdate) 
                    + STRING(RECID(billjournal)) /*FD for uniqe id at vhp web based*/.
      
      /*
      IF NOT billjournal.bezeich MATCHES ("*<*") 
          AND NOT billjournal.bezeich MATCHES ("*>*") THEN 
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
      ELSE
      DO:
        /*
          FIND FIRST h-bill WHERE h-bill.rechnr = billjournal.rechnr AND 
              h-bill.departement = billjournal.betriebsnr NO-LOCK NO-ERROR.
          IF AVAILABLE h-bill THEN
              output-list.gname = h-bill.bilname.
        */
      END. */
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
            ELSE IF NUM-ENTRIES(billjournal.bezeich,"#") GT 1 
              AND billjournal.departement = 0 THEN
            DO:
              /* Dzikri 34D045 - wrong guest deposit guest name */
                lviresnr = -1.
                lvcs = ENTRY(2,billjournal.bezeich, "#").
                IF INDEX(billjournal.bezeich,"Guest") GT 0 THEN
                DO:
                  lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                  FIND FIRST gbuff WHERE gbuff.gastnr EQ lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE gbuff THEN
                  output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                    + gbuff.anrede1 + gbuff.anredefirma.
                END.
                ELSE
                DO:
                  lviresnr = INTEGER(ENTRY(1,lvcs,"]")) NO-ERROR.
                  FIND FIRST reservation WHERE reservation.resnr EQ lviresnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE reservation THEN
                  DO:
                    FIND FIRST gbuff WHERE gbuff.gastnr EQ reservation.gastnr
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE gbuff THEN
                    output-list.gname = gbuff.name + ", " + gbuff.vorname1 + " "
                      + gbuff.anrede1 + gbuff.anredefirma.
                  END.
                END.
              /* Dzikri 34D045 - END */
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
      /*  Dzikri 1795E7 - END */
      qty = qty + billjournal.anzahl. 
      /* IF billjournal.anzahl NE 0 THEN  */ 
      DO: 
        sub-tot = sub-tot + amount. 
        tot = tot + amount. 
      END. 
    END. 
  END. 
  create output-list. 
  IF NOT long-digit THEN STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
  ELSE STR = STRING("", "x(57)") 
          + STRING("T O T A L  ", "x(11)") 
          + STRING(a-qty, "-9999") 
          + STRING(a-tot, "->,>>>,>>>,>>9.99"). 
END. 
 

