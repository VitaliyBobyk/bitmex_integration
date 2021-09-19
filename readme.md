# **_`Hi!`_**

## **This is description for project**

> Useful commands:
> - make run - Build and run everything
> - make test - Test API Gateway
> - make create_admin - Create superuser


> Requirements:
> - Docker

> API Gateway Description:
> - http://127.0.0.1:8000/swagger/ 
> >  There is full documentation for API

> WS Gateway Description
> 
> - In each subscribe/unsubscribe request after connecting to socket need to provide next fields in body of request: 
```

{
    "account": "Account name",
    "symbol":"Instrument f.e(XRPUSD)",
    "action":"subscribe/unsubscribe"
}
````

