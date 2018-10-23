package com.csce465.subsolver.controllers;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SubSolverController {
	
	@RequestMapping("/")
	public String test() {
		return "Hello SubSolver!";
	}
	
}
