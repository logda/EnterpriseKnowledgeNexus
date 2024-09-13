curl -X POST http://localhost:8000/api/llm/qa/single/ \
-H "Content-Type: application/json" \
-H "Authorization: Token f2560f96db820415cacc543ace91cd121d4b8837" \
-d '{
  "document_id": 1,
  "messages": [
    {
      "role": "user",
      "content": "What is this document about?"
    }
  ],
  "stream": false
}'