  
  
DEF INPUT  PARAMETER pvILanguage   AS INTEGER  NO-UNDO.  
DEF INPUT  PARAMETER recid1     AS INT.  
DEF INPUT  PARAMETER moved-room AS CHAR.  
DEF INPUT  PARAMETER ci-date    AS DATE.  
DEF OUTPUT PARAMETER msg-str    AS CHAR.  
  
{SupertransBL.i}  
DEF VAR lvCAREA AS CHAR INITIAL "roomplan".   
  
RUN check-room.  
  
PROCEDURE check-room:   
DEF VARIABLE i               AS INTEGER INITIAL 1  NO-UNDO.   
DEF VARIABLE f-date          AS DATE               NO-UNDO.     /* Rulita 221124 | Fixing For serverless fdate change to f-date */
DEF VARIABLE error-code      AS INTEGER            NO-UNDO.   
DEF VARIABLE rmcat           AS CHAR               NO-UNDO.   
DEF VARIABLE answer          AS LOGICAL INITIAL NO NO-UNDO.   
    
    
  FIND FIRST res-line WHERE RECID(res-line) = recid1 NO-LOCK. 
  IF NOT AVAILABLE res-line THEN                          /* Rulita 201124 | Fixing for serverless */
  DO:
    RETURN.
  END.
  
  FIND FIRST zimmer WHERE zimmer.zinr = moved-room NO-LOCK.   
  IF (zimmer.zistatus NE 0) AND res-line.active-flag = 1 THEN  
  DO:  
    msg-str = msg-str + CHR(2)  
            + translateExtended ("Room assignment not possible.", lvCAREA, "":U).  
    i = 99.  
    RETURN.   
  END.  
  
  FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.   
  IF AVAILABLE zimkateg THEN   
  DO:  
    IF res-line.active-flag = 1 THEN f-date = ci-date.  
    ELSE f-date = res-line.ankunft.   
    rmcat = zimkateg.kurzbez.   
  END.  
  
  RUN res-czinrbl.p(pvILanguage, f-date, res-line.abreise,   
    (res-line.resstatus = 11 OR res-line.resstatus = 13),  
     res-line.resnr, res-line.reslinnr, INPUT-OUTPUT rmcat,  
     zimmer.zinr, OUTPUT error-code, OUTPUT msg-str).  
  
  IF error-code NE 0 THEN   
  DO:   
    msg-str = msg-str + CHR(2)  
            + translateExtended ("Room assignment not possible.", lvCAREA, "":U).  
    i = 99.   
    RETURN.   
  END.   
  ELSE   
  DO:   
    IF zimmer.zikatnr NE res-line.zikatnr THEN   
    DO:   
        /* FD Comment
        msg-str = msg-str + CHR(2) + "&Q"  
              + translateExtended ("Room Type has changed, CONFIRM ROOM CHANGE?",lvCAREA, "":U).  
        */
        /*FD Sept 07, 2022 => 5BE61A - Block when change room to different room type*/
        msg-str = msg-str + CHR(2) + "&W"  
                + translateExtended ("Different Room Type Detected!",lvCAREA, "":U)
                + CHR(10)  
                + translateExtended ("Please Go To Modify Reservation For Change Room.",lvCAREA, "":U).
    END.   
    /*MTRUN move-room.   
    changed = YES. */  
    RETURN.   
  END.   
  
END PROCEDURE.   
