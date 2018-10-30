package com.csce465.subsolver.utils;

import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.stream.Collectors;

public class Analyzer {

	/**
	 * Get letter frequencies given a input string
	 * @param input
	 * @return
	 */
	public static Map<Character, Integer> getLetterFrequencies(String input) {
		input = input.toLowerCase();
		Map<Character, Integer> letterToCountMap = new HashMap<>();
		for (char ch = 'a'; ch <= 'z'; ++ch) {
			letterToCountMap.put(ch, 0); 
		}
		for (int i = 0; i < input.length(); i++) {
		    char c = input.charAt(i);
		    Integer val = letterToCountMap.get(c);
		    if (val != null) {
		    		letterToCountMap.put(c, new Integer(val + 1));
		    }
		}
		return sortByValue(letterToCountMap);
	}

	/**
	 * Sort a map by value in descending order
	 * @param wordCounts
	 * @return
	 */
	public static Map<Character, Integer> sortByValue(final Map<Character, Integer> wordCounts) {
        return wordCounts.entrySet()
                .stream()
                .sorted((Map.Entry.<Character, Integer>comparingByValue().reversed()))
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new));
    }
	
}
