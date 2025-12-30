#!/bin/bash

echo "=== Testing Kapso Flow API Endpoints ==="
echo ""

# Test 1: Check new user (should return exists: false)
echo "1. Testing check-or-create-user for NEW user..."
curl -X POST http://localhost:5000/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'

echo ""
echo ""

# Test 2: Save new user
echo "2. Testing save-user (creating new user)..."
curl -X POST http://localhost:5000/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": []
  }'

echo ""
echo ""

# Test 3: Check existing user (should return exists: true)
echo "3. Testing check-or-create-user for EXISTING user..."
curl -X POST http://localhost:5000/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'

echo ""
echo ""

# Test 4: Get all users
echo "4. Testing get all users..."
curl -X GET http://localhost:5000/users

echo ""
echo ""

# Test 5: Get specific user
echo "5. Testing get specific user..."
curl -X GET http://localhost:5000/users/+1234567890

echo ""
echo ""

