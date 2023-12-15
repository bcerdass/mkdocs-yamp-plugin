FROM python:3.8
RUN pip install mkdocs mkdocs-material

ADD . .
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install .  # Install yamp plugin

# Start development server by default
ENTRYPOINT ["mkdocs"]
