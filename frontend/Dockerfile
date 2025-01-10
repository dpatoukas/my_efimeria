# Use an official Node.js runtime as the base image
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json to the working directory
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm cache clean --force && npm install --include=dev

# Copy the rest of the application to the container
COPY frontend /app

# Ensure node_modules/.bin is in PATH
ENV PATH="./node_modules/.bin:$PATH"

# Expose the Vite development server port
EXPOSE 5173

# Start the Vite development server
CMD ["npm", "run", "dev"]
