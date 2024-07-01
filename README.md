
# Serverless knowledge catalog management system
## 1. Diagram
Diagram of the proposed architecture for the application:
![AWS services diagram](./img/Assignment2.drawio.png "Services used for this application.")

## 2. API documentation
After deploying the application with AWS CDK (cdk deploy) the console will output the base URL path for interacting with the API. For example, https://exclp8y9a0.execute-api.your-region-2.amazonaws.com/prod/
All the following endpoints are added to this base URL with the corresponding HTTP methods.

<table>
<tr>
GET `/catalog_items `
</tr>
<tr>

(Status: 200)

```json
{
    "count": "2",
    "items": [
        {
            "year": {
                "N": "2025"
            },
            "id": {
                "S": "Midterm exercise@GCA"
            },
            "name": {
                "S": "Midterm exercise"
            },
            "course": {
                "S": "GCA"
            },
            "type": {
                "S": "PDF"
            }
        },
        {
            "year": {
                "N": "2024"
            },
            "id": {
                "S": "Slide deck session 1@Databases"
            },
            "name": {
                "S": "Slide deck session 1"
            },
            "course": {
                "S": "Databases"
            },
            "type": {
                "S": "Powerpoint"
            }
        }
    ]
}

```

</tr>

</table>