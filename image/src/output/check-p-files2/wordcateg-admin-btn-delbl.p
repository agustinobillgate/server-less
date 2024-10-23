  
DEF INPUT  PARAMETER int1  AS INT.  
DEF INPUT  PARAMETER int2  AS INT.  
DEF INPUT  PARAMETER int3  AS INT.  
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.  
  
FIND FIRST brief WHERE (brief.briefkateg + 600) = int1 NO-LOCK NO-ERROR.  
IF AVAILABLE brief THEN RETURN.  
ELSE   
    RUN delete-paramtextbl.p  
        (1, int1, int2, int3, OUTPUT success-flag).  
      
  
