#!/bin/bash

# Test script for deployed API
# Usage: ./test_deployed_api.sh https://your-app.onrender.com

if [ -z "$1" ]; then
    echo "Usage: ./test_deployed_api.sh <YOUR_API_URL>"
    echo "Example: ./test_deployed_api.sh https://whatsapp-api.onrender.com"
    exit 1
fi

API_URL=$1

echo "=== Testing Deployed API: $API_URL ==="
echo ""

# Test 1: Health check
echo "1. Health Check..."
curl -s "$API_URL/health" | python3 -m json.tool
echo ""
echo ""

# Test 2: Check new user
echo "2. Check New User (should return exists: false)..."
curl -s -X POST "$API_URL/check-or-create-user" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}' | python3 -m json.tool
echo ""
echo ""

# Test 3: Save user
echo "3. Save User..."
curl -s -X POST "$API_URL/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": []
  }' | python3 -m json.tool
echo ""
echo ""

# Test 4: Check existing user
echo "4. Check Existing User (should return exists: true)..."
curl -s -X POST "$API_URL/check-or-create-user" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}' | python3 -m json.tool
echo ""
echo ""

# Test 5: Get all users
echo "5. Get All Users..."
curl -s "$API_URL/users" | python3 -m json.tool
echo ""
echo ""

echo "=== All Tests Complete ==="

