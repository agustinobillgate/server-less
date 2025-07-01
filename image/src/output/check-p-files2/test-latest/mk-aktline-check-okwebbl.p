{Supertrans.i}

DEFINE INPUT PARAMETER aktionscode  AS INTEGER.
DEFINE INPUT PARAMETER zeit         AS INTEGER.
DEFINE INPUT PARAMETER dauer        AS INTEGER.
DEFINE INPUT PARAMETER gastnr       AS INTEGER.
DEFINE INPUT PARAMETER kontakt      AS CHARACTER.
DEFINE OUTPUT PARAMETER msg-str2    AS CHARACTER.

DEF VAR lvCAREA AS CHAR INITIAL "mk-aktline".

IF aktionscode = 0 THEN 
DO: 
  msg-str2 = "Activity Type not yet defined".  
  RETURN NO-APPLY. 
END.
ELSE IF zeit = 0 THEN 
DO: 
  msg-str2 = "Start Time not yet defined".  
  RETURN NO-APPLY. 
END.
ELSE IF dauer = 0 THEN 
DO:  
  msg-str2 = "End Time not yet defined".  
  RETURN NO-APPLY. 
END.
ELSE IF gastnr = 0 THEN 
DO: 
  msg-str2 = "Company name not yet defined". 
  RETURN NO-APPLY. 
END.
ELSE IF kontakt = "" THEN 
DO: 
  msg-str2 = "Name Contact not yet defined".  
  RETURN NO-APPLY. 
END.
