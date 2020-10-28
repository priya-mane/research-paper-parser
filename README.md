# Research paper parser

[Parser Google Colaboratory Link](https://colab.research.google.com/drive/1gfhYRtO6OKQbVAAiMdmo_r54N2r6xmT7?usp=sharing)

The script reads latex files for research paper from the given directory and extracts essential information from the latex format.

The script purges unwanted items like -
* Images
* Tables
* Equations

The script returns a json object containing following items for each research paper - 
* Title
* Author
* Abstract
* Introduction
* Conclusions
* Results
* Acknowledgments

***

## Run the script using the following command

```
python get_details.py -p <directory_containing_papers> -o <output_file_path>
```

Example :

```
python get_details.py -p ./papers -o op_json.json
```

![Output](results/Capture.JPG)

<h3 align="center"><b>Developed with :heart: by <a href="https://github.com/priya-mane">Priya Mane </a> & <a href="https://github.com/pratik6725"> Pratik Merchant</a>.</b></h1>
