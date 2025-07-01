
DEFINE TEMP-TABLE p-list 
  FIELD pnr AS INTEGER INITIAL 0 
  FIELD sflag AS INTEGER
  FIELD code-name AS CHAR FORMAT "x(28)"
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
  FIELD stage  AS INT FORMAT ">>9"
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
  FIELD ctotal AS INT FORMAT ">>>>>". 

DEFINE TEMP-TABLE slstage-list 
  FIELD pnr AS INTEGER INITIAL 0 
  FIELD sflag AS INTEGER
  FIELD code-name AS CHARACTER
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
  FIELD stage  AS INT FORMAT ">>9"
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
  FIELD ctotal AS INT FORMAT ">>>>>".

DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER next-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER all-flag        AS LOGICAL.
DEF INPUT PARAMETER usr-init        AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR slstage-list.
/* For Testing BL
DEF VARIABLE  pvILanguage AS INTEGER NO-UNDO INIT 1.
DEF VARIABLE  next-date AS DATE INIT ?.
DEF VARIABLE  to-date AS DATE INIT ?.
DEF VARIABLE  all-flag AS LOGICAL INIT NO.
DEF VARIABLE  usr-init AS CHAR INIT "01".
DEFINE VARIABLE p-width AS INTEGER INITIAL 100. 
*/
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "sls-bystage".

IF  next-date NE ? AND to-date NE ? THEN
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

DEF BUFFER akt-code1 FOR akt-code.
DEF BUFFER buf-aktcode FOR akt-code.
DEF BUFFER guest1 FOR guest.
DEF BUFFER akthdr1 FOR akthdr.
DEF BUFFER akt-kont1 FOR akt-kont.
DEF BUFFER buf-akthdr FOR akthdr.

  FOR EACH p-list:
    DELETE p-list.
  END.

  FOR EACH slstage-list:
    DELETE slstage-list.
  END.

  IF all-flag THEN
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 2 NO-LOCK,
      FIRST buf-akthdr WHERE buf-akthdr.stufe = akt-code1.aktionscode 
      AND buf-akthdr.flag = 1 NO-LOCK BY akt-code1.aktionscode:
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        p-list.code-name = STRING(nr, ">9") + " - " + akt-code1.bezeich.
       
        hnr  = 0.
        amt  = 0.
        tamt = 0.
       
        FOR EACH akthdr1 WHERE akthdr1.stufe = akt-code1.aktionscode 
          AND akthdr1.flag = 1 NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = akthdr1.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
          AND akt-kont1.kontakt-nr = akthdr1.kontakt-nr NO-LOCK 
          BY guest1.NAME:         
          
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
            p-list.stage = akthdr1.stufe
            p-list.proz  = STRING(akthdr1.prozent, ">>9%")
            p-list.popen = akthdr1.next-datum
            p-list.pfnsh = akthdr1.erl-datum
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.
            
          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.
       
          IF akthdr1.product[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[1] NO-LOCK NO-ERROR.
          p-list.pnam1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam1 = " ".
        
          IF akthdr1.product[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[2] NO-LOCK NO-ERROR.
          p-list.pnam2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam2 = " ".
        
          IF akthdr1.product[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[3] NO-LOCK NO-ERROR.
          p-list.pnam3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam3 = " ".
        
          IF akthdr1.product[4] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[4] NO-LOCK NO-ERROR.
          p-list.pnam4 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam4 = " ".
        
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
          
          IF akthdr1.referred NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 6 
            AND buf-aktcode.aktionscode = akthdr1.referred NO-LOCK NO-ERROR.
          p-list.refer = buf-aktcode.bezeich.
          END.
          /* ctotal = n + 1.*/  
        END.
        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL : " + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.                     
    END.
    RUN fill-stage.
  END.
  ELSE
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 2 NO-LOCK,
      FIRST buf-akthdr WHERE buf-akthdr.stufe = akt-code1.aktionscode 
      AND buf-akthdr.flag = 1 AND buf-akthdr.userinit = usr-init NO-LOCK 
      BY akt-code1.aktionscode:
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        p-list.code-name = STRING(nr, ">9") + " - " + akt-code1.bezeich.
       
        hnr  = 0.
        amt  = 0.
        tamt = 0.
       
        FOR EACH akthdr1 WHERE akthdr1.stufe = akt-code1.aktionscode 
          AND akthdr1.userinit = usr-init AND akthdr1.flag = 1 NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = akthdr1.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
          AND akt-kont1.kontakt-nr = akthdr1.kontakt-nr NO-LOCK 
          BY guest1.NAME:
          
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
            p-list.stage = akthdr1.stufe
            p-list.proz  = STRING(akthdr1.prozent, ">>9%")
            p-list.popen = akthdr1.next-datum
            p-list.pfnsh = akthdr1.erl-datum
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.
            
          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.
       
          IF akthdr1.product[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[1] NO-LOCK NO-ERROR.
          p-list.pnam1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam1 = " ".
        
          IF akthdr1.product[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[2] NO-LOCK NO-ERROR.
          p-list.pnam2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam2 = " ".
        
          IF akthdr1.product[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[3] NO-LOCK NO-ERROR.
          p-list.pnam3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam3 = " ".
        
          IF akthdr1.product[4] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[4] NO-LOCK NO-ERROR.
          p-list.pnam4 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam4 = " ".
        
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
          
          IF akthdr1.referred NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 6 
            AND buf-aktcode.aktionscode = akthdr1.referred NO-LOCK NO-ERROR.
          p-list.refer = buf-aktcode.bezeich.
          END.
          /* ctotal = n + 1.*/  
        END.
        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL : " + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.                 
    END.
    RUN fill-stage.
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

DEF BUFFER akt-code1 FOR akt-code.
DEF BUFFER buf-aktcode FOR akt-code.
DEF BUFFER guest1 FOR guest.
DEF BUFFER akthdr1 FOR akthdr.
DEF BUFFER akt-kont1 FOR akt-kont.
DEF BUFFER buf-akthdr FOR akthdr.

  FOR EACH p-list:
    DELETE p-list.
  END.

  FOR EACH slstage-list:
    DELETE slstage-list.
  END.

  IF all-flag THEN
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 2 NO-LOCK,
      FIRST buf-akthdr WHERE buf-akthdr.stufe = akt-code1.aktionscode AND buf-akthdr.flag = 1
      AND buf-akthdr.next-datum GE next-date AND buf-akthdr.next-datum LE to-date NO-LOCK
      BY akt-code1.aktionscode:
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        p-list.code-name = STRING(nr, ">9") + " - " + akt-code1.bezeich.
        
        hnr  = 0.
        amt  = 0.
        tamt = 0.
      
        FOR EACH akthdr1 WHERE akthdr1.stufe = akt-code1.aktionscode 
          AND akthdr1.flag = 1 AND akthdr1.next-datum GE next-date 
          AND akthdr1.next-datum LE to-date NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = akthdr1.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
          AND akt-kont1.kontakt-nr = akthdr1.kontakt-nr NO-LOCK 
          BY guest1.NAME:         
          
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
            p-list.stage = akthdr1.stufe
            p-list.proz  = STRING(akthdr1.prozent, ">>9%")
            p-list.popen = akthdr1.next-datum
            p-list.pfnsh = akthdr1.erl-datum
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.
            
          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.
      
          IF akthdr1.product[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[1] NO-LOCK NO-ERROR.
          p-list.pnam1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam1 = " ".
        
          IF akthdr1.product[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[2] NO-LOCK NO-ERROR.
          p-list.pnam2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam2 = " ".
        
          IF akthdr1.product[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[3] NO-LOCK NO-ERROR.
          p-list.pnam3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam3 = " ".
        
          IF akthdr1.product[4] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[4] NO-LOCK NO-ERROR.
          p-list.pnam4 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam4 = " ".
        
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
          
          IF akthdr1.referred NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 6 
            AND buf-aktcode.aktionscode = akthdr1.referred NO-LOCK NO-ERROR.
          p-list.refer = buf-aktcode.bezeich.
          END.
          /* ctotal = n + 1.*/  
        END.
        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL : " + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.                       
    END.
    RUN fill-stage.
  END.
  ELSE
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 2 NO-LOCK,
      FIRST buf-akthdr WHERE buf-akthdr.stufe = akt-code1.aktionscode AND buf-akthdr.userinit = usr-init
      AND buf-akthdr.flag = 1 AND buf-akthdr.next-datum GE next-date AND buf-akthdr.next-datum LE to-date 
      NO-LOCK BY akt-code1.aktionscode:
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        p-list.code-name = STRING(nr, ">9") + " - " + akt-code1.bezeich.
        
        hnr  = 0.
        amt  = 0.
        tamt = 0.
       
        FOR EACH akthdr1 WHERE akthdr1.stufe = akt-code1.aktionscode 
          AND akthdr1.userinit = usr-init AND akthdr1.flag = 1 
          AND akthdr1.next-datum GE next-date AND akthdr1.next-datum LE to-date NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = akthdr1.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
          AND akt-kont1.kontakt-nr = akthdr1.kontakt-nr NO-LOCK 
          BY guest1.NAME:
          
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
            p-list.stage = akthdr1.stufe
            p-list.proz  = STRING(akthdr1.prozent, ">>9%")
            p-list.popen = akthdr1.next-datum
            p-list.pfnsh = akthdr1.erl-datum
            p-list.pid   = akthdr1.userinit
            p-list.pcid  = akthdr1.chg-id.
            
          hnr = hnr + 1.
          amt = p-list.pamt.
          tamt = tamt + amt.
       
          IF akthdr1.product[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[1] NO-LOCK NO-ERROR.
          p-list.pnam1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam1 = " ".
        
          IF akthdr1.product[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[2] NO-LOCK NO-ERROR.
          p-list.pnam2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam2 = " ".
        
          IF akthdr1.product[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[3] NO-LOCK NO-ERROR.
          p-list.pnam3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam3 = " ".
        
          IF akthdr1.product[4] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 3 
            AND buf-aktcode.aktionscode = akthdr1.product[4] NO-LOCK NO-ERROR.
          p-list.pnam4 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pnam4 = " ".
        
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
          
          IF akthdr1.referred NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 6 
            AND buf-aktcode.aktionscode = akthdr1.referred NO-LOCK NO-ERROR.
          p-list.refer = buf-aktcode.bezeich.
          END.
          /* ctotal = n + 1.*/
        END.
        CREATE p-list.
        ASSIGN
          p-list.pcomp = "TOTAL : " + STRING(hnr, ">>>>")
          p-list.pname = "TOTAL Amount : "
          p-list.pamt-str = STRING(tamt, ">,>>>,>>>,>>9.99").

        CREATE p-list.
      END.                       
    END.
    RUN fill-stage.
  END.
END PROCEDURE.

PROCEDURE fill-stage:
  FOR EACH p-list:
    CREATE slstage-list.
    BUFFER-COPY p-list TO slstage-list.
  END.
END PROCEDURE.
