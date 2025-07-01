DEF INPUT PARAMETER inp-resNo AS INTEGER            NO-UNDO.
DEF OUTPUT PARAMETER reslinNo AS INTEGER INITIAL 1  NO-UNDO.
    
FOR EACH res-line WHERE res-line.resnr = inp-resNo NO-LOCK BY res-line.reslinnr
  DESCENDING:
  reslinNo = res-line.reslinnr + 1.
  LEAVE.
END.
