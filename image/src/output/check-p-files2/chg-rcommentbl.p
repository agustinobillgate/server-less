DEFINE INPUT PARAM icase           AS INTEGER      NO-UNDO.
DEFINE INPUT PARAM resno           AS INTEGER      NO-UNDO.
DEFINE INPUT PARAM reslinno        AS INTEGER      NO-UNDO.
DEFINE INPUT PARAM user-init       AS CHAR         NO-UNDO.
DEFINE INPUT-OUTPUT PARAM res-com  AS CHAR         NO-UNDO.
DEFINE INPUT-OUTPUT PARAM resl-com AS CHAR         NO-UNDO.
DEFINE INPUT-OUTPUT PARAM g-com    AS CHAR         NO-UNDO.
DEFINE INPUT-OUTPUT PARAM web-com  AS CHAR         NO-UNDO.

DEFINE VARIABLE str1  AS CHAR    NO-UNDO.
DEFINE VARIABLE str2  AS CHAR    NO-UNDO.
DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
DEFINE VARIABLE loopj AS INTEGER NO-UNDO.
DEFINE VARIABLE loopk AS INTEGER NO-UNDO.
/*naufal - variable for today and time*/
DEFINE VARIABLE heute AS DATE    NO-UNDO. 
DEFINE VARIABLE zeit  AS INTEGER NO-UNDO.
DEFINE VARIABLE cid   AS CHAR FORMAT "x(2)" INITIAL "  "         NO-UNDO. 
DEFINE VARIABLE cdate AS CHAR FORMAT "x(8)" INITIAL "        "   NO-UNDO.

IF icase = 1 THEN RUN read-comment.
ELSE IF icase = 2 THEN RUN update-comment.

PROCEDURE read-comment:
  FIND FIRST res-line WHERE res-line.resnr = resno
    AND res-line.reslinnr = reslinno NO-LOCK. 
  FIND FIRST reservation WHERE reservation.resnr = resno NO-LOCK. 
  FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
  ASSIGN
    g-com     = guest.bemerk
    res-com   = reservation.bemerk 
    resl-com  = res-line.bemerk.

  /*ITA*/   
   DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str1 = ENTRY(loopi,res-line.zimmer-wunsch, ";").
        IF str1 MATCHES "*WCI-req*" THEN DO:
           str2 = ENTRY(2, str1, "=").
           DO loopj = 1 TO NUM-ENTRIES(str2, ","):
               FIND FIRST queasy WHERE queasy.KEY = 160
                   AND queasy.number1 = INT(ENTRY(loopj, str2, ",")) NO-LOCK NO-ERROR.
               IF AVAILABLE queasy THEN DO:
                    DO loopk = 1 TO NUM-ENTRIES(queasy.char1, ";") :
                        IF ENTRY(loopk, queasy.char1, ";") MATCHES "*en*" THEN
                        DO:
                            ASSIGN web-com = ENTRY(2, ENTRY(loopk, queasy.char1, ";"), "=") + ", " + web-com.
                            LEAVE.
                        END.
                    END.
               END.
           END.
        END.
        ELSE IF str1 MATCHES "*PRCODE*" THEN DO:
            ASSIGN web-com = web-com + "PromoCode: " + ENTRY(3,str1,"$").
        END.
    END.
END.

PROCEDURE update-comment:
  FIND FIRST res-line WHERE res-line.resnr = resno
    AND res-line.reslinnr = reslinno EXCLUSIVE-LOCK. 
  FIND FIRST reservation WHERE reservation.resnr = resno EXCLUSIVE-LOCK. 
  FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember EXCLUSIVE-LOCK.

  /*ITA 230617*/
  IF (res-com NE reservation.bemerk) OR (resl-com NE res-line.bemerk) THEN 
  DO:
      /*naufal - add reservation log*/
      ASSIGN
          heute = TODAY
          zeit  = TIME.
      IF TRIM(res-line.changed-id) NE "" THEN 
      DO: 
          cid = res-line.changed-id. 
          cdate = STRING(res-line.changed). 
      END.
      ELSE IF LENGTH(res-line.reserve-char) GE 14 THEN    /* created BY */ 
          cid = SUBSTR(res-line.reserve-char,14).

      CREATE reslin-queasy.
      ASSIGN
          reslin-queasy.key         = "ResChanges"
          reslin-queasy.resnr       = resno  
          reslin-queasy.reslinnr    = reslinno
          reslin-queasy.date2       = heute               
          reslin-queasy.number2     = zeit.

      reslin-queasy.char3 = STRING(res-line.ankunft) + ";" 
                          + STRING(res-line.ankunft) + ";" 
                          + STRING(res-line.abreise) + ";" 
                          + STRING(res-line.abreise) + ";" 
                          + STRING(res-line.zimmeranz) + ";" 
                          + STRING(res-line.zimmeranz) + ";" 
                          + STRING(res-line.erwachs) + ";" 
                          + STRING(res-line.erwachs) + ";" 
                          + STRING(res-line.kind1) + ";" 
                          + STRING(res-line.kind1) + ";" 
                          + STRING(res-line.gratis) + ";" 
                          + STRING(res-line.gratis) + ";" 
                          + STRING(res-line.zikatnr) + ";" 
                          + STRING(res-line.zikatnr) + ";" 
                          + STRING(res-line.zinr) + ";" 
                          + STRING(res-line.zinr) + ";"
                          + STRING(res-line.arrangement) + ";" 
                          + STRING(res-line.arrangement) + ";".

      reslin-queasy.char3 = reslin-queasy.char3 
                          + STRING(res-line.zipreis) + ";" 
                          + STRING(res-line.zipreis) + ";"
                          + STRING(cid) + ";" 
                          + STRING(user-init) + ";" 
                          + STRING(cdate, "x(8)") + ";" 
                          + STRING(heute) + ";" 
                          + STRING(res-line.NAME) + ";" 
                          + STRING(res-line.NAME) + ";".

      IF res-line.was-status EQ 0 THEN
          reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO", "x(3)") + ";".
      ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES", "x(3)") + ";".
      IF res-line.was-status EQ 0 THEN
          reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO", "x(3)") + ";".
      ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES", "x(3)") + ";".
      FIND CURRENT reslin-queasy NO-LOCK.
      RELEASE reslin-queasy.

      FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
      CREATE res-history. 
      ASSIGN 
          res-history.nr          = bediener.nr 
          res-history.resnr       = res-line.resnr 
          res-history.reslinnr    = res-line.reslinnr 
          res-history.datum       = TODAY 
          res-history.zeit        = TIME 
          /*res-history.aenderung   = res-line.bemerk*/ 
          res-history.action      = "Remark". 
 
      res-history.aenderung = STRING(res-line.resnr) + "-" + reservation.bemerk + CHR(10) 
          + res-line.bemerk + CHR(10) + CHR(10) 
          + "*** Changed to:" + CHR(10) + CHR(10) 
          + res-com + CHR(10) + resl-com. 
 
      IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
      RELEASE res-history. 
  END. /*end.*/

  ASSIGN
    guest.bemerk        = g-com
    reservation.bemerk  = res-com 
    res-line.bemerk     = resl-com.

  FIND CURRENT res-line NO-LOCK.
  FIND CURRENT reservation NO-LOCK.
  FIND CURRENT guest NO-LOCK.
END.


