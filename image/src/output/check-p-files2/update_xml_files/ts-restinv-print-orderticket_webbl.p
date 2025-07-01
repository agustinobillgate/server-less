DEFINE TEMP-TABLE submenu-list 
  FIELD menurecid    AS INTEGER 
  FIELD zeit         AS INTEGER 
  FIELD nr           AS INTEGER 
  FIELD artnr        LIKE h-artikel.artnr 
  FIELD bezeich      LIKE h-artikel.bezeich 
  FIELD anzahl       AS INTEGER 
  FIELD zknr         AS INTEGER 
  FIELD request      AS CHAR
  . 

DEFINE TEMP-TABLE header-list 
    FIELD k                   AS INTEGER
    FIELD depart              AS CHARACTER
    FIELD tableno             AS CHARACTER
    FIELD datum               AS DATE
    FIELD pax                 AS CHARACTER
    FIELD zeit                AS CHARACTER
    FIELD ordertaker          AS CHARACTER
    FIELD waiter              AS CHARACTER
    FIELD bill-no             AS CHARACTER
    FIELD guest-name          AS CHARACTER
    .

DEFINE TEMP-TABLE output-list
    FIELD bill-no           AS INTEGER
    FIELD bezeich           AS CHARACTER
    FIELD pos               AS INTEGER
    FIELD subgrp            AS CHARACTER
    FIELD submenu-request   AS CHARACTER
    FIELD printcod-concod   AS CHARACTER
    FIELD aendertext        AS CHARACTER
    FIELD pax               AS CHARACTER
    FIELD stornogrund       AS CHARACTER
    FIELD submenu-bezeich   AS CHARACTER
    FIELD bezeich2          AS CHARACTER
    .

DEFINE INPUT  PARAMETER TABLE FOR submenu-list.
DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER NO-UNDO.  
DEFINE INPUT  PARAMETER close-it        AS LOGICAL.
DEFINE INPUT  PARAMETER reprint-it      AS LOGICAL.
DEFINE INPUT  PARAMETER h-bill-rechnr   AS INT.
DEFINE INPUT  PARAMETER curr-dept       AS INT.
DEFINE INPUT  PARAMETER disc-art1       AS INT.
DEFINE INPUT  PARAMETER disc-art2       AS INT.
DEFINE INPUT  PARAMETER disc-art3       AS INT.
DEFINE INPUT  PARAMETER prOrder         AS INT.
DEFINE INPUT  PARAMETER descLength      AS INTEGER INITIAL 0 NO-UNDO.
DEFINE OUTPUT PARAMETER k               AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE OUTPUT PARAMETER TABLE FOR header-list.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.
                                              

DEFINE VARIABLE prev-zknr       AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE do-it           AS LOGICAL              NO-UNDO.
DEFINE VARIABLE recid-h-bill-line AS INTEGER INITIAL 0  NO-UNDO.

DEFINE BUFFER abuff             FOR vhp.h-artikel.
DEFINE BUFFER hbuff             FOR vhp.h-bill-line.
DEFINE BUFFER hbline            FOR vhp.h-bill-line.
DEFINE BUFFER qsy               FOR vhp.queasy.

{supertransBL.i}   
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "TS-restinv".  

FIND FIRST h-bill WHERE h-bill.rechnr = h-bill-rechnr AND h-bill.departement = curr-dept NO-LOCK.
IF NOT AVAILABLE h-bill THEN RETURN.

FOR EACH hbuff WHERE hbuff.rechnr = h-bill-rechnr 
    AND hbuff.departement = curr-dept NO-LOCK,
    FIRST abuff WHERE abuff.artnr = hbuff.artnr 
    AND abuff.departement = curr-dept AND abuff.artart = 0
    AND abuff.artnr NE disc-art1 AND abuff.artnr NE disc-art2 
    AND abuff.artnr NE disc-art3 NO-LOCK,
    FIRST vhp.wgrpdep WHERE vhp.wgrpdep.departement = curr-dept 
    AND vhp.wgrpdep.zknr = abuff.zwkum NO-LOCK 
    BY vhp.wgrpdep.betriebsnr DESCENDING
    BY vhp.wgrpdep.zknr
    BY hbuff.artnr
    BY hbuff.sysdate BY hbuff.zeit:

    FIND FIRST h-artikel WHERE h-artikel.artnr = hbuff.artnr NO-LOCK.

    recid-h-bill-line = RECID(hbuff). /*FDL Jan 08, 2024 => Ticket 39793F*/
    
    do-it = reprint-it OR (hbuff.steuercode GE 0 AND hbuff.steuercode LT 9999).     
    IF do-it THEN
    DO:
        k = k + 1.
        IF k = 1 THEN RUN create-bon-header. 
        RUN write-article (RECID(hbuff), INPUT-OUTPUT prev-zknr).
        IF close-it THEN
        DO TRANSACTION:
            FIND FIRST hbline WHERE RECID(hbline) = RECID(hbuff)
              EXCLUSIVE-LOCK.
            IF hbline.steuercode = 0 THEN hbuff.steuercode = - prOrder.
            ELSE hbline.steuercode = 9999.
            FIND CURRENT hbline NO-LOCK.
            RELEASE hbline.
        END.
    END.
END.

/********************************** PROCEDURE **********************************/
PROCEDURE create-bon-header: 
DEFINE VARIABLE tableno AS INTEGER  NO-UNDO. 
DEFINE VARIABLE ct      AS CHAR     NO-UNDO.
DEFINE VARIABLE i       AS INTEGER  NO-UNDO.

DEFINE BUFFER qsy FOR queasy.
    
    FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK.
    ct = vhp.hoteldpt.depart.
    
    CREATE header-list.
    ASSIGN
        header-list.tableno = STRING(h-bill.tischnr)
        header-list.pax     = STRING(h-bill.belegung)
        header-list.datum   = TODAY
        header-list.zeit    = STRING(TIME, "HH:MM")
        header-list.depart  = ct
        header-list.bill-no = "Bill No: " + STRING(h-bill.rechnr)
        .    
        
    FIND FIRST qsy WHERE qsy.key EQ 10 AND qsy.number1 EQ h-bill.betriebsnr NO-LOCK NO-ERROR. 
    IF AVAILABLE qsy THEN header-list.ordertaker = qsy.char1 + "-" + qsy.char2.
    ELSE
    DO:
        FIND FIRST kellner WHERE kellner.kellner-nr EQ h-bill.kellner-nr 
            AND kellner.departement EQ h-bill.departement NO-LOCK NO-ERROR. 
        IF AVAILABLE kellner THEN header-list.waiter = kellner.kellnername.  
    END.

    IF h-bill.bilname NE "" OR h-bill.bilname NE ? THEN
    DO:
        header-list.guest-name = "Guest Name: " + h-bill.bilname.
    END.
END.

PROCEDURE write-article:
DEFINE INPUT PARAMETER s-recid AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER prev-zknr AS INTEGER.

DEFINE VARIABLE curr-recid AS INTEGER INITIAL 0. 
DEFINE VARIABLE created    AS LOGICAL INITIAL NO. 
DEFINE VARIABLE i          AS INTEGER NO-UNDO.
DEFINE VARIABLE ct         AS CHAR    NO-UNDO.

DEFINE BUFFER h-art FOR vhp.h-artikel. 
DEFINE BUFFER qbuff FOR vhp.queasy.
DEFINE BUFFER hbuff FOR vhp.h-bill-line.
    
    FIND FIRST hbuff WHERE RECID(hbuff) = s-recid NO-LOCK NO-ERROR.
    CREATE output-list.
    IF hbuff.anzahl LT 0 THEN 
    DO: 
        FIND FIRST vhp.printcod WHERE vhp.printcod.emu = vhp.printer.emu 
            AND vhp.printcod.code = "redpr" NO-LOCK NO-ERROR.    
        IF AVAILABLE vhp.printcod THEN 
        DO:
            CREATE output-list.
            ASSIGN
                output-list.printcod-concod = vhp.printcod.contcod.                
        END.
    END.                
    
    FIND FIRST vhp.h-journal WHERE vhp.h-journal.bill-datum = hbuff.bill-datum 
        AND vhp.h-journal.sysdate = hbuff.sysdate 
        AND vhp.h-journal.zeit = hbuff.zeit 
        AND vhp.h-journal.artnr = hbuff.artnr 
        AND vhp.h-journal.departement = hbuff.departement 
        AND vhp.h-journal.schankbuch = recid-h-bill-line
        NO-LOCK USE-INDEX chrono_ix NO-ERROR. 
    
    IF prev-zknr NE vhp.wgrpdep.zknr THEN
    DO:
        prev-zknr = wgrpdep.zknr.
        output-list.subgrp = "[" + wgrpdep.bezeich + "]".
    END.

    IF descLength = 0 OR LENGTH(hbuff.bezeich) LE descLength THEN
    DO:
        ASSIGN
            output-list.pax = STRING(hbuff.anzahl).
            output-list.bezeich = hbuff.bezeich.    
    END.    
    ELSE 
    RUN write-descript(STRING(hbuff.anzahl), STRING(hbuff.bezeich)). 
    
    FIND FIRST qbuff WHERE qbuff.KEY = 38 
        AND qbuff.number1 = hbuff.departement
        AND qbuff.number2 = hbuff.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE qbuff THEN
    DO:
        IF descLength = 0 OR LENGTH(qbuff.char3) LE descLength THEN
        DO: 
            ASSIGN
                 output-list.bezeich2 =  qbuff.char3.                 
        END.
        ELSE RUN write-descript(STRING("", "x(5)"), STRING(qbuff.char3)).
    END.
    
    IF hbuff.anzahl NE 0 THEN 
    DO: 
        IF AVAILABLE vhp.h-journal AND vhp.h-journal.aendertext NE "" THEN 
        DO:
            output-list.aendertext = ":::" + vhp.h-journal.aendertext. 
        END.
        IF AVAILABLE vhp.h-journal AND vhp.h-journal.stornogrund NE "" THEN
        DO:
            output-list.stornogrund = ">>>" + STRING(vhp.h-journal.stornogrund, "x(20)"). 
        END.
    END.
        
    IF vhp.h-artikel.betriebsnr GT 0 THEN 
    DO: 
        FOR EACH submenu-list WHERE submenu-list.nr = vhp.h-artikel.betriebsnr 
          AND submenu-list.zeit = hbuff.zeit: 
            created = YES. 
            submenu-bezeich = "-> " + STRING(submenu-list.bezeich). 
            IF submenu-list.request NE "" THEN 
            DO:    
                output-list.submenu-request = ":::" + submenu-list.REQUEST. 
            END.
            DELETE submenu-list. 
        END. 
    
        IF NOT created THEN 
        DO: 
            FIND FIRST vhp.h-journal WHERE vhp.h-journal.artnr = hbuff.artnr AND vhp.h-journal.departement = curr-dept 
                AND vhp.h-journal.rechnr = vhp.h-bill.rechnr AND vhp.h-journal.bill-datum = hbuff.bill-datum 
                AND vhp.h-journal.zeit = hbuff.zeit AND vhp.h-journal.sysdate = hbuff.sysdate NO-LOCK NO-ERROR. 
            IF AVAILABLE vhp.h-journal THEN 
            FOR EACH h-mjourn WHERE h-mjourn.departement = curr-dept 
                AND h-mjourn.h-artnr = vhp.h-journal.artnr 
                AND h-mjourn.rechnr = vhp.h-journal.rechnr 
                AND h-mjourn.bill-datum = vhp.h-journal.bill-datum 
                AND h-mjourn.sysdate = vhp.h-journal.sysdate 
                AND h-mjourn.zeit = vhp.h-journal.zeit NO-LOCK: 
                FIND FIRST h-art WHERE h-art.artnr = h-mjourn.artnr 
                AND h-art.departement = curr-dept NO-LOCK NO-ERROR. 
                IF AVAILABLE h-art THEN 
                DO: 
                    created = YES. 
                    output-list.submenu-bezeich =  "-> " + STRING(h-art.bezeich). 
                    IF h-mjourn.request NE "" THEN
                    DO:
                        /*output-list.request = ":::" + h-mjourn.REQUEST.*/
                    END.
                    ELSE
                    DO:
                          h-mjourn.REQUEST = " ".
                    END.
                END.
            END. 
        END. 
    END. 
  
    IF hbuff.anzahl LT 0 THEN 
    DO: 
        FIND FIRST vhp.printcod WHERE vhp.printcod.emu = vhp.printer.emu 
            AND vhp.printcod.code = "redpr-" NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.printcod THEN 
        DO:
            output-list.printcod-concod = vhp.printcod.contcod.
        END. 
    END. 
END.

PROCEDURE write-descript:
DEF INPUT PARAM str1        AS CHAR.
DEF INPUT PARAM str2        AS CHAR.
DEFINE VARIABLE ct          AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE s1          AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE s2          AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE word        AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE next-line   AS LOGICAL         NO-UNDO.
DEFINE VARIABLE i           AS INTEGER         NO-UNDO.
DEFINE VARIABLE length1     AS INTEGER         NO-UNDO.
    /*
    DO i = 1 TO LENGTH(str1):
        output-list.pax = STRING(SUBSTR(ct,i,1), "x(1)").
    END.
    */
    IF NUM-ENTRIES(str2, " ") = 1 THEN
    DO:
      IF ROUND(descLength / 2, 0) * 2 NE descLength THEN 
        length1 = descLength - 1.
      ELSE length1 = descLength.
      ct = SUBSTR(str2, 1, length1).
      DO i = 1 TO LENGTH(ct):
          output-list.bezeich =  STRING(SUBSTR(ct,i,1), "x(1)").
      END.
      output-list.bezeich = " ".
      ct = "".
      DO i = 1 TO LENGTH(str1):
        ct = ct + " ".
      END.
      ct = ct + SUBSTR(str2, length1 + 1).
      DO i = 1 TO LENGTH(ct):
          output-list.bezeich = STRING(SUBSTR(ct,i,1), "x(1)").
      END.
      /*output-list.bezeich = " ".
      RETURN.
      */
    END.

    next-line = NO. 
    DO i = 1 TO NUM-ENTRIES(str2, " "): 
      word = ENTRY(i, str2, " "). 
      IF next-line THEN s2 = s2 + word + " ". 
      ELSE 
      DO: 
        IF LENGTH(s1 + word) LE descLength THEN s1 = s1 + word + " ". 
        ELSE 
        DO: 
          next-line = YES. 
          s2 = s2 + word + " ". 
        END. 
      END. 
    END. 
    ct = s1.
    DO i = 1 TO LENGTH(ct):
        output-list.bezeich = STRING(SUBSTR(ct,i,1), "x(1)").
      
    END.
    output-list.bezeich = " ".
    ct = "".
    DO i = 1 TO LENGTH(str1):
      ct = ct + " ".
    END.
    ct = ct + s2.
    DO i = 1 TO LENGTH(ct):
        output-list.pax = STRING(SUBSTR(ct,i,1), "x(1)").
    END.
    output-list.pax = " ".
END.

