FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies
COPY backend/requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port for the dashboard (default Dash port 8050)
EXPOSE 8050

# Command to run the dashboard (can be adjusted to run the entire pipeline)
CMD ["python", "backend/dashboard/app.py"]
