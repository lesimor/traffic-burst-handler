FROM python:3.9-slim


# Your PyPI credentials
ENV PYPI_USER=admin
ENV PYPI_PASS=0zWUZ1K4fYTQK94d

# Add your private PyPI repository
RUN pip config set global.extra-index-url http://$PYPI_USER:$PYPI_PASS@docker-registry.com/repository/dchain-connect-pypi/
RUN pip config set global.trusted-host docker-registry.com

# Your download and CLI command script
COPY ./scripts/run_scaler.sh /script.sh
RUN chmod +x /script.sh

CMD ["/script.sh"]
