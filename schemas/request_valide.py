scheme = {
      "type": "object",
      "properties": {
        "parent_request_id": {
          "type": "integer",
          "minimum": 0
        },
        "description": {
          "type": "string",
          "maxLength": 255
        },
        "source": {
          "enum" : ["LANDING","VK","OPERATOR","EXCEL","TELEGRAM","ANDROID","IOS","OTHER"] 
        },
        "problem_categories": {
          "type": "array",
          "items": {
              "type": "integer"
            }
        },
        "base_rating":{
            "type": "integer"
        },
        "latitude": {
          "type": "number"
        },
        "longitude": {
          "type": "number"
        },
        "status": {
          "enum" : ["IN PROCESSING", "IN CONSIDERATION", "IN EXECUTION","IN EXECUTION CHECK", "COMPLETED","ARCHIVED"]
        },
        "attachments": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
                "type" : {"enum":["IMAGE","VIDEO"]},
                "url" : {
                  "type":"string",
                  "format":"uri"
                }
            }
          }
        },
        "request_consideration_at": {
          "type": "string",
          "format" : "date-time"
        },
        "begin_request_execution_at": {
          "type": "string",
          "format" : "date-time"
        },
        "complete_request_execution_at": {
          "type": "string",
          "format" : "date-time"
        },
        "request_status_checked_at": {
          "type": "string",
          "format" : "date-time"
        },
        "is_moderated": {
          "type": "boolean"
        },
        "moderator_id": {
          "type": "integer",
          "minimum" : 0
        }
      },
      "required": ["source","latitude","longitude","problem_categories","description"]
    }

