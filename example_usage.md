# API Endpoint Usage

## Main Webhook Endpoint

**POST** `http://localhost:5000/webhook`

## Example Request with Your Sample Data

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "parent": "John",
    "child": "Sarah",
    "wishlist": ["Toy Car", "Book", "Puzzle"]
  }'
```

## Example Response

```json
{
  "status": "success",
  "message": "Message received and stored",
  "received_at": "2024-01-15T10:30:45.123456"
}
```

## How Data is Stored in JSON Database

When you send the above request, it will be stored in `whatsapp_messages.json` like this:

```json
[
  {
    "id": 1,
    "timestamp": "2024-01-15T10:30:45.123456",
    "parent": "John",
    "child": "Sarah",
    "wishlist": ["Toy Car", "Book", "Puzzle"]
  }
]
```

Each new message gets:
- Auto-incremented `id`
- ISO format `timestamp`
- Your original data (parent, child, wishlist)

## Retrieve All Messages

**GET** `http://localhost:5000/messages`

Returns:
```json
{
  "status": "success",
  "count": 1,
  "messages": [
    {
      "id": 1,
      "timestamp": "2024-01-15T10:30:45.123456",
      "parent": "John",
      "child": "Sarah",
      "wishlist": ["Toy Car", "Book", "Puzzle"]
    }
  ]
}
```

## Get Specific Message

**GET** `http://localhost:5000/messages/1`

Returns the message with id=1

