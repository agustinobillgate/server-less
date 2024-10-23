DEF TEMP-TABLE cr-list
    FIELD curr-row   AS INTEGER
    FIELD curr-col   AS INTEGER
    FIELD zistatus   AS INTEGER
    FIELD i-bgcol    AS INTEGER INIT 15
    FIELD i-fgcol    AS INTEGER INIT 0
    FIELD i-resnr    AS INTEGER INIT 0
    FIELD i-reslinnr AS INTEGER INIT 0
    FIELD i-rstat    AS INTEGER INIT ?
    FIELD rmcat      AS CHAR    INIT ""
    FIELD ankunft    AS DATE   
    FIELD abreise    AS DATE   
    FIELD g-info     AS CHAR    INIT ""
    FIELD r-info     AS CHAR    INIT ""
    FIELD arrival    AS LOGICAL INIT NO 
    FIELD selectFlag AS LOGICAL INIT YES
    FIELD room       LIKE zimmer.zinr INIT "" FORMAT "x(12)"
    INDEX zinr_ix room
 .

DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER max-row     AS INTEGER NO-UNDO INIT 0.
DEF OUTPUT PARAMETER max-col     AS INTEGER NO-UNDO INIT 1.
DEF OUTPUT PARAMETER TABLE       FOR cr-list.

DEF VARIABLE curr-i   AS INTEGER NO-UNDO.
DEF VARIABLE ci-date  AS DATE    NO-UNDO.

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

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline". 


FIND FIRST htparam WHERE htparam.paramnr = 700 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr1 = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 701 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr2 = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 702 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr3 = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 703 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr4 = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 704 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr5 = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 705 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr6 = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 706 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr7 = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 707 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr8 = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 708 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr9 = htparam.finteger. 

RUN htpdate.p(87, OUTPUT ci-date).
RUN cal-max-row.
RUN create-r-list.

PROCEDURE cal-max-row:
    DEF VARIABLE s-floor    AS CHAR    NO-UNDO INIT "".
    DEF VARIABLE curr-max   AS INTEGER NO-UNDO INIT 0.
    DEF VARIABLE l-floor    AS INTEGER NO-UNDO.
    FOR EACH zimmer NO-LOCK BY LENGTH(zimmer.zinr) BY zimmer.zinr: /* Malik serverless : BY LENGTH(zinr) BY zinr -> BY LENGTH(zimmer.zinr) BY zimmer.zinr */
        ASSIGN l-floor = LENGTH(STRING(zimmer.etage)).
        IF s-floor NE SUBSTR(zimmer.zinr, 1, l-floor) THEN
        DO:
            IF curr-max GT max-row THEN max-row = curr-max.
            ASSIGN 
                s-floor  = SUBSTR(zimmer.zinr, 1, l-floor)
                curr-max = 1
            .
        END.
        ELSE curr-max = curr-max + 1.
    END.
    IF curr-max GT max-row THEN max-row = curr-max.
    IF max-row GT 22 THEN max-row = ROUND(max-row / 2, 0).
END.

PROCEDURE create-r-list:
    DEF VARIABLE s-floor    AS CHAR    NO-UNDO INIT "".
    DEF VARIABLE l-floor    AS INTEGER NO-UNDO.
    DEF VARIABLE curr-row   AS INTEGER NO-UNDO INIT 1.
    FOR EACH zimmer NO-LOCK BY LENGTH(zimmer.zinr) BY zimmer.zinr: /* Malik serverless : BY LENGTH(zinr) BY zinr -> BY LENGTH(zimmer.zinr) BY zimmer.zinr */
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK.
        ASSIGN l-floor  = LENGTH(STRING(zimmer.etage)).
        IF s-floor = "" THEN s-floor  = SUBSTR(zimmer.zinr, 1, l-floor).

        CREATE cr-list.
        ASSIGN 
            cr-list.curr-row   = curr-row
            cr-list.curr-col   = max-col
            cr-list.room       = zimmer.zinr
            cr-list.rmcat      = zimkateg.kurzbez
            cr-list.zistatus   = zimmer.zistatus
            curr-row           = curr-row + 1.

        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
              AND outorder.gespstart LE ci-date 
              AND outorder.gespende  GE ci-date NO-LOCK NO-ERROR. 
        IF AVAILABLE outorder THEN 
        DO: 
              IF outorder.betriebsnr = 2 THEN cr-list.zistatus = 7. 
              ELSE IF outorder.betriebsnr = 3 OR outorder.betriebsnr = 4 
              THEN cr-list.zistatus = 9.  
        END. 

        CASE cr-list.zistatus:
            WHEN 0 THEN cr-list.i-bgcol = 8. 
            WHEN 1 THEN cr-list.i-bgcol = 11. 
            WHEN 2 THEN cr-list.i-bgcol =  2. 
            WHEN 3 THEN cr-list.i-bgcol =  1. 
            WHEN 4 THEN cr-list.i-bgcol = 14. 
            WHEN 5 THEN cr-list.i-bgcol = 15. 
            WHEN 6 THEN cr-list.i-bgcol = 12. 
            WHEN 7 THEN cr-list.i-bgcol =  4. 
            WHEN 8 THEN cr-list.i-bgcol =  5. 
            WHEN 9 THEN cr-list.i-bgcol = 13. 
        END CASE.
        cr-list.i-fgcol = item-fgcol[cr-list.i-bgcol].  
        
        IF cr-list.zistatus = 6 THEN 
        RUN fill-ooo (cr-list.room,
                      OUTPUT cr-list.g-info,
                      OUTPUT cr-list.r-info).
        
        IF s-floor NE SUBSTR(zimmer.zinr, 1, l-floor) THEN
        DO:
            ASSIGN s-floor  = SUBSTR(zimmer.zinr, 1, l-floor).
            IF curr-row GT 2 AND SUBSTR(zimmer.zinr, 1, l-floor) 
                = STRING(zimmer.etage) THEN
            ASSIGN
                curr-row = 1
                max-col = max-col + 1
            .
        END.
        ELSE IF curr-row GT max-row THEN
        ASSIGN 
            curr-row = 1
            max-col = max-col + 1
        .
    END.
    FOR EACH res-line WHERE res-line.active-flag LE 1 AND 
        res-line.resstatus NE 12                      AND 
        res-line.l-zuordnung[3] = 0                   AND
        res-line.zinr NE "" NO-LOCK 
        BY res-line.active-flag DESCENDING
        BY res-line.ankunft BY res-line.resstatus:
        FIND FIRST reservation WHERE 
            reservation.resnr = res-line.resnr NO-LOCK.
        FIND FIRST cr-list WHERE cr-list.room = res-line.zinr.
        IF cr-list.i-resnr = 0 THEN
        DO:
            ASSIGN
                cr-list.i-resnr     = res-line.resnr
                cr-list.i-reslinnr  = res-line.reslinnr
                cr-list.ankunft     = res-line.ankunft
                cr-list.abreise     = res-line.abreise
                cr-list.i-rstat     = res-line.resstatus.
            RUN fill-res-info(1, INPUT-OUTPUT cr-list.g-info,
                INPUT-OUTPUT cr-list.r-info).

            IF (res-line.active-flag = 0  AND  res-line.ankunft = ci-date) THEN 
                ASSIGN cr-list.arrival   = YES.

        END.
        ELSE IF cr-list.abreise  = ci-date  AND
            (res-line.active-flag = 0       AND 
            res-line.ankunft     = ci-date) THEN
        DO:
            ASSIGN cr-list.arrival   = YES.
            RUN fill-res-info(2, INPUT-OUTPUT cr-list.g-info,
                INPUT-OUTPUT cr-list.r-info).
        END.

        /*IF cr-list.i-rstat = 0 THEN /* arrival check-in */*/
        IF cr-list.arrival = YES THEN DO:

            FIND FIRST queasy WHERE queasy.KEY = 162
                AND queasy.char1   = cr-list.room 
                AND queasy.number1 = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
                ASSIGN 
                    cr-list.i-bgcol = 6 
                    cr-list.i-fgcol = 15.   
            ELSE DO:
                IF cr-list.zistatus = 0 THEN
                    ASSIGN
                        cr-list.i-bgcol = 9 
                        cr-list.i-fgcol = 15. 
            ELSE 
                ASSIGN
                    cr-list.i-bgcol = 10 
                    cr-list.i-fgcol = 0.
            END.            
        END.
        ELSE IF cr-list.zistatus LE 2 THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY = 162
                AND queasy.char1   = cr-list.room 
                AND queasy.number1 = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            ASSIGN 
                cr-list.i-bgcol = 6 
                cr-list.i-fgcol = 15
            .   
            ELSE DO:
                IF cr-list.zistatus = 0 THEN
                    ASSIGN
                        cr-list.i-bgcol = 8
                        cr-list.i-fgcol = 0.
                ELSE IF cr-list.zistatus = 1 THEN
                    ASSIGN
                        cr-list.i-bgcol = 11
                        cr-list.i-fgcol = 0.
                ELSE IF cr-list.zistatus = 2 THEN
                    ASSIGN
                        cr-list.i-bgcol = 2
                        cr-list.i-fgcol = 0.
            END.

            /*ASSIGN
                cr-list.i-bgcol = 10 
                cr-list.i-fgcol = 0. */
        END.
        ELSE IF cr-list.zistatus GE 3 AND 
            cr-list.zistatus LE 5 THEN 
        DO: 
            IF cr-list.arrival THEN
            ASSIGN /* ED + EA */
                cr-list.i-bgcol = 14
                cr-list.i-fgcol = 12
            .
            ELSE IF (res-line.betrieb-gastmem = vipnr1 OR 
                res-line.betrieb-gastmem = vipnr2 OR 
                res-line.betrieb-gastmem = vipnr3 OR 
                res-line.betrieb-gastmem = vipnr4 OR 
                res-line.betrieb-gastmem = vipnr5 OR 
                res-line.betrieb-gastmem = vipnr6 OR 
                res-line.betrieb-gastmem = vipnr7 OR 
                res-line.betrieb-gastmem = vipnr8 OR 
                res-line.betrieb-gastmem = vipnr9) THEN 
            ASSIGN
                cr-list.i-bgcol = 15
                cr-list.i-fgcol = 12
            .
        END.
    END.
END.
/*
PROCEDURE assign-browse-color:
    DEF VARIABLE curr-i     AS INTEGER NO-UNDO.
    DEF VARIABLE curr-j     AS INTEGER NO-UNDO.
    DEF VARIABLE curr-resnr AS INTEGER NO-UNDO INIT 0.
    DEF VARIABLE i-zistat   AS INTEGER NO-UNDO.
    FOR EACH cr-list BY cr-list.curr-row:
      curr-i = cr-list.curr-col:
          IF cr-list.room NE "" THEN
          DO:
              CASE cr-list.zistatus:
                  WHEN 0 THEN cr-list.i-bgcol = 8. 
                  WHEN 1 THEN cr-list.i-bgcol = 11. 
                  WHEN 2 THEN cr-list.i-bgcol =  2. 
                  WHEN 3 THEN cr-list.i-bgcol =  1. 
                  WHEN 4 THEN cr-list.i-bgcol = 14. 
                  WHEN 5 THEN cr-list.i-bgcol = 15. 
                  WHEN 6 THEN cr-list.i-bgcol = 12. 
                  WHEN 7 THEN cr-list.i-bgcol =  4. 
                  WHEN 8 THEN cr-list.i-bgcol =  5. 
                  WHEN 9 THEN cr-list.i-bgcol = 13. 
              END CASE.
              cr-list.i-fgcol = item-fgcol[r-list.i-bgcol].  
              IF cr-list.zistatus = 6 THEN 
              RUN fill-ooo (r-list.room,
                            OUTPUT cr-list.g-info,
                            OUTPUT cr-list.r-info).
          END.
          ELSE
          ASSIGN 
              cr-list.i-bgcol = 15
              cr-list.i-fgcol = 0
          .
      END.
    END.
    FOR EACH cr-list WHERE cr-list.i-resnr GT 0
        BY cr-list.resnr:
        FIND FIRST res-line WHERE res-line.resnr = cr-list.i-resnr
            AND res-line.reslinnr = cr-list.i-reslinnr NO-LOCK.
        IF curr-resnr NE cr-list.i-resnr THEN
        DO:
            curr-resnr = cr-list.i-resnr.
            FIND FIRST reservation WHERE 
                reservation.resnr = curr-resnr NO-LOCK.
        END.
        ASSIGN 
            curr-j                      = room-list.i-col
            cr-list.i-resnr[curr-j]      = room-list.resnr
            cr-list.i-reslinnr[curr-j]   = room-list.reslinnr
            cr-list.ankunft[curr-j]      = room-list.ankunft
            cr-list.abreise[curr-j]      = room-list.abreise
            cr-list.i-rstat[curr-j]      = room-list.resstatus
            cr-list.g-info[curr-j]       = ""
            cr-list.r-info[curr-j]       = ""
        .
        RUN fill-res-info(1, INPUT-OUTPUT cr-list.g-info[curr-j],
            INPUT-OUTPUT cr-list.r-info[curr-j]).
        IF cr-list.zistatus[curr-j] = 0 THEN /* arrival check-in */
        ASSIGN
            cr-list.i-bgcol[curr-j] = 9 
            cr-list.i-fgcol[curr-j] = 15
        . 
        ELSE IF cr-list.zistatus[curr-j] LE 2 THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY = 162
                AND queasy.char1   = cr-list.room[curr-j] 
                AND queasy.number1 = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            ASSIGN 
                cr-list.i-bgcol[curr-j] = 6 
                cr-list.i-fgcol[curr-j] = 15
            .   
            ELSE
            ASSIGN
                cr-list.i-bgcol[curr-j] = 10 
                cr-list.i-fgcol[curr-j] = 0
            . 
        END.
        ELSE IF cr-list.zistatus[curr-j] GE 3 AND 
            cr-list.zistatus[curr-j] LE 5 THEN 
        DO: 

            IF room-list.arrival THEN
            DO:
                RUN fill-res-info(2, INPUT-OUTPUT cr-list.g-info[curr-j],
                    INPUT-OUTPUT cr-list.r-info[curr-j]).
                ASSIGN /* ED + EA */
                    cr-list.i-bgcol[curr-j] = 14
                    cr-list.i-fgcol[curr-j] = 12
                .
            END.
            ELSE IF (res-line.betrieb-gastmem = vipnr1 OR 
                res-line.betrieb-gastmem = vipnr2 OR 
                res-line.betrieb-gastmem = vipnr3 OR 
                res-line.betrieb-gastmem = vipnr4 OR 
                res-line.betrieb-gastmem = vipnr5 OR 
                res-line.betrieb-gastmem = vipnr6 OR 
                res-line.betrieb-gastmem = vipnr7 OR 
                res-line.betrieb-gastmem = vipnr8 OR 
                res-line.betrieb-gastmem = vipnr9) THEN 
            ASSIGN
                cr-list.i-bgcol[curr-j] = 15
                cr-list.i-fgcol[curr-j] = 12
            .
    END.
END.
*/
PROCEDURE fill-ooo:
    DEF INPUT  PARAMETER rmNo   AS CHAR NO-UNDO.
    DEF OUTPUT PARAMETER g-info AS CHAR NO-UNDO INIT "".
    DEF OUTPUT PARAMETER r-info AS CHAR NO-UNDO INIT "".
    FIND FIRST outorder WHERE outorder.zinr = rmNo
        AND NOT outorder.gespstart GT res-line.abreise
        AND NOT outorder.gespende  LE res-line.ankunft 
        NO-LOCK NO-ERROR.
    IF AVAILABLE outorder THEN
    r-info = STRING(outorder.gespstart) + " - "
           + STRING(outorder.gespende) + CHR(10)
           + outorder.gespgrund.
END.

PROCEDURE fill-res-info:
    DEF INPUT  PARAMETER i-case AS INTEGER NO-UNDO.
    DEF INPUT-OUTPUT PARAMETER g-info AS CHAR NO-UNDO INIT "".
    DEF INPUT-OUTPUT PARAMETER r-info AS CHAR NO-UNDO INIT "".
    DEF BUFFER rbuff   FOR res-line.
    DEF BUFFER rsvbuff FOR reservation.
  CASE i-case:
      WHEN 1 THEN
      DO:
          g-info = translateExtended ("ResNo:",lvCAREA,"") + " " + STRING(res-line.resnr) + "   " 
                 + translateExtended ("Room:",lvCAREA,"")    + " " + res-line.zinr + CHR(10) 
                 + translateExtended ("Guest:",lvCAREA,"")   + " " + res-line.name + CHR(10) 
                 + translateExtended ("Group:",lvCAREA,"")   + " " + reservation.groupname + CHR(10) 
                 + translateExtended ("Arrival:",lvCAREA,"") + " " + STRING(res-line.ankunft) + CHR(10) 
                 + translateExtended ("Depart:",lvCAREA,"")  + " " + STRING(res-line.abreise) + CHR(10) 
                 + translateExtended ("Adult:",lvCAREA,"")   + " " + STRING(res-line.erwachs) + CHR(10) 
                 + translateExtended ("RmRate:",lvCAREA,"")  + " " + STRING(res-line.zipreis). 
          IF res-line.betriebsnr GT 0 THEN 
          DO:
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr
                NO-LOCK NO-ERROR.
            IF AVAILABLE waehrung THEN
                 g-info = g-info + " " + waehrung.wabkurz. 
          END. 
          IF reservation.bemerk NE "" OR res-line.bemerk NE "" THEN
          r-info = translateExtended ("Reservation Comment:",lvCAREA,"") + CHR(10) 
                 + reservation.bemerk + CHR(10) 
                 + res-line.bemerk. 
          FIND FIRST reslin-queasy WHERE 
              reslin-queasy.KEY      = "specialRequest" AND
              reslin-queasy.resnr    = res-line.resnr   AND
              reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
          IF AVAILABLE reslin-queasy THEN
          r-info = r-info + CHR(10)
                 + translateExtended ("Special Request:",lvCAREA,"")   + " " 
                 + reslin-queasy.char3.
      END.
      WHEN 2 THEN
      DO:
          FIND FIRST rbuff WHERE rbuff.active-flag = 0
              AND rbuff.ankunft = ci-date
              AND (rbuff.resstatus LE 2 OR rbuff.resstatus = 5)
              AND rbuff.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF NOT AVAIL rbuff THEN
          FIND FIRST rbuff WHERE rbuff.active-flag = 0
              AND rbuff.ankunft = ci-date
              AND rbuff.resstatus = 11
              AND rbuff.l-zuordnung[3] = 0
              AND rbuff.zinr = res-line.zinr NO-LOCK NO-ERROR.
          IF NOT AVAILABLE rbuff THEN RETURN.
          FIND FIRST rsvbuff WHERE rsvbuff.resnr = rbuff.resnr NO-LOCK.
          g-info = g-info + CHR(10) + CHR(10)
                 + translateExtended ("ResNo:",lvCAREA,"")   + " " + STRING(rbuff.resnr) + "   " 
                 + translateExtended ("Room:",lvCAREA,"")    + " " + rbuff.zinr + CHR(10) 
                 + translateExtended ("Guest:",lvCAREA,"")   + " " + rbuff.name + CHR(10) 
                 + translateExtended ("Group:",lvCAREA,"")   + " " + rsvbuff.groupname + CHR(10) 
                 + translateExtended ("Arrival:",lvCAREA,"") + " " + STRING(rbuff.ankunft) + CHR(10) 
                 + translateExtended ("Depart:",lvCAREA,"")  + " " + STRING(rbuff.abreise) + CHR(10) 
                 + translateExtended ("Adult:",lvCAREA,"")   + " " + STRING(rbuff.erwachs) + CHR(10) 
                 + translateExtended ("RmRate:",lvCAREA,"")  + " " + STRING(rbuff.zipreis). 
          IF rbuff.betriebsnr GT 0 THEN 
          DO:
            FIND FIRST waehrung WHERE waehrung.waehrungsnr = rbuff.betriebsnr
                NO-LOCK NO-ERROR.
            IF AVAILABLE waehrung THEN
                 g-info = g-info + " " + waehrung.wabkurz. 
          END. 
          IF rsvbuff.bemerk NE "" OR rbuff.bemerk NE "" THEN
          r-info = r-info + CHR(10) + CHR(10)
                 + translateExtended ("Reservtion Comment:",lvCAREA,"") + CHR(10) 
                 + rsvbuff.bemerk + CHR(10) 
                 + rbuff.bemerk. 
          FIND FIRST reslin-queasy WHERE 
              reslin-queasy.KEY      = "specialRequest" AND
              reslin-queasy.resnr    = rbuff.resnr   AND
              reslin-queasy.reslinnr = rbuff.reslinnr NO-LOCK NO-ERROR.
          IF AVAILABLE reslin-queasy THEN
          r-info = r-info + CHR(10)
                 + translateExtended ("Special Request:",lvCAREA,"")   + " " 
                 + reslin-queasy.char3.
      END.
  END CASE.
END.
