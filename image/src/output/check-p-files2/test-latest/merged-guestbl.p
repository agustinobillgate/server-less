DEF TEMP-TABLE t-mc-guest   LIKE mc-guest.  
DEF TEMP-TABLE t-cl-member  LIKE cl-member. 
DEF TEMP-TABLE t-bk-veran   LIKE bk-veran.  
DEF TEMP-TABLE gast         LIKE guest.
DEF TEMP-TABLE t-guest-pr   LIKE guest-pr.  
DEF TEMP-TABLE t-res-line   LIKE res-line. 

DEFINE INPUT PARAMETER t-gastnr     AS INTEGER.
DEFINE INPUT PARAMETER s-gastnr     AS INTEGER.
DEFINE INPUT PARAMETER tg-karteityp AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHAR.

DEFINE OUTPUT PARAMETER mess-str AS CHAR.

DEFINE VARIABLE answer AS LOGICAL INITIAL NO.   
DEFINE VARIABLE flag1 AS LOGICAL.   
DEFINE VARIABLE flag2 AS LOGICAL.   
    
RUN read-mc-guestbl.p (1, t-gastnr, "", OUTPUT TABLE t-mc-guest).  
FIND FIRST t-mc-guest NO-ERROR.  
IF AVAILABLE t-mc-guest THEN  
DO:  
    mess-str = "Merging not for t-guest with active membership card.".   
    RETURN.  
END.  
  
RUN read-cl-memberbl.p (1, t-gastnr, OUTPUT TABLE t-cl-member).  
FIND FIRST t-cl-member NO-ERROR.  
IF AVAILABLE t-cl-member THEN  
DO:     
    mess-str = "Merging not for club member.".     
    RETURN.  
END.  
  
RUN read-bk-veranbl.p (1, t-gastnr, 5, ?, ?, OUTPUT TABLE t-bk-veran).  
FIND FIRST t-bk-veran NO-ERROR.  
IF AVAILABLE t-bk-veran THEN  
DO:  
    mess-str = "Merging not allowed: Active banquet reservation exists.".     
    RETURN.   
END.  
  
IF s-gastnr GT 0 THEN   
DO:   
    IF s-gastnr = t-gastnr THEN   
    DO:   
        mess-str = "The selected t-guest cards must be different to the first.".     
        RETURN.    
    END.  
    RUN read-guestbl.p (1, s-gastnr, "", "", OUTPUT TABLE gast).  
    FIND FIRST gast.  
    IF gast.karteityp NE tg-karteityp THEN   
    DO:   
        mess-str = "The selected t-guest Card Type must have the same.".     
        RETURN.
    END.   
    
    RUN read-guest-prbl.p (1, t-gastnr, "", OUTPUT TABLE t-guest-pr).  
    FIND FIRST t-guest-pr NO-ERROR.  
    flag1 = AVAILABLE t-guest-pr.  
      
    RUN read-guest-prbl.p (1, s-gastnr, "", OUTPUT TABLE t-guest-pr).  
    FIND FIRST t-guest-pr NO-ERROR.  
    flag2 = AVAILABLE t-guest-pr.  
    
    IF flag1 AND flag2 THEN  
    DO:  
        mess-str = "Contract rates exists, Can not merge the cards.".     
        RETURN.
    END.  
      
    RUN read-res-linebl.p (18, ?,?,?,?, "", ?,?, t-gastnr, ?, "", OUTPUT TABLE t-res-line).  
    FIND FIRST t-res-line NO-ERROR.  
    IF AVAILABLE t-res-line THEN  
    DO:  
        mess-str = "GCF to be merged still has active reservation(s)!".     
        RETURN.
    END.  

    RUN gcf-mergebl.p (user-init, t-gastnr, s-gastnr, flag1, flag2).  
    mess-str = "Merged Successfull".
END.   
