import pysubs2

test_file = "test/Laura Speech Final SMALL.srt"

subs = pysubs2.load(test_file)



for sub in subs:
    print(f"{sub.duration}")