## TLS protection

What's implemented:
- The application uses TLSv1.2 since there is no support for TLSv1.3 in Python and earlier versions of the protocol
are considered insecure. TLSv1.3 is also less adopted than TLSv1.2
- Ciphersuits are chosen based on the recommendation from OWASP[1]. They have been cross-checked with the ciphersuits supported by
my notebook using `openssl ciphers -V <ciphersuit>`. Additional, some of the insecure ciphersuites have been disabled (`!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!DSS:!RC4:!SEED:!ECDSA:!ADH:!IDEA:!3DES`)
- Parameters for Diffie-Hellman are pregenerated in advance using the command `openssl dhparam -out dhparams.pem 4096`.
- Self-signed certificate is created using `openssreq -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`.
- Both the certificate and the private key are stored locally.

What's left out of scope:
- It is a good idea to use reverse proxy (e.g. nginx) with certbot. There are tutorials online (e.g. by DigitalOcean) that simplify this process.
- Some CA should be used to create certificates (e.g. LetsEncrypt).
- Access to certificate and private key files should be restricted. Certbot handles this automatically.

[1]: https://cheatsheetseries.owasp.org/cheatsheets/TLS_Cipher_String_Cheat_Sheet.html
