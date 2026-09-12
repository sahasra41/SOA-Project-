package com.klef.stdreg.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.klef.stdreg.model.Student;
import com.klef.stdreg.repository.StudentRepository;

@Service
public class StudentServiceImpl implements StudentService
{

    @Autowired
    private StudentRepository studentRepository;

    @Override
    public String addStudent(Student student)
    {
        studentRepository.save(student);
        return "Student Registered Successfully";
    }

    @Override
    public List<Student> viewAllStudents()
    {
        return studentRepository.findAll();
    }

}