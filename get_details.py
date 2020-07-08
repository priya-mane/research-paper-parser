from os.path import isfile, join
import re
import json
from os import listdir
import argparse
import os
from tqdm import tqdm


class essential_data:
    """
    Extract essential data from the tex document.
    Essential data includes - title, author, abstract, introduction, conclusions, results, acknowledgments.
    """

    def __init__(self, tex_data):
        self.tex_data = tex_data

    def get_title(self):
        title = re.findall(r'title{(.*?)}', self.tex_data, re.S)
        title = " ".join(title)
        return title

    def get_author(self):
        author = re.findall(r'author{(.*?)}', self.tex_data, re.S)
        author = " ".join(author)
        return author

    def get_abstract(self):
        abstract = re.findall(
            r'\\begin{abstract}(.*?)\\end{abstract}', self.tex_data, re.S)
        abstract = " ".join(abstract)
        return abstract

    def get_introduction(self):
        introduction = re.findall(
            r'\\section{Introduction}(.*?)\\', self.tex_data, re.S)
        introduction = " ".join(introduction)
        return introduction

    def get_conclusions(self):
        conclusions = re.findall(
            r'\\section{Conclusions}(.*?)\\', self.tex_data, re.S)
        conclusions = " ".join(conclusions)
        return conclusions

    def get_results(self):
        results = re.findall(r'\\section{Results}(.*?)\\', self.tex_data, re.S)
        results = " ".join(results)
        return results

    def get_acknowledgments(self):
        acknowledgments = re.findall(
            r'\\acknowledgments(.*?)\\', self.tex_data, re.S)
        acknowledgments = " ".join(acknowledgments)
        return acknowledgments


class clean_data:
    """
    Contains functions to purge all unwanted elements from the tex file.
    """

    def __init__(self, tex_data):
        self.tex_data = tex_data

    def purge_images(self):
        """
        Purges images from the tex data using tag the '\begin{figure}'
        """
        imgs = re.findall(
            r'begin{figure}(.*?)end{figure}', self.tex_data, re.S)
        start = "\\begin{figure}"
        end = "end{figure}"
        imgs = [start + img + end for img in imgs]
        for img in imgs:
            self.tex_data = self.tex_data.replace(img, " ")

    def purge_tables(self):
        """
        Purges tables from the tex data using tag the '\begin{table}'
        """
        tables = re.findall(
            r'begin{table}(.*?)end{table}', self.tex_data, re.S)
        start = "\\begin{table}"
        end = "end{table}"
        tables = [start + table + end for table in tables]
        for table in tables:
            self.tex_data = self.tex_data.replace(table, " ")

    def purge_equations(self):
        """
        Purges equation from the tex data using tag the '\begin{equation}'
        """
        equations = re.findall(
            r'begin{equation}(.*?)end{equation}', self.tex_data, re.S)
        start = "\\begin{equation}"
        end = "end{equation}"
        equations = [start + equation + end for equation in equations]
        for equation in equations:
            self.tex_data = self.tex_data.replace(equation, " ")


# python get_details.py -p ./papers -o op_json.json

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="extract title,author,abstract,introduction,results,conclusions and acknowledgments from given set of research papers.")

    parser.add_argument("-parent", help="enter path to parent directory containing all research papers",
                        dest="parent_path", type=str, required=True)
    parser.add_argument("-output", help="enter path of output file",
                        dest="op", type=str, required=True)

    args = parser.parse_args()
    directory_path = args.parent_path
    op_file = args.op

    all_data = []

    all_files = [f for f in listdir(
        directory_path) if isfile(join(directory_path, f))]

    for tex_file in tqdm(all_files):

        p = os.path.join(directory_path, tex_file)

        data = open(p, encoding='latin-1').read()

        cd = clean_data(data)
        cd.purge_images()
        cd.purge_tables()
        cd.purge_equations()

        ed = essential_data(cd.tex_data)
        title = ed.get_title()
        author = ed.get_author()
        abstract = ed.get_abstract()
        introduction = ed.get_introduction()
        results = ed.get_results()
        conclusions = ed.get_conclusions()
        acknowledgments = ed.get_acknowledgments()

        a_dict = {}
        for variable in ["title", "author", "abstract", "introduction", "results", "conclusions", "acknowledgments"]:
            a_dict[variable] = eval(variable)

        all_data.append(a_dict)

    with open(op_file, "w") as outfile:
        json.dump(all_data, outfile, indent=4)
