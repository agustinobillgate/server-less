DEF TEMP-TABLE reslin-list LIKE res-line.

DEF INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER res-mode    AS CHAR        NO-UNDO.
DEF INPUT PARAMETER guestname   AS CHAR        NO-UNDO.
DEF INPUT PARAMETER mr-comment  AS CHAR        NO-UNDO.
DEF INPUT PARAMETER rl-comment  AS CHAR        NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR        NO-UNDO.
DEF INPUT PARAMETER earlyci     AS LOGICAL     NO-UNDO.
DEF INPUT PARAMETER fixed-rate  AS LOGICAL     NO-UNDO.
DEF INPUT PARAMETER TABLE FOR reslin-list.

DEF VARIABLE RTC1 AS CHAR NO-UNDO INIT "-".
DEF VARIABLE RTC2 AS CHAR NO-UNDO INIT "-".

DEF BUFFER zkbuff1 FOR zimkateg.
DEF BUFFER zkbuff2 FOR zimkateg.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline". 

FIND FIRST reslin-list.
FIND FIRST res-line WHERE res-line.resnr = reslin-list.resnr
    AND res-line.reslinnr = reslin-list.reslinnr NO-LOCK.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

RUN res-changes.

PROCEDURE res-changes: 
DEF VARIABLE do-it   AS LOGICAL INITIAL NO                      NO-UNDO. 
DEF VARIABLE cid     AS CHAR FORMAT "x(2)" INITIAL "  "         NO-UNDO. 
DEF VARIABLE cdate   AS CHAR FORMAT "x(8)" INITIAL "        "   NO-UNDO. 
DEF VARIABLE heute   AS DATE                                    NO-UNDO. 
DEF VARIABLE zeit    AS INTEGER                                 NO-UNDO.

/*sis 161214*/
DEFINE BUFFER gbuff FOR guest.  
DEFINE VARIABLE old-bill-adr AS CHARACTER.
DEFINE VARIABLE new-bill-adr AS CHARACTER.
/*end sis*/

DEFINE VARIABLE rstat-list AS CHAR EXTENT 13 FORMAT "x(9)" NO-UNDO.
rstat-list[1] = translateExtended ("Guaranted",lvCAREA,"").
rstat-list[2] = translateExtended ("6 PM",lvCAREA,"").
rstat-list[3] = translateExtended ("Tentative",lvCAREA,"").
rstat-list[4] = translateExtended ("WaitList",lvCAREA,"").
rstat-list[5] = translateExtended ("VerbConfirm",lvCAREA,"").
rstat-list[6] = translateExtended ("Inhouse",lvCAREA,"").
rstat-list[7] = "".
rstat-list[8] = translateExtended ("Departed",lvCAREA,"").
rstat-list[9] = translateExtended ("Cancelled",lvCAREA,"").
rstat-list[10] = translateExtended ("NoShow",lvCAREA,"").
rstat-list[11] = translateExtended ("ShareRes",lvCAREA,"").
rstat-list[12] = "".
rstat-list[13] = translateExtended ("RmSharer",lvCAREA,"").

DEFINE BUFFER guest1 FOR guest. 
 
  IF res-mode = "new" OR res-mode = "insert" THEN 
  DO: 
    RUN res-changes0. 
    RETURN. 
  END. 
 
  FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK.

  IF res-line.ankunft        NE reslin-list.ankunft 
    OR res-line.abreise      NE reslin-list.abreise 
    OR res-line.zimmeranz    NE reslin-list.zimmeranz 
    OR res-line.erwachs      NE reslin-list.erwachs 
    OR res-line.kind1        NE reslin-list.kind1 
    OR res-line.gratis       NE reslin-list.gratis 
    OR res-line.zikatnr      NE reslin-list.zikatnr 
    OR res-line.zinr         NE reslin-list.zinr 
    OR res-line.arrangement  NE reslin-list.arrangement 
    OR res-line.zipreis      NE reslin-list.zipreis 
    OR reslin-list.was-status  NE INTEGER(fixed-rate) 
    OR res-line.name         NE guestname 
    OR res-line.resstatus    NE reslin-list.resstatus
    OR reservation.bemerk    NE mr-comment
    OR res-line.bemerk       NE rl-comment
    OR res-line.gastnrpay    NE reslin-list.gastnrpay   /*sis 161214*/
  THEN do-it = YES. 
 
  heute = TODAY. 
  zeit = TIME. 
  IF TRIM(res-line.changed-id) NE "" THEN 
  DO: 
    cid = res-line.changed-id. 
    cdate = STRING(res-line.changed). 
  END. 
  ELSE IF LENGTH(res-line.reserve-char) GE 14 THEN    /* created BY */ 
    cid = SUBSTR(res-line.reserve-char,14). 

  IF do-it THEN 
  DO:  
    CREATE reslin-queasy.
    ASSIGN
      reslin-queasy.key         = "ResChanges"
      reslin-queasy.resnr       = reslin-list.resnr
      reslin-queasy.reslinnr    = reslin-list.reslinnr
      reslin-queasy.date2       = heute
      reslin-queasy.number2     = zeit. 
    . 
    IF earlyci THEN reslin-queasy.number1 = 1. 
 
    reslin-queasy.char3 = STRING(res-line.ankunft) + ";" 
                        + STRING(reslin-list.ankunft) + ";" 
                        + STRING(res-line.abreise) + ";" 
                        + STRING(reslin-list.abreise) + ";" 
                        + STRING(res-line.zimmeranz) + ";" 
                        + STRING(reslin-list.zimmeranz) + ";" 
                        + STRING(res-line.erwachs) + ";" 
                        + STRING(reslin-list.erwachs) + ";" 
                        + STRING(res-line.kind1) + ";" 
                        + STRING(reslin-list.kind1) + ";" 
                        + STRING(res-line.gratis) + ";" 
                        + STRING(reslin-list.gratis) + ";" 
                        + STRING(res-line.zikatnr) + ";" 
                        + STRING(reslin-list.zikatnr) + ";" 
                        + STRING(res-line.zinr) + ";" 
                        + STRING(reslin-list.zinr) + ";". 

    IF reslin-list.reserve-int = res-line.reserve-int THEN 
    reslin-queasy.char3 = reslin-queasy.char3 
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(reslin-list.arrangement) + ";". 
    ELSE 
    reslin-queasy.char3 = reslin-queasy.char3 
                        + STRING(res-line.arrangement) + ";" 
                        + STRING(res-line.reserve-int) + ";".

    IF res-line.resstatus NE reslin-list.resstatus THEN     /*FDL July 30, 2024 => Ticket 9B5DCC*/
    DO:
        reslin-queasy.char3 = reslin-queasy.char3 
                            + STRING(res-line.zipreis) + ";" 
                            + STRING(reslin-list.zipreis) + ";"
                            + STRING(cid) + ";" 
                            + STRING(user-init) + ";" 
                            + STRING(cdate, "x(8)") + ";" 
                            + STRING(heute) + ";" 
                            + STRING("ResStatus Changed:") + ";" 
                            + STRING(rstat-list[res-line.resstatus]) + " -> " + STRING(rstat-list[reslin-list.resstatus]) + ";".
    END.
    ELSE
    DO:
        reslin-queasy.char3 = reslin-queasy.char3 
                            + STRING(res-line.zipreis) + ";" 
                            + STRING(reslin-list.zipreis) + ";"
                            + STRING(cid) + ";" 
                            + STRING(user-init) + ";" 
                            + STRING(cdate, "x(8)") + ";" 
                            + STRING(heute) + ";" 
                            + STRING(res-line.NAME) + ";" 
                            + STRING(guestname) + ";". 
    END.
    
    IF reslin-list.was-status = 0 THEN 
      reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO", "x(3)") + ";". 
    ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES", "x(3)") + ";". 
    IF NOT fixed-rate THEN 
      reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO", "x(3)") + ";". 
    ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES", "x(3)") + ";". 
  
    FIND CURRENT reslin-queasy NO-LOCK.
    RELEASE reslin-queasy. 

/*MT 26/02/13 */
    IF res-line.resstatus NE reslin-list.resstatus THEN
    DO:
        CREATE res-history. 
        ASSIGN 
            res-history.nr          = bediener.nr 
            res-history.resnr       = res-line.resnr 
            res-history.reslinnr    = res-line.reslinnr 
            res-history.datum       = heute 
            res-history.zeit        = zeit 
            res-history.aenderung   = res-line.bemerk 
            res-history.action      = "Resstatus Changed". 
        
        IF reslin-list.resstatus = 5 THEN rstat-list[5] = "Verbal Confirm".
        res-history.aenderung = "Resstatus " + CHR(10) 
            + rstat-list[res-line.resstatus] + CHR(10) + CHR(10) 
            + "*** Changed to:" + CHR(10) + CHR(10) 
            + rstat-list[reslin-list.resstatus]
            + " ResNo " + STRING(res-line.resnr) + CHR(10)
            + " RmNo " + STRING(res-line.zinr).
 
        IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
        RELEASE res-history. 
    END.
    /*MT 26/02/13 */

    IF (reservation.bemerk NE mr-comment) OR 
       (res-line.bemerk NE rl-comment) THEN
    DO: 
        CREATE res-history. 
        ASSIGN 
            res-history.nr          = bediener.nr 
            res-history.resnr       = res-line.resnr 
            res-history.reslinnr    = res-line.reslinnr 
            res-history.datum       = heute 
            res-history.zeit        = zeit 
            res-history.aenderung   = res-line.bemerk 
            res-history.action      = "Remark". 
 
        res-history.aenderung = STRING(res-line.resnr) + "-" + reservation.bemerk + CHR(10) 
            + res-line.bemerk + CHR(10) + CHR(10) 
            + "*** Changed to:" + CHR(10) + CHR(10) 
            + mr-comment + CHR(10) + rl-comment. 
 
        IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
        RELEASE res-history. 
    END.  

    /*sis 161214*/
    IF (res-line.gastnrpay NE reslin-list.gastnrpay) AND 
        (res-mode = "modify" OR res-mode = "inhouse" OR res-mode = "split") THEN
    DO:
        FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrpay NO-LOCK NO-ERROR.
        IF AVAILABLE gbuff THEN old-bill-adr = gbuff.NAME.

        FIND FIRST guest WHERE guest.gastnr = reslin-list.gastnrpay NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN new-bill-adr = guest.NAME.

            CREATE res-history. 
            ASSIGN 
                res-history.nr          = bediener.nr 
                res-history.resnr       = res-line.resnr 
                res-history.reslinnr    = res-line.reslinnr 
                res-history.datum       = heute 
                res-history.zeit        = zeit 
                res-history.action      = "Bill Receiver Changed" 
                res-history.aenderung = old-bill-adr + CHR(10) + CHR(10)
                    + "*** Changed to:" + CHR(10) + CHR(10) 
                    + new-bill-adr + CHR(10) + CHR(10) 
                    + "*** Rsv No: " + STRING(res-line.resnr) + CHR(10) 
                    + "*** Rsv Line No: " + STRING(res-line.reslinnr)
            . 
            IF AVAILABLE bediener THEN res-history.betriebsnr = bediener.nr. 
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history. 
        END.
    /*end sis*/
  END.

/* ST 17 AUG 2015 */    
  IF res-line.l-zuordnung[1] NE reslin-list.l-zuordnung[1] THEN
  DO:
    IF res-line.l-zuordnung[1] NE 0 THEN
    FIND FIRST zkbuff1 WHERE zkbuff1.zikatnr = res-line.l-zuordnung[1]
        NO-LOCK NO-ERROR.
    IF AVAILABLE zkbuff1 THEN RTC1 = zkbuff1.kurzbez.
    IF reslin-list.l-zuordnung[1] NE 0 THEN
    FIND FIRST zkbuff2 WHERE zkbuff2.zikatnr = reslin-list.l-zuordnung[1]
        NO-LOCK NO-ERROR.
    IF AVAILABLE zkbuff2 THEN RTC2 = zkbuff2.kurzbez.

    CREATE reslin-queasy.
    ASSIGN
        reslin-queasy.key         = "ResChanges"
        reslin-queasy.resnr       = res-line.resnr
        reslin-queasy.reslinnr    = res-line.reslinnr
        reslin-queasy.date2       = TODAY
        reslin-queasy.number2     = TIME 
    .  
    reslin-queasy.char3 = STRING(reslin-list.ankunft) + ";" 
            + STRING(reslin-list.ankunft) + ";" 
            + STRING(reslin-list.abreise) + ";" 
            + STRING(reslin-list.abreise) + ";" 
            + STRING(reslin-list.zimmeranz) + ";" 
            + STRING(reslin-list.zimmeranz) + ";" 
            + STRING(reslin-list.erwachs) + ";" 
            + STRING(reslin-list.erwachs) + ";" 
            + STRING(reslin-list.kind1) + ";" 
            + STRING(reslin-list.kind1) + ";" 
            + STRING(reslin-list.gratis) + ";" 
            + STRING(reslin-list.gratis) + ";" 
            + STRING(reslin-list.zikatnr) + ";" 
            + STRING(reslin-list.zikatnr) + ";" 
            + STRING(reslin-list.zinr) + ";" 
            + STRING(reslin-list.zinr) + ";"
            + STRING(reslin-list.arrangement) + ";" 
            + STRING(reslin-list.arrangement) + ";"
            + STRING(reslin-list.zipreis) + ";" 
            + STRING(reslin-list.zipreis) + ";"
            + STRING(cid) + ";" 
            + STRING(user-init) + ";" 
            + STRING(cdate, "x(8)") + ";" 
            + STRING(TODAY) + ";" 
            + STRING("RTC changed:") + ";" 
            + STRING(RTC1) + " -> " + STRING(RTC2) + ";" 
            + STRING("YES", "x(3)") + ";" 
            + STRING("YES", "x(3)") + ";" 
    .
    FIND CURRENT reslin-queasy NO-LOCK.
    RELEASE reslin-queasy. 
  END.

END. 

PROCEDURE res-changes0: 
DEF VARIABLE cid     AS CHAR FORMAT "x(2)" INITIAL "  "         NO-UNDO. 
DEF VARIABLE cdate   AS CHAR FORMAT "x(8)" INITIAL "        "   NO-UNDO. 
DEFINE BUFFER guest1 FOR guest. 
  
  CREATE reslin-queasy. 
  ASSIGN
    reslin-queasy.key       = "ResChanges"
    reslin-queasy.resnr     = reslin-list.resnr 
    reslin-queasy.reslinnr  = reslin-list.reslinnr 
    reslin-queasy.date2     = TODAY 
    reslin-queasy.number2   = TIME
  . 
  reslin-queasy.char3 = STRING(reslin-list.ankunft) + ";" 
                        + STRING(reslin-list.ankunft) + ";" 
                        + STRING(reslin-list.abreise) + ";" 
                        + STRING(reslin-list.abreise) + ";" 
                        + STRING(reslin-list.zimmeranz) + ";" 
                        + STRING(reslin-list.zimmeranz) + ";" 
                        + STRING(reslin-list.erwachs) + ";" 
                        + STRING(reslin-list.erwachs) + ";" 
                        + STRING(reslin-list.kind1) + ";" 
                        + STRING(reslin-list.kind1) + ";" 
                        + STRING(reslin-list.gratis) + ";" 
                        + STRING(reslin-list.gratis) + ";" 
                        + STRING(reslin-list.zikatnr) + ";" 
                        + STRING(reslin-list.zikatnr) + ";" 
                        + STRING(reslin-list.zinr) + ";" 
                        + STRING(reslin-list.zinr) + ";" 
                        + STRING(reslin-list.arrangement) + ";" 
                        + STRING(reslin-list.arrangement) + ";"
                        + STRING(reslin-list.zipreis) + ";" 
                        + STRING(reslin-list.zipreis) + ";"
                        + STRING(user-init) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(reslin-list.NAME) + ";" 
                        + STRING("New Reservation") + ";". 
  IF reslin-list.was-status = 0 THEN 
    reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO") + ";". 
  ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES") + ";". 
 
  IF NOT fixed-rate THEN 
    reslin-queasy.char3 = reslin-queasy.char3 + STRING("NO") + ";". 
  ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES") + ";". 
 
  FIND CURRENT reslin-queasy NO-LOCK.
  RELEASE reslin-queasy. 
 
END. 
