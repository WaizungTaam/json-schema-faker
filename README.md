# Json Schema Faker

## Usage

```python
>>> schema = {
  "title": "Product",
  "type": "object",
  "properties": {
    "productId": {
      "type": "integer"
    },
    "productName": {
      "type": "string"
    },
    "price": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1,
      "uniqueItems": True
    }
  },
  "required": ["productId", "productName", "price"]
}

>>> from generators import generate
>>> generate(schema)
{
  "productId": 4435008459824491594,
  "productName": "peVb670VVHBI",
  "price": 4.3245454440117504E+18,
  "tags": [
    "IJO8BCPStyN14",
    "a",
    "nUrFsmf",
    "ClFuuowOkm"
  ]
}
```
