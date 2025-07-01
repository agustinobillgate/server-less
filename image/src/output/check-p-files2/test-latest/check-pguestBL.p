DEFINE TEMP-TABLE c-list   
  FIELD gastnr          AS INTEGER   
  FIELD resstatus       AS INTEGER   
  FIELD res-recid       AS INTEGER   
  FIELD zipreis         AS DECIMAL  FORMAT ">>,>>>,>>9.99"  LABEL "Room Rate"   
  FIELD zinr            LIKE zimmer.zinr                    LABEL "RmNo"    
  FIELD name            AS CHAR     FORMAT "x(32)"          LABEL "Guest Name"   
  FIELD pax             AS INTEGER  FORMAT ">>"             LABEL "Adult"   
  FIELD com             AS INTEGER  FORMAT ">>"             LABEL "Comp"   
  FIELD abreise         AS DATE                             LABEL "Departure"   
  FIELD land            AS CHAR     FORMAT "x(3)"           LABEL "Cntry"   
  FIELD nat             AS CHAR     FORMAT "x(3)"           LABEL "Nat"   
  FIELD nat2            AS CHAR     FORMAT "x(3)"           LABEL "LocRegion"   
  FIELD resart          AS INTEGER  FORMAT ">>"             LABEL "ResType"   
  FIELD segm            AS INTEGER  FORMAT ">>>"            LABEL "Segm"   
  FIELD segmentcode     AS INTEGER  FORMAT ">>>"            LABEL "GSegm"   
  FIELD ch              AS CHAR     FORMAT "x(1)"           LABEL ""   
  FIELD error-code      AS INTEGER INITIAL 0  
  FIELD nation-ok       AS LOGICAL INITIAL NO  
  FIELD land-ok         AS LOGICAL INITIAL NO  
  FIELD grpflag         AS LOGICAL  
  FIELD cardtype        AS INTEGER  
  FIELD resnr           AS INTEGER  
  FIELD reslinnr        AS INTEGER  
  FIELD rgastnr         AS INTEGER
  FIELD email           AS CHAR
  FIELD segm-descr      AS CHAR
  FIELD resart-descr    AS CHAR.

DEF TEMP-TABLE t-nation LIKE nation.  
  
DEF INPUT  PARAM pvILanguage AS INTEGER          NO-UNDO.  
DEF OUTPUT PARAM msg-str     AS CHAR INIT ""     NO-UNDO.  
DEF OUTPUT PARAM tot-room    AS INTEGER INIT 0   NO-UNDO.  
DEF OUTPUT PARAM ext-char    AS CHAR             NO-UNDO.  
DEF OUTPUT PARAM bill-date   AS DATE             NO-UNDO.  
DEF OUTPUT PARAM TABLE FOR t-nation.  
DEF OUTPUT PARAM TABLE FOR c-list.  
  
{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "check-puest".   
  
FIND FIRST htparam WHERE htparam.paramnr = 276 NO-LOCK.  
IF htparam.fchar NE "" THEN  
  RUN read-nationbl.p (0, htparam.fchar, "", OUTPUT TABLE t-nation).  
FIND FIRST t-nation NO-ERROR.  
IF NOT AVAILABLE t-nation THEN RETURN.  
  
RUN htpchar.p (148, OUTPUT ext-char).  
RUN htpdate.p (110, OUTPUT bill-date).  
  
RUN check-it.  
  
PROCEDURE check-it:   
DEF VAR segmentcode AS INTEGER NO-UNDO.  
  
  FOR EACH outorder WHERE outorder.gespende = bill-date NO-LOCK  
      BY outorder.zinr:  
    CREATE c-list.  
    ASSIGN  
      c-list.zinr       = outorder.zinr   
      c-list.name       = outorder.gespgrund  
      c-list.abreise    = outorder.gespende  
      c-list.resstatus  = 14  
      c-list.land       = "-"   
      c-list.nat        = "-"  
    .  
    IF outorder.betriebsnr GT 1 THEN c-list.resstatus = 15.  
  END.  
  FIND FIRST res-line WHERE res-line.zinr = "" AND   
      (res-line.resstatus = 6 OR res-line.resstatus = 13) 
      NO-LOCK NO-ERROR.   
  DO WHILE AVAILABLE res-line:   
    msg-str = msg-str + "&W"  
      + translateExtended ("Mal Reservation found! ResNo:",lvCAREA,"")   
      + " " + STRING(res-line.resnr)   
      + CHR(10)   
      + translateExtended ("Guest Name:",lvCAREA,"") + " " + res-line.name   
      + CHR(10)  
      + translateExtended ("Status inhouse but RmNo not assigend; set back to GUARANTEED.",lvCAREA,"").   
    FIND CURRENT res-line EXCLUSIVE-LOCK.   
    ASSIGN  
      res-line.resstatus   = 1   
      res-line.active-flag = 0  
    .   
    FIND CURRENT res-line NO-LOCK.   
    FIND NEXT res-line WHERE res-line.zinr = ""   
      AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
      NO-LOCK NO-ERROR.   
  END.   
   
  FIND FIRST res-line WHERE res-line.zinr NE ""   
      AND ((res-line.resstatus = 6 AND active-flag = 0)   
    OR (res-line.resstatus = 1 AND active-flag = 1)) NO-LOCK NO-ERROR.   
  DO WHILE AVAILABLE res-line:   
    FIND CURRENT res-line EXCLUSIVE-LOCK.   
    ASSIGN  
      res-line.resstatus   = 6   
      res-line.active-flag = 1  
    .   
    FIND CURRENT res-line NO-LOCK.   
    FIND NEXT res-line WHERE res-line.zinr NE ""   
      AND ((res-line.resstatus = 6 AND active-flag = 0)   
      OR (res-line.resstatus = 1 AND active-flag = 1)) NO-LOCK NO-ERROR.   
  END.   
   
  FOR EACH res-line WHERE res-line.active-flag = 1   
    AND (res-line.resstatus = 6 OR res-line.resstatus = 13)   
    AND res-line.l-zuordnung[3] = 0 NO-LOCK BY res-line.zinr:   
    ASSIGN   
      tot-room    = tot-room + 1  
      segmentcode = 0  
    .   
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK.   
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK.   
    FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr AND   
      guestseg.reihenfolge = 1 NO-LOCK NO-ERROR.   
    IF AVAILABLE guestseg THEN segmentcode = guestseg.segmentcode.   
   
    CREATE c-list.   
    ASSIGN  
        c-list.gastnr       = res-line.gastnrmember  
        c-list.resstatus    = res-line.resstatus  
        c-list.res-recid    = RECID(res-line)  
        c-list.zipreis      = res-line.zipreis   
        c-list.zinr         = res-line.zinr  
        c-list.name         = res-line.NAME  
        c-list.pax          = res-line.erwachs   
        c-list.com          = res-line.gratis   
        c-list.abreise      = res-line.abreise   
        c-list.land         = guest.land  
        c-list.nat          = guest.nation1   
        c-list.nat2         = guest.nation2   
        c-list.resart       = reservation.resart   
        c-list.segmentcode  = segmentcode   
        c-list.segm         = reservation.segmentcode  
        c-list.cardtype     = guest.karteityp  
        c-list.resnr        = res-line.resnr  
        c-list.reslinnr     = res-line.reslinnr  
        c-list.rgastnr      = reservation.gastnr  
        c-list.grpflag      = reservation.grpflag
        c-list.email        = guest.email-adr.  
  
    IF c-list.nat NE "" THEN  
    DO:  
      FIND FIRST nation WHERE nation.kurzbez = c-list.nat NO-LOCK NO-ERROR.  
      c-list.nation-ok = AVAILABLE nation.  
    END.  
  
    IF c-list.land NE "" THEN   
    DO:      
      FIND FIRST nation WHERE nation.kurzbez = c-list.land NO-LOCK NO-ERROR.  
      c-list.land-ok = AVAILABLE nation.  
    END.  

    IF c-list.segm NE 0 THEN DO:
        FIND FIRST segment WHERE segment.segmentcode = c-list.segm NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN c-list.segm-descr = segment.bezeich.
    END.
    
    IF c-list.resart NE 0 THEN DO:
        FIND FIRST Sourccod WHERE Sourccod.source-code = c-list.resart NO-LOCK NO-ERROR.
        IF AVAILABLE Sourccod THEN c-list.resart-descr = Sourccod.bezeich.
    END.
  END.  
END.   
