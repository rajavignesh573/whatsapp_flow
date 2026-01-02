#!/bin/bash
# Quick cURL Testing Commands for WhatsApp Flow API
# Copy and paste these commands to test your endpoints

BASE_URL="https://whatsapp-flow-virid.vercel.app"
# For local testing, use: BASE_URL="http://localhost:5000"

echo "============================================================"
echo "  WhatsApp Flow API - cURL Test Commands"
echo "============================================================"
echo ""
echo "Base URL: $BASE_URL"
echo ""
echo "Copy and paste any command below to test:"
echo ""

# 1. Health Check
echo "# 1. Health Check"
echo "curl -X GET \"$BASE_URL/health\""
echo ""

# 2. Debug Info
echo "# 2. Debug Info"
echo "curl -X GET \"$BASE_URL/debug\""
echo ""

# 3. Save User
echo "# 3. Save User (POST /save-user)"
echo "curl -X POST \"$BASE_URL/save-user\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"user\": \"+1234567890\", \"parent_name\": \"John Doe\", \"child_name\": \"Jane Doe\", \"wishlist\": [\"toy1\", \"toy2\"]}'"
echo ""

# 4. Check or Create User
echo "# 4. Check or Create User"
echo "curl -X POST \"$BASE_URL/check-or-create-user\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"phone\": \"+1234567890\"}'"
echo ""

# 5. Get All Users
echo "# 5. Get All Users"
echo "curl -X GET \"$BASE_URL/users\""
echo ""

# 6. Get User by Phone
echo "# 6. Get User by Phone"
echo "curl -X GET \"$BASE_URL/users/+1234567890\""
echo ""

# 7. Get All Messages
echo "# 7. Get All Messages"
echo "curl -X GET \"$BASE_URL/messages\""
echo ""

# 8. Get Message by ID
echo "# 8. Get Message by ID"
echo "curl -X GET \"$BASE_URL/messages/1\""
echo ""

# 9. Webhook POST
echo "# 9. Webhook POST"
echo "curl -X POST \"$BASE_URL/webhook\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"entry\": [{\"changes\": [{\"value\": {\"messages\": [{\"from\": \"+1234567890\", \"text\": {\"body\": \"Test message\"}}]}}]}]}'"
echo ""

# 10. Webhook GET (Verification)
echo "# 10. Webhook Verification"
echo "curl -X GET \"$BASE_URL/webhook?hub.mode=subscribe&hub.verify_token=your_verify_token_here&hub.challenge=test_challenge\""
echo ""

echo "============================================================"

