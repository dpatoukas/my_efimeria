# Frontend Dockerfile

# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package.json frontend/package-lock.json ./

# Clean cache and install dependencies
RUN npm cache clean --force && rm -rf node_modules && npm install

# Copy the rest of the frontend code
COPY frontend /app

# Expose port for the Vite development server
EXPOSE 5173

# Start the development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
