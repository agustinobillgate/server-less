DEF TEMP-TABLE t-res-line LIKE res-line
    FIELD rec-id AS INT .
DEF TEMP-TABLE t-outorder LIKE outorder
    FIELD rec-id AS INT.
DEF TEMP-TABLE t-outorder1 LIKE outorder.
DEF TEMP-TABLE t-res-line2 
    FIELD resnr LIKE res-line.resnr
    FIELD zinr LIKE res-line.zinr
    FIELD NAME LIKE res-line.name
    FIELD rec-id AS INT
    FIELD ziwech-zeit LIKE res-line.ziwech-zeit
    FIELD ankunft LIKE res-line.ankunft
    FIELD abreise LIKE res-line.abreise
.

DEF TEMP-TABLE t-res-line3 LIKE res-line
    FIELD rec-id AS INT .

DEFINE TEMP-TABLE room-list 
  FIELD location    AS CHAR
  FIELD zistatus    AS INTEGER 
  FIELD ststr       AS CHAR FORMAT "x(2) "   LABEL "St" 
  FIELD build       AS CHAR FORMAT "x(40)" 
  FIELD build-flag  AS CHAR FORMAT "x(2)"   LABEL "P " 
  FIELD etage       AS INTEGER FORMAT "99 " LABEL " FL " 
  FIELD zinr        AS CHAR FORMAT "x(9)"   LABEL "RmNo" /*RA 080622 tambah lenght*/
  FIELD c-char      AS CHAR FORMAT "x(2)"   LABEL " C" 
  FIELD i-char      AS CHAR FORMAT "x(2)"   LABEL " I"
  FIELD zikatnr     AS INTEGER 
  FIELD rmcat       AS CHAR FORMAT "x(8)"   LABEL "RmCat" 
  FIELD bezeich     AS CHARACTER FORMAT "x(30)" LABEL "Room Description" /*Irfan 080118*/
  FIELD connec      AS CHAR FORMAT "x(5)"   LABEL "Cnec" 
  FIELD avtoday     AS CHAR FORMAT "x(1)"   LABEL "" 
  FIELD recid1      AS INTEGER EXTENT 28 
  FIELD gstatus     AS INTEGER EXTENT 28 
  FIELD bcol        AS INTEGER EXTENT 28 INITIAL 0 
  FIELD fcol        AS INTEGER EXTENT 28 INITIAL 0 
  FIELD room        AS CHAR    EXTENT 28 FORMAT "x(32)" 
  FIELD off-mkt     AS LOGICAL EXTENT 28 INITIAL NO
  FIELD resnr       AS INTEGER EXTENT 28
  INDEX zinr_ix zinr. 

DEF INPUT PARAMETER from-room AS CHAR.
DEF INPUT PARAMETER curr-date AS DATE.
DEF INPUT PARAMETER ci-date AS DATE.

DEF OUTPUT PARAMETER do-it AS LOGICAL.
DEF OUTPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-res-line.
DEF OUTPUT PARAMETER TABLE FOR t-res-line2.
DEF OUTPUT PARAMETER TABLE FOR t-outorder.
DEF OUTPUT PARAMETER TABLE FOR t-outorder1.
DEF OUTPUT PARAMETER TABLE FOR room-list.
DEF OUTPUT PARAMETER TABLE FOR t-res-line3.


DEFINE VARIABLE stat-list AS CHAR EXTENT 10 FORMAT "x(2)" 
  INITIAL [ "VC", "VU", "VD", "ED", "OD", "OC", "OO", "OM", "DD", "OS" ]. 
DEF VAR a AS INT INIT 0.

DEFINE VARIABLE item-fgcol AS INTEGER EXTENT 15 INITIAL 
  [15,15,15,15,15,15,15,0,15,0,0,15,0,0,0] NO-UNDO. 

RUN create-browse.
RUN assign-room-list.

PROCEDURE create-browse: 
DEFINE VARIABLE datum1  AS DATE. 
DEFINE VARIABLE datum2  AS DATE. 
DEFINE VARIABLE depart  AS DATE.
DEFINE VARIABLE i       AS INTEGER. 
DEFINE VARIABLE j       AS INTEGER. 
DEFINE VARIABLE do-it1  AS LOGICAL.

  FOR EACH room-list: 
    DELETE room-list. 
  END. 
  
  FOR EACH zimmer WHERE zimmer.zinr GE from-room NO-LOCK:
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR. 
    IF AVAILABLE zimkateg THEN 
    DO:
      create room-list.
      ASSIGN
          room-list.location = zimmer.CODE
          room-list.zistatus = zimmer.zistatus
      . 
      IF zimmer.zistatus = 8 THEN room-list.ststr = stat-list[5]. 
      ELSE room-list.ststr = stat-list[zimmer.zistatus + 1]. 
      room-list.etage = zimmer.etage. 
      room-list.zinr = zimmer.zinr. 
      room-list.connec = zimmer.verbindung[1]. 
      room-list.c-char = " " + zimmer.zikennz + " ". 
      IF NOT zimmer.sleeping THEN room-list.i-char = " I ". 
      room-list.zikatnr = zimkateg.zikatnr. 
      room-list.rmcat = zimkateg.kurzbez. 
      room-list.bezeich = zimkateg.bezeichnung. /*Irfan 080118*/
      IF zimmer.build NE "" THEN 
      DO: 
        room-list.build = zimmer.build. 
        room-list.build-flag = "*". 
      END. 
    END. 
  END.
 
  IF curr-date GE ci-date THEN DO:
      
      FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.abreise EQ curr-date 
        AND res-line.resstatus NE 12 
        AND res-line.zinr NE "" AND res-line.zinr GE from-room NO-LOCK: 
        FIND FIRST room-list WHERE room-list.zinr = res-line.zinr NO-ERROR. 
        IF AVAILABLE room-list THEN room-list.avtoday = ">". 
      END. 
  END.
  ELSE DO:
      FOR EACH res-line WHERE res-line.active-flag = 2 
        AND res-line.abreise EQ curr-date 
        AND res-line.resstatus EQ 8
        AND res-line.zimmerfix = NO 
        AND res-line.zinr GE from-room NO-LOCK BY res-line.ankunft DESCENDING:
        IF res-line.ankunft LT res-line.abreise THEN do-it1 = YES.
        ELSE
        DO:
          FIND FIRST history WHERE history.resnr = res-line.resnr
            AND history.reslinnr = res-line.reslinnr
            AND history.zi-wechsel = NO NO-LOCK NO-ERROR.
          do-it1 = AVAILABLE history. 
        END.
        IF do-it1 THEN
        DO:
          FIND FIRST room-list WHERE room-list.zinr = res-line.zinr NO-ERROR. 
          IF AVAILABLE room-list THEN room-list.avtoday = ">". 
        END. 
      END.

  END.
  to-date = curr-date + 27. 
  FOR EACH res-line WHERE 
    ((res-line.resstatus LE 2 OR res-line.resstatus = 5) 
    AND res-line.zinr NE "" 
    AND res-line.zinr GE from-room AND res-line.active-flag = 0 
    AND  NOT to-date LT res-line.ankunft AND NOT curr-date GE res-line.abreise)
    OR ((resstatus = 6 OR resstatus = 13) AND res-line.active-flag = 1 AND 
    res-line.abreise GT curr-date AND res-line.zinr GE from-room) NO-LOCK:
    
    CREATE t-res-line.
    BUFFER-COPY res-line TO t-res-line.
    ASSIGN t-res-line.rec-id = RECID(res-line).
    
    FIND FIRST history WHERE history.resnr = res-line.resnr
        AND history.reslinnr = res-line.reslinnr
        AND history.zi-wechsel = NO NO-LOCK NO-ERROR.
    IF AVAILABLE history THEN DO:
        CREATE t-res-line3.
        BUFFER-COPY res-line TO t-res-line3.
        ASSIGN t-res-line3.rec-id = RECID(res-line)
               t-res-line3.zinr   = history.zinr.
    END.

    IF (res-line.resstatus LE 2 OR res-line.resstatus = 5) THEN
    DO:
        FIND FIRST outorder WHERE outorder.zinr = res-line.zinr
          AND outorder.betriebsnr = res-line.resnr NO-LOCK NO-ERROR.
        IF AVAILABLE outorder THEN
        DO:
            CREATE t-outorder1.
            BUFFER-COPY outorder TO t-outorder1.
        END.
    END.

    /*MTIF res-line.ankunft GT curr-date THEN datum1 = res-line.ankunft. 
    ELSE datum1 = curr-date. 
    IF res-line.abreise LE to-date THEN datum2 = res-line.abreise - 1. 
    ELSE datum2 = to-date. */
 
    /*MT
    IF print-it THEN 
    DO: 
      i = datum1 - curr-date + 1. 
      FIND FIRST room-list WHERE room-list.zinr = res-line.zinr NO-ERROR. 
      DO datum = datum1 TO datum2: 
        IF res-line.resstatus EQ 13 AND room-list.recid1[i] NE 0 THEN 
        DO: 
          /* NO ENTRY AS the main guest exists */ 
        END. 
        ELSE room-list.room[i] = SUBSTR(res-line.name, 1, LENGTH(res-line.NAME)). 
        i = i + 1. 
      END. 
    END. 
    i = datum1 - curr-date + 1. 
    j = 1. 
    FIND FIRST room-list WHERE room-list.zinr = res-line.zinr NO-ERROR. 
    DO datum = datum1 TO datum2: 
      IF res-line.resstatus = 13 AND room-list.recid1[i] NE 0 THEN 
      DO: 
          /* NO ENTRY AS the main guest exists */ 
      END. 
      ELSE 
      DO: 
/* 
        IF length(res-line.name) GE j THEN 
            room-list.room[i] = SUBSTR(res-line.name, j, 5). 
*/ 
        room-list.room[i] = SUBSTR(res-line.name, 1, LENGTH(res-line.NAME)). 
        IF (res-line.resstatus LE 2 OR res-line.resstatus = 5) THEN
        DO:
          ASSIGN room-list.gstatus[i] = 1. 
          IF res-line.ankunft = datum THEN 
          DO:
            FIND FIRST outorder WHERE outorder.zinr = res-line.zinr
              AND outorder.betriebsnr = res-line.resnr NO-LOCK NO-ERROR. 
            IF AVAILABLE outorder THEN ASSIGN room-list.off-mkt[i] = YES.
            ELSE ASSIGN room-list.off-mkt[i] = NO.
          END.
        END.
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
    END. */
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
       CREATE t-res-line2.
       ASSIGN
         t-res-line2.resnr        = res-line.resnr
         t-res-line2.zinr         = res-line.zinr
         t-res-line2.NAME         = res-line.name
         t-res-line2.rec-id       = RECID(res-line)
         t-res-line2.ziwech-zeit  = res-line.ziwech-zeit
         t-res-line2.ankunft      = res-line.ankunft
         t-res-line2.abreise      = res-line.abreise
         
       .

      /*MTIF print-it THEN 
      DO: 
        i = datum1 - curr-date + 1. 
        FIND FIRST room-list WHERE room-list.zinr = res-line.zinr NO-ERROR. 
        DO datum = datum1 TO datum2: 
          room-list.room[i] = SUBSTR(res-line.name, 1, LENGTH(res-line.NAME)). 
          i = i + 1. 
        END. 
      END. 
      i = datum1 - curr-date + 1. 
      j = 1. 
      FIND FIRST room-list WHERE room-list.zinr = res-line.zinr NO-ERROR. 
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
      END.*/
    END.
  END.

  
  FOR EACH outorder WHERE outorder.gespende GE curr-date NO-LOCK:
    CREATE t-outorder.
    BUFFER-COPY outorder TO t-outorder.
    ASSIGN t-outorder.rec-id = RECID(outorder).
    /*MTIF gespstart GT curr-date THEN datum1 = gespstart. 
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
      ELSE IF outorder.betriebsnr EQ 3 OR outorder.betriebsnr = 4 THEN 
      DO datum = datum1 TO datum2: 
         room-list.room[i] = "O-O-S". 
         room-list.gstatus[i] = 12. 
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
    END. */
  END.
END. 

PROCEDURE assign-room-list:
    DEFINE VARIABLE datum   AS DATE.
    DEFINE VARIABLE datum1  AS DATE.
    DEFINE VARIABLE datum2  AS DATE.
    DEFINE VARIABLE depart  AS DATE.
    DEFINE VARIABLE i       AS INTEGER. 
    DEFINE VARIABLE j       AS INTEGER.

    FOR EACH t-res-line :
        IF t-res-line.ankunft GT curr-date THEN datum1 = t-res-line.ankunft. 
        ELSE datum1 = curr-date. 
        IF t-res-line.abreise LE to-date THEN datum2 = t-res-line.abreise - 1. 
        ELSE datum2 = to-date.                     
    
        i = datum1 - curr-date + 1. 
        FIND FIRST t-res-line3 WHERE t-res-line3.resnr = t-res-line.resnr
            AND t-res-line3.reslinnr = t-res-line.reslinnr
            AND t-res-line3.zinr EQ t-res-line.zinr NO-LOCK NO-ERROR. /*FD Aug 16, 2022 => ticket DC127B Chg NE "" to EQ zinr*/
        IF AVAILABLE t-res-line3 THEN 
        DO:     
            FIND FIRST room-list WHERE room-list.zinr = t-res-line3.zinr NO-ERROR.
            IF t-res-line3.resstatus = 13 AND room-list.recid1[i] NE 0 THEN 
            DO: 
            END. 
            ELSE 
            DO: 
                room-list.room[i] = SUBSTR(t-res-line3.name, 1, LENGTH(t-res-line3.NAME)).
                IF (t-res-line3.resstatus LE 2 OR t-res-line3.resstatus = 5) THEN
                DO:
                    ASSIGN room-list.gstatus[i] = 1. 
                    IF t-res-line3.ankunft = curr-date THEN 
                    DO:
                        FIND FIRST t-outorder1 WHERE t-outorder1.zinr = t-res-line3.zinr
                            AND t-outorder1.betriebsnr = t-res-line3.resnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE t-outorder1 THEN ASSIGN room-list.off-mkt[i] = YES.
                        ELSE ASSIGN room-list.off-mkt[i] = NO.
                    END.
                END.
                ELSE IF t-res-line3.resstatus EQ 6 THEN room-list.gstatus[i] = 2. 
                ELSE IF t-res-line3.resstatus EQ 13 THEN room-list.gstatus[i] = 3. 
                room-list.recid1[i] = t-res-line3.rec-id.
                room-list.resnr[i] = t-res-line3.resnr.
                IF t-res-line3.ziwech-zeit NE 0 THEN 
                DO: 
                    room-list.bcol[i] = t-res-line3.ziwech-zeit. 
                    room-list.fcol[i] = item-fgcol[room-list.bcol[i]]. 
                END. 
            END. 
            i = i + 1.
            datum1 = datum1 + 1.
        END.       
    
        j = 1. 
        FIND FIRST room-list WHERE room-list.zinr = t-res-line.zinr NO-ERROR. 
        DO datum = datum1 TO datum2:         
            IF t-res-line.resstatus = 13 AND room-list.recid1[i] NE 0 THEN 
            DO: 
            END. 
            ELSE 
            DO:             
                room-list.room[i] = SUBSTR(t-res-line.name, 1, LENGTH(t-res-line.NAME)). 
                IF (t-res-line.resstatus LE 2 OR t-res-line.resstatus = 5) THEN
                DO:
                    ASSIGN room-list.gstatus[i] = 1. 
                    IF t-res-line.ankunft = datum THEN 
                    DO:
                        FIND FIRST t-outorder1 WHERE t-outorder1.zinr = t-res-line.zinr
                            AND t-outorder1.betriebsnr = t-res-line.resnr NO-LOCK NO-ERROR. 
                        IF AVAILABLE t-outorder1 THEN ASSIGN room-list.off-mkt[i] = YES.
                        ELSE ASSIGN room-list.off-mkt[i] = NO.
                    END.
                END.
                ELSE IF t-res-line.resstatus EQ 6 THEN room-list.gstatus[i] = 2. 
                ELSE IF t-res-line.resstatus EQ 13 THEN room-list.gstatus[i] = 3. 
                room-list.recid1[i] = t-res-line.rec-id.
                room-list.resnr[i] = t-res-line.resnr.
                IF t-res-line.ziwech-zeit NE 0 THEN 
                DO: 
                  room-list.bcol[i] = t-res-line.ziwech-zeit. 
                  room-list.fcol[i] = item-fgcol[room-list.bcol[i]]. 
                END. 
            END. 
            i = i + 1. 
            j = j + 5. 
        END.
    END.
        
    FOR EACH t-res-line2:
          /*ITA 240214*/
        IF t-res-line2.ankunft GT curr-date THEN datum1 = t-res-line2.ankunft. 
        ELSE datum1 = curr-date. 
        IF t-res-line2.ankunft = t-res-line2.abreise THEN depart = t-res-line2.abreise.
        ELSE depart = t-res-line2.abreise - 1.
        IF t-res-line2.abreise LE to-date THEN datum2 = depart. 
        ELSE datum2 = to-date. 
                
        i = datum1 - curr-date + 1. 
        j = 1. 
        FIND FIRST room-list WHERE room-list.zinr = t-res-line2.zinr NO-ERROR. 
        DO datum = datum1 TO datum2: 
            room-list.room[i] = SUBSTR(t-res-line2.name, 1, LENGTH(t-res-line2.NAME)). 
            room-list.gstatus[i] = 4. 
            room-list.recid1[i] = t-res-line2.rec-id. 
            room-list.resnr[i] = t-res-line2.resnr.
            IF t-res-line2.ziwech-zeit NE 0 THEN 
            DO: 
                room-list.bcol[i] = t-res-line2.ziwech-zeit. 
                room-list.fcol[i] = item-fgcol[room-list.bcol[i]].  
            END. 
            i = i + 1. 
            j = j + 5. 
        END.
    END.
        
    FOR EACH t-outorder :
        IF t-outorder.gespstart GT curr-date THEN datum1 = t-outorder.gespstart.
        ELSE datum1 = curr-date. 
        IF t-outorder.gespende LT to-date THEN datum2 = t-outorder.gespende.
        ELSE datum2 = to-date. 
        i = datum1 - curr-date + 1. 
        FIND FIRST room-list WHERE room-list.zinr = t-outorder.zinr NO-ERROR.
        IF AVAILABLE room-list THEN 
        DO: 
            IF t-outorder.betriebsnr LE 1 THEN 
            DO datum = datum1 TO datum2: 
                 room-list.room[i] = "O-O-O". 
                 room-list.gstatus[i] = 9. 
                 room-list.recid1[i] = t-outorder.rec-id. 
                 i = i + 1. 
            END. 
            ELSE IF t-outorder.betriebsnr EQ 3 OR t-outorder.betriebsnr = 4 THEN 
            DO datum = datum1 TO datum2: 
                 room-list.room[i] = "O-O-S". 
                 room-list.gstatus[i] = 12. 
                 room-list.recid1[i] = t-outorder.rec-id. 
                 room-list.zistatus = 9. /*ITA*/
                 i = i + 1. 
            END. 
            ELSE IF t-outorder.betriebsnr = 2 THEN 
            DO datum = datum1 TO datum2: 
                IF room-list.recid1[i] = 0 THEN 
                DO: 
                    room-list.room[i] = " O-M ". 
                    room-list.gstatus[i] = 10. 
                    room-list.recid1[i] = t-outorder.rec-id. 
                END. 
                i = i + 1. 
            END. 
        END.
    END.
END PROCEDURE.


