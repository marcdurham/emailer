FROM python:alpine

RUN apk update && apk add ca-certificates git

RUN pip install 'emailer>=1.0'
RUN mkdir -p /var/emailer

WORKDIR /var/emailer
CMD ["email", "--active", "--dryrun", "-k", "testkey"]
