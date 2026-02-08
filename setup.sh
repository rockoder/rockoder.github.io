#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting setup for rockoder.com...${NC}"

# 1. Install Node.js dependencies
echo -e "${BLUE}📦 Installing Node.js dependencies with pnpm...${NC}"
pnpm install

# 2. Install Python dependencies
if [ -f "scripts/requirements_hn.txt" ]; then
    echo -e "${BLUE}🐍 Installing Python dependencies...${NC}"
    pip install -r scripts/requirements_hn.txt
else
    echo -e "${BLUE}⚠️ scripts/requirements_hn.txt not found, skipping Python deps.${NC}"
fi

# 3. Install Playwright browsers
echo -e "${BLUE}🎭 Installing Playwright browsers...${NC}"
npx playwright install --with-deps chromium

# 4. Build the site
echo -e "${BLUE}🏗️ Building the site...${NC}"
pnpm build

# 5. Take a snapshot
echo -e "${BLUE}📸 Taking a snapshot...${NC}"
mkdir -p screenshots
pnpm test:visual

echo -e "${GREEN}✅ Setup complete! Homepage snapshot saved to screenshots/homepage.png${NC}"
