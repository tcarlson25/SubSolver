package com.csce465.subsolver;

import java.util.Map;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import com.csce465.subsolver.utils.Analyzer;

@RunWith(SpringRunner.class)
@SpringBootTest
public class SubsolverApplicationTests {

	@Test
	public void contextLoads() {
		Map<Character, Integer> map = Analyzer.getLetterFrequencies("hello. my name is Tyler!");
		System.out.println(map);
	}

}
