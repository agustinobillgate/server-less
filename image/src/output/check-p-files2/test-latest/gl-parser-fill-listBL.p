DEFINE TEMP-TABLE t-brief
  FIELD briefnr LIKE brief.briefnr.
DEFINE TEMP-TABLE t-gl-department
    FIELD nr LIKE gl-department.nr
    FIELD bezeich LIKE gl-department.bezeich.
DEFINE TEMP-TABLE t-gl-acct
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD deptnr    LIKE gl-acct.deptnr
    FIELD bezeich   LIKE gl-acct.bezeich
    FIELD main-nr   LIKE gl-acct.main-nr
    
    FIELD acc-type  LIKE gl-acct.acc-type
    FIELD actual    LIKE gl-acct.actual
    FIELD budget    LIKE gl-acct.budget
    FIELD last-yr   LIKE gl-acct.last-yr
    FIELD ly-budget LIKE gl-acct.ly-budget.
DEFINE TEMP-TABLE t-gl-main
    FIELD nr      LIKE gl-main.nr
    FIELD code    LIKE gl-main.code
    FIELD bezeich LIKE gl-main.bezeich.
DEFINE TEMP-TABLE brief-list 
  FIELD b-text AS CHAR. 
DEFINE TEMP-TABLE htp-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar AS CHAR. 
DEFINE TEMP-TABLE htv-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar AS CHAR.
DEFINE TEMP-TABLE t-briefzei
    FIELD briefnr LIKE briefzei.briefnr
    FIELD briefzeilnr LIKE briefzei.briefzeilnr
    FIELD texte LIKE briefzei.texte.


DEF INPUT  PARAMETER briefnr AS INT.
DEF OUTPUT PARAMETER keycmd  AS CHAR.
DEF OUTPUT PARAMETER keyvar  AS CHAR.
DEF OUTPUT PARAMETER keycont AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR htv-list.
DEF OUTPUT PARAMETER TABLE FOR htp-list.
DEF OUTPUT PARAMETER TABLE FOR brief-list.
DEF OUTPUT PARAMETER TABLE FOR t-brief.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.
DEF OUTPUT PARAMETER TABLE FOR t-gl-department.
DEF OUTPUT PARAMETER TABLE FOR t-gl-main.
DEF OUTPUT PARAMETER TABLE FOR t-briefzei.

DEF VAR i AS INT.
RUN fill-list.
FOR EACH brief:
    CREATE t-brief.
    ASSIGN t-brief.briefnr = brief.briefnr.
END.

FOR EACH gl-acct:
    CREATE t-gl-acct.
    ASSIGN t-gl-acct.fibukonto = gl-acct.fibukonto
           t-gl-acct.deptnr    = gl-acct.deptnr
           t-gl-acct.bezeich   = gl-acct.bezeich
           t-gl-acct.main-nr   = gl-acct.main-nr
           t-gl-acct.acc-type  = gl-acct.acc-type.

    DO i = 1 TO 12:
        ASSIGN
        t-gl-acct.actual[i]    = gl-acct.actual[i]
        t-gl-acct.budget[i]    = gl-acct.budget[i]
        t-gl-acct.last-yr[i]   = gl-acct.last-yr[i]
        t-gl-acct.ly-budget[i] = gl-acct.ly-budget[i].
        i = i + 1.
    END.
END.
FOR EACH gl-main:
    CREATE t-gl-main.
    ASSIGN
      t-gl-main.nr      = gl-main.nr
      t-gl-main.code    = gl-main.code
      t-gl-main.bezeich = gl-main.bezeich.
END.
FOR EACH gl-department:
    CREATE t-gl-department.
    ASSIGN
    t-gl-department.nr      = gl-department.nr
    t-gl-department.bezeich = gl-department.bezeich.
END.

FOR EACH briefzei WHERE briefzei.briefnr = briefnr:
    CREATE t-briefzei.
    ASSIGN
      t-briefzei.briefnr = briefzei.briefnr
      t-briefzei.briefzeilnr = briefzei.briefzeilnr
      t-briefzei.texte = briefzei.texte.
END.


PROCEDURE fill-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE l AS INTEGER. 
DEFINE VARIABLE continued AS LOGICAL INITIAL NO. 
 
  FIND FIRST htparam WHERE paramnr = 600 NO-LOCK. 
  keycmd = htparam.fchar. 
  FIND FIRST htparam WHERE paramnr = 2030 NO-LOCK. 
  keyvar = htparam.fchar. 
  FIND FIRST htparam WHERE paramnr = 1122 NO-LOCK. 
  keycont = keycmd + htparam.fchar. 
 
  FOR EACH htparam WHERE paramgruppe = 39 
    AND htparam.paramnr NE 2030 NO-LOCK BY LENGTH(htparam.fchar) descending: 
     IF SUBSTR(htparam.fchar,1 ,1) = "." THEN 
     DO: 
       create htv-list. 
       htv-list.paramnr = htparam.paramnr. 
       htv-list.fchar = htparam.fchar. 
     END. 
     ELSE 
     DO: 
       create htp-list. 
       htp-list.paramnr = htparam.paramnr. 
       htp-list.fchar = keycmd + htparam.fchar. 
     END. 
  END. 
 
  DO: 
    FOR EACH briefzei WHERE briefzei.briefnr = briefnr NO-LOCK BY briefzei.briefzeilnr: 
      j = 1. 
      DO i = 1 TO LENGTH(briefzei.texte): 
         IF asc(SUBSTR(briefzei.texte, i , 1)) EQ 10 THEN 
         DO: 
           n = i - j. 
           c = SUBSTR(briefzei.texte, j,  n). 
           l = LENGTH(c). 
           IF NOT continued THEN create brief-list. 
           brief-list.b-text = brief-list.b-text + c. 
           j = i + 1. 
           IF l GT LENGTH(keycont) AND 
             SUBSTR(c, l - LENGTH(keycont) + 1, LENGTH(keycont)) = keycont THEN 
           DO: 
             continued = YES. 
             brief-list.b-text = SUBSTR(brief-list.b-text, 1, 
               LENGTH(brief-list.b-text) - LENGTH(keycont)). 
           END. 
           ELSE continued = NO. 
         END. 
      END. 
      n = LENGTH(briefzei.texte) - j + 1. 
      c = SUBSTR(briefzei.texte, j,  n). 
      IF NOT continued THEN create brief-list. 
      brief-list.b-text = brief-list.b-text + c. 
    END. 
  END. 
END. 

