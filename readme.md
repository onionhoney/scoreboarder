# API Design

Each App owner will register a *service* with us. 
Then the owner can open a new category 
(for instance, single, avg 5, or 3*3 puzzle). 
Then the owner can add in new users. 
Finally, for each (service, category, user) tuple, 
the owner can upload an encrypted JSON result. 

## To register a service:
/register/s POST

This will return a secret key used to encrypt. Keep this a secret!

## To register a category:
/register/s/{service-id}/c/ POST

## To register a user:
/register/s/{service-id}/u/ POST

## To upload result:

/s/{service-id}/c/{cat-id}/user/{username} POST

The service-id and cat-id and username must exist. 
The posted message is built like this:

1. Create a JSON
{ date: string, result: float, detail: string }
You can pick what to put in detail, but the total size must be < 1K. 

2. Use RSA encryption to encrypt to JSON 

3. Put the encrypted blob in request body. 

The App should hide the details about the encryption as much as possible. 

## To get result:

/s/.../c/.../result/all
/s/.../c/.../result/10
/s/.../c/.../result/from/{time}/to{time}/10


** The suggested layout of Detail (JSON) **
[
    { scramble: "1 2 3 4 5 ... 15 /" , 
      solution: [], 
      keystroke_time: [], 
    }
]


# How to Run the Project
- create_db.py to create the schema
- mock_db.py to test out SQL 


