DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resno           AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinno        AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER error-number   AS INTEGER NO-UNDO INIT 0.
DEF OUTPUT PARAMETER msg-str        AS CHAR    NO-UNDO INIT "".

DEF VAR ci-date AS DATE NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "reservation". 

/*   RUN zugriff-test.p(user-init, 4, 2, OUTPUT zugriff). */
RUN check-in.

PROCEDURE check-in:
  
  RUN htpdate.p(87, OUTPUT ci-date).

  FIND FIRST res-line WHERE res-line.resnr = resno
    AND res-line.reslinnr = reslinno NO-LOCK NO-ERROR.
  
  IF NOT AVAILABLE res-line THEN
  DO:
    msg-str = translateExtended( "Reservation record not yet selected.", lvCAREA, "":U).
    error-number = 1.
    RETURN.
  END.

  IF ((res-line.ankunft NE ci-date) OR (res-line.active-flag NE 0)) THEN
  DO:
    error-number = 2.
    RETURN.
  END.
  
  IF res-line.l-zuordnung[3] = 1 THEN
  DO:
    msg-str = translateExtended ("Check-in function not for accompanying guest.",lvCAREA,"").
    error-number = 3.
    RETURN.
  END.

END. 
