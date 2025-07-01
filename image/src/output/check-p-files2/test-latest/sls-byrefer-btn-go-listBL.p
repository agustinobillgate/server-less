
DEFINE TEMP-TABLE p-list 
  FIELD pnr AS INTEGER INITIAL 0 
  FIELD sflag AS INTEGER
  FIELD refer-name AS CHAR FORMAT "x(25)"
  FIELD pcomp AS CHAR FORMAT "x(50)" 
  FIELD pcont AS CHAR FORMAT "x(25)"
  FIELD pname AS CHAR FORMAT "x(25)"
  FIELD pntot AS CHAR FORMAT "x(15)"
  FIELD pnam1 AS INT FORMAT ">9"
  FIELD pnam2 AS INT FORMAT ">9"
  FIELD pnam3 AS INT FORMAT ">9"
  FIELD pnam4 AS INT FORMAT ">9"
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
  FIELD refer  AS INT FORMAT ">>"
  FIELD pid AS CHAR FORMAT "x(3)"
  FIELD pcid AS CHAR FORMAT "x(3)"
  FIELD ctotal AS INT FORMAT ">>>>>".

DEFINE TEMP-TABLE slrefer-list 
  FIELD pnr AS INTEGER INITIAL 0 
  FIELD sflag AS INTEGER
  FIELD refer-name AS CHAR FORMAT "x(25)"
  FIELD pcomp AS CHAR FORMAT "x(50)" 
  FIELD pcont AS CHAR FORMAT "x(25)"
  FIELD pname AS CHAR FORMAT "x(25)"
  FIELD pntot AS CHAR FORMAT "x(15)"
  FIELD pnam1 AS INT FORMAT ">9"
  FIELD pnam2 AS INT FORMAT ">9"
  FIELD pnam3 AS INT FORMAT ">9"
  FIELD pnam4 AS INT FORMAT ">9"
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
  FIELD refer  AS INT FORMAT ">>"
  FIELD pid AS CHAR FORMAT "x(3)"
  FIELD pcid AS CHAR FORMAT "x(3)"
  FIELD ctotal AS INT FORMAT ">>>>>".

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER next-date AS DATE.
DEF INPUT  PARAMETER to-date AS DATE.
DEF INPUT  PARAMETER all-flag AS LOGICAL.
DEF INPUT  PARAMETER usr-init AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR slrefer-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "sls-byrefer".

IF  next-date NE ? AND to-date NE ?THEN
RUN browse-open2.
ELSE
RUN browse-open1.

PROCEDURE browse-open1: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VAR nr AS INT.
DEFINE VAR hnr AS INT.
DEFINE VAR tamt AS DEC.
DEFINE VAR amt AS DEC.
DEFINE VAR flag AS LOGICAL INITIAL YES.
DEF VAR lname AS CHAR.
DEF VAR kname AS CHAR. 

DEF BUFFER akt-code1    FOR akt-code.
DEF BUFFER buf-aktcode  FOR akt-code.
DEF BUFFER guest1       FOR guest.
DEF BUFFER akthdr1      FOR akthdr.
DEF BUFFER akt-kont1    FOR akt-kont.
DEF BUFFER buf-akthdr   FOR akthdr.

  FOR EACH p-list:
    DELETE p-list.
  END.

  FOR EACH slrefer-list:
    DELETE slrefer-list.
  END.

  IF all-flag THEN
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 6 NO-LOCK,
      FIRST buf-akthdr WHERE buf-akthdr.referred = akt-code1.aktionscode 
        AND buf-akthdr.referred NE 0 NO-LOCK BY akt-code1.aktionscode:
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.refer-name = STRING(nr, ">9") + " - " + akt-code1.bezeich.

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH akthdr1 WHERE akthdr1.referred = akt-code1.aktionscode NO-LOCK,
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
            p-list.pnam1 = akthdr1.product[1]
            p-list.pnam2 = akthdr1.product[2]
            p-list.pnam3 = akthdr1.product[3]
            p-list.pnam4 = akthdr1.product[4]
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
            p-list.refer = akthdr1.referred
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.

          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.

          IF akthdr1.stufe NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 2 
            AND buf-aktcode.aktionscode = akthdr1.stufe NO-LOCK NO-ERROR.
          p-list.stage  = buf-aktcode.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF akthdr1.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF akthdr1.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF akthdr1.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF akthdr1.grund NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 5 
            AND buf-aktcode.aktionscode = akthdr1.grund NO-LOCK NO-ERROR.
          p-list.reason = buf-aktcode.bezeich.
          END.          
         /* ctotal = n + 1.*/
        END.
        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL " + STRING(akt-code1.bezeich, "x(25)") + ":" + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.
    END.
    RUN fill-refer.
  END.
  ELSE
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 6 NO-LOCK,
      FIRST buf-akthdr WHERE buf-akthdr.referred = akt-code1.aktionscode 
        AND buf-akthdr.referred NE 0 AND buf-akthdr.userinit = usr-init
      NO-LOCK BY akt-code1.aktionscode:
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.refer-name = STRING(nr, ">9") + " - " + akt-code1.bezeich.

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH akthdr1 WHERE akthdr1.referred = akt-code1.aktionscode 
          AND akthdr1.userinit = usr-init NO-LOCK,
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
            p-list.pnam1 = akthdr1.product[1]
            p-list.pnam2 = akthdr1.product[2]
            p-list.pnam3 = akthdr1.product[3]
            p-list.pnam4 = akthdr1.product[4]
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
            p-list.refer = akthdr1.referred
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.

          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.

          IF akthdr1.stufe NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 2 
            AND buf-aktcode.aktionscode = akthdr1.stufe NO-LOCK NO-ERROR.
          p-list.stage  = buf-aktcode.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF akthdr1.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF akthdr1.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF akthdr1.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF akthdr1.grund NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 5 
            AND buf-aktcode.aktionscode = akthdr1.grund NO-LOCK NO-ERROR.
          p-list.reason = buf-aktcode.bezeich.
          END.          
         /* ctotal = n + 1.*/
        END.
        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL " + STRING(akt-code1.bezeich, "x(25)") + ":" + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.
    END.
    RUN fill-refer.
  END.
END PROCEDURE.

PROCEDURE browse-open2: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VAR nr AS INT.
DEFINE VAR hnr AS INT.
DEFINE VAR tamt AS DEC.
DEFINE VAR amt AS DEC.
DEFINE VAR flag AS LOGICAL INITIAL YES.
DEF VAR lname AS CHAR.
DEF VAR kname AS CHAR. 

DEF BUFFER akt-code1    FOR akt-code.
DEF BUFFER buf-aktcode  FOR akt-code.
DEF BUFFER guest1       FOR guest.
DEF BUFFER akthdr1      FOR akthdr.
DEF BUFFER akt-kont1    FOR akt-kont.
DEF BUFFER buf-akthdr   FOR akthdr.

  FOR EACH p-list:
    DELETE p-list.
  END.

  FOR EACH slrefer-list:
    DELETE slrefer-list.
  END.

  IF all-flag THEN
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 6 NO-LOCK,
      FIRST buf-akthdr WHERE buf-akthdr.referred = akt-code1.aktionscode AND buf-akthdr.referred NE 0 
        AND buf-akthdr.next-datum GE next-date AND buf-akthdr.next-datum LE to-date NO-LOCK 
      BY akt-code1.aktionscode:
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.refer-name = STRING(nr, ">9") + " - " + akt-code1.bezeich.

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH akthdr1 WHERE akthdr1.referred = akt-code1.aktionscode 
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
            p-list.pnam1 = akthdr1.product[1]
            p-list.pnam2 = akthdr1.product[2]
            p-list.pnam3 = akthdr1.product[3]
            p-list.pnam4 = akthdr1.product[4]
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
            p-list.refer = akthdr1.referred
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.

          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.

          IF akthdr1.stufe NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 2 
            AND buf-aktcode.aktionscode = akthdr1.stufe NO-LOCK NO-ERROR.
          p-list.stage  = buf-aktcode.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF akthdr1.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF akthdr1.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF akthdr1.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF akthdr1.grund NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 5 
            AND buf-aktcode.aktionscode = akthdr1.grund NO-LOCK NO-ERROR.
          p-list.reason = buf-aktcode.bezeich.
          END.          
         /* ctotal = n + 1.*/
        END.
        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL " + STRING(akt-code1.bezeich, "x(25)") + ":" + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.
    END.
    RUN fill-refer.
  END.
  ELSE
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 6 NO-LOCK,
      FIRST buf-akthdr WHERE buf-akthdr.referred = akt-code1.aktionscode 
        AND buf-akthdr.referred NE 0 AND buf-akthdr.userinit = usr-init
        AND buf-akthdr.next-datum GE next-date 
        AND buf-akthdr.next-datum LE to-date NO-LOCK 
      BY akt-code1.aktionscode:
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.refer-name = STRING(nr, ">9") + " - " + akt-code1.bezeich.

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH akthdr1 WHERE akthdr1.referred = akt-code1.aktionscode AND akthdr1.userinit = usr-init 
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
            p-list.pnam1 = akthdr1.product[1]
            p-list.pnam2 = akthdr1.product[2]
            p-list.pnam3 = akthdr1.product[3]
            p-list.pnam4 = akthdr1.product[4]
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
            p-list.refer = akthdr1.referred
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.

          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.

          IF akthdr1.stufe NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 2 
            AND buf-aktcode.aktionscode = akthdr1.stufe NO-LOCK NO-ERROR.
          p-list.stage  = buf-aktcode.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF akthdr1.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF akthdr1.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF akthdr1.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = akthdr1.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF akthdr1.grund NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 5 
            AND buf-aktcode.aktionscode = akthdr1.grund NO-LOCK NO-ERROR.
          p-list.reason = buf-aktcode.bezeich.
          END.          
         /* ctotal = n + 1.*/
        END.
        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL " + STRING(akt-code1.bezeich, "x(25)") + ":" + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.
    END.
    RUN fill-refer.
  END.
END PROCEDURE.

PROCEDURE fill-refer:
  FOR EACH p-list:
    CREATE slrefer-list.
    BUFFER-COPY p-list TO slrefer-list.
  END.
END PROCEDURE.
