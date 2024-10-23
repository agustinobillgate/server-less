DEFINE TEMP-TABLE obuff 
  FIELD srecid AS INTEGER 
  FIELD remark AS CHAR FORMAT "x(32)" LABEL "Remark"
.
DEF INPUT PARAMETER TABLE FOR obuff.

FOR EACH obuff WHERE obuff.srecid NE 0:
    FIND FIRST l-kredit WHERE RECID(l-kredit) = obuff.srecid EXCLUSIVE-LOCK.
    ASSIGN l-kredit.bemerk = obuff.remark.
    FIND CURRENT l-kredit NO-LOCK.
END.
