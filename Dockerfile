FROM python:3.9-slim


# Your PyPI credentials
ENV PYPI_USER=admin
ENV PYPI_PASS=0zWUZ1K4fYTQK94d

# Add your private PyPI repository
RUN pip config set global.extra-index-url http://$PYPI_USER:$PYPI_PASS@docker-registry.com/repository/dchain-connect-pypi/simple/
RUN pip config set global.trusted-host docker-registry.com
RUN pip install rushguard==0.1.4

# Your download and CLI command script
WORKDIR /app
COPY ./scripts/run_scaler.sh /app/script.sh
COPY ./.env /app/.env
# RUN chmod +x /app/script.sh

CMD ["rushguard", "--env-file", "/app/.env", "--incluster", "resource", "scale"]
