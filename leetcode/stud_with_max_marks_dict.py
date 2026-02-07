# print the students with maximum marks
marks={"sanjay":100 , "sam":90, "ram":100 , "ajay":80, "som":100}
max_marks= max(marks.values())
stud_with_max_marks = [k for k , v in marks.items() if v == max_marks]
print(stud_with_max_marks)

# {'abc': 3, 'bca': 3, 'cab': 3, 'bc': 2, 'cb': 2, 'b': 1}