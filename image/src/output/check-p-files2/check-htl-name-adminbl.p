DEF TEMP-TABLE t-list
    FIELD htl-name  AS CHAR
    FIELD htl-adr1  AS CHAR
    FIELD htl-adr2  AS CHAR
    FIELD htl-adr3  AS CHAR
    FIELD htl-tel   AS CHAR
    FIELD htl-fax   AS CHAR
    FIELD htl-email AS CHAR.

DEF OUTPUT PARAMETER flag AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-list.

FIND FIRST htparam WHERE paramnr = 996 no-lock.   /* VHP Front multi user */ 
IF NOT htparam.flogical THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 1015 no-lock.   /* VHP Lite */ 
  IF NOT htparam.flogical THEN 
  DO: 
    FIND FIRST htparam WHERE paramnr = 990 no-lock.   /* Rest License */ 
    IF htparam.flogical THEN flag = YES.
  END. 
END.
CREATE t-list.
RUN fill-list.



PROCEDURE fill-list: 
  FIND FIRST paramtext WHERE txtnr = 200 NO-LOCK. 
  t-list.htl-name = paramtext.ptexte. 
  FIND FIRST paramtext WHERE txtnr = 201 NO-LOCK. 
  t-list.htl-adr1 = paramtext.ptexte. 
  FIND FIRST paramtext WHERE txtnr = 202 NO-LOCK. 
  t-list.htl-adr2 = paramtext.ptexte. 
  FIND FIRST paramtext WHERE txtnr = 203 NO-LOCK. 
  t-list.htl-adr3 = paramtext.ptexte. 
  FIND FIRST paramtext WHERE txtnr = 204 NO-LOCK. 
  t-list.htl-tel = paramtext.ptexte. 
  FIND FIRST paramtext WHERE txtnr = 205 NO-LOCK. 
  t-list.htl-fax = paramtext.ptexte. 
  FIND FIRST paramtext WHERE txtnr = 206 NO-LOCK. 
  t-list.htl-email = paramtext.ptexte.
END. 
