DEF TEMP-TABLE fixleist-list   LIKE fixleist.

DEF INPUT  PARAMETER TABLE FOR fixleist-list.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER rec-id         AS INTEGER.
DEF INPUT  PARAMETER resnr          AS INTEGER.
DEF INPUT  PARAMETER reslinnr       AS INTEGER.
DEF INPUT  PARAMETER case-type      AS INTEGER.

DEF OUTPUT PARAMETER msg-str        AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-fixart".

FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK.

FIND FIRST fixleist-list.

IF case-type = 1 THEN       /* add */
DO:
    create fixleist.
    RUN fill-fixleist. 
    RUN check-article (RECID(fixleist)).
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST fixleist WHERE RECID(fixleist) = rec-id EXCLUSIVE-LOCK.
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

