FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r req.txt
RUN aerich upgrade
RUN python fill_mock_data.py
CMD uvicorn --factory app.app:create_app --workers 1