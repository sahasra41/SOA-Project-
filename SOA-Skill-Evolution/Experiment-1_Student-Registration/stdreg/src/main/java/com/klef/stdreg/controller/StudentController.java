package com.klef.stdreg.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import com.klef.stdreg.model.Student;
import com.klef.stdreg.service.StudentService;

@Controller
public class StudentController
{

    @Autowired
    private StudentService studentService;

    @GetMapping("/studentform")
    public String studentForm()
    {
        return "studentform";
    }

    @PostMapping("/savestudent")
    public String saveStudent(Student student)
    {
        studentService.addStudent(student);
        return "success";
    }

    @GetMapping("/viewstudents")
    public String viewStudents(Model model)
    {
        List<Student> studentList = studentService.viewAllStudents();

        model.addAttribute("studentList", studentList);

        return "viewstudents";
    }

}