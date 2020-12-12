## Password generator

#### Part 1

Implementation details:
- Passwords are generated with the following distribution:
  - Selected from top 100 passwords - 5%
  - Selected from top 1M passwords - 80%
  - Generated at random - 5%
  - Generated at random in human-like form - 10%
- Generation at random produces a sequence of characters randomly selected from the set of all ASCII letters, digits and `!?` symbols. Size of the sequence is randomly selected to be in the range [5; 10]
- Generation in human-like form uses a dictionary of common English words to include in the password. It also chooses with 50% probability whether to:
  - Prepend numbers - size of the prepended sequence is chosen at random between 3 and 5 inclusively.
  - Append numbers - size of the appended sequence is chosen at random between 2 and 4 inclusively.
  - Replace symbols (e.g. `s` to `$`) - only some of the symbols are replaced if this option is chosen.
- Generated passwords are hashed with the following algorithms:
  - MD5
  - SHA1
  - SHA256
  - bcrypt with cost 4


#### Part 2

Implementation details:
- Hashed passwords are provided in https://github.com/alexandr-gnrk/human_passwords
- A simple dictionary lookup was used to find passwords, ecrypted with SHA1(salted) and MD5. In case of MD5, a dictionary of 1M most common passwords was used.
As a result, 32.44% of passwords were recovered in 7.6 s. In case of SHA1, size of the dictionary is 100 passwords and only 0.06% is recovered in 1min 41s. In both cases,
the whole procedure was parallelized into 4 processes.
- An simple implementation of a rainbow table is also provided. However, I didn't manage to recover any passwords using this approach since the size of the table is pretty small.
It is, of course, possible to create bigger tables but in that case it takes a lot of time to generate them and recover hashed passwords. We could use GPU or OpenCL to fix the time problem
but that would be an overkill for this assignment.
- As a result, using salt significantly complicates the brute-force attack. Also, it seems that SHA1 is slower than MD5 which is a good thing from the security point of view. Thus, it is
better to use bcrypt to hash passwords since it allows one to choose the time it takes for the algorithm to hash the data (bcrypt's cost) and it uses nonce.
As for the restrictions on passwords, it is better to ensure the password consists of ASCII letter, digits and punctuation. Characters in the password should be randomly generated (ideally).
The password should be at least 8 characters long.
