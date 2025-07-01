DEFINE TEMP-TABLE t-brief LIKE brief
    FIELD efield AS CHARACTER.

DEFINE INPUT PARAMETER briefnr AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-brief.

FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK NO-ERROR.
IF AVAILABLE brief THEN
DO:
   CREATE t-brief.
   BUFFER-COPY brief TO t-brief.
   FIND FIRST briefzei WHERE briefzei.briefnr = briefnr
      AND briefzei.briefzeilnr = 1 NO-LOCK NO-ERROR. 
   IF AVAILABLE briefzei THEN t-brief.efield = briefzei.texte.
END.
