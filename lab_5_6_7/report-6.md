## Encrypting sensitive data

What's implemented:
- Envelope encryption is used: data is encrypted with data encryption key (DEK) and DEK is encrypted with key encryption key (KEK).
- AES256-GCM is used to encrypt both the data and the DEK. It is used based on the recommendation from OWASP. Also, this mode
effectively turns a block cipher into a stream cipher which suits us well since our sensitive data can have arbitrary length.
- KEK is stored in a separate file unencrypted.
- DEK and its nonce is stored with data and its nonce in the same table.
- Both DEK and KEK are generated using a CSPRNG (32 bytes).
- New DEK is generated every time new data is written to the database. This is motivated by the recommendation from [1].
- Every user has a separate DEK.

What's left out of scope:
- KEK should be stored in some key management system (KMS) from cloud provider. This way the attacker won't be able to
access KEK even if he has access to the server's filesystem.
- Key rotation should be implemented. This is particularly true for KEK since it doesn't change in the current setting at all.
It is less of an issue with DEKs since they are changed every time we write to the database but it is still might be worthwhile
to implement rotation if the sensitive data remains unmodified for long periods of time.
- DEKs should not be stored together with the data. This guarantees that an attacker won't have access to the DEKs even if the DB
containing sensitive data is compromised.

[1]: https://cloud.google.com/kms/docs/envelope-encryption
