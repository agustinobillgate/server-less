/*FT 201014 filter untuk expected departure --> inhouse dan abreise = ankunft1*/

DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD ind AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE htl-feature 
  FIELD s AS CHAR FORMAT "x(32)" LABEL "Possible Room Features" FONT 1 
  FIELD flag AS INTEGER INITIAL 1. 

DEFINE TEMP-TABLE room-list 
  FIELD i           AS INTEGER 
  FIELD flag        AS LOGICAL INITIAL YES 
  FIELD sleeping    AS LOGICAL INITIAL YES
  FIELD feature     AS CHAR FORMAT "x(16)" EXTENT 99 
  FIELD himmelsr    AS CHAR FORMAT "x(60)" LABEL "Room Features" 
  FIELD build       AS CHAR FORMAT "x(40)" 
  FIELD zikennz     AS CHAR FORMAT "x(1)" COLUMN-LABEL "A" 
  FIELD build-flag  AS CHAR FORMAT "x(1)" LABEL "P" 
  FIELD zistat      AS CHAR FORMAT "x(2)" INITIAL "  " LABEL "ST" 
  FIELD infochar    AS CHAR FORMAT "x(2)" LABEL "    " 
  FIELD zinr        LIKE zimmer.zinr LABEL "RmNo" 
  FIELD bezeich     AS CHAR FORMAT "x(24)" LABEL "Description" 
  FIELD etage       AS INTEGER FORMAT ">9" LABEL "Fl" 
  FIELD outlook     AS CHAR FORMAT "x(14)" LABEL "Overlook" 
  FIELD setup       AS CHAR FORMAT "x(14)" LABEL "BedSetup" 
  FIELD name        AS CHAR FORMAT "x(24)" LABEL "MainGuest" 
  FIELD comment     AS CHAR FORMAT "x(32)" LABEL "Guest Comment" 
  FIELD verbindung1 AS CHAR FORMAT "x(6)" LABEL "Connecting"
  FIELD verbindung2 AS CHAR FORMAT "x(6)" LABEL "Connecting"
  FIELD infonum     AS INTEGER FORMAT "9" INITIAL 3 
  FIELD prioritaet  AS INTEGER 
  FIELD recid1      AS INTEGER INITIAL 0 
  FIELD recid2      AS INTEGER INITIAL 0
  FIELD infostr     AS CHAR.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resNo     AS INTEGER. 
DEF INPUT  PARAMETER reslinNo  AS INTEGER. 
DEF INPUT  PARAMETER zikatNo   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER ankunft1  AS DATE    NO-UNDO. 
DEF INPUT  PARAMETER abreise1  AS DATE    NO-UNDO. 
DEF OUTPUT PARAMETER TABLE FOR room-list.
DEF OUTPUT PARAMETER TABLE FOR htl-feature.
/*
DEF VAR case-type AS INTEGER NO-UNDO INIT 1.
DEF VAR resNo     AS INTEGER INIT 1999. 
DEF VAR reslinNo  AS INTEGER INIT 1. 
DEF VAR zikatNo   AS INTEGER NO-UNDO INIT 2.
DEF VAR ankunft1  AS DATE    NO-UNDO INIT 10/17/14. 
DEF VAR abreise1  AS DATE    NO-UNDO INIT 10/18/14. 
*/
DEF VARIABLE vhp-limited    AS LOGICAL INIT NO  NO-UNDO.
DEF VARIABLE res-rowid      AS INTEGER          NO-UNDO.
DEF VARIABLE ci-date        AS DATE             NO-UNDO.

DEF BUFFER resline   FOR res-line.
DEF BUFFER res-line1 FOR res-line.

RUN htpdate.p (87, OUTPUT ci-date).

FIND FIRST res-line WHERE res-line.resnr = resNo
    AND res-line.reslinnr = reslinNo NO-LOCK.
ASSIGN res-rowid = INTEGER(RECID(res-line)).
/*
res-rowid = 2190856.*/

IF case-type = 1 THEN RUN create-list.
ELSE IF case-type = 2 THEN RUN create-all-list.

FOR EACH room-list:
    RUN show-info.
END.

PROCEDURE create-list: 

  FOR EACH room-list: 
    DELETE room-list. 
  END. 

  FOR EACH zimmer WHERE zimmer.zikatnr = zikatno 
    AND zimmer.zinr NE "" NO-LOCK BY zimmer.zinr: 
    
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
     AND NOT outorder.gespstart GT abreise1
     AND NOT outorder.gespende LT ankunft1 
     AND outorder.betriebsnr LE 2 NO-LOCK NO-ERROR.
    
    IF NOT AVAILABLE outorder THEN
    DO:
      IF zimmer.zistatus = 6 AND ankunft1 LE ci-date THEN .
      ELSE
      DO:
        CREATE room-list. 
        ASSIGN
          room-list.zinr       = zimmer.zinr 
          room-list.prioritaet = zimmer.prioritaet
          room-list.sleeping   = zimmer.sleeping
        .
      END.
    END.
  END.
  
  FOR EACH resline WHERE resline.zikatnr = zikatno
     AND resline.zinr NE ""
     AND resline.resstatus NE 12
     AND resline.active-flag LE 1
     AND resline.l-zuordnung[3] = 0 NO-LOCK:
     IF INTEGER(RECID(resline)) = res-rowid THEN .
     ELSE IF resline.resstatus = 6
         AND resline.abreise LE ankunft1 THEN.
     ELSE IF (resline.abreise LE ankunft1)
       OR (resline.ankunft GE abreise1) THEN.
     ELSE
     DO:
       FIND FIRST room-list WHERE room-list.zinr = resline.zinr
         NO-ERROR.
       IF AVAILABLE room-list THEN DELETE room-list.
     END.
  END.
  /*
  FOR EACH room-list:
     /* expected departure guest */
     FIND FIRST res-line1 WHERE res-line1.resstatus = 6 
       AND res-line1.zinr = room-list.zinr NO-LOCK NO-ERROR. 
     IF AVAILABLE res-line1 AND res-line1.abreise = ankunft1 THEN 
     DO:
       ASSIGN
         room-list.name    = res-line1.NAME 
         room-list.comment = res-line1.bemerk
       .
     END.
     ELSE IF AVAILABLE res-line1 AND res-line1.abreise NE ankunft1 THEN
       DELETE room-list.
  END.
  */
  RUN complete-list.
END. 
 
PROCEDURE create-all-list: 

  FOR EACH room-list: 
    DELETE room-list. 
  END. 

  FOR EACH zimmer WHERE zimmer.zinr NE "" NO-LOCK BY zimmer.zinr: 
    
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
     AND NOT outorder.gespstart GT abreise1
     AND NOT outorder.gespende LT ankunft1 
     AND outorder.betriebsnr LE 2 NO-LOCK NO-ERROR.
    
    IF NOT AVAILABLE outorder THEN
    DO:
      CREATE room-list. 
      ASSIGN
        room-list.zinr       = zimmer.zinr 
        room-list.prioritaet = zimmer.prioritaet
        room-list.sleeping   = zimmer.sleeping
      . 
    END.
  END.

  FOR EACH resline WHERE resline.zinr NE ""
     AND resline.resstatus NE 12
     AND resline.active-flag LE 1
     AND resline.l-zuordnung[3] = 0 NO-LOCK:
     
     IF INTEGER(RECID(resline)) = res-rowid THEN .
     ELSE IF resline.resstatus = 6
         AND resline.abreise LE ankunft1 THEN.
     ELSE IF (resline.abreise LE ankunft1)
       OR (resline.ankunft GE abreise1) THEN.
     ELSE
     DO:
       FIND FIRST room-list WHERE room-list.zinr = resline.zinr
         NO-ERROR.
       IF AVAILABLE room-list THEN DELETE room-list.
     END.
  END.

  RUN complete-list.
END. 
 
PROCEDURE complete-list: 
DEFINE VARIABLE stat-list AS CHAR EXTENT 10 FORMAT "x(23)" NO-UNDO.   
stat-list[1] = "VC".
stat-list[2] = "CU".
stat-list[3] = "VD".
stat-list[4] = "ED".
stat-list[5] = "OD".
stat-list[6] = "OC".

  FOR EACH zimmer NO-LOCK: 
    create om-list. 
    om-list.zinr = zimmer.zinr. 
    om-list.ind = zimmer.zistatus + 1. 
  END. 
  FOR EACH outorder WHERE outorder.betriebsnr GE 2 AND 
    outorder.gespstart LE ci-date AND outorder.gespende GE ci-date NO-LOCK: 
    FIND FIRST om-list WHERE om-list.zinr = outorder.zinr NO-ERROR.
    IF AVAILABLE om-list THEN om-list.ind = 8. 
  END. 

  FOR EACH room-list: 
    FIND FIRST zimmer WHERE zimmer.zinr = room-list.zinr NO-LOCK NO-ERROR. 
    room-list.zikennz = zimmer.zikennz. 
 
    IF zimmer.himmelsr NE "" THEN RUN fill-feature. 
 
    room-list.bezeich = zimmer.bezeich. 
    room-list.verbindung1 = zimmer.verbindung[1]. 
    room-list.verbindung2 = zimmer.verbindung[2].
    room-list.etage = zimmer.etage. 
 
    IF zimmer.typ NE 0 THEN 
    DO: 
      FIND FIRST paramtext WHERE paramtext.txtnr = 230 
        AND paramtext.sprachcode = zimmer.typ NO-LOCK NO-ERROR. 
      IF AVAILABLE paramtext THEN room-list.outlook = paramtext.ptexte. 
    END. 
 
    IF zimmer.setup NE 0 THEN 
    DO: 
      FIND FIRST paramtext WHERE 
        paramtext.txtnr = (zimmer.setup + 9200) NO-LOCK NO-ERROR. 
      IF AVAILABLE paramtext THEN room-list.setup = TRIM(paramtext.ptexte). 
    END. 
 
    FIND FIRST resline WHERE resline.zinr = room-list.zinr 
      AND resline.active-flag LT 2 AND resline.abreise = ankunft1 
      AND resline.resstatus LE 6 NO-LOCK NO-ERROR. 
    IF AVAILABLE resline THEN 
    DO: 
      room-list.infonum = room-list.infonum - 2. 
      room-list.recid1 = INTEGER(RECID(resline)). 
    END. 
 
    FIND FIRST resline WHERE resline.zinr = room-list.zinr 
      AND resline.active-flag = 0 AND resline.ankunft = abreise 
       NO-LOCK NO-ERROR. 
    IF AVAILABLE resline THEN 
    DO: 
      room-list.infonum = room-list.infonum - 1. 
      room-list.recid2 = INTEGER(RECID(resline)). 
    END. 
 
    IF room-list.infonum = 0 THEN room-list.infochar = "<>". 
    ELSE IF room-list.infonum = 1 THEN room-list.infochar = "< ". 
    ELSE IF room-list.infonum = 2 THEN room-list.infochar = " >". 
/* 
    IF ankunft1 LE ci-date THEN 
*/ 
    FIND FIRST om-list WHERE om-list.zinr = room-list.zinr NO-LOCK NO-ERROR.
    IF room-list.prioritaet LT 99999 THEN DO: 
      room-list.zistat = stat-list[om-list.ind].
      
      /*MT
      IF zimmer.zistatus = 0 THEN room-list.zistat = "". 
      ELSE DO: 
        IF res-line.resstatus = 6 AND zimmer.zistatus GE 3 
          AND res-line.zinr NE room-list.zinr THEN 
        DO: 
          IF ankunft1 LE ci-date THEN delete room-list. 
        END. 
        ELSE DO: 
          IF zimmer.zistatus = 1 THEN room-list.zistat = "CU". 
          ELSE IF zimmer.zistatus = 2 THEN room-list.zistat = "VD". 
          ELSE IF zimmer.zistatus = 3 THEN room-list.zistat = "ED". 
          ELSE IF (zimmer.zistatus = 4 OR zimmer.zistatus = 5 
          OR zimmer.zistatus = 8) THEN room-list.zistat = "OC". 
        END. 
      END. 
      */
    END. 
  END. 
END. 
 
PROCEDURE fill-feature: 
DEFINE VARIABLE i  AS INTEGER. 
DEFINE VARIABLE j  AS INTEGER. 
DEFINE VARIABLE k  AS INTEGER. 
DEFINE VARIABLE n  AS INTEGER. 
DEFINE VARIABLE ch AS CHAR FORMAT "x(12)". 

  n = 0. 
  j = 1. 
  room-list.himmelsr = "".  
  DO i = 1 TO length(zimmer.himmelsr): 
    IF SUBSTR(zimmer.himmelsr,i,1) = ";" OR 
      SUBSTR(zimmer.himmelsr,i,1) = "," THEN 
    DO: 
      ch = "". 
      DO k = j TO (j + n - 1): 
        IF SUBSTR(zimmer.himmelsr,k,1) NE chr(10) THEN 
        ch = ch + SUBSTR(zimmer.himmelsr, k, 1). 
      END. 
      ch = TRIM(ch). 
      IF (LENGTH(ch) NE 0) AND (SUBSTR(ch,1,1) NE "$") THEN 
      DO: 
        room-list.i = room-list.i + 1. 
        room-list.feature[room-list.i] = ch. 
        FIND FIRST htl-feature WHERE htl-feature.s = ch NO-ERROR. 
        IF NOT AVAILABLE htl-feature THEN 
        DO: 
          CREATE htl-feature. 
          ASSIGN
            htl-feature.s = ch
            room-list.himmelsr = room-list.himmelsr + ch + ";"
          .
        END. 
      END. 
      j = i + 1. 
      n = 0. 
    END. 
    ELSE n = n + 1. 
  END. 
  IF n NE 0 THEN 
  DO: 
    ch = "". 
    DO k = j TO (j + n - 1): 
      IF SUBSTR(zimmer.himmelsr,k,1) NE chr(10) THEN 
      ch = ch + SUBSTR(zimmer.himmelsr, k, 1). 
    END. 
    ch = TRIM(ch). 
    IF (LENGTH(ch) NE 0) AND (SUBSTR(ch,1,1) NE "$") THEN 
    DO: 
      room-list.i = room-list.i + 1. 
      room-list.feature[room-list.i] = ch. 
      FIND FIRST htl-feature WHERE htl-feature.s = ch NO-ERROR. 
      IF NOT AVAILABLE htl-feature THEN 
      DO: 
        CREATE htl-feature. 
        ASSIGN
          htl-feature.s = ch
          room-list.himmelsr = room-list.himmelsr + ch + ";"
        .
      END. 
    END. 
  END. 
  
  /*FDL March 13, 2023 => Ticket 2C389B*/
  room-list.himmelsr = zimmer.himmelsr.
END. 



PROCEDURE show-info: 
  room-list.infostr = "". 
  IF AVAILABLE room-list AND room-list.infochar NE "" THEN 
  DO: 
    IF SUBSTR(room-list.infochar,1,1) = "<" THEN 
    DO: 
      FIND FIRST res-line1 
        WHERE RECID(res-line1) = room-list.recid1 NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line1 THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = res-line1.gastnrpay NO-LOCK. 
        room-list.infostr = "". 
        room-list.infostr = room-list.infostr 
                  + "<  ResNo:  " 
                  + STRING(res-line1.resnr) + chr(10). 
        room-list.infostr = room-list.infostr + "    " + guest.name + ", " 
                  + guest.vorname1 + guest.anredefirma + chr(10). 
        room-list.infostr = room-list.infostr + "Arrival : " + STRING(res-line1.ankunft) + chr(10). 
        room-list.infostr = room-list.infostr + "Depart : " + STRING(res-line1.abreise). 
        room-list.infostr = room-list.infostr + chr(10) + chr(10). 
      END. 
    END. 
    IF SUBSTR(room-list.infochar,2,1) = ">" THEN 
    DO: 
      FIND FIRST res-line1 
        WHERE RECID(res-line1) = room-list.recid2 NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line1 THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = res-line1.gastnrpay NO-LOCK. 
        room-list.infostr = room-list.infostr 
                  + ">  ResNo:  " 
                  + STRING(res-line1.resnr) + chr(10). 
        room-list.infostr = room-list.infostr + "    " + guest.name + ", " 
                  + guest.vorname1 + guest.anredefirma + chr(10). 
        room-list.infostr = room-list.infostr + "Arrival : " + STRING(res-line1.ankunft) + chr(10). 
        room-list.infostr = room-list.infostr + "Depart : " + STRING(res-line1.abreise) + chr(10). 
      END. 
    END. 
  END.
END. 
