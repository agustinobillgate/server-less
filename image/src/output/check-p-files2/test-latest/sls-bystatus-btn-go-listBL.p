
DEFINE TEMP-TABLE p-list 
  FIELD pnr AS INTEGER INITIAL 0 
  FIELD sflag AS INTEGER
  FIELD pcomp AS CHAR FORMAT "x(50)" 
  FIELD pcont AS CHAR FORMAT "x(25)"
  FIELD pname AS CHAR FORMAT "x(25)"
  FIELD pntot AS CHAR FORMAT "x(15)"
  FIELD pnam1 AS CHAR FORMAT "x(15)"
  FIELD pnam2 AS CHAR FORMAT "x(15)"
  FIELD pnam3 AS CHAR FORMAT "x(15)"
  FIELD pnam4 AS CHAR FORMAT "x(15)"
  FIELD pamt  AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt1 AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt2 AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt3 AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt4 AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD patot AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt-str AS CHARACTER FORMAT "x(16)"
  FIELD stnr  AS INT FORMAT ">9"
  FIELD stage  AS CHAR FORMAT "x(25)"
  FIELD proz  AS CHAR FORMAT "x(4)"
  FIELD popen AS DATE FORMAT "99/99/99"
  FIELD pfnsh AS DATE FORMAT "99/99/99"
  FIELD pmain1 AS CHAR FORMAT "x(15)"
  FIELD pmain2 AS CHAR FORMAT "x(15)"
  FIELD pmain3 AS CHAR FORMAT "x(15)"
  FIELD reason AS CHAR FORMAT "x(15)"
  FIELD refer  AS CHAR FORMAT "x(15)"
  FIELD pid AS CHAR FORMAT "x(3)"
  FIELD pcid AS CHAR FORMAT "x(3)"
  FIELD ctotal AS INT FORMAT ">>>>>"
  FIELD stat-flag AS CHAR FORMAT "x(15)".

DEFINE TEMP-TABLE slstatus-list 
  FIELD pnr AS INTEGER INITIAL 0 
  FIELD sflag AS INTEGER
  FIELD pcomp AS CHAR FORMAT "x(50)" 
  FIELD pcont AS CHAR FORMAT "x(25)"
  FIELD pname AS CHAR FORMAT "x(25)"
  FIELD pntot AS CHAR FORMAT "x(15)"
  FIELD pnam1 AS CHAR FORMAT "x(15)"
  FIELD pnam2 AS CHAR FORMAT "x(15)"
  FIELD pnam3 AS CHAR FORMAT "x(15)"
  FIELD pnam4 AS CHAR FORMAT "x(15)"
  FIELD pamt  AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt1 AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt2 AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt3 AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt4 AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD patot AS DECIMAL FORMAT ">>>,>>>,>>9.99"
  FIELD pamt-str AS CHARACTER FORMAT "x(16)"
  FIELD stnr  AS INT FORMAT ">9"
  FIELD stage  AS CHAR FORMAT "x(25)"
  FIELD proz  AS CHAR FORMAT "x(4)"
  FIELD popen AS DATE FORMAT "99/99/99"
  FIELD pfnsh AS DATE FORMAT "99/99/99"
  FIELD pmain1 AS CHAR FORMAT "x(15)"
  FIELD pmain2 AS CHAR FORMAT "x(15)"
  FIELD pmain3 AS CHAR FORMAT "x(15)"
  FIELD reason AS CHAR FORMAT "x(15)"
  FIELD refer  AS CHAR FORMAT "x(15)"
  FIELD pid AS CHAR FORMAT "x(3)"
  FIELD pcid AS CHAR FORMAT "x(3)"
  FIELD ctotal AS INT FORMAT ">>>>>"
  FIELD stat-flag AS CHAR FORMAT "x(15)".

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER next-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER all-flag       AS LOGICAL.
DEF INPUT  PARAMETER usr-init       AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR slstatus-list.
/* For Testing BL
DEF VARIABLE  pvILanguage AS INTEGER NO-UNDO INIT 1.
DEF VARIABLE  next-date AS DATE INIT ?.
DEF VARIABLE  to-date AS DATE INIT ?.
DEF VARIABLE  all-flag AS LOGICAL INIT YES.
DEF VARIABLE  usr-init AS CHAR INIT "01".
*/
DEF VARIABLE s-flag AS CHAR EXTENT 4.
s-flag[1] = "Open".
s-flag[2] = "Close-Won".
s-flag[3] = "Close-Lost".
s-flag[4] = "Inactive".

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "sls-bystatus".

IF next-date NE ? AND to-date NE ? THEN
RUN browse-open2.
ELSE
RUN browse-open1.

PROCEDURE browse-open1:
DEFINE VAR i    AS INTEGER. 
DEFINE VAR nr   AS INT.
DEFINE VAR hnr  AS INT.
DEFINE VAR tamt AS DEC.
DEFINE VAR amt  AS DEC.

DEF BUFFER akt-code1    FOR akt-code.
DEF BUFFER guest1       FOR guest.
DEF BUFFER akthdr1      FOR akthdr.
DEF BUFFER akt-kont1    FOR akt-kont.
DEF BUFFER buf-akthdr   FOR akthdr.

  FOR EACH p-list:
    DELETE p-list.
  END.

  FOR EACH slstatus-list:
    DELETE slstatus-list.
  END.

  IF all-flag THEN
  DO:
    nr = 0.
    DO i = 1 TO 4:
      s-flag[i].
      FIND FIRST akthdr1 WHERE akthdr1.flag = i NO-LOCK NO-ERROR.
      IF AVAILABLE akthdr1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.stat-flag = STRING(nr,">9") + " - " + s-flag[i].

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH akthdr1 WHERE akthdr1.flag = i NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = akthdr1.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
          AND akt-kont1.kontakt-nr = akthdr1.kontakt-nr NO-LOCK
          BY akthdr1.stufe BY guest1.NAME:

          CREATE p-list.
          ASSIGN
            p-list.pnr   = akthdr1.aktnr
            p-list.sflag = akthdr1.flag
            p-list.pcomp = guest1.NAME + ", " + guest1.anredefirma
            p-list.pcont = akt-kont1.name + ", " + akt-kont1.vorname + " " + akt-kont1.anrede
            p-list.pname = akthdr1.bezeich
            p-list.pntot = akthdr1.stichwort
            p-list.pamt1 = akthdr1.amount[1]
            p-list.pamt2 = akthdr1.amount[2]
            p-list.pamt3 = akthdr1.amount[3]
            p-list.pamt4 = akthdr1.amount[4]
            p-list.pamt  = p-list.pamt1 + p-list.pamt2 + p-list.pamt3
            p-list.pamt-str = STRING(p-list.pamt, ">,>>>,>>>,>>9.99")
            p-list.patot = akthdr1.t-betrag
            p-list.stnr  = akthdr1.stufe
            p-list.proz  = STRING(akthdr1.prozent, ">>9%")
            p-list.popen = akthdr1.next-datum
            p-list.pfnsh = akthdr1.erl-datum
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.

          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.
          
          IF akthdr1.stufe NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 2 
            AND akt-code1.aktionscode = akthdr1.stufe NO-LOCK NO-ERROR.
          p-list.stage  = akt-code1.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF akthdr1.product[1] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[1] NO-LOCK NO-ERROR.
          p-list.pnam1 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam1 = " ".
        
          IF akthdr1.product[2] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[2] NO-LOCK NO-ERROR.
          p-list.pnam2 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam2 = " ".
        
          IF akthdr1.product[3] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[3] NO-LOCK NO-ERROR.
          p-list.pnam3 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam3 = " ".
        
          IF akthdr1.product[4] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[4] NO-LOCK NO-ERROR.
          p-list.pnam4 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam4 = " ".
        
          IF akthdr1.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF akthdr1.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF akthdr1.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF akthdr1.grund NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 5 
            AND akt-code1.aktionscode = akthdr1.grund NO-LOCK NO-ERROR.
          p-list.reason = akt-code1.bezeich.
          END.
          
          IF akthdr1.referred NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 6 
            AND akt-code1.aktionscode = akthdr1.referred NO-LOCK NO-ERROR.
          p-list.refer = akt-code1.bezeich.
          END.
          /*ctotal = n + 1.*/
        END.
        
        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL " + STRING(s-flag[i], "x(10)") + " Opportunity : " + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.
    END.
    RUN fill-status.
  END.     
  ELSE
  DO:
    nr = 0.
    DO i = 1 TO 4:
      s-flag[i].
      FIND FIRST akthdr1 WHERE akthdr1.flag = i 
        AND akthdr1.userinit = usr-init NO-LOCK NO-ERROR.
      IF AVAILABLE akthdr1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.stat-flag = STRING(nr,">9") + " - " + s-flag[i].

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH akthdr1 WHERE akthdr1.flag = i AND akthdr1.userinit = usr-init NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = akthdr1.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
          AND akt-kont1.kontakt-nr = akthdr1.kontakt-nr NO-LOCK
          BY akthdr1.stufe BY guest1.NAME:

          CREATE p-list.
          ASSIGN
            p-list.pnr   = akthdr1.aktnr
            p-list.sflag = akthdr1.flag
            p-list.pcomp = guest1.NAME + ", " + guest1.anredefirma
            p-list.pcont = akt-kont1.name + ", " + akt-kont1.vorname + " " + akt-kont1.anrede
            p-list.pname = akthdr1.bezeich
            p-list.pntot = akthdr1.stichwort
            p-list.pamt1 = akthdr1.amount[1]
            p-list.pamt2 = akthdr1.amount[2]
            p-list.pamt3 = akthdr1.amount[3]
            p-list.pamt4 = akthdr1.amount[4]
            p-list.pamt  = p-list.pamt1 + p-list.pamt2 + p-list.pamt3
            p-list.pamt-str = STRING(p-list.pamt, ">,>>>,>>>,>>9.99")
            p-list.patot = akthdr1.t-betrag
            p-list.stnr  = akthdr1.stufe
            p-list.proz  = STRING(akthdr1.prozent, ">>9%")
            p-list.popen = akthdr1.next-datum
            p-list.pfnsh = akthdr1.erl-datum
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.

          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.
          
          IF akthdr1.stufe NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 2 
            AND akt-code1.aktionscode = akthdr1.stufe NO-LOCK NO-ERROR.
          p-list.stage  = akt-code1.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF akthdr1.product[1] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[1] NO-LOCK NO-ERROR.
          p-list.pnam1 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam1 = " ".
        
          IF akthdr1.product[2] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[2] NO-LOCK NO-ERROR.
          p-list.pnam2 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam2 = " ".
        
          IF akthdr1.product[3] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[3] NO-LOCK NO-ERROR.
          p-list.pnam3 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam3 = " ".
        
          IF akthdr1.product[4] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[4] NO-LOCK NO-ERROR.
          p-list.pnam4 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam4 = " ".
        
          IF akthdr1.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF akthdr1.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF akthdr1.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF akthdr1.grund NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 5 
            AND akt-code1.aktionscode = akthdr1.grund NO-LOCK NO-ERROR.
          p-list.reason = akt-code1.bezeich.
          END.
          
          IF akthdr1.referred NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 6 
            AND akt-code1.aktionscode = akthdr1.referred NO-LOCK NO-ERROR.
          p-list.refer = akt-code1.bezeich.
          END.
          /*ctotal = n + 1.*/
        END.

        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL " + STRING(s-flag[i], "x(10)") + " Opportunity : " + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.
    END.
    RUN fill-status.
  END.
END PROCEDURE.

PROCEDURE browse-open2:
DEFINE VAR i    AS INTEGER. 
DEFINE VAR nr   AS INT.
DEFINE VAR hnr  AS INT.
DEFINE VAR tamt AS DEC.
DEFINE VAR amt  AS DEC.

DEF BUFFER akt-code1    FOR akt-code.
DEF BUFFER guest1       FOR guest.
DEF BUFFER akthdr1      FOR akthdr.
DEF BUFFER akt-kont1    FOR akt-kont.
DEF BUFFER buf-akthdr   FOR akthdr.

  FOR EACH p-list:
    DELETE p-list.
  END.

  FOR EACH slstatus-list:
    DELETE slstatus-list.
  END.

  IF all-flag THEN
  DO:
    nr = 0.
    DO i = 1 TO 4:
      s-flag[i].
      FIND FIRST akthdr1 WHERE akthdr1.flag = i
        AND akthdr1.next-datum GE next-date AND akthdr1.next-datum LE to-date NO-LOCK NO-ERROR.
      IF AVAILABLE akthdr1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.stat-flag = STRING(nr,">9") + " - " + s-flag[i].

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH akthdr1 WHERE akthdr1.flag = i
          AND akthdr1.next-datum GE next-date AND akthdr1.next-datum LE to-date NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = akthdr1.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
          AND akt-kont1.kontakt-nr = akthdr1.kontakt-nr NO-LOCK
          BY akthdr1.stufe BY guest1.NAME:

          CREATE p-list.
          ASSIGN
            p-list.pnr   = akthdr1.aktnr
            p-list.sflag = akthdr1.flag
            p-list.pcomp = guest1.NAME + ", " + guest1.anredefirma
            p-list.pcont = akt-kont1.name + ", " + akt-kont1.vorname + " " + akt-kont1.anrede
            p-list.pname = akthdr1.bezeich
            p-list.pntot = akthdr1.stichwort
            p-list.pamt1 = akthdr1.amount[1]
            p-list.pamt2 = akthdr1.amount[2]
            p-list.pamt3 = akthdr1.amount[3]
            p-list.pamt4 = akthdr1.amount[4]
            p-list.pamt  = p-list.pamt1 + p-list.pamt2 + p-list.pamt3
            p-list.pamt-str = STRING(p-list.pamt, ">,>>>,>>>,>>9.99")
            p-list.patot = akthdr1.t-betrag
            p-list.stnr  = akthdr1.stufe
            p-list.proz  = STRING(akthdr1.prozent, ">>9%")
            p-list.popen = akthdr1.next-datum
            p-list.pfnsh = akthdr1.erl-datum
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.

          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.
          
          IF akthdr1.stufe NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 2 
            AND akt-code1.aktionscode = akthdr1.stufe NO-LOCK NO-ERROR.
          p-list.stage  = akt-code1.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF akthdr1.product[1] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[1] NO-LOCK NO-ERROR.
          p-list.pnam1 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam1 = " ".
        
          IF akthdr1.product[2] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[2] NO-LOCK NO-ERROR.
          p-list.pnam2 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam2 = " ".
        
          IF akthdr1.product[3] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[3] NO-LOCK NO-ERROR.
          p-list.pnam3 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam3 = " ".
        
          IF akthdr1.product[4] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[4] NO-LOCK NO-ERROR.
          p-list.pnam4 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam4 = " ".
        
          IF akthdr1.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF akthdr1.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF akthdr1.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF akthdr1.grund NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 5 
            AND akt-code1.aktionscode = akthdr1.grund NO-LOCK NO-ERROR.
          p-list.reason = akt-code1.bezeich.
          END.
          
          IF akthdr1.referred NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 6 
            AND akt-code1.aktionscode = akthdr1.referred NO-LOCK NO-ERROR.
          p-list.refer = akt-code1.bezeich.
          END.
          /*ctotal = n + 1.*/
        END.

        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL " + STRING(s-flag[i], "x(10)") + " Opportunity : " + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.
    END.
    RUN fill-status.
  END.     
  ELSE
  DO:
    nr = 0.
    DO i = 1 TO 4:
      s-flag[i].
      FIND FIRST akthdr1 WHERE akthdr1.flag = i AND akthdr1.userinit = usr-init 
        AND akthdr1.next-datum GE next-date AND akthdr1.next-datum LE to-date NO-LOCK NO-ERROR.
      IF AVAILABLE akthdr1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.stat-flag = STRING(nr,">9") + " - " + s-flag[i].

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH akthdr1 WHERE akthdr1.flag = i AND akthdr1.userinit = usr-init 
          AND akthdr1.next-datum GE next-date AND akthdr1.next-datum LE to-date NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = akthdr1.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
          AND akt-kont1.kontakt-nr = akthdr1.kontakt-nr NO-LOCK
          BY akthdr1.stufe BY guest1.NAME:

          CREATE p-list.
          ASSIGN
            p-list.pnr   = akthdr1.aktnr
            p-list.sflag = akthdr1.flag
            p-list.pcomp = guest1.NAME + ", " + guest1.anredefirma
            p-list.pcont = akt-kont1.name + ", " + akt-kont1.vorname + " " + akt-kont1.anrede
            p-list.pname = akthdr1.bezeich
            p-list.pntot = akthdr1.stichwort
            p-list.pamt1 = akthdr1.amount[1]
            p-list.pamt2 = akthdr1.amount[2]
            p-list.pamt3 = akthdr1.amount[3]
            p-list.pamt4 = akthdr1.amount[4]
            p-list.pamt  = p-list.pamt1 + p-list.pamt2 + p-list.pamt3
            p-list.pamt-str = STRING(p-list.pamt, ">,>>>,>>>,>>9.99")
            p-list.patot = akthdr1.t-betrag
            p-list.stnr  = akthdr1.stufe
            p-list.proz  = STRING(akthdr1.prozent, ">>9%")
            p-list.popen = akthdr1.next-datum
            p-list.pfnsh = akthdr1.erl-datum
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.

          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.
          
          IF akthdr1.stufe NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 2 
            AND akt-code1.aktionscode = akthdr1.stufe NO-LOCK NO-ERROR.
          p-list.stage  = akt-code1.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF akthdr1.product[1] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[1] NO-LOCK NO-ERROR.
          p-list.pnam1 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam1 = " ".
        
          IF akthdr1.product[2] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[2] NO-LOCK NO-ERROR.
          p-list.pnam2 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam2 = " ".
        
          IF akthdr1.product[3] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[3] NO-LOCK NO-ERROR.
          p-list.pnam3 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam3 = " ".
        
          IF akthdr1.product[4] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 3 
            AND akt-code1.aktionscode = akthdr1.product[4] NO-LOCK NO-ERROR.
          p-list.pnam4 = akt-code1.bezeich.
          END.
          ELSE p-list.pnam4 = " ".
        
          IF akthdr1.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF akthdr1.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF akthdr1.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 4 
            AND akt-code1.aktionscode = akthdr1.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = akt-code1.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF akthdr1.grund NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 5 
            AND akt-code1.aktionscode = akthdr1.grund NO-LOCK NO-ERROR.
          p-list.reason = akt-code1.bezeich.
          END.
          
          IF akthdr1.referred NE 0 THEN
          DO:
          FIND FIRST akt-code1 WHERE akt-code1.aktiongrup = 6 
            AND akt-code1.aktionscode = akthdr1.referred NO-LOCK NO-ERROR.
          p-list.refer = akt-code1.bezeich.
          END.
          /*ctotal = n + 1.*/
        END.

        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL " + STRING(s-flag[i], "x(10)") + " Opportunity : " + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.
    END.
    RUN fill-status.
  END.
END PROCEDURE.

PROCEDURE fill-status:
  FOR EACH p-list:
    CREATE slstatus-list.
    BUFFER-COPY p-list TO slstatus-list.
  END.
END PROCEDURE.
