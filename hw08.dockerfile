FROM r-base:4.3.0

RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /hw08

COPY hw08.R /hw08/
COPY Пациенты.xlsx /hw08/

RUN R -e "install.packages('readxl', repos='https://cloud.r-project.org/')"

CMD ["Rscript", "hw08.R"]