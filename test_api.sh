#!/bin/bash
# API Testing Script using cURL
# Tests all endpoints of the WhatsApp Flow API

BASE_URL="https://whatsapp-flow-virid.vercel.app"
# For local testing, use: BASE_URL="http://localhost:5000"

echo "============================================================"
echo "  WhatsApp Flow API - Endpoint Testing (cURL)"
echo "============================================================"
echo ""
echo "Testing endpoints at: $BASE_URL"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_section() {
    echo ""
    echo "============================================================"
    echo "  $1"
    echo "============================================================"
}

# 1. Health Check
print_section "Health Check (GET /health)"
curl -X GET "$BASE_URL/health" \
    -H "Content-Type: application/json" \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/health" -w "\nHTTP Status: %{http_code}\n" -s

# 2. Debug Info
print_section "Debug Info (GET /debug)"
curl -X GET "$BASE_URL/debug" \
    -H "Content-Type: application/json" \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/debug" -w "\nHTTP Status: %{http_code}\n" -s

# 3. Save User
print_section "Save User (POST /save-user)"
curl -X POST "$BASE_URL/save-user" \
    -H "Content-Type: application/json" \
    -d '{
        "user": "+1234567890",
        "parent_name": "John Doe",
        "child_name": "Jane Doe",
        "wishlist": ["toy1", "toy2"]
    }' \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | jq '.' 2>/dev/null || curl -X POST "$BASE_URL/save-user" \
    -H "Content-Type: application/json" \
    -d '{"user": "+1234567890", "parent_name": "John Doe", "child_name": "Jane Doe", "wishlist": ["toy1", "toy2"]}' \
    -w "\nHTTP Status: %{http_code}\n" -s

# 4. Check or Create User
print_section "Check or Create User (POST /check-or-create-user)"
curl -X POST "$BASE_URL/check-or-create-user" \
    -H "Content-Type: application/json" \
    -d '{"phone": "+1234567890"}' \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | jq '.' 2>/dev/null || curl -X POST "$BASE_URL/check-or-create-user" \
    -H "Content-Type: application/json" \
    -d '{"phone": "+1234567890"}' \
    -w "\nHTTP Status: %{http_code}\n" -s

# 5. Get All Users
print_section "Get All Users (GET /users)"
curl -X GET "$BASE_URL/users" \
    -H "Content-Type: application/json" \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/users" -w "\nHTTP Status: %{http_code}\n" -s

# 6. Get User by Phone
print_section "Get User by Phone (GET /users/+1234567890)"
curl -X GET "$BASE_URL/users/+1234567890" \
    -H "Content-Type: application/json" \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/users/+1234567890" -w "\nHTTP Status: %{http_code}\n" -s

# 7. Get All Messages
print_section "Get All Messages (GET /messages)"
curl -X GET "$BASE_URL/messages" \
    -H "Content-Type: application/json" \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/messages" -w "\nHTTP Status: %{http_code}\n" -s

# 8. Get Message by ID
print_section "Get Message by ID (GET /messages/1)"
curl -X GET "$BASE_URL/messages/1" \
    -H "Content-Type: application/json" \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/messages/1" -w "\nHTTP Status: %{http_code}\n" -s

# 9. Webhook POST
print_section "Webhook POST (POST /webhook)"
curl -X POST "$BASE_URL/webhook" \
    -H "Content-Type: application/json" \
    -d '{
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "+1234567890",
                        "text": {"body": "Test message"}
                    }]
                }
            }]
        }]
    }' \
    -w "\nHTTP Status: %{http_code}\n" \
    -s | jq '.' 2>/dev/null || curl -X POST "$BASE_URL/webhook" \
    -H "Content-Type: application/json" \
    -d '{"entry": [{"changes": [{"value": {"messages": [{"from": "+1234567890", "text": {"body": "Test message"}}]}}]}]}' \
    -w "\nHTTP Status: %{http_code}\n" -s

# 10. Webhook GET (Verification)
print_section "Webhook GET Verification (GET /webhook)"
curl -X GET "$BASE_URL/webhook?hub.mode=subscribe&hub.verify_token=your_verify_token_here&hub.challenge=test_challenge" \
    -w "\nHTTP Status: %{http_code}\n" \
    -s

echo ""
echo "============================================================"
echo "  Testing Complete"
echo "============================================================"

