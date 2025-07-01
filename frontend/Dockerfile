# Use official Node.js Alpine image for smaller footprint
FROM node:20-alpine AS builder

# Set working directory inside the container
WORKDIR /app

# Copy package manifests
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
# May be RUN npm ci for exact dependencies based on package-lock.json!
RUN npm install

# Copy all source files
COPY . .

# Expose port 5173, which is the default port Vite dev server listens on
EXPOSE 5173

# Run the Vite development server to serve the React app with hot reload
CMD ["npm", "run", "dev"]

###### For production!
# Build the Vite React app for production
# -> RUN npm run build

# Production image to serve built files with a lightweight web server
# -> FROM nginx:stable-alpine

# Copy built static files from builder stage
# -> COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config if you have one -> optional
# -> COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 to the outside world
# -> EXPOSE 80

# Start nginx server
# -> CMD ["nginx", "-g", "daemon off;"]
