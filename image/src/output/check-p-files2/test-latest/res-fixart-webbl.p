DEFINE TEMP-TABLE fixleist-list   LIKE fixleist.

DEF INPUT  PARAMETER TABLE FOR fixleist-list.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER rec-id         AS INTEGER.
DEF INPUT  PARAMETER resnr          AS INTEGER.
DEF INPUT  PARAMETER reslinnr       AS INTEGER.
DEF INPUT  PARAMETER case-type      AS INTEGER.
DEF INPUT  PARAMETER user-init      AS CHARACTER.  /* Dzikri 44C4DB - log fixcost */

DEF OUTPUT PARAMETER msg-str        AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-fixart".

DEFINE VARIABLE is-fixrate AS CHAR INITIAL "NO". /* Dzikri 44C4DB - log fixcost */

FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK.

/* Dzikri 44C4DB - log fixcost, check if reservation fixrate or not */
FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement"
  AND reslin-queasy.resnr    EQ resnr
  AND reslin-queasy.reslinnr EQ reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE reslin-queasy THEN is-fixrate = "YES".
/* Dzikri 44C4DB - END */

FIND FIRST fixleist-list.

if user-init eq ? then user-init = " ".

IF case-type = 1 THEN       /* add */
DO:
    create fixleist.
    RUN fill-fixleist. 
    RUN check-article (RECID(fixleist)).
    RUN fixcost-changes-add. /* Dzikri 44C4DB - log fixcost */
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST fixleist WHERE RECID(fixleist) = rec-id EXCLUSIVE-LOCK.
    RUN fixcost-changes-chg. /* Dzikri 44C4DB - log fixcost */
    RUN fill-fixleist. 
    RUN check-article (RECID(fixleist)). 
    /*RUN init-fixleist-list. */
    FIND CURRENT fixleist NO-LOCK. 
    /*MTDISABLE fixleist-list.departement fixleist-list.artnr 
          fixleist-list.bezeich fixleist-list.number 
          fixleist-list.sequenz fixleist-list.dekade fixleist-list.lfakt 
          fixleist-list.betrag 
          btn-ask1 btn-ask2 /*btn-ask3*/ 
          WITH FRAME frame1. 
    ENABLE btn-addart btn-chgart btn-delart WITH FRAME frame1. */
    /*OPEN QUERY q1 FOR EACH fixleist WHERE fixleist.resnr = resnr 
      AND fixleist.reslinnr = reslinnr NO-LOCK 
      BY fixleist.departement BY fixleist.artnr. 
    curr-select = "". 
    RETURN NO-APPLY. */
END.


PROCEDURE fill-fixleist: 
  fixleist.resnr        = resnr. 
  fixleist.reslinnr     = reslinnr. 
  fixleist.departement  = fixleist-list.departement. 
  fixleist.artnr        = fixleist-list.artnr. 
  fixleist.number       = fixleist-list.number. 
  fixleist.sequenz      = fixleist-list.sequenz. 
  fixleist.dekade       = fixleist-list.dekade. 
  fixleist.lfakt        = fixleist-list.lfakt. 
  fixleist.betrag       = fixleist-list.betrag. 
  fixleist.bezeich      = fixleist-list.bezeich. 
END. 

PROCEDURE check-article: 
DEFINE INPUT PARAMETER fix-recid AS INTEGER. 
DEFINE VARIABLE b-date AS DATE INITIAL ?. 
DEFINE VARIABLE e-date AS DATE INITIAL ?. 
DEFINE VARIABLE b1-date AS DATE. 
DEFINE VARIABLE e1-date AS DATE. 
DEFINE VARIABLE warn-it AS LOGICAL INITIAL NO. 
DEFINE buffer fixleist1 FOR fixleist. 
 
  IF fixleist-list.sequenz = 1 THEN 
  DO: 
    b-date = res-line.ankunft. 
    e-date = res-line.abreise - 1. 
  END. 
  ELSE IF fixleist-list.sequenz = 2 THEN 
  DO: 
    b-date = res-line.ankunft. 
    e-date = res-line.ankunft. 
  END. 
  ELSE IF fixleist-list.sequenz = 6 THEN 
  DO: 
    IF fixleist-list.lfakt = ? THEN b-date = res-line.ankunft. 
    ELSE b-date = fixleist-list.lfakt. 
    e-date = b-date + fixleist-list.dekade - 1. 
  END. 
 
  FOR EACH fixleist1 WHERE fixleist1.resnr = resnr 
    AND fixleist1.reslinnr = reslinnr 
    AND fixleist1.artnr = fixleist.artnr 
    AND fixleist1.departement = fixleist.departement 
    AND RECID(fixleist1) NE fix-recid NO-LOCK: 
    IF fixleist1.sequenz = 1 THEN 
    DO: 
      b1-date = res-line.ankunft. 
      e1-date = res-line.abreise - 1. 
    END. 
    ELSE IF fixleist1.sequenz = 2 THEN 
    DO: 
      b1-date = res-line.ankunft. 
     e1-date = res-line.ankunft. 
    END. 
    ELSE IF fixleist1.sequenz = 6 THEN 
    DO: 
      IF fixleist1.lfakt = ? THEN b1-date = res-line.ankunft. 
      ELSE b1-date = fixleist1.lfakt. 
      e1-date = b1-date + fixleist1.dekade - 1. 
    END. 
    IF (b-date GE b1-date AND b-date LE e1-date) OR 
       (e-date GE b1-date AND e-date LE e1-date) OR 
       (b1-date GE b-date AND b1-date LE e-date) OR 
       (e1-date GE b-date AND e1-date LE e-date) THEN warn-it = YES. 
    IF warn-it THEN 
    DO: 
      msg-str = msg-str + CHR(2) + "&W"
              + translateExtended ("Overlapping posting found for",lvCAREA,"") + " "
              + STRING(fixleist-list.artnr) + " - " + fixleist-list.bezeich
              + CHR(10)
              + translateExtended ("Posting Date",lvCAREA,"") + " " + STRING(b1-date) + " - " + STRING(e1-date) 
              + CHR(10)
              + translateExtended ("Please recheck to avoid N/A double posting error.",lvCAREA,"").
    END. 
  END. 
END. 

/* Dzikri 44C4DB - log fixcost */
PROCEDURE fixcost-changes-add:
DEF VAR cid   AS CHAR NO-UNDO INIT "".
DEF VAR cdate AS CHAR NO-UNDO FORMAT "x(8)" INIT "        ". 
DEF BUFFER rqy FOR reslin-queasy.

    IF NOT AVAILABLE res-line THEN RETURN.
    IF res-line.active-flag = 2 THEN RETURN.
    
    IF res-line.changed NE ? THEN
    ASSIGN
        cid   = res-line.changed-id 
        cdate = STRING(res-line.changed)
    .
    CREATE rqy.
    ASSIGN
      rqy.key         = "ResChanges"
      rqy.resnr       = res-line.resnr
      rqy.reslinnr    = res-line.reslinnr
      rqy.date2       = TODAY
      rqy.number2     = TIME 
    . 
    rqy.char3 = STRING(res-line.ankunft) + ";" 
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
            + STRING(res-line.arrangement) + ";"
            + STRING(res-line.zipreis) + ";" 
            + STRING(res-line.zipreis) + ";"
            + STRING(cid) + ";" 
            + STRING(user-init) + ";" 
            + STRING(cdate, "x(8)") + ";" 
            + STRING(TODAY) + ";" 
            + STRING("ADD Fixcost:") + ";" 
            + STRING(fixleist-list.artnr) 
            + "-" + STRING(fixleist-list.bezeich) + ";"
            + STRING(is-fixrate, "x(3)") + ";" 
            + STRING(is-fixrate, "x(3)") + ";" 
    .
    FIND CURRENT rqy NO-LOCK.
    RELEASE rqy. 

END.

PROCEDURE fixcost-changes-chg:
DEF VAR cid   AS CHAR NO-UNDO INIT "".
DEF VAR cdate AS CHAR NO-UNDO FORMAT "x(8)" INIT "        ". 
DEF VAR temp-str1   AS CHAR NO-UNDO INIT "".
DEF VAR temp-str2   AS CHAR NO-UNDO INIT "".
DEF BUFFER rqy FOR reslin-queasy.

    IF NOT AVAILABLE res-line THEN RETURN.
    IF res-line.active-flag = 2 THEN RETURN.

    IF res-line.changed NE ? THEN
    ASSIGN
        cid   = res-line.changed-id 
        cdate = STRING(res-line.changed)
    .
    IF fixleist.number NE fixleist-list.number THEN
    DO:
      CREATE rqy.
      ASSIGN
        rqy.key         = "ResChanges"
        rqy.resnr       = res-line.resnr
        rqy.reslinnr    = res-line.reslinnr
        rqy.date2       = TODAY
        rqy.number2     = TIME 
      .  
      rqy.char3 = STRING(res-line.ankunft) + ";" 
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
              + STRING(res-line.arrangement) + ";"
              + STRING(res-line.zipreis) + ";" 
              + STRING(res-line.zipreis) + ";"
              + STRING(cid) + ";" 
              + STRING(user-init) + ";" 
              + STRING(cdate, "x(8)") + ";" 
              + STRING(TODAY) + ";" 
              + STRING("CHG Fixcost ")
              + STRING(fixleist.artnr) + "-" + STRING(fixleist.bezeich) + STRING(" FR:") + ";"  
              + STRING("QTY : ") + STRING(fixleist.number) + ";"
              + STRING(is-fixrate, "x(3)") + ";" 
              + STRING(is-fixrate, "x(3)") + ";" 
      .

      FIND CURRENT rqy NO-LOCK.
      RELEASE rqy. 

      CREATE rqy.
      ASSIGN
        rqy.key         = "ResChanges"
        rqy.resnr       = res-line.resnr
        rqy.reslinnr    = res-line.reslinnr
        rqy.date2       = TODAY
        rqy.number2     = TIME 
      .  
      rqy.char3 = STRING(res-line.ankunft) + ";" 
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
              + STRING(res-line.arrangement) + ";"
              + STRING(res-line.zipreis) + ";" 
              + STRING(res-line.zipreis) + ";"
              + STRING(cid) + ";" 
              + STRING(user-init) + ";" 
              + STRING(cdate, "x(8)") + ";" 
              + STRING(TODAY) + ";" 
              + STRING("CHG Fixcost ")
              + STRING(fixleist-list.artnr) + "-" + STRING(fixleist-list.bezeich) + STRING(" TO:") + ";"  
              + STRING("QTY : ") + STRING(fixleist-list.number) + ";"
              + STRING(is-fixrate, "x(3)") + ";" 
              + STRING(is-fixrate, "x(3)") + ";" 
      .

      FIND CURRENT rqy NO-LOCK.
      RELEASE rqy. 
    END.

    IF fixleist.betrag NE fixleist-list.betrag THEN
    DO:
      CREATE rqy.
      ASSIGN
        rqy.key         = "ResChanges"
        rqy.resnr       = res-line.resnr
        rqy.reslinnr    = res-line.reslinnr
        rqy.date2       = TODAY
        rqy.number2     = TIME 
      .  
      rqy.char3 = STRING(res-line.ankunft) + ";" 
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
              + STRING(res-line.arrangement) + ";"
              + STRING(res-line.zipreis) + ";" 
              + STRING(res-line.zipreis) + ";"
              + STRING(cid) + ";" 
              + STRING(user-init) + ";" 
              + STRING(cdate, "x(8)") + ";" 
              + STRING(TODAY) + ";" 
              + STRING("CHG Fixcost ")
              + STRING(fixleist.artnr) + "-" + STRING(fixleist.bezeich) + STRING(" FR:") + ";"  
              + STRING("Price : ") + STRING(fixleist.betrag) + ";"
              + STRING(is-fixrate, "x(3)") + ";" 
              + STRING(is-fixrate, "x(3)") + ";" 
      .

      FIND CURRENT rqy NO-LOCK.
      RELEASE rqy. 

      CREATE rqy.
      ASSIGN
        rqy.key         = "ResChanges"
        rqy.resnr       = res-line.resnr
        rqy.reslinnr    = res-line.reslinnr
        rqy.date2       = TODAY
        rqy.number2     = TIME 
      .  
      rqy.char3 = STRING(res-line.ankunft) + ";" 
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
              + STRING(res-line.arrangement) + ";"
              + STRING(res-line.zipreis) + ";" 
              + STRING(res-line.zipreis) + ";"
              + STRING(cid) + ";" 
              + STRING(user-init) + ";" 
              + STRING(cdate, "x(8)") + ";" 
              + STRING(TODAY) + ";" 
              + STRING("CHG Fixcost ")
              + STRING(fixleist-list.artnr) + "-" + STRING(fixleist-list.bezeich) + STRING(" TO:") + ";"  
              + STRING("Price : ") + STRING(fixleist-list.betrag) + ";"
              + STRING(is-fixrate, "x(3)") + ";" 
              + STRING(is-fixrate, "x(3)") + ";" 
      .

      FIND CURRENT rqy NO-LOCK.
      RELEASE rqy. 
    END.

    IF fixleist.sequenz NE fixleist-list.sequenz THEN
    DO:
      CREATE rqy.
      ASSIGN
        rqy.key         = "ResChanges"
        rqy.resnr       = res-line.resnr
        rqy.reslinnr    = res-line.reslinnr
        rqy.date2       = TODAY
        rqy.number2     = TIME 
      .  
      /* Dzikri 44C4DB - fixcost TYPE 6 treatment */
      IF fixleist.sequenz EQ 6 THEN temp-str1 = STRING(fixleist.sequenz) + "-" + STRING(fixleist.dekade) + "|" + STRING(fixleist.lfakt).
      ELSE temp-str1 = STRING(fixleist.sequenz).
      IF fixleist-list.sequenz EQ 6 THEN temp-str2 = STRING(fixleist-list.sequenz) + "-" + STRING(fixleist-list.dekade) + "|" + STRING(fixleist-list.lfakt).
      ELSE temp-str2 = STRING(fixleist-list.sequenz).
      /* Dzikri 44C4DB - END */

      rqy.char3 = STRING(res-line.ankunft) + ";" 
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
              + STRING(res-line.arrangement) + ";"
              + STRING(res-line.zipreis) + ";" 
              + STRING(res-line.zipreis) + ";"
              + STRING(cid) + ";" 
              + STRING(user-init) + ";" 
              + STRING(cdate, "x(8)") + ";" 
              + STRING(TODAY) + ";" 
              + STRING("CHG Fixcost ")
              + STRING(fixleist.artnr) + "-" + STRING(fixleist.bezeich) + STRING(" FR:") + ";"  
              + STRING("Type : ") + temp-str1 + ";"
              + STRING(is-fixrate, "x(3)") + ";" 
              + STRING(is-fixrate, "x(3)") + ";" 
      .

      FIND CURRENT rqy NO-LOCK.
      RELEASE rqy. 

      CREATE rqy.
      ASSIGN
        rqy.key         = "ResChanges"
        rqy.resnr       = res-line.resnr
        rqy.reslinnr    = res-line.reslinnr
        rqy.date2       = TODAY
        rqy.number2     = TIME 
      .  
      rqy.char3 = STRING(res-line.ankunft) + ";" 
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
              + STRING(res-line.arrangement) + ";"
              + STRING(res-line.zipreis) + ";" 
              + STRING(res-line.zipreis) + ";"
              + STRING(cid) + ";" 
              + STRING(user-init) + ";" 
              + STRING(cdate, "x(8)") + ";" 
              + STRING(TODAY) + ";" 
              + STRING("CHG Fixcost ")
              + STRING(fixleist-list.artnr) + "-" + STRING(fixleist-list.bezeich) + STRING(" TO:") + ";"  
              + STRING("Type : ") + temp-str2 + ";"
              + STRING(is-fixrate, "x(3)") + ";" 
              + STRING(is-fixrate, "x(3)") + ";" 
      .

      FIND CURRENT rqy NO-LOCK.
      RELEASE rqy. 
    END.
    
    /* Dzikri 44C4DB - fixcost TYPE 6 treatment */
    ELSE IF fixleist.sequenz EQ 6 AND fixleist-list.sequenz EQ 6 AND (fixleist.dekade NE fixleist-list.dekade OR fixleist.lfakt NE fixleist-list.lfakt) THEN
    DO:
      CREATE rqy.
      ASSIGN
        rqy.key         = "ResChanges"
        rqy.resnr       = res-line.resnr
        rqy.reslinnr    = res-line.reslinnr
        rqy.date2       = TODAY
        rqy.number2     = TIME 
      .  
      rqy.char3 = STRING(res-line.ankunft) + ";" 
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
              + STRING(res-line.arrangement) + ";"
              + STRING(res-line.zipreis) + ";" 
              + STRING(res-line.zipreis) + ";"
              + STRING(cid) + ";" 
              + STRING(user-init) + ";" 
              + STRING(cdate, "x(8)") + ";" 
              + STRING(TODAY) + ";" 
              + STRING("CHG Fixcost ")
              + STRING(fixleist.artnr) + "-" + STRING(fixleist.bezeich) + STRING(" FR:") + ";"  
              + STRING("Type : ") + STRING(fixleist.sequenz) + "-" + STRING(fixleist.dekade) + "|" + STRING(fixleist.lfakt) + ";"
              + STRING(is-fixrate, "x(3)") + ";" 
              + STRING(is-fixrate, "x(3)") + ";" 
      .

      FIND CURRENT rqy NO-LOCK.
      RELEASE rqy. 

      CREATE rqy.
      ASSIGN
        rqy.key         = "ResChanges"
        rqy.resnr       = res-line.resnr
        rqy.reslinnr    = res-line.reslinnr
        rqy.date2       = TODAY
        rqy.number2     = TIME 
      .  

      rqy.char3 = STRING(res-line.ankunft) + ";" 
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
              + STRING(res-line.arrangement) + ";"
              + STRING(res-line.zipreis) + ";" 
              + STRING(res-line.zipreis) + ";"
              + STRING(cid) + ";" 
              + STRING(user-init) + ";" 
              + STRING(cdate, "x(8)") + ";" 
              + STRING(TODAY) + ";" 
              + STRING("CHG Fixcost ")
              + STRING(fixleist-list.artnr) + "-" + STRING(fixleist-list.bezeich) + STRING(" TO:") + ";"  
              + STRING("Type : ") + STRING(fixleist-list.sequenz) + "-" + STRING(fixleist-list.dekade) + "|" + STRING(fixleist-list.lfakt) + ";"
              + STRING(is-fixrate, "x(3)") + ";" 
              + STRING(is-fixrate, "x(3)") + ";" 
      .
      
      FIND CURRENT rqy NO-LOCK.
      RELEASE rqy. 
    END.
END.
/* Dzikri 44C4DB - END */

