DEF TEMP-TABLE t-brief LIKE brief
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER kateg          AS INTEGER. 
DEF OUTPUT PARAMETER kategbezeich   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-brief.

DEFINE VARIABLE kategnr AS INTEGER NO-UNDO.

IF kateg NE ? THEN
    kategnr = kateg + 600.
ELSE kateg = 0.

FIND FIRST paramtext WHERE paramtext.txtnr = (kateg + 600) NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext THEN /*FT serverless*/
    kategbezeich = paramtext.ptexte. 

FOR EACH brief WHERE brief.briefkateg = kateg NO-LOCK BY brief.briefnr:
    CREATE t-brief.
    BUFFER-COPY brief TO t-brief.
    ASSIGN t-brief.rec-id = RECID(brief).
END.
