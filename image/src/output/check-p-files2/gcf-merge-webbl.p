DEFINE TEMP-TABLE tlist
    FIELD gastno AS INTEGER.


DEF TEMP-TABLE t-mc-guest   LIKE mc-guest.  
DEF TEMP-TABLE t-cl-member  LIKE cl-member. 
DEF TEMP-TABLE t-bk-veran   LIKE bk-veran.  
DEF TEMP-TABLE t-guest-pr   LIKE guest-pr.  


DEFINE INPUT PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER userinit       AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER bgastno        AS INTEGER NO-UNDO. /*tujuan merge*/
DEFINE INPUT PARAMETER TABLE FOR tlist. /*yang akan dimerge*/

DEFINE OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER msg-str      AS CHAR    NO-UNDO INIT "".

DEFINE VARIABLE doit AS LOGICAL.
DEFINE VARIABLE flag1 AS LOGICAL.   
DEFINE VARIABLE flag2 AS LOGICAL.   

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gcf-merge-web".


FOR EACH tlist NO-LOCK:
      
  ASSIGN doit = YES.

  RUN read-mc-guestbl.p(1, tlist.gastno, "", OUTPUT TABLE t-mc-guest).  
  FIND FIRST t-mc-guest NO-ERROR.  
  IF AVAILABLE t-mc-guest THEN 
      ASSIGN doit       = NO
             msg-str    = translateExtended ("Merging not for t-guest with active membership card.",lvCAREA,"").
    
  IF doit THEN DO:
      RUN read-cl-memberbl.p(1, tlist.gastno, OUTPUT TABLE t-cl-member).  
      FIND FIRST t-cl-member NO-ERROR.  
      IF AVAILABLE t-cl-member THEN 
          ASSIGN doit       = NO
                 msg-str    = translateExtended ("Merging not for club member.",lvCAREA,"")                 
           .
  END.

  IF doit THEN DO:  
      RUN read-bk-veranbl.p(1, tlist.gastno, 5, ?, ?, OUTPUT TABLE t-bk-veran).  
      FIND FIRST t-bk-veran NO-ERROR.  
      IF AVAILABLE t-bk-veran THEN 
          ASSIGN doit     = NO
                 msg-str  = translateExtended ("Merging not allowed: Active banquet reservation exists.",lvCAREA,"")                  
         .
  END.  

  IF doit THEN DO:
        RUN read-guest-prbl.p(1, tlist.gastno, "", OUTPUT TABLE t-guest-pr).  
        FIND FIRST t-guest-pr NO-ERROR.  
        flag1 = AVAILABLE t-guest-pr.  
        RUN read-guest-prbl.p(1, bgastno, "", OUTPUT TABLE t-guest-pr).  
        FIND FIRST t-guest-pr NO-ERROR.  
        flag2 = AVAILABLE t-guest-pr.  
        IF flag1 AND flag2 THEN 
            ASSIGN doit = NO
                   msg-str  = translateExtended( "Contract rates exists, Can not merge the cards.",lvCAREA, "":U)   
                .
  END.

  IF doit = NO THEN LEAVE.

  IF doit THEN DO:
      RUN gcf-mergebl.p(userinit, tlist.gastno, bgastno, flag1, flag2).     
      ASSIGN success-flag = YES.
  END.
END.
