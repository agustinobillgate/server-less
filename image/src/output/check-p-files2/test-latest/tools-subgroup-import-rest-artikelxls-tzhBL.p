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

DEFINE INPUT PARAMETER TABLE FOR rest-article-list.
DEFINE INPUT PARAMETER TABLE FOR rest-maingroup-list.
DEFINE INPUT PARAMETER TABLE FOR rest-subgroup-list.
DEFINE OUTPUT PARAMETER artnr     AS INTEGER.
DEFINE OUTPUT PARAMETER dept      AS CHARACTER.
DEFINE OUTPUT PARAMETER art-desc1 AS CHARACTER.
DEFINE OUTPUT PARAMETER art-desc2 AS CHARACTER.
DEFINE OUTPUT PARAMETER maingroup AS INTEGER.
DEFINE OUTPUT PARAMETER subgroup  AS INTEGER.
DEFINE OUTPUT PARAMETER fl-flag   AS INTEGER INIT 0.

DEFINE BUFFER b-article-list FOR rest-article-list.
DEFINE BUFFER b-maingroup-list FOR rest-maingroup-list.
DEFINE BUFFER b-subgroup-list FOR rest-subgroup-list.
DEFINE BUFFER b-wgrpgen FOR wgrpgen.
DEFINE BUFFER b-wgrpdep FOR wgrpdep.
DEFINE BUFFER b-artikel FOR h-artikel.

RUN fix-subgroup.

PROCEDURE fix-subgroup:
  FIND FIRST rest-subgroup-list WHERE rest-subgroup-list.dept-no = rest-article-list.dept-no 
      AND ((rest-subgroup-list.subgroup-desc = rest-article-list.sub-group-desc) OR (rest-subgroup-list.new-subgroup-desc = rest-article-list.sub-group-desc)) NO-LOCK NO-ERROR.
  IF AVAILABLE rest-subgroup-list THEN
  DO:              
    IF TRIM(rest-subgroup-list.subgroup-desc) = TRIM(rest-article-list.sub-group-desc) THEN 
    DO:
        ASSIGN rest-article-list.sub-group = rest-subgroup-list.new-subgroup-no.
    END.
    ELSE IF trim(rest-subgroup-list.new-subgroup-desc) = (rest-article-list.sub-group-desc) THEN 
    DO:
        ASSIGN rest-article-list.sub-group = rest-subgroup-list.new-subgroup-no.
    END.
  END.

  FOR EACH h-artikel:
      FIND FIRST b-article-list WHERE b-article-list.artnr = h-artikel.artnr AND b-article-list.dept-no = h-artikel.departement
          AND b-article-list.sub-group NE h-artikel.zwkum NO-LOCK NO-ERROR.
      IF AVAILABLE b-article-list THEN
      DO:
         ASSIGN h-artikel.zwkum = b-article-list.sub-group.
      END.
  END.
END.
