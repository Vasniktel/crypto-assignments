openssl dhparam -out dhparams.pem 4096  # create parameters for Diffie-Hellman in advance
openssreq -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365  # create self-signed certificates
