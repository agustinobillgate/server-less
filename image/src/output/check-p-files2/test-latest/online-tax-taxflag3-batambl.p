

DEF TEMP-TABLE online-tax
    FIELD line-nr   AS INTEGER
    FIELD ct        AS CHAR
    FIELD departement AS INTEGER
.

DEFINE INPUT PARAMETER curr-date     AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER already-read AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR online-tax.
DEFINE OUTPUT PARAMETER avail-flag   AS LOGICAL NO-UNDO.   
     
  RUN read-onlinetax.p(curr-date, OUTPUT already-read, OUTPUT TABLE online-tax).
  FIND FIRST online-tax NO-ERROR.
  IF NOT AVAILABLE online-tax THEN 
  DO: 
      RUN delete-onlinetaxbl.p(curr-date,curr-date).
      RUN nt-onlinetax-batam-billdate-manual.p(curr-date, curr-date, OUTPUT avail-flag).
      RUN if-read-onlinetax-mbl.p(curr-date).
      RUN read-onlinetax.p(curr-date, OUTPUT already-read, OUTPUT TABLE online-tax).
      FIND FIRST online-tax NO-ERROR.
      IF NOT AVAILABLE online-tax THEN RETURN.
  END.

