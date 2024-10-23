DEFINE TEMP-TABLE rest-article-list
    FIELD dept-no           AS INTEGER
    FIELD dept-name         AS CHARACTER
    FIELD artnr             AS INTEGER
    FIELD art-desc          AS CHARACTER
    FIELD main-group        AS INTEGER
    FIELD sub-group         AS INTEGER
    FIELD main-group-desc   AS CHARACTER
    FIELD sub-group-desc    AS CHARACTER
    FIELD art-type          AS INTEGER
    FIELD price             AS DECIMAL
    FIELD cost%             AS DECIMAL
    FIELD fo-artnr          AS INTEGER
    FIELD foart-desc        AS CHARACTER
    FIELD recipe-no         AS INTEGER
    FIELD recipe-desc       AS CHARACTER
    FIELD kp-no             AS INTEGER
    FIELD kp-desc           AS CHARACTER
    FIELD active-art        AS LOGICAL
    .

DEFINE TEMP-TABLE rest-maingroup-list
    FIELD maingroup-no          AS INTEGER
    FIELD maingroup-desc        AS CHARACTER
    FIELD new-maingroup-no      AS INTEGER
    FIELD new-maingroup-desc    AS CHARACTER
    FIELD fibukonto             AS CHARACTER
    FIELD betriebsnr            AS INTEGER
    .

DEFINE TEMP-TABLE rest-subgroup-list
    FIELD dept-no               AS INTEGER
    FIELD dept-name             AS CHARACTER
    FIELD subgroup-no           AS INTEGER
    FIELD subgroup-desc         AS CHARACTER
    FIELD subgroup-prior        AS INTEGER
    FIELD subgroup-bgcol        AS INTEGER
    FIELD new-subgroup-no       AS INTEGER
    FIELD new-subgroup-desc     AS CHARACTER
    FIELD fibukonto             AS CHARACTER
    FIELD betriebsnr            AS INTEGER
    .

DEFINE TEMP-TABLE output-list
   FIELD dept-no    AS INTEGER
   FIELD dept-name  AS CHARACTER
   FIELD artnr      AS INTEGER
   FIELD art-desc   AS CHARACTER
   FIELD maingroup  AS INTEGER
   FIELD subgroup   AS INTEGER
   FIELD str        AS CHAR
   FIELD KEY        AS CHAR
   FIELD flag       AS INTEGER.

DEFINE INPUT  PARAMETER TABLE FOR rest-article-list.
DEFINE INPUT  PARAMETER TABLE FOR rest-maingroup-list.
DEFINE INPUT  PARAMETER TABLE FOR rest-subgroup-list.

DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE BUFFER b-article-list FOR rest-article-list.
DEFINE BUFFER b-maingroup-list FOR rest-maingroup-list.
DEFINE BUFFER b-subgroup-list FOR rest-subgroup-list.

FOR EACH output-list:
    DELETE output-list.
END.

FOR EACH rest-maingroup-list NO-LOCK :
    IF rest-maingroup-list.new-maingroup-no NE ? AND rest-maingroup-list.new-maingroup-desc EQ ? THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "There is a new main group but no description " + "(" + STRING(rest-maingroup-list.new-maingroup-no) + ")"
              output-list.KEY = "maingroup".
    END.
    IF rest-maingroup-list.new-maingroup-no EQ ? AND rest-maingroup-list.new-maingroup-desc NE ? THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "There is a new main group but has not number " + "(" + rest-maingroup-list.new-maingroup-desc + ")"
              output-list.KEY = "maingroup".
    END.
END.

FOR EACH rest-subgroup-list NO-LOCK:
   IF rest-subgroup-list.new-subgroup-no NE ? AND rest-subgroup-list.new-subgroup-desc EQ ? THEN
   DO:
      CREATE output-list.
      ASSIGN output-list.str = "There is a new sub group but no description " + "(" + STRING(rest-subgroup-list.new-subgroup-no) + ")"
             output-list.KEY = "subgroup".
   END.

   IF rest-subgroup-list.new-subgroup-no EQ ? AND rest-subgroup-list.new-subgroup-desc NE ? THEN
   DO:
       CREATE output-list.
       ASSIGN output-list.str = "There is a new sub group but has not number " + "(" + rest-subgroup-list.new-subgroup-desc + ")"
              output-list.KEY = "subgroup".
   END.

   IF rest-subgroup-list.new-subgroup-no NE ? OR rest-subgroup-list.new-subgroup-desc NE ? THEN
   DO:
      IF rest-subgroup-list.dept-no EQ ? THEN
      DO:
        CREATE output-list.
        ASSIGN output-list.str = "There is a new sub group but has not departement number " + "(" + STRING(rest-subgroup-list.new-subgroup-no) + ")"
               output-list.KEY = "subgroup".
      END.
      IF rest-subgroup-list.dept-name EQ ? THEN
      DO:
        CREATE output-list.
        ASSIGN output-list.str = "There is a new sub group but has not departement description " + "(" + STRING(rest-subgroup-list.new-subgroup-no) + ")"
               output-list.KEY = "subgroup".
      END.
   END.
END.

FOR EACH rest-article-list NO-LOCK:
    IF rest-article-list.dept-no EQ ? THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "There is an article has not departement number at article " + "(" + STRING(rest-article-list.artnr) + ")"
              output-list.KEY = "article".
    END.
    IF rest-article-list.art-desc EQ ? THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "There is an article has not description at article " + "(" + STRING(rest-article-list.artnr) + ")"
              output-list.KEY = "article".
    END.
    IF rest-article-list.price EQ ? THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "Please fill the Price column at article " + "(" + STRING(rest-article-list.artnr) + ")"
              output-list.KEY = "article".
    END.
    IF rest-article-list.cost% EQ ? THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "Please fill Cost% column at article " + "(" + STRING(rest-article-list.artnr) + ")"
              output-list.KEY = "article".
    END.
    IF rest-article-list.kp-no EQ ? THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "Please fill KP NO column at article " + "(" + STRING(rest-article-list.artnr) + ")"
              output-list.KEY = "article".
    END.
    IF rest-article-list.fo-artnr EQ ? THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "Please fill FO Art column at article " + "(" + STRING(rest-article-list.artnr) + ")"
              output-list.KEY = "article".
    END.
    IF rest-article-list.recipe-no EQ ? THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "Please fill Recipe column at article " + "(" + STRING(rest-article-list.artnr) + ")"
              output-list.KEY = "article".
    END.

    FIND FIRST b-maingroup-list WHERE (b-maingroup-list.maingroup-desc EQ rest-article-list.main-group-desc)
        OR (b-maingroup-list.new-maingroup-desc EQ rest-article-list.main-group-desc) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE b-maingroup-list THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "There is an invalid maingroup description at article " + "(" + STRING(rest-article-list.artnr) + ")" + " Department " +
                                rest-article-list.dept-name
              output-list.KEY = "article".
    END.

    FIND FIRST b-subgroup-list WHERE (b-subgroup-list.subgroup-desc EQ rest-article-list.sub-group-desc)
        OR (b-subgroup-list.new-subgroup-desc EQ rest-article-list.sub-group-desc) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE b-subgroup-list THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str = "There is an invalid subgroup description at article " + "(" + STRING(rest-article-list.artnr) + ")" + " Department " +
                                rest-article-list.dept-name
              output-list.KEY = "article".
    END.

    FIND FIRST b-article-list WHERE b-article-list.dept-no = rest-article-list.dept-no
        AND b-article-list.artnr = rest-article-list.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE b-article-list THEN
    DO:
       IF b-article-list.art-desc NE rest-article-list.art-desc THEN
       DO:
         CREATE output-list.
         ASSIGN output-list.str = "Article " + b-article-list.art-desc + " has the same article number with " + rest-article-list.art-desc.
                output-list.KEY = "article".
       END.
    END.

    IF LENGTH(STRING(rest-article-list.artnr)) GT 8 THEN
    DO:
      FIND FIRST rest-maingroup-list WHERE rest-maingroup-list.new-maingroup-no = INTEGER(SUBSTR(STRING(rest-article-list.artnr),1,1)) NO-LOCK NO-ERROR.
      IF NOT AVAILABLE rest-maingroup-list THEN
      DO:
        CREATE output-list.
        ASSIGN output-list.str = "New Article " + rest-article-list.art-desc + " has invalid main group number in article number".
               output-list.KEY = "article".  
      END.
      
      FIND FIRST rest-subgroup-list WHERE rest-subgroup-list.new-subgroup-no = INTEGER(SUBSTR(STRING(rest-article-list.artnr),4,2))
          AND rest-subgroup-list.dept-no = rest-article-list.dept-no NO-LOCK NO-ERROR.
      IF NOT AVAILABLE rest-subgroup-list THEN
      DO:
        CREATE output-list.
        ASSIGN output-list.str = "New Article " + rest-article-list.art-desc + " has invalid sub group number in article number".
               output-list.KEY = "article".
      END.
    END.

    IF rest-article-list.recipe-no NE 0 THEN
    DO:
      FIND FIRST h-rezept WHERE h-rezept.artnrrezept = rest-article-list.recipe-no NO-LOCK NO-ERROR.
      IF NOT AVAILABLE h-rezept THEN
      DO:
         CREATE output-list.
         ASSIGN output-list.str = "Article " + rest-article-list.art-desc + "(" + STRING(rest-article-list.artnr) + ")" + " has invalid recipe number (not found)".
                output-list.KEY = "article".
      END.
    END.

    FIND FIRST h-artikel WHERE h-artikel.artnr = rest-article-list.artnr
        AND h-artikel.departement = rest-article-list.dept-no
        AND h-artikel.activeflag NE rest-article-list.active-art NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
       CREATE output-list.
       ASSIGN output-list.str  = "Article " + rest-article-list.art-desc + " ( " + STRING(rest-article-list.artnr) + " )" + " at departement " + rest-article-list.dept-name + " is exist but flag is not same."
              output-list.KEY  = "completed"
              output-list.flag = 1.
    END.
END.

FIND FIRST output-list WHERE output-list.KEY NE "completed" NO-ERROR.
IF NOT AVAILABLE output-list THEN
DO:
   CREATE output-list.
   ASSIGN output-list.str  = "EXCEL COMPLETED"
          output-list.KEY  = "completed"
          output-list.flag = 2.
END.
