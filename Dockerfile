# Start with a Debian 12 base image
FROM debian:12

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    sudo


RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

# Debian 12
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg

#Debian 12
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
RUN exit

RUN sudo apt-get update

RUN sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
RUN sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN source ~/.bashrc
# optional: for unixODBC development headers
RUN sudo apt-get install -y unixodbc-dev
# optional: kerberos library for debian-slim distributions
RUN sudo apt-get install -y libgssapi-krb5-2


# Apply PATH changes
SHELL ["/bin/bash", "-c"]
RUN source ~/.bashrc

# Set entrypoint
ENTRYPOINT ["/bin/bash"]

# Copy the application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 1337

# Run the app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:1337", "app:app"]

