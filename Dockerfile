FROM python:3.10.12 as python-dev

# Install poetry
RUN pip install poetry

# Set up the in-tree virtual environment
WORKDIR /app

# Copy your application code to the container
COPY . /app

# Install the requirements in the virtual environment
RUN poetry install

RUN chmod 700 ./start.sh

EXPOSE 5001

# Run your application
ENTRYPOINT ["/app/start.sh"]

CMD ["SERVER"]
