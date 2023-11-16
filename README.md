# Web-Phone-shop
A website for an imaginary phone shop.

There are three pages available to customers, and one admin page. Customers can send orders. On the admin page, we can see these orders along with the customer's contact info. We can delete contacts and start/end a sale.

There are some APIs to handle GET, POST, and DELETE requests, all implemented in JavaScript. 

The server is written in Python. It handles the requests, and responds with the requested files. It handles the URL parsing, and the POST request body, and ensures the data received is mostly accurate.

Not implemented in this version:
- Starting a sale doesn't give any discounts on the items.
