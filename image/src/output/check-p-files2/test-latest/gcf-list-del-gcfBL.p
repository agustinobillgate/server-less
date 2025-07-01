
DEF INPUT PARAMETER i-case      AS INTEGER          NO-UNDO.  
DEF INPUT PARAMETER pvILanguage AS INTEGER          NO-UNDO.  
DEF INPUT PARAMETER gastno      AS INTEGER          NO-UNDO.  
DEF INPUT PARAMETER user-init   AS CHAR             NO-UNDO.  
DEF OUTPUT PARAMETER msg-str    AS CHAR INIT ""     NO-UNDO.  
DEF OUTPUT PARAMETER error-flag AS LOGICAL INIT YES NO-UNDO.  
  
DEF VAR zugriff     AS LOGICAL  NO-UNDO.  
DEF VAR error-code  AS INTEGER  NO-UNDO.  
  
{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "gcf-list".   
    
FIND FIRST guest WHERE guest.gastnr = gastno NO-LOCK.
IF NOT AVAILABLE guest THEN
DO:
    msg-str = translateExtended ("The guest no longer available",lvCAREA,"").
    RETURN.
END.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.  
  
IF i-case = 1 THEN  
DO:  
  IF guest.anlage-datum = TODAY THEN   
    zugriff = SUBSTR(bediener.permission, 2, 1) GE "2".  
  ELSE zugriff = SUBSTR(bediener.permission, 2, 1) GE "3".  
  IF NOT zugriff THEN  
  DO:  
    IF guest.anlage-datum = TODAY THEN   
      msg-str = translateExtended ("No User Access Right [2,2]",lvCAREA,"").  
    ELSE  
      msg-str = translateExtended ("No User Access Right [2,3]",lvCAREA,"").  
    RETURN.  
  END.  
  
  msg-str = "&Q"  
    + translateExtended( "Do you really want to delete the guestcard: ", lvCAREA, "":U)   
    + CAPS(guest.name) + " ?".  
  error-flag = NO.  

  RETURN.  
END.  
  
RUN del-gcfbl.p(INPUT guest.gastnr, OUTPUT error-code).   

IF error-code = 0 THEN   
DO:  
  msg-str = translateExtended( "Guestcard deleted.", lvCAREA, "":U).  
  error-flag = NO.  
END.  
ELSE IF error-code = 1 THEN   
   msg-str = translateExtended( "Reservation record exists, deletion not possible.", lvCAREA,"").  
      
ELSE IF error-code = 2 THEN   
  msg-str = translateExtended( "Debt record exists, deletion not possible.",lvCAREA,"").  
      
ELSE IF error-code = 3 THEN   
DO:   
DEF BUFFER guest1 FOR guest.  
  FIND FIRST guest1 WHERE guest1.master-gastnr = guest.gastnr NO-LOCK.   
  msg-str = translateExtended( "The file is currently used as Master-file of the guest file ",   
        lvCAREA, "":U) +  
        caps(guest1.name) + ", " + caps(guest1.vorname1) + " " +   
        caps(guest1.anredefirma) + caps(guest1.anrede1)   
        + CHR(10)  
        + translateExtended( "Deletion not possible.", lvCAREA, "":U).  
END.   
      
ELSE IF error-code = 4 THEN   
  msg-str = translateExtended( "Sales customer record exists, deletion not possible.",lvCAREA, "":U).   
      
ELSE IF error-code = 5 THEN   
  msg-str = translateExtended( "Bill record exists, deletion not possible.",lvCAREA, "":U).  
      
ELSE IF error-code = 6 THEN   
  msg-str =translateExtended( "Allotment record exists, deletion not possible.",lvCAREA, "":U).  
      
ELSE IF error-code = 7 THEN   
  msg-str =translateExtended( "Condo unit exists, deletion not possible.",lvCAREA,"":U).  
      
ELSE IF error-code = 8 THEN   
  msg-str = translateExtended( "Banquet reservation exists, deletion not possible.", lvCAREA, "":U).  
      
ELSE IF error-code = 9 THEN   
  msg-str = translateExtended( "Member Card exists, deletion not possible.",lvCAREA, "":U).  
      
ELSE IF error-code = 10 THEN   
  msg-str = translateExtended( "Sport Club Member exists, deletion not possible.",lvCAREA, "":U).  
      
ELSE IF error-code = 11 THEN   
DO:   
DEF VAR gname AS CHAR INITIAL "" NO-UNDO.  
DEF BUFFER gbuff FOR guest.  
  FIND FIRST akt-kont WHERE akt-kont.betrieb-gast = guest.gastnr NO-LOCK.  
  FIND FIRST gbuff WHERE gbuff.gastnr = akt-kont.gastnr NO-LOCK NO-ERROR.  
  IF AVAILABLE gbuff THEN gname = gbuff.NAME.  
  msg-str = translateExtended( "Name contact using guest's GcfNO exists, deletion not possible.",lvCAREA, "":U)   
          + CHR(10)  
          + translateExtended ("Please check names contact list under:",lvCAREA,"") + " " + gname.  
END.
/*IF 080319 - Add validation for deleting Dummy Guest Card for OTA in paramnr 615 requested by Faisal*/
ELSE IF error-code EQ 12 THEN 
DO:    
    msg-str = translateExtended("Deleting Guest Card Not Possible", lvCAREA, "").
    error-flag = YES.
END.
/*END IF*/  
