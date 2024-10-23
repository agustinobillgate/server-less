DEFINE TEMP-TABLE htp-list 
  FIELD nr AS INTEGER FORMAT ">,>>9" 
  FIELD fchar AS CHAR FORMAT "x(16)" 
  FIELD bezeich AS CHAR FORMAT "x(44)". 

DEF TEMP-TABLE t-briefzei LIKE briefzei.

DEFINE INPUT PARAMETER briefnr AS INTEGER.
DEF OUTPUT PARAMETER gl-file AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR htp-list.
DEF OUTPUT PARAMETER TABLE FOR t-briefzei.

DEFINE VARIABLE gl-nr AS INTEGER. 
RUN create-list.
FOR EACH briefzei:
    CREATE t-briefzei.
    BUFFER-COPY briefzei TO t-briefzei.
END.


PROCEDURE create-list: 
DEFINE VARIABLE keychar AS CHAR. 
  FIND FIRST htparam WHERE paramnr = 987 NO-LOCK. 
  gl-nr = htparam.finteger. 
  FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 600 NO-LOCK. 
  keychar = htparam.fchar. 
  IF brief.briefkateg = gl-nr THEN 
  DO: 
    gl-file = YES. 
    FOR EACH htparam WHERE htparam.paramgruppe = 39 
      AND htparam.paramnr NE 2030 NO-LOCK 
/*   BY htparam.reihenfolge: */ 
      BY htparam.fchar: 
      create htp-list. 
      htp-list.nr = htparam.paramnr. 
      IF SUBSTR(htparam.fchar, 1, 1) = "." THEN 
      htp-list.fchar = htparam.fchar. 
      ELSE htp-list.fchar = keychar + htparam.fchar. 
      htp-list.bezeich = htparam.bezeich. 
    END. 
  END. 
  ELSE 
  DO: 
    FOR EACH htparam WHERE htparam.paramgruppe = 17 NO-LOCK 
      BY htparam.reihenfolge: 
      create htp-list. 
      htp-list.nr = htparam.paramnr. 
      htp-list.fchar = keychar + htparam.fchar. 
      htp-list.bezeich = htparam.bezeich. 
    END. 
  END. 
END. 
