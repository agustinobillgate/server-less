DEFINE TEMP-TABLE room-list 
  FIELD zistatus    AS INTEGER 
  FIELD ststr       AS CHAR FORMAT "x(2)" LABEL "St" 
  FIELD build       AS CHAR FORMAT "x(40)" 
  FIELD build-flag  AS CHAR FORMAT "x(1)"  LABEL "P" 
  FIELD recid1      AS INTEGER EXTENT 17 
  FIELD etage       AS INTEGER FORMAT "99 " LABEL "FL " 
  FIELD zinr        AS CHAR FORMAT "x(5)" LABEL "RmNo" 
  FIELD c-char      AS CHAR FORMAT "x(2)" LABEL " C" 
  FIELD i-char      AS CHAR FORMAT "x(2)" LABEL " I" 
  FIELD zikatnr     AS INTEGER 
  FIELD rmcat       AS CHAR FORMAT "x(5)" LABEL "RmCat" 
  FIELD connec      AS CHAR FORMAT "x(5)" LABEL "Cnec" 
  FIELD avtoday     AS CHAR FORMAT "x(2)" LABEL "" 
  FIELD gstatus     AS INTEGER EXTENT 17 
  FIELD bcol        AS INTEGER EXTENT 17 INITIAL 0 
  FIELD fcol        AS INTEGER EXTENT 17 INITIAL 0 
  FIELD room        AS CHAR EXTENT 17 FORMAT "x(5)"
  INDEX zinr_ix zinr.

DEF INPUT  PARAMETER print-it   AS LOGICAL. 
DEF INPUT  PARAMETER from-room  AS CHAR.
DEF INPUT  PARAMETER curr-date  AS DATE.
DEF INPUT  PARAMETER ci-date    AS DATE.
DEF OUTPUT PARAMETER TABLE FOR room-list.

DEFINE VARIABLE stat-list AS CHAR EXTENT 10 FORMAT "x(2)" 
  INITIAL [ "VC", "VU", "VD", "ED", "OD", "OC", "OO", "OM", "DD", "OS" ].

DEFINE VARIABLE item-fgcol AS INTEGER EXTENT 15 INITIAL 
  [15,15,15,15,15,15,15,0,15,0,0,15,0,0,0] NO-UNDO. 

DEFINE VARIABLE datum     AS DATE. 


RUN create-browse.

PROCEDURE create-browse: 
DEFINE VARIABLE datum1  AS DATE. 
DEFINE VARIABLE datum2  AS DATE. 
DEFINE VARIABLE to-date AS DATE. 
DEFINE VARIABLE depart  AS DATE.
DEFINE VARIABLE i       AS INTEGER. 
DEFINE VARIABLE j       AS INTEGER. 
DEFINE VARIABLE do-it   AS LOGICAL.
  
  FOR EACH room-list: 
    DELETE room-list. 
  END. 
  
  FOR EACH zimmer WHERE zimmer.zinr GE from-room NO-LOCK: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    create room-list. 
    room-list.zistatus = zimmer.zistatus. 
    IF zimmer.zistatus = 8 THEN room-list.ststr = stat-list[5]. 
    ELSE room-list.ststr = stat-list[zimmer.zistatus + 1]. 
    room-list.etage = zimmer.etage. 
    room-list.zinr = zimmer.zinr. 
    room-list.connec = zimmer.verbindung[1]. 
    room-list.c-char = " " + zimmer.zikennz + " ". 
    IF NOT zimmer.sleeping THEN room-list.i-char = " I ". 
    room-list.zikatnr = zimkateg.zikatnr. 
    room-list.rmcat = zimkateg.kurzbez. 
    IF zimmer.build NE "" THEN 
    DO: 
      room-list.build = zimmer.build. 
      room-list.build-flag = "*". 
    END. 
    IF zimmer.zistatus = 6 THEN 
    DO: 
        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
            AND outorder.gespstart LE ci-date NO-LOCK NO-ERROR. 
        IF AVAILABLE outorder AND 
            (outorder.betriebsnr = 3 OR outorder.betriebsnr = 4) THEN 
        DO: 
          room-list.zistatus = 9. 
          room-list.ststr = stat-list[10]. 
        END. 
    END. 
  END. 
 
  IF curr-date GE ci-date THEN
  FOR EACH res-line WHERE res-line.active-flag LE 1 
      AND res-line.abreise EQ curr-date 
      AND res-line.resstatus NE 12 
      AND res-line.zinr NE "" AND res-line.zinr GE from-room NO-LOCK: 
    FIND FIRST room-list WHERE room-list.zinr = res-line.zinr NO-ERROR. 
    IF AVAILABLE room-list THEN room-list.avtoday = ">". 
  END. 
  ELSE
  FOR EACH res-line WHERE res-line.active-flag = 2 
    AND res-line.abreise EQ curr-date 
    AND res-line.resstatus EQ 8
    AND res-line.zimmerfix = NO 
    AND res-line.zinr GE from-room NO-LOCK BY res-line.ankunft DESCENDING:
    IF res-line.ankunft LT res-line.abreise THEN do-it = YES.
    ELSE
    DO:
      FIND FIRST history WHERE history.resnr = res-line.resnr
        AND history.reslinnr = res-line.reslinnr
        AND history.zi-wechsel = NO NO-LOCK NO-ERROR.
      do-it = AVAILABLE history. 
    END.
    IF do-it THEN
    DO:
      FIND FIRST room-list WHERE room-list.zinr = res-line.zinr NO-ERROR. 
      IF AVAILABLE room-list THEN room-list.avtoday = ">". 
    END. 
  END.
 
  to-date = curr-date + 16. 
  FOR EACH res-line WHERE 
    ((res-line.resstatus LE 2 OR res-line.resstatus = 5) 
    AND res-line.zinr NE "" 
    AND res-line.zinr GE from-room AND res-line.active-flag = 0 
    AND  NOT to-date LT res-line.ankunft AND NOT curr-date GE res-line.abreise)
    OR ((resstatus = 6 OR resstatus = 13) AND res-line.active-flag = 1 AND 
    res-line.abreise GT curr-date AND res-line.zinr GE from-room) NO-LOCK: 
    IF res-line.ankunft GT curr-date THEN datum1 = res-line.ankunft. 
    ELSE datum1 = curr-date. 
    IF res-line.abreise LE to-date THEN datum2 = res-line.abreise - 1. 
    ELSE datum2 = to-date. 

    IF print-it THEN 
    DO: 
      i = datum1 - curr-date + 1. 
      FIND FIRST room-list WHERE room-list.zinr = res-line.zinr. 
      DO datum = datum1 TO datum2: 
        IF res-line.resstatus EQ 13 AND room-list.recid1[i] NE 0 THEN 
        DO: 
          /* NO ENTRY AS the main guest exists */ 
        END. 
        ELSE room-list.room[i] = SUBSTR(res-line.name, 1, 5). 
        i = i + 1. 
      END. 
    END. 
    i = datum1 - curr-date + 1. 
    j = 1. 
    FIND FIRST room-list WHERE room-list.zinr = res-line.zinr. 
    DO datum = datum1 TO datum2: 
      IF res-line.resstatus = 13 AND room-list.recid1[i] NE 0 THEN 
      DO: 
          /* NO ENTRY AS the main guest exists */ 
      END. 
      ELSE DO: 
        IF length(res-line.name) GE j THEN 
            room-list.room[i] = SUBSTR(res-line.name, j, 5). 
        IF res-line.resstatus LE 2 OR res-line.resstatus = 5
          THEN room-list.gstatus[i] = 1. 
        ELSE IF res-line.resstatus EQ 6 THEN room-list.gstatus[i] = 2. 
        ELSE IF res-line.resstatus EQ 13 THEN room-list.gstatus[i] = 3. 
        room-list.recid1[i] = RECID(res-line). 
        IF res-line.ziwech-zeit NE 0 THEN 
        DO: 
          room-list.bcol[i] = res-line.ziwech-zeit. 
          room-list.fcol[i] = item-fgcol[room-list.bcol[i]]. 
        END. 
      END. 
      i = i + 1. 
      j = j + 5. 
    END. 
  END. 
 
  IF curr-date LT ci-date THEN
  FOR EACH res-line WHERE res-line.resstatus = 8 AND res-line.active-flag = 2
    AND res-line.zinr GE from-room AND res-line.abreise GE res-line.ankunft 
    AND NOT res-line.zimmerfix /* room sharer */ 
    AND NOT to-date LT res-line.ankunft AND NOT curr-date GE res-line.abreise
    NO-LOCK BY res-line.ankunft DESCENDING: 
    IF res-line.ankunft GT curr-date THEN datum1 = res-line.ankunft. 
    ELSE datum1 = curr-date. 
    IF res-line.ankunft = res-line.abreise THEN depart = res-line.abreise.
    ELSE depart = res-line.abreise - 1.
    IF res-line.abreise LE to-date THEN datum2 = depart. 
    ELSE datum2 = to-date. 
 
    IF res-line.ankunft LT res-line.abreise THEN do-it = YES.
    ELSE
    DO:
      FIND FIRST history WHERE history.resnr = res-line.resnr
        AND history.reslinnr = res-line.reslinnr
        AND history.zi-wechsel = NO NO-LOCK NO-ERROR.
      do-it = AVAILABLE history. 
    END.
    IF do-it THEN
    DO:
      IF print-it THEN 
      DO: 
        i = datum1 - curr-date + 1. 
        FIND FIRST room-list WHERE room-list.zinr = res-line.zinr. 
        DO datum = datum1 TO datum2: 
          room-list.room[i] = SUBSTR(res-line.name, 1, LENGTH(res-line.NAME)). 
          i = i + 1. 
        END. 
      END. 
      i = datum1 - curr-date + 1. 
      j = 1. 
      FIND FIRST room-list WHERE room-list.zinr = res-line.zinr. 
      DO datum = datum1 TO datum2: 
        room-list.room[i] = SUBSTR(res-line.name, 1, LENGTH(res-line.NAME)). 
        room-list.gstatus[i] = 4. 
        room-list.recid1[i] = RECID(res-line). 
        IF res-line.ziwech-zeit NE 0 THEN 
        DO: 
          room-list.bcol[i] = res-line.ziwech-zeit. 
          room-list.fcol[i] = item-fgcol[room-list.bcol[i]].  
        END. 
        i = i + 1. 
        j = j + 5. 
      END.
    END.
  END. 
 
  FOR EACH outorder WHERE gespende GE curr-date NO-LOCK: 
    IF gespstart GT curr-date THEN datum1 = gespstart. 
    ELSE datum1 = curr-date. 
    IF gespende LT to-date THEN datum2 = gespende. 
    ELSE datum2 = to-date. 
    i = datum1 - curr-date + 1. 
    FIND FIRST room-list WHERE room-list.zinr = outorder.zinr NO-ERROR. 
    IF AVAILABLE room-list THEN 
    DO: 
      IF outorder.betriebsnr LE 1 THEN 
      DO datum = datum1 TO datum2: 
         room-list.room[i] = "O-O-O". 
         room-list.gstatus[i] = 9. 
         room-list.recid1[i] = RECID(outorder). 
         i = i + 1. 
      END. 
      ELSE IF outorder.betriebsnr = 2 THEN 
      DO datum = datum1 TO datum2: 
        IF room-list.recid1[i] = 0 THEN 
        DO: 
          room-list.room[i] = " O-M ". 
          room-list.gstatus[i] = 10. 
          room-list.recid1[i] = RECID(outorder). 
        END. 
        i = i + 1. 
      END. 
      ELSE IF outorder.betriebsnr = 3 OR outorder.betriebsnr = 4 THEN 
      DO datum = datum1 TO datum2: 
          room-list.room[i] = "O-O-S". 
          room-list.gstatus[i] = 11. 
          room-list.recid1[i] = RECID(outorder). 
          i = i + 1. 
      END. 
    END. 
  END. 
 
END. 
