FROM python:3
ADD . .
RUN pip install -r requirements.txt .

# Start development server by default
ENTRYPOINT ["mkdocs"]