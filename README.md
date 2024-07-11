# GROCERY-STORE-CLONE
It is a multi-user app (one required admin/store manager and other
users). Used for buying grocery. User can buy many products for one or
multiple sections. Store manager can add section/category and products



## -Technologies used
- Login Framework used for User >> flask_login, wtforms, flask_bcrypt for encryption.
- Application code >> Flask
- Webpages >> Jinja2 templates + Bootstrap for HTML generation and styling
- SQLite for data storage

## DB Schema Design

<img width="880" alt="Screenshot 2024-07-11 at 2 07 29 PM" src="https://github.com/utkarsh-vashistha/GROCERY-STORE-CLONE/assets/96648073/ef00a67c-f2de-4be6-a06a-774f02c98672">



<img width="708" alt="Screenshot 2024-07-11 at 2 09 35 PM" src="https://github.com/utkarsh-vashistha/GROCERY-STORE-CLONE/assets/96648073/34d7e053-1189-43ca-88bb-0f4f19ca9752">

All relations and database table helps to reduce redundancy clutter and simplify data
retrieval and storage. For admin no records are being kept nor the login frame work is being
used.


## CRUD

### -Create: This operation involves adding new data to a database. It's the
process of inserting a new record or entry into a database table. For
example, adding a new user to a user database, creating a new product
in an e-commerce system, or adding a new post to a blog.

### -Read: Reading refers to retrieving existing data from a database. This
operation involves querying the database to fetch specific records or
information. It's used to display, retrieve, or process data. For example,
fetching a user's profile information, displaying a list of products, or
showing comments on a blog post.

### -Update: This operation involves modifying existing data in the database.
It's used when you need to change the values of one or more fields in a
record. For example, updating a user's email address, changing the price
of a product, or editing the content of a blog post.

### -Delete: Deleting refers to removing data from the database. This
operation is used to permanently remove a record from the database
table. For example, removing a user account, deleting a product that's no
longer available, or deleting comments from a post.
