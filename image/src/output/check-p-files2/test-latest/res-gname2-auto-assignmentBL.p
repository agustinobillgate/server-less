
DEFINE TEMP-TABLE s-list 
  FIELD res-recid   AS INTEGER 
  FIELD resstatus   AS INTEGER 
  FIELD active-flag AS INTEGER
  FIELD flag        AS INTEGER INITIAL 0 
  FIELD karteityp   AS INTEGER 
  FIELD zimmeranz   AS INTEGER
  FIELD erwachs     AS INTEGER FORMAT ">9" LABEL "Adult" 
  FIELD kind1       AS INTEGER LABEL "Ch1" FORMAT ">9"    FIELD kind2       AS INTEGER LABEL "Ch2" FORMAT ">9" 
  FIELD old-zinr    AS CHAR 
  FIELD name        AS CHAR FORMAT "x(36)" LABEL "Name, Firstname, Title" 
  FIELD nat         AS CHAR FORMAT "x(3)" LABEL "Nation" 
  FIELD land        AS CHAR FORMAT "x(3)" LABEL "Cntry" 
  FIELD zinr        LIKE zimmer.zinr LABEL "RmNo " 
  FIELD eta         AS CHAR FORMAT "99:99" LABEL "ETA" INITIAL "0000"
  FIELD etd         AS CHAR FORMAT "99:99" LABEL "ETD" INITIAL "0000"
  FIELD flight1     AS CHAR
  FIELD flight2     AS CHAR
  FIELD rmcat       AS CHAR FORMAT "x(6)" LABEL "RmCat" 
  FIELD ankunft     AS DATE LABEL "Arrival" 
  FIELD abreise     AS DATE LABEL "Departure" 
  FIELD zipreis     AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" LABEL "Room Rate"
  FIELD bemerk      AS CHAR
. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR s-list.
DEF INPUT PARAMETER location AS CHAR.
DEF INPUT PARAMETER froom AS CHAR.
DEF INPUT PARAMETER troom AS CHAR.

RUN auto-assignment.

PROCEDURE auto-assignment: 
DEF BUFFER s1-list FOR s-list. 
DEF BUFFER s2-list FOR s-list. 
DEF BUFFER rline   FOR res-line. 
DEF BUFFER resline FOR res-line. 
DEF VAR last-zinr AS CHAR. 
DEF VAR do-it AS LOGICAL. 
DEF VAR found AS LOGICAL. 

  FOR EACH s1-list WHERE s1-list.zinr = "" AND s1-list.resstatus NE 11
      AND s1-list.zimmeranz = 1: 
    FIND FIRST rline WHERE RECID(rline) = s1-list.res-recid NO-LOCK. 
    found = NO. 
    
    IF location NE "" THEN
    FIND FIRST zimmer WHERE zimmer.CODE = location
      AND zimmer.zinr GE froom AND zimmer.zinr LE troom 
      AND zimmer.zikatnr = rline.zikatnr AND zimmer.setup = rline.setup 
      AND zimmer.zinr GT last-zinr NO-LOCK NO-ERROR. 
    ELSE
    FIND FIRST zimmer WHERE zimmer.zinr GE froom AND zimmer.zinr LE troom 
      AND zimmer.zikatnr = rline.zikatnr AND zimmer.setup = rline.setup 
      AND zimmer.zinr GT last-zinr NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE zimmer AND NOT found: 
      do-it = YES. 
      IF etage GT 0 AND (etage NE zimmer.etage) THEN do-it = NO. 
      IF do-it THEN 
      DO: 
        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
          AND outorder.betriebsnr NE rline.resnr 
          AND ((rline.ankunft GE gespstart AND rline.ankunft LE gespende) 
          OR (rline.abreise GT gespstart AND rline.abreise LE gespende) 
          OR (gespstart GE rline.ankunft AND gespstart LT rline.abreise) 
          OR (gespende GE rline.ankunft AND gespende LE rline.abreise)) 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE outorder THEN do-it = NO. 
      END. 
      IF do-it THEN 
      DO: 
        FIND FIRST resline WHERE RECID(resline) NE RECID(rline) 
          AND resline.resstatus LE 6 AND resline.active-flag LE 1 
          AND resline.zinr = zimmer.zinr 
          AND ((rline.ankunft GE resline.ankunft AND rline.ankunft LT resline.abreise) 
          OR (rline.abreise GT resline.ankunft AND rline.abreise LE resline.abreise) 
          OR (resline.ankunft GE rline.ankunft AND resline.ankunft LT rline.abreise) 
          OR (resline.abreise GT rline.ankunft AND resline.abreise LE rline.abreise)) 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE resline THEN do-it = NO. 
      END. 
      IF do-it THEN 
      DO: 
        s1-list.zinr = zimmer.zinr. 
        last-zinr = zimmer.zinr. 
        found = YES. 
      END. 
      ELSE 
      DO:
        IF location NE "" THEN
        FIND NEXT zimmer WHERE zimmer.CODE = location
          AND zimmer.zinr GE froom AND zimmer.zinr LE troom 
          AND zimmer.zikatnr = rline.zikatnr AND zimmer.setup = rline.setup 
          AND zimmer.zinr GT last-zinr NO-LOCK NO-ERROR. 
        ELSE
        FIND NEXT zimmer WHERE zimmer.zinr GE froom AND zimmer.zinr LE troom 
          AND zimmer.zikatnr = rline.zikatnr AND zimmer.setup = rline.setup 
          AND zimmer.zinr GT last-zinr NO-LOCK NO-ERROR. 
      END.
    END.
  END. 
  last-zinr = "". 
  FOR EACH s1-list WHERE s1-list.zinr = "" 
      AND s1-list.active-flag = 0 AND s1-list.resstatus NE 11: 
    FIND FIRST rline WHERE RECID(rline) = s1-list.res-recid NO-LOCK. 
    found = NO. 
    IF location NE "" THEN
    FIND FIRST zimmer WHERE zimmer.CODE = location
      AND zimmer.zinr GE froom AND zimmer.zinr LE troom 
      AND zimmer.zikatnr = rline.zikatnr AND zimmer.setup NE rline.setup 
      AND zimmer.zinr GT last-zinr NO-LOCK NO-ERROR. 
    ELSE
    FIND FIRST zimmer WHERE zimmer.zinr GE froom AND zimmer.zinr LE troom 
      AND zimmer.zikatnr = rline.zikatnr AND zimmer.setup NE rline.setup 
      AND zimmer.zinr GT last-zinr NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE zimmer AND NOT found: 
      do-it = YES. 
      IF etage GT 0 AND (etage NE zimmer.etage) THEN do-it = NO. 
      IF do-it THEN 
      DO: 
        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
          AND outorder.betriebsnr NE rline.resnr 
          AND ((rline.ankunft GE gespstart AND rline.ankunft LE gespende) 
          OR (rline.abreise GT gespstart AND rline.abreise LE gespende) 
          OR (gespstart GE rline.ankunft AND gespstart LT rline.abreise) 
          OR (gespende GE rline.ankunft AND gespende LE rline.abreise)) 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE outorder THEN do-it = NO. 
      END. 
      IF do-it THEN 
      DO: 
        FIND FIRST resline WHERE RECID(resline) NE RECID(rline) 
          AND resline.resstatus LE 6 AND resline.active-flag LE 1 
          AND resline.zinr = zimmer.zinr 
          AND ((rline.ankunft GE resline.ankunft AND rline.ankunft LT resline.abreise) 
          OR (rline.abreise GT resline.ankunft AND rline.abreise LE resline.abreise) 
          OR (resline.ankunft GE rline.ankunft AND resline.ankunft LT rline.abreise) 
          OR (resline.abreise GT rline.ankunft AND resline.abreise LE rline.abreise)) 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE resline THEN do-it = NO. 
      END. 
      IF do-it THEN 
      DO: 
        FIND FIRST s2-list WHERE s2-list.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
        IF AVAILABLE s2-list THEN do-it = NO. 
      END. 
      IF do-it THEN 
      DO: 
        s1-list.zinr = zimmer.zinr. 
        last-zinr = zimmer.zinr. 
        found = YES. 
      END. 
      ELSE 
      DO:
        IF location NE "" THEN
        FIND NEXT zimmer WHERE zimmer.CODE = location
          AND zimmer.zinr GE froom AND zimmer.zinr LE troom 
          AND zimmer.zikatnr = rline.zikatnr AND zimmer.setup NE rline.setup 
          AND zimmer.zinr GT last-zinr NO-LOCK NO-ERROR. 
        ELSE
        FIND NEXT zimmer WHERE zimmer.zinr GE froom AND zimmer.zinr LE troom 
          AND zimmer.zikatnr = rline.zikatnr AND zimmer.setup NE rline.setup 
          AND zimmer.zinr GT last-zinr NO-LOCK NO-ERROR. 
      END. 
    END.
  END. 
  /*MTOPEN QUERY q1 FOR EACH s-list BY s-list.ankunft BY s-list.rmcat 
    BY s-list.flag BY s-list.resstatus BY s-list.karteityp 
    BY s-list.erwachs DESCENDING. */
END. 
