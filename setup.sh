#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}ReactFast Contacts - Local Development Setup${NC}"
echo "======================================"

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    echo "Visit https://docs.docker.com/get-docker/ for installation instructions."
    exit 1
else
    echo -e "${GREEN}✓ Docker is installed${NC}"
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    echo "Visit https://docs.docker.com/compose/install/ for installation instructions."
    exit 1
else
    echo -e "${GREEN}✓ Docker Compose is installed${NC}"
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Node.js is not installed. It's recommended for local development without Docker.${NC}"
else
    echo -e "${GREEN}✓ Node.js is installed${NC}"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is not installed. It's recommended for local development without Docker.${NC}"
else
    echo -e "${GREEN}✓ Python 3 is installed${NC}"
fi

# Create necessary directories
echo -e "\n${YELLOW}Creating necessary directories...${NC}"
mkdir -p prometheus grafana/provisioning/datasources grafana/provisioning/dashboards
echo -e "${GREEN}✓ Directories created${NC}"

# Copy example env file if it doesn't exist
if [ ! -f frontend/.env.local ]; then
    echo -e "\n${YELLOW}Creating frontend/.env.local from example...${NC}"
    cp frontend/.env.local.example frontend/.env.local
    echo -e "${GREEN}✓ Created frontend/.env.local${NC}"
    echo -e "${YELLOW}Please edit frontend/.env.local with your Firebase configuration if you want to use authentication.${NC}"
fi

# Start the application with Docker Compose
echo -e "\n${YELLOW}Starting the application with Docker Compose...${NC}"
echo "This may take a few minutes for the first run as Docker images need to be downloaded."
docker-compose up -d

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "The application is now running at:"
echo -e "  - Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "  - Backend API: ${GREEN}http://localhost:8000${NC}"
echo -e "  - API Documentation: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  - Prometheus: ${GREEN}http://localhost:9090${NC}"
echo -e "  - Grafana: ${GREEN}http://localhost:3001${NC} (admin/password)"
echo -e "\nTo stop the application, run: ${YELLOW}docker-compose down${NC}"
echo -e "To view logs, run: ${YELLOW}docker-compose logs -f${NC}"
