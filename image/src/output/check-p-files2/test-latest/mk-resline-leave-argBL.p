DEF TEMP-TABLE reslin-list LIKE res-line.  
  
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.  
  
DEFINE INPUT PARAMETER res-mode         AS CHAR    NO-UNDO.   
DEFINE INPUT PARAMETER old-arg          AS CHAR    NO-UNDO.   
DEFINE INPUT PARAMETER contcode         AS CHAR    NO-UNDO.  
DEFINE INPUT-OUTPUT PARAMETER curr-arg  AS CHAR    NO-UNDO.   
  
DEFINE INPUT PARAMETER fixed-rate       AS LOGICAL NO-UNDO.   
DEFINE INPUT PARAMETER ebdisc-flag      AS LOGICAL NO-UNDO.   
DEFINE INPUT PARAMETER kbdisc-flag      AS LOGICAL NO-UNDO.   
DEFINE INPUT PARAMETER rate-readonly    AS LOGICAL NO-UNDO.   
  
DEFINE INPUT PARAMETER bookdate         AS DATE    NO-UNDO.  
  
DEFINE INPUT PARAMETER TABLE FOR reslin-list.  
  
DEFINE OUTPUT PARAMETER value-ok        AS LOGICAL NO-UNDO INIT NO.  
DEFINE OUTPUT PARAMETER restricted-disc AS LOGICAL NO-UNDO.   
DEFINE OUTPUT PARAMETER new-rate        AS DECIMAL NO-UNDO INIT ?.  
DEFINE OUTPUT PARAMETER msg-str         AS CHAR    NO-UNDO INIT "".  
DEFINE OUTPUT PARAMETER rate-tooltip    AS CHAR    NO-UNDO INIT ?.  
  
{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline".   
  
FIND FIRST reslin-list.  
RUN leave-argt.  
  
PROCEDURE leave-argt:   
  
  FIND FIRST arrangement WHERE arrangement.arrangement   
    = reslin-list.arrangement NO-LOCK NO-ERROR.   
  IF NOT AVAILABLE arrangement THEN   
  DO:   
    msg-str = translateExtended ("No such Arrangement", lvCAREA, "":U).   
    RETURN.   
  END.   
    
  IF (reslin-list.resstatus = 11 OR reslin-list.resstatus = 13)   
      AND (reslin-list.erwachs + reslin-list.kind1) = 0 THEN  
  DO:  
    FIND FIRST res-line WHERE res-line.resnr = reslin-list.resnr  
      AND (res-line.resstatus LE 2 OR res-line.resstatus = 5 OR res-line.resstatus = 6)  
      AND res-line.zinr = reslin-list.zinr NO-LOCK NO-ERROR.  
    IF AVAILABLE res-line AND res-line.arrangement NE reslin-list.arrangement THEN  
    DO:  
      msg-str = translateExtended ("Wrong Arrangement as Room Sharer with adult = 0", lvCAREA, "":U).   
      RETURN.   
    END.  
  END.  
  
  IF arrangement.waeschewechsel NE 0 AND reslin-list.erwachs NE  
     arrangement.waeschewechsel THEN  
  DO:  
    msg-str = translateExtended ("Wrong Arrangement / Adult", lvCAREA, "":U).  
    RETURN.   
  END.  
  
  IF arrangement.handtuch NE 0 AND reslin-list.anztage NE  
     arrangement.handtuch THEN  
  DO:  
    msg-str = translateExtended ("Wrong Arrangement / Night of Stay", lvCAREA, "":U).  
    RETURN.   
  END.  
  
  ASSIGN  
    value-ok = YES  
    curr-arg = reslin-list.arrangement  
  .   
    
  IF curr-arg NE old-arg THEN   
  DO:  
    IF (res-mode = "new" OR res-mode = "insert") THEN  
    RUN mk-resline-set-ratebl.p (NO, fixed-rate, ebdisc-flag, kbdisc-flag,   
      rate-readonly, reslin-list.gastnr, res-mode, curr-arg,  
      contcode, bookdate, TABLE reslin-list, OUTPUT restricted-disc,   
      OUTPUT new-rate, OUTPUT rate-tooltip).  
  END.  
  ELSE  
  DO:  
    FIND FIRST res-line WHERE res-line.resnr = reslin-list.resnr  
      AND res-line.reslinnr = reslin-list.reslinnr NO-LOCK NO-ERROR.  
    IF AVAILABLE res-line AND (curr-arg NE res-line.arrangement) THEN  
    msg-str = translateExtended ("Arrangement changed, re-check the RoomRate.", lvCAREA, "":U).   
  END.  
END.   
