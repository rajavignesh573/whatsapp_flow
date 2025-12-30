#!/bin/bash

echo "=== Testing Supabase Setup ==="
echo ""

# Test 1: Health check (should show Supabase configured)
echo "1. Health Check (should show Supabase=True)..."
curl -s http://localhost:5000/health | python3 -m json.tool
echo ""
echo ""

# Test 2: Save user to Supabase
echo "2. Saving user to Supabase..."
curl -s -X POST http://localhost:5000/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+9998887777",
    "parent_name": "Test Parent",
    "child_name": "Test Child",
    "wishlist": []
  }' | python3 -m json.tool
echo ""
echo ""

# Test 3: Check if user exists
echo "3. Checking if user exists..."
curl -s -X POST http://localhost:5000/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+9998887777"}' | python3 -m json.tool
echo ""
echo ""

# Test 4: Get all users
echo "4. Getting all users from Supabase..."
curl -s http://localhost:5000/users | python3 -m json.tool
echo ""
echo ""

echo "=== Tests Complete ==="
echo ""
echo "✅ If you see 'supabase_configured': true, Supabase is working!"
echo "✅ Check your Supabase dashboard to see the data:"
echo "   https://supabase.com/dashboard/project/huyzlryubollexkuykgd/editor"

