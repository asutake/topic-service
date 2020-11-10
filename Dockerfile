FROM python:3.8-buster as builder

COPY Pipfile Pipfile.lock ./

RUN pip3 install pipenv && pipenv install --system

FROM python:3.8-slim-buster as runner

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uwsgi

RUN apt-get update \
  && apt-get install -y libpq5 libxml2 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV APP_ROOT /opt/service

WORKDIR $APP_ROOT

RUN useradd -r -s /bin/false uwsgi

COPY . $APP_ROOT
RUN ln -nfs /usr/local $APP_ROOT/.venv

RUN chown -R uwsgi:uwsgi $APP_ROOT

USER uwsgi

EXPOSE 9090

ENTRYPOINT ["./docker-entrypoint.sh"]
