package com.csce465.subsolver.controllers;

import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

import com.csce465.subsolver.domain.Ciphertext;
import com.csce465.subsolver.utils.Analyzer;

@Controller
public class SubSolverController {
	
	@GetMapping("/home")
	public String home(Model model) {
		model.addAttribute("ciphertext", new Ciphertext());
		return "home";
	}
	
	@PostMapping("/home")
	public String homeSubmit(@ModelAttribute Ciphertext ciphertext, Model model) {
		Map<Character, Integer> letterFreqs = Analyzer.getLetterFrequencies(ciphertext.getContent());
		return "home";
	}
	
}
