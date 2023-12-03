FROM python:3.9
WORKDIR /pub

ENV VIRTUAL_ENV=/pub/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . /pub
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
ENV ENDPOINT "localhost"
CMD [ "python", "pub.py" ]