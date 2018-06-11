# OpenRelex : A Path Based Open Relation Extractor

OpenRelex (ping me if you have a better name) is a path based, open domain relation extractor out of the sentences.
This is the first version of the code, and it is still not fine tuned, but works out fine. The users can fine tune it  according to their needs.
Apart from this, there is Stanford OpenIE, however it was giving me redundant relations hence I decided to build my own relation extractor.
If you want to reach out, email me at akashsarda3@gmail.com!

Currently I have hardcoded the file "larry" in front.py, but however you can use it as a imported class in your code  like

```sh
from postprocessing import PostProcessor
a = PostProcessor()
a.information("After enrolling in a computer science PhD program at Stanford University, Page was in search of a dissertation theme and considered exploring the mathematical properties of the World Wide Web.")
```

If you just want to see it's output, paste your paragraph in a file, and then:
```sh
$ python3 front.py <filename>
```
Currently can not handle text in quotation marks in the sentence, as the dependancy parser gives funny results on that. Will be very glad if someone happens to perform coreferencing with this.
