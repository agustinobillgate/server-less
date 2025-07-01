DEFINE TEMP-TABLE htp-list 
  FIELD nr      AS INTEGER  FORMAT ">,>>9" 
  FIELD fchar   AS CHAR     FORMAT "x(16)" 
  FIELD bezeich AS CHAR     FORMAT "x(44)". 

DEF INPUT  PARAMETER briefnr    AS INTEGER.
DEF OUTPUT PARAMETER word-exist AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER efield     AS CHAR INIT NO.
DEF OUTPUT PARAMETER ebuffer    AS CHAR INIT NO.
DEF OUTPUT PARAMETER sms-kateg  AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR htp-list.

DEFINE VARIABLE gl-nr   AS INTEGER              NO-UNDO. 
DEFINE VARIABLE gl-file AS LOGICAL INITIAL NO   NO-UNDO. 

RUN create-list.
RUN fill-words.

FIND FIRST htparam WHERE htparam.paramnr = 839 NO-LOCK.
sms-kateg = htparam.finteger.


/*MT
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
      AND htparam.paramnr NE 2030 NO-LOCK BY htparam.reihenfolge:
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
    FOR EACH htparam WHERE htparam.paramgruppe = 17 NO-LOCK BY htparam.reihenfolge: 
      create htp-list. 
      htp-list.nr = htparam.paramnr. 
      htp-list.fchar = keychar + htparam.fchar. 
      htp-list.bezeich = htparam.bezeich. 
    END. 
  END. 
END. 
*/

PROCEDURE create-list: 
DEFINE VARIABLE keychar AS CHAR. 
  FIND FIRST htparam WHERE paramnr = 987 NO-LOCK. 
  gl-nr = htparam.finteger. 
  FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK NO-ERROR.
  IF NOT AVAILABLE brief THEN RETURN.
 
  FIND FIRST htparam WHERE htparam.paramnr = 600 NO-LOCK. 
  keychar = htparam.fchar. 
  IF brief.briefkateg = gl-nr THEN 
  DO: 
    gl-file = YES. 
    FOR EACH htparam WHERE htparam.paramgruppe = 39 
      AND htparam.paramnr NE 2030 NO-LOCK BY htparam.reihenfolge: 
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
    FOR EACH htparam WHERE htparam.paramgruppe = 17 NO-LOCK BY htparam.reihenfolge: 
      create htp-list. 
      htp-list.nr = htparam.paramnr. 
      htp-list.fchar = keychar + htparam.fchar. 
      htp-list.bezeich = htparam.bezeich. 
    END. 
    /*FT add word key*/
    CREATE htp-list.
    ASSIGN 
      htp-list.nr = 9999 
      htp-list.fchar = keychar + "supp1"
      htp-list.bezeich = "Supplier1(P/R)". 
    CREATE htp-list.
    ASSIGN 
      htp-list.nr = 9998 
      htp-list.fchar = keychar + "supp2"
      htp-list.bezeich = "Supplier2(P/R)". 
    CREATE htp-list.
    ASSIGN 
      htp-list.nr = 9997 
      htp-list.fchar = keychar + "supp3"
      htp-list.bezeich = "Supplier3(P/R)". 
    CREATE htp-list.
    ASSIGN 
      htp-list.nr = 9996 
      htp-list.fchar = keychar + "du-price2"
      htp-list.bezeich = "DU-Price2(P/R)". 
    CREATE htp-list.
    ASSIGN 
      htp-list.nr = 9995 
      htp-list.fchar = keychar + "du-price3"
      htp-list.bezeich = "DU-Price3(P/R)". 
    CREATE htp-list.
    ASSIGN 
      htp-list.nr = 9994 
      htp-list.fchar = keychar + "cont"
      htp-list.bezeich = "Content Article(P/R)". 
    CREATE htp-list.
    ASSIGN 
      htp-list.nr = 9993 
      htp-list.fchar = keychar + "t-amount"
      htp-list.bezeich = "Total Amount(P/R)". 
    CREATE htp-list.
    ASSIGN 
      htp-list.nr = 9992 
      htp-list.fchar = keychar + "Supps"
      htp-list.bezeich = "Supplier Selected(P/R)". 
    CREATE htp-list.
    ASSIGN 
      htp-list.nr = 9991 
      htp-list.fchar = keychar + "du-price1"
      htp-list.bezeich = "DU-Price1(P/R)". 
  END. 
END. 

PROCEDURE fill-words: 
  FIND FIRST briefzei WHERE briefzei.briefnr = briefnr
      AND briefzei.briefzeilnr = 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE briefzei THEN 
  DO:
    word-exist  = YES.
    efield = briefzei.texte.
    ebuffer = briefzei.texte.
  END.
END.
