# Frontend Dockerfile

# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the development server port
EXPOSE 3000

# Start the application and bind it to all network interfaces
CMD ["npm", "start", "--", "--host", "0.0.0.0"]
