.
DEF TEMP-TABLE p-list LIKE argt-line.

DEF INPUT PARAMETER icase           AS INTEGER NO-UNDO.
DEF INPUT-OUTPUT PARAMETER s-recid  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER argtnr          AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resnr           AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinnr        AS INTEGER NO-UNDO.
DEF INPUT PARAMETER ch1-betrag      AS DECIMAL NO-UNDO.
DEF INPUT PARAMETER ch2-betrag      AS DECIMAL NO-UNDO.
DEF INPUT PARAMETER from-date       AS DATE NO-UNDO.
DEF INPUT PARAMETER to-date         AS DATE NO-UNDO.
DEF INPUT PARAMETER vt-percnt       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER TABLE FOR p-list.

FIND FIRST p-list.

CASE icase:
    WHEN 1 THEN RUN add-argt.
    WHEN 2 THEN RUN chg-argt.
    WHEN 3 THEN RUN del-argt.
END CASE.

PROCEDURE add-argt:
  CREATE reslin-queasy.
  ASSIGN
    reslin-queasy.KEY       = "fargt-line"
    reslin-queasy.number1   = p-list.departement
    reslin-queasy.number2   = argtnr
    reslin-queasy.number3   = p-list.argt-artnr
    reslin-queasy.resnr     = resnr
    reslin-queasy.reslinnr  = reslinnr
    reslin-queasy.deci1     = p-list.betrag
    reslin-queasy.deci2     = ch1-betrag
    reslin-queasy.deci3     = ch2-betrag
    reslin-queasy.date1     = from-date
    reslin-queasy.date2     = to-date
    reslin-queasy.char2     = STRING(p-list.vt-percnt).
  FIND CURRENT reslin-queasy NO-LOCK.
  s-recid = INTEGER(RECID(reslin-queasy)).
END.

PROCEDURE chg-argt:
  FIND FIRST reslin-queasy WHERE RECID(reslin-queasy) = s-recid NO-LOCK NO-ERROR.
  IF AVAILABLE reslin-queasy THEN DO:
      FIND CURRENT reslin-queasy EXCLUSIVE-LOCK.
      ASSIGN
        reslin-queasy.deci1 = p-list.betrag
        reslin-queasy.deci2 = ch1-betrag
        reslin-queasy.deci3 = ch2-betrag
        reslin-queasy.date1 = from-date
        reslin-queasy.date2 = to-date
        reslin-queasy.char2 = STRING(p-list.vt-percnt).
      FIND CURRENT reslin-queasy NO-LOCK.
      RELEASE reslin-queasy.
  END.
END.

PROCEDURE del-argt:
  FIND FIRST reslin-queasy WHERE RECID(reslin-queasy) = s-recid NO-LOCK NO-ERROR.
  IF AVAILABLE reslin-queasy THEN DO:
      FIND CURRENT reslin-queasy EXCLUSIVE-LOCK.
      DELETE reslin-queasy.
      RELEASE reslin-queasy.
  END.
END.
