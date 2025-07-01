DEF TEMP-TABLE t-guest LIKE guest.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER gastNo    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER gname     AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER fname     AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-guest.

DEF VARIABLE hHandle AS HANDLE NO-UNDO.
hHandle = THIS-PROCEDURE.

CASE case-type:
  WHEN 1 THEN
  DO:
    IF gastNo > 0 THEN
        FIND FIRST guest WHERE guest.gastnr = gastNo NO-LOCK NO-ERROR.
    ELSE IF gname NE "" THEN
        FIND FIRST guest WHERE guest.NAME = gname AND guest.gastnr > 0 NO-LOCK NO-ERROR.
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST guest WHERE guest.NAME = gname AND 
      (guest.vorname1 + guest.anredefirma) = fname
      AND guest.gastnr GT 0 NO-LOCK NO-ERROR.
  END.
  WHEN 3 THEN
  DO:
    IF gastNo > 0 THEN
    FIND FIRST guest WHERE guest.gastnr = gastNo EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
    ELSE IF gname NE "" THEN
    FIND FIRST guest WHERE guest.NAME = gname AND guest.gastnr > 0 
      EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
  END.
  WHEN 4 THEN
  DO:
    FIND FIRST guest WHERE guest.NAME = gname AND guest.vorname1 = fname
      AND guest.gastnr NE gastNo NO-LOCK NO-ERROR.
  END.
  WHEN 5 THEN
  DO:
    IF fname NE "" THEN
    FIND FIRST guest WHERE guest.NAME = gname 
      AND (guest.vorname1 + guest.anredefirma) = fname
      AND guest.gastnr GT 0 NO-LOCK NO-ERROR.
    ELSE
    FIND FIRST guest WHERE guest.NAME = gname 
      AND guest.gastnr GT 0 NO-LOCK NO-ERROR.
  END.
  WHEN 6 THEN
  DO:
    FIND FIRST guest WHERE guest.NAME = gname AND 
      (guest.vorname1 + guest.anredefirma) = fname
      AND guest.karteityp = gastNo
      AND guest.gastnr GT 0 NO-LOCK NO-ERROR.
  END.
  WHEN 7 THEN
  DO:
      FIND FIRST guest WHERE guest.karteityp GE 1 
      AND guest.gastnr GT gastNo AND guest.firmen-nr GT 0 USE-INDEX 
          typenam_ix NO-LOCK NO-ERROR.
  END.
  WHEN 8 THEN
  DO:
      FIND FIRST guest WHERE guest.karteityp GE 1
      AND guest.gastnr GT gastNo AND guest.steuernr NE "" USE-INDEX 
          typenam_ix NO-LOCK NO-ERROR.
  END.
  WHEN 9 THEN
  DO:
    FIND FIRST guest WHERE guest.name = gname OR 
        (guest.NAME + ", " + guest.anredefirma) = gname NO-LOCK NO-ERROR. 
  END.
  WHEN 10 THEN
  DO:
      FIND LAST guest NO-LOCK NO-ERROR.
  END.
  WHEN 11 THEN
  DO:
      FIND FIRST guest WHERE guest.ausweis-nr1 = gname
          AND guest.karteityp = 0
          AND guest.gastnr GT 0 NO-LOCK NO-ERROR.
  END.
  WHEN 12 THEN
  DO:
      FIND FIRST guest WHERE guest.master-gastnr = gastNo
          AND guest.karteityp = 0
          AND guest.gastnr GT 0 NO-LOCK NO-ERROR.
  END.
  WHEN 13 THEN
  DO:
      FIND FIRST guest WHERE guest.karteityp = 0 NO-LOCK NO-ERROR.
  END.
  WHEN 14 THEN
  DO:
      FIND FIRST guest WHERE guest.nation1 = gname NO-LOCK NO-ERROR.
  END.
  WHEN 15 THEN
  DO:
      FIND FIRST guest WHERE guest.gastnr = gastNo
          AND guest.karteityp GT 0 EXCLUSIVE-LOCK NO-ERROR.
  END.
  WHEN 16 THEN
  DO:
      FIND FIRST bill WHERE bill.rechnr = gastNo NO-ERROR.
      IF NOT AVAILABLE bill THEN RETURN NO-APPLY.
      FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK NO-ERROR.
  END.
  WHEN 17 THEN
  DO:
    FIND FIRST guest WHERE guest.karteityp = 1 AND guest.name = gname 
      AND guest.gastnr NE gastNo AND guest.gastnr GT 0 NO-LOCK NO-ERROR. 
  END.
  WHEN 18 THEN
  DO:
    FIND FIRST guest WHERE guest.karteityp = 2 AND guest.name = gname 
      AND guest.gastnr NE gastNo AND guest.gastnr GT 0 NO-LOCK NO-ERROR. 
  END.

END CASE.

IF AVAILABLE guest THEN
DO:
  CREATE t-guest.
  BUFFER-COPY guest TO t-guest.
END.

PROCEDURE delete-procedure:
    DELETE PROCEDURE hHandle NO-ERROR.
END.

