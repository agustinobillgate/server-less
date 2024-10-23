DEFINE TEMP-TABLE t-argt-line      LIKE argt-line.
DEFINE TEMP-TABLE t-arrangement    LIKE arrangement.
DEFINE TEMP-TABLE t-artikel        LIKE artikel.
DEFINE TEMP-TABLE t-hoteldpt       LIKE hoteldpt.
DEFINE TEMP-TABLE artBuff          LIKE artikel.
DEFINE TEMP-TABLE htlBuff          LIKE hoteldpt.

DEFINE TEMP-TABLE t-list
    FIELD arrangement AS CHAR
    FIELD artnr       AS INTEGER
    FIELD bezeich     AS CHAR
    FIELD depart      AS CHAR
    FIELD betrag      AS DECIMAL
    FIELD post-type   AS CHAR
    FIELD inRate      AS LOGICAL
    FIELD pers-type   AS CHAR
    FIELD fixCost     AS LOGICAL
    FIELD argt-artnr  AS INTEGER
    FIELD departement AS INTEGER
    FIELD vt-percnt   AS DECIMAL
  .


DEFINE INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER argtnr          AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "select-argtline". 

DEFINE VARIABLE post-type AS CHAR FORMAT "x(12)" EXTENT 6.
ASSIGN
    post-type[1] = translateExtended("Daily",lvCAREA,"")
    post-type[2] = translateExtended("CI Day",lvCAREA,"")
    post-type[3] = translateExtended("2nd Day",lvCAREA,"")
    post-type[4] = translateExtended("Mon 1st Day",lvCAREA,"")
    post-type[5] = translateExtended("Mon LastDay",lvCAREA,"")
    post-type[6] = translateExtended("Special",lvCAREA,"").
DEFINE VARIABLE pers-type AS CHAR FORMAT "x(6)" EXTENT 3.
ASSIGN
    pers-type[1] = translateExtended("Adult",lvCAREA,"")
    pers-type[2] = translateExtended("Child",lvCAREA,"")
    pers-type[3] = translateExtended("Ch2",lvCAREA,"").


RUN read-arrangementbl.p (1, argtnr, "", OUTPUT TABLE t-arrangement).
FIND FIRST t-arrangement NO-ERROR.
RUN load-argt-linebl.p (argtnr, OUTPUT TABLE t-argt-line).
FIND FIRST t-argt-line NO-ERROR.
DO WHILE AVAILABLE t-argt-line:
    FIND FIRST t-artikel WHERE t-artikel.artnr = t-argt-line.argt-artnr
      AND t-artikel.departement = t-argt-line.departement NO-ERROR.
    IF NOT AVAILABLE t-artikel THEN
    DO:
      RUN read-artikelbl.p (t-argt-line.argt-artnr, t-argt-line.departement, "", 
                            OUTPUT TABLE artBuff).
      FIND FIRST artBuff NO-ERROR.
      CREATE t-artikel.
      BUFFER-COPY artBuff TO t-artikel.
    END.
    FIND FIRST t-hoteldpt WHERE t-hoteldpt.num = t-argt-line.departement
        NO-ERROR.
    IF NOT AVAILABLE t-hoteldpt THEN
    DO:
      RUN read-hoteldptbl.p (t-argt-line.departement, OUTPUT TABLE htlBuff).
      FIND FIRST htlBuff NO-ERROR.
      CREATE t-hoteldpt.
      BUFFER-COPY htlBuff TO t-hoteldpt.
    END.
    FIND NEXT t-argt-line NO-ERROR.
END.


FOR EACH t-argt-line, 
  FIRST t-arrangement WHERE t-arrangement.argtnr = t-argt-line.argtnr, 
  FIRST t-artikel WHERE t-artikel.artnr = t-argt-line.argt-artnr 
   AND t-artikel.departement = t-argt-line.departement, 
  FIRST t-hoteldpt WHERE t-hoteldpt.num = t-artikel.departement BY t-argt-line.argt-artnr:

    CREATE t-list.
    ASSIGN
          t-list.arrangement    = t-arrangement.arrangement
          t-list.artnr          = t-artikel.artnr     
          t-list.bezeich        = t-artikel.bezeich     
          t-list.depart         = t-hoteldpt.depart      
          t-list.betrag         = t-argt-line.betrag      
          t-list.post-type      = post-type[t-argt-line.fakt-modus]
          t-list.inrate         = LOGICAL(t-argt-line.kind1)
          t-list.pers-type      = pers-type[INTEGER(t-argt-line.vt-percnt) + 1]
          t-list.fixCost        = t-argt-line.kind2
          t-list.argt-artnr     = t-argt-line.argt-artnr
          t-list.departement    = t-argt-line.departement
          t-list.vt-percnt      = t-argt-line.vt-percnt
       .
END.

