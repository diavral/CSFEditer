## CSFEditer
C&amp;C RA2 ra2(md).csf file editer in python.
### 
Decode bytes of a \*.csf file or encode data to bytes of \*.csf file.
#### Readme
This is when I tried to batch edit the CSF file of RA2,
I found that there was no suitable software, so I wrote one myself,
but I did not learn PyQt/PySide a lot, and some functions could not be implemented.
I don't have time for this at the moment.In the test.py file are transcoding and decoding functions.\[translated]
#### To figure out (in reference link)
Decoding the value

To decode the value to a Unicode string, not every byte of the value data (or subtract it from 0xFF).
An example in C++:
```c++
int ValueDataLength = ValueLength << 1;
for(int i = 0; i < ValueDataLength; ++i) {
  ValueData[i] = ~ValueData[i];
}
```
I'm not sure what the 'not every byte of the value data' means.

[Reference link](https://modenc.renegadeprojects.com/CSF_File_Format)<-

~~**现成的软件不好用.好用的软件写不出.**~~
