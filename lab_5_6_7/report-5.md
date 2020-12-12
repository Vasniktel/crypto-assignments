We will use Flask framework to create a server and a bcrypt algorithm to hash passwords. Flask doesn't have any builtin security features, although there are some extensions that provide that. Bcrypt was chosen because of the recommendation on OWASP. It uses a 12 work factor and a salt, generated with Python's CSPRNG. We also make sure the password satisfies some simple requirements, suggested on OWASP:

- Length of the password is in range [8; 64]. The reason for these boundaries is that 8 is small enough to be remembered by a human but still provides a strong password[1] and 64 prevents long password DoS attack (also, bcrypt supports messages up to 72 characters long).
- The password must have at least one lowercase letter, uppercase letter, number and a punctuation symbol.
- We also use a Pony ORM to work with the database. Its implementation is safe from SQL injections.

Additionally, our database only accepts connections from a single endpoint (localhost in this case) which prohibits remote access to the data from unauthorized IPs.

[1]: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html