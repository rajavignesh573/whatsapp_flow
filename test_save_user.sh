#!/bin/bash

API_URL="https://whatsapp-flow-pi.vercel.app"

echo "=== Testing Save User Endpoint ==="
echo ""

# Test 1: Save new user
echo "1. Saving new user..."
RESPONSE=$(curl -s -X POST "$API_URL/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1112223333",
    "parent_name": "Alice",
    "child_name": "Bob",
    "wishlist": []
  }')
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Test 2: Verify user was saved
echo "2. Verifying user was saved..."
curl -s "$API_URL/users/+1112223333" | python3 -m json.tool
echo ""

# Test 3: Update existing user
echo "3. Updating existing user..."
RESPONSE=$(curl -s -X POST "$API_URL/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1112223333",
    "parent_name": "Alice Updated",
    "child_name": "Bob Updated",
    "wishlist": []
  }')
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Test 4: Missing field (error test)
echo "4. Testing missing field (should error)..."
curl -s -X POST "$API_URL/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1112223333",
    "parent_name": "Test"
  }' | python3 -m json.tool
echo ""

# Test 5: Empty request (error test)
echo "5. Testing empty request (should error)..."
curl -s -X POST "$API_URL/save-user" \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool
echo ""

echo "=== Tests Complete ==="

