
DEF TEMP-TABLE online-tax
    FIELD line-nr   AS INTEGER
    FIELD ct        AS CHAR
    FIELD departement AS INTEGER
.

DEFINE INPUT PARAMETER curr-date     AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER taxflag       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER include-flag  AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER already-read AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR online-tax.
DEFINE OUTPUT PARAMETER avail-flag   AS LOGICAL NO-UNDO.   
     
  MESSAGE "1" VIEW-AS ALERT-BOX INFO.
  RUN read-onlinetax.p(curr-date, OUTPUT already-read, OUTPUT TABLE online-tax).
  /*FIND FIRST online-tax NO-ERROR.
  IF NOT AVAILABLE online-tax THEN */
  DO: 
       MESSAGE "2" VIEW-AS ALERT-BOX INFO.
      RUN delete-onlinetaxbl.p(curr-date,curr-date).
      RUN nt-onlinetax-sby-billdate-manual_1.p(curr-date, curr-date, taxflag, include-flag, 
                                               OUTPUT avail-flag).
       MESSAGE "3" VIEW-AS ALERT-BOX INFO.
      RUN if-read-onlinetax-mbl.p(curr-date).
      RUN read-onlinetax.p(curr-date, OUTPUT already-read, OUTPUT TABLE online-tax).
       MESSAGE "4" VIEW-AS ALERT-BOX INFO.
      FIND FIRST online-tax NO-ERROR.
      IF NOT AVAILABLE online-tax THEN RETURN.
       MESSAGE "5" VIEW-AS ALERT-BOX INFO.
  END.
