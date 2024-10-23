
DEFINE TEMP-TABLE p-list 
  FIELD pnr AS INTEGER INITIAL 0 
  FIELD sflag AS INTEGER
  FIELD product AS CHAR FORMAT "x(25)"
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
  FIELD refer  AS CHAR FORMAT "x(15)"
  FIELD pid AS CHAR FORMAT "x(3)"
  FIELD pcid AS CHAR FORMAT "x(3)"
  FIELD ctotal AS INT FORMAT ">>>>>". 

DEFINE TEMP-TABLE slprod-list 
  FIELD pnr AS INTEGER INITIAL 0 
  FIELD sflag AS INTEGER
  FIELD product AS CHAR FORMAT "x(25)"
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
  FIELD refer  AS CHAR FORMAT "x(15)"
  FIELD pid AS CHAR FORMAT "x(3)"
  FIELD pcid AS CHAR FORMAT "x(3)"
  FIELD ctotal AS INT FORMAT ">>>>>". 

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER next-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER all-flag       AS LOGICAL.
DEF INPUT  PARAMETER usr-init       AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR slprod-list.
/* For Testing BL
DEF VARIABLE  pvILanguage AS INTEGER NO-UNDO INIT 1.
DEF VARIABLE  next-date AS DATE INIT ?.
DEF VARIABLE  to-date AS DATE INIT ?.
DEF VARIABLE  all-flag AS LOGICAL INIT YES.
DEF VARIABLE  usr-init AS CHAR INIT "01".
DEFINE VARIABLE p-width AS INTEGER INITIAL 122. 
*/
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "sls-byproduct".

IF  next-date NE ? AND to-date NE ? THEN
RUN browse-open2.
ELSE
RUN browse-open1.

PROCEDURE browse-open1: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VAR nr AS INT.
DEFINE VAR hnr AS INT.
DEFINE VAR tamt AS DEC.
DEFINE VAR flag AS LOGICAL INITIAL YES.
DEF VAR lname AS CHAR.
DEF VAR kname AS CHAR.

DEF VAR amt AS DEC.
DEF VAR amt1 AS DEC.
DEF VAR amt2 AS DEC.
DEF VAR amt3 AS DEC. 

DEF BUFFER akt-code1    FOR akt-code.
DEF BUFFER buf-aktcode  FOR akt-code.
DEF BUFFER guest1       FOR guest.
DEF BUFFER akthdr1      FOR akthdr.
DEF BUFFER akt-kont1    FOR akt-kont.
DEF BUFFER buf-akthdr   FOR akthdr.

  FOR EACH p-list:
    DELETE p-list.
  END.

  FOR EACH slprod-list:
    DELETE slprod-list.
  END.

  IF all-flag THEN
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 3 NO-LOCK,
      FIRST akthdr1 WHERE (akthdr1.product[1] = akt-code1.aktionscode 
      OR akthdr1.product[2] = akt-code1.aktionscode OR akthdr1.product[3] = akt-code1.aktionscode)
      AND (akthdr1.product[1] NE 0 OR akthdr1.product[2] NE 0 OR akthdr1.product[3] NE 0) NO-LOCK 
      BY akt-code1.aktionscode:  
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.product = STRING(nr, ">9") + " - " + akt-code1.bezeich.

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH buf-akthdr WHERE (buf-akthdr.product[1] = akt-code1.aktionscode
          OR buf-akthdr.product[2] = akt-code1.aktionscode
          OR buf-akthdr.product[3] = akt-code1.aktionscode) NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = buf-akthdr.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
            AND akt-kont1.kontakt-nr = buf-akthdr.kontakt-nr NO-LOCK
          BY buf-akthdr.stufe BY guest1.NAME:

          CREATE p-list.
          ASSIGN
            p-list.pnr   = buf-akthdr.aktnr
            p-list.sflag = buf-akthdr.flag
            p-list.pcomp = guest1.NAME + ", " + guest1.anredefirma
            p-list.pcont = akt-kont1.name + ", " + akt-kont1.vorname + " " + akt-kont1.anrede
            p-list.pname = buf-akthdr.bezeich
            p-list.pntot = buf-akthdr.stichwort
            p-list.pnam1 = buf-akthdr.product[1]
            p-list.pnam2 = buf-akthdr.product[2]
            p-list.pnam3 = buf-akthdr.product[3]
            p-list.pnam4 = buf-akthdr.product[4]
            p-list.pamt1 = buf-akthdr.amount[1]
            p-list.pamt2 = buf-akthdr.amount[2]
            p-list.pamt3 = buf-akthdr.amount[3]
            p-list.pamt4 = buf-akthdr.amount[4]
            p-list.patot = buf-akthdr.t-betrag
            p-list.stnr  = buf-akthdr.stufe
            p-list.proz  = STRING(buf-akthdr.prozent, ">>9%")
            p-list.popen = buf-akthdr.next-datum
            p-list.pfnsh = buf-akthdr.erl-datum
            p-list.pid   = buf-akthdr.userinit
            p-list.pcid  = buf-akthdr.chg-id.

          IF p-list.pnam1 = akt-code1.aktionscode THEN
            amt1 = p-list.pamt1.
          ELSE amt1 = 0.
          IF p-list.pnam2 = akt-code1.aktionscode THEN
            amt2 = p-list.pamt2.
          ELSE amt2 = 0.
          IF p-list.pnam3 = akt-code1.aktionscode THEN
            amt3 = p-list.pamt3.
          ELSE amt3 = 0.
          
          hnr  = hnr + 1.
          amt  = amt1 + amt2 + amt3.          
          tamt = tamt + amt.
          p-list.pamt-str = STRING(amt, ">,>>>,>>>,>>9.99").

          IF buf-akthdr.stufe NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 2 
            AND buf-aktcode.aktionscode = buf-akthdr.stufe NO-LOCK NO-ERROR.
          p-list.stage  = buf-aktcode.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF buf-akthdr.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF buf-akthdr.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF buf-akthdr.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF buf-akthdr.grund NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 5 
            AND buf-aktcode.aktionscode = buf-akthdr.grund NO-LOCK NO-ERROR.
          p-list.reason = buf-aktcode.bezeich.
          END.
          
          IF buf-akthdr.referred NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 6 
            AND buf-aktcode.aktionscode = buf-akthdr.referred NO-LOCK NO-ERROR.
          p-list.refer = buf-aktcode.bezeich.
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
    RUN fill-prod.
  END.
  ELSE
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 3 NO-LOCK,
      FIRST akthdr1 WHERE (akthdr1.product[1] = akt-code1.aktionscode 
      OR akthdr1.product[2] = akt-code1.aktionscode OR akthdr1.product[3] = akt-code1.aktionscode)
      AND (akthdr1.product[1] NE 0 OR akthdr1.product[2] NE 0 OR akthdr1.product[3] NE 0) 
      AND akthdr1.userinit = usr-init NO-LOCK BY akt-code1.aktionscode:  
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.product = STRING(nr, ">9") + " - " + akt-code1.bezeich.

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH buf-akthdr WHERE (buf-akthdr.product[1] = akt-code1.aktionscode
          OR buf-akthdr.product[2] = akt-code1.aktionscode
          OR buf-akthdr.product[3] = akt-code1.aktionscode) 
          AND buf-akthdr.userinit = usr-init NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = buf-akthdr.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
            AND akt-kont1.kontakt-nr = buf-akthdr.kontakt-nr NO-LOCK
          BY buf-akthdr.stufe BY guest1.NAME:

          CREATE p-list.
          ASSIGN
            p-list.pnr   = buf-akthdr.aktnr
            p-list.sflag = buf-akthdr.flag
            p-list.pcomp = guest1.NAME + ", " + guest1.anredefirma
            p-list.pcont = akt-kont1.name + ", " + akt-kont1.vorname + " " + akt-kont1.anrede
            p-list.pname = buf-akthdr.bezeich
            p-list.pntot = buf-akthdr.stichwort
            p-list.pnam1 = buf-akthdr.product[1]
            p-list.pnam2 = buf-akthdr.product[2]
            p-list.pnam3 = buf-akthdr.product[3]
            p-list.pnam4 = buf-akthdr.product[4]
            p-list.pamt1 = buf-akthdr.amount[1]
            p-list.pamt2 = buf-akthdr.amount[2]
            p-list.pamt3 = buf-akthdr.amount[3]
            p-list.pamt4 = buf-akthdr.amount[4]
            p-list.patot = buf-akthdr.t-betrag
            p-list.stnr  = buf-akthdr.stufe
            p-list.proz  = STRING(buf-akthdr.prozent, ">>9%")
            p-list.popen = buf-akthdr.next-datum
            p-list.pfnsh = buf-akthdr.erl-datum
            p-list.pid   = buf-akthdr.userinit
            p-list.pcid  = buf-akthdr.chg-id.

          IF p-list.pnam1 = akt-code1.aktionscode THEN
            amt1 = p-list.pamt1.
          ELSE amt1 = 0.
          IF p-list.pnam2 = akt-code1.aktionscode THEN
            amt2 = p-list.pamt2.
          ELSE amt2 = 0.
          IF p-list.pnam3 = akt-code1.aktionscode THEN
            amt3 = p-list.pamt3.
          ELSE amt3 = 0.
          
          hnr  = hnr + 1.
          amt  = amt1 + amt2 + amt3.          
          tamt = tamt + amt.
          p-list.pamt-str = STRING(amt, ">,>>>,>>>,>>9.99").

          IF buf-akthdr.stufe NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 2 
            AND buf-aktcode.aktionscode = buf-akthdr.stufe NO-LOCK NO-ERROR.
          p-list.stage  = buf-aktcode.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF buf-akthdr.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF buf-akthdr.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF buf-akthdr.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF buf-akthdr.grund NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 5 
            AND buf-aktcode.aktionscode = buf-akthdr.grund NO-LOCK NO-ERROR.
          p-list.reason = buf-aktcode.bezeich.
          END.
          
          IF buf-akthdr.referred NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 6 
            AND buf-aktcode.aktionscode = buf-akthdr.referred NO-LOCK NO-ERROR.
          p-list.refer = buf-aktcode.bezeich.
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
    RUN fill-prod.
  END.
END PROCEDURE.

PROCEDURE browse-open2: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VAR nr AS INT.
DEFINE VAR hnr AS INT.
DEFINE VAR tamt AS DEC.
DEFINE VAR flag AS LOGICAL INITIAL YES.
DEF VAR lname AS CHAR.
DEF VAR kname AS CHAR.

DEF VAR amt AS DEC.
DEF VAR amt1 AS DEC.
DEF VAR amt2 AS DEC.
DEF VAR amt3 AS DEC. 

DEF BUFFER akt-code1    FOR akt-code.
DEF BUFFER buf-aktcode  FOR akt-code.
DEF BUFFER guest1       FOR guest.
DEF BUFFER akthdr1      FOR akthdr.
DEF BUFFER akt-kont1    FOR akt-kont.
DEF BUFFER buf-akthdr   FOR akthdr.

  FOR EACH p-list:
    DELETE p-list.
  END.

  FOR EACH slprod-list:
    DELETE slprod-list.
  END.

  IF all-flag THEN
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 3 NO-LOCK,
      FIRST akthdr1 WHERE (akthdr1.product[1] = akt-code1.aktionscode 
      OR akthdr1.product[2] = akt-code1.aktionscode OR akthdr1.product[3] = akt-code1.aktionscode)
      AND (akthdr1.product[1] NE 0 OR akthdr1.product[2] NE 0 OR akthdr1.product[3] NE 0) 
      AND akthdr1.next-datum GE next-date AND akthdr1.next-datum LE to-date NO-LOCK 
      BY akt-code1.aktionscode:  
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.product = STRING(nr, ">9") + " - " + akt-code1.bezeich.

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH buf-akthdr WHERE (buf-akthdr.product[1] = akt-code1.aktionscode
          OR buf-akthdr.product[2] = akt-code1.aktionscode
          OR buf-akthdr.product[3] = akt-code1.aktionscode) 
          AND buf-akthdr.next-datum GE next-date AND buf-akthdr.next-datum LE to-date NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = buf-akthdr.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
            AND akt-kont1.kontakt-nr = buf-akthdr.kontakt-nr NO-LOCK
          BY buf-akthdr.stufe BY guest1.NAME:

          CREATE p-list.
          ASSIGN
            p-list.pnr   = buf-akthdr.aktnr
            p-list.sflag = buf-akthdr.flag
            p-list.pcomp = guest1.NAME + ", " + guest1.anredefirma
            p-list.pcont = akt-kont1.name + ", " + akt-kont1.vorname + " " + akt-kont1.anrede
            p-list.pname = buf-akthdr.bezeich
            p-list.pntot = buf-akthdr.stichwort
            p-list.pnam1 = buf-akthdr.product[1]
            p-list.pnam2 = buf-akthdr.product[2]
            p-list.pnam3 = buf-akthdr.product[3]
            p-list.pnam4 = buf-akthdr.product[4]
            p-list.pamt1 = buf-akthdr.amount[1]
            p-list.pamt2 = buf-akthdr.amount[2]
            p-list.pamt3 = buf-akthdr.amount[3]
            p-list.pamt4 = buf-akthdr.amount[4]
            p-list.patot = buf-akthdr.t-betrag
            p-list.stnr  = buf-akthdr.stufe
            p-list.proz  = STRING(buf-akthdr.prozent, ">>9%")
            p-list.popen = buf-akthdr.next-datum
            p-list.pfnsh = buf-akthdr.erl-datum
            p-list.pid   = buf-akthdr.userinit
            p-list.pcid  = buf-akthdr.chg-id.

          IF p-list.pnam1 = akt-code1.aktionscode THEN
            amt1 = p-list.pamt1.
          ELSE amt1 = 0.
          IF p-list.pnam2 = akt-code1.aktionscode THEN
            amt2 = p-list.pamt2.
          ELSE amt2 = 0.
          IF p-list.pnam3 = akt-code1.aktionscode THEN
            amt3 = p-list.pamt3.
          ELSE amt3 = 0.
          
          hnr  = hnr + 1.
          amt  = amt1 + amt2 + amt3.          
          tamt = tamt + amt.
          p-list.pamt-str = STRING(amt, ">,>>>,>>>,>>9.99").

          IF buf-akthdr.stufe NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 2 
            AND buf-aktcode.aktionscode = buf-akthdr.stufe NO-LOCK NO-ERROR.
          p-list.stage  = buf-aktcode.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF buf-akthdr.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF buf-akthdr.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF buf-akthdr.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF buf-akthdr.grund NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 5 
            AND buf-aktcode.aktionscode = buf-akthdr.grund NO-LOCK NO-ERROR.
          p-list.reason = buf-aktcode.bezeich.
          END.
          
          IF buf-akthdr.referred NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 6 
            AND buf-aktcode.aktionscode = buf-akthdr.referred NO-LOCK NO-ERROR.
          p-list.refer = buf-aktcode.bezeich.
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
    RUN fill-prod.
  END.
  ELSE
  DO:
    nr = 0.
    FOR EACH akt-code1 WHERE akt-code1.aktiongrup = 3 NO-LOCK,
      FIRST akthdr1 WHERE (akthdr1.product[1] = akt-code1.aktionscode 
      OR akthdr1.product[2] = akt-code1.aktionscode OR akthdr1.product[3] = akt-code1.aktionscode)
      AND (akthdr1.product[1] NE 0 OR akthdr1.product[2] NE 0 OR akthdr1.product[3] NE 0) 
      AND akthdr1.userinit = usr-init AND akthdr1.next-datum GE next-date 
      AND akthdr1.next-datum LE to-date NO-LOCK BY akt-code1.aktionscode:  
      IF AVAILABLE akt-code1 THEN
      DO:
        nr = nr + 1.
        CREATE p-list.
        ASSIGN
          p-list.product = STRING(nr, ">9") + " - " + akt-code1.bezeich.

        hnr  = 0.
        amt  = 0.
        tamt = 0.

        FOR EACH buf-akthdr WHERE (buf-akthdr.product[1] = akt-code1.aktionscode
          OR buf-akthdr.product[2] = akt-code1.aktionscode
          OR buf-akthdr.product[3] = akt-code1.aktionscode) AND buf-akthdr.userinit = usr-init 
          AND buf-akthdr.next-datum GE next-date AND buf-akthdr.next-datum LE to-date NO-LOCK,
          FIRST guest1 WHERE guest1.gastnr = buf-akthdr.gastnr NO-LOCK,
          FIRST akt-kont1 WHERE akt-kont1.gastnr = guest1.gastnr 
            AND akt-kont1.kontakt-nr = buf-akthdr.kontakt-nr NO-LOCK
          BY buf-akthdr.stufe BY guest1.NAME:

          CREATE p-list.
          ASSIGN
            p-list.pnr   = buf-akthdr.aktnr
            p-list.sflag = buf-akthdr.flag
            p-list.pcomp = guest1.NAME + ", " + guest1.anredefirma
            p-list.pcont = akt-kont1.name + ", " + akt-kont1.vorname + " " + akt-kont1.anrede
            p-list.pname = buf-akthdr.bezeich
            p-list.pntot = buf-akthdr.stichwort
            p-list.pnam1 = buf-akthdr.product[1]
            p-list.pnam2 = buf-akthdr.product[2]
            p-list.pnam3 = buf-akthdr.product[3]
            p-list.pnam4 = buf-akthdr.product[4]
            p-list.pamt1 = buf-akthdr.amount[1]
            p-list.pamt2 = buf-akthdr.amount[2]
            p-list.pamt3 = buf-akthdr.amount[3]
            p-list.pamt4 = buf-akthdr.amount[4]
            p-list.patot = buf-akthdr.t-betrag
            p-list.stnr  = buf-akthdr.stufe
            p-list.proz  = STRING(buf-akthdr.prozent, ">>9%")
            p-list.popen = buf-akthdr.next-datum
            p-list.pfnsh = buf-akthdr.erl-datum
            p-list.pid   = buf-akthdr.userinit
            p-list.pcid  = buf-akthdr.chg-id.

          IF p-list.pnam1 = akt-code1.aktionscode THEN
            amt1 = p-list.pamt1.
          ELSE amt1 = 0.
          IF p-list.pnam2 = akt-code1.aktionscode THEN
            amt2 = p-list.pamt2.
          ELSE amt2 = 0.
          IF p-list.pnam3 = akt-code1.aktionscode THEN
            amt3 = p-list.pamt3.
          ELSE amt3 = 0.
          
          hnr  = hnr + 1.
          amt  = amt1 + amt2 + amt3.          
          tamt = tamt + amt.
          p-list.pamt-str = STRING(amt, ">,>>>,>>>,>>9.99").

          IF buf-akthdr.stufe NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 2 
            AND buf-aktcode.aktionscode = buf-akthdr.stufe NO-LOCK NO-ERROR.
          p-list.stage  = buf-aktcode.bezeich.
          END.
          ELSE p-list.stage = " ".
        
          IF buf-akthdr.mitbewerber[1] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[1] NO-LOCK NO-ERROR.
          p-list.pmain1 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain1 = " ".
        
          IF buf-akthdr.mitbewerber[2] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[2] NO-LOCK NO-ERROR.
          p-list.pmain2 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain2 = " " .
        
          IF buf-akthdr.mitbewerber[3] NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 4 
            AND buf-aktcode.aktionscode = buf-akthdr.mitbewerber[3] NO-LOCK NO-ERROR.
          p-list.pmain3 = buf-aktcode.bezeich.
          END.
          ELSE p-list.pmain3 = " ".
        
          IF buf-akthdr.grund NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 5 
            AND buf-aktcode.aktionscode = buf-akthdr.grund NO-LOCK NO-ERROR.
          p-list.reason = buf-aktcode.bezeich.
          END.
          
          IF buf-akthdr.referred NE 0 THEN
          DO:
          FIND FIRST buf-aktcode WHERE buf-aktcode.aktiongrup = 6 
            AND buf-aktcode.aktionscode = buf-akthdr.referred NO-LOCK NO-ERROR.
          p-list.refer = buf-aktcode.bezeich.
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
    RUN fill-prod.
  END.
END PROCEDURE.

PROCEDURE fill-prod:
  FOR EACH p-list:
    CREATE slprod-list.
    BUFFER-COPY p-list TO slprod-list.
  END.
END PROCEDURE.
