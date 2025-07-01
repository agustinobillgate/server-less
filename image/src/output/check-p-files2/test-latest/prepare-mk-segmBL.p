  
DEFINE TEMP-TABLE hsegm-list LIKE segment.  
DEFINE TEMP-TABLE gsegm-list LIKE segment.  
  
DEFINE INPUT  PARAMETER gastnr    AS INTEGER.   
DEFINE OUTPUT PARAMETER gtitle    AS CHAR.  
DEFINE OUTPUT PARAMETER mainscode AS INTEGER.  
DEFINE OUTPUT PARAMETER mainseg   AS INTEGER.  
DEFINE OUTPUT PARAMETER vip-flag1 AS LOGICAL.  
DEFINE OUTPUT PARAMETER TABLE FOR hsegm-list.  
DEFINE OUTPUT PARAMETER TABLE FOR gsegm-list.  
  
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
  
FOR EACH segment WHERE segment.vip-level = 0   
    AND NUM-ENTRIES(segment.bezeich, "$$0") = 1 NO-LOCK:   
    CREATE hsegm-list.   
    BUFFER-COPY segment TO hsegm-list.  
END.   
  
FOR EACH guestseg WHERE guestseg.gastnr = gastnr:   
  FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode.   
  create gsegm-list.   
  gsegm-list.segmentcode = segment.segmentcode.   
  gsegm-list.bezeich = segment.bezeich.   
  IF guestseg.reihenfolge = 1 THEN   
  DO:   
    gtitle = "        " + segment.bezeich.   
    mainscode = segment.segmentcode.   
    mainseg = mainscode.   
  END.   
  FIND FIRST hsegm-list WHERE   
    hsegm-list.segmentcode = gsegm-list.segmentcode NO-ERROR.   
  IF AVAILABLE hsegm-list THEN delete hsegm-list.   
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
IF AVAILABLE gsegm-list THEN vip-flag1 = YES.   
