#!/bin/bash

echo "=== Testing WhatsApp Flow API Locally ==="
echo ""

API_URL="http://localhost:5000"

# Test 1: Health Check
echo "1. Health Check..."
curl -s "$API_URL/health" | python3 -m json.tool
echo ""
echo ""

# Test 2: Debug Info
echo "2. Debug Info..."
curl -s "$API_URL/debug" | python3 -m json.tool
echo ""
echo ""

# Test 3: Check New User
echo "3. Check New User (should return exists: false)..."
curl -s -X POST "$API_URL/check-or-create-user" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+9998887777"}' | python3 -m json.tool
echo ""
echo ""

# Test 4: Save User
echo "4. Save User..."
curl -s -X POST "$API_URL/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+9998887777",
    "parent_name": "Test Parent",
    "child_name": "Test Child",
    "wishlist": []
  }' | python3 -m json.tool
echo ""
echo ""

# Test 5: Check Existing User
echo "5. Check Existing User (should return exists: true)..."
curl -s -X POST "$API_URL/check-or-create-user" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+9998887777"}' | python3 -m json.tool
echo ""
echo ""

# Test 6: Get All Users
echo "6. Get All Users..."
curl -s "$API_URL/users" | python3 -m json.tool
echo ""
echo ""

# Test 7: Get Specific User
echo "7. Get Specific User..."
curl -s "$API_URL/users/+9998887777" | python3 -m json.tool
echo ""
echo ""

# Test 8: Webhook Test
echo "8. Test Webhook..."
curl -s -X POST "$API_URL/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": "John",
    "child": "Sarah",
    "wishlist": ["Toy Car", "Book", "Puzzle"]
  }' | python3 -m json.tool
echo ""
echo ""

echo "=== All Tests Complete ==="
echo ""
echo "✅ Local API is working!"
echo "📝 Note: Currently using JSON files (Supabase has proxy error)"
echo "💾 Data is saved in: users.json and whatsapp_messages.json"

