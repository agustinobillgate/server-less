

DEFINE TEMP-TABLE htp-list 
  FIELD nr      AS INTEGER FORMAT ">,>>9" 
  FIELD fchar   AS CHAR FORMAT "x(16)" 
  FIELD bezeich AS CHAR FORMAT "x(44)". 

DEF TEMP-TABLE t-briefzei LIKE briefzei.

DEF INPUT PARAMETER briefnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-briefzei.
DEF OUTPUT PARAMETER TABLE FOR htp-list.

RUN create-list. 
RUN fill-words. 


PROCEDURE create-list: 
DEFINE VARIABLE keychar AS CHAR. 
  FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 600 NO-LOCK. 
  keychar = htparam.fchar. 
  FOR EACH htparam WHERE htparam.paramgruppe = 8 
    AND htparam.bezeich NE "Not Used" NO-LOCK BY htparam.fchar: 
    create htp-list. 
    htp-list.nr = htparam.paramnr. 
    IF SUBSTR(htparam.fchar, 1, 1) = "." THEN 
    htp-list.fchar = htparam.fchar. 
    ELSE htp-list.fchar = keychar + htparam.fchar. 
    htp-list.bezeich = htparam.bezeich. 
  END. 

  CREATE htp-list.
  ASSIGN
      htp-list.nr = 9092
      htp-list.fchar   = keychar + "SourceRev"
      htp-list.bezeich = "Logding Revenue of selected Source"
      .
  CREATE htp-list.
  ASSIGN
      htp-list.nr = 9813
      htp-list.fchar   = keychar + "SourceRoom"
      htp-list.bezeich = "Rooms of selected Source"
      .
  CREATE htp-list.
  ASSIGN
      htp-list.nr = 9814
      htp-list.fchar   = keychar + "SourcePers"
      htp-list.bezeich = "Number of Pax of selected Source"
      .

END. 
 
PROCEDURE fill-words: 
  FOR EACH briefzei WHERE briefzei.briefnr = briefnr NO-LOCK
      BY briefzei.briefzeilnr:
      CREATE t-briefzei.
      BUFFER-COPY briefzei TO t-briefzei.
  END.
END. 
