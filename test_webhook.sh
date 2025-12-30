#!/bin/bash

# Test the webhook endpoint with sample data
echo "Testing WhatsApp Webhook API..."
echo ""

# Sample wishlist data
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "parent": "John",
    "child": "Sarah",
    "wishlist": ["Toy Car", "Book", "Puzzle"]
  }'

echo ""
echo ""
echo "Retrieving all messages..."
curl -X GET http://localhost:5000/messages

