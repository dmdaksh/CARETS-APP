# Use a base image with Node.js installed
FROM node:14-alpine

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json into the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the Next.js app into the container
COPY . .

# Build the app for production
RUN npm run build

# Expose port 3000 to the host
EXPOSE 3000

# Start the app in production mode
CMD ["npm", "start"]
