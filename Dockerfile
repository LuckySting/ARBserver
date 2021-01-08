FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r req.txt
CMD aerich upgrade && rm migrations/models/old_models.py && python fill_mock_data.py && uvicorn --factory app.app:create_app --workers 1