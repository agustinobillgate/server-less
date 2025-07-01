DEFINE TEMP-TABLE language-list
  FIELD lang-num        AS INTEGER
  FIELD lang-id         AS CHARACTER
  FIELD lang-default    AS CHARACTER
  FIELD lang-other      AS CHARACTER
.
DEFINE TEMP-TABLE article-list
  FIELD art-department  AS INTEGER
  FIELD art-recid       AS INTEGER
  FIELD art-number      AS INTEGER
  FIELD art-name        AS CHARACTER
  FIELD art-group       AS INTEGER
  FIELD art-subgrp      AS INTEGER
  FIELD art-group-str   AS CHARACTER
  FIELD art-subgrp-str  AS CHARACTER
  FIELD art-desc        AS CHARACTER
  FIELD art-price       AS DECIMAL
  FIELD art-image       AS CHARACTER
  FIELD art-active-flag AS LOGICAL  
    .
DEFINE TEMP-TABLE carousel-list
  FIELD carousel-recid  AS INTEGER
  FIELD carousel-dept   AS INTEGER
  FIELD carousel-num    AS INTEGER
  FIELD carousel-title  AS CHARACTER
  FIELD carousel-desc   AS CHARACTER
  FIELD carousel-image  AS CHARACTER
.
DEFINE TEMP-TABLE maingroup-list
    FIELD maingrp-no AS INT
    FIELD maingrp-description AS CHAR.

DEFINE TEMP-TABLE subgroup-list
    FIELD subgrp-no          AS INT
    FIELD subgrp-description AS CHAR.

DEFINE INPUT PARAMETER outlet-no        AS INTEGER.
DEFINE OUTPUT PARAMETER user-init       AS CHARACTER.
DEFINE OUTPUT PARAMETER font-color      AS CHARACTER.
DEFINE OUTPUT PARAMETER bg-color        AS CHARACTER.
DEFINE OUTPUT PARAMETER outlet-name     AS CHARACTER.
DEFINE OUTPUT PARAMETER hotel-name      AS CHARACTER.
DEFINE OUTPUT PARAMETER image-logo      AS CHARACTER.
DEFINE OUTPUT PARAMETER image-food      AS CHARACTER.
DEFINE OUTPUT PARAMETER image-bev       AS CHARACTER.
DEFINE OUTPUT PARAMETER image-other     AS CHARACTER.
DEFINE OUTPUT PARAMETER mess-result     AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR language-list.
DEFINE OUTPUT PARAMETER TABLE FOR article-list.
DEFINE OUTPUT PARAMETER TABLE FOR carousel-list.
DEFINE OUTPUT PARAMETER TABLE FOR subgroup-list.
DEFINE OUTPUT PARAMETER TABLE FOR maingroup-list.
/*********************************************************************************************/
FOR EACH article-list:
    DELETE article-list.
END.
FOR EACH maingroup-list:
    DELETE maingroup-list.
END.
FOR EACH subgroup-list:
    DELETE subgroup-list.
END.

FOR EACH wgrpdep WHERE wgrpdep.departement = outlet-no 
    NO-LOCK BY wgrpdep.betriebsnr DESCENDING BY wgrpdep.zknr:
    CREATE subgroup-list.
    ASSIGN subgroup-list.subgrp-no = wgrpdep.zknr        
           subgroup-list.subgrp-description = wgrpdep.bezeich.
END.
FOR EACH wgrpgen NO-LOCK BY wgrpgen.eknr:
    CREATE maingroup-list.
    ASSIGN maingroup-list.maingrp-no = wgrpgen.eknr        
           maingroup-list.maingrp-description = wgrpgen.bezeich.
END.

FOR EACH language-list:
    DELETE language-list.
END.
FOR EACH carousel-list:
    DELETE carousel-list.
END.
FIND FIRST bediener WHERE bediener.username EQ input-username NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN user-init = bediener.userinit.
FIND FIRST hoteldpt WHERE hoteldpt.num EQ outlet-no NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN outlet-name = hoteldpt.depart.
FIND FIRST paramtext WHERE paramtext.txtnr EQ 200 NO-LOCK NO-ERROR.
IF AVAILABLE paramtext THEN hotel-name = paramtext.ptexte.
RUN selforder-loadarticlebl.p(outlet-no, OUTPUT mess-result, OUTPUT TABLE article-list).
FOR EACH queasy WHERE queasy.key EQ 222 
    AND queasy.number1 EQ 1 NO-LOCK BY queasy.number2:
    IF queasy.number2 EQ 1 THEN font-color = queasy.char2.
    ELSE IF queasy.number2 EQ 2 THEN bg-color = queasy.char2.
    ELSE IF queasy.number2 EQ 3 THEN image-logo = queasy.char2.
END.
FIND FIRST queasy WHERE queasy.key EQ 222 AND queasy.number1 EQ 4 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    ASSIGN
    image-food  = queasy.char1
    image-bev   = queasy.char2
    image-other = queasy.char3
    .
END.
FOR EACH queasy WHERE queasy.key EQ 222 
    AND queasy.number1 EQ 3 
    AND queasy.number3 EQ outlet-no 
    AND queasy.logi1 NO-LOCK:
    CREATE carousel-list.
    ASSIGN
      carousel-list.carousel-recid    = RECID(queasy)
      carousel-list.carousel-dept     = queasy.number3
      carousel-list.carousel-num      = queasy.number2
      carousel-list.carousel-title    = queasy.char1
      carousel-list.carousel-desc     = queasy.char3
      carousel-list.carousel-image    = queasy.char2
    .
END.
mess-result = "Success load data".
