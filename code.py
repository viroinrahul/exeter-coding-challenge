import csv
import fileinput
import string
import pandas as pd
import os
import psutil

# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss
  
# decorator function
def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("{}:consumed memory: {:,}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))
        return result
    return wrapper

        
@profile

def func():
    f = open('french_dictionary.csv', 'r')
    reader = csv.reader(f)

    dictionary = {}
    d_count = {}
    
    for row in reader:
        dictionary[row[0]] = row[1]
        d_count[row[0]] = 0
        
    text = open('t8.shakespeare.txt', 'r')
    for line in text:
        line = line.strip()
        words = line.split(" ")
        for word in words:
             if word in d_count:
                    d_count[word] += 1
                    
        
    df = pd.read_csv("wordCounter.csv")
    df['Frequency'] = df['English Word'].map(d_count)
    
    df.to_csv(r'C:\Users\Rahul Sinha\Documents\exeter\frequency.csv', index=False)
    text.close()
    
    for line in fileinput.input('t8.shakespeare.txt', inplace=True):
        line = line.rstrip()
        if not line:
            continue
        for key, value in dictionary.items():
             if key in line:
                    line = line.replace(key,value)
        
        print(line)
              

func()