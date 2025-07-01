DEFINE TEMP-TABLE room-list 
  FIELD flag       AS INTEGER 
  FIELD build      AS CHAR FORMAT "x(40)" 
  FIELD build-flag AS CHAR FORMAT "x(1)"  LABEL "P" 
  FIELD zistatus   AS INTEGER 
  FIELD infochar   AS CHAR FORMAT "x(2)"  LABEL "    " 
  FIELD inactive   AS CHAR FORMAT "x(1)" LABEL "I" FGCOLOR 12 
  FIELD zinr       LIKE zimmer.zinr LABEL "RmNo" 
  FIELD bezeich    AS CHAR FORMAT "x(12)" LABEL "ShortDescript" 
  FIELD zikatnr    AS INTEGER FORMAT "999" 
  FIELD rmcat      AS CHAR FORMAT "x(6)"  LABEL "RmCat" 
  FIELD etage      AS INTEGER FORMAT ">9" LABEL "FL" 
  FIELD outlook    AS CHAR FORMAT "x(14)" LABEL "Overlook" 
  FIELD setup      AS CHAR FORMAT "x(14)" LABEL "BedSetup" 
  FIELD verbindung AS CHAR EXTENT 2 FORMAT "x(6)" 
                      LABEL "Connecting", "Connecting" 
  FIELD infonum    AS INTEGER FORMAT "9" INITIAL 3 
  FIELD recid1     AS INTEGER INITIAL 0 
  FIELD recid2     AS INTEGER INITIAL 0
  FIELD infostr    AS CHAR

. 

DEFINE INPUT PARAMETER mi-clean     AS LOGICAL.
DEFINE INPUT PARAMETER mi-clean1    AS LOGICAL.
DEFINE INPUT PARAMETER mi-dirty     AS LOGICAL.
DEFINE INPUT PARAMETER mi-depart    AS LOGICAL.
DEFINE INPUT PARAMETER mi-occ       AS LOGICAL.
DEFINE INPUT PARAMETER mi-ooo       AS LOGICAL.
DEFINE INPUT PARAMETER mi-off       AS LOGICAL.
DEFINE INPUT PARAMETER ankunft      AS DATE.
DEFINE INPUT PARAMETER abreise      AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.

DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE zikatnr AS INTEGER NO-UNDO INIT 0. /*FT serverless*/
 
  FOR EACH room-list: 
    delete room-list. 
  END. 
 
  FOR EACH zimmer BY zimmer.zinr: 
    do-it = NO. 
    IF zikatnr = 0 OR zimmer.zikatnr = zikatnr THEN do-it = YES. 
    IF do-it THEN 
    DO: 
      IF zimmer.zistatus EQ 0 AND mi-clean = NO 
        THEN do-it = NO. 
      IF zimmer.zistatus EQ 1 AND mi-clean1 = NO 
        THEN do-it = NO. 
      IF zimmer.zistatus EQ 2 AND mi-dirty = NO 
        THEN do-it = NO. 
      IF zimmer.zistatus EQ 3 AND mi-depart = NO 
        THEN do-it = NO. 
      IF zimmer.zistatus EQ 4 OR zimmer.zistatus EQ 5 OR zimmer.zistatus = 8 
        AND mi-occ = NO THEN do-it = NO. 
      IF zimmer.zistatus EQ 6 AND mi-ooo = NO 
        THEN do-it = NO. 
      IF zimmer.zistatus EQ 7 AND mi-off = NO 
        THEN do-it = NO. 
    END. 
 
    IF do-it THEN 
    DO: 
      FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
         AND ( (outorder.gespstart LT ankunft AND outorder.gespende GT ankunft) 
            OR (outorder.gespstart LT abreise AND outorder.gespende GT abreise) 
            OR (outorder.gespstart GE ankunft AND outorder.gespstart LE abreise) 
            OR (outorder.gespende GE ankunft AND outorder.gespende LE abreise)) NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE outorder THEN 
      DO: 
        FIND FIRST res-line WHERE res-line.active-flag LE 1 
          AND res-line.resstatus NE 12 AND res-line.zinr = zimmer.zinr 
          AND NOT res-line.ankunft GE abreise 
          AND NOT res-line.abreise LE ankunft NO-LOCK NO-ERROR. 
/* 
        FIND FIRST zimplan WHERE zimplan.zinr = zimmer.zinr 
          AND zimplan.datum GE ankunft AND zimplan.datum LT abreise 
          NO-LOCK NO-ERROR. 
*/ 
        IF NOT AVAILABLE /*zimplan*/ res-line THEN 
        DO: 
          create room-list. 
          room-list.zinr = zimmer.zinr. 
          IF NOT zimmer.sleeping THEN room-list.inactive = "I". 
        END. 
        ELSE 
        DO: 
          create room-list. 
          room-list.zinr = zimmer.zinr. 
          IF zimmer.zistatus = 8 THEN room-list.flag = 4. 
          ELSE 
          DO: 
            IF res-line.active-flag = 0 THEN room-list.flag = 4. 
            ELSE room-list.flag = zimmer.zistatus. 
          END. 
          IF NOT zimmer.sleeping THEN room-list.inactive = "I". 
        END. 
      END. 
      ELSE 
      DO: 
        create room-list. 
        room-list.zinr = zimmer.zinr. 
        IF outorder.betriebsnr GE 2 THEN room-list.flag = 7. 
        ELSE room-list.flag = 6. 
        IF NOT zimmer.sleeping THEN room-list.inactive = "I". 
      END. 
    END. 
  END. 
 
  FOR EACH room-list: 
    FIND FIRST zimmer WHERE zimmer.zinr = room-list.zinr NO-LOCK. 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    IF zimmer.build NE "" THEN 
    DO: 
      room-list.build = zimmer.build. 
      room-list.build-flag = "*". 
    END. 
    room-list.bezeich = zimmer.kbezeich. 
    room-list.verbindung[1] = zimmer.verbindung[1]. 
    room-list.verbindung[2] = zimmer.verbindung[2]. 
    room-list.etage = zimmer.etage. 
    room-list.rmcat = zimkateg.kurzbez. 
    room-list.zikatnr = zimkateg.zikatnr. 
 
/*  room outlooks */ 
    IF zimmer.typ NE 0 THEN 
    DO: 
      FIND FIRST paramtext WHERE paramtext.txtnr = 230 
        AND paramtext.sprachcode = zimmer.typ NO-LOCK NO-ERROR. 
      IF AVAILABLE paramtext THEN room-list.outlook = paramtext.ptexte. 
    END. 
 
/* room setup */ 
    IF zimmer.setup NE 0 THEN 
    DO: 
      FIND FIRST paramtext WHERE 
         paramtext.txtnr = (zimmer.setup + 9200) NO-LOCK NO-ERROR. 
      IF AVAILABLE paramtext THEN room-list.setup = paramtext.ptexte. 
    END. 
 
    FIND FIRST zimplan WHERE zimplan.zinr = room-list.zinr 
      AND zimplan.datum = (ankunft - 1) NO-LOCK NO-ERROR. 
    IF AVAILABLE zimplan THEN 
    DO: 
     room-list.infonum = room-list.infonum - 2. 
      room-list.recid1 = zimplan.res-recid. 
    END. 
    FIND FIRST zimplan WHERE zimplan.zinr = room-list.zinr 
      AND zimplan.datum = abreise NO-LOCK NO-ERROR. 
    IF AVAILABLE zimplan THEN 
    DO: 
      room-list.infonum = room-list.infonum - 1. 
      room-list.recid2 = zimplan.res-recid. 
    END. 
    IF room-list.infonum = 0 THEN room-list.infochar = "<>". 
    ELSE IF room-list.infonum = 1 THEN room-list.infochar = "< ". 
    ELSE IF room-list.infonum = 2 THEN room-list.infochar = " >". 
    IF zimmer.zistatus = 8 THEN room-list.zistat = 5. 
    ELSE room-list.zistat = zimmer.zistatus + 1. 
    IF room-list.flag = 7 THEN room-list.zistat = 8. 
  END. 

  FOR EACH room-list:
    IF SUBSTR(room-list.infochar,1,1) = "<" THEN 
    DO: 
      FIND FIRST res-line 
        WHERE RECID(res-line) = room-list.recid1 NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay NO-LOCK.
        ASSIGN
          room-list.infostr = room-list.infostr 
                  + "<  ResNo:  " 
                  + STRING(res-line.resnr) + CHR(10)
          room-list.infostr = room-list.infostr + "    " + guest.name + ", " 
                  + guest.vorname1 + guest.anredefirma + CHR(10) 
          room-list.infostr = room-list.infostr + "Arrival : " + STRING(res-line.ankunft) 
                  + CHR(10) 
          room-list.infostr = room-list.infostr + "Depart : " + STRING(res-line.abreise) 
                          + CHR(10) + CHR(10)
        . 
      END. 
    END. 
    IF SUBSTR(room-list.infochar,2,1) = ">" THEN 
    DO: 
      FIND FIRST res-line 
        WHERE RECID(res-line) = room-list.recid2 NO-LOCK NO-ERROR. 
      IF AVAILABLE res-line THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay NO-LOCK. 
        ASSIGN
          room-list.infostr = room-list.infostr 
                  + ">  ResNo:  " 
                  + STRING(res-line.resnr) + CHR(10)
          room-list.infostr = room-list.infostr + "    " + guest.name + ", " 
                  + guest.vorname1 + guest.anredefirma + CHR(10) 
          room-list.infostr = room-list.infostr + "Arrival : " + STRING(res-line.ankunft) + CHR(10) 
          room-list.infostr = room-list.infostr + "Depart : " + STRING(res-line.abreise)
        . 
      END. 
    END. 
    IF room-list.zistatus = 7 THEN 
    DO: 
      FIND FIRST outorder WHERE outorder.zinr = room-list.zinr NO-LOCK NO-ERROR. 
      IF AVAILABLE outorder THEN 
      DO: 
        IF room-list.infostr NE "" THEN room-list.infostr = room-list.infostr + CHR(10). 
        room-list.infostr = room-list.infostr + outorder.gespgrund. 
      END. 
    END. 
    IF room-list.zistatus = 8 THEN 
    DO: 
      FIND FIRST outorder WHERE outorder.zinr = room-list.zinr NO-LOCK NO-ERROR. 
      IF AVAILABLE outorder THEN 
      DO: 
        IF room-list.infostr NE "" THEN room-list.infostr = room-list.infostr + CHR(10). 
        room-list.infostr = room-list.infostr + outorder.gespgrund. 
      END. 
    END. 
  END.
