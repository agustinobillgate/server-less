DEFINE TEMP-TABLE rml 
  FIELD nr          AS INTEGER 
  FIELD raum        AS CHAR 
  FIELD bezeich     AS CHAR FORMAT "x(32)" LABEL "Room" FONT 1 
  FIELD departement AS INTEGER
  FIELD resnr       AS INTEGER EXTENT 48 
  FIELD reslinnr    AS INTEGER EXTENT 48 
  FIELD gstatus     AS INTEGER EXTENT 48 
  FIELD room        AS CHAR    EXTENT 48 FORMAT "x(1)" FONT 1
  FIELD blocked     AS INTEGER EXTENT 48
. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR rml.
DEF INPUT PARAMETER from-date AS DATE.


DEFINE VARIABLE gastname AS CHAR NO-UNDO.
DEFINE BUFFER rmBuff  FOR bk-raum.
DEFINE BUFFER childRM FOR bk-raum.
DEFINE BUFFER gast    FOR guest. 

FOR EACH bk-reser WHERE (bk-reser.datum GE from-date
    AND bk-reser.datum LE from-date + 11)
    AND (bk-reser.resstatus EQ 8 OR bk-reser.resstatus LE 2) NO-LOCK, 
    FIRST bk-veran WHERE bk-veran.veran-nr = bk-reser.veran-nr NO-LOCK, 
    FIRST gast WHERE gast.gastnr = bk-veran.gastnr NO-LOCK:

    /*ITA 020415*/
    IF AVAILABLE gast THEN ASSIGN gastname = gast.NAME.
    ELSE ASSIGN gastname = "Please re-attach guest.".

    RUN create-wlist1(bk-reser.raum, bk-reser.raum).

    FIND FIRST childRM WHERE childRM.raum = bk-reser.raum NO-LOCK.
    FOR EACH rmBuff WHERE rmBuff.raum = childRM.lu-raum NO-LOCK:
      RUN create-wlist2(bk-reser.raum, rmBuff.raum).
    END.

END. 

PROCEDURE create-wlist1:
DEFINE INPUT PARAMETER parent-rm AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER curr-rm   AS CHAR NO-UNDO.
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE j           AS INTEGER. 
DEFINE VARIABLE k           AS INTEGER. 
DEFINE VARIABLE l           AS INTEGER. 
DEFINE VARIABLE from-time   AS INTEGER. 
DEFINE VARIABLE to-time     AS INTEGER. 
DEFINE BUFFER bk-buff  FOR bk-reser.
DEFINE BUFFER rmBuff   FOR bk-raum.

    FIND FIRST rml WHERE rml.raum = curr-rm 
    AND rml.nr = bk-reser.resstatus.

    j = bk-reser.datum - from-date. 
    k = bk-reser.bis-datum - from-date. 
    IF bk-reser.von-i LT 13 THEN 
    DO: 
      from-time = (j * 4) + 1. 
    END. 
    ELSE IF bk-reser.von-i LT 25 THEN 
    DO: 
      from-time = (j * 4) + 2. 
    END. 
    ELSE IF bk-reser.von-i LT 37 THEN 
    DO: 
      from-time = (j * 4) + 3.          
    END. 
    ELSE IF bk-reser.von-i LT 49 THEN 
    DO: 
      from-time = (j * 4) + 4. 
    END. 
    IF bk-reser.datum = bk-reser.bis-datum THEN 
    DO: 
      IF bk-reser.bis-i LT 13 THEN 
      DO: 
        to-time = (j * 4) + 1. 
      END. 
      ELSE IF bk-reser.bis-i LT 25 THEN 
      DO: 
        to-time = (j * 4) + 2. 
      END. 
      ELSE IF bk-reser.bis-i LT 37 THEN 
      DO: 
        to-time = (j * 4) + 3. 
      END. 
      ELSE IF bk-reser.bis-i LT 49 THEN 
      DO: 
        to-time = (j * 4) + 4. 
      END. 
    END. 
    ELSE IF bk-reser.bis-datum GT bk-reser.datum THEN 
    DO: 
      IF bk-reser.bis-i LT 13 THEN 
      DO: 
        to-time = (k * 4) + 1. 
      END. 
      ELSE IF bk-reser.bis-i LT 25 THEN 
      DO: 
        to-time = (k * 4) + 2. 
      END. 
      ELSE IF bk-reser.bis-i LT 37 THEN 
      DO: 
        to-time = (k * 4) + 3. 
      END. 
      ELSE IF bk-reser.bis-i LT 49 THEN 
      DO: 
        to-time = (k * 4) + 4. 
      END. 
    END. 
    l = 1. 
    DO i = from-time TO to-time: 
      rml.gstatus[i] = bk-reser.resstatus. 
      IF bk-reser.resstatus = 2 THEN
      DO:
          FIND FIRST bk-buff WHERE bk-buff.datum = bk-reser.datum 
              AND bk-buff.resstatus = 3 AND bk-buff.raum = bk-reser.raum NO-LOCK NO-ERROR.
          IF AVAILABLE bk-buff THEN
          DO:
              IF (i MOD 4 = 1) AND bk-buff.von-i LT 13 THEN
                  rml.gstatus[i] = -1.
              ELSE IF (i MOD 4 = 2) AND bk-buff.von-i LT 25 THEN
                  rml.gstatus[i] = -1.
              ELSE IF (i MOD 4 = 3) AND bk-buff.von-i LT 31 THEN
                  rml.gstatus[i] = -1.
              ELSE IF (i MOD 4 = 1) AND bk-buff.von-i LT 37 THEN
                  rml.gstatus[i] = -1.
          END.
      END.
      ASSIGN
        rml.room[i]     = SUBSTR(gastname, l, 1) 
        rml.resnr[i]    = bk-reser.veran-nr
        rml.reslinnr[i] = bk-reser.veran-resnr 
        l               = l + 1
      . 
      IF parent-rm NE curr-rm THEN rml.blocked[i] = 1.
    END.     

    FOR EACH rmBuff WHERE rmBuff.lu-raum = curr-rm NO-LOCK:
        RUN create-wlist1 (bk-reser.raum, rmBuff.raum).
    END.

END.


PROCEDURE create-wlist2:
DEFINE INPUT PARAMETER parent-rm AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER curr-rm   AS CHAR NO-UNDO.
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE j           AS INTEGER. 
DEFINE VARIABLE k           AS INTEGER. 
DEFINE VARIABLE l           AS INTEGER. 
DEFINE VARIABLE from-time   AS INTEGER. 
DEFINE VARIABLE to-time     AS INTEGER. 
DEFINE BUFFER bk-buff  FOR bk-reser.
DEFINE BUFFER rmBuff   FOR bk-raum.
DEFINE BUFFER childRm  FOR bk-raum.

    FIND FIRST rml WHERE rml.raum = curr-rm 
    AND rml.nr = bk-reser.resstatus.

    j = bk-reser.datum - from-date. 
    k = bk-reser.bis-datum - from-date. 
    IF bk-reser.von-i LT 13 THEN 
    DO: 
      from-time = (j * 4) + 1. 
    END. 
    ELSE IF bk-reser.von-i LT 25 THEN 
    DO: 
      from-time = (j * 4) + 2. 
    END. 
    ELSE IF bk-reser.von-i LT 37 THEN 
    DO: 
      from-time = (j * 4) + 3.          
    END. 
    ELSE IF bk-reser.von-i LT 49 THEN 
    DO: 
      from-time = (j * 4) + 4. 
    END. 
    IF bk-reser.datum = bk-reser.bis-datum THEN 
    DO: 
      IF bk-reser.bis-i LT 13 THEN 
      DO: 
        to-time = (j * 4) + 1. 
      END. 
      ELSE IF bk-reser.bis-i LT 25 THEN 
      DO: 
        to-time = (j * 4) + 2. 
      END. 
      ELSE IF bk-reser.bis-i LT 37 THEN 
      DO: 
        to-time = (j * 4) + 3. 
      END. 
      ELSE IF bk-reser.bis-i LT 49 THEN 
      DO: 
        to-time = (j * 4) + 4. 
      END. 
    END. 
    ELSE IF bk-reser.bis-datum GT bk-reser.datum THEN 
    DO: 
      IF bk-reser.bis-i LT 13 THEN 
      DO: 
        to-time = (k * 4) + 1. 
      END. 
      ELSE IF bk-reser.bis-i LT 25 THEN 
      DO: 
        to-time = (k * 4) + 2. 
      END. 
      ELSE IF bk-reser.bis-i LT 37 THEN 
      DO: 
        to-time = (k * 4) + 3. 
      END. 
      ELSE IF bk-reser.bis-i LT 49 THEN 
      DO: 
        to-time = (k * 4) + 4. 
      END. 
    END. 
    l = 1. 
    DO i = from-time TO to-time: 
        rml.gstatus[i] = bk-reser.resstatus. 
        IF bk-reser.resstatus = 2 THEN
        DO:
            FIND FIRST bk-buff WHERE bk-buff.datum = bk-reser.datum 
                AND bk-buff.resstatus = 3 AND bk-buff.raum = bk-reser.raum NO-LOCK NO-ERROR.
            IF AVAILABLE bk-buff THEN
            DO:
                IF (i MOD 4 = 1) AND bk-buff.von-i LT 13 THEN
                    rml.gstatus[i] = -1.
                ELSE IF (i MOD 4 = 2) AND bk-buff.von-i LT 25 THEN
                    rml.gstatus[i] = -1.
                ELSE IF (i MOD 4 = 3) AND bk-buff.von-i LT 31 THEN
                    rml.gstatus[i] = -1.
                ELSE IF (i MOD 4 = 1) AND bk-buff.von-i LT 37 THEN
                    rml.gstatus[i] = -1.
            END.
        END.
        ASSIGN
          rml.room[i]     = SUBSTR(gast.name, l, 1) 
          rml.resnr[i]    = bk-reser.veran-nr
          rml.reslinnr[i] = bk-reser.veran-resnr 
          l               = l + 1
        . 
        IF parent-rm NE curr-rm THEN rml.blocked[i] = 1.
    END.     

    FIND FIRST childRM WHERE childRM.raum = curr-rm NO-LOCK.
    FOR EACH rmBuff WHERE rmBuff.raum = childRM.lu-raum NO-LOCK:
        RUN create-wlist2 (bk-reser.raum, rmBuff.raum).
    END.

END.

