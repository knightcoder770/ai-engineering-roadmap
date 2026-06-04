student_data={}

def student_marks(student_id):
    while True:    
        try:
            no_of_subjects=int(input("enter the no of subjects: "))
        except ValueError:
            print("enter only numbers")
            continue
        marks={}
        for i in range(0,no_of_subjects):
            subject=input("enter the name of subject: ")
            while True:    
                try:
                    mark=int(input(f"enter mark of {subject}: "))
                    break
                except ValueError:
                    print("mark must be in integer")
                    continue
            marks[subject]=mark
        return marks
  
def add_student():
    student_id=input("enter the student id: ")
    name=input("enter the student name: ")
    while True:
        try:
            age=int(input("enter the age of the student: "))
            break           
        except ValueError:
            print("age should be only numbers")
            continue
    marks_given=student_marks(student_id)    
    student_data[student_id]={"name":name,"age":age,"marks":marks_given}
    print("student added sucessfully")       
                                                                                                                                  
def remove_student():      
    student_id=input("enter the student id you want to remove : ")
    if student_id in student_data:
        del student_data[student_id]
        print("student data deleted sucessfully")
    else:
        print("the student id is not available in database to delete")

def edit_student():   
    student_id=input("enter student id that needs to be edited")   
    if student_id in student_data:   
        name=input("enter name or leave blank to keep it unchanged : ")            
        try:
            age=int(input("enter age or leave blank to keep it unchanged : "))
        except ValueError:
            print("only type numbers for age")            
        marks=input("do you want to change marks? or leave blank to keep it unchanged : ")
        if name:
            student_data[student_id]['name']=name 
        if age:
            student_data[student_id]['age']=age 
        if marks:
            student_data[student_id]['marks']=student_marks(student_id)
        print("student details editted successfully")
    else:
        print("student id is not found in the data base")

def view_student():
    student_id=input("enter the student id of the person you want to view: ")
    if student_id in student_data:
        student_info=student_data[student_id]
        print(f"name:{student_info['name']}")
        print(f"age:{student_info['age']}")
        print(f"marks:{student_info['marks']}")
        avg_marks=average_marks(student_id)
        result_grade=grade(avg_marks)
        print(result_grade)
    else:
        print("student id is not in data base")

def average_marks(student_id):
    if student_id in student_data:
        marks_dict=student_data[student_id]['marks']
        if not marks_dict:
            print("no marks id found for this student")
        total_mark=sum(marks_dict.values())
        total_subjects=len(marks_dict)
        average=total_mark/total_subjects
        return average
    
def grade(avg_marks):
    if avg_marks>=85:
        return "you got A grade"
    if 70<=avg_marks<85:
        return "you got B grade"
    if 50<=avg_marks<70:
        return "you got C grade"
    else:
        return "you got failed overall"

def main():    
    while True:
        print('*'*70)
        print("choose the option below to add and enter the marks of student")
        print('*'*70)
        print("1-add student\n2-remove student\n3-view student\n4-edit student\n5-exit")
        while True:   
            try:
                option=int(input("choose the option no you want to do :"))
                if option in range(1,6):
                    break
                else:
                    print("you must choose the option between [1-5]")
                    continue
            except ValueError:
                print("you should only type the option number")
                continue
        if option==1:
            add_student()
        elif option==2:
            remove_student()
        elif option==3:
            view_student()
        elif option==4:
            edit_student() 
        else:
            break

if __name__ == "__main__":
    main()