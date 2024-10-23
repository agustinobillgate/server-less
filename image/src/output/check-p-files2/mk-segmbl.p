  
DEFINE TEMP-TABLE gsegm-list LIKE segment.  
  
DEFINE INPUT  PARAMETER TABLE FOR gsegm-list.  
DEFINE INPUT  PARAMETER gastnr    AS INTEGER.  
DEFINE INPUT  PARAMETER done      AS LOGICAL.  
DEFINE INPUT  PARAMETER flag      AS LOGICAL.  
DEFINE INPUT  PARAMETER change-it AS LOGICAL.  
DEFINE INPUT  PARAMETER vip-flag1 AS LOGICAL.  
DEFINE INPUT  PARAMETER mainscode AS INTEGER.  
DEFINE INPUT  PARAMETER mainseg   AS INTEGER.  
/*MTDEF VAR gastnr AS INT INIT 408.  
DEF VAR done AS LOGICAL INIT YES.  
DEF VAR flag AS LOGICAL INIT YES.  
DEF VAR change-it AS LOGICAL INIT YES.  
DEF VAR vip-flag1 AS LOGICAL INIT NO.  
DEF VAR mainscode AS INT INIT 7.  
DEF VAR mainseg AS INT INIT 7.*/  
  
  
DEFINE VARIABLE vip-flag2 AS LOGICAL INITIAL NO.  
DEFINE VARIABLE vip-segm  AS INTEGER INITIAL 0.   
  
DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999.   
  
RUN get-vipnrbl.p  
    (OUTPUT vipnr1, OUTPUT vipnr2, OUTPUT vipnr3, OUTPUT vipnr4,  
     OUTPUT vipnr5, OUTPUT vipnr6, OUTPUT vipnr7, OUTPUT vipnr8,  
     OUTPUT vipnr9).  
  
IF done = YES AND flag = YES AND change-it THEN   
DO:   
    FOR EACH guestseg WHERE guestseg.gastnr = gastnr:   
      delete guestseg.   
    END.  
  
    FIND FIRST gsegm-list WHERE gsegm-list.segmentcode = mainscode NO-ERROR.   
    IF AVAILABLE gsegm-list THEN   
    DO:   
      create guestseg.   
      guestseg.gastnr = gastnr.   
      guestseg.segmentcode = gsegm-list.segmentcode.   
      guestseg.reihenfolge = 1.   
    END.   
    FOR EACH gsegm-list WHERE gsegm-list.segmentcode NE mainscode:   
      create guestseg.   
      guestseg.gastnr = gastnr.   
      guestseg.segmentcode = gsegm-list.segmentcode.   
    END.   
    IF mainscode NE mainseg THEN   
    DO:   
/*   
      FIND FIRST res-line WHERE res-line.gastnrmember = gastnr   
        AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.   
      DO WHILE AVAILABLE res-line:   
        FIND CURRENT res-line EXCLUSIVE-LOCK.   
        gsegm-list.segmentcode = mainscode.   
        FIND CURRENT res-line NO-LOCK.   
        FIND NEXT res-line WHERE res-line.gastnrmember = gastnr   
          AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.   
      END.   
*/   
    END.   
END.   
   
  FIND FIRST gsegm-list WHERE   
   (gsegm-list.segmentcode = vipnr1 OR   
    gsegm-list.segmentcode = vipnr2 OR   
    gsegm-list.segmentcode = vipnr3 OR   
    gsegm-list.segmentcode = vipnr4 OR   
    gsegm-list.segmentcode = vipnr5 OR   
    gsegm-list.segmentcode = vipnr6 OR   
    gsegm-list.segmentcode = vipnr7 OR   
    gsegm-list.segmentcode = vipnr8 OR   
    gsegm-list.segmentcode = vipnr9) NO-LOCK NO-ERROR.   
  IF AVAILABLE gsegm-list THEN   
  DO:   
    vip-flag2 = YES.   
    vip-segm = gsegm-list.segmentcode.   
  END.   
  IF vip-flag1 NE vip-flag2 THEN   
  DO:   
    /*MTCURRENT-WINDOW:LOAD-MOUSE-POINTER("wait").   
    PROCESS EVENTS. */  
    FIND FIRST res-line WHERE res-line.gastnrmember = gastnr   
      AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.   
    DO WHILE AVAILABLE res-line:   
      FIND CURRENT res-line EXCLUSIVE-LOCK.   
      res-line.betrieb-gastmem = vip-segm.   
      FIND CURRENT res-line NO-LOCK.   
      FIND NEXT res-line WHERE res-line.gastnrmember = gastnr   
        AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.   
    END.   
    /*MTCURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow"). */  
  END.   
   
   
