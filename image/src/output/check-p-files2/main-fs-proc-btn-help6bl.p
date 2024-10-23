
DEF INPUT PARAMETER text-p2-1 AS CHAR.
DEF OUTPUT PARAMETER b-dept-finteger AS INT.
DEF OUTPUT PARAMETER zwkum-zknr AS INT.

DEFINE buffer b-dept FOR htparam. 

FIND FIRST b-dept WHERE b-dept.paramnr = 900 USE-INDEX paramnr_ix 
  NO-LOCK NO-ERROR.
FIND FIRST zwkum WHERE zwkum.departement = b-dept.finteger 
  AND zwkum.bezeich = text-p2-1 USE-INDEX zkbez_ix NO-LOCK NO-ERROR. 

b-dept-finteger = b-dept.finteger.
zwkum-zknr = zwkum.zknr.
