# Use an official Ruby runtime as the base image
FROM ruby:3.2

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  libgtk-3-dev \
  libgirepository1.0-dev \
  pkg-config \
  libcairo2-dev \
  libglib2.0-dev \
  libatk1.0-dev \
  libpango1.0-dev \
  libgdk-pixbuf2.0-dev \
  libgdk3.0-cil-dev \
  && rm -rf /var/lib/apt/lists/*

# Install pkg-config and other necessary tools
RUN gem install pkg-config

# Set the working directory
WORKDIR /app

# Copy Gemfile and Gemfile.lock
COPY Gemfile* ./

# Install gems
RUN bundle install

# Copy the rest of the application code
COPY . .

# Define the default command to run the app
CMD ["ruby", "app/promocato_app.rb"]
