package com.csce465.subsolver.controllers;

import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class SubSolverController {
	
	@RequestMapping("/")
	public String home(Map<String, Object> model) {
		model.put("message", "Welcome Screen!");
		return "home";
	}
	
}
