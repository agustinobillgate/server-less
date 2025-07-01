DEFINE TEMP-TABLE room-list 
  FIELD wd           AS INTEGER 
  FIELD datum        AS DATE 
  FIELD bezeich      AS CHAR FORMAT "x(15)"
  FIELD room         AS DECIMAL FORMAT " >>9.99" EXTENT 17 INITIAL 0 
  FIELD coom         AS CHAR EXTENT /*21*/ 17 FORMAT "x(7)" INITIAL "" 
  FIELD k-pax        AS INTEGER INITIAL 0
  FIELD t-pax        AS INTEGER INITIAL 0
  FIELD lodg         AS DECIMAL EXTENT 7 FORMAT "->>>,>>>,>>>,>>9.99" /* Modify by Michael @ 30/11/2018 for Nihiwatu Resort - ticket no 36774F */
  FIELD avrglodg     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" 
  FIELD avrglodg2    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
  FIELD avrgrmrev    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" /*MT 17/10/13 */
  FIELD avrgrmrev2   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" /*FONT 2*/ 
  FIELD others       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" EXTENT 8 /* Modify by Michael @ 30/11/2018 for Nihiwatu Resort - ticket no 36774F */
  FIELD ly-fcast     AS CHAR    FORMAT "x(7)"
  FIELD ly-actual    AS CHAR    FORMAT "x(7)"
  FIELD ly-avlodge   AS CHAR    FORMAT "x(13)"
  FIELD room-excComp AS INT INIT 0
  FIELD room-comp    AS INT INIT 0
.

DEFINE TEMP-TABLE segm-list 
  FIELD selected     AS LOGICAL INITIAL NO 
  FIELD segm         AS INTEGER 
  FIELD bezeich      AS CHAR FORMAT "x(24)". 
 
DEFINE TEMP-TABLE argt-list 
  FIELD selected     AS LOGICAL INITIAL NO 
  FIELD argtnr       AS INTEGER
  FIELD argt         AS CHAR 
  FIELD bezeich      AS CHAR FORMAT "x(24)". 
 
DEFINE TEMP-TABLE zikat-list 
  FIELD selected     AS LOGICAL INITIAL NO 
  FIELD zikatnr      AS INTEGER 
  FIELD bezeich      AS CHAR FORMAT "x(24)". 

DEFINE TEMP-TABLE outlook-list
    FIELD SELECTED   AS LOGICAL INITIAL NO
    FIELD outlook-nr AS INTEGER
    FIELD bezeich    AS CHAR FORMAT "x(16)".


DEFINE INPUT PARAMETER language-code AS INTEGER.
DEFINE INPUT PARAMETER from-date    AS DATE. /*curr-date*/
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER flag-i       AS INTEGER.
DEFINE INPUT PARAMETER all-segm     AS LOGICAL.
DEFINE INPUT PARAMETER all-argt     AS LOGICAL.
DEFINE INPUT PARAMETER all-zikat    AS LOGICAL.
DEFINE INPUT PARAMETER mi-lessOOO   AS LOGICAL.
DEFINE INPUT PARAMETER mi-incltent  AS LOGICAL.
DEFINE INPUT PARAMETER rev-typ      AS INTEGER.
DEFINE INPUT PARAMETER mi-exclcomp  AS LOGICAL.
DEFINE INPUT PARAMETER all-outlook  AS LOGICAL.
DEFINE INPUT PARAMETER mi-lastyr    AS LOGICAL.

DEFINE INPUT PARAMETER TABLE FOR segm-list.
DEFINE INPUT PARAMETER TABLE FOR argt-list.
DEFINE INPUT PARAMETER TABLE FOR zikat-list.
DEFINE INPUT PARAMETER TABLE FOR outlook-list.

DEFINE OUTPUT PARAMETER msg-str AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.

DEF VAR vhp-limited AS LOGICAL initial NO.
/*
MESSAGE language-code
        from-date   
        to-date     
        flag-i      
        all-segm    
        all-argt    
        all-zikat   
        mi-lessOOO  
        mi-incltent 
        rev-typ     
        mi-exclcomp 
        all-outlook 
        mi-lastyr 
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
IF to-date LT from-date THEN 
DO: 
    msg-str = "ToDate can not be earlier then FromDate.".
    RETURN. 
END. 

RUN cr-occfcast1_2bl.p(TABLE segm-list,
                       TABLE argt-list,
                       TABLE zikat-list,
                       TABLE outlook-list,
                       language-code, 
                       0, 
                       flag-i, 
                       from-date, 
                       to-date, 
                       all-segm,
                       all-argt, 
                       all-zikat,
                       mi-lessOOO, 
                       mi-incltent,
                       rev-typ, 
                       vhp-limited,
                       mi-exclcomp, 
                       all-outlook,
                       OUTPUT TABLE room-list). 

IF mi-lastyr THEN 
DO: 
    RUN cr-occfcast1_1lybl.p(from-date, to-date, all-segm, all-argt, all-zikat,
                 INPUT-OUTPUT TABLE room-list, TABLE segm-list,
                 TABLE argt-list, TABLE zikat-list). 
END.
