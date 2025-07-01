DEF INPUT  PARAMETER datum      AS DATE              NO-UNDO.
DEF INPUT  PARAMETER rmType     AS CHAR              NO-UNDO.
DEF INPUT  PARAMETER global-occ AS LOGICAL           NO-UNDO.
DEF OUTPUT PARAMETER occ-rooms  AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR use-it                  AS LOGICAL           NO-UNDO.
DEF VAR ci-date                 AS DATE              NO-UNDO.
DEF VAR tot-occ-rooms           AS INTEGER           NO-UNDO.
DEF VAR rmcat-rooms             AS INTEGER           NO-UNDO INIT 0.
DEF VAR total-rooms             AS INTEGER           NO-UNDO INIT 0.
DEF VAR occ-rooms-1             AS INTEGER           NO-UNDO INIT 0.
DEF VAR i-method                AS INTEGER           NO-UNDO INIT 0.
DEF VAR d-occupancy             AS DECIMAL           NO-UNDO.
DEF VAR calc-rm                 AS LOGICAL           NO-UNDO.

/* SY 21/09/2014: global-occ & code enhancement */

FIND FIRST res-line WHERE res-line.active-flag LE 1
    AND res-line.resstatus LE 6 
    AND res-line.resstatus NE 3 
    AND res-line.resstatus NE 4 
    AND NOT res-line.ankunft GT datum
    AND NOT res-line.abreise LE datum NO-LOCK NO-ERROR.
IF NOT AVAILABLE res-line THEN RETURN.

RUN htpdate.p(87, OUTPUT ci-date).
FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmType NO-LOCK NO-ERROR.

FIND FIRST htparam WHERE htparam.paramnr = 439 NO-LOCK.
IF htparam.feldtyp = 1 AND htparam.finteger LE 2 THEN
    ASSIGN i-method = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 459 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN calc-rm = htparam.flogical.


IF calc-rm = NO THEN DO:
    IF i-method = 0 THEN RUN cal-method0.
    ELSE IF i-method = 1 THEN 
    DO:    
      RUN cal-method1.
      occ-rooms = occ-rooms-1.
    END.
    ELSE IF i-method = 2 THEN
    DO:
      RUN cal-method0.
      RUN cal-method1.
      IF occ-rooms-1 GT occ-rooms THEN occ-rooms = occ-rooms-1.
    END.
END.
ELSE IF calc-rm = YES THEN DO:
      RUN cal-method2.
      occ-rooms = occ-rooms-1.
END.

PROCEDURE cal-method0:
  IF zimkateg.typ NE 0 THEN
  DO:
      RUN cal-method0A.
      RETURN.
  END.
  IF datum GE ci-date THEN
  DO:
    FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 
        AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.zikatnr EQ zimkateg.zikatnr
        AND res-line.ankunft LE datum
        AND res-line.abreise GE datum NO-LOCK:
        use-it = YES.
        IF res-line.ankunft = res-line.abreise THEN use-it = (res-line.zipreis GT 0).
        IF res-line.abreise GT res-line.ankunft AND res-line.abreise = datum 
          THEN use-it = NO.
        IF use-it AND res-line.zinr NE "" THEN
        DO:
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN use-it = NO.
        END.
        IF use-it THEN occ-rooms = occ-rooms + res-line.zimmeranz.      
    END.
  END.
  ELSE
  DO:
    FOR EACH genstat WHERE genstat.datum = datum
        AND genstat.zinr NE ""
        AND genstat.resstatus = 6
        AND genstat.res-logic[2] EQ YES
        AND genstat.zikatnr = zimkateg.zikatnr NO-LOCK:
        occ-rooms = occ-rooms + 1.
    END.
  END.
END.

PROCEDURE cal-method0A:
DEF BUFFER zkbuff FOR zimkateg.
  IF datum GE ci-date THEN
  DO:
    FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 
        AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.ankunft LE datum
        AND res-line.abreise GE datum NO-LOCK:
        FIND FIRST zkbuff WHERE zkbuff.zikatnr = res-line.zikatnr
            NO-LOCK.
        use-it = (zkbuff.typ = zimkateg.typ).
        
        IF use-it THEN
        DO:
          IF res-line.ankunft = res-line.abreise THEN use-it = (res-line.zipreis GT 0).
          IF res-line.abreise GT res-line.ankunft AND res-line.abreise = datum 
            THEN use-it = NO.
        END.
        IF use-it AND res-line.zinr NE "" THEN
        DO:
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN use-it = NO.
        END.
        IF use-it THEN occ-rooms = occ-rooms + res-line.zimmeranz.      
    END.
  END.
  ELSE
  DO:
    FOR EACH genstat WHERE genstat.datum = datum
        AND genstat.zinr NE ""
        AND genstat.resstatus = 6
        AND genstat.res-logic[2] EQ YES NO-LOCK:
        FIND FIRST zkbuff WHERE zkbuff.zikatnr = genstat.zikatnr
            NO-LOCK.
        IF zkbuff.typ = zimkateg.typ THEN occ-rooms = occ-rooms + 1.
    END.
  END.
END.

PROCEDURE cal-method1:
DEF BUFFER zkbuff FOR zimkateg.
  IF AVAILABLE zimkateg AND zimkateg.typ NE 0 THEN
  DO:
      RUN cal-method1A.
      RETURN.
  END.
  IF datum GE ci-date THEN
  DO:
    FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK:
        FIND FIRST zkbuff WHERE zkbuff.zikatnr = zimmer.zikatnr NO-LOCK.
        total-rooms = total-rooms + 1.
        IF zkbuff.kurzbez = rmType THEN rmcat-rooms = rmcat-rooms + 1.
    END.
    FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 
        AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.ankunft LE datum
        AND res-line.abreise GE datum NO-LOCK:
        use-it = YES.
        IF res-line.ankunft = res-line.abreise THEN use-it = (res-line.zipreis GT 0).
        IF res-line.abreise GT res-line.ankunft AND res-line.abreise = datum 
          THEN use-it = NO.
        IF use-it AND res-line.zinr NE "" THEN
        DO:
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN use-it = NO.
        END.
        IF use-it THEN tot-occ-rooms = tot-occ-rooms + res-line.zimmeranz.      
    END.
    IF global-occ THEN occ-rooms-1 = tot-occ-rooms.
    ELSE
    occ-rooms-1 = ROUND(tot-occ-rooms * rmcat-rooms / total-rooms, 0).
    /*
    DISP i-method rmtype total-rooms rmcat-rooms tot-occ-rooms occ-rooms-1 occ-rooms.
    PAUSE NO-MESSAGE.
    */
  END.
  ELSE
  DO:
    FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
      total-rooms = total-rooms + zkstat.anz100.
      IF AVAILABLE zimkateg 
        AND zkstat.zikatnr = zimkateg.zikatnr THEN 
        rmcat-rooms = rmcat-rooms + zkstat.anz100.
    END.
    FOR EACH genstat WHERE genstat.datum = datum
        AND genstat.zinr NE ""
        AND genstat.resstatus = 6
        AND genstat.res-logic[2] EQ YES NO-LOCK:
        tot-occ-rooms = tot-occ-rooms + 1.
    END.
    IF global-occ THEN occ-rooms-1 = tot-occ-rooms.
    ELSE
    occ-rooms-1 = ROUND(tot-occ-rooms * rmcat-rooms / total-rooms, 0).
  END.
END.

PROCEDURE cal-method1A:
DEF BUFFER zkbuff FOR zimkateg.
  IF datum GE ci-date THEN
  DO:
    FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK:
        FIND FIRST zkbuff WHERE zkbuff.zikatnr = zimmer.zikatnr NO-LOCK.
        total-rooms = total-rooms + 1.
        IF zkbuff.typ = zimkateg.typ THEN rmcat-rooms = rmcat-rooms + 1.
    END.
    FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 
        AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.ankunft LE datum
        AND res-line.abreise GE datum NO-LOCK:
        use-it = YES.
        IF res-line.ankunft = res-line.abreise THEN use-it = (res-line.zipreis GT 0).
        IF res-line.abreise GT res-line.ankunft AND res-line.abreise = datum 
          THEN use-it = NO.
        IF use-it AND res-line.zinr NE "" THEN
        DO:
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN use-it = NO.
        END.
        IF use-it THEN tot-occ-rooms = tot-occ-rooms + res-line.zimmeranz.      
    END.
    IF global-occ THEN occ-rooms-1 = tot-occ-rooms.
    ELSE
    occ-rooms-1 = ROUND(tot-occ-rooms * rmcat-rooms / total-rooms, 0).
    /*
    DISP i-method rmtype total-rooms rmcat-rooms tot-occ-rooms occ-rooms-1 occ-rooms.
    PAUSE NO-MESSAGE.
    */
  END.
  ELSE
  DO:
    FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
      total-rooms = total-rooms + zkstat.anz100.
      FIND FIRST zkbuff WHERE zkbuff.zikatnr = zkstat.zikatnr NO-LOCK.
      IF zkbuff.typ = zimkateg.typ THEN 
        rmcat-rooms = rmcat-rooms + zkstat.anz100.
    END.
    FOR EACH genstat WHERE genstat.datum = datum
        AND genstat.zinr NE ""
        AND genstat.resstatus = 6
        AND genstat.res-logic[2] EQ YES NO-LOCK:
        tot-occ-rooms = tot-occ-rooms + 1.
    END.
    IF global-occ THEN occ-rooms-1 = tot-occ-rooms.
    ELSE
    occ-rooms-1 = ROUND(tot-occ-rooms * rmcat-rooms / total-rooms, 0).
  END.
END.


PROCEDURE cal-method2:
DEF BUFFER zkbuff FOR zimkateg.   
    
  IF AVAILABLE zimkateg AND zimkateg.typ NE 0 THEN
  DO:
      RUN cal-method2A.
      RETURN.
  END.
  IF datum GE ci-date THEN
  DO:
    FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK:
        FIND FIRST zkbuff WHERE zkbuff.zikatnr = zimmer.zikatnr NO-LOCK.
        total-rooms = total-rooms + 1.
        IF zkbuff.typ = zimkateg.typ THEN rmcat-rooms = rmcat-rooms + 1.
    END.
    FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 
        AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.ankunft LE datum
        AND res-line.abreise GE datum NO-LOCK:
        use-it = YES.
        IF res-line.ankunft = res-line.abreise THEN use-it = (res-line.zipreis GT 0).
        IF res-line.abreise GT res-line.ankunft AND res-line.abreise = datum 
          THEN use-it = NO.
        IF use-it AND res-line.zinr NE "" THEN
        DO:
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF AVAILABLE zimmer THEN DO:
              IF NOT zimmer.sleeping THEN use-it = NO.
              ELSE DO:
                  FIND FIRST zkbuff WHERE zkbuff.zikatnr = zimmer.zikatnr NO-LOCK.
                  IF zkbuff.typ = zimkateg.typ THEN use-it = YES.   
                  ELSE use-it = NO.
              END.
          END.              
        END.
        IF use-it THEN tot-occ-rooms = tot-occ-rooms + res-line.zimmeranz.      
    END.
    ASSIGN occ-rooms-1 = tot-occ-rooms.
    /*IF global-occ THEN occ-rooms-1 = tot-occ-rooms.
    ELSE 
    occ-rooms-1 = ROUND(tot-occ-rooms * rmcat-rooms / total-rooms, 0).*/
  END.
  ELSE
  DO:
    FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
      total-rooms = total-rooms + zkstat.anz100.
      IF zkbuff.typ = zimkateg.typ THEN 
        rmcat-rooms = rmcat-rooms + zkstat.anz100.
    END.
    FOR EACH genstat WHERE genstat.datum = datum
        AND genstat.zinr NE ""
        AND genstat.resstatus = 6
        AND genstat.res-logic[2] EQ YES NO-LOCK:
        FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN DO:
              IF NOT zimmer.sleeping THEN use-it = NO.
              ELSE DO:
                  FIND FIRST zkbuff WHERE zkbuff.zikatnr = zimmer.zikatnr NO-LOCK.
                  IF zkbuff.typ = zimkateg.typ THEN use-it = YES. 
                  ELSE use-it = NO.
              END.
        END.
        IF use-it THEN ASSIGN tot-occ-rooms = tot-occ-rooms + 1.
    END.
    ASSIGN occ-rooms-1 = tot-occ-rooms.
    /*IF global-occ THEN occ-rooms-1 = tot-occ-rooms.
    ELSE 
    occ-rooms-1 = ROUND(tot-occ-rooms * rmcat-rooms / total-rooms, 0).*/
  END.
END.

PROCEDURE cal-method2A:
DEF BUFFER zkbuff FOR zimkateg.
  IF datum GE ci-date THEN
  DO:
    FOR EACH zimmer WHERE zimmer.sleeping NO-LOCK:
        FIND FIRST zkbuff WHERE zkbuff.zikatnr = zimmer.zikatnr NO-LOCK.
        total-rooms = total-rooms + 1.
        IF zkbuff.typ = zimkateg.typ THEN rmcat-rooms = rmcat-rooms + 1.
    END.
    FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 
        AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.ankunft LE datum
        AND res-line.abreise GE datum NO-LOCK BY res-line.zinr:
        use-it = YES.
        IF res-line.ankunft = res-line.abreise THEN use-it = (res-line.zipreis GT 0).
        IF res-line.abreise GT res-line.ankunft AND res-line.abreise = datum 
          THEN use-it = NO.
        IF use-it AND res-line.zinr NE "" THEN
        DO:
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF AVAILABLE zimmer THEN DO:
              IF NOT zimmer.sleeping THEN use-it = NO.
              ELSE DO:
                  FIND FIRST zkbuff WHERE zkbuff.zikatnr = zimmer.zikatnr NO-LOCK.
                  IF zkbuff.typ = zimkateg.typ THEN use-it = YES. 
                  ELSE use-it = NO.
              END.
          END.
        END.
        IF use-it THEN tot-occ-rooms = tot-occ-rooms + res-line.zimmeranz. 
    END.
    ASSIGN occ-rooms-1 = tot-occ-rooms.
    /*IF global-occ THEN occ-rooms-1 = tot-occ-rooms.
    ELSE
    occ-rooms-1 = ROUND(tot-occ-rooms * rmcat-rooms / total-rooms, 0).*/
  END.
  ELSE
  DO:
    FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
      total-rooms = total-rooms + zkstat.anz100.
      FIND FIRST zkbuff WHERE zkbuff.zikatnr = zkstat.zikatnr NO-LOCK.
      IF zkbuff.typ = zimkateg.typ THEN 
        rmcat-rooms = rmcat-rooms + zkstat.anz100.
    END.
    FOR EACH genstat WHERE genstat.datum = datum
        AND genstat.zinr NE ""
        AND genstat.resstatus = 6
        AND genstat.res-logic[2] EQ YES NO-LOCK:
        FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK NO-ERROR.
        IF AVAILABLE zimmer THEN DO:
              IF NOT zimmer.sleeping THEN use-it = NO.
              ELSE DO:
                  FIND FIRST zkbuff WHERE zkbuff.zikatnr = zimmer.zikatnr NO-LOCK.
                  IF zkbuff.typ = zimkateg.typ THEN use-it = YES. 
                  ELSE use-it = NO.
              END.
        END.
        IF use-it THEN ASSIGN tot-occ-rooms = tot-occ-rooms + 1.
    END.
    ASSIGN occ-rooms-1 = tot-occ-rooms.
    /*IF global-occ THEN occ-rooms-1 = tot-occ-rooms.
    ELSE
    occ-rooms-1 = ROUND(tot-occ-rooms * rmcat-rooms / total-rooms, 0).*/
  END.
END.
