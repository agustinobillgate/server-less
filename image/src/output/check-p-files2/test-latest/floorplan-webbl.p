
DEFINE TEMP-TABLE florplan-list
  FIELD char1       LIKE queasy.char1
  FIELD deci1       LIKE queasy.deci1
  FIELD deci2       LIKE queasy.deci2
  FIELD curr-n      AS INT
  FIELD bcol        AS INT
  FIELD fcol        AS INT
  FIELD zistatus    AS INT
  FIELD g-info      AS CHARACTER
  FIELD r-info      AS CHARACTER.
DEFINE TEMP-TABLE gstat-list 
  FIELD SELECTED AS LOGICAL INITIAL NO 
  FIELD resstatus AS INTEGER           
  FIELD bezeich  AS CHAR FORMAT "x(24)". 
DEFINE TEMP-TABLE zikat-list 
  FIELD SELECTED AS LOGICAL INITIAL NO 
  FIELD zikatnr  AS INTEGER 
  FIELD kurzbez  AS CHAR 
  FIELD bezeich  AS CHAR FORMAT "x(24)".
DEFINE TEMP-TABLE zistat-list 
  FIELD SELECTED AS LOGICAL INITIAL NO 
  FIELD zistatus AS INTEGER 
  FIELD bezeich  AS CHAR FORMAT "x(24)". 
DEFINE TEMP-TABLE t-zimmer      LIKE zimmer.
DEFINE TEMP-TABLE t-res-line    LIKE res-line.
DEFINE TEMP-TABLE t-reservation LIKE reservation.
DEFINE TEMP-TABLE t-waehrung    LIKE waehrung.
DEFINE TEMP-TABLE t-outorder    LIKE outorder.
 
DEFINE INPUT PARAMETER TABLE FOR gstat-list.
DEFINE INPUT PARAMETER TABLE FOR zikat-list.
DEFINE INPUT PARAMETER TABLE FOR zistat-list.
DEFINE INPUT PARAMETER location     AS INTEGER.
DEFINE INPUT PARAMETER floor        AS INTEGER.
DEFINE INPUT PARAMETER all-gstat    AS LOGICAL.
DEFINE INPUT PARAMETER all-zikat    AS LOGICAL.
DEFINE INPUT PARAMETER all-zistat   AS LOGICAL.
DEFINE INPUT PARAMETER ci-date      AS DATE.
DEFINE INPUT PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR florplan-list.
{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-rzinr".
DEF VAR do-it       AS LOGICAL.
DEF VAR curr-n      AS INTEGER.
DEF VAR zistatus    AS INTEGER.
DEF VAR bcol        AS INTEGER.
DEF VAR fcol        AS INTEGER.
DEF VAR g-info      AS CHAR.
DEF VAR r-info      AS CHAR.
DEFINE VARIABLE n-edit AS CHAR.
DEFINE VARIABLE c-edit AS CHAR.
DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE item-fgcol AS INTEGER EXTENT 15 INITIAL 
  [15,15,15,15,15,15,15,0,15,0,0,15,0,0,0] NO-UNDO. 
DEFINE BUFFER gtbuff FOR gstat-list. 
DEFINE BUFFER zkbuff FOR zikat-list. 
DEFINE BUFFER stbuff FOR zistat-list. 

FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
IF finteger NE 0 THEN vipnr1 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
IF finteger NE 0 THEN vipnr2 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
IF finteger NE 0 THEN vipnr3 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
IF finteger NE 0 THEN vipnr4 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
IF finteger NE 0 THEN vipnr5 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
IF finteger NE 0 THEN vipnr6 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
IF finteger NE 0 THEN vipnr7 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
IF finteger NE 0 THEN vipnr8 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
IF finteger NE 0 THEN vipnr9 = htparam.finteger. 
FOR EACH queasy WHERE queasy.key = 25 
    AND queasy.number1 = location AND queasy.number2 = floor 
    NO-LOCK BY queasy.char1: 
    FIND FIRST zimmer WHERE zimmer.zinr = queasy.char1 NO-LOCK NO-ERROR. 
    do-it = YES.
    curr-n = curr-n + 1.
    IF NOT AVAILABLE zimmer THEN do-it = NO. 
    ELSE 
    DO: 
      IF NOT all-gstat THEN 
      DO: 
         do-it = NO. 
         FOR EACH res-line WHERE res-line.active-flag LE 1 
           AND res-line.zinr = zimmer.zinr AND res-line.ankunft LE ci-date 
           AND res-line.resstatus NE 12 AND res-line.abreise GE ci-date NO-LOCK: 
           IF res-line.active-flag = 0 AND res-line.ankunft = ci-date THEN 
           DO: 
             FIND FIRST gtbuff WHERE gtbuff.SELECTED AND gtbuff.resstatus = 0 
                 NO-LOCK NO-ERROR. 
             IF AVAILABLE gtbuff THEN do-it = YES. 
           END. 
           ELSE IF res-line.active-flag = 1 AND res-line.abreise > ci-date THEN 
           DO: 
             FIND FIRST gtbuff WHERE gtbuff.SELECTED AND gtbuff.resstatus = 1 
                 NO-LOCK NO-ERROR. 
             IF AVAILABLE gtbuff THEN do-it = YES. 
           END. 
           ELSE IF res-line.active-flag = 1 AND res-line.abreise = ci-date THEN 
           DO: 
             FIND FIRST gtbuff WHERE gtbuff.SELECTED AND gtbuff.resstatus = 2 
                 NO-LOCK NO-ERROR. 
             IF AVAILABLE gtbuff THEN do-it = YES. 
           END. 
         END. 
      END.
      IF do-it AND NOT all-zikat THEN 
      DO: 
          FIND FIRST zkbuff WHERE zkbuff.SELECTED AND zkbuff.zikatnr 
              = zimmer.zikatnr NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE zkbuff THEN do-it = NO. 
      END. 
      IF do-it AND NOT all-zistat THEN 
      DO: 
          FIND FIRST stbuff WHERE stbuff.SELECTED AND stbuff.zistatus = 
              zimmer.zistatus NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE stbuff THEN do-it = NO. 
      END. 
 
      IF do-it THEN 
      DO:
        CREATE florplan-list.
        ASSIGN
            florplan-list.char1    = queasy.char1
            florplan-list.deci1    = queasy.deci1
            florplan-list.deci2    = queasy.deci2
            florplan-list.curr-n   = curr-n.
            
      END. 
    END. 
 
    IF AVAILABLE zimmer AND do-it THEN 
    DO: 
      
        ASSIGN florplan-list.zistatus = zimmer.zistatus.
            
        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
          AND outorder.gespstart LE ci-date 
          AND outorder.gespende  GE ci-date NO-LOCK NO-ERROR. 
        IF AVAILABLE outorder THEN 
        DO: 
          IF outorder.betriebsnr = 2 THEN florplan-list.zistatus = 7. 
          ELSE IF outorder.betriebsnr = 3 OR outorder.betriebsnr = 4 
          THEN florplan-list.zistatus = 9.  
        END. 
        
        IF florplan-list.zistatus = 0 THEN florplan-list.bcol = 8. 
        ELSE IF florplan-list.zistatus = 1 THEN florplan-list.bcol = 11. 
        ELSE IF florplan-list.zistatus = 2 THEN florplan-list.bcol =  2. 
        ELSE IF florplan-list.zistatus = 3 THEN florplan-list.bcol =  1. 
        ELSE IF florplan-list.zistatus = 4 THEN florplan-list.bcol = 14. 
        ELSE IF florplan-list.zistatus = 5 THEN florplan-list.bcol = 15. 
        ELSE IF florplan-list.zistatus = 6 THEN florplan-list.bcol = 12. 
        ELSE IF florplan-list.zistatus = 7 THEN florplan-list.bcol =  4. 
        ELSE IF florplan-list.zistatus = 8 THEN florplan-list.bcol =  5. 
        ELSE IF florplan-list.zistatus = 9 THEN florplan-list.bcol = 13. 
        florplan-list.fcol = item-fgcol[florplan-list.bcol]. 
 
        IF zimmer.zistatus = 0 THEN 
        DO: 
            FIND FIRST res-line WHERE res-line.active-flag = 0 
                AND res-line.ankunft = ci-date 
                AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
            IF AVAILABLE res-line THEN 
            DO: 
                florplan-list.bcol = 9. 
                florplan-list.fcol = 15.
            END. 
        END. 
 
        ELSE IF zimmer.zistatus GE 1 AND zimmer.zistatus LE 2 THEN 
        DO: 
            FIND FIRST res-line WHERE res-line.active-flag = 0 
                AND res-line.ankunft = ci-date 
                AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
            IF AVAILABLE res-line THEN 
            DO: 
                florplan-list.bcol = 10. 
                florplan-list.fcol = 0. 
            END. 
        END. 
 
        ELSE IF zimmer.zistatus GE 3 AND zimmer.zistatus LE 5 THEN 
        DO: 
            FIND FIRST res-line WHERE res-line.active-flag = 1 
                AND res-line.zinr = zimmer.zinr NO-LOCK NO-ERROR. 
            IF AVAILABLE res-line AND 
              (res-line.betrieb-gastmem = vipnr1 OR 
               res-line.betrieb-gastmem = vipnr2 OR 
               res-line.betrieb-gastmem = vipnr3 OR 
               res-line.betrieb-gastmem = vipnr4 OR 
               res-line.betrieb-gastmem = vipnr5 OR 
               res-line.betrieb-gastmem = vipnr6 OR 
               res-line.betrieb-gastmem = vipnr7 OR 
               res-line.betrieb-gastmem = vipnr8 OR 
               res-line.betrieb-gastmem = vipnr9) THEN 
            DO: 
               florplan-list.bcol      = 15. 
               florplan-list.fcol      = 12.
            END. 
        END. 
        RUN fill-ooo (zimmer.zinr, OUTPUT florplan-list.g-info, OUTPUT florplan-list.r-info).        
    END. 
END. 
PROCEDURE fill-ooo:
DEF INPUT  PARAMETER curr-room   AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER n-edit AS CHAR NO-UNDO INIT "".
DEF OUTPUT PARAMETER c-edit AS CHAR NO-UNDO INIT "".
  FOR EACH t-res-line:
      DELETE t-res-line.
  END.
  FOR EACH t-reservation:
      DELETE t-reservation.
  END.
  FOR EACH t-waehrung:
      DELETE t-waehrung.
  END.
  FOR EACH t-outorder:
      DELETE t-outorder.
  END.
  
  RUN read-res-linebl.p(20, ?,?, 6, 1, curr-room, ?,?,?,?, "", OUTPUT TABLE t-res-line).
  FIND FIRST t-res-line NO-ERROR.
  IF NOT AVAILABLE t-res-line THEN 
  RUN read-res-linebl.p(20, ?,?, 13, 1, curr-room, ?,?,?,?, "", OUTPUT TABLE t-res-line).
  IF NOT AVAILABLE t-res-line THEN 
      RUN read-res-linebl.p(55, ?,?,?,?, curr-room, ci-date, ?,?,?, "", OUTPUT TABLE t-res-line).
  FIND FIRST t-res-line NO-ERROR.
  IF NOT AVAILABLE t-res-line THEN DO:
      RUN read-res-linebl.p(56, ?,?,?,?, curr-room, ?,?,?,?, "", OUTPUT TABLE t-res-line).
  END.
  IF AVAILABLE t-res-line THEN 
  DO:
      RUN read-reservationbl.p(1, t-res-line.resnr, ?, "", OUTPUT TABLE t-reservation).
      FIND FIRST t-reservation.
      n-edit = translateExtended ("ResNo:",lvCAREA,"") + " " + STRING(t-res-line.resnr) + "   " 
           + translateExtended ("Room:",lvCAREA,"")    + " " + t-res-line.zinr + CHR(10) 
           + translateExtended ("Guest:",lvCAREA,"")   + " " + t-res-line.name + CHR(10) 
           + translateExtended ("Group:",lvCAREA,"")   + " " + t-reservation.groupname + CHR(10) 
           + translateExtended ("Arrival:",lvCAREA,"") + " " + STRING(t-res-line.ankunft) + CHR(10) 
           + translateExtended ("Depart:",lvCAREA,"")  + " " + STRING(t-res-line.abreise) + CHR(10) 
           + translateExtended ("Adult:",lvCAREA,"")   + " " + STRING(t-res-line.erwachs) + CHR(10) 
           + translateExtended ("RmRate:",lvCAREA,"")  + " " + STRING(t-res-line.zipreis). 
      IF t-res-line.betriebsnr GT 0 THEN 
      DO:
        RUN read-waehrungbl.p(1, t-res-line.betriebsnr, "", OUTPUT TABLE t-waehrung).
        FIND FIRST t-waehrung NO-ERROR.
        IF AVAILABLE t-waehrung THEN n-edit = n-edit + " " + t-waehrung.wabkurz. 
      END. 
      c-edit = translateExtended ("Reservation Comment:",lvCAREA,"") + CHR(10) 
           + t-reservation.bemerk + CHR(10) 
           + t-res-line.bemerk. 
      FIND FIRST zimmer WHERE zimmer.zinr = curr-room NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN DO:
          RUN read-outorderbl.p(4, zimmer.zinr, ?, ci-date, ?, OUTPUT TABLE t-outorder).
          FIND FIRST t-outorder NO-ERROR.
          IF AVAILABLE t-outorder THEN
          DO:
              c-edit = STRING(t-outorder.gespstart) + " - " +
                       string(t-outorder.gespende) + CHR(10)
                     + t-outorder.gespgrund.
          END.
      END.
  END.
END.
