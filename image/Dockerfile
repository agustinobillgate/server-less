FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies

RUN pip install -r requirements.txt

# Copy source code
COPY src/* ${LAMBDA_TASK_ROOT}

# Copy models
RUN mkdir -p ${LAMBDA_TASK_ROOT}/models
COPY src/models/* ${LAMBDA_TASK_ROOT}/models

# Copy modules
RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules
COPY src/modules/. ${LAMBDA_TASK_ROOT}/modules/

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/Common
COPY src/modules/Common/* ${LAMBDA_TASK_ROOT}/modules/Common

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/Horeka
COPY src/modules/Horeka/* ${LAMBDA_TASK_ROOT}/modules/Horeka

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/HouseKeeping
COPY src/modules/HouseKeeping/* ${LAMBDA_TASK_ROOT}/modules/HouseKeeping

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/mobileCI
COPY src/modules/mobileCI/* ${LAMBDA_TASK_ROOT}/modules/mobileCI

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/preCI
COPY src/modules/preCI/* ${LAMBDA_TASK_ROOT}/modules/preCI

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/selfOrder
COPY src/modules/selfOrder/* ${LAMBDA_TASK_ROOT}/modules/selfOrder

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpAP
COPY src/modules/vhpAP/* ${LAMBDA_TASK_ROOT}/modules/vhpAP

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpAR
COPY src/modules/vhpAR/* ${LAMBDA_TASK_ROOT}/modules/vhpAR

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpCommon
COPY src/modules/vhpCommon/* ${LAMBDA_TASK_ROOT}/modules/vhpCommon

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpENG
COPY src/modules/vhpENG/* ${LAMBDA_TASK_ROOT}/modules/vhpENG

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpFA
COPY src/modules/vhpFA/* ${LAMBDA_TASK_ROOT}/modules/vhpFA

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpFOC
COPY src/modules/vhpFOC/* ${LAMBDA_TASK_ROOT}/modules/vhpFOC

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpFOR
COPY src/modules/vhpFOR/* ${LAMBDA_TASK_ROOT}/modules/vhpFOR

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpGC
COPY src/modules/vhpGC/* ${LAMBDA_TASK_ROOT}/modules/vhpGC

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpGL
COPY src/modules/vhpGL/* ${LAMBDA_TASK_ROOT}/modules/vhpGL

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpHK
COPY src/modules/vhpHK/* ${LAMBDA_TASK_ROOT}/modules/vhpHK

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpIA
COPY src/modules/vhpIA/* ${LAMBDA_TASK_ROOT}/modules/vhpIA

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpINV
COPY src/modules/vhpINV/* ${LAMBDA_TASK_ROOT}/modules/vhpINV

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpNA
COPY src/modules/vhpNA/* ${LAMBDA_TASK_ROOT}/modules/vhpNA

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpPC
COPY src/modules/vhpPC/* ${LAMBDA_TASK_ROOT}/modules/vhpPC

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpPOS
COPY src/modules/vhpPOS/* ${LAMBDA_TASK_ROOT}/modules/vhpPOS

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpSC
COPY src/modules/vhpSC/* ${LAMBDA_TASK_ROOT}/modules/vhpSC

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpSelfOrder
COPY src/modules/vhpSelfOrder/* ${LAMBDA_TASK_ROOT}/modules/vhpSelfOrder

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpSetup
COPY src/modules/vhpSetup/* ${LAMBDA_TASK_ROOT}/modules/vhpSetup

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpSM
COPY src/modules/vhpSM/* ${LAMBDA_TASK_ROOT}/modules/vhpSM

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpSS
COPY src/modules/vhpSS/* ${LAMBDA_TASK_ROOT}/modules/vhpSS

RUN mkdir -p ${LAMBDA_TASK_ROOT}/modules/vhpTO
COPY src/modules/vhpTO/* ${LAMBDA_TASK_ROOT}/modules/vhpTO

# Copy functions
RUN mkdir -p ${LAMBDA_TASK_ROOT}/functions
COPY src/functions/* ${LAMBDA_TASK_ROOT}/functions

CMD [ "main.handler"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]