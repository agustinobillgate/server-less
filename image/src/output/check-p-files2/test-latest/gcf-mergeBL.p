

DEF INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER gastnr1 AS INTEGER. 
DEFINE INPUT PARAMETER gastnr2 AS INTEGER. 
DEFINE INPUT PARAMETER flag1 AS LOGICAL. 
DEFINE INPUT PARAMETER flag2 AS LOGICAL. 

RUN gcf-merge.


PROCEDURE gcf-merge: 
DEFINE buffer gast FOR guest. 
DEFINE buffer gast1 FOR guest. 
DEFINE buffer gast2 FOR guest. 
DEFINE buffer gastat FOR guestat1. 
DEFINE VAR name1 AS CHAR NO-UNDO. 
DEFINE VAR name2 AS CHAR NO-UNDO. 
 
  FIND FIRST gast2 WHERE gast2.gastnr = gastnr2 NO-LOCK. 
  name2 = gast2.NAME. 
 
  DO TRANSACTION: 
    
    FIND FIRST gast1 WHERE gast1.gastnr = gastnr1 EXCLUSIVE-LOCK. 
    name1 = gast1.NAME. 

    FOR EACH akt-kont WHERE akt-kont.betrieb-gast = gastnr1:
      akt-kont.betrieb-gast = gastnr2.
    END.

    FOR EACH genstat WHERE genstat.gastnr = gastnr1:
      genstat.gastnr = gastnr2.
    END.

    FOR EACH genstat WHERE genstat.gastnrmember = gastnr1:
      genstat.gastnrmember = gastnr2.
    END.

    FOR EACH queasy WHERE queasy.key = 14 AND queasy.number3 = gastnr1: 
      queasy.number3 = gastnr2. 
    END. 
    FOR EACH history WHERE history.gastnr = gastnr1: 
      history.gastnr = gastnr2. 
    END. 
    FOR EACH reservation WHERE reservation.gastnr = gastnr1: 
      reservation.gastnr = gastnr2. 
      reservation.name = gast2.name. 
    END. 
    FOR EACH reservation WHERE reservation.gastnrherk = gastnr1: 
      reservation.gastnrherk = gastnr2. 
    END. 
    FOR EACH res-line WHERE res-line.gastnr = gastnr1: 
      ASSIGN
        res-line.gastnr  = gastnr2
        res-line.resname = gast2.NAME
      . 
    END. 
    FOR EACH res-line WHERE res-line.gastnrmember = gastnr1: 
      res-line.gastnrmember = gastnr2. 
      res-line.name = gast2.name + ", " + gast2.vorname1 + " " + gast2.anrede1. 
    END. 
    FOR EACH res-line WHERE res-line.gastnrpay = gastnr1: 
      res-line.gastnrpay = gastnr2. 
    END. 
    FOR EACH bill WHERE bill.gastnr = gastnr1: 
      bill.gastnr = gastnr2. 
      bill.name = gast2.name. 
    END. 
    FOR EACH debitor WHERE debitor.gastnr = gastnr1: 
      debitor.gastnr = gastnr2. 
      debitor.name = gast2.name. 
    END. 
    FOR EACH debitor WHERE debitor.gastnrmember = gastnr1: 
      debitor.gastnrmember = gastnr2. 
    END. 
    FOR EACH gast WHERE gast.master-gastnr = gastnr1: 
      gast.master-gastnr = gastnr2. 
    END. 
    FOR EACH guestat1 WHERE guestat1.gastnr = gastnr1: 
      FIND FIRST gastat WHERE gastat.gastnr = gastnr2 
        AND gastat.datum = guestat1.datum EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE gastat THEN 
      DO: 
       gastat.zimmeranz = gastat.zimmeranz + guestat1.zimmeranz. 
       gastat.betriebsnr = gastat.betriebsnr + guestat1.betriebsnr. 
       gastat.persanz = gastat.persanz + guestat1.persanz. 
       gastat.logis = gastat.logis + guestat1.logis. 
       delete guestat1. 
      END. 
      ELSE guestat1.gastnr = gastnr2. 
    END. 
 
    FOR EACH zimmer WHERE zimmer.owner-nr = gastnr1: 
      zimmer.owner-nr = gastnr2. 
    END. 
 
    FOR EACH kontline WHERE kontline.gastnr = gastnr1: 
      kontline.gastnr = gastnr2. 
      kontline.gastnrpay = gastnr2. 
    END. 

    RUN check-global-allotment(gastnr1, gastnr2).

    FOR EACH master WHERE master.gastnr = gastnr1: 
      master.gastnr = gastnr2. 
      master.gastnrpay = gastnr2. 
    END. 
    FOR EACH messages WHERE messages.gastnr = gastnr1: 
      messages.gastnr = gastnr2. 
      messages.name = gast2.name + ", " + gast2.vorname1 + " " + gast2.anrede1. 
    END. 
 
    FOR EACH bk-veran WHERE bk-veran.gastnr = gastnr1:
        FOR EACH bk-func WHERE bk-func.veran-nr = bk-veran.veran-nr:
          ASSIGN
            bk-func.bestellt_durch = name2
            bk-func.adurch = name2
            bk-func.nadkarte[1] = name2
            bk-func.betriebsnr = gastnr2.
        END.
        bk-veran.gastnr = gastnr2.
    END.

    IF flag1 THEN 
    DO: 
      FIND FIRST guest-pr WHERE guest-pr.gastnr = gastnr1 EXCLUSIVE-LOCK. 
      guest-pr.gastnr = gastnr2. 
      FIND CURRENT guest-pr NO-LOCK. 
    END. 
  
    FIND CURRENT gast2 EXCLUSIVE-LOCK. 
    ASSIGN 
      gast2.logisumsatz = gast2.logisumsatz + gast1.logisumsatz 
      gast2.argtumsatz = gast2.argtumsatz + gast1.argtumsatz 
      gast2.f-b-umsatz = gast2.f-b-umsatz + gast1.f-b-umsatz 
      gast2.sonst-umsatz = gast2.sonst-umsatz + gast1.sonst-umsatz 
      gast2.gesamtumsatz = gast2.gesamtumsatz + gast1.gesamtumsatz 
      gast2.zimmeranz = gast2.zimmeranz + gast1.zimmeranz 
      gast2.aufenthalte = gast2.aufenthalte + gast1.aufenthalte 
      gast2.logiernachte = gast2.logiernachte + gast1.logiernachte. 
    ASSIGN 
      gast1.name = "" 
      gast1.gastnr = - gast1.gastnr. 
 
    FIND CURRENT gast1 NO-LOCK. 
    FIND CURRENT gast2 NO-LOCK. 
 
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    CREATE res-history. 
    ASSIGN 
        res-history.nr = bediener.nr 
        res-history.datum = TODAY 
        res-history.zeit = TIME 
        res-history.aenderung = "Merge GuestCard: GastNo " + STRING(gastnr1) 
          + " " + name1 + "TO GastNo " + STRING(gastnr2) + " " + name2 
        res-history.action = "GuestFile". 
    FIND CURRENT res-history NO-LOCK. 
    RELEASE res-history. 
 
    /*IF sorttype = 0 THEN b1:DELETE-CURRENT-ROW( ) IN FRAME frame1. 
    ELSE IF sorttype GE 1 THEN b2:DELETE-CURRENT-ROW( ) IN FRAME frame1. */
 
  END. 
END. 

PROCEDURE check-global-allotment:
DEF INPUT PARAMETER gastnr1 AS INTEGER NO-UNDO.
DEF INPUT PARAMETER gastnr2 AS INTEGER NO-UNDO.

DEF VAR tokcounter AS INTEGER NO-UNDO.
DEF VAR mesValue   AS CHAR    NO-UNDO.
DEF VAR global-str AS CHAR    NO-UNDO.
DEF VAR changed    AS LOGICAL NO-UNDO.
DEF BUFFER qsy     FOR queasy.
  FOR EACH queasy WHERE queasy.KEY = 147 AND queasy.number1 = gastnr1:
     queasy.number1 = gastnr2.
  END.

  FOR EACH queasy WHERE queasy.KEY = 147 NO-LOCK:
    ASSIGN
        changed    = NO
        global-str = ""
    .
    DO tokcounter = 1 TO NUM-ENTRIES(queasy.char3, ","):
      mesValue = ENTRY(tokcounter, queasy.char3, ",").
      IF mesValue NE "" THEN
      DO:
        IF INTEGER(mesValue) = gastnr1 THEN
        ASSIGN
          changed    = YES
          global-str = global-str + STRING(gastnr2) + ",".
        ELSE global-str = global-str + mesValue + ",".
      END.
    END.
    IF changed THEN
    DO:
      FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK.
      ASSIGN qsy.char3 = global-str.
      FIND CURRENT qsy NO-LOCK.
    END.
  END.

END.
