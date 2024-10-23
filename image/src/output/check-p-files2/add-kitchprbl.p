/************ print vhp.h-bill-line TO kitchen vhp.printer ***********/ 

/*sis 230414 --> add billno to kitchen printer (queasy.char3)*/
/*FDL July 29, 2024 => Ticket 9E23EA*/

DEFINE TEMP-TABLE t-queasy LIKE queasy.

DEFINE TEMP-TABLE submenu-list 
  FIELD menurecid   AS INTEGER 
  FIELD zeit        AS INTEGER 
  FIELD nr          AS INTEGER
  FIELD artnr       LIKE vhp.h-artikel.artnr 
  FIELD bezeich     LIKE vhp.h-artikel.bezeich 
  FIELD anzahl      AS INTEGER 
  FIELD zknr        AS INTEGER 
  FIELD request     AS CHAR.

DEFINE INPUT  PARAMETER pvILanguage         AS INTEGER         NO-UNDO.
DEFINE INPUT  PARAMETER session-parameter   AS CHAR.
DEFINE INPUT  PARAMETER dept                AS INTEGER. 
DEFINE INPUT  PARAMETER rechnr              AS INTEGER. 
DEFINE INPUT  PARAMETER billdate            AS DATE. 
DEFINE INPUT  PARAMETER user-init           AS CHAR.
DEFINE OUTPUT PARAMETER error-str           AS CHAR INITIAL "" NO-UNDO.
  
{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "add-kitchpr". 

DEFINE /*MTNEW GLOBAL SHARED*/ VARIABLE kitchen-pr AS INTEGER EXTENT 10 
  INITIAL[0,0,0,0,0,0,0,0,0,-1]. 
 
DEFINE VARIABLE numcat1         AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE numcat2         AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE k               AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE prev-zknr       AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE add-zeit        AS INTEGER INITIAL 0    NO-UNDO. 

DEFINE VARIABLE always-do       AS LOGICAL INITIAL YES  NO-UNDO. 
DEFINE VARIABLE bline-created   AS LOGICAL INITIAL NO   NO-UNDO. 
DEFINE VARIABLE print-subgrp    AS LOGICAL INITIAL YES  NO-UNDO. 
DEFINE VARIABLE print-single    AS LOGICAL INITIAL NO   NO-UNDO. 
DEFINE VARIABLE DescLength      AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE sort-subgrp     AS LOGICAL INITIAL NO   NO-UNDO. 
DEFINE VARIABLE recid-h-bill-line AS INTEGER INITIAL 0  NO-UNDO.
DEFINE VARIABLE sort-subgrp-prior AS LOGICAL INITIAL NO   NO-UNDO. 

/*sis 230414*/
DEFINE VARIABLE room      AS CHARACTER NO-UNDO.
DEFINE VARIABLE gname     AS CHARACTER NO-UNDO.
DEFINE VARIABLE room-str  AS CHARACTER NO-UNDO.
/*end sis*/

DEFINE VARIABLE printer-loc AS CHARACTER NO-UNDO.

DEFINE VARIABLE create-queasy AS LOGICAL INIT NO.
DEFINE VARIABLE count-k AS INTEGER INITIAL 0.

DEFINE BUFFER hbline FOR vhp.h-bill-line.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 252 NO-LOCK.
numcat1 = vhp.htparam.finteger.
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 562 NO-LOCK.
numcat2 = vhp.htparam.finteger.

RUN htpdate.p(110, OUTPUT billdate).
IF TODAY GT billdate THEN billdate = TODAY.

/* IF kitchen-pr[10] = -1 THEN */ 
RUN readSession. 

FIND FIRST htparam WHERE htparam.paramnr = 450 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN print-subgrp = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 147 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN sort-subgrp = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 838 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN sort-subgrp-prior = htparam.flogical.

FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = dept NO-LOCK. 
FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement = dept 
  AND vhp.h-bill.rechnr = rechnr NO-LOCK NO-ERROR. 
 
IF sort-subgrp = YES THEN DO:
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = rechnr 
      AND vhp.h-bill-line.departement = dept AND vhp.h-bill-line.steuercode LE 0 NO-LOCK,
      FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr 
      AND vhp.h-artikel.departement = dept AND vhp.h-artikel.artart = 0 NO-LOCK,
      FIRST vhp.wgrpdep WHERE vhp.wgrpdep.departement = dept 
      AND vhp.wgrpdep.zknr = vhp.h-artikel.zwkum NO-LOCK      
      BY vhp.h-artikel.bondruckernr[1]       
      BY vhp.h-artikel.zwkum
      BY vhp.h-bill-line.sysdate BY vhp.h-bill-line.zeit 
      BY RECID(vhp.h-bill-line)     /*FDL March 10, 2023 => Ticket BB727B*/
      /*BY vhp.h-artikel.endkum
      BY vhp.wgrpdep.betriebsnr DESCENDING
      BY vhp.wgrpdep.zknr
      BY vhp.h-bill-line.artnr*/:
    
      add-zeit = add-zeit + 1. 
      recid-h-bill-line = RECID(vhp.h-bill-line).
      FIND FIRST vhp.htparam WHERE paramnr = 865 NO-LOCK. 
      IF vhp.htparam.flogical /* i.e. kitchen vhp.printer is active */ 
        AND vhp.h-artikel.bondruckernr[1] GT 0 THEN 
      DO: 
        IF NOT print-single THEN
        DO:
          IF (k NE vhp.h-artikel.bondruckernr[1]) THEN 
          DO: 
            IF k GT 0 THEN RUN cut-it. 
            RUN create-bon-output. 
            k = vhp.h-artikel.bondruckernr[1]. 
          END. 
          RUN write-article. 
        END.
        ELSE
        DO:
          RUN create-bon-output.
          k = vhp.h-artikel.bondruckernr[1].
          
          RUN write-article. 
          RUN cut-it.
        END.
      END. 
      DO TRANSACTION:
        FIND FIRST hbline WHERE RECID(hbline) = RECID(vhp.h-bill-line)
            EXCLUSIVE-LOCK.
        IF vhp.h-artikel.bondruckernr[1] NE 0 THEN 
        DO:
          IF hbline.steuercode = 0 THEN 
              hbline.steuercode = vhp.h-artikel.bondruckernr[1]. 
          ELSE hbline.steuercode = 9999. /* used by kitchen + order printer */
        END.
        ELSE 
        DO:    
            IF hbline.steuercode = 0 THEN vhp.h-bill-line.steuercode = 1.
            ELSE hbline.steuercode = 9999.
        END.
        FIND CURRENT hbline NO-LOCK.
        RELEASE hbline.
        bline-created = YES. 
      END.
    END. 
END.
ELSE IF sort-subgrp-prior EQ YES THEN /*FDL August 02, 2023 => Ticket AFAB58*/
DO:
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = rechnr 
        AND vhp.h-bill-line.departement = dept AND vhp.h-bill-line.steuercode LE 0 NO-LOCK,
        FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr 
        AND vhp.h-artikel.departement = dept AND vhp.h-artikel.artart = 0 NO-LOCK,
        FIRST vhp.wgrpdep WHERE vhp.wgrpdep.departement = dept 
        AND vhp.wgrpdep.zknr = vhp.h-artikel.zwkum NO-LOCK      
        BY vhp.h-artikel.bondruckernr[1]       
        BY vhp.wgrpdep.betriebsnr DESC
        BY vhp.h-bill-line.sysdate BY vhp.h-bill-line.zeit 
        BY RECID(vhp.h-bill-line):     /*FDL March 10, 2023 => Ticket BB727B*/                        

        add-zeit = add-zeit + 1. 
        recid-h-bill-line = RECID(vhp.h-bill-line).
        FIND FIRST vhp.htparam WHERE paramnr = 865 NO-LOCK. 
        IF vhp.htparam.flogical /* i.e. kitchen vhp.printer is active */ 
            AND vhp.h-artikel.bondruckernr[1] GT 0 THEN 
        DO: 
            IF NOT print-single THEN
            DO:
                IF (k NE vhp.h-artikel.bondruckernr[1]) THEN 
                DO: 
                    IF k GT 0 THEN RUN cut-it. 
                    RUN create-bon-output. 
                    k = vhp.h-artikel.bondruckernr[1]. 
                END. 
                RUN write-article. 
            END.
            ELSE
            DO:
                RUN create-bon-output.
                k = vhp.h-artikel.bondruckernr[1].
                
                RUN write-article. 
                RUN cut-it.
            END.
        END. 
        DO TRANSACTION:
            FIND FIRST hbline WHERE RECID(hbline) = RECID(vhp.h-bill-line) EXCLUSIVE-LOCK.
            IF vhp.h-artikel.bondruckernr[1] NE 0 THEN 
            DO:
                IF hbline.steuercode = 0 THEN hbline.steuercode = vhp.h-artikel.bondruckernr[1]. 
                ELSE hbline.steuercode = 9999. /* used by kitchen + order printer */
            END.
            ELSE 
            DO:    
                IF hbline.steuercode = 0 THEN vhp.h-bill-line.steuercode = 1.
                ELSE hbline.steuercode = 9999.
            END.
            FIND CURRENT hbline NO-LOCK.
            RELEASE hbline.
            bline-created = YES. 
        END.
    END. 
END.
ELSE DO:
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = rechnr 
      AND vhp.h-bill-line.departement = dept AND vhp.h-bill-line.steuercode LE 0 NO-LOCK,
      FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr 
      AND vhp.h-artikel.departement = dept AND vhp.h-artikel.artart = 0 NO-LOCK,
      FIRST vhp.wgrpdep WHERE vhp.wgrpdep.departement = dept 
      AND vhp.wgrpdep.zknr = vhp.h-artikel.zwkum NO-LOCK      
      BY vhp.h-artikel.bondruckernr[1]       
      BY vhp.h-bill-line.sysdate BY vhp.h-bill-line.zeit
      BY RECID(vhp.h-bill-line)     /*FDL March 10, 2023 => Ticket BB727B*/
      /*BY vhp.h-artikel.endkum
      BY vhp.wgrpdep.betriebsnr DESCENDING
      BY vhp.wgrpdep.zknr
      BY vhp.h-bill-line.artnr*/:
    
      count-k = count-k + 1.
      add-zeit = add-zeit + 1. 
      recid-h-bill-line = RECID(vhp.h-bill-line).

      /*Debug Alas Harum
      MESSAGE 
          "#QUEASY KP TRAP LOG FIRST: " count-k SKIP
          ">>>" "Date=" STRING(h-bill-line.bill-datum) " | " "BillNo=" h-bill-line.rechnr " | " "Dept=" h-bill-line.departement SKIP
          ">>>" "ArtNo=" h-bill-line.artnr " | " "Desc=" h-bill-line.bezeich " | " "KP-No=" h-artikel.bondruckernr[1] SKIP
          ">>>" "Steuercode=" h-bill-line.steuercode " | "  "Time=" STRING(TIME + add-zeit,"HH:MM:SS") " | " "RecID=" STRING(RECID(h-bill-line)) SKIP
          "#END QUEASY KP FIRST"
          VIEW-AS ALERT-BOX INFO BUTTONS OK.*/

      FIND FIRST vhp.htparam WHERE paramnr = 865 NO-LOCK. 
      IF vhp.htparam.flogical /* i.e. kitchen vhp.printer is active */ 
        AND vhp.h-artikel.bondruckernr[1] GT 0 THEN 
      DO: 
        IF NOT print-single THEN
        DO:
          IF (k NE vhp.h-artikel.bondruckernr[1]) THEN 
          DO: 
            IF k GT 0 THEN RUN cut-it. 
            RUN create-bon-output. 
            k = vhp.h-artikel.bondruckernr[1]. 
          END. 
          RUN write-article. 
        END.
        ELSE
        DO:
          RUN create-bon-output.
          k = vhp.h-artikel.bondruckernr[1].
          
          RUN write-article. 
          RUN cut-it.
        END.
      END. 

      /*Debug Alas Harum
      MESSAGE 
          "#QUEASY KP TRAP LOG 1: " count-k SKIP
          ">>>" "Date=" STRING(h-bill-line.bill-datum) " | " "BillNo=" h-bill-line.rechnr " | " "Dept=" h-bill-line.departement SKIP
          ">>>" "ArtNo=" h-bill-line.artnr " | " "Desc=" h-bill-line.bezeich " | " "KP-No=" h-artikel.bondruckernr[1] SKIP
          ">>>" "Steuercode=" h-bill-line.steuercode " | "  "Time=" STRING(TIME + add-zeit,"HH:MM:SS") " | " "RecID=" STRING(RECID(h-bill-line)) SKIP
          "#END QUEASY KP 1"
          VIEW-AS ALERT-BOX INFO BUTTONS OK.*/

      DO TRANSACTION:
        FIND FIRST hbline WHERE RECID(hbline) = RECID(vhp.h-bill-line)
            EXCLUSIVE-LOCK.
        IF vhp.h-artikel.bondruckernr[1] NE 0 THEN 
        DO:
          IF hbline.steuercode = 0 THEN hbline.steuercode = vhp.h-artikel.bondruckernr[1]. 
          ELSE hbline.steuercode = 9999. /* used by kitchen + order printer */
        END.
        ELSE 
        DO:    
            IF hbline.steuercode = 0 THEN vhp.h-bill-line.steuercode = 1.
            ELSE hbline.steuercode = 9999.
        END.
        FIND CURRENT hbline NO-LOCK.

        /*Debug Alas Harum
        MESSAGE 
            "#QUEASY KP TRAP LOG 2: " count-k SKIP
            ">>>" "ArtNo=" h-bill-line.artnr " | " "Desc=" h-bill-line.bezeich SKIP
            ">>>" "Steuercode=" hbline.steuercode " | "  "Steuercode2=" h-bill-line.steuercode SKIP
            "#END QUEASY KP 2"
            VIEW-AS ALERT-BOX INFO BUTTONS OK.*/

          RELEASE hbline.
          bline-created = YES. 
      END.
    END. 
END.
IF k GT 0 AND NOT print-single THEN RUN cut-it. 
 
FOR EACH t-queasy:
    DO TRANSACTION:
        CREATE queasy.
        BUFFER-COPY t-queasy TO queasy.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
END.

PROCEDURE create-bon-output:

DEF VARIABLE tableno AS INTEGER NO-UNDO. 
DEF BUFFER qsy FOR t-queasy.

    /*Debug*/
    MESSAGE "create-bon-output:=" h-artikel.bondruckernr[1]
        VIEW-AS ALERT-BOX INFO BUTTONS OK.

  FIND FIRST vhp.printer WHERE vhp.printer.nr = vhp.h-artikel.bondruckernr[1] NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE vhp.printer THEN 
  DO: 
    error-str = error-str + translateExtended ("The kitchen vhp.printer number",lvCAREA,"")
      + " " + STRING(h-artikel.bondrucker[1]) + CHR(10) 
      + translateExtended ("in Article",lvCAREA,"") + " " 
      + STRING(h-artikel.artnr) + " - " + vhp.h-artikel.bezeich + CHR(10)
      + translateExtended ("not defined in the vhp.printer Administration!",lvCAREA,"")
      + CHR(10).
    CREATE t-queasy. 
    ASSIGN 
        t-queasy.key = 3
        /*t-queasy.number1 = vhp.PRINTER.nr
        t-queasy.number3 = vhp.PRINTER.nr*/.
  END. 
  ELSE DO: 
      RUN get-printer-number.
      FIND FIRST queasy WHERE queasy.KEY = 208 AND queasy.number1 = vhp.h-artikel.endkum
          NO-LOCK NO-ERROR.
      IF NOT AVAILABLE queasy THEN DO:
          CREATE queasy.
          ASSIGN 
              queasy.KEY     = 208 
              queasy.number1 = vhp.h-artikel.endkum
              queasy.number2 = 1.
      END.
      ELSE DO:
           FIND CURRENT queasy EXCLUSIVE-LOCK.
           ASSIGN queasy.number2 = queasy.number2 + 1.
           FIND CURRENT queasy NO-LOCK.
      END.

      CREATE t-queasy. 
      ASSIGN
          t-queasy.key = 3
          t-queasy.number1 = vhp.PRINTER.nr
          t-queasy.number3 = vhp.PRINTER.nr
          t-queasy.deci1   = queasy.number2.

      /*Debug*/
      MESSAGE  
          "Available:=" t-queasy.KEY "|" t-queasy.number1 "|" t-queasy.number3
          VIEW-AS ALERT-BOX INFO BUTTONS OK.
  END.

  ASSIGN 
      tableno          = vhp.h-bill-line.tischnr
      t-queasy.number2 = TIME + add-zeit  
      t-queasy.logi1   = NO
      t-queasy.date1   = billdate
      t-queasy.date2   = TODAY
      t-queasy.char2   = printer-loc
      t-queasy.logi2   = YES
      .

  t-queasy.char3 = vhp.hoteldpt.depart + CHR(10) 
    /*sis  +  CHR(10) + " " + CHR(10)*/
      + translateExtended ("BillNo", lvCAREA,"") + " " + STRING(vhp.h-bill.rechnr) + CHR(10) /*sis 230414 add billno info*/
      + translateExtended (room-str, lvCAREA,"") + " " + STRING(room) + " " + STRING(gname) + CHR(10) /*sis 230414 add rmno and guest info*/
      + translateExtended ("Table", lvCAREA,"") + " " + STRING(tableno) + " "
      + translateExtended ("Pax", lvCAREA,"")   + " " + STRING(vhp.h-bill.belegung) + CHR(10)
      /*+ " - "*/ + STRING(TODAY) + " " + STRING(time, "HH:MM") + CHR(10). 
 
  FIND FIRST vhp.bediener WHERE vhp.bediener.userinit = user-init NO-LOCK
      NO-ERROR.
  IF AVAILABLE vhp.bediener THEN
  t-queasy.char3 = t-queasy.char3 
  + translateExtended ("Posted by:",lvCAREA,"") + " " 
  + vhp.bediener.username + CHR(10).
  ELSE
  DO:
    FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr 
      = vhp.h-bill.kellner-nr AND vhp.kellner.departement 
      = vhp.h-bill.departement NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.kellner THEN 
    t-queasy.char3 = t-queasy.char3 
      + translateExtended ("Waiter:",lvCAREA,"") + " " 
      + vhp.kellner.kellnername + CHR(10).
  END.
  FIND FIRST qsy WHERE qsy.key = 10 
    AND qsy.number1 = vhp.h-bill.betriebsnr NO-LOCK NO-ERROR. 
  IF AVAILABLE qsy THEN 
  t-queasy.char3 = t-queasy.char3 
    + translateExtended ("Order Taker:",lvCAREA,"") + " " 
    + qsy.char1 + CHR(10).
   
  t-queasy.char3 = t-queasy.char3 + CHR(10).
  
END. 
 
PROCEDURE write-article: 
DEFINE VARIABLE curr-recid AS INTEGER INITIAL 0. 
DEFINE VARIABLE created AS LOGICAL INITIAL NO. 
DEFINE BUFFER h-art FOR vhp.h-artikel. 
DEFINE BUFFER qbuff FOR t-queasy.

  /*IF vhp.h-bill-line.anzahl LT 0 THEN 
  DO: 
    FIND FIRST vhp.printcod WHERE vhp.printcod.emu = vhp.printer.emu 
      AND vhp.printcod.code = "redpr" NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.printcod THEN t-queasy.char3 = t-queasy.char3 
      + vhp.printcod.contcod. 
  END. */
 
  FIND FIRST vhp.h-journal WHERE vhp.h-journal.bill-datum 
    = vhp.h-bill-line.bill-datum 
    AND vhp.h-journal.sysdate = vhp.h-bill-line.sysdate 
    AND vhp.h-journal.zeit = vhp.h-bill-line.zeit 
    AND vhp.h-journal.artnr = vhp.h-bill-line.artnr 
    AND vhp.h-journal.departement = vhp.h-bill-line.departement 
    AND vhp.h-journal.schankbuch = recid-h-bill-line /*FD June 13, 2022 => Ticket 431485*/
    NO-LOCK USE-INDEX chrono_ix NO-ERROR. 
 
  IF print-subgrp AND print-single THEN
  DO:
    prev-zknr = vhp.wgrpdep.zknr.
    t-queasy.char3 = t-queasy.char3 
      + "[" + STRING(vhp.wgrpdep.bezeich) + "]" + CHR(10). 

  END.
  ELSE IF (print-subgrp OR sort-subgrp-prior) AND NOT print-single AND (prev-zknr NE vhp.wgrpdep.zknr) THEN
  DO:
    prev-zknr = vhp.wgrpdep.zknr.
    t-queasy.char3 = t-queasy.char3 
      + "[" + STRING(vhp.wgrpdep.bezeich) + "]" + CHR(10). 
  END.

  IF descLength = 0 OR LENGTH(vhp.h-bill-line.bezeich) LE descLength THEN
  DO:
    t-queasy.char3 = t-queasy.char3 
      + STRING(vhp.h-bill-line.anzahl, "->>9 ")
      + STRING(vhp.h-bill-line.bezeich) + CHR(10). 
  END.
  ELSE RUN write-descript(STRING(vhp.h-bill-line.anzahl, "->>9 "),
                          STRING(vhp.h-bill-line.bezeich)).

  FIND FIRST qbuff WHERE qbuff.KEY = 38
    AND qbuff.number1 = vhp.h-bill-line.departement
    AND qbuff.number2 = vhp.h-bill-line.artnr NO-LOCK NO-ERROR.
  IF AVAILABLE qbuff THEN
  DO:
    IF descLength = 0 OR LENGTH(t-queasy.char3) LE descLength THEN
    t-queasy.char3 = t-queasy.char3 + STRING("","x(5)")
       + STRING(qbuff.char3) + CHR(10). 
    ELSE RUN write-descript(STRING("", "x(5)"), STRING(qbuff.char3)).
  END.

  IF vhp.h-bill-line.anzahl NE 0 /* AND vhp.h-artikel.aenderwunsch */ THEN 
  DO: 
    IF AVAILABLE vhp.h-journal AND vhp.h-journal.aendertext NE "" THEN 
      t-queasy.char3 = t-queasy.char3 + " ::: " 
      + vhp.h-journal.aendertext + CHR(10). 
    IF AVAILABLE vhp.h-journal AND vhp.h-journal.stornogrund NE "" THEN 
      t-queasy.char3 = t-queasy.char3 + " >>> " 
      + STRING(vhp.h-journal.stornogrund, "x(20)") + CHR(10). 
  END. 
 
  IF vhp.h-artikel.betriebsnr GT 0 THEN 
  DO: 
    FOR EACH submenu-list WHERE submenu-list.nr = vhp.h-artikel.betriebsnr 
      AND submenu-list.zeit = vhp.h-bill-line.zeit: 
      created = YES. 
      t-queasy.char3 = t-queasy.char3 + 
        "  -> " + STRING(submenu-list.bezeich) + CHR(10). 
      IF submenu-list.request NE "" THEN t-queasy.char3 
        = t-queasy.char3 + ":::" + submenu-list.request + CHR(10). 
      DELETE submenu-list. 
    END. 
    IF NOT created THEN 
    DO: 
      FIND FIRST vhp.h-journal WHERE vhp.h-journal.artnr = vhp.h-bill-line.artnr 
        AND vhp.h-journal.departement = dept 
        AND vhp.h-journal.rechnr = rechnr 
        AND vhp.h-journal.bill-datum = vhp.h-bill-line.bill-datum 
        AND vhp.h-journal.zeit = vhp.h-bill-line.zeit 
        AND vhp.h-journal.sysdate = vhp.h-bill-line.sysdate 
        AND vhp.h-journal.schankbuch = recid-h-bill-line /*FD June 13, 2022 => Ticket 431485*/  
        NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.h-journal THEN 
      FOR EACH h-mjourn WHERE h-mjourn.departement = dept 
        AND h-mjourn.h-artnr = vhp.h-journal.artnr 
        AND h-mjourn.rechnr = vhp.h-journal.rechnr 
        AND h-mjourn.bill-datum = vhp.h-journal.bill-datum 
        AND h-mjourn.sysdate = vhp.h-journal.sysdate 
        AND h-mjourn.zeit = vhp.h-journal.zeit NO-LOCK: 
        FIND FIRST h-art WHERE h-art.artnr = h-mjourn.artnr 
          AND h-art.departement = dept NO-LOCK NO-ERROR. 
        IF AVAILABLE h-art THEN 
        DO: 
          created = YES. 
          t-queasy.char3 = t-queasy.char3 + 
            "  -> " + STRING(h-art.bezeich) + CHR(10). 
          IF h-mjourn.request NE "" THEN t-queasy.char3 
            = t-queasy.char3 + ":::" + h-mjourn.request + CHR(10). 
        END. 
      END. 
    END. 
  END. 
  IF created THEN t-queasy.char3 = t-queasy.char3 + " " + CHR(10). 
  
  /*
  IF vhp.h-bill-line.anzahl LT 0 THEN 
  DO: 
    FIND FIRST vhp.printcod WHERE vhp.printcod.emu = vhp.printer.emu 
      AND vhp.printcod.code = "redpr-" NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.printcod THEN t-queasy.char3 = t-queasy.char3 
      + vhp.printcod.contcod. 
  END.*/ 
  MESSAGE t-queasy.char3 t-queasy.number1
      VIEW-AS ALERT-BOX INFO BUTTONS OK.
END. 
 
PROCEDURE write-descript:
DEF INPUT PARAM str1        AS CHAR.
DEF INPUT PARAM str2        AS CHAR.
DEFINE VARIABLE s1          AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE s2          AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE word        AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE next-line   AS LOGICAL         NO-UNDO.
DEFINE VARIABLE i           AS INTEGER         NO-UNDO.
DEFINE VARIABLE length1     AS INTEGER         NO-UNDO.

    t-queasy.char3 = t-queasy.char3 + str1.
    IF NUM-ENTRIES(str2, " ") = 1 THEN
    DO:
      IF ROUND(descLength / 2, 0) * 2 NE descLength THEN 
        length1 = descLength - 1.
      ELSE length1 = descLength.
      t-queasy.char3 = t-queasy.char3 + SUBSTR(str2, 1, length1) + CHR(10).
      DO i = 1 TO LENGTH(str1):
        t-queasy.char3 = t-queasy.char3 + " ".
      END.
      t-queasy.char3 = t-queasy.char3 + SUBSTR(str2, length1 + 1) + CHR(10).
    RETURN.
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
    t-queasy.char3 = t-queasy.char3 + s1 + CHR(10).
    DO i = 1 TO LENGTH(str1):
      t-queasy.char3 = t-queasy.char3 + " ".
    END.
    t-queasy.char3 = t-queasy.char3 + s2 + CHR(10).
END.

PROCEDURE cut-it:
DEF VAR i AS INTEGER.
  IF numcat1 = 0 THEN t-queasy.char3 = t-queasy.char3 + " " 
    + CHR(10) + CHR(10) + " " + CHR(10) + " " + CHR(10). 
  ELSE
  DO i = 1 TO numcat1:
    t-queasy.char3 = t-queasy.char3 + " " + CHR(10). 
  END.

  FIND FIRST vhp.printcod WHERE vhp.printcod.emu = vhp.printer.emu 
    AND vhp.printcod.code = "cut" NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.printcod THEN 
  DO: 
      t-queasy.char3 = t-queasy.char3 + vhp.printcod.contcod + CHR(10). 
  END. 
  ELSE 
  DO:
    IF numcat2 = 0 THEN
    t-queasy.char3 = t-queasy.char3 + " " + CHR(10) + " " + CHR(10) 
      + " " +  CHR(10) + " " + CHR(10) + " " + CHR(10). 
    ELSE
    DO i = 1 TO numcat2:
      t-queasy.char3 = t-queasy.char3 + " " + CHR(10).
    END.
  END.
END. 
 
PROCEDURE readSession: 
    DEFINE VARIABLE  lvCTmp AS CHARACTER            NO-UNDO. 
    DEFINE VARIABLE lvCLeft AS CHARACTER            NO-UNDO. 
    DEFINE VARIABLE lvCVal AS CHARACTER             NO-UNDO. 
    DEFINE VARIABLE lvICnt AS INTEGER               NO-UNDO. 
    DEFINE VARIABLE lvI AS INTEGER                  NO-UNDO. 
    DEFINE VARIABLE lvITmp AS INTEGER               NO-UNDO. 
    DEFINE VARIABLE i      AS INTEGER               NO-UNDO. 
 
    lvICnt = NUM-ENTRIES(session-parameter, ";"). 
    DO lvI = 1 TO lvICnt: 
        ASSIGN 
            lvCTmp  = "" 
            lvCLeft = "" 
        . 
 
        lvCtmp = TRIM(ENTRY(lvI, session-parameter, ";")). 
        lvCLeft = TRIM(ENTRY(1, lvCTmp, "=")) NO-ERROR. 
 
        CASE lvCLeft: 
            WHEN "kpr1" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                kitchen-pr[1] = INTEGER(lvCVAL). 
            END. 
            WHEN "kpr2" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                kitchen-pr[2] = INTEGER(lvCVAL). 
            END. 
            WHEN "kpr3" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                kitchen-pr[3] = INTEGER(lvCVAL). 
            END. 
            WHEN "kpr4" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                kitchen-pr[4] = INTEGER(lvCVAL). 
            END. 
            WHEN "kpr5" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                kitchen-pr[5] = INTEGER(lvCVAL). 
            END. 
            WHEN "kpr6" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                kitchen-pr[6] = INTEGER(lvCVAL). 
            END. 
            WHEN "kpr7" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                kitchen-pr[7] = INTEGER(lvCVAL). 
            END. 
            WHEN "kpr8" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                kitchen-pr[8] = INTEGER(lvCVAL). 
            END. 
            WHEN "kpr9" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                kitchen-pr[9] = INTEGER(lvCVAL). 
            END. 
            WHEN "DesLen" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                DescLength = INTEGER(lvCVAL). 
            END. 
            WHEN "PrSubgrp" THEN DO: 
                IF TRIM(ENTRY(2, lvCTmp, "=")) = "NO" 
                    THEN print-subgrp = NO.
            END. 
            WHEN "PrSingle" THEN DO: 
                IF TRIM(ENTRY(2, lvCTmp, "=")) = "YEs" 
                    THEN print-single = YES.
            END. 
            WHEN "printer-loc" THEN DO: 
                lvCVal = TRIM(ENTRY(2, lvCTmp, "=")). 
                printer-loc = lvCVAL.
            END. 
        END CASE.
    END. 
 
    DO i = 1 TO 9: 
      IF kitchen-pr[i] NE 0 THEN 
      DO: 
        FIND FIRST PRINTER WHERE PRINTER.nr = kitchen-pr[i] NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE PRINTER THEN 
        DO: 
          error-str = error-str + translateExtended ("Kitchen Printer Number",lvCAREA,"")
            + " " + STRING(kitchen-pr[i]) + " " 
            + translateExtended ("not found (wrong parameter startup).",lvCAREA,"")
            + CHR(10).
          STOP. 
        END. 
      END. 
    END. 
    kitchen-pr[10] = 1. 
 
END PROCEDURE. 
 
PROCEDURE get-printer-number: 
  CASE vhp.PRINTER.path: 
      WHEN "KPR1" THEN DO: 
        FIND FIRST vhp.printer WHERE vhp.printer.nr = kitchen-pr[1] NO-LOCK. 
        RETURN. 
      END. 
      WHEN "KPR2" THEN DO: 
        FIND FIRST vhp.printer WHERE vhp.printer.nr = kitchen-pr[2] NO-LOCK. 
        RETURN. 
      END. 
      WHEN "KPR3" THEN DO: 
        FIND FIRST vhp.printer WHERE vhp.printer.nr = kitchen-pr[3] NO-LOCK. 
        RETURN. 
      END. 
      WHEN "KPR4" THEN DO: 
        FIND FIRST vhp.printer WHERE vhp.printer.nr = kitchen-pr[4] NO-LOCK. 
        RETURN. 
      END. 
      WHEN "KPR5" THEN DO: 
        FIND FIRST vhp.printer WHERE vhp.printer.nr = kitchen-pr[5] NO-LOCK. 
        RETURN. 
      END. 
      WHEN "KPR6" THEN DO: 
        FIND FIRST vhp.printer WHERE vhp.printer.nr = kitchen-pr[6] NO-LOCK. 
        RETURN. 
      END. 
      WHEN "KPR7" THEN DO: 
        FIND FIRST vhp.printer WHERE vhp.printer.nr = kitchen-pr[7] NO-LOCK. 
        RETURN. 
      END. 
      WHEN "KPR8" THEN DO: 
        FIND FIRST vhp.printer WHERE vhp.printer.nr = kitchen-pr[8] NO-LOCK. 
        RETURN. 
      END. 
      WHEN "KPR9" THEN DO: 
        FIND FIRST vhp.printer WHERE vhp.printer.nr = kitchen-pr[9] NO-LOCK. 
        RETURN. 
      END. 
  END CASE. 
 
END PROCEDURE. 
