FROM node:alpine

# Set node environment, either development or production
ARG NODE_ENV=production
ENV NODE_ENV $NODE_ENV

# Install dependencies
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm install --no-optional && npm cache clean --force

# Install app
COPY *.js /app/
COPY data/* /app/

# Export app port and set entrypoint at startup
EXPOSE 3030
ENTRYPOINT ["node", "index.js"]
CMD [""]
