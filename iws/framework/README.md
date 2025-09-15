# Framework

---



# Headers

---

## Request Headers


## Response Headers

- Content-Type

It’s important to always set the correct ```Content-Type``` header on your response.
If you send ```JSON```, then set Content-Type to ```application/json```. If ```XML```, then set it to ```application/xml```. 
This header tells the user how they should parse the data.


## Request Types

---

### POST

201 Created status code to tell the user that a new resource was created. Make sure to use 201 Created instead of 200 OK for all successful POST requests.


### DELETE

This response only includes the status code ```204 No Content```. 
This status code tells a user that the operation was successful, but no content was returned in the response.
This makes sense since the resource has been deleted. There’s no reason to send a copy of it back in the response.



**Note**:

It’s important to always send back a copy of a resource when a user creates it with ```POST``` or modifies it with ```PUT``` or ```PATCH```. 
This way, the user can see the changes that they’ve made.



## Error Responses

---





# Author

---

- Rohtash Lakra
