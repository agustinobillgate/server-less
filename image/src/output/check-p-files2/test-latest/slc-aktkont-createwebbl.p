
DEFINE TEMP-TABLE t-akt-kont1 LIKE akt-kont.
DEFINE TEMP-TABLE t-akt-kont LIKE akt-kont.

DEFINE INPUT PARAMETER gastnr   AS INTEGER.
DEFINE INPUT PARAMETER gname    AS CHARACTER.
DEFINE OUTPUT PARAMETER kontnr  AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-akt-kont1.

DEF VAR curr-gastnr AS INTEGER.  
DEF VAR success-flag AS LOGICAL.

RUN read-akt-kontbl.p(6, gastnr, ?, "", OUTPUT TABLE t-akt-kont).

FIND LAST t-akt-kont NO-ERROR.  
IF AVAILABLE t-akt-kont THEN curr-gastnr = t-akt-kont.kontakt-nr + 1.  
ELSE curr-gastnr = 1.

CREATE t-akt-kont1.
ASSIGN
    t-akt-kont1.gastnr = gastnr   
    t-akt-kont1.kontakt-nr = curr-gastnr  
    t-akt-kont1.name = gname.  
kontnr = t-akt-kont1.kontakt-nr.
