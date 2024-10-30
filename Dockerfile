# Use Debian 11 as base image
FROM debian:11

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    sudo \
    python3-pip \
    python3-venv \
    libssl-dev \
    libssl1.1 \
    vim

# Add Microsoft package signing key and repository for Debian 11
RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list


# Update and install msodbcsql17, mssql-tools, and other optional packages
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc-dev libgssapi-krb5-2

# Add mssql-tools to PATH
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
    /bin/bash -c "source ~/.bashrc"

# Modify the OpenSSL configuration to allow legacy algorithms
RUN sed -i '/^\[system_default_sect\]/a Options = UnsafeLegacyRenegotiation' /etc/ssl/openssl.cnf || \
    echo -e '[system_default_sect]\nOptions = UnsafeLegacyRenegotiation' >> /etc/ssl/openssl.cnf

# Create a virtual environment and install Python dependencies in it
#RUN python3 -m venv /app/venv
#ENV PATH="/app/venv/bin:$PATH"

# Copy application files to the container
COPY . /app

# Modify the OpenSSL configuration to set minimum protocol and cipher string
RUN sed -i '/^\[system_default_sect\]/a MinProtocol = TLSv1\nCipherString = DEFAULT@SECLEVEL=1' /etc/ssl/openssl.cnf || \
    echo -e '[system_default_sect]\nMinProtocol = TLSv1\nCipherString = DEFAULT@SECLEVEL=1' >> /etc/ssl/openssl.cnf


# Install Python dependencies explicitly in the virtual environment
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 54321

# Set the default command to run the app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:54321", "app:app"]

