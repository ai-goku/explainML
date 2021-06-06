FROM python:3.8.10-alpine3.13
WORKDIR app
COPY . .
RUN apk update && \
 apk upgrade && \
 apk add build-base && \
 echo "#include <unistd.h>" > /usr/include/sys/unistd.h
RUN pip install -r requirements.txt
# RUN apk add build-base
# RUN echo "#include <unistd.h>" > /usr/include/sys/unistd.h
# RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["python", "main.py"]