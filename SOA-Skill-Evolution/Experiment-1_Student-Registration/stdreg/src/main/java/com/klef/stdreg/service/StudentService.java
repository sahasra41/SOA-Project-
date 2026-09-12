package com.klef.stdreg.service;

import java.util.List;
import com.klef.stdreg.model.Student;

public interface StudentService
{
    public String addStudent(Student student);

    public List<Student> viewAllStudents();
}