## Weak nonce

The original text was recovered using crib-dragging approach. It goes roughly as follows:
- Xor two lines from the encoded text. You will get a string that contains a result of a xor operation between two original texts in those lines.
I used lines 2 and 4 (0-based indexing).
- Try guessing words in one of the lines by xoring them with some common English words. I used ` you`. This way you'll be able to recover a small
part of the text from the other line. If you are stuck, try xoring one of the lines with some other line of encoded text.
- Sooner or later you'll find a more or less readable piece of text. At this point, you can just use Google to find the original text.
- Now, you need to find the largest line in the encoded text and xor it with the corresponding line of a plaintext - you'll get an OTP string used to encrypt the text.
- Use that OTP string to decrypt the whole thing.
